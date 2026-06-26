"""
Shared Magento 2 REST API client — OAuth 1.0a auth, JSON helpers, pagination.
All other scripts import MagentoClient from here.
"""

import os
import sys
import json
import warnings
import logging
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util import Retry
    from requests_oauthlib import OAuth1
except ImportError:
    sys.exit("Missing dependencies. Run: uv pip install requests requests-oauthlib")


# Set up basic logging to stderr for internal debugging if MAGENTO_DEBUG is set
if os.environ.get("MAGENTO_DEBUG"):
    logging.basicConfig(level=logging.DEBUG, stream=sys.stderr, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("magento_client")


class MagentoAPIError(Exception):
    def __init__(self, status: int, message: str, url: str = ""):
        self.status = status
        self.url = url
        super().__init__(message)

    def to_json(self) -> str:
        return json.dumps({"error": f"{self.status}", "message": str(self), "url": self.url})


class MagentoClient:
    def __init__(self, site: str | None = None):
        self._site_suffix = str(site).upper() if site else None
        self.site = site
        self.base_url = self._require_env("MAGENTO_BASE_URL").rstrip("/")
        self.timeout = int(self._env_with_fallback("MAGENTO_TIMEOUT", "30"))
        self.auth = OAuth1(
            client_key=self._require_env("MAGENTO_CONSUMER_KEY"),
            client_secret=self._require_env("MAGENTO_CONSUMER_SECRET"),
            resource_owner_key=self._require_env("MAGENTO_ACCESS_TOKEN"),
            resource_owner_secret=self._require_env("MAGENTO_ACCESS_TOKEN_SECRET"),
            signature_method="HMAC-SHA256",
        )
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "Accept": "application/json"})

        # Setup retries for transient errors
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _require_env(self, name: str) -> str:
        lookup = f"{name}_{self._site_suffix}" if self._site_suffix else name
        value = os.environ.get(lookup)
        if not value:
            sys.exit(json.dumps({"error": "missing_env", "message": f"Environment variable {lookup!r} is not set.", "url": ""}))
        return value

    def _env_with_fallback(self, name: str, default: str) -> str:
        if self._site_suffix:
            value = os.environ.get(f"{name}_{self._site_suffix}")
            if value:
                return value
        return os.environ.get(name, default)

    def _url(self, path: str) -> str:
        # We must encode path segments (especially SKUs) that might contain spaces or slashes.
        # Magento expects slashes within a SKU to be encoded (e.g., %2F).
        # Split by / and encode each part, then join.
        # If the path already starts with /rest/ then we don't prepend /rest/V1/
        if path.startswith("/rest/"):
             return f"{self.base_url}{path}"
        
        parts = [urllib.parse.quote(p, safe="") for p in path.lstrip("/").split("/")]
        return f"{self.base_url}/rest/V1/{'/'.join(parts)}"

    def _raise_for_status(self, resp: requests.Response) -> None:
        if not resp.ok:
            try:
                body = resp.json()
                message = body.get("message", resp.text)
            except Exception:
                message = resp.text
            raise MagentoAPIError(resp.status_code, message, resp.url)

    def get(self, path: str, params: dict | None = None) -> Any:
        resp = self.session.get(self._url(path), params=params, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def post(self, path: str, body: dict) -> Any:
        resp = self.session.post(self._url(path), json=body, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def put(self, path: str, body: dict) -> Any:
        resp = self.session.put(self._url(path), json=body, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def delete(self, path: str) -> Any:
        resp = self.session.delete(self._url(path), auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()

    def search(
        self,
        resource: str,
        filters: list[dict | list[dict]] | None = None,
        page_size: int = 20,
        current_page: int = 1,
        sort_field: str | None = None,
        sort_dir: str = "DESC",
    ) -> dict:
        """
        Build a Magento search criteria query and GET the resource.

        filters: list of (dict or list of dicts).
        Each top-level element is a filterGroup (ANDed).
        If an element is a list, its contents are filters within that group (ORed).
        """
        params: dict[str, Any] = {
            "searchCriteria[pageSize]": page_size,
            "searchCriteria[currentPage]": current_page,
        }

        if sort_field:
            params["searchCriteria[sortOrders][0][field]"] = sort_field
            params["searchCriteria[sortOrders][0][direction]"] = sort_dir

        for i, group in enumerate(filters or []):
            if not isinstance(group, list):
                group = [group]
            for j, f in enumerate(group):
                params[f"searchCriteria[filterGroups][{i}][filters][{j}][field]"] = f["field"]
                params[f"searchCriteria[filterGroups][{i}][filters][{j}][value]"] = f["value"]
                params[f"searchCriteria[filterGroups][{i}][filters][{j}][conditionType]"] = f.get("condition_type", "eq")

        resp = self.session.get(self._url(resource), params=params, auth=self.auth, timeout=self.timeout)
        self._raise_for_status(resp)
        return resp.json()


def print_error_and_exit(err: MagentoAPIError) -> None:
    print(err.to_json(), file=sys.stderr)
    sys.exit(1)


def get_client(site: str | None = None) -> MagentoClient:
    """Convenience factory — call this at the top of each script."""
    return MagentoClient(site=site)


def list_configured_sites() -> tuple[list[str], bool]:
    """Discover configured sites by scanning MAGENTO_BASE_URL_* env vars."""
    prefix = "MAGENTO_BASE_URL_"
    sites = sorted(
        key[len(prefix):].lower()
        for key in os.environ
        if key.startswith(prefix)
    )
    has_default = bool(os.environ.get("MAGENTO_BASE_URL"))
    return sites, has_default


# ---------------------------------------------------------------------------
# Shared utility functions
# ---------------------------------------------------------------------------

def fetch_all(client, resource: str, filters: list | None = None,
              max_pages: int | None = 50, page_size: int = 200) -> list[dict]:
    """Fetch all pages for a given resource.

    Safety guardrails:
    - max_pages limits pagination (default 50 pages = 10,000 items)
    - Set max_pages=None to disable the limit (may be needed for very large catalogs)
    - Avoids infinite loops or OOM for large catalogs
    """
    all_items: list[dict] = []
    page = 1
    result: dict = {}
    while True:
        result = client.search(
            resource,
            filters=filters,
            page_size=page_size,
            current_page=page,
        )
        items = result.get("items", [])
        all_items.extend(items)
        # Stop when we've fetched all reported items or the API returns no items.
        if len(all_items) >= result.get("total_count", 0) or not items:
            break
        page += 1
        # Enforce max_pages guardrail only when it is explicitly set.
        if max_pages is not None and page > max_pages:
            total = result.get("total_count", "unknown")
            warnings.warn(
                f"fetch_all: reached max_pages={max_pages} limit. "
                f"Fetched {len(all_items)} of {total} total items. "
                f"Results are truncated — consider narrowing filters "
                f"or calling fetch_all(..., max_pages=None) for no limit.",
                stacklevel=2,
            )
            break
    return all_items


def utc_range(hours: int = 24) -> tuple[str, str]:
    """Return (start, end) UTC datetime strings for the last N hours."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    return start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S")


def env_default(env_key: str, cli_value, hardcoded_default):
    """Read config with priority: CLI arg > env var > hardcoded default."""
    if cli_value is not None:
        return cli_value
    env_val = os.environ.get(env_key)
    if env_val is not None:
        return type(hardcoded_default)(env_val)
    return hardcoded_default


def parse_csv_input(csv_path: str | None, items_str: str | None,
                    expected_columns: list[str]) -> list[dict]:
    """Parse bulk input from CSV file or inline comma/colon-delimited string.

    CSV format: header row matching expected_columns, then data rows.

    Inline format:
      - Comma-separated entries.
      - Each entry may be:
          * A single value, mapped to the first expected column.
          * Colon-separated positional values (e.g. "VAL1:VAL2[:VAL3...]"),
            assigned to expected_columns in order.

    Note: inline format uses colons as delimiters, so values containing
    colons (e.g. SKUs like "CONFIG:RED:L") cannot be used inline.
    Use --csv instead for such cases.

    Returns list of dicts with keys drawn from expected_columns.
    """
    import csv

    if csv_path:
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = []
                for row in reader:
                    parsed = {}
                    for col in expected_columns:
                        val = row.get(col, "").strip()
                        if val:
                            parsed[col] = val
                    if parsed:
                        rows.append(parsed)
                return rows
        except OSError as e:
            print(f"Error: could not read CSV file '{csv_path}': {e}", file=sys.stderr)
            sys.exit(1)

    if items_str:
        rows = []
        for entry in items_str.split(","):
            entry = entry.strip()
            if not entry:
                continue
            if ":" in entry:
                parts = entry.split(":", maxsplit=len(expected_columns) - 1)
                row = {}
                for i, col in enumerate(expected_columns):
                    if i < len(parts):
                        row[col] = parts[i].strip()
                rows.append(row)
            else:
                rows.append({expected_columns[0]: entry})
        return rows

    return []


# ---------------------------------------------------------------------------
# Structured output protocol for Morning Brief and Diagnose
# ---------------------------------------------------------------------------

@dataclass
class SectionResult:
    title: str
    status: str  # "ok" | "warning" | "error" | "skipped"
    elapsed_seconds: float = 0.0
    rows: list[dict] | None = None
    findings: list[str] | None = None
    error: str | None = None


def _section_to_dict(s: SectionResult) -> dict:
    """Convert a SectionResult to a JSON-friendly dict."""
    entry = {
        "title": s.title,
        "status": s.status,
        "elapsed_seconds": round(s.elapsed_seconds, 1),
    }
    if s.rows is not None:
        entry["rows"] = s.rows
    if s.findings is not None:
        entry["findings"] = s.findings
    if s.error is not None:
        entry["error"] = s.error
    return entry


def render_sections(sections: list[SectionResult], format: str = "markdown") -> str:
    """Render sections as markdown (human) or JSON (AI agent consumption)."""
    if format == "json":
        return json.dumps([_section_to_dict(s) for s in sections],
                          indent=2, ensure_ascii=False)

    # Markdown output
    lines: list[str] = []
    for s in sections:
        status_icon = {"ok": "✓", "warning": "⚠", "error": "✗", "skipped": "—"}.get(s.status, "")
        lines.append(f"## {s.title} [{s.elapsed_seconds:.1f}s] {status_icon}")
        if s.error:
            lines.append(f"Error: {s.error}")
        elif s.rows:
            headers = list(s.rows[0].keys())
            row_data = [[r.get(h, "") for h in headers] for r in s.rows]
            try:
                from tabulate import tabulate
                lines.append(tabulate(row_data, headers=headers, tablefmt="github"))
            except ImportError:
                lines.append(str(row_data))
        elif s.findings:
            for f in s.findings:
                lines.append(f"- {f}")
        lines.append("")
    return "\n".join(lines)