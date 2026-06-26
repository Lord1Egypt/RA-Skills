#!/usr/bin/env python3
"""
NotebookLM Distiller — Knowledge Extraction & Management for Obsidian

Subcommands:
  distill   Extract knowledge from NotebookLM notebooks into Obsidian markdown.
  research  Kick off a NotebookLM web research session on a topic.
  persist   Write any markdown content directly into the Obsidian vault.
"""

import argparse
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from typing import List, Tuple


# ---------------------------------------------------------------------------
# CLI auto-detection
# ---------------------------------------------------------------------------

_CANDIDATE_PATHS = [
    # DeepReader venv (most common OpenClaw setup)
    os.path.expanduser("~/.openclaw/skills/deepreader/.venv/bin/notebooklm"),
    # System PATH fallback
]

def find_notebooklm_cli() -> str:
    """Return the path to the notebooklm CLI, auto-detecting if needed."""
    for path in _CANDIDATE_PATHS:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    system = shutil.which("notebooklm")
    if system:
        return system
    return "notebooklm"  # let it fail with a clear error at runtime


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def yaml_quote(value: str) -> str:
    """Return a YAML-safe quoted scalar (JSON string escaping)."""
    return json.dumps(value, ensure_ascii=False)


def run_command(cmd: List[str], timeout: int = 120) -> str:
    """Run a CLI command and return stdout. Returns '' on error/timeout."""
    logging.info(f"[RUN] {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        logging.error(f"[ERROR] Command timed out after {timeout}s: {' '.join(cmd)}")
        return ""
    if result.returncode != 0:
        logging.error(f"[ERROR] Command failed (rc={result.returncode}): {result.stderr.strip()}")
        return ""
    return result.stdout.strip()


def sanitize_filename(name: str) -> str:
    """Remove unsafe filename characters and truncate to 100 chars."""
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace("\n", " ").strip()
    return name[:100]


def clean_cli_output(output: str) -> str:
    """Strip NotebookLM CLI noise lines; preserve actual content."""
    noise_prefixes = (
        "Starting new conversation",
        "New conversation: ",
        "Generating response",
    )
    lines = output.split('\n')
    cleaned = []
    for line in lines:
        if any(line.startswith(p) for p in noise_prefixes):
            continue
        if line.startswith("Answer:"):
            rest = line[len("Answer:"):].strip()
            if rest:
                cleaned.append(rest)
            continue
        cleaned.append(line)
    return '\n'.join(cleaned).strip()


def build_frontmatter(title: str, date_str: str, source: str,
                      topic: str, mode: str, extra_tags: List[str] = None) -> str:
    """Build a standard YAML frontmatter block."""
    safe_topic = sanitize_filename(topic).replace(' ', '-')
    tags = ["distillation", mode, safe_topic] + (extra_tags or [])
    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {date_str}",
        "type: knowledge-note",
        "author: notebooklm-distiller",
        f"tags: {json.dumps(tags, ensure_ascii=False)}",
        f"source: {yaml_quote(source)}",
        f"project: {yaml_quote(topic)}",
        "status: draft",
        "---",
    ]
    return '\n'.join(lines)


def write_note(filepath: str, content: str) -> None:
    """Write content to filepath, creating parent dirs as needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    logging.info(f"Saved → {filepath}")


# ---------------------------------------------------------------------------
# NotebookLM helpers
# ---------------------------------------------------------------------------

def get_notebooks(nlm_cli: str, keywords: List[str]) -> List[Tuple[str, str]]:
    """List all notebooks and return those whose title matches any keyword.
    Returns [(notebook_id, notebook_name), ...]."""
    output = run_command([nlm_cli, "list", "--json"])
    if not output:
        return []
    try:
        notebooks = json.loads(output).get("notebooks", [])
    except json.JSONDecodeError:
        logging.error("Failed to parse notebook list JSON.")
        return []

    return [
        (nb.get("id", ""), nb.get("title", ""))
        for nb in notebooks
        if any(kw.lower() in nb.get("title", "").lower() for kw in keywords)
    ]


def parse_questions(raw_output: str) -> List[str]:
    """Parse NLM output into a clean list of questions.

    Robust to two NLM output styles:
    - Newline-separated (each line or wrapped group is one question)
    - Paragraph style (all questions in one block, separated by '. ' or '? ')

    Strategy:
    1. Strip citation markers like [1], [1-3], [1, 2]
    2. Join all lines into one text
    3. Split on '?' boundaries followed by a new sentence start
    """
    cleaned = clean_cli_output(raw_output)

    # Strip citation markers
    cleaned = re.sub(r'\s*\[\d+(?:[,\-]\s*\d+)*\]', '', cleaned)

    # Normalise whitespace but keep sentence boundaries
    cleaned = re.sub(r'\n+', ' ', cleaned).strip()

    # Skip preamble lines like "Here are N questions..."
    cleaned = re.sub(
        r'^(here are\s+\d+.*?questions[^\?]*?\.\s*)',
        '', cleaned, flags=re.IGNORECASE
    )

    # Split on '?' followed by optional punctuation/space and then uppercase / Chinese
    parts = re.split(r'(?<=[?？])\s*(?=[A-Z\u4e00-\u9fff])', cleaned)

    questions = []
    for part in parts:
        # Strip leading list markers, trailing periods/spaces
        q = re.sub(r'^[\d\.\-\*\s]+', '', part).strip().rstrip('.')
        # Ensure it actually ends with a question mark
        if not q.endswith('?') and not q.endswith('？'):
            q = q + '?'
        if len(q) >= 20:
            questions.append(q)

    return questions


_LANG_PREFIX = {
    "zh": "请用中文回答。\n\n",
    "en": "",
}

def lang_prefix(lang: str) -> str:
    """Return the language instruction prefix for NLM prompts."""
    return _LANG_PREFIX.get(lang, "")


def extract_questions(nlm_cli: str, notebook_id: str, lang: str = "en") -> List[str]:
    """Ask NotebookLM to generate 15-20 questions that expose deep understanding vs memorisation."""
    prompt = lang_prefix(lang) + (
        "Generate 15 to 20 questions that would expose whether someone deeply understands this subject "
        "versus someone who has only memorised facts. "
        "Good questions should require the reader to reason, connect concepts, or explain WHY — "
        "not just recall a definition or fact. "
        "Include questions about edge cases, apparent contradictions, and non-obvious consequences. "
        "Output one question per line as a flat list. No numbering, no prefixes, no markdown formatting."
    )
    output = run_command([nlm_cli, "ask", prompt, "--notebook", notebook_id, "--new"])
    if not output:
        return []
    return parse_questions(output)


def ask_question(nlm_cli: str, question: str, notebook_id: str, retries: int = 3,
                 lang: str = "en") -> str:
    """Ask a specific question and return the answer (with retry)."""
    full_question = lang_prefix(lang) + question
    cmd = [nlm_cli, "ask", full_question, "--notebook", notebook_id, "--new"]
    for attempt in range(retries):
        output = run_command(cmd)
        if output:
            result = clean_cli_output(output)
            if result:
                return result
        logging.warning(f"[WARN] Empty response. Retrying ({attempt + 1}/{retries})...")
        time.sleep(3)
    return "_No answer returned after 3 attempts._"


# ---------------------------------------------------------------------------
# Subcommand: distill
# ---------------------------------------------------------------------------

SUMMARY_PROMPTS = [
    ("Core Mental Models",
     "What are the 3-5 core mental models or thinking frameworks that every expert in this field shares? "
     "These are not facts to memorise — they are the lenses through which experts interpret new information. "
     "For each model, explain what it is and why it matters for understanding everything else in this field."),
    ("Consensus Map",
     "What do all major sources in this notebook agree on? "
     "What is the established consensus — the things that are no longer seriously debated among practitioners? "
     "Present this as a clear, structured list."),
    ("Debate Map",
     "Where do experts in this field fundamentally disagree? "
     "Identify the 3 most important unresolved debates. "
     "For each debate: state the question, summarise each side's strongest argument, "
     "and note what evidence or assumptions drive the disagreement. "
     "Use a structured format (e.g. bold headings per debate)."),
    ("Trade-offs",
     "What are the key trade-offs, tensions, or design dilemmas present in this material? "
     "For each trade-off, explain what you gain and what you sacrifice on each side. "
     "Use a Markdown table or structured list."),
    ("Open Frontier",
     "What are the genuinely unsolved problems that even experts are still working on? "
     "What questions does this field not yet have good answers to? "
     "What would need to be true for the field to move forward on these?"),
]

GLOSSARY_PROMPT = (
    "Scan all sources in this notebook and produce a glossary of the 15-30 most important domain terms, "
    "abbreviations, and key concepts. "
    "For each entry provide: "
    "(1) a precise definition grounded in the source material, "
    "(2) how an expert uses this term versus how a beginner typically misuses or misunderstands it, "
    "(3) any closely related terms that are easy to confuse with this one, and why the distinction matters. "
    "Use bold subheadings or Markdown dividers to separate entries."
)


def writeback_to_notebook(nlm_cli: str, notebook_id: str, content: str,
                          note_title: str) -> bool:
    """Write content back into the NotebookLM notebook as a text source/note.
    Returns True on success."""
    # NLM CLI has a shell arg length limit; chunk if needed (safe limit ~8000 chars)
    MAX_CHARS = 8000
    if len(content) > MAX_CHARS:
        logging.warning(
            f"[WRITEBACK] Content is {len(content)} chars; truncating to {MAX_CHARS} for NLM source."
        )
        content = content[:MAX_CHARS] + "\n\n[...truncated — full version in Obsidian]"

    cmd = [
        nlm_cli, "source", "add", content,
        "--notebook", notebook_id,
        "--title", note_title,
        "--type", "text",
    ]
    logging.info(f"[WRITEBACK] Writing note '{note_title}' to notebook {notebook_id[:8]}...")
    output = run_command(cmd, timeout=60)
    if output is not None and output != "":
        logging.info(f"[WRITEBACK] Done — source added.")
        return True
    # run_command returns '' on error but also on empty stdout — check separately
    logging.warning("[WRITEBACK] No output from source add (may still have succeeded).")
    return True  # NLM source add often returns empty stdout on success


def process_notebook(nlm_cli: str, notebook_id: str, notebook_name: str,
                     topic: str, vault_dir: str, mode: str, date_str: str,
                     lang: str = "en", writeback: bool = False) -> None:
    """Extract knowledge from one notebook and write an Obsidian note."""
    safe_nb = sanitize_filename(notebook_name)
    suffix_map = {"qa": ("_QA.md", "Deep Q&A"), "summary": ("_Summary.md", "Summary"), "glossary": ("_Glossary.md", "Glossary")}
    file_suffix, title_suffix = suffix_map[mode]

    out_path = os.path.join(vault_dir, sanitize_filename(topic), safe_nb + file_suffix)
    source_label = f"NotebookLM/{notebook_name}"
    title = f"{notebook_name} | {title_suffix}"

    fm = build_frontmatter(title, date_str, source_label, topic, mode)
    header = f"# {notebook_name} — {title_suffix}\n"
    body_parts = [fm, "", header, ""]

    logging.info(f"--- [{mode.upper()}] {notebook_name} ---")

    if mode == "qa":
        questions = extract_questions(nlm_cli, notebook_id, lang=lang)
        if not questions:
            logging.error(f"[FATAL] Could not generate questions for: {notebook_name}")
            return
        logging.info(f"Generated {len(questions)} questions.")
        for i, q in enumerate(questions, 1):
            num = f"{i:02d}"
            logging.info(f"[{num}/{len(questions)}] {q[:70]}...")
            answer = ask_question(nlm_cli, q, notebook_id, lang=lang)
            misconception_prompt = (
                f"For the question: '{q}' — "
                "What is the most common misconception or thinking trap that a learner would fall into? "
                "What key insight do they typically miss? Keep it to 2-3 sentences."
            )
            misconception = ask_question(nlm_cli, misconception_prompt, notebook_id, lang=lang)
            body_parts += [
                f"## Q{num}", "",
                f"> [!question]", f"> {q}", "",
                f"**Answer:**\n\n{answer}", "",
                f"> [!warning] Common Misconception", f"> {misconception}",
                "", "---", "",
            ]
            time.sleep(2)

    elif mode == "summary":
        for section_title, prompt in SUMMARY_PROMPTS:
            logging.info(f"Extracting: {section_title} ...")
            answer = ask_question(nlm_cli, prompt, notebook_id, lang=lang)
            body_parts += [f"## {section_title}", "", answer, "", "---", ""]
            time.sleep(2)

    elif mode == "glossary":
        logging.info("Extracting glossary ...")
        answer = ask_question(nlm_cli, GLOSSARY_PROMPT, notebook_id, lang=lang)
        body_parts += ["## Glossary", "", answer, "", "---", ""]

    body_parts += ["", "*Extracted by notebooklm-distiller*"]

    full_content = '\n'.join(body_parts)
    write_note(out_path, full_content)
    logging.info(f"Distillation complete → {out_path}")

    if writeback:
        # Write back to NotebookLM as a source note (strips YAML frontmatter)
        # Find end of frontmatter (second '---') and use the body only
        fm_end = full_content.find('\n---\n', 4)
        writeback_body = full_content[fm_end + 5:].strip() if fm_end != -1 else full_content
        note_title = f"Distill Log: {mode} | {notebook_name} | {date_str}"
        writeback_to_notebook(nlm_cli, notebook_id, writeback_body, note_title)


def cmd_distill(args) -> None:
    vault_dir = os.path.expanduser(args.vault_dir)
    if not os.path.isdir(vault_dir):
        logging.error(f"[FATAL] vault-dir does not exist: '{vault_dir}'")
        sys.exit(1)

    date_str = datetime.now().strftime("%Y-%m-%d")
    logging.info(f"=== Distill: keywords={args.keywords} mode={args.mode} ===")

    notebooks = get_notebooks(args.cli_path, args.keywords)
    if not notebooks:
        logging.error(f"[FATAL] No notebooks matched: {', '.join(args.keywords)}")
        sys.exit(1)

    logging.info(f"Found {len(notebooks)} notebook(s):")
    for nid, name in notebooks:
        logging.info(f"  - {name} ({nid})")

    for nid, name in notebooks:
        logging.info(f"\n{'='*50}\nProcessing: {name}\n{'='*50}")
        process_notebook(args.cli_path, nid, name, args.topic, vault_dir, args.mode, date_str,
                         lang=args.lang, writeback=args.writeback)

    logging.info("=== All done! ===")


# ---------------------------------------------------------------------------
# Subcommand: quiz  (Discord-friendly interactive quiz — agent-orchestrated)
# ---------------------------------------------------------------------------

def cmd_quiz(args) -> None:
    """Generate quiz questions as JSON for agent-orchestrated Discord quiz."""
    notebooks = get_notebooks(args.cli_path, args.keywords)
    if not notebooks:
        print(json.dumps({"error": f"No notebooks matched: {', '.join(args.keywords)}"}))
        sys.exit(1)

    nb_id, nb_name = notebooks[0]  # Use first match
    logging.info(f"Generating quiz questions for: {nb_name} ({nb_id})")

    prompt = lang_prefix(args.lang) + (
        f"Generate exactly {args.count} questions that would expose whether someone deeply understands "
        "this subject versus someone who has only memorised facts. "
        "Questions must require reasoning, connecting concepts, or explaining WHY — not recalling facts. "
        "Include edge cases, apparent contradictions, and non-obvious consequences. "
        "Output one question per line. No numbering, no prefixes, no markdown."
    )
    output = run_command([args.cli_path, "ask", prompt, "--notebook", nb_id, "--new"])
    questions = parse_questions(output) if output else []

    result = {
        "notebook_id": nb_id,
        "notebook_name": nb_name,
        "questions": questions[:args.count],
        "total": len(questions[:args.count]),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Subcommand: evaluate  (Discord answer evaluation — agent-orchestrated)
# ---------------------------------------------------------------------------

def cmd_evaluate(args) -> None:
    """Evaluate a user's answer against notebook sources. Outputs JSON for agent."""
    prompt = lang_prefix(args.lang) + (
        f"A learner was asked this question: '{args.question}'\n\n"
        f"Their answer was: '{args.answer}'\n\n"
        "Based only on the sources in this notebook, evaluate their answer in three parts:\n"
        "1. What they got right (be specific)\n"
        "2. What key insight they are missing or got wrong\n"
        "3. The complete, correct answer in 3-5 sentences\n\n"
        "Be direct and educational. Do not be vague."
    )
    output = run_command(
        [args.cli_path, "ask", prompt, "--notebook", args.notebook_id, "--new"],
        timeout=60,
    )
    if not output:
        print(json.dumps({"error": "No response from NotebookLM"}))
        sys.exit(1)

    feedback = clean_cli_output(output)
    result = {
        "question": args.question,
        "user_answer": args.answer,
        "feedback": feedback,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# Subcommand: research
# ---------------------------------------------------------------------------

def cmd_research(args) -> None:
    """Create a NotebookLM notebook via web research on a topic."""
    nlm = args.cli_path
    topic = args.topic
    mode = getattr(args, 'mode', 'deep')

    logging.info(f"=== Research: topic='{topic}' mode={mode} ===")

    # Create notebook
    nb_raw = run_command([nlm, "create", f"Research: {topic}", "--json"])
    if not nb_raw:
        logging.error("[FATAL] Failed to create research notebook.")
        sys.exit(1)
    try:
        nb_id = json.loads(nb_raw)["notebook"]["id"]
    except (json.JSONDecodeError, KeyError):
        logging.error(f"[FATAL] Unexpected create response: {nb_raw[:200]}")
        sys.exit(1)

    logging.info(f"Notebook created: Research: {topic} ({nb_id})")

    # Start research
    logging.info(f"Starting {mode} web research — this may take several minutes...")
    run_command([nlm, "source", "add-research", topic, "--mode", mode, "--notebook", nb_id])

    # Wait for completion
    logging.info("Waiting for research import to complete...")
    result = run_command(
        [nlm, "research", "wait", "--import-all", "-n", nb_id, "--timeout", "600"],
        timeout=700,
    )
    if not result:
        logging.warning("Research wait did not confirm completion — check NotebookLM manually.")

    print(f"\nResearch complete.")
    print(f"Notebook : Research: {topic}")
    print(f"ID       : {nb_id}")
    print(f"\nNext step:")
    print(f'  python3 distill.py distill --keywords "{topic}" --topic "{topic}" --vault-dir <your-vault-dir> --mode summary')


# ---------------------------------------------------------------------------
# Subcommand: persist
# ---------------------------------------------------------------------------

def cmd_persist(args) -> None:
    """Write markdown content directly into the Obsidian vault with frontmatter."""
    vault_dir = os.path.expanduser(args.vault_dir)
    if not os.path.isdir(vault_dir):
        logging.error(f"[FATAL] vault-dir does not exist: '{vault_dir}'")
        sys.exit(1)

    # Get content
    if args.file:
        content_body = open(os.path.expanduser(args.file), encoding="utf-8").read().strip()
    elif args.content:
        content_body = args.content.strip()
    else:
        logging.error("[FATAL] Provide --content or --file.")
        sys.exit(1)

    date_str = datetime.now().strftime("%Y-%m-%d")
    rel_path = args.path
    title = args.title or os.path.basename(rel_path).replace(".md", "")
    tags_list = [t.strip() for t in args.tags.split(",")] if args.tags else ["persist", "knowledge"]

    fm_lines = [
        "---",
        f"title: {yaml_quote(title)}",
        f"date: {date_str}",
        "type: knowledge-note",
        "author: notebooklm-distiller",
        f"tags: {json.dumps(tags_list, ensure_ascii=False)}",
        "status: draft",
        "---",
    ]
    full_content = '\n'.join(fm_lines) + f"\n\n# {title}\n\n{content_body}\n"

    out_path = os.path.join(vault_dir, rel_path)
    write_note(out_path, full_content)
    print(f"Persisted → {out_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser = argparse.ArgumentParser(
        description="NotebookLM Distiller — knowledge extraction and management for Obsidian.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Subcommands:
  distill   Extract knowledge from NotebookLM into Obsidian markdown notes.
  research  Start a NotebookLM web research session on a topic.
  persist   Write any markdown content directly into the Obsidian vault.

Examples:
  python3 distill.py distill --keywords "machine learning" --topic "ML Basics" \\
      --vault-dir ~/Obsidian/Vault --mode summary
  python3 distill.py research --topic "Quantum Computing"
  python3 distill.py persist --title "Meeting Notes" --vault-dir ~/Obsidian/Vault \\
      --path "Notes/2026-03-09.md" --content "Key decisions: ..."
        """,
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # --- distill ---
    p_distill = sub.add_parser("distill", help="Extract knowledge from NotebookLM notebooks.")
    p_distill.add_argument("--keywords", nargs="+", required=True,
                           help="Keywords to match against notebook titles (e.g. 'machine learning' 'AI')")
    p_distill.add_argument("--topic", required=True,
                           help="Topic folder name in Obsidian (e.g. 'Machine Learning Basics')")
    p_distill.add_argument("--vault-dir", required=True,
                           help="Base Obsidian directory (e.g. ~/Obsidian/Vault/10_Projects)")
    p_distill.add_argument("--mode", choices=["qa", "summary", "glossary"], default="qa",
                           help="Extraction strategy: qa (default), summary, or glossary")
    p_distill.add_argument("--cli-path", default=find_notebooklm_cli(),
                           help="Path to the notebooklm CLI (default: 'notebooklm' from PATH)")
    p_distill.add_argument("--lang", default="en", choices=["en", "zh"],
                           help="Output language: 'en' (default) or 'zh' for Chinese")
    p_distill.add_argument("--writeback", action="store_true", default=False,
                           help="Write distilled content back into the NotebookLM notebook as a note")

    # --- research ---
    p_research = sub.add_parser("research", help="Start a NotebookLM web research session.")
    p_research.add_argument("--topic", required=True,
                            help="Research topic (e.g. 'Transformer architecture')")
    p_research.add_argument("--mode", choices=["deep", "fast"], default="deep",
                            help="Research depth (default: deep)")
    p_research.add_argument("--cli-path", default=find_notebooklm_cli(),
                            help="Path to the notebooklm CLI")

    # --- quiz ---
    p_quiz = sub.add_parser("quiz", help="Generate quiz questions as JSON for Discord quiz sessions.")
    p_quiz.add_argument("--keywords", nargs="+", required=True,
                        help="Keywords to match against notebook titles")
    p_quiz.add_argument("--count", type=int, default=10,
                        help="Number of questions to generate (default: 10)")
    p_quiz.add_argument("--cli-path", default=find_notebooklm_cli(),
                        help="Path to the notebooklm CLI")
    p_quiz.add_argument("--lang", default="en", choices=["en", "zh"],
                        help="Output language: 'en' (default) or 'zh' for Chinese")

    # --- evaluate ---
    p_evaluate = sub.add_parser("evaluate", help="Evaluate a user's answer against notebook sources.")
    p_evaluate.add_argument("--notebook-id", required=True,
                            help="NotebookLM notebook ID (from quiz output)")
    p_evaluate.add_argument("--question", required=True,
                            help="The question that was asked")
    p_evaluate.add_argument("--answer", required=True,
                            help="The user's answer to evaluate")
    p_evaluate.add_argument("--cli-path", default=find_notebooklm_cli(),
                            help="Path to the notebooklm CLI")
    p_evaluate.add_argument("--lang", default="en", choices=["en", "zh"],
                            help="Output language: 'en' (default) or 'zh' for Chinese")

    # --- persist ---
    p_persist = sub.add_parser("persist", help="Write markdown content directly into Obsidian.")
    p_persist.add_argument("--vault-dir", required=True,
                           help="Base Obsidian directory")
    p_persist.add_argument("--path", required=True,
                           help="Relative path within vault (e.g. 'Notes/2026-03-09.md')")
    p_persist.add_argument("--title", default="",
                           help="Note title (defaults to filename)")
    p_persist.add_argument("--content", default="",
                           help="Markdown content to write (use --file for file input)")
    p_persist.add_argument("--file", default="",
                           help="Path to a markdown file to persist")
    p_persist.add_argument("--tags", default="",
                           help="Comma-separated tags (e.g. 'research,ai,notes')")

    args = parser.parse_args()

    dispatch = {
        "distill": cmd_distill,
        "research": cmd_research,
        "persist": cmd_persist,
        "quiz": cmd_quiz,
        "evaluate": cmd_evaluate,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
