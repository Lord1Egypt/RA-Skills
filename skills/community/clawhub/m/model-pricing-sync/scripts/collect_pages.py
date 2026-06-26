from __future__ import annotations

import html
from concurrent.futures import ThreadPoolExecutor
import re
import time
from collections import defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError, sync_playwright

from _shared import (
    ARTIFACTS_DIR,
    COLLECT_ISSUE_FIELDS,
    SOURCE_PAGE_FIELDS,
    filter_vendor_configs,
    generate_run_dir,
    load_latest_run,
    load_target_api_models,
    load_target_subscription_plans,
    load_vendor_configs,
    parse_bool,
    read_json_data,
    safe_filename,
    save_latest_run,
    short_hash,
    utc_now,
    read_csv_rows,
    write_json_data,
    write_csv_rows,
)

MAIN_TAB_KEYWORDS = [
    "价格",
    "计费",
    "订阅",
    "模型",
    "API",
    "pricing",
    "Pricing",
    "price",
    "plans",
    "Plans",
    "套餐",
]

SUBSCRIPTION_CYCLE_KEYWORDS = [
    "月",
    "月付",
    "monthly",
    "Monthly",
    "季",
    "季度",
    "quarter",
    "quarterly",
    "Quarterly",
    "年",
    "年付",
    "annual",
    "Annual",
    "yearly",
    "Yearly",
]

SUBSCRIPTION_CYCLE_LABELS = [
    "连续包月",
    "连续包季",
    "连续包年",
    "月付",
    "季付",
    "年付",
    "按月计费",
    "按季计费",
    "按年计费",
    "Monthly",
    "Quarterly",
    "Yearly",
    "Annual",
]

REGION_KEYWORDS = [
    "中国",
    "中国内地",
    "全球",
    "国际",
    "global",
    "Global",
    "international",
    "International",
    "US",
    "EU",
    "China",
]

EXCLUDED_API_TAB_KEYWORDS = [
    "batch",
    "flex",
    "priority",
    "discount",
    "promo",
    "promotion",
    "优惠",
    "折扣",
    "优化",
    "促销",
]

ACTION_CONTROL_KEYWORDS = [
    "获取",
    "立即体验",
    "免费试用",
    "注册",
    "登录",
    "订阅",
    "购买",
    "联系销售",
    "get ",
    "start",
    "sign up",
    "log in",
    "login",
    "subscribe",
    "buy",
    "contact sales",
]

FAQ_CONTROL_KEYWORDS = [
    "faq",
    "常见问题",
    "为什么",
    "如何",
    "怎么",
    "哪个",
    "多少",
    "what",
    "why",
    "how",
    "which",
    "where",
]

BLOCKED_PAGE_PATTERNS = [
    "just a moment",
    "verify you are human",
    "please enable cookies",
    "access denied",
    "attention required",
    "checking your browser",
    "captcha",
]

DYNAMIC_LOADING_PATTERNS = [
    "loading models",
    "loading pricing",
    "loading prices",
    "loading plans",
    "加载中",
    "正在加载",
]

TRANSIENT_NAVIGATION_PATTERNS = [
    "ERR_CONNECTION_CLOSED",
    "ERR_HTTP2_PROTOCOL_ERROR",
    "ERR_NETWORK_CHANGED",
    "ERR_TIMED_OUT",
    "ERR_CONNECTION_RESET",
]

STEALTH_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
COLLECT_MAX_WORKERS = 3


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def is_blocked_page(view: dict[str, str]) -> bool:
    text = "\n".join([view.get("title", ""), view.get("body_text", ""), view.get("markdown", "")]).lower()
    return any(pattern in text for pattern in BLOCKED_PAGE_PATTERNS)


def is_blocked_text(text: str) -> bool:
    lowered = (text or "").lower()
    return any(pattern in lowered for pattern in BLOCKED_PAGE_PATTERNS)


def has_dynamic_loading_text(text: str) -> bool:
    lowered = (text or "").lower()
    return any(pattern in lowered for pattern in DYNAMIC_LOADING_PATTERNS)


def is_transient_navigation_error(exc: Exception) -> bool:
    message = str(exc)
    return any(pattern in message for pattern in TRANSIENT_NAVIGATION_PATTERNS)


def is_openai_subscription_source(source_url: str, track_types: set[str]) -> bool:
    lowered = (source_url or "").lower()
    return "subscription" in track_types and "openai.com/chatgpt/pricing" in lowered


def add_stealth_script(context) -> None:
    context.add_init_script(
        """
        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
        Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
        Object.defineProperty(navigator, 'language', {get: () => 'en-US'});
        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
        window.chrome = { runtime: {} };
        """
    )


def wait_for_price_ready(page, track_types: set[str]) -> None:
    if not track_types:
        return
    previous_body = ""
    stable_ticks = 0
    blank_ticks = 0
    for _ in range(8):
        body_text = current_body_text(page)
        normalized_body = normalize_space(body_text)
        if normalized_body and normalized_body == previous_body:
            stable_ticks += 1
        else:
            stable_ticks = 0
        if not normalized_body:
            blank_ticks += 1
        else:
            blank_ticks = 0
        previous_body = normalized_body
        has_price_signal = explicit_price_signal_count(body_text) > 0
        still_loading = has_dynamic_loading_text(body_text)
        if has_price_signal and not still_loading and stable_ticks >= 1:
            return
        if not normalized_body and not still_loading and blank_ticks >= 2:
            return
        if normalized_body and not still_loading and stable_ticks >= 2 and len(normalized_body) >= 500:
            return
        page.wait_for_timeout(1000)


def current_body_text(page) -> str:
    candidates: list[str] = []
    for selector in ["main", "article", "body"]:
        try:
            candidate = page.locator(selector).first.inner_text(timeout=250)
            if normalize_space(candidate):
                candidates.append(candidate)
        except Exception:
            continue
    return max(candidates, key=lambda text: len(normalize_space(text)), default="")


def has_openai_visible_prices(text: str) -> bool:
    lowered = (text or "").lower()
    if not all(token in lowered for token in ["go", "plus", "pro"]):
        return False
    dollar_amounts = {
        match.group(0).replace(" ", "")
        for match in re.finditer(r"\$\s*\d+(?:\.\d+)?", text or "")
    }
    has_monthly_pricing = bool(
        re.search(r"/\s*(?:user\s*/\s*)?month|per\s+(?:user\s+)?month|/\s*month", lowered, flags=re.IGNORECASE)
    )
    return len(dollar_amounts) >= 3 and has_monthly_pricing


def wait_for_openai_visible_prices(page, timeout_seconds: int = 30) -> bool:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        body_text = current_body_text(page)
        if has_openai_visible_prices(body_text):
            return True
        page.wait_for_timeout(1000)
    return False


def reveal_lazy_content(page) -> None:
    try:
        page.evaluate(
            """
            async () => {
              const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
              const height = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
              for (const ratio of [0.25, 0.5, 0.75, 1]) {
                window.scrollTo(0, Math.floor(height * ratio));
                await sleep(250);
              }
              window.scrollTo(0, 0);
            }
            """
        )
        page.wait_for_timeout(500)
    except Exception:
        pass


def merge_text_snapshots(snapshots: list[str]) -> str:
    seen: set[str] = set()
    output: list[str] = []
    for snapshot in snapshots:
        for line in snapshot.splitlines():
            normalized = normalize_space(line)
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            output.append(line.strip())
    return "\n".join(output)


def capture_scrolled_body_text(page) -> str:
    snapshots: list[str] = []
    try:
        height = page.evaluate("Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    except Exception:
        height = 0
    ratios = [0, 0.33, 0.66, 1]
    for ratio in ratios:
        try:
            if height:
                page.evaluate("(y) => window.scrollTo(0, y)", int(height * ratio))
                page.wait_for_timeout(180)
            text = current_body_text(page)
            if text:
                snapshots.append(text)
        except Exception:
            continue
    try:
        page.evaluate("window.scrollTo(0, 0)")
    except Exception:
        pass
    return merge_text_snapshots(snapshots) or current_body_text(page)


def load_page(page, source_url: str, timeout_seconds: int, track_types: set[str] | None = None) -> None:
    timeout_ms = timeout_seconds * 1000
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            page.goto(source_url, wait_until="domcontentloaded", timeout=timeout_ms)
            last_exc = None
            break
        except Exception as exc:
            last_exc = exc
            if attempt < 2 and is_transient_navigation_error(exc):
                page.wait_for_timeout(1500 * (attempt + 1))
                continue
            raise
    if last_exc:
        raise last_exc
    try:
        page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 5000))
    except PlaywrightTimeoutError:
        pass
    page.wait_for_timeout(600)
    active_track_types = track_types or set()
    wait_for_price_ready(page, active_track_types)
    reveal_lazy_content(page)
    if active_track_types and has_dynamic_loading_text(current_body_text(page)):
        try:
            page.reload(wait_until="domcontentloaded", timeout=timeout_ms)
            try:
                page.wait_for_load_state("networkidle", timeout=min(timeout_ms, 5000))
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(1000)
            wait_for_price_ready(page, active_track_types)
            reveal_lazy_content(page)
        except Exception:
            pass


def build_context(browser, *, stealth: bool = True):
    if not stealth:
        return browser.new_context()
    context = browser.new_context(
        locale="en-US",
        timezone_id="America/New_York",
        viewport={"width": 1440, "height": 2200},
        user_agent=STEALTH_USER_AGENT,
        extra_http_headers={
            "Accept-Language": "en-US,en;q=0.9",
            "Upgrade-Insecure-Requests": "1",
        },
    )
    add_stealth_script(context)
    return context


def visible_tables(page) -> list[list[list[str]]]:
    script = """
    els => els
      .filter(el => {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
      })
      .map(table => Array.from(table.querySelectorAll('tr'))
        .map(row => Array.from(row.querySelectorAll('th, td'))
          .map(cell => (cell.innerText || cell.textContent || '').replace(/\\s+/g, ' ').trim())
          .filter(Boolean))
        .filter(row => row.length > 0))
      .filter(table => table.length > 0)
    """
    try:
        return page.locator("table").evaluate_all(script)
    except Exception:
        return []


def visible_markdown_from_page(page, title: str, body_text: str) -> str:
    lines = [normalize_space(line) for line in body_text.splitlines()]
    lines = [line for line in lines if line]
    blocks = [f"# {title}".strip(), ""]
    blocks.extend(lines)
    tables = visible_tables(page)
    if tables:
        blocks.extend(["", "## Extracted tables"])
        for index, table in enumerate(tables, start=1):
            blocks.append(f"\n### Table {index}")
            for row in table:
                blocks.append(" | ".join(row))
    embedded_snippets = embedded_pricing_snippets(page, body_text) if explicit_price_signal_count(body_text) < 5 else []
    if embedded_snippets:
        blocks.extend(["", "## Embedded pricing snippets"])
        for index, snippet in enumerate(embedded_snippets, start=1):
            blocks.append(f"\n### Snippet {index}")
            blocks.append(snippet)
    return "\n".join(blocks).strip()


def decode_embedded_text(text: str) -> str:
    decoded = html.unescape(text or "")
    replacements = {
        "\\u003e": ">",
        "\\u003c": "<",
        "\\u0026": "&",
        "\\u002f": "/",
        "\\u002F": "/",
        "\\n": "\n",
        '\\"': '"',
    }
    for old, new in replacements.items():
        decoded = decoded.replace(old, new)
    return decoded


def embedded_pricing_snippets(page, visible_text: str) -> list[str]:
    try:
        script_text = "\n".join(page.locator("script").evaluate_all("els => els.map(el => el.textContent || '')"))
    except Exception:
        return []
    decoded = decode_embedded_text(script_text)
    if not decoded:
        return []
    visible_compact = normalize_space(visible_text).lower()
    amount_pattern = r"(?:\$|USD|US\$|¥|￥|RMB|CNY)\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?\s*(?:元|/ ?month|/ ?year|per month|per year|per 1m tokens|/ ?m tokens)"
    snippets: list[str] = []
    for match in re.finditer(amount_pattern, decoded, flags=re.IGNORECASE):
        start = max(0, match.start() - 260)
        end = min(len(decoded), match.end() + 360)
        snippet = normalize_space(decoded[start:end])
        lowered = snippet.lower()
        if any(blocked in lowered for blocked in ["bug bounty", "cash rewards", "token of our appreciation"]):
            continue
        if not any(keyword in lowered for keyword in ["price", "pricing", "pricetoken", "plan", "subscription", "套餐", "价格", "计费"]):
            continue
        if snippet.lower() in visible_compact:
            continue
        if any(snippet in existing or existing in snippet for existing in snippets):
            continue
        snippets.append(snippet[:900])
        if len(snippets) >= 12:
            break
    return snippets


def explicit_price_signal_count(text: str) -> int:
    patterns = [
        r"\$\s*\d",
        r"(?:¥|￥)\s*\d",
        r"\d+(?:\.\d+)?\s*元",
        r"per\s+1m\s+tokens",
        r"per\s+month",
        r"per\s+year",
        r"月付|年付|季度|monthly|annual|yearly|quarterly",
    ]
    lowered = text.lower()
    total = 0
    for pattern in patterns:
        total += len(re.findall(pattern, lowered, flags=re.IGNORECASE))
    return total


def distinct_priced_subscription_cycles(text: str) -> set[str]:
    lowered = (text or "").lower()
    cycles: set[str] = set()
    if re.search(r"(?:[$¥￥]\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?)\s*/\s*(?:月|month)|per\s+month|按月计费", lowered, flags=re.IGNORECASE):
        cycles.add("monthly")
    if re.search(r"(?:[$¥￥]\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?)\s*/\s*(?:季|quarter)|per\s+quarter|按季计费|下个季度续费金额", lowered, flags=re.IGNORECASE):
        cycles.add("quarterly")
    if re.search(r"(?:[$¥￥]\s*\d+(?:\.\d+)?|\d+(?:\.\d+)?)\s*/\s*(?:年|year)|per\s+year|按年计费", lowered, flags=re.IGNORECASE):
        cycles.add("annual")
    return cycles


def visible_subscription_cycle_labels(page) -> list[str]:
    labels: list[str] = []
    for label in SUBSCRIPTION_CYCLE_LABELS:
        try:
            if page.get_by_text(label, exact=True).count() > 0:
                labels.append(label)
        except Exception:
            continue
    return labels


def is_relevant_view(view: dict[str, str], track_types: set[str]) -> bool:
    text = f"{view.get('title', '')}\n{view.get('body_text', '')}\n{view.get('markdown', '')}"
    lowered = text.lower()
    price_signals = explicit_price_signal_count(text)
    table_markers = lowered.count("### table")
    if "subscription" in track_types:
        return price_signals > 0 or table_markers > 0
    if "api" in track_types:
        return price_signals > 1 or table_markers > 0
    return price_signals > 0 or table_markers > 0


def should_probe_controls(default_view: dict[str, str], track_types: set[str]) -> bool:
    text = default_view.get("body_text", "")
    markdown = default_view.get("markdown", "").lower()
    price_signals = explicit_price_signal_count(text)
    table_markers = markdown.count("### table")
    if table_markers >= 2 and price_signals >= 2:
        return False
    if price_signals >= 12:
        return False
    return True


def matches_control_allowlist(control_text: str, track_types: set[str]) -> bool:
    text = normalize_space(control_text)
    if not text:
        return False
    lowered = text.lower()
    if any(keyword in lowered for keyword in ACTION_CONTROL_KEYWORDS):
        return False
    if (text.endswith("?") or "？" in text or any(keyword in lowered for keyword in FAQ_CONTROL_KEYWORDS)) and len(text) > 12:
        return False
    if len(text) > 30:
        return False
    if "api" in track_types and any(keyword in lowered for keyword in EXCLUDED_API_TAB_KEYWORDS):
        return False
    if any(keyword.lower() in lowered for keyword in REGION_KEYWORDS):
        return True
    if "subscription" in track_types and any(keyword.lower() in lowered for keyword in SUBSCRIPTION_CYCLE_KEYWORDS):
        return True
    if "standard" in lowered:
        return True
    return any(keyword.lower() in lowered for keyword in MAIN_TAB_KEYWORDS)


def compact_control_text(text: str) -> str:
    return re.sub(r"[^0-9a-zA-Z\u4e00-\u9fff]+", "", (text or "").lower())


def matches_target_control(control_text: str, target_names: set[str]) -> bool:
    text = normalize_space(control_text)
    text_compact = compact_control_text(text)
    if not text_compact:
        return False
    for name in target_names:
        name = normalize_space(name)
        if not name:
            continue
        name_compact = compact_control_text(name)
        if not name_compact:
            continue
        if len(name_compact) < 4:
            if text_compact == name_compact:
                return True
            continue
        if name_compact in text_compact or text_compact in name_compact:
            return True
    return False


def target_control_names(source_configs: list[dict[str, str]], track_types: set[str]) -> set[str]:
    vendor_keys = {config.get("vendor_key", "").strip() for config in source_configs if config.get("vendor_key", "").strip()}
    source_urls = {config.get("source_url", "").strip() for config in source_configs if config.get("source_url", "").strip()}
    names: set[str] = set()
    if "api" in track_types:
        for target in load_target_api_models():
            if not parse_bool(target.get("is_active", "true")):
                continue
            if target.get("vendor_key", "").strip() not in vendor_keys:
                continue
            target_url = target.get("source_url", "").strip()
            if target_url and target_url not in source_urls:
                continue
            if target.get("model_name", "").strip():
                names.add(target.get("model_name", "").strip())
    if "subscription" in track_types:
        for target in load_target_subscription_plans():
            if not parse_bool(target.get("is_active", "true")):
                continue
            if target.get("vendor_key", "").strip() not in vendor_keys:
                continue
            target_url = target.get("source_url", "").strip()
            if target_url and target_url not in source_urls:
                continue
            if target.get("plan_name", "").strip():
                names.add(target.get("plan_name", "").strip())
    return names


def is_same_origin_url(page_url: str, href: str) -> bool:
    if not href:
        return True
    parsed_page = urlparse(page_url)
    parsed_href = urlparse(urljoin(page_url, href))
    return (parsed_page.scheme, parsed_page.netloc) == (parsed_href.scheme, parsed_href.netloc)


def is_same_document_url(page_url: str, href: str) -> bool:
    if not href:
        return True
    parsed_page = urlparse(page_url)
    parsed_href = urlparse(urljoin(page_url, href))
    return (
        parsed_page.scheme,
        parsed_page.netloc,
        parsed_page.path.rstrip("/"),
    ) == (
        parsed_href.scheme,
        parsed_href.netloc,
        parsed_href.path.rstrip("/"),
    )


def should_include_control(control_text: str, track_types: set[str], target_names: set[str], *, is_link: bool = False, href: str = "", page_url: str = "") -> bool:
    lowered = normalize_space(control_text).lower()
    if any(keyword in lowered for keyword in ACTION_CONTROL_KEYWORDS):
        return False
    if matches_target_control(control_text, target_names):
        return True
    if is_link and href:
        return is_same_document_url(page_url, href) and matches_control_allowlist(control_text, track_types)
    return matches_control_allowlist(control_text, track_types)


def candidate_controls(page, target_names: set[str], track_types: set[str]) -> list[dict[str, str]]:
    script = """
    (els) => els
      .filter(el => {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
      })
      .map(el => ({
        text: (el.innerText || el.textContent || '').replace(/\\s+/g, ' ').trim(),
        href: el.href || el.getAttribute('href') || '',
        tag: el.tagName.toLowerCase(),
        role: el.getAttribute('role') || ''
      }))
      .filter(item => item.text && item.text.length <= 60)
    """
    raw_candidates: list[dict[str, str]] = []
    for selector in ["[role=tab]", "button", "[role=button]", "a"]:
        try:
            raw_candidates.extend(page.locator(selector).evaluate_all(script))
        except Exception:
            continue
    if "subscription" in track_types:
        for label in visible_subscription_cycle_labels(page):
            raw_candidates.append({"text": label, "href": "", "tag": "text", "role": "cycle"})
    candidates: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for candidate in raw_candidates:
        text = normalize_space(candidate.get("text", ""))
        href = candidate.get("href", "")
        is_link = candidate.get("tag", "") == "a"
        if is_link and href and not is_same_origin_url(page.url, href):
            continue
        if not should_include_control(text, track_types, target_names, is_link=is_link, href=href, page_url=page.url):
            continue
        key = (text, href)
        if key in seen:
            continue
        seen.add(key)
        candidates.append({**candidate, "text": text, "href": href})
    return candidates[:12]


def candidate_control_texts(page) -> list[str]:
    return [candidate["text"] for candidate in candidate_controls(page, set(), set())]


def control_priority(control_text: str, track_types: set[str]) -> tuple[int, int, int]:
    text = normalize_space(control_text)
    lowered = text.lower()
    is_standard = 0 if "standard" in lowered else 1
    is_region = 0 if any(keyword.lower() in lowered for keyword in REGION_KEYWORDS) else 1
    is_cycle = 0 if ("subscription" in track_types and any(keyword.lower() in lowered for keyword in SUBSCRIPTION_CYCLE_KEYWORDS)) else 1
    return (is_standard, is_region, is_cycle)


def max_controls_to_try(track_types: set[str]) -> int:
    if "subscription" in track_types:
        return 5
    if "api" in track_types:
        return 5
    return 5


def page_id_for(source_url: str, source_configs: list[dict[str, str]]) -> str:
    vendor_keys = "-".join(sorted({safe_filename(config.get("vendor_key", "").strip()) for config in source_configs if config.get("vendor_key", "").strip()}))
    track_types = "-".join(sorted({safe_filename(config.get("track_type", "").strip()) for config in source_configs if config.get("track_type", "").strip()}))
    regions = "-".join(sorted({safe_filename(config.get("region", "").strip()) for config in source_configs if config.get("region", "").strip()}))
    return f"{vendor_keys or 'vendor'}__{track_types or 'track'}__{regions or 'region'}"


def chunked_grouped_items(grouped_items: list[tuple[str, list[dict[str, str]]]], chunk_count: int) -> list[list[tuple[str, list[dict[str, str]]]]]:
    chunks = [[] for _ in range(chunk_count)]
    for index, item in enumerate(grouped_items):
        chunks[index % chunk_count].append(item)
    return [chunk for chunk in chunks if chunk]


def extraction_key(row: dict[str, Any], name_field: str) -> tuple[str, str, str, str]:
    return (
        str(row.get("vendor_key", "")).strip().lower(),
        str(row.get("region", "")).strip().lower(),
        str(row.get("product_name", "")).strip().lower(),
        str(row.get(name_field, "")).strip().lower(),
    )


def merge_json_skeleton(path: Path, skeleton_rows: list[dict[str, Any]], name_field: str) -> None:
    existing_payload = read_json_data(path)
    if existing_payload is None:
        existing_rows: list[dict[str, Any]] = []
    elif isinstance(existing_payload, list):
        existing_rows = existing_payload
    else:
        raise RuntimeError(f"{path} 必须是 JSON 数组。")

    existing_keys = {extraction_key(row, name_field) for row in existing_rows if isinstance(row, dict)}
    merged_rows = list(existing_rows)
    for row in skeleton_rows:
        key = extraction_key(row, name_field)
        if key in existing_keys:
            continue
        merged_rows.append(row)
        existing_keys.add(key)
    write_json_data(path, merged_rows)


def source_url_for_target(target: dict[str, str], track_type: str, configs: list[dict[str, str]]) -> str:
    vendor_key = target.get("vendor_key", "").strip()
    region = target.get("region", "").strip()
    candidates = [
        config
        for config in configs
        if config.get("vendor_key", "").strip() == vendor_key
        and config.get("track_type", "").strip() == track_type
        and config.get("source_url", "").strip()
    ]
    exact = [config for config in candidates if config.get("region", "").strip() == region]
    if exact:
        return exact[0].get("source_url", "").strip()
    if len(candidates) == 1:
        return candidates[0].get("source_url", "").strip()
    return ""


def api_skeleton_rows(selected_vendor_keys: set[str], selected_urls: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_configs = [
        config
        for config in filter_vendor_configs(load_vendor_configs(), allowed_vendor_keys=selected_vendor_keys)
        if config.get("source_url", "").strip() in selected_urls
    ]
    for target in load_target_api_models():
        if not parse_bool(target.get("is_active", "true")):
            continue
        vendor_key = target.get("vendor_key", "").strip()
        source_url = source_url_for_target(target, "api", source_configs)
        if vendor_key not in selected_vendor_keys or not source_url:
            continue
        rows.append(
            {
                "vendor_key": vendor_key,
                "region": target.get("region", "").strip(),
                "product_name": target.get("product_name", "").strip(),
                "model_name": target.get("model_name", "").strip(),
                "source_url": source_url,
                "prices": [],
                "notes": "",
            }
        )
    return rows


def subscription_skeleton_rows(selected_vendor_keys: set[str], selected_urls: set[str]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_configs = [
        config
        for config in filter_vendor_configs(load_vendor_configs(), allowed_vendor_keys=selected_vendor_keys)
        if config.get("source_url", "").strip() in selected_urls
    ]
    for target in load_target_subscription_plans():
        if not parse_bool(target.get("is_active", "true")):
            continue
        vendor_key = target.get("vendor_key", "").strip()
        source_url = source_url_for_target(target, "subscription", source_configs)
        if vendor_key not in selected_vendor_keys or not source_url:
            continue
        rows.append(
            {
                "vendor_key": vendor_key,
                "region": target.get("region", "").strip(),
                "product_name": target.get("product_name", "").strip(),
                "plan_name": target.get("plan_name", "").strip(),
                "source_url": source_url,
                "prices": [],
                "features": [],
                "plan_summary": "",
                "notes": "",
            }
        )
    return rows


def init_extracted_templates(extracted_dir: Path, selected_vendor_keys: set[str], selected_urls: set[str]) -> None:
    merge_json_skeleton(extracted_dir / "api_pricing.json", api_skeleton_rows(selected_vendor_keys, selected_urls), "model_name")
    merge_json_skeleton(
        extracted_dir / "subscription_plans.json",
        subscription_skeleton_rows(selected_vendor_keys, selected_urls),
        "plan_name",
    )


def prepare_extracted_templates(run_dir: str = "") -> dict[str, Any]:
    resolved_run_dir = run_dir.strip() if run_dir.strip() else load_latest_run()
    run_path = ARTIFACTS_DIR / resolved_run_dir
    if not run_path.exists():
        raise RuntimeError(f"找不到 artifacts/{resolved_run_dir}，请先运行 --mode collect。")
    collected_dir = run_path / "collected"
    extracted_dir = run_path / "extracted"
    source_pages = read_csv_rows(collected_dir / "source_pages.csv")
    if not source_pages:
        raise RuntimeError(f"{collected_dir / 'source_pages.csv'} 为空或不存在，请先运行 --mode collect。")
    selected_vendor_keys = {
        vendor_key.strip()
        for row in source_pages
        if str(row.get("status", "")).strip().lower() == "ok"
        for vendor_key in str(row.get("vendor_keys", "")).split(";")
        if vendor_key.strip()
    }
    selected_urls = {
        row.get("source_url", "").strip()
        for row in source_pages
        if str(row.get("status", "")).strip().lower() == "ok" and row.get("source_url", "").strip()
    }
    if not selected_vendor_keys or not selected_urls:
        raise RuntimeError(f"{collected_dir / 'source_pages.csv'} 没有 status=ok 的来源页，请先处理采集异常。")
    extracted_dir.mkdir(parents=True, exist_ok=True)
    init_extracted_templates(extracted_dir, selected_vendor_keys, selected_urls)
    save_latest_run(resolved_run_dir)
    return {
        "run_dir": resolved_run_dir,
        "artifact_dir": str(run_path),
        "source_pages_ok": len(selected_urls),
        "vendors_scope": ",".join(sorted(selected_vendor_keys)),
        "api_json": str(extracted_dir / "api_pricing.json"),
        "subscription_json": str(extracted_dir / "subscription_plans.json"),
    }


def page_issue(configs: list[dict[str, str]], source_url: str, stage: str, message: str, created_at: str) -> dict[str, str]:
    return {
        "issue_id": f"{stage}:{short_hash(source_url + message)}",
        "stage": stage,
        "vendor_keys": ";".join(sorted({config.get("vendor_key", "").strip() for config in configs if config.get("vendor_key", "").strip()})),
        "track_types": ";".join(sorted({config.get("track_type", "").strip() for config in configs if config.get("track_type", "").strip()})),
        "source_url": source_url,
        "severity": "error",
        "message": message,
        "created_at": created_at,
    }


def normalize_control_label(control_text: str) -> str:
    text = normalize_space(control_text)
    return text[:60] if text else "Default"


def canonical_section_title(control_text: str) -> str:
    text = normalize_control_label(control_text)
    if not text:
        return "Default"
    lowered = text.lower()
    if any(token == lowered for token in ["monthly", "quarterly", "yearly", "annual"]):
        return text.title()
    if lowered in {"月", "月付"}:
        return "Monthly"
    if lowered in {"季", "季度"}:
        return "Quarterly"
    if lowered in {"年", "年付"}:
        return "Yearly"
    return text


def markdown_without_h1(markdown: str) -> str:
    lines = markdown.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and lines[0].startswith("# "):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    return "\n".join(lines).strip()


def dedupe_lines(markdown: str) -> str:
    lines = markdown.splitlines()
    seen: set[str] = set()
    output: list[str] = []
    for line in lines:
        key = normalize_space(line)
        if not key:
            if output and output[-1] != "":
                output.append("")
            continue
        if key in seen and not line.lstrip().startswith(("#", "|")):
            continue
        seen.add(key)
        output.append(line)
    while output and output[-1] == "":
        output.pop()
    return "\n".join(output).strip()


def build_merged_markdown(source_url: str, title: str, sections: list[dict[str, str]]) -> str:
    blocks = [f"# {title}".strip(), "", f"Source URL: {source_url}", ""]
    for section in sections:
        body = markdown_without_h1(section["markdown"])
        if not body:
            continue
        body = dedupe_lines(body)
        if not body:
            continue
        blocks.append(f"## {section['label']}")
        blocks.append("")
        blocks.append(body)
        blocks.append("")
    while blocks and not blocks[-1].strip():
        blocks.pop()
    return "\n".join(blocks) + "\n"


def capture_view(page, control_text: str = "", *, fast: bool = False) -> dict[str, str]:
    title = page.title()
    body_text = current_body_text(page) if fast else capture_scrolled_body_text(page)
    markdown = visible_markdown_from_page(page, title, body_text)
    return {
        "label": canonical_section_title(control_text or "Default"),
        "markdown": markdown,
        "title": title,
        "body_text": body_text,
        "normalized_body": normalize_space(body_text),
    }


def capture_control_view_in_place(page, candidate: dict[str, str], track_types: set[str]) -> dict[str, str] | None:
    control_text = candidate.get("text", "")
    try:
        before_url = page.url
        before_body = normalize_space(current_body_text(page))
        page.get_by_text(control_text, exact=True).first.click(timeout=3000)
        navigated = bool(candidate.get("href")) and page.url != before_url
        if navigated:
            try:
                page.wait_for_load_state("domcontentloaded", timeout=10000)
            except PlaywrightTimeoutError:
                pass
            page.wait_for_timeout(800)
            wait_for_price_ready(page, track_types)
        else:
            for _ in range(3):
                page.wait_for_timeout(500)
                current_body = normalize_space(current_body_text(page))
                if current_body and current_body != before_body:
                    break
            if has_dynamic_loading_text(current_body_text(page)):
                wait_for_price_ready(page, track_types)
        return capture_view(page, control_text, fast=not navigated)
    except Exception:
        return None


def save_merged_page(
    *,
    source_url: str,
    source_configs: list[dict[str, str]],
    pages_dir: Path,
    fetched_at: str,
    title: str,
    sections: list[dict[str, str]],
) -> dict[str, str]:
    source_page_id = page_id_for(source_url, source_configs)
    markdown_name = f"{source_page_id}.md"
    (pages_dir / markdown_name).write_text(build_merged_markdown(source_url, title, sections), encoding="utf-8")
    captured_views = ";".join(section["label"] for section in sections)
    return {
        "source_page_id": source_page_id,
        "source_url": source_url,
        "source_title": title,
        "vendor_keys": ";".join(sorted({config.get("vendor_key", "").strip() for config in source_configs if config.get("vendor_key", "").strip()})),
        "track_types": ";".join(sorted({config.get("track_type", "").strip() for config in source_configs if config.get("track_type", "").strip()})),
        "regions": ";".join(sorted({config.get("region", "").strip() for config in source_configs if config.get("region", "").strip()})),
        "markdown_path": f"pages/{markdown_name}",
        "captured_views": captured_views,
        "status": "ok",
        "fetched_at": fetched_at,
        "error_message": "",
    }


def collect_source_pages_batch(
    grouped_items: list[tuple[str, list[dict[str, str]]]],
    pages_dir: Path,
    fetched_at: str,
    timeout_seconds: int,
    *,
    headed: bool = False,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    pages: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []
    with sync_playwright() as playwright:
        launch_args = ["--headless=new"] if not headed else []
        browser = playwright.chromium.launch(headless=not headed, args=launch_args)
        try:
            for source_url, source_configs in grouped_items:
                if not source_url:
                    continue
                track_types = {config.get("track_type", "").strip() for config in source_configs if config.get("track_type", "").strip()}
                use_openai_headed = is_openai_subscription_source(source_url, track_types)
                context = None
                page = None
                special_browser = None

                def open_page(*, stealth: bool) -> None:
                    nonlocal context, page, special_browser
                    if context is not None:
                        context.close()
                        context = None
                    if special_browser is not None:
                        special_browser.close()
                        special_browser = None
                    if use_openai_headed:
                        special_browser = playwright.chromium.launch(headless=False)
                        context = build_context(special_browser, stealth=stealth)
                    else:
                        context = build_context(browser, stealth=stealth)
                    page = context.new_page()

                open_page(stealth=True)
                try:
                    load_page(page, source_url, timeout_seconds, track_types)
                    if use_openai_headed:
                        ready = wait_for_openai_visible_prices(page, 30)
                        if not ready:
                            try:
                                page.reload(wait_until="domcontentloaded", timeout=timeout_seconds * 1000)
                                try:
                                    page.wait_for_load_state("networkidle", timeout=min(timeout_seconds * 1000, 5000))
                                except PlaywrightTimeoutError:
                                    pass
                                page.wait_for_timeout(600)
                                wait_for_price_ready(page, track_types)
                                reveal_lazy_content(page)
                                wait_for_openai_visible_prices(page, 30)
                            except Exception:
                                pass
                    default_view = capture_view(page, "Default", fast="subscription" in track_types)
                    default_price_signals = explicit_price_signal_count(default_view["body_text"])
                    if (not default_view["normalized_body"] or default_price_signals == 0) and not is_blocked_page(default_view) and not use_openai_headed:
                        open_page(stealth=False)
                        load_page(page, source_url, timeout_seconds, track_types)
                        default_view = capture_view(page, "Default", fast="subscription" in track_types)
                    if is_blocked_page(default_view):
                        issues.append(page_issue(source_configs, source_url, "fetch", "命中反爬/验证页面，未获取到有效正文。", fetched_at))
                        continue
                    selected_sections = [{"label": default_view["label"], "markdown": default_view["markdown"]}]
                    seen_texts = {default_view["normalized_body"]}
                    seen_labels = {default_view["label"]}
                    cycle_labels: list[str] = []
                    should_probe = should_probe_controls(default_view, track_types)
                    if use_openai_headed and has_openai_visible_prices(default_view["body_text"]):
                        should_probe = False
                    if "subscription" in track_types:
                        cycle_labels = visible_subscription_cycle_labels(page)
                        priced_cycles = distinct_priced_subscription_cycles(default_view["markdown"])
                        if len(cycle_labels) > len(priced_cycles):
                            should_probe = True
                    if not should_probe:
                        pages.append(
                            save_merged_page(
                                source_url=source_url,
                                source_configs=source_configs,
                                pages_dir=pages_dir,
                                fetched_at=fetched_at,
                                title=default_view["title"],
                                sections=selected_sections,
                            )
                        )
                        continue
                    target_names = target_control_names(source_configs, track_types)
                    control_candidates = sorted(candidate_controls(page, target_names, track_types), key=lambda candidate: control_priority(candidate["text"], track_types))[
                        : max_controls_to_try(track_types)
                    ]
                    if "subscription" in track_types and cycle_labels:
                        cycle_label_set = set(cycle_labels)
                        control_candidates = [candidate for candidate in control_candidates if candidate["text"] in cycle_label_set or matches_target_control(candidate["text"], target_names)]
                    for candidate in control_candidates:
                        control_text = candidate["text"]
                        view = capture_control_view_in_place(page, candidate, track_types)
                        if not view:
                            continue
                        if view["label"] in seen_labels:
                            continue
                        if view["normalized_body"] in seen_texts:
                            continue
                        if not is_relevant_view(view, track_types):
                            continue
                        seen_labels.add(view["label"])
                        seen_texts.add(view["normalized_body"])
                        selected_sections.append({"label": view["label"], "markdown": view["markdown"]})
                    pages.append(
                        save_merged_page(
                            source_url=source_url,
                            source_configs=source_configs,
                            pages_dir=pages_dir,
                            fetched_at=fetched_at,
                            title=default_view["title"],
                            sections=selected_sections,
                        )
                    )
                except PlaywrightTimeoutError as exc:
                    issues.append(page_issue(source_configs, source_url, "fetch", f"Timeout: {exc}", fetched_at))
                except Exception as exc:
                    issues.append(page_issue(source_configs, source_url, "fetch", str(exc), fetched_at))
                finally:
                    if context is not None:
                        context.close()
                    if special_browser is not None:
                        special_browser.close()
        finally:
            browser.close()
    return pages, issues


def collect_source_pages(
    configs: list[dict[str, str]],
    pages_dir: Path,
    fetched_at: str,
    timeout_seconds: int,
    *,
    headed: bool = False,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for config in configs:
        grouped[config.get("source_url", "").strip()].append(config)

    grouped_items = [(source_url, source_configs) for source_url, source_configs in grouped.items() if source_url]
    if not grouped_items:
        return [], []

    max_workers = min(COLLECT_MAX_WORKERS, len(grouped_items))
    if max_workers <= 1:
        return collect_source_pages_batch(
            grouped_items,
            pages_dir,
            fetched_at,
            timeout_seconds,
            headed=headed,
        )

    pages: list[dict[str, str]] = []
    issues: list[dict[str, str]] = []
    batches = chunked_grouped_items(grouped_items, max_workers)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                collect_source_pages_batch,
                batch,
                pages_dir,
                fetched_at,
                timeout_seconds,
                headed=headed,
            )
            for batch in batches
        ]
        for future in futures:
            batch_pages, batch_issues = future.result()
            pages.extend(batch_pages)
            issues.extend(batch_issues)
    pages.sort(key=lambda row: row.get("source_url", ""))
    issues.sort(key=lambda row: row.get("source_url", ""))
    return pages, issues


def run_collect(allowed_vendor_keys: set[str] | None = None, *, timeout_seconds: int = 120, headed: bool = False) -> dict[str, Any]:
    now_text = utc_now()
    all_configs = load_vendor_configs()
    selected_configs = filter_vendor_configs(all_configs, allowed_vendor_keys=allowed_vendor_keys)
    if not selected_configs:
        raise RuntimeError("没有匹配到启用的 vendor 配置。")

    selected_vendor_keys = {config.get("vendor_key", "").strip() for config in selected_configs if config.get("vendor_key", "").strip()}
    run_dir = generate_run_dir()
    run_path = ARTIFACTS_DIR / run_dir
    collected_dir = run_path / "collected"
    pages_dir = collected_dir / "pages"
    extracted_dir = run_path / "extracted"
    pages_dir.mkdir(parents=True, exist_ok=True)
    extracted_dir.mkdir(parents=True, exist_ok=True)

    selected_urls = {config.get("source_url", "").strip() for config in selected_configs if config.get("source_url", "").strip()}
    grouped_selected: dict[str, list[dict[str, str]]] = defaultdict(list)
    for config in selected_configs:
        grouped_selected[config.get("source_url", "").strip()].append(config)
    previous_pages = read_csv_rows(collected_dir / "source_pages.csv")
    previous_issues = read_csv_rows(collected_dir / "collect_issues.csv")

    new_pages, new_issues = collect_source_pages(selected_configs, pages_dir, now_text, timeout_seconds, headed=headed)
    new_pages_by_url = {row.get("source_url", ""): row for row in new_pages if row.get("source_url")}
    previous_pages_by_url = {row.get("source_url", ""): row for row in previous_pages if row.get("source_url")}
    reused_markdown_paths = {row.get("markdown_path", "") for row in new_pages if row.get("markdown_path")}

    merged_pages: list[dict[str, str]] = []
    for row in previous_pages:
        source_url = row.get("source_url", "")
        row_vendor_keys = {part.strip() for part in row.get("vendor_keys", "").split(";") if part.strip()}
        if row_vendor_keys & selected_vendor_keys:
            if source_url not in selected_urls:
                old_markdown = row.get("markdown_path", "")
                if old_markdown and old_markdown not in reused_markdown_paths:
                    old_path = collected_dir / old_markdown
                    if old_path.exists():
                        old_path.unlink()
                continue
            continue
        if source_url:
            merged_pages.append(row)
    for source_url in sorted(selected_urls):
        if source_url in new_pages_by_url:
            old_row = previous_pages_by_url.get(source_url)
            new_row = new_pages_by_url[source_url]
            old_markdown = old_row.get("markdown_path", "") if old_row else ""
            new_markdown = new_row.get("markdown_path", "")
            if old_markdown and old_markdown != new_markdown:
                old_path = collected_dir / old_markdown
                if old_path.exists():
                    old_path.unlink()
            merged_pages.append(new_row)
        elif source_url in previous_pages_by_url:
            previous_row = previous_pages_by_url[source_url]
            markdown_path = previous_row.get("markdown_path", "")
            markdown_file = collected_dir / markdown_path if markdown_path else None
            title = previous_row.get("source_title", "")
            if markdown_file and markdown_file.exists() and not is_blocked_text(title):
                merged_pages.append(previous_row)
            elif markdown_file and markdown_file.exists():
                markdown_file.unlink()

    merged_issues = []
    for row in previous_issues:
        row_vendor_keys = {part.strip() for part in row.get("vendor_keys", "").split(";") if part.strip()}
        if row_vendor_keys & selected_vendor_keys:
            continue
        merged_issues.append(row)
    merged_issues.extend(new_issues)

    active_markdown_paths = {row.get("markdown_path", "") for row in merged_pages if row.get("markdown_path")}
    for source_url, source_configs in grouped_selected.items():
        if not source_url:
            continue
        expected_markdown = f"pages/{page_id_for(source_url, source_configs)}.md"
        if expected_markdown in active_markdown_paths:
            continue
        stale_path = collected_dir / expected_markdown
        if stale_path.exists():
            stale_path.unlink()

    write_csv_rows(collected_dir / "source_pages.csv", merged_pages, SOURCE_PAGE_FIELDS)
    write_csv_rows(collected_dir / "collect_issues.csv", merged_issues, COLLECT_ISSUE_FIELDS)
    init_extracted_templates(extracted_dir, selected_vendor_keys, selected_urls)
    save_latest_run(run_dir)

    return {
        "run_dir": run_dir,
        "artifact_dir": str(run_path),
        "source_urls_seen": len({config.get("source_url", "").strip() for config in selected_configs if config.get("source_url", "").strip()}),
        "source_pages": len(merged_pages),
        "collect_issues": len(merged_issues),
        "vendors_scope": ",".join(sorted({config.get("vendor_key", "").strip() for config in selected_configs if config.get("vendor_key", "").strip()})),
        "headed": headed,
    }
