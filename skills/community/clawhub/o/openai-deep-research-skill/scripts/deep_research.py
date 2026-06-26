#!/usr/bin/env python3
"""Run a multi-step deep-research workflow with the OpenAI Responses API."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import textwrap
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_PLANNER_MODEL = "gpt-4.1-mini"
DEFAULT_RESEARCH_MODEL = "gpt-4.1"
DEFAULT_WRITER_MODEL = "gpt-4.1"
DEFAULT_PLANNER_MAX_OUTPUT_TOKENS = 1200
DEFAULT_RESEARCH_MAX_OUTPUT_TOKENS = 1800
DEFAULT_WRITER_MAX_OUTPUT_TOKENS = 3200
REQUIRED_REPORT_SECTIONS = [
    "# Executive Summary",
    "# Key Findings",
    "# Evidence by Sub-question",
    "# Contradictions and Uncertainty",
    "# Recommendations",
    "# Sources",
]
RESEARCH_DEPTH_OPTIONS = ("shallow", "standard", "deep")


class DeepResearchError(RuntimeError):
    """Raised when the workflow cannot continue safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a cited research report using OpenAI APIs.",
    )
    parser.add_argument(
        "topic",
        nargs="+",
        help="Research topic or question.",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory where run artifacts are written (default: outputs).",
    )
    parser.add_argument(
        "--language",
        default="zh-CN",
        help="Output language tag (example: zh-CN, en-US).",
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=5,
        help="Number of sub-questions to investigate (2-12).",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        default=2,
        help="How many sub-questions to research concurrently (1-8).",
    )
    parser.add_argument(
        "--research-depth",
        choices=RESEARCH_DEPTH_OPTIONS,
        default="standard",
        help="Evidence detail level per sub-question (shallow|standard|deep).",
    )
    parser.add_argument(
        "--planner-model",
        default=DEFAULT_PLANNER_MODEL,
        help=f"Model used for research planning (default: {DEFAULT_PLANNER_MODEL}).",
    )
    parser.add_argument(
        "--research-model",
        default=DEFAULT_RESEARCH_MODEL,
        help=f"Model used for evidence gathering (default: {DEFAULT_RESEARCH_MODEL}).",
    )
    parser.add_argument(
        "--writer-model",
        default=DEFAULT_WRITER_MODEL,
        help=f"Model used for final report synthesis (default: {DEFAULT_WRITER_MODEL}).",
    )
    parser.add_argument(
        "--web-tool-type",
        default="web_search_preview",
        help="Responses API web-search tool type (default: web_search_preview).",
    )
    parser.add_argument(
        "--disable-web-search",
        action="store_true",
        help="Disable web-search tool usage during evidence gathering.",
    )
    parser.add_argument(
        "--api-key",
        default=os.getenv("OPENAI_API_KEY", ""),
        help="OpenAI API key. Defaults to OPENAI_API_KEY environment variable.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("OPENAI_BASE_URL", ""),
        help="Optional custom OpenAI-compatible endpoint.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=120.0,
        help="Request timeout in seconds (default: 120).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Retry count for transient API errors (default: 3).",
    )
    parser.add_argument(
        "--planner-max-output-tokens",
        type=int,
        default=DEFAULT_PLANNER_MAX_OUTPUT_TOKENS,
        help=f"Planner max output tokens (default: {DEFAULT_PLANNER_MAX_OUTPUT_TOKENS}).",
    )
    parser.add_argument(
        "--research-max-output-tokens",
        type=int,
        default=DEFAULT_RESEARCH_MAX_OUTPUT_TOKENS,
        help=f"Per sub-question max output tokens (default: {DEFAULT_RESEARCH_MAX_OUTPUT_TOKENS}).",
    )
    parser.add_argument(
        "--writer-max-output-tokens",
        type=int,
        default=DEFAULT_WRITER_MAX_OUTPUT_TOKENS,
        help=f"Writer max output tokens (default: {DEFAULT_WRITER_MAX_OUTPUT_TOKENS}).",
    )
    parser.add_argument(
        "--max-total-output-tokens",
        type=int,
        default=0,
        help=(
            "Optional hard ceiling for estimated total output tokens. "
            "0 means no ceiling."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Skip API calls and create mock artifacts for workflow testing.",
    )

    args = parser.parse_args()
    args.topic = " ".join(args.topic).strip()

    if args.depth < 2 or args.depth > 12:
        parser.error("--depth must be between 2 and 12")
    if args.parallel < 1 or args.parallel > 8:
        parser.error("--parallel must be between 1 and 8")
    if args.max_retries < 1:
        parser.error("--max-retries must be >= 1")
    if args.planner_max_output_tokens < 1:
        parser.error("--planner-max-output-tokens must be >= 1")
    if args.research_max_output_tokens < 1:
        parser.error("--research-max-output-tokens must be >= 1")
    if args.writer_max_output_tokens < 1:
        parser.error("--writer-max-output-tokens must be >= 1")
    if args.max_total_output_tokens < 0:
        parser.error("--max-total-output-tokens must be >= 0")

    return args


def estimate_max_output_tokens(
    *,
    depth: int,
    planner_max_output_tokens: int,
    research_max_output_tokens: int,
    writer_max_output_tokens: int,
) -> Dict[str, int]:
    planner = planner_max_output_tokens
    research = depth * research_max_output_tokens
    writer = writer_max_output_tokens
    total = planner + research + writer
    return {
        "planner": planner,
        "research_total": research,
        "writer": writer,
        "estimated_total": total,
    }


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "research"


def make_run_dir(base_dir: str, topic: str) -> Path:
    run_id = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = slugify(topic)[:50]
    run_dir = Path(base_dir).expanduser().resolve() / f"{run_id}-{slug}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_openai_client(api_key: str, base_url: str, timeout: float) -> Any:
    if not api_key:
        raise DeepResearchError("Missing API key. Set OPENAI_API_KEY or pass --api-key.")

    try:
        from openai import OpenAI  # type: ignore
    except ImportError as exc:
        raise DeepResearchError(
            "Dependency missing: openai package is not installed. "
            "Run: pip install -r scripts/requirements.txt"
        ) from exc

    kwargs: Dict[str, Any] = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url

    try:
        kwargs["timeout"] = timeout
        return OpenAI(**kwargs)
    except TypeError:
        kwargs.pop("timeout", None)
        return OpenAI(**kwargs)


def call_responses_api(
    client: Any,
    *,
    model: str,
    input_text: str,
    tools: Optional[List[Dict[str, Any]]],
    max_retries: int,
    max_output_tokens: Optional[int],
) -> Any:
    payload: Dict[str, Any] = {
        "model": model,
        "input": input_text,
    }
    if tools:
        payload["tools"] = tools
    if max_output_tokens:
        payload["max_output_tokens"] = max_output_tokens

    last_error: Optional[Exception] = None
    for attempt in range(1, max_retries + 1):
        try:
            return client.responses.create(**payload)
        except Exception as exc:
            last_error = exc
            if attempt >= max_retries:
                break
            sleep_seconds = min(2 ** (attempt - 1), 8)
            print(
                f"[warn] API call failed on attempt {attempt}/{max_retries}: {exc}. "
                f"Retrying in {sleep_seconds}s...",
                file=sys.stderr,
            )
            time.sleep(sleep_seconds)

    raise DeepResearchError(f"API call failed after {max_retries} attempts: {last_error}")


def response_to_text(response: Any) -> str:
    output_text = getattr(response, "output_text", None)
    if isinstance(output_text, str) and output_text.strip():
        return output_text.strip()

    payload: Dict[str, Any] = {}
    if hasattr(response, "model_dump"):
        payload = response.model_dump()
    elif hasattr(response, "to_dict"):
        payload = response.to_dict()
    elif isinstance(response, dict):
        payload = response

    chunks: List[str] = []
    for item in payload.get("output", []):
        if not isinstance(item, dict):
            continue
        if item.get("type") != "message":
            continue
        for content in item.get("content", []):
            if not isinstance(content, dict):
                continue
            if content.get("type") in {"output_text", "text"}:
                value = content.get("text") or content.get("value")
                if isinstance(value, str) and value.strip():
                    chunks.append(value.strip())

    if chunks:
        return "\n".join(chunks).strip()

    if payload:
        return json.dumps(payload, ensure_ascii=False, indent=2)

    return str(response)


def strip_code_fence(text: str) -> str:
    fenced = re.findall(r"```(?:json)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
    if fenced:
        return fenced[0].strip()
    return text.strip()


def extract_json_object(text: str) -> Dict[str, Any]:
    cleaned = strip_code_fence(text)

    candidates = [cleaned]
    brace_level = 0
    start = None
    for idx, char in enumerate(cleaned):
        if char == "{":
            if brace_level == 0:
                start = idx
            brace_level += 1
        elif char == "}" and brace_level > 0:
            brace_level -= 1
            if brace_level == 0 and start is not None:
                candidates.append(cleaned[start : idx + 1])

    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        try:
            parsed = json.loads(candidate)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            continue

    raise DeepResearchError("Model output is not valid JSON.")


def build_plan_prompt(topic: str, depth: int, language: str) -> str:
    return textwrap.dedent(
        f"""
        You are a research planner.
        Break the topic into exactly {depth} sub-questions that can be investigated independently.

        Topic:
        {topic}

        Return strict JSON only with this schema:
        {{
          "research_goal": "string",
          "sub_questions": [
            {{
              "id": "Q1",
              "question": "string",
              "why_it_matters": "string",
              "search_query": "string"
            }}
          ],
          "final_report_outline": ["string"]
        }}

        Rules:
        - Use language tag {language} for all text values.
        - Keep each question specific and evidence-seeking.
        - Include one search_query per sub-question.
        - Do not add markdown or code fences.
        """
    ).strip()


def normalize_plan(plan_payload: Dict[str, Any], topic: str, depth: int) -> Dict[str, Any]:
    goal = str(plan_payload.get("research_goal") or f"Analyze: {topic}").strip()
    raw_questions = plan_payload.get("sub_questions")
    normalized_questions: List[Dict[str, str]] = []

    if isinstance(raw_questions, list):
        for item in raw_questions:
            if len(normalized_questions) >= depth:
                break
            if isinstance(item, str):
                question = item.strip()
                if not question:
                    continue
                idx = len(normalized_questions) + 1
                normalized_questions.append(
                    {
                        "id": f"Q{idx}",
                        "question": question,
                        "why_it_matters": "Supports final recommendation.",
                        "search_query": question,
                    }
                )
                continue

            if not isinstance(item, dict):
                continue

            question = str(item.get("question") or "").strip()
            if not question:
                continue

            idx = len(normalized_questions) + 1
            question_id = str(item.get("id") or f"Q{idx}").strip() or f"Q{idx}"
            normalized_questions.append(
                {
                    "id": question_id,
                    "question": question,
                    "why_it_matters": str(item.get("why_it_matters") or "Supports final recommendation.").strip(),
                    "search_query": str(item.get("search_query") or question).strip(),
                }
            )

    while len(normalized_questions) < depth:
        idx = len(normalized_questions) + 1
        question = f"{topic}: key dimension {idx}"
        normalized_questions.append(
            {
                "id": f"Q{idx}",
                "question": question,
                "why_it_matters": "Fill missing analysis scope.",
                "search_query": question,
            }
        )

    outline = plan_payload.get("final_report_outline")
    normalized_outline: List[str] = []
    if isinstance(outline, list):
        for item in outline:
            if isinstance(item, str) and item.strip():
                normalized_outline.append(item.strip())
    if not normalized_outline:
        normalized_outline = [
            "Executive Summary",
            "Evidence by Sub-question",
            "Contradictions and Uncertainty",
            "Actionable Recommendations",
        ]

    return {
        "research_goal": goal,
        "sub_questions": normalized_questions,
        "final_report_outline": normalized_outline,
    }


def research_depth_profile(research_depth: str) -> Dict[str, Any]:
    if research_depth == "shallow":
        return {
            "min_sources": 2,
            "max_sources": 4,
            "analysis_instruction": "Keep analysis concise and prioritize breadth over depth.",
        }
    if research_depth == "deep":
        return {
            "min_sources": 5,
            "max_sources": 10,
            "analysis_instruction": (
                "Use deeper cross-source validation and highlight disagreements explicitly."
            ),
        }
    return {
        "min_sources": 3,
        "max_sources": 6,
        "analysis_instruction": "Balance coverage depth and conciseness.",
    }


def build_research_prompt(
    topic: str,
    language: str,
    question: Dict[str, str],
    research_depth: str,
) -> str:
    profile = research_depth_profile(research_depth)
    return textwrap.dedent(
        f"""
        You are an evidence-first researcher.

        Topic: {topic}
        Sub-question ID: {question['id']}
        Sub-question: {question['question']}
        Why it matters: {question['why_it_matters']}
        Suggested query: {question['search_query']}

        Return strict JSON only using this schema:
        {{
          "question_id": "{question['id']}",
          "question": "{question['question']}",
          "answer_summary": "string",
          "key_findings": ["string"],
          "source_notes": [
            {{
              "title": "string",
              "url": "https://...",
              "publisher": "string",
              "published_date": "YYYY-MM-DD or unknown",
              "evidence": "string",
              "reliability": "high|medium|low"
            }}
          ],
          "confidence": "high|medium|low",
          "gaps": ["string"]
        }}

        Rules:
        - Use language tag {language} for all narrative text.
        - Provide {profile['min_sources']} to {profile['max_sources']} source_notes with absolute URLs.
        - Prefer primary sources, official docs, filings, standards, and first-party data.
        - Flag disagreement between sources in key_findings or gaps.
        - {profile['analysis_instruction']}
        - Do not add markdown or code fences.
        """
    ).strip()


def normalize_finding(question: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
    answer_summary = str(payload.get("answer_summary") or "No answer summary generated.").strip()

    key_findings: List[str] = []
    raw_findings = payload.get("key_findings")
    if isinstance(raw_findings, list):
        for item in raw_findings:
            if isinstance(item, str) and item.strip():
                key_findings.append(item.strip())

    gaps: List[str] = []
    raw_gaps = payload.get("gaps")
    if isinstance(raw_gaps, list):
        for item in raw_gaps:
            if isinstance(item, str) and item.strip():
                gaps.append(item.strip())

    normalized_sources: List[Dict[str, str]] = []
    raw_sources = payload.get("source_notes")
    if isinstance(raw_sources, list):
        for source in raw_sources:
            if not isinstance(source, dict):
                continue
            url = str(source.get("url") or "").strip()
            if not url:
                continue
            normalized_sources.append(
                {
                    "title": str(source.get("title") or "Untitled source").strip(),
                    "url": url,
                    "publisher": str(source.get("publisher") or "unknown").strip(),
                    "published_date": str(source.get("published_date") or "unknown").strip(),
                    "evidence": str(source.get("evidence") or "").strip(),
                    "reliability": str(source.get("reliability") or "medium").strip().lower(),
                }
            )

    confidence = str(payload.get("confidence") or "low").strip().lower()
    if confidence not in {"high", "medium", "low"}:
        confidence = "low"

    return {
        "question_id": str(payload.get("question_id") or question["id"]).strip() or question["id"],
        "question": str(payload.get("question") or question["question"]).strip() or question["question"],
        "answer_summary": answer_summary,
        "key_findings": key_findings,
        "source_notes": normalized_sources,
        "confidence": confidence,
        "gaps": gaps,
    }


def fallback_finding(question: Dict[str, str], error_message: str) -> Dict[str, Any]:
    return {
        "question_id": question["id"],
        "question": question["question"],
        "answer_summary": "Research step failed for this sub-question.",
        "key_findings": [],
        "source_notes": [],
        "confidence": "low",
        "gaps": [error_message],
    }


def run_sub_question(
    client: Any,
    *,
    topic: str,
    language: str,
    question: Dict[str, str],
    research_depth: str,
    model: str,
    use_web_search: bool,
    web_tool_type: str,
    max_retries: int,
    max_output_tokens: int,
) -> Tuple[Dict[str, Any], str]:
    prompt = build_research_prompt(topic, language, question, research_depth)
    tools = None
    if use_web_search:
        tools = [{"type": web_tool_type}]

    response = call_responses_api(
        client,
        model=model,
        input_text=prompt,
        tools=tools,
        max_retries=max_retries,
        max_output_tokens=max_output_tokens,
    )
    raw_text = response_to_text(response)
    parsed = extract_json_object(raw_text)
    finding = normalize_finding(question, parsed)
    return finding, raw_text


def build_synthesis_prompt(
    topic: str,
    language: str,
    plan: Dict[str, Any],
    findings: List[Dict[str, Any]],
) -> str:
    plan_json = json.dumps(plan, ensure_ascii=False, indent=2)
    findings_json = json.dumps(findings, ensure_ascii=False, indent=2)

    return textwrap.dedent(
        f"""
        You are a principal research analyst.
        Synthesize the provided evidence into a final decision-quality report.

        Topic: {topic}
        Language tag: {language}

        Research plan JSON:
        {plan_json}

        Evidence JSON:
        {findings_json}

        Output markdown only.

        Required sections:
        1. # Executive Summary
        2. # Key Findings
        3. # Evidence by Sub-question
        4. # Contradictions and Uncertainty
        5. # Recommendations
        6. # Sources

        Rules:
        - Use language tag {language} for all narrative text.
        - Cite sources inline with markdown links, for example [World Bank](https://...).
        - Do not invent sources that are not in Evidence JSON.
        - Explicitly call out weak evidence and unresolved gaps.
        - Keep recommendation statements specific and actionable.
        """
    ).strip()


def collect_source_bullets(findings: List[Dict[str, Any]]) -> List[str]:
    bullets: List[str] = []
    seen_urls = set()
    for finding in findings:
        sources = finding.get("source_notes")
        if not isinstance(sources, list):
            continue
        for source in sources:
            if not isinstance(source, dict):
                continue
            url = str(source.get("url") or "").strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            title = str(source.get("title") or "Source").strip() or "Source"
            bullets.append(f"- [{title}]({url})")
    if not bullets:
        bullets.append("- No validated sources were extracted.")
    return bullets


def strip_markdown_fence_wrapper(report: str) -> str:
    text = report.strip()
    fenced_match = re.match(r"^```[a-zA-Z0-9_-]*\n(.*)\n```$", text, re.DOTALL)
    if fenced_match:
        return fenced_match.group(1).strip()
    return text


def ensure_markdown_report(report: str, findings: List[Dict[str, Any]], language: str) -> str:
    text = strip_markdown_fence_wrapper(report)
    if not text:
        text = "# Executive Summary\nNo content was generated."

    if not re.search(r"(?m)^#\s+", text):
        text = "# Executive Summary\n" + text

    missing: List[str] = []
    for heading in REQUIRED_REPORT_SECTIONS:
        heading_text = heading[2:]
        if not re.search(rf"(?mi)^#\s+{re.escape(heading_text)}\s*$", text):
            missing.append(heading)

    if not missing:
        return text

    print(
        f"[warn] Missing required report sections: {', '.join(missing)}. Appending placeholders.",
        file=sys.stderr,
    )

    placeholder = (
        "待补充：模型本轮未输出该章节，请二次补全。"
        if language.lower().startswith("zh")
        else "TODO: model did not provide this section. Complete in follow-up pass."
    )

    addition_lines: List[str] = []
    for heading in missing:
        addition_lines.append("")
        addition_lines.append(heading)
        if heading == "# Sources":
            addition_lines.extend(collect_source_bullets(findings))
        else:
            addition_lines.append(placeholder)

    return text.rstrip() + "\n" + "\n".join(addition_lines).rstrip()


def build_dry_run_artifacts(topic: str, language: str, depth: int) -> Tuple[Dict[str, Any], List[Dict[str, Any]], str]:
    sub_questions = []
    findings = []

    for i in range(1, depth + 1):
        question = {
            "id": f"Q{i}",
            "question": f"{topic}: analysis dimension {i}",
            "why_it_matters": "Dry-run placeholder scope.",
            "search_query": f"{topic} dimension {i}",
        }
        sub_questions.append(question)
        findings.append(
            {
                "question_id": question["id"],
                "question": question["question"],
                "answer_summary": "Dry-run mode: no real API call made.",
                "key_findings": [
                    "This is a placeholder finding.",
                    "Install dependencies and rerun without --dry-run for real evidence.",
                ],
                "source_notes": [
                    {
                        "title": "Placeholder source",
                        "url": "https://example.com",
                        "publisher": "example",
                        "published_date": "unknown",
                        "evidence": "Dry-run placeholder evidence.",
                        "reliability": "low",
                    }
                ],
                "confidence": "low",
                "gaps": ["No real data in dry-run mode."],
            }
        )

    plan = {
        "research_goal": f"Dry-run plan for topic: {topic}",
        "sub_questions": sub_questions,
        "final_report_outline": [
            "Executive Summary",
            "Evidence by Sub-question",
            "Recommendations",
        ],
    }

    lines = [
        "# Executive Summary",
        f"Dry-run mode completed for topic: **{topic}**.",
        "",
        "# Key Findings",
        "- No real model or web-search calls were made.",
        f"- Generated {depth} placeholder sub-questions.",
        "",
        "# Evidence by Sub-question",
    ]
    for item in findings:
        lines.extend(
            [
                f"## {item['question_id']}",
                item["answer_summary"],
            ]
        )
    lines.extend(
        [
            "",
            "# Contradictions and Uncertainty",
            "- All findings are placeholders and should not be used for decisions.",
            "",
            "# Recommendations",
            "1. Install dependencies from `scripts/requirements.txt`.",
            "2. Configure `OPENAI_API_KEY`.",
            "3. Rerun without `--dry-run`.",
            "",
            "# Sources",
            "- [Placeholder source](https://example.com)",
        ]
    )
    report = "\n".join(lines)

    return plan, findings, report


def main() -> int:
    args = parse_args()
    token_estimate = estimate_max_output_tokens(
        depth=args.depth,
        planner_max_output_tokens=args.planner_max_output_tokens,
        research_max_output_tokens=args.research_max_output_tokens,
        writer_max_output_tokens=args.writer_max_output_tokens,
    )
    if (
        args.max_total_output_tokens
        and token_estimate["estimated_total"] > args.max_total_output_tokens
    ):
        print(
            "[error] Estimated max output tokens exceed --max-total-output-tokens: "
            f"{token_estimate['estimated_total']} > {args.max_total_output_tokens}",
            file=sys.stderr,
        )
        return 1

    run_dir = make_run_dir(args.output_dir, args.topic)

    metadata = {
        "topic": args.topic,
        "language": args.language,
        "depth": args.depth,
        "research_depth": args.research_depth,
        "parallel": args.parallel,
        "planner_model": args.planner_model,
        "research_model": args.research_model,
        "writer_model": args.writer_model,
        "planner_max_output_tokens": args.planner_max_output_tokens,
        "research_max_output_tokens": args.research_max_output_tokens,
        "writer_max_output_tokens": args.writer_max_output_tokens,
        "max_total_output_tokens": args.max_total_output_tokens,
        "token_estimate": token_estimate,
        "web_search_enabled": not args.disable_web_search,
        "web_tool_type": args.web_tool_type,
        "dry_run": args.dry_run,
        "created_at": dt.datetime.now().isoformat(),
    }
    write_json(run_dir / "run_meta.json", metadata)
    print(
        "[info] Estimated max output tokens "
        f"(planner + depth*research + writer): "
        f"{token_estimate['planner']} + {token_estimate['research_total']} + "
        f"{token_estimate['writer']} = {token_estimate['estimated_total']}"
    )

    if args.dry_run:
        plan, findings, report = build_dry_run_artifacts(args.topic, args.language, args.depth)
        report = ensure_markdown_report(report, findings, args.language)
        write_json(run_dir / "plan.json", plan)
        write_json(run_dir / "findings.json", {"findings": findings})
        write_text(run_dir / "report.md", report)
        print(f"[ok] Dry-run artifacts created: {run_dir}")
        return 0

    try:
        client = load_openai_client(args.api_key, args.base_url, args.timeout)

        print("[info] Planning research scope...")
        plan_response = call_responses_api(
            client,
            model=args.planner_model,
            input_text=build_plan_prompt(args.topic, args.depth, args.language),
            tools=None,
            max_retries=args.max_retries,
            max_output_tokens=args.planner_max_output_tokens,
        )
        plan_raw_text = response_to_text(plan_response)
        plan_payload = extract_json_object(plan_raw_text)
        plan = normalize_plan(plan_payload, args.topic, args.depth)

        write_text(run_dir / "plan_raw.txt", plan_raw_text)
        write_json(run_dir / "plan.json", plan)

        sub_questions = plan["sub_questions"]
        results: List[Optional[Dict[str, Any]]] = [None] * len(sub_questions)
        raw_by_question: Dict[str, str] = {}

        print(f"[info] Researching {len(sub_questions)} sub-questions...")

        if args.parallel == 1:
            for idx, question in enumerate(sub_questions):
                try:
                    finding, raw_text = run_sub_question(
                        client,
                        topic=args.topic,
                        language=args.language,
                        question=question,
                        research_depth=args.research_depth,
                        model=args.research_model,
                        use_web_search=not args.disable_web_search,
                        web_tool_type=args.web_tool_type,
                        max_retries=args.max_retries,
                        max_output_tokens=args.research_max_output_tokens,
                    )
                except Exception as exc:
                    finding = fallback_finding(question, str(exc))
                    raw_text = f"ERROR: {exc}"

                results[idx] = finding
                raw_by_question[question["id"]] = raw_text
                print(f"[info] Completed {question['id']}: {question['question']}")
        else:
            with ThreadPoolExecutor(max_workers=args.parallel) as executor:
                future_map = {
                    executor.submit(
                        run_sub_question,
                        client,
                        topic=args.topic,
                        language=args.language,
                        question=question,
                        research_depth=args.research_depth,
                        model=args.research_model,
                        use_web_search=not args.disable_web_search,
                        web_tool_type=args.web_tool_type,
                        max_retries=args.max_retries,
                        max_output_tokens=args.research_max_output_tokens,
                    ): (idx, question)
                    for idx, question in enumerate(sub_questions)
                }

                for future in as_completed(future_map):
                    idx, question = future_map[future]
                    try:
                        finding, raw_text = future.result()
                    except Exception as exc:
                        finding = fallback_finding(question, str(exc))
                        raw_text = f"ERROR: {exc}"

                    results[idx] = finding
                    raw_by_question[question["id"]] = raw_text
                    print(f"[info] Completed {question['id']}: {question['question']}")

        findings = [item for item in results if item is not None]
        write_json(run_dir / "findings.json", {"findings": findings})
        write_json(run_dir / "research_raw.json", raw_by_question)

        print("[info] Synthesizing final report...")
        synthesis_response = call_responses_api(
            client,
            model=args.writer_model,
            input_text=build_synthesis_prompt(args.topic, args.language, plan, findings),
            tools=None,
            max_retries=args.max_retries,
            max_output_tokens=args.writer_max_output_tokens,
        )
        report = response_to_text(synthesis_response)
        report = ensure_markdown_report(report, findings, args.language)
        write_text(run_dir / "report.md", report)

        print(f"[ok] Research report generated: {run_dir / 'report.md'}")
        print(f"[ok] All artifacts directory: {run_dir}")
        return 0

    except DeepResearchError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        print(f"[error] Partial artifacts directory: {run_dir}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
