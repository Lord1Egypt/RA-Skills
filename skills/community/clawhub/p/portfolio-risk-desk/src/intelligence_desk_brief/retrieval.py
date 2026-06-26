"""Evidence retrieval services."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import re
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from intelligence_desk_brief.apify_bootstrap import ensure_apify_tasks
from intelligence_desk_brief.config import AppConfig
from intelligence_desk_brief.contracts import CreateBriefRequest
from intelligence_desk_brief.fixtures import load_mock_evidence
from intelligence_desk_brief.ops import log_event
from intelligence_desk_brief.providers.base import RetrievalAdapter

TICKER_ALIASES = {
    "NVDA": ["NVIDIA"],
    "AMD": ["Advanced Micro Devices"],
    "TSM": ["TSMC", "Taiwan Semiconductor"],
    "ASML": ["ASML Holding", "ASML"],
}
TOP_HEDGE_FUNDS = [
    "Citadel",
    "Bridgewater",
    "Pershing Square",
    "Third Point",
    "Tiger Global",
    "Coatue",
    "Viking Global",
]


class FixtureRetrievalAdapter(RetrievalAdapter):
    """Deterministic fixture-backed retrieval used in Order 1."""

    def collect(self, request: CreateBriefRequest) -> list[dict[str, Any]]:
        del request
        return load_mock_evidence()


class LiveRetrievalAdapter(RetrievalAdapter):
    """Apify-backed retrieval for bounded live evidence collection."""

    def __init__(self, config: AppConfig):
        self._config = config
        self._apify_task_id = self._normalize_task_id(config.apify_task_id)
        self._apify_x_task_id = self._normalize_task_id(config.apify_x_task_id)
        self._bootstrap_warning: str | None = None
        self._bootstrap_apify_tasks_if_needed()

    def _normalize_task_id(self, task_id: str | None) -> str | None:
        if task_id is None:
            return None
        normalized = task_id.strip()
        if not normalized:
            return None
        # Apify accepts either a raw task ID or owner~task-name.
        # Users often copy owner/task-name from the UI, so normalize it here.
        if "/" in normalized and "~" not in normalized:
            owner, task_name = normalized.split("/", 1)
            return f"{owner}~{task_name}"
        return normalized

    def collect(self, request: CreateBriefRequest) -> list[dict[str, Any]]:
        if not self._config.enable_live_providers:
            return load_mock_evidence()
        collected: list[dict[str, Any]] = []
        primary_items: list[dict[str, Any]] = []
        primary_notices: list[dict[str, Any]] = []
        for task_input in self._build_primary_inputs(request):
            items, notice = self._run_task(
                request=request,
                task_id=self._apify_task_id,
                task_input=task_input,
                lane="primary_web",
            )
            primary_items.extend(items)
            if notice:
                primary_notices.append(notice)

        collected.extend(primary_items)
        if primary_items:
            collected.extend(
                notice for notice in primary_notices if notice["retrieval_status"] == "failed"
            )
        elif primary_notices:
            collected.append(primary_notices[0])

        if self._bootstrap_warning and not primary_items and not primary_notices:
            collected.append(
                self._build_notice(
                    lane="primary_web",
                    url=self._config.apify_base_url,
                    fact=self._bootstrap_warning,
                    raw_reference={"bootstrap": "failed"},
                )
            )

        if self._config.enable_x_signals and self._apify_x_task_id:
            x_items, x_notice = self._run_task(
                request=request,
                task_id=self._apify_x_task_id,
                task_input=self._build_x_input(request),
                lane="x_signals",
            )
            collected.extend(x_items)
            if x_notice:
                collected.append(x_notice)

        return collected or load_mock_evidence()

    def _bootstrap_apify_tasks_if_needed(self) -> None:
        if not self._config.enable_live_providers or not self._config.apify_api_token:
            return
        needs_primary = not self._apify_task_id
        needs_x = self._config.enable_x_signals and not self._apify_x_task_id
        if not needs_primary and not needs_x:
            return
        try:
            created = ensure_apify_tasks(
                token=self._config.apify_api_token,
                base_url=self._config.apify_base_url,
                include_x_signals=self._config.enable_x_signals,
            )
        except Exception as error:  # pragma: no cover - network failures are environment-specific
            self._bootstrap_warning = (
                "Apify task bootstrap failed. "
                "Provide APIFY_TASK_ID and APIFY_X_TASK_ID manually if automatic setup is unavailable. "
                f"Error: {error}"
            )
            log_event("retrieval.task.bootstrap_failed", error=str(error))
            return
        created_by_env = {item["env_var"]: item["task_id"] for item in created}
        self._apify_task_id = self._normalize_task_id(self._apify_task_id or created_by_env.get("APIFY_TASK_ID"))
        self._apify_x_task_id = self._normalize_task_id(self._apify_x_task_id or created_by_env.get("APIFY_X_TASK_ID"))
        log_event(
            "retrieval.task.bootstrap_succeeded",
            primary_task_id=self._apify_task_id,
            x_task_id=self._apify_x_task_id,
        )

    def _run_task(
        self,
        *,
        request: CreateBriefRequest,
        task_id: str | None,
        task_input: dict[str, Any],
        lane: str,
    ) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
        if not task_id:
            return [], None

        query = urlencode(
            {
                "token": self._config.apify_api_token or "",
                "timeout": str(self._config.apify_timeout_seconds),
                "format": "json",
                "clean": "1",
                "limit": str(self._config.apify_max_items),
            }
        )
        base_url = self._config.apify_base_url.rstrip("/")
        url = f"{base_url}/actor-tasks/{task_id}/run-sync-get-dataset-items?{query}"
        body = json.dumps(task_input).encode("utf-8")
        http_request = Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        last_error: Exception | None = None
        for attempt in range(1, self._config.apify_retry_attempts + 1):
            try:
                log_event("retrieval.task.attempt", lane=lane, attempt=attempt, task_id=task_id)
                with urlopen(http_request, timeout=self._config.apify_timeout_seconds + 5) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                break
            except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as error:
                last_error = error
                log_event("retrieval.task.retryable_failure", lane=lane, attempt=attempt, error=str(error))
        else:
            notice = self._build_notice(
                lane=lane,
                url=url,
                fact=f"{lane} retrieval failed after {self._config.apify_retry_attempts} attempts: {last_error}",
                raw_reference={"error": str(last_error), "task_input": task_input},
            )
            return [], notice

        items = payload if isinstance(payload, list) else []
        filtered_items = [item for item in items if not self._is_no_result_item(item)]
        if not filtered_items:
            log_event("retrieval.task.empty", lane=lane, task_id=task_id)
            notice = self._build_notice(
                lane=lane,
                url=url,
                fact=f"{lane} retrieval returned no usable results.",
                raw_reference={"task_input": task_input, "raw_payload": items[:3]},
                retrieval_status="empty",
            )
            return [], notice
        log_event("retrieval.task.succeeded", lane=lane, task_id=task_id, item_count=len(filtered_items))
        return [self._coerce_item(item, request=request, lane=lane) for item in filtered_items], None

    def _build_primary_inputs(self, request: CreateBriefRequest) -> list[dict[str, Any]]:
        return [
            {
                "query": query,
                "maxItems": max(self._config.apify_max_items, 5),
                "country": "us",
                "language": "en",
                "domain": "google.com",
            }
            for query in self._build_primary_queries(request)
        ]

    def _build_x_input(self, request: CreateBriefRequest) -> dict[str, Any]:
        return {
            "searchTerms": self._build_x_search_terms(request),
            "maxItems": max(self._config.apify_max_items * 2, 20),
            "sort": "Top",
            "tweetLanguage": "en",
            "includeSearchTerms": True,
        }

    def _coerce_item(
        self,
        item: dict[str, Any],
        *,
        request: CreateBriefRequest,
        lane: str,
    ) -> dict[str, Any]:
        query_context = self._extract_query_context(item)
        content_text = " ".join(
            str(value)
            for value in [
                item.get("title"),
                item.get("headline"),
                item.get("description"),
                item.get("summary"),
                item.get("snippet"),
                item.get("text"),
                item.get("full_text"),
                item.get("sourceUrl"),
                item.get("url"),
            ]
            if value
        )
        text_blob = f"{content_text} {query_context}".strip()

        affected_names = (
            item.get("affected_names")
            or item.get("tickers")
            or item.get("symbols")
            or self._extract_entity_symbols(item)
            or self._infer_affected_names(
                text_blob if lane == "primary_web" else content_text,
                request,
            )
        )
        if isinstance(affected_names, str):
            affected_names = [affected_names]

        author = item.get("author") if isinstance(item.get("author"), dict) else {}
        source_title = (
            item.get("source_title")
            or item.get("title")
            or item.get("headline")
            or (
                f"Tweet by @{author.get('screen_name')}"
                if lane == "x_signals" and author.get("screen_name")
                else None
            )
            or f"Apify {lane} item"
        )
        url = (
            item.get("url")
            or item.get("twitterUrl")
            or item.get("sourceUrl")
            or item.get("link")
            or ""
        )
        published_at = (
            item.get("published_at")
            or item.get("timestamp")
            or item.get("scrapedAt")
            or item.get("created_at")
            or item.get("date")
            or datetime.now(timezone.utc).isoformat()
        )
        snippet = (
            item.get("fact")
            or item.get("snippet")
            or item.get("text")
            or item.get("summary")
            or item.get("description")
            or item.get("full_text")
            or ""
        )
        inferred_factor = self._infer_factor(text_blob, request.themes, lane)
        interpretation = (
            item.get("interpretation")
            or item.get("why_it_matters")
            or item.get("analysis")
            or (
                f"Google search result matched '{query_context}'."
                if lane == "primary_web" and query_context
                else "Live evidence collected for downstream ranking and synthesis."
            )
        )
        source_type = (
            item.get("source_type")
            or item.get("document_type")
            or ("google_search_result" if lane == "primary_web" else "x_post")
        )
        category = item.get("category") or self._categorize_item(text_blob, url, lane)
        provider = item.get("provider") or "apify"
        signal_strength = item.get("signal_strength") or item.get("signal") or self._infer_signal_strength(
            item,
            lane=lane,
            affected_names=list(affected_names),
        )
        confidence_level = item.get("confidence_level") or self._infer_confidence_level(
            item,
            lane=lane,
            affected_names=list(affected_names),
        )
        digest = hashlib.sha1(f"{lane}|{source_title}|{url}".encode("utf-8")).hexdigest()[:12]

        return {
            "id": str(item.get("id") or item.get("item_id") or f"{lane}-{digest}"),
            "item_type": item.get("item_type", "evidence"),
            "category": category,
            "factor": item.get("factor") or inferred_factor,
            "affected_names": list(affected_names),
            "source_title": source_title,
            "url": url,
            "published_at": published_at,
            "recency_note": item.get("recency_note") or self._build_recency_note(lane, query_context),
            "fact": snippet or f"Live {lane} evidence collected from {source_title}.",
            "interpretation": interpretation,
            "why_it_matters": item.get("why_it_matters") or self._build_why_it_matters(
                lane=lane,
                query_context=query_context,
                affected_names=list(affected_names),
            ),
            "watchpoint": item.get("watchpoint") or self._build_watchpoint(lane, url),
            "change_label": item.get("change_label") or "new",
            "confidence_level": confidence_level,
            "signal_strength": signal_strength,
            "retrieval_status": item.get("retrieval_status") or "success",
            "provider": provider,
            "source_type": source_type,
            "raw_reference": item,
        }

    def _is_no_result_item(self, item: dict[str, Any]) -> bool:
        return (
            bool(item.get("noResults"))
            or bool(item.get("no_results"))
            or item.get("resultType") == "searchOverview"
        )

    def _build_notice(
        self,
        *,
        lane: str,
        url: str,
        fact: str,
        raw_reference: dict[str, Any],
        retrieval_status: str = "failed",
    ) -> dict[str, Any]:
        return {
            "id": f"retrieval-notice-{lane}",
            "item_type": "retrieval_notice",
            "category": "retrieval_status",
            "lane": lane,
            "source_title": f"Apify {lane} retrieval notice",
            "url": url,
            "published_at": datetime.now(timezone.utc).isoformat(),
            "recency_note": "Retrieved during current run",
            "fact": fact,
            "interpretation": "The brief is continuing with partial evidence rather than aborting.",
            "retrieval_status": retrieval_status,
            "confidence_level": "low",
            "signal_strength": "low",
            "provider": "apify",
            "source_type": lane,
            "raw_reference": raw_reference,
        }

    def _build_primary_queries(self, request: CreateBriefRequest) -> list[str]:
        queries: list[str] = []
        tracked_names = request.holdings or request.watchlist
        for symbol in tracked_names[:2]:
            primary_name = TICKER_ALIASES.get(symbol, [symbol])[0]
            queries.append(
                f'("{symbol}" OR "{primary_name}") ("earnings report" OR "investor relations" OR guidance OR "quarterly results")'
            )
            queries.append(
                f'("{symbol}" OR "{primary_name}") ("competitor" OR peer OR supplier OR customer OR pricing OR capacity)'
            )
        portfolio_terms = " OR ".join(f'"{symbol}"' for symbol in tracked_names[:4])
        hedge_fund_terms = " OR ".join(f'"{fund}"' for fund in TOP_HEDGE_FUNDS[:4])
        if portfolio_terms:
            queries.append(
                f'({portfolio_terms}) ("hedge fund" OR "13F" OR "fund letter" OR "investor letter") ({hedge_fund_terms})'
            )
            queries.append(
                f'({portfolio_terms}) (politics OR regulation OR export controls OR tariff OR policy)'
            )
            queries.append(
                f'({portfolio_terms}) ("industry news" OR semiconductor OR supply chain OR foundry OR capex)'
            )
        for theme in request.themes[:2]:
            queries.append(f'"{theme}" ("industry news" OR outlook OR policy OR regulation)')
        return queries[:8]

    def _build_x_search_terms(self, request: CreateBriefRequest) -> list[str]:
        search_terms: list[str] = []
        tracked_names = request.holdings or request.watchlist
        for symbol in tracked_names[:4]:
            aliases = TICKER_ALIASES.get(symbol, [])
            alias_term = f' OR "{aliases[0]}"' if aliases else ""
            search_terms.append(
                f'("${symbol}" OR "{symbol}"{alias_term}) (earnings OR stock OR semiconductor OR AI) lang:en -is:retweet'
            )
        if not search_terms:
            for theme in request.themes[:2]:
                search_terms.append(f'"{theme}" lang:en -is:retweet')
        return search_terms

    def _extract_query_context(self, item: dict[str, Any]) -> str:
        search_query = item.get("searchQuery")
        if isinstance(search_query, dict):
            return str(search_query.get("term") or search_query.get("query") or "")
        return str(
            item.get("query")
            or item.get("searchTerm")
            or item.get("matchedSearchTerm")
            or item.get("search_term")
            or ""
        )

    def _infer_affected_names(
        self,
        text_blob: str,
        request: CreateBriefRequest,
    ) -> list[str]:
        affected_names: list[str] = []
        upper_text = text_blob.upper()
        for symbol in request.holdings + request.watchlist:
            symbol_upper = symbol.upper()
            if re.search(rf"(?<![A-Z0-9])\$?{re.escape(symbol_upper)}(?![A-Z0-9])", upper_text):
                affected_names.append(symbol)
                continue
            for alias in TICKER_ALIASES.get(symbol, []):
                if alias.upper() in upper_text:
                    affected_names.append(symbol)
                    break
        return affected_names

    def _extract_entity_symbols(self, item: dict[str, Any]) -> list[str]:
        entities = item.get("entities")
        if not isinstance(entities, dict):
            return []
        symbols = entities.get("symbols")
        if not isinstance(symbols, list):
            return []
        extracted: list[str] = []
        for symbol in symbols:
            if isinstance(symbol, dict) and isinstance(symbol.get("text"), str):
                extracted.append(symbol["text"])
        return extracted

    def _infer_factor(self, text_blob: str, themes: list[str], lane: str) -> str:
        lowered = text_blob.lower()
        if "rate" in lowered or "yield" in lowered or "fed" in lowered:
            return "Rates and multiple compression sensitivity"
        if "hedge fund" in lowered or "13f" in lowered or "fund letter" in lowered or "investor letter" in lowered:
            return "Earnings revision sensitivity"
        if "china" in lowered or "export" in lowered or "regulation" in lowered or "policy" in lowered:
            return "China, regulation, or policy exposure"
        if "foundry" in lowered or "supply" in lowered or "lithography" in lowered or "asml" in lowered or "tsm" in lowered:
            return "Supply-chain concentration or foundry dependence"
        if "earnings" in lowered or "guidance" in lowered or "revenue" in lowered or "miss" in lowered:
            return "Earnings revision sensitivity"
        if "inventory" in lowered or "semiconductor" in lowered or "chip" in lowered or "demand" in lowered:
            return "Semiconductor demand and inventory cycle exposure"
        if "ai" in lowered or "infrastructure" in lowered or "capex" in lowered:
            return "AI capex and infrastructure sensitivity"
        if lane == "x_signals" and any(theme.lower() in lowered for theme in themes):
            return "AI capex and infrastructure sensitivity"
        return "Unmapped live factor"

    def _infer_signal_strength(
        self,
        item: dict[str, Any],
        *,
        lane: str,
        affected_names: list[str],
    ) -> str:
        if lane == "primary_web":
            return "high" if affected_names else "medium"
        author = item.get("author") if isinstance(item.get("author"), dict) else {}
        if author.get("screen_name") and (
            author.get("verified") or author.get("is_blue_verified") or author.get("followers_count", 0) > 100000
        ):
            return "medium"
        return "low"

    def _infer_confidence_level(
        self,
        item: dict[str, Any],
        *,
        lane: str,
        affected_names: list[str],
    ) -> str:
        if lane == "primary_web":
            return "medium" if affected_names else "low"
        author = item.get("author") if isinstance(item.get("author"), dict) else {}
        if author.get("verified") or author.get("is_blue_verified"):
            return "medium"
        return "low"

    def _categorize_item(self, text_blob: str, url: str, lane: str) -> str:
        if lane == "x_signals":
            return "x_signals"
        lowered = f"{text_blob} {url}".lower()
        if any(keyword in lowered for keyword in ["competitor", "peer", "rival", "supplier", "customer", "pricing", "capacity"]):
            return "peer"
        if "sec.gov" in lowered or "10-q" in lowered or "10-k" in lowered or "8-k" in lowered or "filing" in lowered:
            return "filing"
        if "investor" in lowered or "ir." in lowered:
            return "investor_relations"
        if "earnings" in lowered or "guidance" in lowered:
            return "earnings_material"
        if "hedge fund" in lowered or "13f" in lowered or "fund letter" in lowered or "investor letter" in lowered:
            return "hedge_fund_analysis"
        if "policy" in lowered or "regulation" in lowered or "export controls" in lowered or "politics" in lowered or "tariff" in lowered:
            return "policy_news"
        return "market_news"

    def _build_recency_note(self, lane: str, query_context: str) -> str:
        if lane == "primary_web" and query_context:
            return f"Matched live Google query: {query_context}"
        if lane == "x_signals" and query_context:
            return f"Matched live X query: {query_context}"
        return "Retrieved during current run"

    def _build_why_it_matters(
        self,
        *,
        lane: str,
        query_context: str,
        affected_names: list[str],
    ) -> str:
        if lane == "primary_web" and query_context:
            return f"The result matched the portfolio evidence query '{query_context}'."
        if lane == "x_signals" and affected_names:
            return f"Supplementary X context touching {', '.join(affected_names)}."
        return "Live evidence collected for downstream ranking and synthesis."

    def _build_watchpoint(self, lane: str, url: str) -> str:
        if lane == "primary_web" and url:
            return "Open the linked page and confirm the underlying filing, earnings report, hedge-fund analysis, or article."
        if lane == "x_signals":
            return "Look for confirmation from primary sources or company channels."
        return "Validate follow-through in the next refresh."
