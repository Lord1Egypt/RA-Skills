"""Core Perplexity search functions with anti-detection.

All modes share one pipeline (_search_core) parameterized by MODES config.
"""

import logging
import random
import time
from typing import Any, Dict, Optional, TypedDict, List

from .config import Config, get_config
from .drivers.base import BrowserDriver
from .drivers import create_driver
from .utils import compact_json, find_textbox, find_menuitem, submit_query
from .utils.antidetect import (
    human_delay, micro_delay,
    human_paste, human_scroll,
    combined_snapshot_and_info, combined_extract,
)
from .utils.i18n import get_ui_string
from .verify import verify_result

logger = logging.getLogger(__name__)


_GROUNDING_REQUIREMENTS = """Requirements:
1. Cite sources with URLs
2. If no verified source, say so
3. For pricing: official page URLs only
4. Format as comparison table with Source URL column"""


# ──────────────────────────────────────────────
# Type definitions
# ──────────────────────────────────────────────

class Source(TypedDict):
    text: str
    href: str


class SearchResult(TypedDict, total=False):
    answer: Optional[str]
    sources: List[Source]
    url: str
    title: str
    follow_ups: List[str]
    mode: str
    query: str
    error: str
    searched_at: str
    session: str
    quality: Dict[str, Any]
    verification: Dict[str, Any]


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _make_driver(config: Config) -> BrowserDriver:
    """Create the task driver; all modes share its task session."""
    return create_driver(config)


def build_grounded_query(query: str) -> str:
    """Apply the canonical source-grounding wrapper exactly once."""
    if "requirements:" in query.casefold() or "要求：" in query or "要求:" in query:
        return query
    return f"{query.rstrip()}\n{_GROUNDING_REQUIREMENTS}"


def _session_has_tabs(driver: Any) -> Optional[bool]:
    """Return whether a driver session already has a tab, if supported.

    WebBridge's ``success: true, tabs: []`` is a healthy empty session. Any
    explicit error or failed status is raised so a dead bridge cannot be
    mistaken for a reason to switch execution routes.
    """
    list_tabs = getattr(driver, "list_tabs", None)
    if not callable(list_tabs):
        return None
    try:
        response = list_tabs()
    except NotImplementedError:
        return None
    except Exception as exc:
        raise RuntimeError(f"list_tabs precheck failed: {exc}") from exc

    if not isinstance(response, dict):
        raise RuntimeError("list_tabs precheck returned a non-object response")
    if response.get("error"):
        raise RuntimeError(f"list_tabs precheck failed: {response['error']}")
    for status_key in ("success", "ok"):
        if status_key in response and response[status_key] is False:
            raise RuntimeError(f"list_tabs precheck failed: {response}")
    if "tabs" not in response:
        raise RuntimeError("list_tabs precheck omitted the tabs field")
    return bool(response.get("tabs"))


def _resolve_new_tab(driver: Any, requested: Optional[bool]) -> bool:
    """Resolve the navigation policy for a task-scoped session."""
    has_tabs = _session_has_tabs(driver)
    return (
        requested if requested is not None
        else (not has_tabs if has_tabs is not None else True)
    )


def _snapshot_compact(driver) -> str:
    resp = driver.snapshot()
    tree = resp.get("data", {}).get("tree", "")
    return compact_json(tree)


def _find_and_click_textbox(driver, s: str) -> Optional[str]:
    """Find textbox and click it with human-like timing."""
    ref = find_textbox(s)
    if ref:
        micro_delay(0.1, 0.3)
        driver.click(ref)
        human_delay(0.3, 0.6)
        logger.debug("Textbox found: %s", ref)
    else:
        logger.debug("Textbox not found in snapshot")
    return ref


def _activate_mode(driver, mode_name: str) -> bool:
    """Activate a search mode via '/' menu with human timing."""
    driver.cdp("Input.insertText", {"text": "/"})
    human_delay(0.8, 1.3)

    s = _snapshot_compact(driver)
    ref = find_menuitem(s, mode_name)
    if not ref:
        logger.debug("Mode menu item %r not found", mode_name)
        return False

    driver.click(ref)
    human_delay(0.8, 1.2)
    logger.debug("Activated mode %r via menuitem %s", mode_name, ref)
    return True


def _submit_query(driver) -> str:
    """Submit query with trusted CDP Enter key."""
    status = submit_query(driver)
    if status == "submitted":
        logger.info("Query submitted")
    elif status == "submitted_retry":
        logger.info("Query submitted after retry")
    else:
        logger.warning("No submit detected")
    return status


def _switch_to_tab(driver, tab_text: str):
    """Click a tab by text with human delay."""
    driver.evaluate(f"""(() => {{
        const tabs = Array.from(document.querySelectorAll("[role=tab]"));
        const t = tabs.find(t => t.innerText.includes("{tab_text}"));
        if (t) t.click();
    }})()""")
    micro_delay(0.2, 0.5)


def _is_search_done(driver) -> bool:
    return combined_snapshot_and_info(driver).get("done", False)


def _expand_answer(driver, locale: str = "zh") -> bool:
    """Click expand button to show full answer."""
    show_more = get_ui_string("show_more", locale)
    result = driver.evaluate(f"""(() => {{
        const btns = Array.from(document.querySelectorAll("button"));
        const more = btns.find(b => b.innerText.includes("{show_more}"));
        if (more) {{ more.click(); return "expanded"; }}
        return "no expand";
    }})()""")
    if result == "expanded":
        logger.debug("Answer expanded")
        human_delay(0.5, 1.0)
        return True
    return False


def _extract_results(driver, locale: str = "zh") -> dict:
    """Extract answer, sources, and follow-ups in one consolidated call."""
    sources_tab = get_ui_string("sources_tab", locale)
    answer_tab = get_ui_string("answer_tab", locale)
    _switch_to_tab(driver, sources_tab)
    human_delay(0.3, 0.6)
    data = combined_extract(driver)
    _switch_to_tab(driver, answer_tab)
    human_delay(0.2, 0.4)
    return data


def _log_completion(mode: str, query: str, data: dict, info: dict) -> None:
    answer = data.get("answer", "")
    sources = data.get("sources", [])
    if not answer:
        logger.warning("%s: empty answer for %r", mode, query[:80])
    if not sources:
        logger.warning("%s: no sources for %r", mode, query[:80])
    logger.info("%s done: answer_len=%d sources=%d url=%s",
                mode, len(answer), len(sources), info.get("url", ""))


def _error_result(mode: str, message: str) -> SearchResult:
    return {"error": message, "answer": None, "sources": [],
            "url": "", "title": "", "follow_ups": [], "mode": mode}


# ──────────────────────────────────────────────
# Retry with exponential backoff
# ──────────────────────────────────────────────

_RATE_LIMIT_PHRASES = ("limit reached", "too many requests", "rate limit")


def _search_with_retry(
    query: str, mode: str, config: Config,
    driver: Optional[BrowserDriver] = None,
    wait_seconds: Optional[float] = None,
    expand: Optional[bool] = None, new_tab: Optional[bool] = None,
) -> SearchResult:
    """Run _search_core with retry + exponential backoff."""
    max_retries = config.max_retries
    best_result: SearchResult = _error_result(mode, "no attempts")

    for attempt in range(max_retries + 1):
        try:
            result = _search_core_once(
                query, mode, config, driver, wait_seconds, expand, new_tab
            )
        except Exception as e:
            logger.error("%s attempt %d exception: %s", mode, attempt + 1, e)
            result = _error_result(mode, str(e))

        best_result = result

        # Check if retry needed
        if result.get("error"):
            reason = "error"
        elif not result.get("answer") and not result.get("sources"):
            reason = "empty"
        elif any(p in (result.get("answer") or "").lower() for p in _RATE_LIMIT_PHRASES):
            reason = "rate_limit"
        else:
            break  # Success

        if attempt < max_retries:
            if reason == "rate_limit":
                wait = 10 * (2 ** attempt) + random.uniform(0, 2)
            else:
                wait = 2 * (2 ** attempt) + random.uniform(0, 1)
            logger.warning("%s retry %d/%d (%s), backoff %.1fs",
                           mode, attempt + 1, max_retries, reason, wait)
            time.sleep(wait)
        else:
            logger.error("%s exhausted %d retries (%s)", mode, max_retries, reason)

    return best_result


# ──────────────────────────────────────────────
# Mode configuration
# ──────────────────────────────────────────────

_BASE_MODE = {
    "wait": "search_wait", "mode_name": None, "label": "",
    "poll": False, "scroll": False, "scroll_amount": 2, "scroll_delay": 0.4,
    "expand": False, "session": "search", "group": "",
}

MODES = {
    "search": {**_BASE_MODE,
               "label": "Search", "scroll": True, "expand": True, "group": "Search"},
    "deep_research": {**_BASE_MODE, "wait": "deep_research_wait",
                      "mode_name": "deep_research",
                      "label": "Deep Research", "poll": True, "scroll": True,
                      "scroll_amount": 3, "scroll_delay": 0.5,
                      "session": "deep-research", "group": "DR"},
    "model_council": {**_BASE_MODE, "wait": "model_council_wait",
                      "mode_name": "model_council",
                      "label": "Model Council", "session": "council", "group": "Council"},
    "step_by_step": {**_BASE_MODE, "wait": "step_by_step_wait",
                     "mode_name": "step_by_step",
                     "label": "Step-by-step", "session": "stepbystep", "group": "SbS"},
}


# ──────────────────────────────────────────────
# Core pipeline (single attempt)
# ──────────────────────────────────────────────

def _search_core_once(
    query: str, mode: str, config: Config,
    driver: Optional[BrowserDriver] = None,
    wait_seconds: Optional[float] = None,
    expand: Optional[bool] = None, new_tab: Optional[bool] = None,
) -> SearchResult:
    """One attempt of the Perplexity pipeline for a given mode."""
    m = MODES[mode]
    cfg = config
    drv = driver or _make_driver(cfg)
    wait = wait_seconds or getattr(cfg, m["wait"])
    locale = cfg.locale
    if expand is None:
        expand = m["expand"]

    logger.info("Search start: mode=%s query=%r wait=%.1fs", mode, query[:80], wait)

    # Preflight the session before navigation. On WebBridge, only the first
    # navigation creates a tab; subsequent calls reuse the current tab.
    effective_new_tab = _resolve_new_tab(drv, new_tab)

    # Navigate
    human_delay(0.5, 1.5)
    drv.navigate(cfg.base_url, new_tab=effective_new_tab,
                 group_title=f"{m['group']}: {query[:50]}")
    time.sleep(cfg.page_load_wait)

    # Find textbox
    s = _snapshot_compact(drv)
    ref = _find_and_click_textbox(drv, s)
    if not ref:
        logger.warning("%s aborted: no textbox", mode)
        return _error_result(mode, "Could not find textbox")

    # Activate mode via '/' menu
    if m["mode_name"]:
        display_name = get_ui_string(m["mode_name"], locale)
        if not _activate_mode(drv, display_name):
            logger.warning("%s aborted: mode %r not found", mode, display_name)
            return _error_result(mode, f"Could not activate {m['label']}")

    # Type + submit
    human_delay(0.3, 0.6)
    human_paste(drv, build_grounded_query(query), chunk_size=6, delay=0.06)
    human_delay(0.3, 0.8)
    _submit_query(drv)

    # Wait
    if m["poll"]:
        elapsed = 0
        while elapsed < wait:
            sleep_time = random.uniform(12, 18)
            time.sleep(sleep_time)
            elapsed += sleep_time
            if _is_search_done(drv):
                logger.debug("%s finished after %.0fs", mode, elapsed)
                break
        else:
            logger.debug("%s wait elapsed %.0fs", mode, elapsed)
    else:
        time.sleep(wait)

    # Scroll + expand
    if m["scroll"]:
        human_scroll(drv, "down", amount=m["scroll_amount"], delay=m["scroll_delay"])
    if expand:
        _expand_answer(drv, locale)
        human_delay(0.5, 1.0)

    # Extract
    data = _extract_results(drv, locale)
    info = combined_snapshot_and_info(drv)
    _log_completion(mode, query, data, info)

    return {
        "answer": data.get("answer", ""),
        "sources": data.get("sources", []),
        "url": info.get("url", ""),
        "title": info.get("title", ""),
        "follow_ups": data.get("follow_ups", []),
        "mode": mode,
        "session": getattr(drv, "session", ""),
    }


def _search_core(
    query: str, mode: str, config: Optional[Config] = None,
    driver: Optional[BrowserDriver] = None,
    wait_seconds: Optional[float] = None,
    expand: Optional[bool] = None, new_tab: Optional[bool] = None,
    verify: bool = True,
) -> SearchResult:
    """Run the Perplexity pipeline with retry and quality verification."""
    cfg = config or get_config()
    result = _search_with_retry(query, mode, cfg, driver, wait_seconds, expand, new_tab)
    if verify and not result.get("error"):
        result = verify_result(result)
        quality = result.get("quality", {})
        result["verification"] = {
            "state": quality.get("verification_state", "unverified"),
            "claim_support": quality.get("claim_support", "not_evaluated"),
            "source_check": quality.get("source_check", {}),
        }
    return result


# ──────────────────────────────────────────────
# Public search functions (thin wrappers)
# ──────────────────────────────────────────────

def search(query: str, config: Optional[Config] = None, driver: Optional[BrowserDriver] = None,
           wait_seconds: Optional[float] = None, expand: bool = True,
           new_tab: Optional[bool] = None, verify: bool = True) -> SearchResult:
    """Standard Perplexity search with anti-detection."""
    return _search_core(query, "search", config, driver, wait_seconds, expand,
                        new_tab, verify)


def deep_research(query: str, config: Optional[Config] = None, driver: Optional[BrowserDriver] = None,
                  wait_seconds: Optional[float] = None, new_tab: Optional[bool] = None,
                  verify: bool = True) -> SearchResult:
    """Deep Research mode — multi-step, longer answers, 60-120s."""
    return _search_core(query, "deep_research", config, driver, wait_seconds,
                        None, new_tab, verify)


def model_council(query: str, config: Optional[Config] = None, driver: Optional[BrowserDriver] = None,
                  wait_seconds: Optional[float] = None, new_tab: Optional[bool] = None,
                  verify: bool = True) -> SearchResult:
    """Model Council mode — multiple models answer the same question."""
    return _search_core(query, "model_council", config, driver, wait_seconds,
                        None, new_tab, verify)


def step_by_step(query: str, config: Optional[Config] = None, driver: Optional[BrowserDriver] = None,
                 wait_seconds: Optional[float] = None, new_tab: Optional[bool] = None,
                 verify: bool = True) -> SearchResult:
    """Step-by-step Learning mode — guided, structured answers."""
    return _search_core(query, "step_by_step", config, driver, wait_seconds,
                        None, new_tab, verify)
