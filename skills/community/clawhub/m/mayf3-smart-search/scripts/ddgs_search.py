#!/usr/bin/env python3.12
"""
DDGS Smart Search v3.6 - Multi-backend search with auto-lang detection, timeout,
type support, extract, retry, fallback, batch, multi-type, quiet, and urls-only.

Usage:
  # Text search (default)
  python3.12 ddgs_search.py -q "search query" [-b backend] [-m max_results] [-t timelimit] [-o json]

  # Show version
  python3.12 ddgs_search.py --version

  # Type-specific search (supports --fallback auto-fallback chain)
  python3.12 ddgs_search.py -q "search query" --type news --fallback
  python3.12 ddgs_search.py -q "search query" --type images --fallback
  python3.12 ddgs_search.py -q "search query" --type videos --fallback
  python3.12 ddgs_search.py -q "search query" --type books

  # Multi-type search (text + news + videos)
  python3.12 ddgs_search.py -q "search query" --type all
  # Multi-type search with images (text + news + videos + images)
  python3.12 ddgs_search.py -q "search query" --type all+

  # Extract full text from a URL (after search)
  python3.12 ddgs_search.py -q "search query" --extract
  python3.12 ddgs_search.py --extract-url "https://example.com/article"

  # Batch search (one query per line from file)
  python3.12 ddgs_search.py --batch-file queries.txt [-b backend] [-m 3] [-o json]

  # Retry with exponential backoff
  python3.12 ddgs_search.py -q "query" --retries 3

  # Auto fallback through backends (auto-detects CN/EN query)
  python3.12 ddgs_search.py -q "query" --fallback

  # Global timeout (seconds)
  python3.12 ddgs_search.py -q "query" --timeout 15

  # Extract length control
  python3.12 ddgs_search.py -q "query" --extract --extract-length 5000

  # Force language for backend chain
  python3.12 ddgs_search.py -q "query" --lang cn --fallback
  python3.12 ddgs_search.py -q "query" --lang en --fallback

  # Quiet mode (suppress stderr retry/timeout messages)
  python3.12 ddgs_search.py -q "query" --quiet --fallback

  # URLs only (one URL per line, for piping)
  python3.12 ddgs_search.py -q "query" --urls-only --fallback
  python3.12 ddgs_search.py -q "query" --urls-only --fallback | xargs -I{} curl {}

Search types: text, news, images, videos, books, all, all+ (default: text)
Backends: auto, all, bing, brave, duckduckgo, google, yandex, yahoo, wikipedia
Timelimit: d (day), w (week), m (month), y (year)

Examples:
  python3.12 ddgs_search.py -q "AI agent framework 2026"
  python3.12 ddgs_search.py -q "搜索API对比" --fallback -m 5
  python3.12 ddgs_search.py -q "site:github.com ddgs" -b brave
  python3.12 ddgs_search.py -q "LLM news" --type news --fallback -o json
  python3.12 ddgs_search.py -q "machine learning" --type books --fallback -o json
  python3.12 ddgs_search.py -q "python tutorial" --type videos --fallback
  python3.12 ddgs_search.py -q "AI news" --type all -m 3
  python3.12 ddgs_search.py -q "AI news" --type all+ -m 3
  python3.12 ddgs_search.py -q "query" --extract -o json
  python3.12 ddgs_search.py -q "query" --fallback --retries 2 --timeout 20
  python3.12 ddgs_search.py -q "query" --urls-only --fallback | head -5
"""

import argparse
import json
import random
import re
import signal
import sys
import threading
import time

VERSION = "3.6"

# Preferred backend chains for different scenarios
FALLBACK_CHAIN_EN = ["brave", "yandex", "yahoo", "bing"]
FALLBACK_CHAIN_CN = ["bing", "yandex", "yahoo", "brave"]
# Type-specific fallback chains (EN and CN separated)
FALLBACK_CHAIN_TYPE_EN = ["brave", "yandex", "yahoo", "bing"]
FALLBACK_CHAIN_TYPE_CN = ["bing", "yandex", "yahoo", "brave"]

DEFAULT_TIMEOUT = 30  # seconds


def is_cjk_query(query, force_lang=None):
    """Detect if query contains CJK characters (Chinese/Japanese/Korean).
    
    Args:
        query: Search query string.
        force_lang: If 'en' or 'cn', override auto-detection.
    """
    if force_lang == "en":
        return False
    if force_lang == "cn":
        return True
    cjk_pattern = re.compile(
        r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u309f\u30a0-\u30ff\uac00-\ud7af]'
    )
    return bool(cjk_pattern.search(query))


def get_fallback_chain(query, typed=False, force_lang=None):
    """Get appropriate fallback chain based on query language.

    CJK queries get bing-first chains, English queries get brave-first chains.
    For typed searches (news/images/videos/books), use type-specific chains.
    
    Args:
        query: Search query string.
        typed: If True, use type-specific fallback chains.
        force_lang: Override auto-detection ('en' or 'cn').
    """
    if is_cjk_query(query, force_lang=force_lang):
        return FALLBACK_CHAIN_TYPE_CN if typed else FALLBACK_CHAIN_CN
    return FALLBACK_CHAIN_TYPE_EN if typed else FALLBACK_CHAIN_EN


class TimeoutError(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutError("Search timed out")


class _DeadlineTimer:
    """Thread-safe deadline timer using threading.Event.

    Works in both main thread and worker threads (unlike signal.SIGALRM).
    Usage:
        timer = _DeadlineTimer(timeout_seconds)
        timer.start()
        # ... do work ...
        timer.check()  # raises TimeoutError if expired
        timer.cancel()
    """
    def __init__(self, timeout_seconds):
        self.timeout = timeout_seconds
        self._event = threading.Event()
        self._thread = None
        self._expired = False

    def start(self):
        if self.timeout and self.timeout > 0:
            self._thread = threading.Thread(target=self._countdown, daemon=True)
            self._thread.start()

    def _countdown(self):
        if not self._event.wait(timeout=self.timeout):
            self._expired = True

    def check(self):
        """Raise TimeoutError if the deadline has passed."""
        if self._expired:
            raise TimeoutError(f"Operation timed out after {self.timeout}s")

    @property
    def expired(self):
        return self._expired

    def cancel(self):
        self._event.set()
        if self._thread:
            self._thread.join(timeout=0.1)


def search_with_retry(query, backend="auto", max_results=5, timelimit=None,
                      region=None, max_retries=3, fallback_backends=None,
                      timeout=None, use_signal=True):
    """Execute search with exponential backoff and optional fallback chain.

    Returns (results, backend_used, elapsed_seconds) or raises on total failure.

    Args:
        use_signal: If True (default), use SIGALRM for timeout in main thread.
                    If False, use thread-safe _DeadlineTimer (for worker threads).
    """
    try:
        from ddgs import DDGS
    except ImportError:
        print("ERROR: ddgs not installed. Run: pip install ddgs", file=sys.stderr)
        sys.exit(1)

    # Determine backends to try
    if fallback_backends:
        backends_to_try = fallback_backends
    elif backend and backend != "auto":
        backends_to_try = [backend]
    else:
        backends_to_try = [None]  # auto

    # Set up timeout: use signal (main thread) or thread-safe timer (workers)
    timer = None
    use_sigalrm = False
    if timeout and timeout > 0:
        if use_signal and threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout)
            use_sigalrm = True
        else:
            timer = _DeadlineTimer(timeout)
            timer.start()

    last_error = None
    start = time.time()

    try:
        for be in backends_to_try:
            for attempt in range(max_retries):
                try:
                    # Check thread-safe timer
                    if timer:
                        timer.check()

                    with DDGS() as d:
                        kwargs = {}
                        if be:
                            kwargs["backend"] = be
                        if timelimit:
                            kwargs["timelimit"] = timelimit
                        if region:
                            kwargs["region"] = region

                        results = list(d.text(query, max_results=max_results, **kwargs))

                        if results:
                            elapsed = time.time() - start
                            return results, be or "auto", elapsed

                    # Empty results: if fallback, try next backend
                    last_error = "empty results"
                    break  # no point retrying same backend with same query

                except TimeoutError:
                    elapsed = time.time() - start
                    last_error = f"timed out after {timeout}s"
                    print(f"  Timeout on backend '{be}' after {timeout}s", file=sys.stderr)
                    break  # try next backend

                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                        wait = (2 ** attempt) + random.uniform(0, 1)
                        print(f"  Retry {attempt+1}/{max_retries} for backend '{be}': {e}. "
                              f"Waiting {wait:.1f}s...", file=sys.stderr)
                        time.sleep(wait)

        elapsed = time.time() - start
        return [], backend, elapsed

    finally:
        if use_sigalrm:
            signal.alarm(0)
        if timer:
            timer.cancel()


def deduplicate_results(all_results):
    """Deduplicate results by URL (href), keeping first occurrence."""
    seen = set()
    unique = []
    for r in all_results:
        url = r.get("href", r.get("url", ""))
        if url and url not in seen:
            seen.add(url)
            unique.append(r)
    return unique


def search_by_type(query, search_type="text", backend="auto", max_results=5,
                   timelimit=None, region=None, max_retries=3,
                   fallback=None, timeout=None, use_signal=True,
                   force_lang=None):
    """Execute a type-specific search (text/news/images/videos/books) with optional fallback chain.

    If fallback=True, automatically tries backends in language-appropriate chain.
    """
    try:
        from ddgs import DDGS
    except ImportError:
        print("ERROR: ddgs not installed. Run: pip install ddgs", file=sys.stderr)
        sys.exit(1)

    # Determine backends to try
    if fallback:
        backends_to_try = get_fallback_chain(query, typed=True, force_lang=force_lang)
    elif backend and backend != "auto":
        backends_to_try = [backend]
    else:
        backends_to_try = [None]  # auto

    method_map = {
        "text": "text",
        "news": "news",
        "images": "images",
        "videos": "videos",
        "books": "books",
    }
    method_name = method_map.get(search_type, "text")

    # Set up timeout: use signal (main thread) or thread-safe timer (workers)
    timer = None
    use_sigalrm = False
    if timeout and timeout > 0:
        if use_signal and threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout)
            use_sigalrm = True
        else:
            timer = _DeadlineTimer(timeout)
            timer.start()

    start = time.time()
    last_error = None

    try:
        for be in backends_to_try:
            for attempt in range(max_retries):
                try:
                    # Check thread-safe timer
                    if timer:
                        timer.check()

                    with DDGS() as d:
                        kwargs = {}
                        if be:
                            kwargs["backend"] = be
                        if timelimit:
                            kwargs["timelimit"] = timelimit
                        if region:
                            kwargs["region"] = region

                        method = getattr(d, method_name)
                        results = list(method(query, max_results=max_results, **kwargs))

                        if results:
                            elapsed = time.time() - start
                            return results, be or "auto", elapsed

                        # Empty results: break to try next backend
                        if fallback:
                            last_error = f"no results on backend '{be}', trying next..."
                            break
                        else:
                            last_error = f"no results on backend '{be}'"
                            break  # no point retrying same backend with same query

                except TimeoutError:
                    last_error = f"timed out after {timeout}s"
                    print(f"  Timeout on {search_type}/{be} after {timeout}s", file=sys.stderr)
                    break

                except Exception as e:
                    last_error = e
                    if attempt < max_retries - 1:
                        wait = (2 ** attempt) + random.uniform(0, 1)
                        print(f"  Retry {attempt+1}/{max_retries} for {search_type}/{be}: {e}. "
                              f"Waiting {wait:.1f}s...", file=sys.stderr)
                        time.sleep(wait)
                    else:
                        # Last retry failed, try next backend
                        if fallback and be != backends_to_try[-1]:
                            print(f"  Backend '{be}' failed after {max_retries} retries, "
                                  f"falling to next...", file=sys.stderr)
                            break

        elapsed = time.time() - start
        raise Exception(f"All backends exhausted for {search_type} type: {last_error}")

    finally:
        if use_sigalrm:
            signal.alarm(0)
        if timer:
            timer.cancel()


def search_all_types(query, backend="auto", max_results=3, timelimit=None,
                     region=None, max_retries=2, fallback=None,
                     include_images=False, timeout=None, force_lang=None):
    """Search across text, news, and videos types at once. Returns dict keyed by type."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    types = ["text", "news", "videos"]
    if include_images:
        types.append("images")
    results_by_type = {}
    errors = []

    def search_one(st):
        try:
            r, be, el = search_by_type(
                query, search_type=st, backend=backend,
                max_results=max_results, timelimit=timelimit,
                region=region, max_retries=max_retries, fallback=fallback,
                timeout=timeout, use_signal=False,  # thread-safe: no SIGALRM in workers
                force_lang=force_lang
            )
            return st, r, be, el, None
        except Exception as e:
            return st, [], "N/A", 0.0, str(e)

    # Run all type searches in parallel
    start = time.time()
    with ThreadPoolExecutor(max_workers=len(types)) as pool:
        futures = {pool.submit(search_one, t): t for t in types}
        for future in as_completed(futures):
            t, r, be, el, err = future.result()
            results_by_type[t] = {"results": r, "backend": be, "elapsed": el}
            if err:
                errors.append(f"  [{t}] {err}")

    total_elapsed = time.time() - start
    return results_by_type, total_elapsed, errors


def extract_from_url(url, fmt="text_markdown", max_retries=2, timeout=None, use_signal=True):
    """Extract full text from a URL using DDGS extract()."""
    try:
        from ddgs import DDGS
    except ImportError:
        print("ERROR: ddgs not installed. Run: pip install ddgs", file=sys.stderr)
        sys.exit(1)

    timer = None
    use_sigalrm = False
    if timeout and timeout > 0:
        if use_signal and threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(timeout)
            use_sigalrm = True
        else:
            timer = _DeadlineTimer(timeout)
            timer.start()

    start = time.time()
    last_error = None

    try:
        for attempt in range(max_retries):
            try:
                if timer:
                    timer.check()

                with DDGS() as d:
                    result = d.extract(url, fmt=fmt)
                    elapsed = time.time() - start
                    return result, elapsed

            except TimeoutError:
                raise TimeoutError(f"Extract timed out after {timeout}s")

            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    print(f"  Extract retry {attempt+1}/{max_retries}: {e}. "
                          f"Waiting {wait:.1f}s...", file=sys.stderr)
                    time.sleep(wait)

        raise last_error

    finally:
        if use_sigalrm:
            signal.alarm(0)
        if timer:
            timer.cancel()


def search_single(query, backend="auto", max_results=5, timelimit=None,
                  region=None, max_retries=3, fallback=False, output=None,
                  search_type="text", extract=False, extract_length=2000,
                  timeout=None, force_lang=None):
    """Execute a single search query, with type and extract support."""
    start_time = time.time()

    # Multi-type search (text + news + videos + optional images)
    if search_type == "all" or search_type == "all+":
        return _search_multi_type(query, backend, max_results, timelimit,
                                  region, max_retries, fallback, output,
                                  include_images=(search_type == "all+"),
                                  timeout=timeout, force_lang=force_lang)

    # Type-specific search (news/images/videos/books)
    if search_type != "text":
        try:
            results, used_backend, elapsed = search_by_type(
                query, search_type=search_type, backend=backend,
                max_results=max_results, timelimit=timelimit,
                region=region, max_retries=max_retries, fallback=fallback,
                timeout=timeout, force_lang=force_lang
            )
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"ERROR: {search_type} search failed: {e}", file=sys.stderr)
            results, used_backend, elapsed = [], "N/A", elapsed

            if output == "json":
                out = {
                    "query": query,
                    "type": search_type,
                    "backend": used_backend,
                    "results_count": 0,
                    "elapsed_seconds": round(elapsed, 2),
                    "error": str(e),
                    "results": [],
                }
                print(json.dumps(out, ensure_ascii=False, indent=2))
            else:
                print(f"Query: {query}")
                print(f"Type: {search_type} | Backend: {used_backend} | Results: 0 | "
                      f"Time: {elapsed:.1f}s (failed)")
                print("-" * 60)
                print(f"  ERROR: {e}")

            return results

        if output == "json":
            out = {
                "query": query,
                "type": search_type,
                "backend": used_backend,
                "results_count": len(results),
                "elapsed_seconds": round(elapsed, 2),
                "results": results,
            }
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print(f"Query: {query}")
            print(f"Type: {search_type} | Backend: {used_backend} | "
                  f"Results: {len(results)} | Time: {elapsed:.1f}s")
            print("-" * 60)
            for i, r in enumerate(results, 1):
                title = r.get("title", r.get("name", ""))
                url_val = r.get("href", r.get("url", r.get("image", "")))
                print(f"\n{i}. {title}")
                print(f"   {url_val}")
                if search_type == "videos":
                    dur = r.get("duration", "")
                    prov = r.get("provider", "")
                    pub = r.get("published", "")
                    if dur:
                        print(f"   Duration: {dur}")
                    if prov:
                        print(f"   Provider: {prov}")
                    if pub:
                        print(f"   Published: {pub}")
                    body = r.get("content", r.get("description", ""))
                elif search_type == "books":
                    author = r.get("author", "")
                    pub_info = r.get("publisher", "")
                    body = r.get("info", "")
                    if author:
                        print(f"   Author: {author}")
                    if pub_info:
                        print(f"   Publisher: {pub_info}")
                elif search_type == "news":
                    src = r.get("source", "")
                    date = r.get("date", "")
                    if date:
                        print(f"   Date: {date}")
                    if src:
                        print(f"   Source: {src}")
                    body = r.get("body", "")
                else:
                    body = r.get("body", r.get("content", ""))

                if body:
                    print(f"   {body[:200]}...")

        return results

    # Standard text search with fallback support
    fallback_backends = None
    if fallback:
        fallback_backends = get_fallback_chain(query, typed=False, force_lang=force_lang)

    results, used_backend, elapsed = search_with_retry(
        query, backend=backend, max_results=max_results,
        timelimit=timelimit, region=region,
        max_retries=max_retries, fallback_backends=fallback_backends,
        timeout=timeout
    )

    if output == "json":
        out = {
            "query": query,
            "backend": used_backend,
            "results_count": len(results),
            "elapsed_seconds": round(elapsed, 2),
            "results": results,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Query: {query}")
        print(f"Backend: {used_backend} | Results: {len(results)} | Time: {elapsed:.1f}s")
        print("-" * 60)
        for i, r in enumerate(results, 1):
            title = r.get("title", "")
            href = r.get("href", r.get("url", ""))
            body = r.get("body", r.get("content", ""))[:150]
            print(f"\n{i}. {title}")
            print(f"   {href}")
            if body:
                print(f"   {body}...")

    # Optional: extract full text from first result
    if extract and results:
        first_url = results[0].get("href", results[0].get("url", ""))
        if first_url:
            try:
                print(f"\n{'='*60}")
                print(f"Extracting content from: {first_url}")
                print(f"{'='*60}")
                content, ext_elapsed = extract_from_url(
                    first_url, max_retries=2, timeout=timeout
                )
                extracted = content.get("content", "")
                if extracted:
                    display = extracted[:extract_length]
                    if len(extracted) > extract_length:
                        display += "..."
                    print(f"\n{display}")
                    print(f"\n--- Extract time: {ext_elapsed:.2f}s ---")
            except Exception as e:
                print(f"Extract failed: {e}", file=sys.stderr)

    return results


def _search_multi_type(query, backend, max_results, timelimit,
                       region, max_retries, fallback, output,
                       include_images=False, timeout=None, force_lang=None):
    """Handle --type all / all+ search: text + news + videos (+ optional images) in parallel."""
    results_by_type, total_elapsed, errors = search_all_types(
        query, backend=backend, max_results=max_results,
        timelimit=timelimit, region=region,
        max_retries=max_retries, fallback=fallback,
        include_images=include_images, timeout=timeout,
        force_lang=force_lang
    )

    type_label = "ALL (text + news + videos + images)" if include_images else "ALL (text + news + videos)"

    if output == "json":
        out = {
            "query": query,
            "type": "all" + ("+" if include_images else ""),
            "total_elapsed_seconds": round(total_elapsed, 2),
            "types": {},
        }
        for t, data in results_by_type.items():
            out["types"][t] = {
                "backend": data["backend"],
                "results_count": len(data["results"]),
                "elapsed_seconds": round(data["elapsed"], 2),
                "results": data["results"],
            }
        if errors:
            out["errors"] = errors
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"Query: {query}")
        print(f"Type: {type_label} | Total: {total_elapsed:.1f}s")
        print("=" * 60)

        display_types = ["text", "news", "videos"]
        if include_images:
            display_types.append("images")

        for t in display_types:
            data = results_by_type.get(t, {"results": [], "backend": "N/A", "elapsed": 0.0})
            res = data["results"]
            be = data["backend"]
            el = data["elapsed"]
            print(f"\n--- [{t.upper()}] {be} | {len(res)} results | {el:.1f}s ---")
            for i, r in enumerate(res[:max_results], 1):
                if t == "images":
                    title = r.get("title", "")
                    img_url = r.get("image", r.get("url", ""))
                    thumb = r.get("thumbnail", "")
                    print(f"  {i}. {title}")
                    print(f"     URL: {img_url}")
                    if thumb:
                        print(f"     Thumbnail: {thumb}")
                else:
                    title = r.get("title", r.get("name", ""))
                    url_val = r.get("href", r.get("url", ""))
                    print(f"  {i}. {title}")
                    print(f"     {url_val}")

        if errors:
            print(f"\nErrors ({len(errors)}):")
            for e in errors:
                print(f"  ⚠ {e}")

    return results_by_type


def search_batch(batch_file, backend="auto", max_results=5, timelimit=None,
                 region=None, max_retries=3, fallback=False, output=None,
                 timeout=None, force_lang=None):
    """Execute batch search from a file (one query per line)."""
    try:
        with open(batch_file, "r", encoding="utf-8") as f:
            queries = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"ERROR: Batch file not found: {batch_file}", file=sys.stderr)
        sys.exit(1)

    if not queries:
        print("ERROR: No queries found in batch file", file=sys.stderr)
        sys.exit(1)

    # Rotate backends to distribute load
    backends = FALLBACK_CHAIN_EN if backend == "auto" else [backend]
    all_batch_results = []
    start = time.time()

    for i, query in enumerate(queries):
        # Auto-select backend based on query language
        if backend == "auto":
            chain = get_fallback_chain(query, typed=False, force_lang=force_lang)
            be = chain[i % len(chain)]
        else:
            be = backend

        print(f"\n[{i+1}/{len(queries)}] Searching: {query} (backend: {be})",
              file=sys.stderr)

        fallback_backends = get_fallback_chain(query, typed=False, force_lang=force_lang) if fallback else None

        results, used_be, elapsed = search_with_retry(
            query, backend=be, max_results=max_results,
            timelimit=timelimit, region=region,
            max_retries=max_retries,
            fallback_backends=fallback_backends,
            timeout=timeout
        )

        all_batch_results.append({
            "query": query,
            "backend": used_be,
            "results_count": len(results),
            "results": results,
        })

        # Polite delay between queries
        if i < len(queries) - 1:
            delay = random.uniform(1.0, 2.5)
            time.sleep(delay)

    total_elapsed = time.time() - start

    if output == "json":
        out = {
            "batch_size": len(queries),
            "total_elapsed_seconds": round(total_elapsed, 2),
            "batch": all_batch_results,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Batch complete: {len(queries)} queries in {total_elapsed:.1f}s")
        for item in all_batch_results:
            print(f"  - {item['query']}: {item['results_count']} results ({item['backend']})")

    return all_batch_results


def main():
    parser = argparse.ArgumentParser(
        description=f"DDGS Smart Search v{VERSION} - with auto-lang, timeout, type support, extract, fallback, batch"
    )
    parser.add_argument("-q", "--query", help="Search query (single search)")
    parser.add_argument("--batch-file", help="File with queries (one per line)")
    parser.add_argument("-b", "--backend", default="auto",
                        choices=["auto", "all", "bing", "brave", "duckduckgo",
                                 "google", "yandex", "yahoo", "wikipedia"],
                        help="Search backend (default: auto)")
    parser.add_argument("-m", "--max-results", type=int, default=5,
                        help="Max results per query (default: 5)")
    parser.add_argument("-t", "--timelimit", choices=["d", "w", "m", "y"],
                        help="Time limit: day/week/month/year")
    parser.add_argument("-r", "--region", help="Region (e.g., us-en, zh-cn)")
    parser.add_argument("-o", "--output", choices=["json"], help="Output format")
    parser.add_argument("--retries", type=int, default=3,
                        help="Max retries per backend (default: 3)")
    parser.add_argument("--fallback", action="store_true",
                        help="Auto fallback through backend chain on failure")
    parser.add_argument("--version", action="store_true",
                        help="Show version and exit")
    parser.add_argument("--type", dest="search_type", default="text",
                        choices=["text", "news", "images", "videos", "books",
                                 "all", "all+"],
                        help="Search type (default: text, 'all' for text+news+videos, "
                             "'all+' for text+news+videos+images)")
    parser.add_argument("--extract", action="store_true",
                        help="Extract full text from the first result URL")
    parser.add_argument("--extract-url",
                        help="Direct URL to extract text from (no search)")
    parser.add_argument("--extract-length", type=int, default=2000,
                        help="Max chars to display from extract (default: 2000)")
    parser.add_argument("--timeout", type=int, default=0,
                        help="Global timeout in seconds (default: 0 = no timeout)")
    parser.add_argument("--lang", choices=["en", "cn"],
                        help="Force language for backend selection (en=brave-first, cn=bing-first). "
                             "Overrides auto-detection.")
    parser.add_argument("--quiet", action="store_true",
                        help="Quiet mode: suppress headers/stats, only output results")
    parser.add_argument("--urls-only", action="store_true",
                        help="Only output result URLs (one per line, for piping)")
    args = parser.parse_args()

    # Show version and exit
    if args.version:
        print(f"ddgs_search.py v{VERSION}")
        return

    # --quiet suppresses stderr (retry/timeout messages)
    if args.quiet:
        import os
        sys.stderr = open(os.devnull, 'w')

    timeout = args.timeout if args.timeout > 0 else None

    # Direct URL extraction (no search needed)
    if args.extract_url:
        try:
            content, elapsed = extract_from_url(
                args.extract_url, max_retries=2, timeout=timeout
            )
            extracted = content.get("content", "")
            if args.output == "json":
                print(json.dumps({
                    "url": args.extract_url,
                    "elapsed_seconds": round(elapsed, 2),
                    "content": extracted,
                }, ensure_ascii=False, indent=2))
            else:
                print(f"URL: {args.extract_url}")
                print(f"Time: {elapsed:.2f}s")
                print("=" * 60)
                display = extracted[:args.extract_length]
                if len(extracted) > args.extract_length:
                    display += "..."
                print(display)
        except Exception as e:
            print(f"ERROR: Extract failed: {e}", file=sys.stderr)
        return

    if not args.query and not args.batch_file:
        parser.error("Either --query or --batch-file is required")

    force_lang = args.lang

    # --urls-only: suppress normal output, only print URLs at the end
    import io
    if args.urls_only:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()  # capture and discard normal output

    try:
        if args.batch_file:
            results = search_batch(args.batch_file, backend=args.backend,
                         max_results=args.max_results, timelimit=args.timelimit,
                         region=args.region, max_retries=args.retries,
                         fallback=args.fallback, output=args.output,
                         timeout=timeout, force_lang=force_lang)
        else:
            results = search_single(args.query, backend=args.backend,
                          max_results=args.max_results, timelimit=args.timelimit,
                          region=args.region, max_retries=args.retries,
                          fallback=args.fallback, output=args.output,
                          search_type=args.search_type, extract=args.extract,
                          extract_length=args.extract_length,
                          timeout=timeout, force_lang=force_lang)
    finally:
        if args.urls_only:
            sys.stdout = old_stdout

    if args.urls_only:
        urls = []
        if isinstance(results, dict):
            for t, data in results.items():
                for r in data.get("results", []):
                    url = r.get("href", r.get("url", r.get("image", "")))
                    if url:
                        urls.append(url)
        elif isinstance(results, list):
            if results and isinstance(results[0], dict) and "results" in results[0]:
                # batch results
                for item in results:
                    for r in item.get("results", []):
                        url = r.get("href", r.get("url", ""))
                        if url:
                            urls.append(url)
            else:
                for r in results:
                    url = r.get("href", r.get("url", ""))
                    if url:
                        urls.append(url)
        for url in urls:
            print(url)


if __name__ == "__main__":
    main()
