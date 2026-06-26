#!/usr/bin/env python3
"""Build a Moltbook evidence pack for keyword-driven research."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_BASE_URL = "https://www.moltbook.com/api/v1"
DEFAULT_SITE_URL = "https://www.moltbook.com"
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
DEFAULT_DIGEST_FILENAME = "digest.md"
DEFAULT_EVIDENCE_FILENAME = "evidence.json"
DEFAULT_ANALYSIS_INPUT_FILENAME = "analysis_input.md"
DEFAULT_ANALYSIS_REPORT_FILENAME = "analysis_report.md"
DEFAULT_AGENT_HANDOFF_FILENAME = "agent_handoff.md"
DEFAULT_ANALYSIS_SYSTEM_PROMPT = (
    "You are a rigorous Moltbook research analyst. Use only the provided evidence, avoid hallucinations, "
    "distinguish facts from inference, and explicitly call out uncertainty and data limits."
)
DEFAULT_ANALYSIS_LANGUAGE = "zh-CN"
DEFAULT_ANALYSIS_QUESTION_TEMPLATE = (
    "Analyze Moltbook discussions around: {queries}. "
    "Extract core themes, disagreements, risks, and practical actions."
)
DEFAULT_ANALYSIS_QUESTION_TEMPLATE_ZH = (
    "分析 Moltbook 上围绕 {queries} 的讨论。"
    "提炼核心主题、分歧、风险与可执行建议。"
)
DEFAULT_FEED_ANALYSIS_QUESTION_TEMPLATE = (
    "Analyze the Moltbook {feed_sort} feed{scope_suffix}. "
    "Extract the most important themes, changes, signals, and follow-up actions from this tracked snapshot."
)
DEFAULT_FEED_ANALYSIS_QUESTION_TEMPLATE_ZH = (
    "分析 Moltbook 的 {feed_sort} 信息流{scope_suffix}。"
    "从这次追踪快照中提炼最重要的主题、变化信号与后续行动。"
)
DEFAULT_ANALYSIS_CONTRACT_TEMPLATE = """Research question: {analysis_question}
User preferred language: {analysis_language}
Hard requirement: Write the final report in {analysis_language}.

You must follow this workflow:
1) First summarize the corpus before deep analysis:
   - For each key post, extract its central claim and contribution.
   - Then extract common patterns and distinctive differences across posts.
   - Organize per-post summaries in a Related Work style.
   - For each work, cover problem/context, approach, contribution, and limitations.
   - Explain how each work relates to the user problem and to other works.
   - Use short post reference tags such as `[P1]`, `[P2]`, `[P3]` to organize each per-post block.
   - Do not use placeholder labels like Work A, Work B, Work C.
   - Write in natural human language with clear flow, simple wording, and varied sentence length.
   - Avoid repetitive AI-style phrasing, redundant wording, and em dash punctuation.
   - Prefer short paragraphs over bullet-only dumps in analytical sections.
2) Then apply first-principles reasoning:
   - Restate the underlying user problem from goals/constraints/tradeoffs.
   - Do not assume the user is fully clear about goals or path.
   - If intent is ambiguous, explicitly list assumptions and alternative interpretation paths.
3) Then perform deep interpretation:
   - Separate evidence from inference.
   - Explain causal mechanisms, not just conclusions.
   - Highlight contradictions, blind spots, and confidence limits.
4) End with actionable recommendations:
   - Prioritized actions.
   - What to ask the user next if key assumptions remain uncertain.

HARD OUTPUT FORMAT CONTRACT (must be followed exactly):
- Use these exact H2 section titles in this order:
  1) `## 1. Corpus summary`
  2) `## 2. First-principles framing`
  3) `## 3. Deep interpretation`
  4) `## 4. Confidence and blind spots`
  5) `## 5. Prioritized actions and follow-up questions`
- Under section 1, include exactly these H3 subsections:
  - `### 1.1 Related Work (per-post)`
  - `### 1.2 Common patterns`
  - `### 1.3 Distinctive differences`
- In `### 1.1 Related Work (per-post)`, organize each discussed post as a short prose block using its compact tag:
  - Example opening: `**[P1] Post title.**`
- Do not use level-4 headings such as `####` for per-post entries.
- Do not cite raw post UUIDs or long URLs in running prose.
- Use short post reference tags such as `[P1]`, `[P2]`, `[P3]` in the body when referring to posts.
- Put clickable post links only in the final `## References` section.
- End the report with `## References`, mapping each post tag to a clickable markdown link.
- Recommendations in section 5 must be a numbered list with priority labels (`[P1]`, `[P2]`...).
- Follow-up questions in section 5 must be a separate numbered list.
- Cite concrete evidence throughout using compact inline markers such as `[P1]`, `[P2]`, or `[P2 comment by author]`.
- If evidence is insufficient for any claim, say so explicitly and reduce confidence.
- Do not output meta text such as “I will follow the format” or “self-check”.

QUALITY GATE BEFORE FINAL OUTPUT:
- Verify all required H2/H3 headings exist.
- Verify each Related Work entry clearly uses a compact post tag such as `[P1]`.
- Verify no level-4 headings are used for per-post entries.
- Verify compact reference markers appear in every H2 section.
- Verify section 2 includes assumptions and alternatives.
- Verify section 3 includes tradeoffs/contradictions.
- Verify section 4 includes uncertainty and blind spots.
- Verify section 5 includes both prioritized actions and follow-up questions.
- Verify the final `## References` section exists and maps post tags to clickable links.

Reference structure:
{report_structure}
"""

DEFAULT_REPORT_STRUCTURE = "\n".join(
    [
        "## 1. Corpus summary",
        "### 1.1 Related Work (per-post)",
        "### 1.2 Common patterns",
        "### 1.3 Distinctive differences",
        "## 2. First-principles framing",
        "## 3. Deep interpretation",
        "## 4. Confidence and blind spots",
        "## 5. Prioritized actions and follow-up questions",
        "## References",
    ]
)
CONFIG_LANGUAGE_PLACEHOLDERS = {
    "__USER_PREFERRED_LANGUAGE__",
    "<USER_PREFERRED_LANGUAGE>",
    "<SET_USER_LANGUAGE>",
    "__ASK_USER__",
}
DEFAULT_LLM_CONFIG_PATH = "config.yaml"
SUPPORTED_PROVIDERS = (
    "agent",
    "openai",
    "claude",
    "gemini",
    "siliconflow",
    "minimax",
    "volcengine",
)
PROVIDER_DEFAULTS = {
    "agent": {"analysis_mode": "agent"},
    "openai": {"analysis_mode": "litellm", "model": "openai/gpt-4.1-mini", "api_key_env": "OPENAI_API_KEY"},
    "claude": {
        "analysis_mode": "litellm",
        "model": "anthropic/claude-3-7-sonnet-latest",
        "api_key_env": "ANTHROPIC_API_KEY",
    },
    "gemini": {"analysis_mode": "litellm", "model": "gemini/gemini-2.0-flash", "api_key_env": "GEMINI_API_KEY"},
    "siliconflow": {
        "analysis_mode": "litellm",
        "model": "openai/Qwen/Qwen2.5-72B-Instruct",
        "api_key_env": "SILICONFLOW_API_KEY",
        "api_base": "https://api.siliconflow.cn/v1",
    },
    "minimax": {
        "analysis_mode": "litellm",
        "model": "openai/MiniMax-Text-01",
        "api_key_env": "MINIMAX_API_KEY",
        "api_base": "https://api.minimax.chat/v1",
    },
    "volcengine": {
        "analysis_mode": "litellm",
        "model": "openai/doubao-1.5-pro-32k-250115",
        "api_key_env": "ARK_API_KEY",
        "api_base": "https://ark.cn-beijing.volces.com/api/v3",
    },
}


def normalize_output_language(language: str | None) -> str:
    value = str(language or "").strip().lower()
    if value.startswith("zh"):
        return "zh-CN"
    return "en"


def is_chinese_output(language: str | None) -> bool:
    return normalize_output_language(language) == "zh-CN"


def pick_text(language: str | None, english: str, chinese: str) -> str:
    return chinese if is_chinese_output(language) else english


class ApiRequestError(RuntimeError):
    """Recoverable API request error for per-item fault tolerance."""


def init_diagnostics() -> dict[str, Any]:
    return {
        "search_request_failures": 0,
        "post_fetch_failures": 0,
        "comment_fetch_failures": 0,
        "warnings": [],
    }


def add_warning(diagnostics: dict[str, Any], message: str) -> None:
    warnings = diagnostics.setdefault("warnings", [])
    if isinstance(warnings, list):
        warnings.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Collect Moltbook search hits, expanded posts, and comment context.",
    )
    parser.add_argument(
        "--query",
        action="append",
        dest="queries",
        default=[],
        help="Semantic search query. Repeat for broader coverage.",
    )
    parser.add_argument(
        "--collection-mode",
        choices=("search", "feed"),
        default="search",
        help="Collection entry point: semantic search research or trending feed digest.",
    )
    parser.add_argument(
        "--type",
        choices=("all", "posts", "comments"),
        default="all",
        help="What to search.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Search results per page and per query. Max 50.",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=1,
        help="Pages to fetch per query.",
    )
    parser.add_argument(
        "--feed-sort",
        choices=("hot", "new", "top", "rising"),
        default="hot",
        help="Trending feed sort order when --collection-mode=feed.",
    )
    parser.add_argument(
        "--max-posts",
        type=int,
        default=5,
        help="Maximum expanded posts to include in the evidence pack.",
    )
    parser.add_argument(
        "--comment-limit",
        type=int,
        default=10,
        help="Top-level comments to request per selected post.",
    )
    parser.add_argument(
        "--comment-sort",
        choices=("best", "new", "old"),
        default="best",
        help="Comment sort order for expanded posts.",
    )
    parser.add_argument(
        "--submolt",
        action="append",
        dest="submolts",
        default=[],
        help="Optional submolt filter. Repeat to allow multiple submolts.",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for output files. Defaults to output/moltbook-digest/<timestamp>-<slug>.",
    )
    parser.add_argument(
        "--history-dir",
        help="Optional directory for snapshot history. When set, the run saves a scope-specific snapshot and compares against the latest previous one.",
    )
    parser.add_argument(
        "--base-url",
        default=os.environ.get("MOLTBOOK_API_BASE", DEFAULT_BASE_URL),
        help="Override the API base URL.",
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("MOLTBOOK_API_KEY"),
        help="Optional API key. Read-only endpoints currently work without one.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="HTTP timeout in seconds.",
    )
    parser.add_argument(
        "--analysis-mode",
        choices=("none", "litellm", "agent", "auto"),
        default="none",
        help="How to interpret collected content: none, litellm, agent, or auto.",
    )
    parser.add_argument(
        "--analysis-question",
        help="Optional research question the interpretation should answer.",
    )
    parser.add_argument(
        "--analysis-language",
        default=None,
        help="Preferred language for analysis output. If omitted, uses analysis.default_language from config.",
    )
    parser.add_argument(
        "--analysis-comment-evidence-limit",
        type=int,
        default=12,
        help="Representative comments per post for analysis context.",
    )
    parser.add_argument(
        "--analysis-post-char-limit",
        type=int,
        default=12000,
        help="Character budget per post body in LLM mode; use 0 for no cap.",
    )
    parser.add_argument(
        "--analysis-context-char-limit",
        type=int,
        default=180000,
        help="Total character budget for LLM input context; use 0 for no cap.",
    )
    parser.add_argument(
        "--litellm-model",
        default=os.environ.get("LITELLM_MODEL"),
        help="Model name passed to LiteLLM, e.g. openai/gpt-4.1-mini.",
    )
    parser.add_argument(
        "--litellm-temperature",
        type=float,
        default=0.2,
        help="Temperature for LiteLLM completion.",
    )
    parser.add_argument(
        "--litellm-max-tokens",
        type=int,
        default=2800,
        help="Max output tokens for LiteLLM completion.",
    )
    parser.add_argument(
        "--litellm-system-prompt",
        default=os.environ.get("MOLTBOOK_ANALYSIS_SYSTEM_PROMPT", DEFAULT_ANALYSIS_SYSTEM_PROMPT),
        help="System prompt used by LiteLLM analysis mode.",
    )
    parser.add_argument(
        "--llm-config",
        "--config",
        dest="llm_config",
        default=DEFAULT_LLM_CONFIG_PATH,
        help="Path to config.yaml (used to resolve provider defaults and the analysis contract).",
    )
    parser.add_argument(
        "--active-provider",
        choices=SUPPORTED_PROVIDERS,
        help="Override provider from config file. If omitted, uses active_provider in config.",
    )
    return parser.parse_args()


def clean_text(value: Any) -> str:
    text = value or ""
    text = TAG_RE.sub("", str(text))
    return unescape(text).strip()


def one_line(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def is_secret_placeholder(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    if not text:
        return True
    return text.startswith("<") and text.endswith(">")


def is_language_placeholder(value: Any) -> bool:
    if value is None:
        return True
    text = str(value).strip()
    if not text:
        return True
    return text in CONFIG_LANGUAGE_PLACEHOLDERS


def clip(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def load_yaml_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "PyYAML is required to read llm config. Install dependencies with uv "
            "(for example: uv sync --project moltbook-digest)."
        ) from exc

    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Failed to parse llm config {path}: {exc}") from exc

    if payload is None:
        return {}
    if not isinstance(payload, dict):
        raise SystemExit(f"llm config {path} must be a mapping at the top level.")
    return payload


def resolve_active_provider(args: argparse.Namespace, llm_config: dict[str, Any]) -> str:
    if args.active_provider:
        return args.active_provider

    top_level = llm_config.get("active_provider")
    if isinstance(top_level, str) and top_level in SUPPORTED_PROVIDERS:
        return top_level

    defaults = llm_config.get("defaults") or {}
    default_provider = defaults.get("active_provider")
    if isinstance(default_provider, str) and default_provider in SUPPORTED_PROVIDERS:
        return default_provider

    return "agent"


def get_provider_config(llm_config: dict[str, Any], provider: str) -> dict[str, Any]:
    providers = llm_config.get("providers") or {}
    if isinstance(providers, dict):
        config = providers.get(provider) or {}
        if isinstance(config, dict):
            return config
    return {}


def resolve_provider_runtime(args: argparse.Namespace, llm_config: dict[str, Any]) -> dict[str, Any]:
    provider = resolve_active_provider(args, llm_config)
    preset = PROVIDER_DEFAULTS.get(provider, {})
    provider_cfg = get_provider_config(llm_config, provider)
    analysis_cfg = llm_config.get("analysis") if isinstance(llm_config.get("analysis"), dict) else {}
    runtime_mode = args.analysis_mode
    if runtime_mode == "auto":
        runtime_mode = preset.get("analysis_mode", "none")

    model = args.litellm_model or provider_cfg.get("model") or preset.get("model")
    api_base = provider_cfg.get("api_base") or preset.get("api_base")
    api_key_env = provider_cfg.get("api_key_env") or preset.get("api_key_env")
    raw_api_key = provider_cfg.get("api_key")
    api_key = None if is_secret_placeholder(raw_api_key) else str(raw_api_key).strip()
    if not api_key and isinstance(api_key_env, str) and api_key_env:
        api_key = os.environ.get(api_key_env)

    system_prompt = args.litellm_system_prompt
    cfg_system_prompt = provider_cfg.get("system_prompt")
    if cfg_system_prompt and args.litellm_system_prompt == DEFAULT_ANALYSIS_SYSTEM_PROMPT:
        system_prompt = str(cfg_system_prompt)
    contract_template = analysis_cfg.get("contract_template")
    if not contract_template:
        contract_template = DEFAULT_ANALYSIS_CONTRACT_TEMPLATE
    question_template = analysis_cfg.get("question_template")
    if not isinstance(question_template, str) or not question_template.strip():
        question_template = DEFAULT_ANALYSIS_QUESTION_TEMPLATE
    report_structure = analysis_cfg.get("report_structure")
    if not isinstance(report_structure, str) or not report_structure.strip():
        report_structure = DEFAULT_REPORT_STRUCTURE
    default_language = analysis_cfg.get("default_language")
    if not isinstance(default_language, str) or not default_language.strip():
        default_language = DEFAULT_ANALYSIS_LANGUAGE

    return {
        "provider": provider,
        "analysis_mode": runtime_mode,
        "litellm_model": model,
        "litellm_api_base": api_base,
        "litellm_api_key": api_key,
        "litellm_api_key_env": api_key_env,
        "litellm_system_prompt": system_prompt,
        "analysis_contract_template": str(contract_template),
        "analysis_question_template": str(question_template),
        "analysis_report_structure": str(report_structure),
        "analysis_default_language": str(default_language),
    }


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "query"


def parse_iso(value: str | None) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def api_get(
    base_url: str,
    path: str,
    params: dict[str, Any] | None,
    api_key: str | None,
    timeout: int,
    retries: int = 2,
) -> dict[str, Any]:
    query = urlencode({k: v for k, v in (params or {}).items() if v is not None})
    url = f"{base_url}{path}"
    if query:
        url = f"{url}?{query}"

    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    transient_http_codes = {408, 425, 429, 500, 502, 503, 504}
    backoff_seconds = 0.8

    for attempt in range(retries + 1):
        request = Request(url, headers=headers, method="GET")
        try:
            with urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            should_retry = exc.code in transient_http_codes and attempt < retries
            if should_retry:
                time.sleep(backoff_seconds * (2**attempt))
                continue
            raise ApiRequestError(format_http_error(exc.code, message, url)) from exc
        except URLError as exc:
            should_retry = attempt < retries
            if should_retry:
                time.sleep(backoff_seconds * (2**attempt))
                continue
            raise ApiRequestError(f"Network error while requesting {url}: {exc.reason}") from exc

    raise ApiRequestError(f"Request failed after retries: {url}")


def format_http_error(code: int, body: str, url: str) -> str:
    cleaned = body.strip()
    if cleaned.startswith("{"):
        try:
            payload = json.loads(cleaned)
            if isinstance(payload, dict):
                error = payload.get("error") or payload.get("message") or cleaned
                hint = payload.get("hint")
                if hint:
                    return f"HTTP {code} for {url}: {error}. Hint: {hint}"
                return f"HTTP {code} for {url}: {error}"
        except json.JSONDecodeError:
            pass
    return f"HTTP {code} for {url}: {clip(cleaned, 280)}"


def normalize_hit(hit: dict[str, Any], query: str) -> dict[str, Any]:
    score = hit.get("similarity")
    if score is None:
        score = hit.get("relevance")

    post_id = hit.get("post_id") or hit.get("id")
    relative_url = hit.get("url")
    if relative_url:
        url = relative_url if relative_url.startswith("http") else f"{DEFAULT_SITE_URL}{relative_url}"
    else:
        url = f"{DEFAULT_SITE_URL}/post/{post_id}"

    return {
        "id": hit.get("id"),
        "type": hit.get("type"),
        "query": query,
        "score_kind": "semantic",
        "title": clean_text(hit.get("title")),
        "content": clean_text(hit.get("content")),
        "score": score,
        "created_at": hit.get("created_at"),
        "post_id": post_id,
        "url": url,
        "author_name": clean_text((hit.get("author") or {}).get("name")),
        "submolt_name": clean_text((hit.get("submolt") or {}).get("name")),
        "submolt_display_name": clean_text((hit.get("submolt") or {}).get("display_name")),
        "post_title": clean_text((hit.get("post") or {}).get("title")),
    }


def normalize_feed_post(post: dict[str, Any], sort: str, rank: int) -> dict[str, Any]:
    author = post.get("author") or {}
    submolt = post.get("submolt") or {}
    post_id = post.get("id")
    title = clean_text(post.get("title"))
    content = clean_text(post.get("content"))
    return {
        "id": post_id,
        "post_id": post_id,
        "type": "feed",
        "query": f"feed:{sort}",
        "score_kind": "feed",
        "title": title,
        "content": content,
        "score": post.get("score", post.get("upvotes", 0)),
        "created_at": post.get("created_at"),
        "url": f"{DEFAULT_SITE_URL}/post/{post_id}",
        "author_name": clean_text(author.get("name")),
        "submolt_name": clean_text(submolt.get("name")),
        "submolt_display_name": clean_text(submolt.get("display_name", submolt.get("displayName"))),
        "post_title": title,
        "rank": rank,
    }


def collect_search_hits(args: argparse.Namespace, diagnostics: dict[str, Any]) -> list[dict[str, Any]]:
    all_hits: list[dict[str, Any]] = []

    for query in args.queries:
        cursor = None
        for page_index in range(args.pages):
            try:
                payload = api_get(
                    args.base_url,
                    "/search",
                    {
                        "q": query,
                        "type": args.type,
                        "limit": min(max(args.limit, 1), 50),
                        "cursor": cursor,
                    },
                    args.api_key,
                    args.timeout,
                )
            except ApiRequestError as exc:
                diagnostics["search_request_failures"] = int(diagnostics.get("search_request_failures", 0)) + 1
                add_warning(
                    diagnostics,
                    f"Search request failed for query `{query}` page `{page_index + 1}`: {exc}",
                )
                break

            for hit in payload.get("results", []):
                all_hits.append(normalize_hit(hit, query))

            if not payload.get("has_more") or not payload.get("next_cursor"):
                break
            cursor = payload["next_cursor"]

    return all_hits


def collect_feed_hits(args: argparse.Namespace, diagnostics: dict[str, Any]) -> list[dict[str, Any]]:
    all_hits: list[dict[str, Any]] = []
    cursor = None
    rank = 1

    for page_index in range(args.pages):
        try:
            payload = api_get(
                args.base_url,
                "/posts",
                {
                    "sort": args.feed_sort,
                    "limit": min(max(args.limit, 1), 50),
                    "cursor": cursor,
                    "submolt": args.submolts[0] if len(args.submolts) == 1 else None,
                },
                args.api_key,
                args.timeout,
            )
        except ApiRequestError as exc:
            diagnostics["search_request_failures"] = int(diagnostics.get("search_request_failures", 0)) + 1
            add_warning(
                diagnostics,
                f"Feed request failed for sort `{args.feed_sort}` page `{page_index + 1}`: {exc}",
            )
            break

        posts = payload.get("posts", [])
        for post in posts:
            all_hits.append(normalize_feed_post(post, args.feed_sort, rank))
            rank += 1

        if not payload.get("has_more") or not payload.get("next_cursor"):
            break
        cursor = payload["next_cursor"]

    return all_hits


def build_post_candidates(search_hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: dict[str, dict[str, Any]] = {}

    for hit in search_hits:
        post_id = hit["post_id"]
        if not post_id:
            continue

        candidate = candidates.setdefault(
            post_id,
            {
                "post_id": post_id,
                "best_score": float("-inf"),
                "matched_queries": set(),
                "search_hits": [],
                "latest_hit_at": hit.get("created_at"),
                "score_kind": hit.get("score_kind") or "semantic",
            },
        )
        candidate["best_score"] = max(candidate["best_score"], float(hit.get("score") or 0.0))
        candidate["matched_queries"].add(hit["query"])
        candidate["search_hits"].append(hit)
        if hit.get("score_kind") == "semantic":
            candidate["score_kind"] = "semantic"

        latest = hit.get("created_at")
        if parse_iso(latest) > parse_iso(candidate.get("latest_hit_at")):
            candidate["latest_hit_at"] = latest

    ranked = []
    for candidate in candidates.values():
        candidate["matched_queries"] = sorted(candidate["matched_queries"])
        candidate["search_hits"] = sorted(
            candidate["search_hits"],
            key=lambda item: (float(item.get("score") or 0.0), parse_iso(item.get("created_at"))),
            reverse=True,
        )
        ranked.append(candidate)

    ranked.sort(
        key=lambda item: (
            len(item["matched_queries"]),
            float(item["best_score"]),
            parse_iso(item.get("latest_hit_at")),
        ),
        reverse=True,
    )
    return ranked


def sanitize_post(post: dict[str, Any], evidence: dict[str, Any]) -> dict[str, Any]:
    author = post.get("author") or {}
    submolt = post.get("submolt") or {}
    score_kind = evidence.get("score_kind") or "semantic"
    top_hit = evidence["search_hits"][0] if evidence.get("search_hits") else {}
    return {
        "id": post.get("id"),
        "title": clean_text(post.get("title")),
        "content": clean_text(post.get("content")),
        "type": post.get("type"),
        "created_at": post.get("created_at"),
        "updated_at": post.get("updated_at"),
        "upvotes": post.get("upvotes", 0),
        "downvotes": post.get("downvotes", 0),
        "score": post.get("score", 0),
        "comment_count": post.get("comment_count", post.get("comments_count", 0)),
        "verification_status": post.get("verification_status"),
        "author": {
            "id": author.get("id"),
            "name": clean_text(author.get("name")),
            "description": clean_text(author.get("description")),
            "karma": author.get("karma"),
            "follower_count": author.get("followerCount", author.get("follower_count")),
            "following_count": author.get("followingCount", author.get("following_count")),
        },
        "submolt": {
            "id": submolt.get("id"),
            "name": clean_text(submolt.get("name")),
            "display_name": clean_text(submolt.get("display_name", submolt.get("displayName"))),
        },
        "url": f"{DEFAULT_SITE_URL}/post/{post.get('id')}",
        "matched_queries": evidence["matched_queries"],
        "best_score_kind": score_kind,
        "best_match_score": evidence["best_score"] if score_kind == "semantic" else None,
        "feed_rank": top_hit.get("rank") if score_kind == "feed" else None,
        "search_hits": evidence["search_hits"][:5],
    }


def sanitize_comment_tree(comments: list[dict[str, Any]], depth: int = 0) -> list[dict[str, Any]]:
    cleaned = []
    for comment in comments:
        author = comment.get("author") or {}
        replies = comment.get("replies") or []
        cleaned.append(
            {
                "id": comment.get("id"),
                "content": clean_text(comment.get("content")),
                "created_at": comment.get("created_at"),
                "upvotes": comment.get("upvotes", 0),
                "downvotes": comment.get("downvotes", 0),
                "score": comment.get("score", 0),
                "depth": depth,
                "author": {
                    "id": author.get("id"),
                    "name": clean_text(author.get("name")),
                },
                "replies": sanitize_comment_tree(replies, depth + 1),
            }
        )
    return cleaned


def flatten_comments(comments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    flat: list[dict[str, Any]] = []

    def _walk(nodes: list[dict[str, Any]]) -> None:
        for node in nodes:
            entry = {
                "id": node.get("id"),
                "content": node.get("content"),
                "created_at": node.get("created_at"),
                "upvotes": node.get("upvotes", 0),
                "downvotes": node.get("downvotes", 0),
                "score": node.get("score", 0),
                "depth": node.get("depth", 0),
                "author_name": clean_text((node.get("author") or {}).get("name")),
            }
            flat.append(entry)
            _walk(node.get("replies") or [])

    _walk(comments)
    return flat


def select_comment_samples(flat_comments: list[dict[str, Any]], limit: int = 5) -> list[dict[str, Any]]:
    if not flat_comments:
        return []

    selected: list[dict[str, Any]] = []
    seen: set[str] = set()
    by_score = sorted(
        flat_comments,
        key=lambda item: (item.get("score", 0), parse_iso(item.get("created_at"))),
        reverse=True,
    )
    by_newest = sorted(flat_comments, key=lambda item: parse_iso(item.get("created_at")), reverse=True)

    for pool in (by_score, by_newest):
        for item in pool:
            if not item["content"] or item["id"] in seen:
                continue
            selected.append(
                {
                    "id": item["id"],
                    "author_name": item["author_name"],
                    "content": item["content"],
                    "created_at": item["created_at"],
                    "score": item["score"],
                    "depth": item["depth"],
                }
            )
            seen.add(item["id"])
            if len(selected) >= limit:
                return selected

    return selected


def expand_posts(
    args: argparse.Namespace,
    candidates: list[dict[str, Any]],
    diagnostics: dict[str, Any],
) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    allowed_submolts = {name.lower() for name in args.submolts}

    for candidate in candidates:
        if len(selected) >= args.max_posts:
            break

        try:
            post_payload = api_get(
                args.base_url,
                f"/posts/{candidate['post_id']}",
                None,
                args.api_key,
                args.timeout,
            )
        except ApiRequestError as exc:
            diagnostics["post_fetch_failures"] = int(diagnostics.get("post_fetch_failures", 0)) + 1
            add_warning(diagnostics, f"Skipped post `{candidate['post_id']}` because post detail fetch failed: {exc}")
            continue

        post = post_payload.get("post") or {}
        submolt_name = clean_text(((post.get("submolt") or {}).get("name"))).lower()
        if allowed_submolts and submolt_name not in allowed_submolts:
            continue

        try:
            comments_payload = api_get(
                args.base_url,
                f"/posts/{candidate['post_id']}/comments",
                {"sort": args.comment_sort, "limit": args.comment_limit},
                args.api_key,
                args.timeout,
            )
        except ApiRequestError as exc:
            diagnostics["comment_fetch_failures"] = int(diagnostics.get("comment_fetch_failures", 0)) + 1
            add_warning(diagnostics, f"Post `{candidate['post_id']}` comments fetch failed; continuing with empty comments: {exc}")
            comments_payload = {"sort": args.comment_sort, "count": 0, "has_more": False, "comments": []}

        cleaned_tree = sanitize_comment_tree(comments_payload.get("comments", []))
        raw_comment_count = comments_payload.get("count")
        comment_count = raw_comment_count if isinstance(raw_comment_count, int) else len(cleaned_tree)

        selected.append(
            {
                "post": sanitize_post(post, candidate),
                "comments": {
                    "sort": comments_payload.get("sort", args.comment_sort),
                    "count": comment_count,
                    "has_more": comments_payload.get("has_more", False),
                    "items": cleaned_tree,
                },
            }
        )

    return selected


def build_stats(
    args: argparse.Namespace,
    search_hits: list[dict[str, Any]],
    selected_posts: list[dict[str, Any]],
) -> dict[str, Any]:
    submolt_counts: Counter[str] = Counter()
    author_counts: Counter[str] = Counter()
    created_ats: list[str] = []

    for item in selected_posts:
        post = item["post"]
        submolt = post["submolt"]["name"] or "unknown"
        author = post["author"]["name"] or "unknown"
        submolt_counts[submolt] += 1
        author_counts[author] += 1
        if post.get("created_at"):
            created_ats.append(post["created_at"])

    time_range = None
    if created_ats:
        ordered = sorted(created_ats, key=parse_iso)
        time_range = {"earliest": ordered[0], "latest": ordered[-1]}

    return {
        "collection_mode": args.collection_mode,
        "queries": args.queries,
        "search_type": args.type,
        "feed_sort": args.feed_sort,
        "pages_per_query": args.pages,
        "limit_per_page": args.limit,
        "requested_max_posts": args.max_posts,
        "comment_limit": args.comment_limit,
        "comment_sort": args.comment_sort,
        "submolt_filter": args.submolts,
        "raw_search_hits": len(search_hits),
        "unique_posts_from_hits": len({hit["post_id"] for hit in search_hits if hit.get("post_id")}),
        "selected_posts": len(selected_posts),
        "top_submolts": submolt_counts.most_common(10),
        "top_authors": author_counts.most_common(10),
        "time_range": time_range,
    }


def history_scope_key(args: argparse.Namespace) -> str:
    parts = [args.collection_mode]
    if args.collection_mode == "feed":
        parts.append(args.feed_sort)
    else:
        parts.append(slugify("-".join(args.queries)[:80]))
        parts.append(args.type)
    if args.submolts:
        parts.append("submolt-" + slugify("-".join(sorted(args.submolts))))
    return "-".join(part for part in parts if part)


def build_history_snapshot(pack: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    posts = []
    for rank, item in enumerate(pack["posts"], start=1):
        post = item["post"]
        posts.append(
            {
                "rank": rank,
                "id": post.get("id"),
                "title": post.get("title"),
                "url": post.get("url"),
                "author": (post.get("author") or {}).get("name"),
                "submolt": (post.get("submolt") or {}).get("name"),
                "score": post.get("score", 0),
                "upvotes": post.get("upvotes", 0),
                "comment_count": post.get("comment_count", 0),
                "created_at": post.get("created_at"),
            }
        )
    return {
        "generated_at": pack["generated_at"],
        "scope_key": history_scope_key(args),
        "collection_mode": args.collection_mode,
        "queries": args.queries,
        "feed_sort": args.feed_sort,
        "submolts": args.submolts,
        "posts": posts,
    }


def load_latest_history_snapshot(history_root: Path, scope_key: str) -> dict[str, Any] | None:
    latest_path = history_root / scope_key / "latest.json"
    if not latest_path.exists():
        return None
    try:
        payload = json.loads(latest_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return payload if isinstance(payload, dict) else None


def compare_history_snapshots(previous: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any] | None:
    if not previous:
        return None

    prev_posts = {post["id"]: post for post in previous.get("posts", []) if post.get("id")}
    curr_posts = {post["id"]: post for post in current.get("posts", []) if post.get("id")}

    new_posts = [curr_posts[post_id] for post_id in curr_posts.keys() - prev_posts.keys()]
    dropped_posts = [prev_posts[post_id] for post_id in prev_posts.keys() - curr_posts.keys()]

    rank_changes = []
    engagement_changes = []
    for post_id in curr_posts.keys() & prev_posts.keys():
        prev_post = prev_posts[post_id]
        curr_post = curr_posts[post_id]
        rank_delta = int(prev_post.get("rank", 0)) - int(curr_post.get("rank", 0))
        score_delta = int(curr_post.get("score", 0)) - int(prev_post.get("score", 0))
        comment_delta = int(curr_post.get("comment_count", 0)) - int(prev_post.get("comment_count", 0))
        if rank_delta:
            rank_changes.append(
                {
                    "id": post_id,
                    "title": curr_post.get("title"),
                    "url": curr_post.get("url"),
                    "previous_rank": prev_post.get("rank"),
                    "current_rank": curr_post.get("rank"),
                    "rank_delta": rank_delta,
                }
            )
        if score_delta or comment_delta:
            engagement_changes.append(
                {
                    "id": post_id,
                    "title": curr_post.get("title"),
                    "url": curr_post.get("url"),
                    "score_delta": score_delta,
                    "comment_delta": comment_delta,
                }
            )

    rank_changes.sort(key=lambda item: abs(int(item["rank_delta"])), reverse=True)
    engagement_changes.sort(
        key=lambda item: (abs(int(item["score_delta"])), abs(int(item["comment_delta"]))),
        reverse=True,
    )

    return {
        "previous_generated_at": previous.get("generated_at"),
        "current_generated_at": current.get("generated_at"),
        "new_posts": new_posts,
        "dropped_posts": dropped_posts,
        "rank_changes": rank_changes,
        "engagement_changes": engagement_changes,
    }


def save_history_snapshot(history_root: Path, scope_key: str, snapshot: dict[str, Any]) -> tuple[Path, Path]:
    scope_dir = history_root / scope_key
    snapshots_dir = scope_dir / "snapshots"
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    archive_path = snapshots_dir / f"{stamp}.json"
    latest_path = scope_dir / "latest.json"
    payload = json.dumps(snapshot, indent=2, ensure_ascii=True) + "\n"
    archive_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return archive_path, latest_path


def as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def natural_join(parts: list[str], language: str | None = None) -> str:
    cleaned = [part.strip() for part in parts if part and str(part).strip()]
    if not cleaned:
        return ""
    if is_chinese_output(language):
        if len(cleaned) == 1:
            return cleaned[0]
        if len(cleaned) == 2:
            return f"{cleaned[0]}和{cleaned[1]}"
        return "、".join(cleaned[:-1]) + f"和{cleaned[-1]}"
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"


def pluralize(
    count: int,
    singular: str,
    plural: str | None = None,
    language: str | None = None,
    zh_unit: str | None = None,
) -> str:
    if is_chinese_output(language):
        return f"{count}{zh_unit or singular}"
    label = singular if count == 1 else (plural or singular + "s")
    return f"{count} {label}"


def post_reference_tag(index: int) -> str:
    return f"P{index}"


def post_signal_penalty(post: dict[str, Any]) -> tuple[int, list[str]]:
    title = one_line(post.get("title") or "")
    body = clean_text(post.get("content") or "")
    alpha_chars = [char for char in title if char.isalpha()]
    upper_chars = [char for char in alpha_chars if char.isupper()]
    caps_ratio = (len(upper_chars) / len(alpha_chars)) if alpha_chars else 0.0
    emphatic_punctuation = title.count("!") + title.count("?")
    has_ellipsis = "..." in title
    body_length = len(body)
    comments = as_int(post.get("comment_count"))
    score = as_int(post.get("score"))

    penalty = 0
    notes: list[str] = []
    if body_length < 160:
        penalty += 8
        notes.append("very_short_body")
    elif body_length < 320:
        penalty += 4
        notes.append("fairly_short_body")
    if emphatic_punctuation >= 3 or has_ellipsis:
        penalty += 4
        notes.append("dramatic_punctuation")
    if caps_ratio >= 0.28 and len(alpha_chars) >= 12:
        penalty += 3
        notes.append("aggressive_casing")
    if body_length < 240 and score >= 50 and comments < 6:
        penalty += 3
        notes.append("shallow_discussion")

    return penalty, notes


def localize_signal_note(note: str, language: str | None = None) -> str:
    mapping = {
        "very_short_body": pick_text(language, "the post body is very short", "正文非常短"),
        "fairly_short_body": pick_text(language, "the post body is fairly short", "正文偏短"),
        "dramatic_punctuation": pick_text(language, "the title leans on dramatic punctuation", "标题较依赖夸张标点"),
        "aggressive_casing": pick_text(language, "the title leans on aggressive casing", "标题使用了较强的强调式大小写"),
        "shallow_discussion": pick_text(
            language,
            "visibility is higher than the current depth of discussion",
            "曝光度高于当前讨论深度",
        ),
    }
    return mapping.get(note, note)


def post_signal_caveat(post: dict[str, Any], language: str | None = None) -> str | None:
    penalty, notes = post_signal_penalty(post)
    if penalty < 7 or not notes:
        return None
    localized_notes = [localize_signal_note(note, language) for note in notes]
    if is_chinese_output(language):
        return "这条帖子更适合作为对照信号而不是主锚点，因为" + natural_join(localized_notes, language) + "。"
    return (
        "Treat this as a noisier signal than the stronger anchor posts in this run because "
        + natural_join(localized_notes, language)
        + "."
    )


def build_history_maps(comparison: dict[str, Any] | None) -> dict[str, Any]:
    comparison = comparison if isinstance(comparison, dict) else {}
    return {
        "new_ids": {post.get("id") for post in comparison.get("new_posts", []) if post.get("id")},
        "rank_changes": {
            post.get("id"): post for post in comparison.get("rank_changes", []) if post.get("id")
        },
        "engagement_changes": {
            post.get("id"): post for post in comparison.get("engagement_changes", []) if post.get("id")
        },
    }


def product_signal_score(post: dict[str, Any], history_maps: dict[str, Any]) -> int:
    post_id = post.get("id")
    matched_queries = post.get("matched_queries") or []
    score = as_int(post.get("score"))
    comments = as_int(post.get("comment_count"))
    total = score + min(comments, 60) + len(matched_queries) * 12

    best_match_score = post.get("best_match_score")
    if post.get("best_score_kind") == "semantic" and best_match_score is not None:
        try:
            total += int(float(best_match_score) * 25)
        except (TypeError, ValueError):
            pass
    feed_rank = as_int(post.get("feed_rank"))
    if feed_rank > 0:
        total += max(0, 12 - min(feed_rank, 12))

    if post_id in history_maps.get("new_ids", set()):
        total += 18

    rank_change = (history_maps.get("rank_changes") or {}).get(post_id) or {}
    engagement_change = (history_maps.get("engagement_changes") or {}).get(post_id) or {}
    total += min(max(as_int(rank_change.get("rank_delta")), 0) * 5, 20)
    total += min(max(as_int(engagement_change.get("score_delta")), 0), 15)
    total += min(max(as_int(engagement_change.get("comment_delta")), 0) * 2, 12)
    penalty, _ = post_signal_penalty(post)
    total -= min(penalty, 12)
    return total


def why_this_post_matters(post: dict[str, Any], history_maps: dict[str, Any], language: str | None = None) -> str:
    post_id = post.get("id")
    reasons: list[str] = []
    matched_queries = post.get("matched_queries") or []
    score = as_int(post.get("score"))
    comments = as_int(post.get("comment_count"))

    if post_id in history_maps.get("new_ids", set()):
        reasons.append(pick_text(language, "it is new since the previous tracked snapshot", "它是相对上一轮快照新出现的帖子"))

    rank_change = (history_maps.get("rank_changes") or {}).get(post_id) or {}
    if as_int(rank_change.get("rank_delta")) > 0:
        reasons.append(
            pick_text(
                language,
                f"it moved up from #{rank_change.get('previous_rank')} to #{rank_change.get('current_rank')}",
                f"它的排名从第 {rank_change.get('previous_rank')} 位上升到第 {rank_change.get('current_rank')} 位",
            )
        )

    engagement_change = (history_maps.get("engagement_changes") or {}).get(post_id) or {}
    if as_int(engagement_change.get("score_delta")) > 0 or as_int(engagement_change.get("comment_delta")) > 0:
        reasons.append(pick_text(language, "its engagement is still climbing", "它的互动还在继续上升"))

    feed_rank = as_int(post.get("feed_rank"))
    if feed_rank == 1:
        reasons.append(pick_text(language, "it is currently at the top of the feed snapshot", "它当前位于这次信息流快照的榜首"))
    elif 1 < feed_rank <= 3:
        reasons.append(pick_text(language, "it sits near the top of the current feed snapshot", "它当前位于这次信息流快照的前列"))

    if len(matched_queries) >= 2:
        reasons.append(
            pick_text(language, "it matched multiple queries and sits close to the center of the topic", "它同时命中多个查询，处在这次主题的中心位置")
        )
    elif post.get("best_score_kind") == "semantic" and post.get("best_match_score") not in (None, ""):
        try:
            if float(post.get("best_match_score") or 0.0) >= 0.65:
                reasons.append(pick_text(language, "it is a strong semantic match for this research scope", "它与这次研究范围有很强的语义匹配"))
        except (TypeError, ValueError):
            pass

    if comments >= 20:
        reasons.append(
            pick_text(language, "the comment thread is large enough to surface objections and practical nuance", "评论区足够大，能暴露反对意见和实践细节")
        )
    elif score >= 40:
        reasons.append(pick_text(language, "it stands out on score relative to this run", "它在本轮结果里的热度分数比较突出"))

    if not reasons:
        reasons.append(pick_text(language, "it is one of the stronger anchor posts in this run", "它是本轮结果里较强的锚点帖子之一"))

    caveat = post_signal_caveat(post, language)
    if caveat:
        reasons.append(
            pick_text(
                language,
                "it is still worth reading mainly as a contrast case rather than a primary anchor",
                "它仍然值得阅读，但更适合作为对照样本而不是主锚点",
            )
        )

    sentence = natural_join(reasons, language)
    if is_chinese_output(language):
        base = sentence + "。"
    else:
        base = sentence[:1].upper() + sentence[1:] + "."
    if caveat:
        return base + ("" if is_chinese_output(language) else " ") + caveat
    return base


def summarize_group_posts(items: list[dict[str, Any]], history_maps: dict[str, Any], limit: int = 3) -> str:
    ranked = sorted(
        items,
        key=lambda item: (
            product_signal_score(item["post"], history_maps),
            parse_iso(item["post"].get("created_at")),
        ),
        reverse=True,
    )
    return ", ".join(
        f"[{post['post'].get('title') or '(untitled)'}]({post['post'].get('url')})"
        for post in ranked[:limit]
    )


def render_reader_brief(pack: dict[str, Any], args: argparse.Namespace) -> list[str]:
    lines: list[str] = []
    language = args.analysis_language
    zh = is_chinese_output(language)
    stats = pack["stats"]
    items = pack["posts"]
    history = pack.get("history")
    comparison = history.get("comparison") if isinstance(history, dict) else None
    history_maps = build_history_maps(comparison)

    ranked_items = sorted(
        items,
        key=lambda item: (
            product_signal_score(item["post"], history_maps),
            parse_iso(item["post"].get("created_at")),
        ),
        reverse=True,
    )
    top_posts = ranked_items[:3]

    lines.append("## 阅读摘要" if zh else "## Reader Brief")
    lines.append("")
    lines.append("### 快速结论" if zh else "### Quick Take")
    lines.append("")
    if stats["collection_mode"] == "feed":
        if zh:
            lines.append(f"- 本次运行扫描了 Moltbook 的 `{stats['feed_sort']}` 信息流，并扩展了 {pluralize(stats['selected_posts'], 'post', language=language, zh_unit='篇帖子')}。")
        else:
            lines.append(
                f"- This run scanned the Moltbook `{stats['feed_sort']}` feed and expanded {pluralize(stats['selected_posts'], 'post', language=language)}."
            )
    else:
        query_text = ", ".join(f"`{query}`" for query in stats["queries"])
        if zh:
            lines.append(f"- 本次运行围绕 {query_text} 检索了 Moltbook，并扩展了 {pluralize(stats['selected_posts'], 'post', language=language, zh_unit='篇帖子')} 进行细读。")
        else:
            lines.append(
                f"- This run searched Moltbook for {query_text} and expanded {pluralize(stats['selected_posts'], 'post', language=language)} for close reading."
            )
    if stats["top_submolts"]:
        top_submolt_name, top_submolt_count = stats["top_submolts"][0]
        if zh:
            lines.append(f"- 讨论最集中在 `{top_submolt_name}`，其中包含 {pluralize(top_submolt_count, 'expanded post', language=language, zh_unit='篇已扩展帖子')}。")
        else:
            lines.append(
                f"- The discussion is most concentrated in `{top_submolt_name}`, which accounts for {pluralize(top_submolt_count, 'expanded post', language=language)}."
            )
    if comparison:
        if zh:
            lines.append(
                f"- 相比上一轮快照，这个范围内出现了 {pluralize(len(comparison.get('new_posts', [])), 'new post', language=language, zh_unit='篇新帖子')}、"
                f"{pluralize(len(comparison.get('rank_changes', [])), 'rank movement', language=language, zh_unit='处排名变化')}，以及"
                f"{pluralize(len(comparison.get('engagement_changes', [])), 'engagement shift', language=language, zh_unit='处互动变化')}。"
            )
        else:
            lines.append(
                f"- Since the previous snapshot, this scope shows {pluralize(len(comparison.get('new_posts', [])), 'new post', language=language)}, "
                f"{pluralize(len(comparison.get('rank_changes', [])), 'rank movement', language=language)}, and "
                f"{pluralize(len(comparison.get('engagement_changes', [])), 'engagement shift', language=language)}."
            )
    warnings = (pack.get("diagnostics") or {}).get("warnings") or []
    if warnings:
        if zh:
            lines.append(f"- 覆盖性提示：记录到了 `{len(warnings)}` 条非致命警告，因此这份摘要更适合用于方向判断，而不是完整覆盖。")
        else:
            lines.append(
                f"- Coverage caveat: `{len(warnings)}` non-fatal warnings were recorded, so treat this digest as directional rather than exhaustive."
            )
    else:
        lines.append("- 覆盖性提示：本次运行没有记录到非致命采集警告。" if zh else "- Coverage caveat: this run completed without non-fatal collection warnings.")
    lines.append("")

    lines.append("### 推荐深读" if zh else "### Recommended Deep Reads")
    lines.append("")
    if top_posts:
        for index, item in enumerate(top_posts, start=1):
            post = item["post"]
            lines.append(f"#### {index}. [{post.get('title') or '(untitled post)'}]({post.get('url')})")
            lines.append("")
            lines.append(f"{'为什么值得阅读' if zh else 'Why it is worth reading'}: {why_this_post_matters(post, history_maps, language)}")
            feed_rank_note = f", feed rank `{post['feed_rank']}`" if post.get("feed_rank") else ""
            if zh:
                zh_feed_rank_note = f"，信息流排名 `{post['feed_rank']}`" if post.get("feed_rank") else ""
                lines.append(
                    "信号快照："
                    f"分数 `{as_int(post.get('score'))}`，评论 `{as_int(post.get('comment_count'))}`，"
                    f"submolt `{post['submolt']['name'] or 'unknown'}`，作者 `{post['author']['name'] or 'unknown'}`"
                    f"{zh_feed_rank_note}。"
                )
            else:
                lines.append(
                    "Signal snapshot: "
                    f"score `{as_int(post.get('score'))}`, comments `{as_int(post.get('comment_count'))}`, "
                    f"submolt `{post['submolt']['name'] or 'unknown'}`, author `{post['author']['name'] or 'unknown'}`"
                    f"{feed_rank_note}."
                )
            caveat = post_signal_caveat(post, language)
            if caveat:
                lines.append(f"{'信号提示' if zh else 'Signal caveat'}: {caveat}")
            lines.append("")
    else:
        lines.append("- 本次没有帖子进入短名单。" if zh else "- No posts were expanded into the shortlist.")
        lines.append("")

    lines.append("### 主题地图" if zh else "### Topic Map")
    lines.append("")
    by_submolt: dict[str, list[dict[str, Any]]] = {}
    by_author: dict[str, list[dict[str, Any]]] = {}
    for item in items:
        post = item["post"]
        submolt = post["submolt"]["name"] or "unknown"
        author = post["author"]["name"] or "unknown"
        by_submolt.setdefault(submolt, []).append(item)
        by_author.setdefault(author, []).append(item)

    if by_submolt:
        lines.append("按 submolt 划分：" if zh else "By submolt:")
        for name, group in sorted(by_submolt.items(), key=lambda entry: len(entry[1]), reverse=True)[:3]:
            if zh:
                lines.append(f"- `{name}`（{pluralize(len(group), 'post', language=language, zh_unit='篇帖子')}）：{summarize_group_posts(group, history_maps)}")
            else:
                lines.append(f"- `{name}` ({pluralize(len(group), 'post', language=language)}): {summarize_group_posts(group, history_maps)}")
    if by_author:
        lines.append("按作者划分：" if zh else "By author:")
        for name, group in sorted(by_author.items(), key=lambda entry: len(entry[1]), reverse=True)[:3]:
            if zh:
                lines.append(f"- `{name}`（{pluralize(len(group), 'post', language=language, zh_unit='篇帖子')}）：{summarize_group_posts(group, history_maps, limit=2)}")
            else:
                lines.append(f"- `{name}` ({pluralize(len(group), 'post', language=language)}): {summarize_group_posts(group, history_maps, limit=2)}")
    if items:
        highest_score = max(items, key=lambda item: as_int(item["post"].get("score")))
        most_discussed = max(items, key=lambda item: as_int(item["post"].get("comment_count")))
        lines.append("按互动划分：" if zh else "By engagement:")
        if zh:
            lines.append(
                f"- 分数最高：[{highest_score['post'].get('title') or '(untitled)'}]({highest_score['post'].get('url')})，"
                f"分数为 `{as_int(highest_score['post'].get('score'))}`。"
            )
            lines.append(
                f"- 讨论最多：[{most_discussed['post'].get('title') or '(untitled)'}]({most_discussed['post'].get('url')})，"
                f"共有 `{as_int(most_discussed['post'].get('comment_count'))}` 条评论。"
            )
        else:
            lines.append(
                f"- Highest score: [{highest_score['post'].get('title') or '(untitled)'}]({highest_score['post'].get('url')}) "
                f"with score `{as_int(highest_score['post'].get('score'))}`."
            )
            lines.append(
                f"- Most discussed: [{most_discussed['post'].get('title') or '(untitled)'}]({most_discussed['post'].get('url')}) "
                f"with `{as_int(most_discussed['post'].get('comment_count'))}` comments."
            )
    lines.append("")

    lines.append("### 观察清单" if zh else "### Watchlist")
    lines.append("")
    if comparison:
        if comparison.get("new_posts"):
            newest = comparison["new_posts"][:3]
            prefix = "- 新出现：" if zh else "- Newly surfaced: "
            lines.append(prefix + ", ".join(f"[{post.get('title') or '(untitled)'}]({post.get('url')})" for post in newest))
        if comparison.get("rank_changes"):
            movers = comparison["rank_changes"][:3]
            prefix = "- 排名变化：" if zh else "- Rank movers: "
            lines.append(
                prefix
                + ", ".join(
                    f"[{post.get('title') or '(untitled)'}]({post.get('url')}) "
                    f"`{post.get('previous_rank')} -> {post.get('current_rank')}`"
                    for post in movers
                )
            )
        if comparison.get("engagement_changes"):
            hot_now = comparison["engagement_changes"][:3]
            prefix = "- 互动变化：" if zh else "- Engagement movers: "
            if zh:
                lines.append(
                    prefix
                    + ", ".join(
                        f"[{post.get('title') or '(untitled)'}]({post.get('url')}) "
                        f"(分数 `+{as_int(post.get('score_delta'))}`，评论 `+{as_int(post.get('comment_delta'))}`)"
                        for post in hot_now
                    )
                )
            else:
                lines.append(
                    prefix
                    + ", ".join(
                        f"[{post.get('title') or '(untitled)'}]({post.get('url')}) "
                        f"(score `+{as_int(post.get('score_delta'))}`, comments `+{as_int(post.get('comment_delta'))}`)"
                        for post in hot_now
                    )
                )
        if not comparison.get("new_posts") and not comparison.get("rank_changes") and not comparison.get("engagement_changes"):
            lines.append("- 相比上一轮快照，没有检测到有意义的变化。" if zh else "- No meaningful changes were detected against the previous snapshot.")
    else:
        if top_posts:
            lines.append(
                "- 如果你想更快进入下一步，可以先从上面的首条深读开始，再决定其余帖子是否值得完整分析。"
                if zh
                else "- If you want a faster next step, start with the top deep read above and then decide whether the remaining posts deserve full analysis."
            )
        else:
            lines.append("- 这次运行还没有形成观察清单，因为没有得到短名单结果。" if zh else "- No watchlist yet because this run did not produce a shortlist.")
    lines.append("")
    return lines


def render_markdown(
    pack: dict[str, Any],
    args: argparse.Namespace,
    runtime: dict[str, Any],
) -> str:
    lines: list[str] = []
    language = args.analysis_language
    zh = is_chinese_output(language)
    stats = pack["stats"]
    diagnostics = pack.get("diagnostics") or {}
    warnings = diagnostics.get("warnings") if isinstance(diagnostics.get("warnings"), list) else []
    mode = runtime.get("analysis_mode") or "none"

    lines.append("# Moltbook 摘要" if zh else "# Moltbook Digest")
    lines.append("")
    lines.extend(render_reader_brief(pack, args))
    lines.append("## 运行概览" if zh else "## Run Summary")
    lines.append("")
    lines.append(f"- {'生成时间' if zh else 'Generated at'}: `{pack['generated_at']}`")
    lines.append(f"- {'分析模式' if zh else 'Analysis mode'}: `{mode}`")
    lines.append(f"- {'Provider 路由' if zh else 'Provider routing'}: `{runtime.get('provider')}`")
    lines.append(f"- {'采集模式' if zh else 'Collection mode'}: `{stats['collection_mode']}`")
    if stats["collection_mode"] == "search":
        query_text = ", ".join(f'`{query}`' for query in stats["queries"]) if stats["queries"] else "none"
        lines.append(f"- {'查询' if zh else 'Queries'}: {query_text}")
        lines.append(f"- {'搜索类型' if zh else 'Search type'}: `{stats['search_type']}`")
        lines.append(f"- {'原始搜索命中数' if zh else 'Raw search hits'}: `{stats['raw_search_hits']}`")
        lines.append(f"- {'去重后的帖子数' if zh else 'Unique posts from hits'}: `{stats['unique_posts_from_hits']}`")
    else:
        lines.append(f"- {'信息流排序' if zh else 'Feed sort'}: `{stats['feed_sort']}`")
        lines.append(f"- {'抓取到的信息流帖子数' if zh else 'Feed posts fetched'}: `{stats['raw_search_hits']}`")
    lines.append(f"- {'扩展帖子数' if zh else 'Expanded posts'}: `{stats['selected_posts']}`")
    lines.append("")
    lines.append("## 采集诊断" if zh else "## Collection Diagnostics")
    lines.append("")
    lines.append(f"- {'搜索请求失败数' if zh else 'Search request failures'}: `{diagnostics.get('search_request_failures', 0)}`")
    lines.append(f"- {'帖子详情拉取失败数' if zh else 'Post detail fetch failures'}: `{diagnostics.get('post_fetch_failures', 0)}`")
    lines.append(f"- {'评论拉取失败数' if zh else 'Comment fetch failures'}: `{diagnostics.get('comment_fetch_failures', 0)}`")
    if warnings:
        lines.append("非致命警告：" if zh else "Non-fatal warnings:")
        for warning in warnings[:8]:
            lines.append(f"- {'警告' if zh else 'Warning'}: {warning}")
        remaining = len(warnings) - 8
        if remaining > 0:
            lines.append(f"- {'另外还有' if zh else '... and'} `{remaining}` {'条警告' if zh else 'additional warnings'}")
    else:
        lines.append("- 非致命警告：无" if zh else "- Non-fatal warnings: none")
    lines.append("")
    lines.append("## 范围与覆盖" if zh else "## Scope & Coverage")
    lines.append("")
    if stats["submolt_filter"]:
        lines.append(f"- {'Submolt 过滤' if zh else 'Submolt filter'}: {', '.join(f'`{name}`' for name in stats['submolt_filter'])}")
    else:
        lines.append("- Submolt 过滤：无" if zh else "- Submolt filter: none")
    lines.append(f"- {'请求页数' if zh else 'Pages requested'}: `{stats['pages_per_query']}`")
    lines.append(f"- {'评论排序与上限' if zh else 'Comment sort and limit'}: `{stats['comment_sort']}` / `{stats['comment_limit']}`")
    if stats["top_submolts"]:
        lines.append(("- 热门 submolt：" if zh else "- Top submolts: ") + ", ".join(f"`{name}` ({count})" for name, count in stats["top_submolts"][:5]))
    if stats["top_authors"]:
        lines.append(("- 活跃作者：" if zh else "- Top authors: ") + ", ".join(f"`{name}` ({count})" for name, count in stats["top_authors"][:5]))
    if stats["time_range"]:
        if zh:
            lines.append(f"- 已扩展帖子的时间范围：`{stats['time_range']['earliest']}` 到 `{stats['time_range']['latest']}`")
        else:
            lines.append(
                f"- Time range across expanded posts: `{stats['time_range']['earliest']}` to `{stats['time_range']['latest']}`"
            )
    lines.append("")
    lines.append("## 建议继续追问的问题" if zh else "## Suggested Analytical Questions")
    lines.append("")
    if zh:
        lines.append("- 哪些主题在多篇帖子中反复出现，而不是只出现一次？")
        lines.append("- 哪些说法在评论区的碰撞之后仍然站得住？")
        lines.append("- 作者之间的分歧，哪些来自假设不同而不是事实不同？")
        lines.append("- 这份样本里还缺少哪些重要视角？")
    else:
        lines.append("- What themes recur across multiple posts instead of appearing only once?")
        lines.append("- Which claims survive contact with the comment threads?")
        lines.append("- Where do authors disagree because of different assumptions rather than different facts?")
        lines.append("- What important perspectives are still missing from this sample?")
    lines.append("")
    history = pack.get("history")
    comparison = history.get("comparison") if isinstance(history, dict) else None
    history_maps = build_history_maps(comparison)
    if isinstance(history, dict):
        lines.append("## 连续追踪" if zh else "## Continuity")
        lines.append("")
        lines.append(f"- {'历史范围' if zh else 'History scope'}: `{history.get('scope_key')}`")
        if history.get("saved_archive_path"):
            lines.append(f"- {'已保存快照' if zh else 'Saved snapshot'}: `{history.get('saved_archive_path')}`")
        if comparison:
            lines.append(f"- {'对比的上一轮快照时间' if zh else 'Compared with previous snapshot from'}: `{comparison.get('previous_generated_at')}`")
            lines.append(f"- {'新帖子' if zh else 'New posts'}: `{len(comparison.get('new_posts', []))}`")
            lines.append(f"- {'掉榜帖子' if zh else 'Dropped posts'}: `{len(comparison.get('dropped_posts', []))}`")
            lines.append(f"- {'排名变化' if zh else 'Rank changes'}: `{len(comparison.get('rank_changes', []))}`")
            lines.append(f"- {'互动变化' if zh else 'Engagement changes'}: `{len(comparison.get('engagement_changes', []))}`")
            if comparison.get("new_posts"):
                lines.append("新出现的帖子：" if zh else "Newly surfaced posts:")
                for post in comparison["new_posts"][:5]:
                    lines.append(f"- [{post.get('title') or '(untitled)'}]({post.get('url')})")
            if comparison.get("rank_changes"):
                lines.append("排名变化最大的帖子：" if zh else "Largest rank movements:")
                for post in comparison["rank_changes"][:5]:
                    direction = "up" if int(post.get("rank_delta", 0)) > 0 else "down"
                    if zh:
                        direction_label = "上升" if direction == "up" else "下降"
                        lines.append(
                            f"- [{post.get('title') or '(untitled)'}]({post.get('url')}) "
                            f"`{post.get('previous_rank')} -> {post.get('current_rank')}`（{direction_label}）"
                        )
                    else:
                        lines.append(
                            f"- [{post.get('title') or '(untitled)'}]({post.get('url')}) "
                            f"`{post.get('previous_rank')} -> {post.get('current_rank')}` ({direction})"
                        )
        else:
            lines.append("- 还没有上一轮快照。本次运行初始化了追踪基线。" if zh else "- No previous snapshot available yet. This run initialized the tracking baseline.")
        lines.append("")
    lines.append("## 完整证据帖子" if zh else "## Full Evidence Posts")
    lines.append("")

    for index, item in enumerate(pack["posts"], start=1):
        post = item["post"]
        comments = item["comments"]
        lines.append(f"### {index}. {post['title'] or '(untitled post)'}")
        lines.append("")
        lines.append(f"- {'链接' if zh else 'URL'}: {post['url']}")
        lines.append(f"- {'作者' if zh else 'Author'}: `{post['author']['name'] or 'unknown'}`")
        lines.append(f"- {'Submolt' if zh else 'Submolt'}: `{post['submolt']['name'] or 'unknown'}`")
        lines.append(f"- {'发布时间' if zh else 'Created at'}: `{post['created_at']}`")
        lines.append(f"- {'分数 / 评论' if zh else 'Score / comments'}: `{post['score']}` / `{post['comment_count']}`")
        if stats["collection_mode"] == "feed" and post.get("feed_rank"):
            lines.append(f"- {'信息流排名' if zh else 'Feed rank'}: `{post['feed_rank']}`")
        else:
            matched_queries = ", ".join(f'`{query}`' for query in post["matched_queries"]) if post["matched_queries"] else "n/a"
            lines.append(f"- {'命中的来源查询' if zh else 'Matched sources'}: {matched_queries}")
        if post.get("best_score_kind") == "semantic" and post.get("best_match_score") is not None:
            lines.append(f"- {'语义匹配分数' if zh else 'Semantic match score'}: `{post['best_match_score']}`")
        lines.append(f"- {'为什么重要' if zh else 'Why it matters'}: {why_this_post_matters(post, history_maps, language)}")
        caveat = post_signal_caveat(post, language)
        if caveat:
            lines.append(f"- {'信号提示' if zh else 'Signal caveat'}: {caveat}")
        lines.append("")
        if stats["collection_mode"] == "feed":
            lines.append("信息流证据：" if zh else "Feed evidence:")
            for hit in post["search_hits"]:
                excerpt = one_line(hit["content"] or hit["title"] or hit["post_title"])
                lines.append(
                    f"- [feed] sort=`{args.feed_sort}` rank=`{hit.get('rank', 'n/a')}` "
                    f"score=`{hit['score']}` excerpt={clip(excerpt, 180)}"
                )
        else:
            lines.append("搜索证据：" if zh else "Search evidence:")
            for hit in post["search_hits"]:
                excerpt = one_line(hit["content"] or hit["title"] or hit["post_title"])
                lines.append(
                    f"- [{hit['type']}] query=`{hit['query']}` score=`{hit['score']}` excerpt={clip(excerpt, 180)}"
                )
        lines.append("")
        lines.append("帖子正文：" if zh else "Post body:")
        lines.append("")
        lines.append("```text")
        lines.append(post["content"] or "")
        lines.append("```")
        lines.append("")
        lines.append(
            (
                f"代表性评论（共 `{comments.get('count', 0)}` 条评论，本处最多展示 `{args.analysis_comment_evidence_limit}` 条）："
                if zh
                else "Representative comments "
                f"(sampled from `{comments.get('count', 0)}` comments, capped at `{args.analysis_comment_evidence_limit}`):"
            )
        )
        sampled_comments = select_analysis_comments(comments["items"], args.analysis_comment_evidence_limit)
        if sampled_comments:
            for sample in sampled_comments:
                lines.append(
                    f"- depth={sample['depth']} score={sample['score']} author=`{sample['author_name'] or 'unknown'}`"
                )
                lines.append("")
                lines.append("```text")
                lines.append(sample["content"] or "")
                lines.append("```")
        else:
            lines.append("- 没有抽取到评论。" if zh else "- No comments sampled.")
        lines.append("")

    if mode == "agent":
        lines.append("## Agent 任务卡" if zh else "## Agent Task Card")
        lines.append("")
        lines.append("Agent 模式规则：不要只凭 digest 就起草报告。" if zh else "Agent mode rule: do not draft the report from the digest alone.")
        lines.append("")
        lines.append("不可协商的约束：" if zh else "Non-negotiable guardrails:")
        lines.append(f"- {'最终报告必须使用' if zh else 'The final report must be written in'} `{args.analysis_language}`{'。' if zh else '.'}")
        lines.append("- 如果任何段落漂移到其他语言，保存前必须改回目标语言。" if zh else "- If any drafted paragraph drifts into another language, rewrite it before saving the report.")
        lines.append("- 必须先读取 resolved analysis contract，不要凭记忆临时拼出替代契约。" if zh else "- Read the resolved analysis contract first. Do not improvise a substitute contract from memory.")
        lines.append("")
        lines.append("必需工作流：" if zh else "Required workflow:")
        lines.append(
            f"1. 开始写之前，先完整阅读 `{DEFAULT_AGENT_HANDOFF_FILENAME}` 里的 resolved analysis contract。"
            if zh
            else f"1. Read the resolved analysis contract in `{DEFAULT_AGENT_HANDOFF_FILENAME}` before writing anything."
        )
        lines.append("2. 把这份契约当作结构、风格和证据使用方式的唯一任务契约。" if zh else "2. Treat that contract as the canonical report contract for structure, style, and evidence use.")
        lines.append(
            f"3. 然后再阅读 `{DEFAULT_DIGEST_FILENAME}`、`{DEFAULT_EVIDENCE_FILENAME}` 和 `{DEFAULT_ANALYSIS_INPUT_FILENAME}`。"
            if zh
            else f"3. Then read `{DEFAULT_DIGEST_FILENAME}`, `{DEFAULT_EVIDENCE_FILENAME}`, and `{DEFAULT_ANALYSIS_INPUT_FILENAME}`."
        )
        lines.append("4. 如果契约缺失或无法读取，就停下来询问用户，不要自行发挥。" if zh else "4. If the contract is missing or unreadable, stop and ask the user instead of improvising.")
        lines.append("")
        lines.append(f"- {'报告文件' if zh else 'Report file'}: `{DEFAULT_ANALYSIS_REPORT_FILENAME}`")
        lines.append(f"- {'输出语言' if zh else 'Output language'}: `{args.analysis_language}`")
        lines.append(
            f"- {'完整的 resolved analysis contract 请阅读' if zh else 'Read the full resolved analysis contract in'} `{DEFAULT_AGENT_HANDOFF_FILENAME}`."
        )
        lines.append(
            f"- {'结构化证据语料请阅读' if zh else 'Read the structured evidence corpus in'} `{DEFAULT_ANALYSIS_INPUT_FILENAME}`."
        )
        lines.append("")

    lines.append("## 输出文件" if zh else "## Output Files")
    lines.append("")
    lines.append(f"- {'统一的 Markdown 摘要' if zh else 'Unified markdown digest'}: `{DEFAULT_DIGEST_FILENAME}`")
    lines.append(f"- {'完整归一化语料' if zh else 'Full normalized corpus'}: `{DEFAULT_EVIDENCE_FILENAME}`")
    if mode == "litellm":
        lines.append(f"- {'LLM 生成的报告' if zh else 'LLM-generated report'}: `{DEFAULT_ANALYSIS_REPORT_FILENAME}`")
    if mode == "agent":
        lines.append(
            f"- {'结构化分析语料' if zh else 'Structured analysis corpus'}: `{DEFAULT_ANALYSIS_INPUT_FILENAME}`"
        )
        lines.append(
            f"- {'分析契约' if zh else 'Analysis contract'}: `{DEFAULT_AGENT_HANDOFF_FILENAME}`"
        )
        lines.append(
            f"- {'最终报告目标路径（由调用该 skill 的 agent 写入）' if zh else 'Final report target (written by the calling agent)'}: `{DEFAULT_ANALYSIS_REPORT_FILENAME}`"
        )
    lines.append("")
    return "\n".join(lines)


def resolve_analysis_question(args: argparse.Namespace, runtime: dict[str, Any] | None = None) -> str:
    output_language = args.analysis_language or (runtime.get("analysis_default_language") if runtime else None)
    if args.analysis_question:
        return clean_text(args.analysis_question)
    if not args.queries and args.collection_mode == "feed":
        if is_chinese_output(output_language):
            scope_suffix = ""
            if args.submolts:
                scope_suffix = "，范围限定在 submolt " + ", ".join(args.submolts)
            template = DEFAULT_FEED_ANALYSIS_QUESTION_TEMPLATE_ZH
        else:
            scope_suffix = ""
            if args.submolts:
                scope_suffix = " within submolts " + ", ".join(args.submolts)
            template = DEFAULT_FEED_ANALYSIS_QUESTION_TEMPLATE
        return clean_text(
            template.format(
                feed_sort=args.feed_sort,
                scope_suffix=scope_suffix,
            )
        )
    template = None
    if runtime and isinstance(runtime.get("analysis_question_template"), str):
        template = runtime["analysis_question_template"]
    if not template or template == DEFAULT_ANALYSIS_QUESTION_TEMPLATE:
        template = (
            DEFAULT_ANALYSIS_QUESTION_TEMPLATE_ZH
            if is_chinese_output(output_language)
            else DEFAULT_ANALYSIS_QUESTION_TEMPLATE
        )
    queries = ", ".join(args.queries)
    try:
        return clean_text(template.format(queries=queries))
    except KeyError as exc:
        missing = str(exc).strip("'")
        raise SystemExit(
            "Invalid analysis.question_template in config: missing placeholder "
            f"{{{missing}}}. Allowed placeholder is {{queries}}."
        ) from exc


def apply_char_cap(text: str, limit: int, label: str) -> tuple[str, bool]:
    if limit <= 0 or len(text) <= limit:
        return text, False
    capped = text[:limit].rstrip()
    note = f"\n\n[TRUNCATED {label}: original {len(text)} chars, capped at {limit} chars]"
    return capped + note, True


def select_analysis_comments(comment_tree: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    flat = flatten_comments(comment_tree)
    if not flat:
        return []
    if limit <= 0 or len(flat) <= limit:
        return sorted(
            flat,
            key=lambda item: (item.get("score", 0), parse_iso(item.get("created_at"))),
            reverse=True,
        )
    return select_comment_samples(flat, limit)


def render_analysis_input(
    pack: dict[str, Any],
    args: argparse.Namespace,
    for_litellm: bool,
    runtime: dict[str, Any] | None = None,
) -> str:
    lines: list[str] = []
    language = args.analysis_language
    zh = is_chinese_output(language)
    stats = pack["stats"]
    question = resolve_analysis_question(args, runtime)

    lines.append("# Moltbook 分析输入" if zh else "# Moltbook Analysis Input")
    lines.append("")
    lines.append(f"- {'研究问题' if zh else 'Research question'}: {question}")
    lines.append(f"- {'偏好报告语言' if zh else 'Preferred report language'}: `{args.analysis_language}`")
    if stats["collection_mode"] == "feed":
        lines.append(f"- {'采集模式' if zh else 'Collection mode'}: `feed`")
        lines.append(f"- {'信息流排序' if zh else 'Feed sort'}: `{stats['feed_sort']}`")
    else:
        lines.append(f"- {'查询' if zh else 'Queries'}: {', '.join(f'`{query}`' for query in stats['queries'])}")
    lines.append(f"- {'扩展帖子数' if zh else 'Expanded posts'}: `{stats['selected_posts']}`")
    if stats["collection_mode"] == "feed":
        lines.append(f"- {'抓取到的信息流帖子数' if zh else 'Feed posts fetched'}: `{stats['raw_search_hits']}`")
    else:
        lines.append(f"- {'原始搜索命中数' if zh else 'Raw search hits'}: `{stats['raw_search_hits']}`")
    lines.append("")
    lines.append("## 方法提醒" if zh else "## Method Reminder")
    lines.append("")
    if zh:
        lines.append("- 只使用这个文件中的证据。")
        lines.append("- 把直接证据和推断分开。")
        lines.append("- 明确指出盲点和置信度边界。")
    else:
        lines.append("- Use only the evidence in this file.")
        lines.append("- Separate direct evidence from inference.")
        lines.append("- Call out blind spots and confidence limits.")
    lines.append("")
    history = pack.get("history")
    comparison = history.get("comparison") if isinstance(history, dict) else None
    if isinstance(history, dict):
        lines.append("## 连续追踪上下文" if zh else "## Continuity Context")
        lines.append("")
        lines.append(f"- {'历史范围' if zh else 'History scope'}: `{history.get('scope_key')}`")
        if comparison:
            lines.append(f"- {'上一轮快照时间' if zh else 'Previous snapshot time'}: `{comparison.get('previous_generated_at')}`")
            lines.append(f"- {'相对上一轮的新帖子' if zh else 'New posts since previous snapshot'}: `{len(comparison.get('new_posts', []))}`")
            lines.append(f"- {'相对上一轮掉榜的帖子' if zh else 'Dropped posts since previous snapshot'}: `{len(comparison.get('dropped_posts', []))}`")
            lines.append(f"- {'检测到的排名变化' if zh else 'Rank changes detected'}: `{len(comparison.get('rank_changes', []))}`")
            lines.append(f"- {'检测到的互动变化' if zh else 'Engagement changes detected'}: `{len(comparison.get('engagement_changes', []))}`")
        else:
            lines.append("- 还没有上一轮快照。这是初始化基线。" if zh else "- No previous snapshot available. This is the initial baseline.")
        lines.append("")
    lines.append("## 帖子引用索引" if zh else "## Post Reference Index")
    lines.append("")
    for index, item in enumerate(pack["posts"], start=1):
        post = item["post"]
        tag = post_reference_tag(index)
        lines.append(f"- [{tag}] [{post['title'] or '(untitled)'}]({post['url']})")
    lines.append("")
    lines.append(
        "在最终报告正文里使用这些短引用标签。不要在行文中直接粘贴原始 UUID 或长链接。"
        if zh
        else "Use these short post tags in the final report body. Do not paste raw UUIDs or long URLs into running prose."
    )
    lines.append(
        "可点击的帖子链接应统一放在最终 `## References` 部分，不要在 `### 1.1` 内重复展开。"
        if zh
        else "Keep clickable post links in the final `## References` section instead of repeating them inside section `### 1.1`."
    )
    lines.append("")
    lines.append("## 证据语料" if zh else "## Evidence Corpus")
    lines.append("")

    for index, item in enumerate(pack["posts"], start=1):
        post = item["post"]
        comments = item["comments"]
        tag = post_reference_tag(index)
        lines.append(f"### [{tag}] {post['title'] or '(untitled)'}")
        lines.append("")
        lines.append(f"- {'帖子引用标签' if zh else 'Post reference tag'}: `[{tag}]`")
        lines.append("- 规范链接：见上方帖子引用索引" if zh else "- Canonical link: see the Post Reference Index above")
        lines.append(f"- {'作者' if zh else 'Author'}: `{post['author']['name'] or 'unknown'}`")
        lines.append(f"- {'Submolt' if zh else 'Submolt'}: `{post['submolt']['name'] or 'unknown'}`")
        lines.append(f"- {'分数 / 评论' if zh else 'Score / comments'}: `{post['score']}` / `{post['comment_count']}`")
        if stats["collection_mode"] == "feed" and post.get("feed_rank"):
            lines.append(f"- {'信息流排名' if zh else 'Feed rank'}: `{post['feed_rank']}`")
        else:
            matched_queries = ", ".join(f'`{query}`' for query in post["matched_queries"]) if post["matched_queries"] else "n/a"
            lines.append(f"- {'命中的来源查询' if zh else 'Matched sources'}: {matched_queries}")
        if post.get("best_score_kind") == "semantic" and post.get("best_match_score") is not None:
            lines.append(f"- {'语义匹配分数' if zh else 'Semantic match score'}: `{post['best_match_score']}`")
        caveat = post_signal_caveat(post, language)
        if caveat:
            lines.append(f"- {'信号提示' if zh else 'Signal caveat'}: {caveat}")
        lines.append("")
        body = post["content"] or ""
        if for_litellm:
            body, _ = apply_char_cap(body, args.analysis_post_char_limit, "post body")
        lines.append("帖子正文：" if zh else "Post body:")
        lines.append("")
        lines.append("```text")
        lines.append(body)
        lines.append("```")
        lines.append("")

        sampled_comments = select_analysis_comments(comments["items"], args.analysis_comment_evidence_limit)
        lines.append(
            f"用于分析的代表性评论（`{len(sampled_comments)}` 条）："
            if zh
            else f"Representative comments for analysis (`{len(sampled_comments)}`):"
        )
        if not sampled_comments:
            lines.append("- 没有可用评论。" if zh else "- No comments available.")
            lines.append("")
            continue

        for sample in sampled_comments:
            lines.append(
                f"- Comment `{sample['id']}` depth=`{sample['depth']}` "
                f"score=`{sample['score']}` author=`{sample['author_name'] or 'unknown'}`"
            )
            comment_body = sample["content"] or ""
            if for_litellm:
                comment_body, _ = apply_char_cap(comment_body, 1500, "comment body")
            lines.append("")
            lines.append("```text")
            lines.append(comment_body)
            lines.append("```")
        lines.append("")

    rendered = "\n".join(lines)
    if for_litellm:
        rendered, _ = apply_char_cap(
            rendered,
            args.analysis_context_char_limit,
            "analysis context",
        )
    return rendered


def extract_litellm_text(response: Any) -> str:
    if isinstance(response, dict):
        choices = response.get("choices") or []
        if choices:
            message = choices[0].get("message") or {}
            content = message.get("content")
            return str(content or "").strip()

    choices = getattr(response, "choices", None)
    if choices:
        message = getattr(choices[0], "message", None)
        if message:
            content = getattr(message, "content", "")
            return str(content or "").strip()
    return ""


def build_analysis_contract(
    question: str,
    language: str,
    template: str,
    report_structure: str,
) -> str:
    try:
        return template.format(
            analysis_question=question,
            analysis_language=language,
            report_structure=report_structure,
        )
    except KeyError as exc:
        missing = str(exc).strip("'")
        raise SystemExit(
            "Invalid contract_template in config: missing placeholder "
            f"{{{missing}}}. Allowed placeholders are "
            "{analysis_question}, {analysis_language}, {report_structure}."
        ) from exc


def build_litellm_prompt(
    contract_text: str,
    analysis_input_text: str,
) -> str:
    return f"{contract_text}\n\nEvidence corpus:\n{analysis_input_text}"


def build_runtime_analysis_contract(
    args: argparse.Namespace,
    runtime: dict[str, Any],
) -> str:
    question = resolve_analysis_question(args, runtime)
    return build_analysis_contract(
        question,
        args.analysis_language,
        runtime.get("analysis_contract_template") or DEFAULT_ANALYSIS_CONTRACT_TEMPLATE,
        runtime.get("analysis_report_structure") or DEFAULT_REPORT_STRUCTURE,
    )


def build_runtime_litellm_prompt(
    args: argparse.Namespace,
    runtime: dict[str, Any],
    analysis_input_text: str,
) -> str:
    contract_text = build_runtime_analysis_contract(args, runtime)
    return build_litellm_prompt(
        contract_text,
        analysis_input_text,
    )


def run_litellm_analysis(args: argparse.Namespace, prompt: str, runtime: dict[str, Any]) -> str:
    try:
        from litellm import completion  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            "LiteLLM is required for LiteLLM analysis. Install dependencies with uv "
            "(for example: uv sync --project moltbook-digest)."
        ) from exc

    try:
        response = completion(
            model=runtime["litellm_model"],
            temperature=args.litellm_temperature,
            max_tokens=args.litellm_max_tokens,
            api_base=runtime.get("litellm_api_base"),
            api_key=runtime.get("litellm_api_key"),
            messages=[
                {"role": "system", "content": runtime.get("litellm_system_prompt") or args.litellm_system_prompt},
                {"role": "user", "content": prompt},
            ],
        )
    except Exception as exc:
        raise SystemExit(f"LiteLLM analysis call failed: {exc}") from exc

    content = extract_litellm_text(response).strip()
    if not content:
        raise SystemExit("LiteLLM returned an empty analysis response.")

    zh = is_chinese_output(args.analysis_language)
    header = "\n".join(
        [
            "# Moltbook 分析报告" if zh else "# Moltbook Analysis Report",
            "",
            f"- {'生成时间' if zh else 'Generated at'}: `{datetime.now(timezone.utc).isoformat()}`",
            f"- {'模式' if zh else 'Mode'}: `litellm`",
            f"- {'Provider' if zh else 'Provider'}: `{runtime.get('provider')}`",
            f"- {'模型' if zh else 'Model'}: `{runtime.get('litellm_model')}`",
            f"- {'语言' if zh else 'Language'}: `{args.analysis_language}`",
            "",
        ]
    )
    return header + content + "\n"


def validate_analysis_report(report_text: str) -> list[str]:
    issues: list[str] = []
    required_headings = [
        "## 1. Corpus summary",
        "### 1.1 Related Work (per-post)",
        "### 1.2 Common patterns",
        "### 1.3 Distinctive differences",
        "## 2. First-principles framing",
        "## 3. Deep interpretation",
        "## 4. Confidence and blind spots",
        "## 5. Prioritized actions and follow-up questions",
        "## References",
    ]
    for heading in required_headings:
        if heading not in report_text:
            issues.append(f"Missing required heading: {heading}")

    body, _, references = report_text.partition("\n## References")
    if re.search(r"^####\s+", body, flags=re.MULTILINE):
        issues.append("Per-post entries still use level-4 headings; use compact post tags in prose blocks instead.")
    if re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", body, flags=re.IGNORECASE):
        issues.append("Report body contains raw post UUIDs.")
    if re.search(r"https?://\S+", body):
        issues.append("Report body contains raw URLs outside the final references section.")

    h2_sections = re.findall(r"^##\s+.+?(?=^##\s+|\Z)", body, flags=re.MULTILINE | re.DOTALL)
    for section in h2_sections:
        heading = section.splitlines()[0].strip()
        if heading == "## References":
            continue
        if not re.search(r"\[P\d+\]", section):
            issues.append(f"{heading} does not contain any compact post reference tags.")

    referenced_tags = sorted(set(re.findall(r"\[P\d+\]", body)))
    if referenced_tags:
        for tag in referenced_tags:
            if tag not in references:
                issues.append(f"{tag} is used in the body but missing from the final references section.")

    return issues


def render_agent_handoff(
    args: argparse.Namespace,
    runtime: dict[str, Any],
    prompt_text: str,
) -> str:
    question = resolve_analysis_question(args, runtime)
    zh = is_chinese_output(args.analysis_language)
    lines = [
        "# Agent 深度解读交接单" if zh else "# Agent Handoff for Deep Interpretation",
        "",
        "## 目标" if zh else "## Objective",
        "",
        question,
        "",
        "## 路由" if zh else "## Routing",
        "",
        "- 分析路径：`agent`" if zh else "- Analysis path: `agent`",
        "- 模板策略：与 `litellm` 模式共享（`analysis.contract_template` + `analysis.report_structure`）"
        if zh
        else "- Template policy: shared with `litellm` mode (`analysis.contract_template` + `analysis.report_structure`)",
        f"- 报告文件：`{DEFAULT_ANALYSIS_REPORT_FILENAME}`，语言为 `{args.analysis_language}`"
        if zh
        else f"- Report file: `{DEFAULT_ANALYSIS_REPORT_FILENAME}` in `{args.analysis_language}`",
        "",
        "## 不可协商的约束" if zh else "## Non-negotiable Guardrails",
        "",
        f"- 最终报告必须使用 `{args.analysis_language}`。" if zh else f"- Write the final report in `{args.analysis_language}`.",
        "- 如果任何段落漂移到其他语言，保存前必须改回目标语言。" if zh else "- If any drafted paragraph drifts into another language, rewrite it before saving the report.",
        "- 不要凭记忆自行重构分析契约，直接使用这个文件里的 resolved 契约。" if zh else "- Do not improvise the analysis contract from memory. Use the resolved contract in this file.",
        "",
        "## 必需工作流" if zh else "## Required Workflow",
        "",
        "1. 在起草任何报告内容之前，先阅读这个文件里的 resolved 契约。" if zh else "1. Read the resolved contract in this file before drafting any report content.",
        "2. 把这份契约当作结构、风格、证据处理和引用方式的唯一任务契约。" if zh else "2. Treat that contract as the canonical task contract for structure, style, evidence handling, and references.",
        "3. 只有在读完契约之后，才去阅读 digest、evidence 和 analysis input 文件。" if zh else "3. Only after reading the contract should you read the digest, evidence, and analysis input files.",
        "4. 如果契约缺失或无法读取，就停下来询问用户，不要自行发挥。" if zh else "4. If the contract is missing or unreadable, stop and ask the user instead of improvising.",
        "",
        "## 需要读取的文件" if zh else "## Files to read",
        "",
        f"- `{DEFAULT_DIGEST_FILENAME}`",
        f"- `{DEFAULT_EVIDENCE_FILENAME}`",
        f"- `{DEFAULT_ANALYSIS_INPUT_FILENAME}`",
        "",
        "## 请先阅读的 Resolved Analysis Contract（与 LiteLLM 路径共享）" if zh else "## Resolved Analysis Contract To Read First (Shared with LiteLLM Path)",
        "",
        "```text",
        prompt_text,
        "```",
        "",
    ]
    return "\n".join(lines)


def default_output_dir(args: argparse.Namespace) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    if args.collection_mode == "feed":
        seed = f"feed-{args.feed_sort}"
        if args.submolts:
            seed += "-" + "-".join(args.submolts)
    else:
        seed = "-".join(args.queries)[:48]
    slug = slugify(seed[:48])
    return Path("output") / "moltbook-digest" / f"{stamp}-{slug}"


def write_outputs(
    pack: dict[str, Any],
    args: argparse.Namespace,
    runtime: dict[str, Any],
    output_dir: Path,
) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / DEFAULT_EVIDENCE_FILENAME
    brief_path = output_dir / DEFAULT_DIGEST_FILENAME
    json_path.write_text(json.dumps(pack, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    brief_path.write_text(
        render_markdown(pack, args, runtime) + "\n",
        encoding="utf-8",
    )
    return json_path, brief_path


def validate_args(args: argparse.Namespace) -> None:
    if args.collection_mode == "search" and not args.queries:
        raise SystemExit("--query is required when --collection-mode=search")
    if args.limit < 1 or args.limit > 50:
        raise SystemExit("--limit must be between 1 and 50")
    if args.pages < 1 or args.pages > 5:
        raise SystemExit("--pages must be between 1 and 5")
    if args.max_posts < 1 or args.max_posts > 25:
        raise SystemExit("--max-posts must be between 1 and 25")
    if args.comment_limit < 1 or args.comment_limit > 100:
        raise SystemExit("--comment-limit must be between 1 and 100")
    if not args.base_url.startswith("https://www.moltbook.com"):
        raise SystemExit("--base-url must point at https://www.moltbook.com")
    if args.analysis_comment_evidence_limit < 1:
        raise SystemExit("--analysis-comment-evidence-limit must be >= 1")
    if args.analysis_post_char_limit < 0:
        raise SystemExit("--analysis-post-char-limit must be >= 0")
    if args.analysis_context_char_limit < 0:
        raise SystemExit("--analysis-context-char-limit must be >= 0")
    if args.litellm_temperature < 0 or args.litellm_temperature > 2:
        raise SystemExit("--litellm-temperature must be between 0 and 2")
    if args.litellm_max_tokens < 64:
        raise SystemExit("--litellm-max-tokens must be >= 64")
def validate_runtime(args: argparse.Namespace, runtime: dict[str, Any]) -> None:
    mode = runtime["analysis_mode"]
    config_path = Path(args.llm_config)
    using_example_config = config_path.name == "config.example.yaml"
    if mode != "none":
        if not config_path.exists():
            raise SystemExit(
                "Interpretation requires a user-specific config.yaml. Copy `moltbook-digest/config.example.yaml` "
                "to `moltbook-digest/config.yaml`, then customize it for the user before rerunning."
            )
        if using_example_config:
            raise SystemExit(
                "Do not run interpretation directly from `config.example.yaml`. Copy it to `config.yaml`, then "
                "customize provider, language, and templates for the user before rerunning."
            )
        if is_language_placeholder(runtime.get("analysis_default_language")):
            raise SystemExit(
                "analysis.default_language is still a placeholder. Copy `config.example.yaml` to `config.yaml`, "
                "set the user's preferred language, and adapt the config before rerunning."
            )
    if mode == "litellm" and not runtime.get("litellm_model"):
        raise SystemExit(
            "LiteLLM mode requires a model. Set --litellm-model or configure model in config providers.<name>.model"
        )
    if mode == "litellm" and runtime.get("provider") != "agent":
        if not runtime.get("litellm_api_key"):
            env_name = runtime.get("litellm_api_key_env") or "provider API key env var"
            raise SystemExit(
                f"{runtime.get('provider')} requires API key. Set providers.{runtime.get('provider')}.api_key "
                f"or export {env_name}."
            )


def main() -> int:
    args = parse_args()
    validate_args(args)
    llm_config = load_yaml_file(Path(args.llm_config))
    runtime = resolve_provider_runtime(args, llm_config)
    if not args.analysis_language:
        args.analysis_language = runtime.get("analysis_default_language") or DEFAULT_ANALYSIS_LANGUAGE
    validate_runtime(args, runtime)
    diagnostics = init_diagnostics()

    hits = collect_search_hits(args, diagnostics) if args.collection_mode == "search" else collect_feed_hits(args, diagnostics)
    if not hits:
        warning_hint = ""
        warnings = diagnostics.get("warnings")
        if isinstance(warnings, list) and warnings:
            warning_hint = f" Last warning: {warnings[0]}"
        if args.collection_mode == "feed":
            raise SystemExit(
                "No feed posts returned. Try a different --feed-sort, provide API credentials if required, "
                f"or retry later.{warning_hint}"
            )
        raise SystemExit(f"No search hits returned. Try broader or more descriptive queries.{warning_hint}")

    candidates = build_post_candidates(hits)
    expanded_posts = expand_posts(args, candidates, diagnostics)
    if not expanded_posts:
        if args.collection_mode == "feed":
            raise SystemExit("No feed posts matched the current filters after expansion. Try removing the submolt filter or using another feed sort.")
        raise SystemExit("No posts matched the current filters after expansion. Try removing the submolt filter or broadening the query.")

    pack = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "api_base_url": args.base_url,
        "runtime": {
            "analysis_mode": runtime.get("analysis_mode"),
            "provider": runtime.get("provider"),
        },
        "stats": build_stats(args, hits, expanded_posts),
        "diagnostics": diagnostics,
        "search_hits": hits,
        "posts": expanded_posts,
    }

    if args.history_dir:
        history_root = Path(args.history_dir)
        snapshot = build_history_snapshot(pack, args)
        scope_key = snapshot["scope_key"]
        previous = load_latest_history_snapshot(history_root, scope_key)
        comparison = compare_history_snapshots(previous, snapshot)
        archive_path, latest_path = save_history_snapshot(history_root, scope_key, snapshot)
        pack["history"] = {
            "scope_key": scope_key,
            "saved_archive_path": str(archive_path),
            "latest_path": str(latest_path),
            "comparison": comparison,
        }

    output_dir = Path(args.output_dir) if args.output_dir else default_output_dir(args)
    json_path, brief_path = write_outputs(pack, args, runtime, output_dir)
    print(f"Wrote {brief_path}")
    print(f"Wrote {json_path}")
    if diagnostics.get("warnings"):
        print(
            "Completed with non-fatal warnings "
            f"(`{len(diagnostics['warnings'])}` total). See `diagnostics.warnings` in {json_path.name}."
        )

    if runtime["analysis_mode"] != "none":
        analysis_input_text = render_analysis_input(pack, args, for_litellm=False, runtime=runtime)
        analysis_input_path = output_dir / DEFAULT_ANALYSIS_INPUT_FILENAME
        analysis_input_path.write_text(analysis_input_text + "\n", encoding="utf-8")
        print(f"Wrote {analysis_input_path}")

        if runtime["analysis_mode"] == "litellm":
            llm_input = render_analysis_input(pack, args, for_litellm=True, runtime=runtime)
            llm_prompt = build_runtime_litellm_prompt(args, runtime, llm_input)
            report_text = run_litellm_analysis(args, llm_prompt, runtime)
            analysis_report_path = output_dir / DEFAULT_ANALYSIS_REPORT_FILENAME
            analysis_report_path.write_text(report_text, encoding="utf-8")
            print(f"Wrote {analysis_report_path}")
            validation_issues = validate_analysis_report(report_text)
            if validation_issues:
                print(
                    "Analysis report format warnings "
                    f"(`{len(validation_issues)}` total). Review the report structure before shipping it."
                )
                for issue in validation_issues[:8]:
                    print(f"- Format warning: {issue}")
                remaining = len(validation_issues) - 8
                if remaining > 0:
                    print(f"- ... and `{remaining}` additional format warnings")

        if runtime["analysis_mode"] == "agent":
            handoff_prompt = build_runtime_analysis_contract(args, runtime)
            handoff_path = output_dir / DEFAULT_AGENT_HANDOFF_FILENAME
            handoff_path.write_text(
                render_agent_handoff(args, runtime, handoff_prompt) + "\n",
                encoding="utf-8",
            )
            print(f"Wrote {handoff_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
