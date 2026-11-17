#!/usr/bin/env python3
"""
Copyright (c) 2026 JRSoft Technology Ltd.
Licensed under the MIT License.
Version: 1.0.4

InsurAI API Helper - Wraps all InsurAI API calls.

Minimum software requirements:
  - Python  : 3.9 or higher (CPython)
  - Library : requests, provided by the trusted runtime environment

To verify dependencies before running:
    python3 -c "import requests; print(requests.__version__)"

Optimizations:
  - Session reuse with connection pooling
  - Retry with exponential backoff for transient failures
  - Per-endpoint timeout tuning
  - API key validation on startup
  - Batch parallel metadata lookups (preserves input order)
  - Progress indicator for long operations
  - Rate-limit (429) handling with Retry-After
  - Minified JSON output option
"""
import sys
import json
import os
import argparse
import time
import concurrent.futures
from urllib.parse import urlparse
from typing import Any, Dict, List, Optional, Tuple

# ── Lazy HTTP dependencies ───────────────────────────────────────────────────
Session = Any
adapters = None
exceptions = None
_http_dependencies_loaded = False

def _load_http_dependencies() -> None:
    global Session, adapters, exceptions
    global _http_dependencies_loaded

    if _http_dependencies_loaded:
        return

    try:
        from requests import Session as RequestsSession
        from requests import adapters as requests_adapters
        from requests import exceptions as requests_exceptions
    except ImportError:
        sys.stderr.write(
            "[insurai_api] ERROR: 'requests' and its dependencies are not installed.\n"
            "[insurai_api] Provide the 'requests' package in the trusted runtime environment before running this helper.\n"
        )
        sys.exit(1)

    Session = RequestsSession
    adapters = requests_adapters
    exceptions = requests_exceptions
    _http_dependencies_loaded = True

# ── Configuration ──────────────────────────────────────────────────────────────
BASE = os.environ.get("INSURAI_AGENT_URL", "https://insurai.com.tw/insurai/agent").rstrip("/")

HEADERS = {"Content-Type": "application/json"}


def _get_api_key() -> str:
    """Read only the documented InsurAI API key; never enumerate environment variables."""
    try:
        return os.environ["INSURAI_API_KEY"].strip()
    except KeyError:
        return ""


def _validate_base_url() -> None:
    parsed = urlparse(BASE)
    if parsed.scheme != "https" or not parsed.netloc:
        raise RuntimeError("INSURAI_AGENT_URL must be an https URL.")

# Per-operation timeouts (seconds)
TIMEOUTS = {
    "occupations_search": 30,
    "plan_interpret":      60,
    "recommend":          60,
    "search":             60,
    "metadata":           15,   # quick lookup, can batch
    "document":          120,   # large content
    "pdf_link":           120,
}

# ── Session with connection pooling ────────────────────────────────────────────
_session = None

def get_session() -> Session:
    global _session
    _load_http_dependencies()
    api_key = _get_api_key()
    headers = {**HEADERS, "X-API-KEY": api_key}
    if _session is None:
        _session = Session()
        # Increase pool size for batch operations
        _session.mount("https://", adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=0,  # we handle retries manually
        ))
        _session.headers.update(headers)
    elif _session.headers.get("X-API-KEY") != api_key:
        # API key changed (e.g. reloaded in long-running process) — refresh headers
        _session.headers.update(headers)
    return _session

# ── Global flags (set once at startup, read by retry/logic helpers) ───────────────
_QUIET = False

# ── Retry logic ───────────────────────────────────────────────────────────────
def _request_with_retry(method: str, url: str, timeout: int,
                        max_retries: int = 3, backoff_base: float = 2,
                        **kwargs) -> Any:
    """
    Execute HTTP request with exponential backoff retry.
    Handles 429 Rate-Limit (respects Retry-After header) and 5xx transient errors.

    Args:
        method: HTTP method (GET, POST, etc.)
        url: Full URL to request
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts (default 3)
        backoff_base: Exponential base for wait calculation (default 2)
        **kwargs: Additional arguments passed to session.request()

    Returns:
        Response object. On success, the non-retryable response (2xx/3xx/4xx).
        If retries are exhausted on persistent 429/5xx, the LAST such response is
        returned so the caller (_check_response) can surface its real status code.

    Raises:
        last_exc: The last connection-level exception if every attempt failed to
            reach the server and no HTTP response was ever received.
    """
    _validate_base_url()
    session = get_session()
    last_exc: Optional[Exception] = None
    last_retryable_response: Any = None  # last 429/5xx seen; surfaced if retries exhaust

    def _log(msg: str) -> None:
        if not _QUIET:
            print(msg, file=sys.stderr)

    for attempt in range(1, max_retries + 1):
        is_last_attempt = attempt == max_retries
        try:
            response = session.request(method, url, timeout=timeout, **kwargs)

            if response.status_code == 429:
                last_retryable_response = response
                if is_last_attempt:
                    break  # don't sleep after the final attempt — no retry follows
                # Respect Retry-After header if present; fall back to 5s, ignore non-numeric
                retry_after_raw = response.headers.get("Retry-After", "5")
                try:
                    retry_after = int(retry_after_raw)
                except ValueError:
                    retry_after = 5
                _log(f"[insurai_api] 429 Rate-Limited — waiting {retry_after}s before retry (attempt {attempt}/{max_retries})...")
                time.sleep(retry_after)
                continue

            if 500 <= response.status_code < 600:
                # Transient server error — retry with exponential backoff
                last_retryable_response = response
                if is_last_attempt:
                    break
                wait = backoff_base ** attempt
                _log(f"[insurai_api] HTTP {response.status_code} — retrying in {wait}s (attempt {attempt}/{max_retries})...")
                time.sleep(wait)
                continue

            # Non-retryable status (2xx, 3xx, 4xx) — return as-is; caller handles
            return response

        except (exceptions.ConnectionError, exceptions.Timeout,
                exceptions.RequestException) as e:
            last_exc = e
            if is_last_attempt:
                break
            wait = backoff_base ** attempt
            _log(f"[insurai_api] Connection error: {e} — retrying in {wait}s (attempt {attempt}/{max_retries})...")
            time.sleep(wait)

    # All retries exhausted — prefer surfacing the real HTTP status over a generic error
    if last_retryable_response is not None:
        return last_retryable_response
    raise last_exc or RuntimeError(f"Request failed after {max_retries} retries")

# ── HTTP Status validation ────────────────────────────────────────────────────
def _check_response(response: Any) -> Dict[str, Any]:
    """
    Validate HTTP response before parsing JSON.
    Raises RuntimeError for 4xx client errors and 5xx server errors.
    Returns JSON dict for successful responses.
    """
    if 200 <= response.status_code < 300:
        content_type = response.headers.get("Content-Type", "")
        if "json" not in content_type.lower():
            snippet = response.text[:200].replace("\n", " ").strip()
            raise RuntimeError(
                "Expected JSON response but received "
                f"{content_type or 'unknown content type'} from {response.url}. "
                "Check INSURAI_AGENT_URL and reverse proxy routing. "
                f"Response preview: {snippet}"
            )
        try:
            return response.json()
        except ValueError as e:
            raise RuntimeError(f"Invalid JSON response from {response.url}: {e}") from e
    if response.status_code == 402:
        # Insufficient credits — surface clearly (ProblemDetail uses "detail")
        try:
            body = response.json()
            reason = body.get("detail", body.get("message", body.get("error", "insufficient credits")))
        except Exception:
            reason = response.text[:200] or "insufficient credits"
        raise RuntimeError(f"點數不足 (402 Payment Required): {reason}")
    if 400 <= response.status_code < 500:
        # Try to parse error body, but don't trust it blindly
        try:
            body = response.json()
            reason = body.get("message", body.get("error", body.get("detail", response.text[:200])))
        except Exception:
            reason = response.text[:200] or f"HTTP {response.status_code}"
        raise RuntimeError(f"Client error {response.status_code}: {reason}")
    if 500 <= response.status_code < 600:
        raise RuntimeError(f"Server error {response.status_code}: {response.text[:200]}")
    # Unexpected status
    raise RuntimeError(f"Unexpected HTTP {response.status_code}: {response.text[:200]}")

# ── API Functions ─────────────────────────────────────────────────────────────
def occupations_search(keyword: str, timeout: int = None) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["occupations_search"]
    resp = _request_with_retry(
        "get",
        f"{BASE}/api/skill/v1/occupations/search",
        params={"q": keyword},
        timeout=timeout,
    )
    return _check_response(resp)

def insur_plan_interpret(scenario: str, timeout: int = None) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["plan_interpret"]
    resp = _request_with_retry(
        "post",
        f"{BASE}/api/skill/v1/insur-plan/interpret",
        json={"scenario": scenario},
        timeout=timeout,
    )
    return _check_response(resp)

def insur_contracts_recommend(
    protection_names, age=None, gender=None,
    insurers=None, occupation_level=None,
    recommend_type: str = "main",
    timeout: int = None
) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["recommend"]
    body: Dict[str, Any] = {"protectionNames": protection_names, "recommendType": recommend_type}
    if age is not None: body["age"] = age
    if gender: body["gender"] = gender
    if insurers: body["insurers"] = insurers
    if occupation_level is not None: body["occupationLevel"] = occupation_level
    resp = _request_with_retry(
        "post",
        f"{BASE}/api/skill/v1/insur-contracts/recommend",
        json=body,
        timeout=timeout,
    )
    return _check_response(resp)

def insur_contracts_search(
    q=None, product_name=None, protection_names=None,
    insurers=None, available_product=True,
    occupation_level=None, gender=None, age=None,
    page_size: int = 10, timeout: int = None
) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["search"]
    body: Dict[str, Any] = {"pageSize": page_size}
    if q: body["q"] = q
    if product_name: body["productName"] = product_name
    if protection_names: body["protectionNames"] = protection_names
    if insurers: body["insurers"] = insurers
    body["availableProduct"] = available_product
    if occupation_level is not None: body["occupationLevel"] = occupation_level
    if gender: body["gender"] = gender
    if age is not None: body["age"] = age
    resp = _request_with_retry(
        "post",
        f"{BASE}/api/skill/v1/insur-contracts/search",
        json=body,
        timeout=timeout,
    )
    return _check_response(resp)

def insur_contracts_metadata(product_code: str, timeout: int = None) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["metadata"]
    resp = _request_with_retry(
        "get",
        f"{BASE}/api/skill/v1/insur-contracts/{product_code}/metadata",
        timeout=timeout,
    )
    return _check_response(resp)

def insur_contracts_document(product_code: str, campaign_overview_type: str = "contract", timeout: int = None) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["document"]
    resp = _request_with_retry(
        "get",
        f"{BASE}/api/skill/v1/insur-contracts/{product_code}/document",
        params={"campaignOverviewType": campaign_overview_type},
        timeout=timeout,
    )
    return _check_response(resp)

def insur_contracts_pdf_link(product_code: str, campaign_overview_type: str = "contract", timeout: int = None) -> Dict[str, Any]:
    timeout = timeout or TIMEOUTS["pdf_link"]
    resp = _request_with_retry(
        "get",
        f"{BASE}/api/skill/v1/insur-contracts/{product_code}/pdf-link",
        params={"campaignOverviewType": campaign_overview_type},
        timeout=timeout,
    )
    return _check_response(resp)

# ── Batch parallel lookup ──────────────────────────────────────────────────────
def batch_metadata(product_codes: List[str], show_progress: bool = False) -> List[Dict[str, Any]]:
    """
    Fetch metadata for multiple product codes in parallel using threading.
    Preserves input order (results returned in same order as codes were provided).
    Returns list of results (with 'code', 'company', 'name', 'type' or 'error' keys).

    Raises:
        RuntimeError: if ALL codes fail (all items return errors)
    """
    total = len(product_codes)
    if total == 0:
        return []  # nothing to fetch; avoids ThreadPoolExecutor(max_workers=0) / empty all() pitfalls
    # pre-allocate distinct dicts to preserve order (NOT [{}] * total — that aliases one dict)
    results: List[Dict[str, Any]] = [{} for _ in range(total)]
    max_workers = min(8, total)  # bound by code count

    def fetch_one(code: str, index: int) -> Tuple[int, Dict[str, Any]]:
        try:
            data = insur_contracts_metadata(code)
            meta = data.get("metadata") or {}
            if not isinstance(meta, dict):
                raise ValueError("metadata is not a JSON object")
            return (index, {
                "code": code,
                "company": meta.get("insuranceCompany", "N/A"),
                "name": meta.get("productName", "N/A"),
                "type": meta.get("contractType", "N/A"),
            })
        except Exception as e:
            return (index, {"code": code, "error": str(e)})

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(fetch_one, code, i): i
            for i, code in enumerate(product_codes)
        }
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            index, result = future.result()
            results[index] = result
            completed += 1
            if show_progress:
                print(f"[insurai_api] Progress: {completed}/{total}", file=sys.stderr)

    # Detect all-failure — if every result has an 'error' key, surface it
    if all("error" in r for r in results):
        error_msgs = [r["error"] for r in results]
        raise RuntimeError(f"All {total} metadata lookups failed: {error_msgs[0]}")

    return results

# ── CLI ────────────────────────────────────────────────────────────────────────
USAGE = """InsurAI API Helper  v1.0.4
Usage:
  python3 insurai_api.py occupations_search --keyword <keyword>
  python3 insurai_api.py plan_interpret     --scenario <text>
  python3 insurai_api.py recommend         --protection <name> [--age N --gender M --occupation-level N --recommend-type main|main-rider]
  python3 insurai_api.py search            --q <query> [--page-size N]
  python3 insurai_api.py metadata          --product-code <code>
  python3 insurai_api.py document          --product-code <code> [--campaign-type contract|premium]
  python3 insurai_api.py pdf_link         --product-code <code> [--campaign-type contract|premium]
  python3 insurai_api.py batch-metadata    --codes <code> [<code>...]  # parallel lookup
"""

def _main():
    parser = argparse.ArgumentParser(
        description="InsurAI API Helper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=USAGE,
        allow_abbrev=False,
    )
    parser.add_argument("action", help="Action: occupations_search, plan_interpret, recommend, search, metadata, document, pdf_link, batch-metadata")
    parser.add_argument("--keyword")
    parser.add_argument("--scenario")
    parser.add_argument("--protection", nargs="+")
    parser.add_argument("--age", type=int)
    parser.add_argument("--gender")
    parser.add_argument("--insurers", nargs="+")
    parser.add_argument("--occupation-level", type=int)
    parser.add_argument("--recommend-type", default="main")
    parser.add_argument("--product-code")
    parser.add_argument("--campaign-type", default="contract")
    parser.add_argument("--q")
    parser.add_argument("--product-name")
    parser.add_argument(
        "--available-product",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Filter search to currently available products",
    )
    parser.add_argument("--page-size", type=int, default=10)
    parser.add_argument("--codes", nargs="+", help="Product codes for batch-metadata")
    parser.add_argument("--minify", action="store_true", help="Output compact JSON (no indentation)")
    parser.add_argument("--quiet", action="store_true", help="Suppress progress messages to stderr")
    parser.add_argument("--timeout", type=int, default=None, help="Override timeout for this call (seconds)")

    args = parser.parse_args()
    available_product_specified = any(
        arg in ("--available-product", "--no-available-product")
        for arg in sys.argv[1:]
    )

    # ── Global flag: quiet mode ─────────────────────────────────────────────────
    global _QUIET
    _QUIET = bool(args.quiet)

    # ── One-time validation at CLI entry ──────────────────────────────────────
    if not _get_api_key():
        print("[insurai_api] ERROR: INSURAI_API_KEY environment variable is not set.", file=sys.stderr)
        print(
            "[insurai_api] Register at https://insurai.com.tw and apply for an INSURAI-API-KEY, then run:",
            file=sys.stderr,
        )
        print("[insurai_api] export INSURAI_API_KEY='your_api_key_here'", file=sys.stderr)
        sys.exit(1)

    # ── Parameter validation ───────────────────────────────────────────────────
    errors: List[str] = []

    if args.action == "recommend":
        # recommend does NOT support availableProduct — fixed to true server-side
        if available_product_specified and not args.quiet:
            print("[insurai_api] WARNING: --available-product/--no-available-product is ignored for 'recommend' "
                  "(availableProduct is fixed to true).", file=sys.stderr)
        if not args.protection:
            errors.append("recommend requires --protection <name> [<name>...]")
        # recommendType must be main or main-rider
        if args.recommend_type not in ("main", "main-rider"):
            errors.append(f"--recommend-type must be 'main' or 'main-rider', got '{args.recommend_type}'")

    if args.action in ("search", "document", "pdf_link", "metadata"):
        if available_product_specified and args.action != "search":
            errors.append(f"--available-product/--no-available-product is only valid for 'search', not '{args.action}'")

    if args.gender and args.gender not in ("male", "female"):
        errors.append(f"--gender must be 'male' or 'female', got '{args.gender}'")

    if args.age is not None and args.age <= 0:
        errors.append(f"--age must be a positive integer, got {args.age}")

    if args.occupation_level is not None and not (1 <= args.occupation_level <= 6):
        errors.append(f"--occupation-level must be 1-6, got {args.occupation_level}")

    if args.campaign_type not in ("contract", "premium"):
        errors.append(f"--campaign-type must be 'contract' or 'premium', got '{args.campaign_type}'")

    if args.page_size <= 0:
        errors.append(f"--page-size must be positive, got {args.page_size}")

    if args.page_size > 100 and not args.quiet:
        print(f"[insurai_api] WARNING: --page-size {args.page_size} is large; results may be truncated server-side.", file=sys.stderr)

    if args.action == "occupations_search" and not (args.keyword or "").strip():
        errors.append("occupations_search requires --keyword <keyword>")

    if args.action == "plan_interpret" and not (args.scenario or "").strip():
        errors.append("plan_interpret requires --scenario <text>")

    if args.action == "search" and not any([
        (args.q or "").strip(),
        (args.product_name or "").strip(),
        args.protection,
    ]):
        errors.append("search requires at least one of --q, --product-name, or --protection")

    if args.codes:
        if len(args.codes) > 500:
            errors.append(f"--codes上限為500筆（收到 {len(args.codes)} 筆），請分批執行")
        # batch_metadata max_workers bounded by code count
        if len(args.codes) > 100 and not args.quiet:
            print(f"[insurai_api] WARNING: --codes {len(args.codes)} is large; consider batching.", file=sys.stderr)

    if errors:
        for e in errors:
            print(json.dumps({"error": e}))
        sys.exit(1)

    result = None
    action = args.action

    try:
        if action == "occupations_search":
            result = occupations_search(args.keyword or "", timeout=args.timeout)

        elif action == "plan_interpret":
            result = insur_plan_interpret(args.scenario or "", timeout=args.timeout)

        elif action == "recommend":
            result = insur_contracts_recommend(
                args.protection or [],
                age=args.age,
                gender=args.gender,
                insurers=args.insurers,
                occupation_level=args.occupation_level,
                recommend_type=args.recommend_type,
                timeout=args.timeout,
            )

        elif action == "search":
            result = insur_contracts_search(
                q=args.q,
                product_name=args.product_name,
                protection_names=args.protection,
                insurers=args.insurers,
                available_product=args.available_product,
                occupation_level=args.occupation_level,
                gender=args.gender,
                age=args.age,
                page_size=args.page_size,
                timeout=args.timeout,
            )

        elif action == "metadata":
            code = args.product_code or ""
            if not code:
                print(json.dumps({"error": "metadata requires --product-code <code>"}), file=sys.stderr)
                sys.exit(1)
            result = insur_contracts_metadata(code, timeout=args.timeout)

        elif action == "document":
            code = args.product_code or ""
            if not code:
                print(json.dumps({"error": "document requires --product-code <code>"}), file=sys.stderr)
                sys.exit(1)
            result = insur_contracts_document(code, args.campaign_type, timeout=args.timeout)

        elif action == "pdf_link":
            code = args.product_code or ""
            if not code:
                print(json.dumps({"error": "pdf_link requires --product-code <code>"}), file=sys.stderr)
                sys.exit(1)
            result = insur_contracts_pdf_link(code, args.campaign_type, timeout=args.timeout)

        elif action == "batch-metadata":
            if not args.codes:
                print(json.dumps({"error": "batch-metadata requires --codes <code> [<code>...]"}), file=sys.stderr)
                sys.exit(1)
            if not args.quiet:
                print(f"[insurai_api] Fetching metadata for {len(args.codes)} codes in parallel...", file=sys.stderr)
            result = batch_metadata(args.codes, show_progress=not args.quiet)

        else:
            print(json.dumps({"error": f"Unknown action: {action}"}))
            sys.exit(1)

        # Output JSON — minified or pretty-printed
        separators = (",", ":") if args.minify else (",", ": ")
        print(json.dumps(result, ensure_ascii=False, indent=2 if not args.minify else None, separators=separators))

    except KeyboardInterrupt:
        print("\n[insurai_api] Interrupted.", file=sys.stderr)
        sys.exit(130)
    except RuntimeError as e:
        # Structured errors from _check_response — already clear
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    _main()
