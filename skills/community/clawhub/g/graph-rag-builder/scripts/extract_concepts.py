#!/usr/bin/env python3
"""
extract_concepts.py — Content Extraction + LLM Concept Extraction (M2)

Two phases in one script:
  Phase 2: HTML → clean chunked text (split at h2 boundaries, code blocks
           extracted from <pre> tags alongside their section text)
  Phase 3: Each chunk → Claude API call → structured concepts, tags,
           prerequisites, relationships, code example descriptions

Usage:
    python extract_concepts.py --input ./output/strudel-cc-mcp
    python extract_concepts.py --input ./output/strudel-cc-mcp --model sonnet
    python extract_concepts.py --input ./output/strudel-cc-mcp --max-pages 5 --dry-run
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Dependency bootstrap
# ---------------------------------------------------------------------------

def _ensure_deps():
    deps = {"bs4": "beautifulsoup4", "lxml": "lxml", "anthropic": "anthropic"}
    missing = [pkg for mod, pkg in deps.items()
               if not __import_ok(mod)]
    if missing:
        print(f"Installing: {', '.join(missing)}")
        os.system(f"pip install {' '.join(missing)} --break-system-packages -q")

def __import_ok(mod):
    try:
        __import__(mod)
        return True
    except ImportError:
        return False

_ensure_deps()

from bs4 import BeautifulSoup, NavigableString, Tag
import anthropic


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

# Pages to skip regardless of content
SKIP_URL_PATTERNS = [
    "/de/",          # German translations
    "/fr/",          # French (future-proofing)
    "/bakery",       # Interactive gallery, no prose
    "/intro/showcase",  # Short gallery page
]

# Primary content selector — works for all Strudel docs pages
CONTENT_SELECTOR = ("article", {"class": "content"})

# Model shortcuts → full API strings
MODEL_MAP = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-5-20250929",
    "opus":   "claude-opus-4-5-20251101",
}

# Max words per chunk before we force-split a section
MAX_CHUNK_WORDS = 700

# Drop chunks with fewer than this many words (footers, stubs).
# 30 is intentionally low to preserve function-reference pages where
# each h2 section is a single function with a one-liner + code example.
MIN_CHUNK_WORDS = 30

# Max code blocks to include in the LLM prompt per chunk
MAX_CODES_IN_PROMPT = 6


# ---------------------------------------------------------------------------
# Phase 2: HTML → structured chunks
# ---------------------------------------------------------------------------

def extract_article(html: str) -> Tag | None:
    """Return the <article class='content'> element or None."""
    soup = BeautifulSoup(html, "lxml")
    return soup.find(*CONTENT_SELECTOR)


def _word_count(text: str) -> int:
    return len(text.split())


def split_into_chunks(article: Tag, url: str, page_title: str) -> list[dict]:
    """
    Strudel docs structure:
        <article class='content'>
          <section>            ← all prose (h1/h2/p/pre/ul...)
          <nav>                ← footer ("Edit this page") — skipped
        </article>

    We recursively walk the <section>, treating h1 and h2 headings as chunk
    boundaries. h3/h4 stay within their parent chunk.

    The first h1 we encounter is used as the canonical page title (cleaner
    than the browser <title> tag which includes emoji and site suffix).

    Returns list of chunk dicts with keys:
        id, url, page_title, section, text, code_examples_raw, word_count
    """
    url_hash = _url_hash(url)

    # Content root: the <section> child of the article.
    # Fall back to the article itself for non-standard pages.
    content_root = article.find("section") or article

    chunks: list[dict] = []
    chunk_idx = 0
    inferred_title = page_title   # overwritten by first h1 we find
    current_section = page_title
    current_parts: list[str] = []
    current_codes: list[str] = []

    def _flush():
        nonlocal chunk_idx
        text = "\n".join(p for p in current_parts if p.strip()).strip()
        if _word_count(text) < MIN_CHUNK_WORDS:
            return
        for sub_text, sub_codes in _force_split(text, list(current_codes), MAX_CHUNK_WORDS):
            if _word_count(sub_text) >= MIN_CHUNK_WORDS:
                chunks.append({
                    "id": f"{url_hash}_chunk_{chunk_idx:03d}",
                    "url": url,
                    "page_title": inferred_title,
                    "section": current_section,
                    "text": sub_text,
                    "code_examples_raw": sub_codes,
                    "word_count": _word_count(sub_text),
                })
                chunk_idx += 1

    def _walk(node: Tag) -> None:
        nonlocal current_section, inferred_title

        for el in node.children:
            if isinstance(el, NavigableString):
                continue
            if not hasattr(el, "name") or not el.name:
                continue

            tag = el.name

            # Skip footer nav and non-content elements
            if tag in ("nav", "style", "script"):
                continue

            if tag in ("h1", "h2"):
                _flush()
                current_parts.clear()
                current_codes.clear()
                heading = el.get_text(strip=True)
                # First h1 becomes the canonical page title
                if tag == "h1" and not chunks and chunk_idx == 0 and not current_parts:
                    inferred_title = heading
                current_section = heading
                current_parts.append(f"{'#' * int(tag[1])} {heading}")

            elif tag in ("h3", "h4"):
                current_parts.append(f"{'#' * int(tag[1])} {el.get_text(strip=True)}")

            elif tag == "pre":
                code = el.get_text(strip=True)
                current_parts.append(f"\n```strudel\n{code}\n```\n")
                current_codes.append(code)

            elif tag == "p":
                text = el.get_text(separator=" ", strip=True)
                if text:
                    current_parts.append(text)

            elif tag in ("ul", "ol"):
                for li in el.find_all("li"):
                    current_parts.append(f"- {li.get_text(separator=' ', strip=True)}")

            elif tag in ("table",):
                # Simple table → flatten to text
                current_parts.append(el.get_text(separator=" ", strip=True))

            elif tag not in ("img", "iframe", "input", "button", "form",
                             "svg", "canvas", "audio", "video"):
                # Recurse into ANY other element (div, section, astro-island,
                # custom-repl, details, summary, blockquote, etc.)
                # This future-proofs against new component types.
                _walk(el)

    _walk(content_root)
    _flush()
    return chunks


def _force_split(text: str, codes: list[str], max_words: int) -> list[tuple[str, list[str]]]:
    """
    If text exceeds max_words, split at paragraph boundaries.
    Returns list of (text_fragment, code_list) tuples.
    """
    if _word_count(text) <= max_words:
        return [(text, codes)]

    paragraphs = re.split(r"\n{2,}", text)
    parts = []
    current: list[str] = []
    current_wc = 0

    for para in paragraphs:
        para_wc = _word_count(para)
        if current_wc + para_wc > max_words and current:
            parts.append(("\n\n".join(current), []))
            current = [para]
            current_wc = para_wc
        else:
            current.append(para)
            current_wc += para_wc

    if current:
        parts.append(("\n\n".join(current), []))

    # Attach codes to first sub-chunk only
    if parts:
        parts[0] = (parts[0][0], codes)
    return parts


def _url_hash(url: str) -> str:
    import hashlib
    return hashlib.sha256(url.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Phase 3: LLM concept extraction
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a knowledge extraction assistant specializing in technical documentation
for Strudel, a JavaScript live-coding music pattern library.

Your job: given a section of documentation, extract structured knowledge that
will be used to build a searchable knowledge graph and MCP server.

Always respond with valid JSON only — no markdown fences, no explanation.
"""

def _build_user_prompt(chunk: dict) -> str:
    # Truncate code examples to avoid token overflow
    codes_text = ""
    if chunk["code_examples_raw"]:
        shown = chunk["code_examples_raw"][:MAX_CODES_IN_PROMPT]
        codes_text = "\n\nCode examples in this section:\n" + "\n---\n".join(
            f"```\n{c[:400]}\n```" for c in shown
        )

    return f"""Documentation section from: {chunk['page_title']} ({chunk['url']})
Section heading: {chunk['section']}

--- Content ---
{chunk['text'][:3000]}
{codes_text}
--- End ---

Extract the following as a JSON object:

{{
  "concepts": [
    {{"name": "short concept name", "definition": "one clear sentence"}}
  ],
  "tags": ["tag1", "tag2"],
  "code_examples": [
    {{"code": "...", "description": "one sentence describing what this demonstrates"}}
  ],
  "prerequisites": ["concept names the reader should already understand"],
  "relationships": [
    {{"from": "concept A", "to": "concept B", "type": "requires|related_to|explains|part_of"}}
  ]
}}

Guidelines:
- concepts: name the specific ideas taught here (2-8 concepts, not generic terms)
- tags: broad categories (e.g. "rhythm", "synthesis", "beginner", "pattern")
- code_examples: only include examples that clearly demonstrate a concept
- prerequisites: be specific, use exact concept names where possible
- relationships: only include confident relationships, 0-5 is fine
"""


def _extract_json(response_text: str) -> dict:
    """
    Robustly extract a JSON object from LLM response text.
    Handles cases where the model adds explanation or markdown fences.
    """
    text = response_text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip markdown code fences
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)

    # Find the outermost JSON object
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass

    return {}


def _empty_extraction() -> dict:
    return {
        "concepts": [],
        "tags": [],
        "code_examples": [],
        "prerequisites": [],
        "relationships": [],
    }


def extract_concepts_llm(
    chunk: dict,
    client: anthropic.Anthropic,
    model: str,
    retries: int = 3,
) -> dict:
    """
    Call Claude API to extract concepts from a single chunk.
    Returns the parsed extraction dict, or an empty dict on failure.
    """
    for attempt in range(retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": _build_user_prompt(chunk)}],
            )
            raw = response.content[0].text
            parsed = _extract_json(raw)
            if parsed:
                return parsed
            print(f"         ⚠  JSON parse failed, attempt {attempt+1}/{retries}")
            print(f"            Response: {raw[:200]}")

        except anthropic.RateLimitError:
            wait = (attempt + 1) * 10
            print(f"         ⚠  Rate limit hit. Waiting {wait}s...")
            time.sleep(wait)
        except anthropic.APIError as e:
            print(f"         ✗  API error: {e}")
            time.sleep(2)
        except Exception as e:
            print(f"         ✗  Unexpected error: {e}")
            time.sleep(2)

    return _empty_extraction()


# ---------------------------------------------------------------------------
# State management (mirrors CrawlDB from crawl.py)
# ---------------------------------------------------------------------------

def load_state(output_path: Path) -> dict:
    state_file = output_path / "crawl.json"
    if state_file.exists():
        return json.loads(state_file.read_text())
    return {"pages": [], "meta": []}


def save_state(output_path: Path, state: dict):
    state_file = output_path / "crawl.json"
    state_file.write_text(json.dumps(state, indent=2))


def get_page_status(state: dict, url: str) -> str | None:
    for p in state["pages"]:
        if p["url"] == url:
            return p["status"]
    return None


def set_page_status(state: dict, url: str, status: str):
    for p in state["pages"]:
        if p["url"] == url:
            p["status"] = status
            return
    state["pages"].append({"url": url, "status": status})


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def should_skip(url: str) -> bool:
    return any(pat in url for pat in SKIP_URL_PATTERNS)


def process_page(
    raw_file: Path,
    output_dir: Path,
    client: anthropic.Anthropic | None,
    model: str,
    dry_run: bool,
    api_delay: float,
) -> dict:
    """
    Process a single raw_content JSON file.
    Returns a summary dict with counts.
    """
    d = json.loads(raw_file.read_text())
    url = d["url"]
    page_title = d.get("title", url.split("/")[-1])

    # Skip conditions
    if should_skip(url):
        return {"url": url, "skipped": "url_pattern", "chunks": 0}

    html = d.get("raw_html", "")
    article = extract_article(html)
    if not article:
        return {"url": url, "skipped": "no_article", "chunks": 0}

    # Phase 2: chunking
    chunks = split_into_chunks(article, url, page_title)
    if not chunks:
        return {"url": url, "skipped": "no_chunks", "chunks": 0}

    # Phase 3: LLM extraction (or dry-run pass-through)
    extracted_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"           chunk {i+1}/{len(chunks)}: \"{chunk['section'][:50]}\"  "
              f"({chunk['word_count']} words, {len(chunk['code_examples_raw'])} code blocks)")

        if dry_run or client is None:
            extraction = _empty_extraction()
        else:
            extraction = extract_concepts_llm(chunk, client, model)
            if api_delay > 0:
                time.sleep(api_delay)

        extracted_chunks.append({**chunk, **extraction})

    # Save to extracted/
    extracted_dir = output_dir / "extracted"
    extracted_dir.mkdir(exist_ok=True)
    out_file = extracted_dir / f"{_url_hash(url)}.json"
    out_data = {
        "url": url,
        "title": page_title,
        "processed_at": datetime.now().isoformat(),
        "model": model if not dry_run else "dry-run",
        "chunks": extracted_chunks,
    }
    out_file.write_text(json.dumps(out_data, indent=2, ensure_ascii=False))

    return {"url": url, "skipped": None, "chunks": len(chunks)}


def run(
    input_dir: str,
    model_shorthand: str = "haiku",
    max_pages: int | None = None,
    dry_run: bool = False,
    force: bool = False,
    api_delay: float = 0.2,
):
    output_path = Path(input_dir)
    raw_dir = output_path / "raw_content"

    if not raw_dir.exists():
        print(f"✗  raw_content/ not found at {raw_dir}")
        sys.exit(1)

    # Resolve model
    model = MODEL_MAP.get(model_shorthand, model_shorthand)
    print(f"\n{'━'*62}")
    print(f"  GraphRAG Builder — Concept Extraction (M2)")
    print(f"{'━'*62}")
    print(f"  Input:   {output_path}")
    print(f"  Model:   {model}{' (dry-run, no API calls)' if dry_run else ''}")
    if max_pages:
        print(f"  Limit:   first {max_pages} pages")
    print(f"{'━'*62}\n")

    # Set up Anthropic client
    client = None
    if not dry_run:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("✗  ANTHROPIC_API_KEY not set. Use --dry-run to test without API calls.")
            sys.exit(1)
        client = anthropic.Anthropic(api_key=api_key)

    # Load crawl state
    state = load_state(output_path)

    raw_files = sorted(raw_dir.glob("*.json"))
    if max_pages:
        raw_files = raw_files[:max_pages]

    stats = {"processed": 0, "skipped": 0, "total_chunks": 0, "failed": 0}

    for raw_file in raw_files:
        d = json.loads(raw_file.read_text())
        url = d["url"]
        status = get_page_status(state, url)

        # Incremental: skip if already extracted (unless --force)
        if not force and status in ("extracted", "embedded", "graphed", "complete"):
            print(f"  ✓  already extracted — skip  {url.replace('https://strudel.cc', '')}")
            stats["skipped"] += 1
            continue

        short_url = url.replace("https://strudel.cc", "") or "/"
        print(f"  Processing: {short_url}")

        result = process_page(
            raw_file=raw_file,
            output_dir=output_path,
            client=client,
            model=model,
            dry_run=dry_run,
            api_delay=api_delay,
        )

        if result["skipped"]:
            print(f"           → skipped ({result['skipped']})")
            stats["skipped"] += 1
        else:
            stats["processed"] += 1
            stats["total_chunks"] += result["chunks"]
            # Advance status in state
            set_page_status(state, url, "extracted")

    save_state(output_path, state)

    print(f"\n{'━'*62}")
    print(f"  Done!")
    print(f"  Pages processed:   {stats['processed']}")
    print(f"  Pages skipped:     {stats['skipped']}")
    print(f"  Total chunks:      {stats['total_chunks']}")
    print(f"  Output:            {output_path}/extracted/")
    print(f"{'━'*62}\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="GraphRAG Builder — Concept Extraction (M2)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run — test chunking without API calls:
  python extract_concepts.py --input ./output/strudel-cc-mcp --dry-run

  # Extract 5 pages with haiku (cheap, fast):
  python extract_concepts.py --input ./output/strudel-cc-mcp --max-pages 5

  # Full extraction with sonnet (better quality):
  python extract_concepts.py --input ./output/strudel-cc-mcp --model sonnet

  # Re-run everything, ignoring prior extracted status:
  python extract_concepts.py --input ./output/strudel-cc-mcp --force
        """,
    )
    parser.add_argument("--input", required=True,
                        help="Path to the MCP output folder (contains raw_content/)")
    parser.add_argument("--model", default="haiku",
                        help="Model shorthand: haiku, sonnet, opus, or full model string (default: haiku)")
    parser.add_argument("--max-pages", type=int, default=None, metavar="N",
                        help="Process only the first N pages (for testing)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Run chunking only, skip LLM calls. Good for testing.")
    parser.add_argument("--force", action="store_true",
                        help="Re-extract pages even if already marked as extracted")
    parser.add_argument("--api-delay", type=float, default=0.2, metavar="SEC",
                        help="Seconds between API calls to avoid rate limiting (default: 0.2)")

    args = parser.parse_args()
    run(
        input_dir=args.input,
        model_shorthand=args.model,
        max_pages=args.max_pages,
        dry_run=args.dry_run,
        force=args.force,
        api_delay=args.api_delay,
    )


if __name__ == "__main__":
    main()
