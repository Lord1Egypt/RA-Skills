#!/usr/bin/env python3
import argparse
import json
import os
import ssl
import sys
import urllib.error
import urllib.request

TAVILY_URL = "https://api.tavily.com/search"
MAX_RESPONSE_BYTES = 2 * 1024 * 1024
USER_AGENT = "tavily-search-agent-skill/0.2.1"


class TavilySearchError(RuntimeError):
    pass


def configure_utf8_stream(stream):
    reconfigure = getattr(stream, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8", errors="replace")


def configure_console_encoding():
    configure_utf8_stream(sys.stdout)
    configure_utf8_stream(sys.stderr)


def load_key():
    key = os.environ.get("TAVILY_API_KEY")
    return key.strip() if key and key.strip() else None


def _read_bounded(response):
    body = response.read(MAX_RESPONSE_BYTES + 1)
    if len(body) > MAX_RESPONSE_BYTES:
        raise TavilySearchError(
            f"Tavily response exceeded the {MAX_RESPONSE_BYTES}-byte safety limit"
        )
    return body.decode("utf-8", errors="replace")


def _http_error_message(error):
    if error.code == 401:
        return "Tavily authentication failed; check TAVILY_API_KEY"
    if error.code == 429:
        return "Tavily rate limit or credit quota exceeded"

    detail = ""
    try:
        body = error.read(4096).decode("utf-8", errors="replace")
        parsed = json.loads(body)
        if isinstance(parsed, dict):
            candidate = (
                parsed.get("detail") or parsed.get("message") or parsed.get("error")
            )
            if isinstance(candidate, str):
                detail = candidate.strip()
    except (OSError, ValueError, TypeError):
        pass

    suffix = f": {detail[:300]}" if detail else ""
    return f"Tavily returned HTTP {error.code}{suffix}"


def _is_certificate_error(error):
    reason = getattr(error, "reason", None)
    return isinstance(error, ssl.SSLCertVerificationError) or isinstance(
        reason, ssl.SSLCertVerificationError
    )


def _certifi_context():
    try:
        import certifi
    except (ImportError, OSError):
        return None
    return ssl.create_default_context(cafile=certifi.where())


def _request_json(request, timeout):
    def attempt(context):
        try:
            with urllib.request.urlopen(
                request, timeout=timeout, context=context
            ) as response:
                body = _read_bounded(response)
        except urllib.error.HTTPError as error:
            raise TavilySearchError(_http_error_message(error)) from error
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError as error:
            raise TavilySearchError(
                f"Tavily returned invalid JSON: {body[:300]}"
            ) from error
        if not isinstance(parsed, dict):
            raise TavilySearchError("Tavily returned an unexpected JSON response")
        return parsed

    try:
        return attempt(ssl.create_default_context())
    except urllib.error.URLError as error:
        if _is_certificate_error(error) and not os.environ.get("SSL_CERT_FILE"):
            context = _certifi_context()
            if context is not None:
                try:
                    return attempt(context)
                except urllib.error.URLError as retry_error:
                    error = retry_error

        if _is_certificate_error(error):
            raise TavilySearchError(
                "TLS certificate verification failed. Update the local CA store or set "
                "SSL_CERT_FILE to a trusted CA bundle; certificate verification was not disabled."
            ) from error
        raise TavilySearchError(f"Unable to reach Tavily: {error.reason}") from error


def _clean_domains(domains, limit):
    cleaned = []
    for domain in domains or []:
        value = domain.strip().lower()
        if value and value not in cleaned:
            cleaned.append(value)
    if len(cleaned) > limit:
        raise TavilySearchError(f"Too many domains: maximum is {limit}")
    return cleaned


def tavily_search(
    query,
    max_results,
    include_answer,
    search_depth,
    topic="general",
    time_range=None,
    include_domains=None,
    exclude_domains=None,
    country=None,
    timeout=30,
):
    query = query.strip()
    if not query:
        raise TavilySearchError("Search query must not be empty")
    if country and topic != "general":
        raise TavilySearchError(
            "Country boosting is available only for the general topic"
        )

    key = load_key()
    if not key:
        raise TavilySearchError("Missing TAVILY_API_KEY environment variable")

    payload = {
        "query": query,
        "max_results": max_results,
        "search_depth": search_depth,
        "topic": topic,
        "include_answer": bool(include_answer),
        "include_images": False,
        "include_raw_content": False,
    }
    if time_range:
        payload["time_range"] = time_range
    included = _clean_domains(include_domains, 300)
    excluded = _clean_domains(exclude_domains, 150)
    if included:
        payload["include_domains"] = included
    if excluded:
        payload["exclude_domains"] = excluded
    if country:
        payload["country"] = country

    request = urllib.request.Request(
        TAVILY_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )
    response = _request_json(request, timeout)

    output = {"query": query, "answer": response.get("answer"), "results": []}
    for result in (response.get("results") or [])[:max_results]:
        if not isinstance(result, dict):
            continue
        item = {
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content"),
        }
        if isinstance(result.get("score"), (int, float)):
            item["score"] = result["score"]
        output["results"].append(item)

    if not include_answer:
        output.pop("answer", None)
    return output


def to_brave_like(obj):
    results = []
    for result in obj.get("results", []) or []:
        item = {
            "title": result.get("title"),
            "url": result.get("url"),
            "snippet": result.get("content"),
        }
        if "score" in result:
            item["score"] = result["score"]
        results.append(item)
    output = {"query": obj.get("query"), "results": results}
    if "answer" in obj:
        output["answer"] = obj.get("answer")
    return output


def to_markdown(obj):
    lines = []
    if obj.get("answer"):
        lines.extend([obj["answer"].strip(), ""])
    for index, result in enumerate(obj.get("results", []) or [], 1):
        title = (result.get("title") or "").strip() or result.get("url") or "(no title)"
        url = result.get("url") or ""
        snippet = (result.get("content") or "").strip()
        lines.append(f"{index}. {title}")
        if url:
            lines.append(f"   {url}")
        if snippet:
            lines.append(f"   - {snippet}")
    return "\n".join(lines).strip() + "\n"


def build_parser():
    parser = argparse.ArgumentParser(description="Search the public web with Tavily")
    parser.add_argument("--query", required=True)
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--include-answer", action="store_true")
    parser.add_argument(
        "--search-depth",
        default="basic",
        choices=["basic", "advanced", "fast", "ultra-fast"],
    )
    parser.add_argument(
        "--topic", default="general", choices=["general", "news", "finance"]
    )
    parser.add_argument("--time-range", choices=["day", "week", "month", "year"])
    parser.add_argument("--include-domain", action="append", default=[])
    parser.add_argument("--exclude-domain", action="append", default=[])
    parser.add_argument("--country")
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--format", default="raw", choices=["raw", "brave", "md"])
    return parser


def main(argv=None):
    configure_console_encoding()
    args = build_parser().parse_args(argv)
    try:
        result = tavily_search(
            query=args.query,
            max_results=max(1, min(args.max_results, 20)),
            include_answer=args.include_answer,
            search_depth=args.search_depth,
            topic=args.topic,
            time_range=args.time_range,
            include_domains=args.include_domain,
            exclude_domains=args.exclude_domain,
            country=args.country,
            timeout=max(1, min(args.timeout, 120)),
        )
    except TavilySearchError as error:
        print(f"tavily-search: {error}", file=sys.stderr)
        return 1

    if args.format == "md":
        sys.stdout.write(to_markdown(result))
        return 0
    if args.format == "brave":
        result = to_brave_like(result)
    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
