#!/usr/bin/env python3
"""
Perplexica Search Skill
AI-powered search using local Perplexica instance.
Local-only: only localhost/127.0.0.1/::1/host.docker.internal; no redirects; no exfiltration.
Resolved IPs are validated (loopback or private only) to mitigate DNS/hosts tampering.
"""

import argparse
import json
import os
import socket
import sys
import time
from urllib.parse import urlparse
from urllib.request import (
    Request,
    build_opener,
    HTTPHandler,
    HTTPSHandler,
)
from urllib.error import URLError, HTTPError

REDIRECT_CODES = (301, 302, 303, 307, 308)


def _reject_redirect(response):
    """Raise if response is a redirect (local-only skill must not follow redirects to remote hosts)."""
    if getattr(response, "code", None) in REDIRECT_CODES:
        raise URLError(
            "HTTP redirects are not allowed (local-only skill). "
            "Rejecting redirect to prevent contact with non-local hosts."
        )


class NoRedirectHTTPHandler(HTTPHandler):
    """Reject redirects for http:// so the client never contacts a non-local host."""

    def http_response(self, request, response):
        _reject_redirect(response)
        return response


class NoRedirectHTTPSHandler(HTTPSHandler):
    """Reject redirects for https:// so the client never contacts a non-local host."""

    def https_response(self, request, response):
        _reject_redirect(response)
        return response


# Opener that does not follow redirects. Used explicitly (no install_opener) so we don't
# modify global urllib state if this module were ever imported in a shared process.
_http_opener = build_opener(NoRedirectHTTPHandler, NoRedirectHTTPSHandler)

# Hostnames that are considered local (no exfiltration).
# host.docker.internal = host machine when script runs inside Docker (Mac/Windows).
LOCAL_HOSTS = frozenset({"localhost", "127.0.0.1", "::1", "host.docker.internal"})


def _is_loopback_or_private_ip(ip_str):
    """Return True if the IP is loopback (127.x, ::1) or private (RFC 1918)."""
    if not ip_str:
        return False
    try:
        addr = ip_str.strip()
        if addr == "::1":
            return True
        if addr.startswith("127."):
            return True
        parts = addr.split(".")
        if len(parts) != 4:
            return False
        a, b, c, d = (int(p) for p in parts)
        if a == 10:
            return True
        if a == 172 and 16 <= b <= 31:
            return True
        if a == 192 and b == 168:
            return True
        return False
    except (ValueError, IndexError):
        return False


def validate_resolved_host(host):
    """
    Ensure the host resolves only to loopback or private IPs (mitigate DNS/hosts tampering).
    Raises URLError if the host is not in LOCAL_HOSTS or resolves to a non-local IP.
    """
    if not host or host.lower() not in LOCAL_HOSTS:
        return
    if host == "127.0.0.1" or host == "::1":
        return
    try:
        # Resolve to all addresses; require every one to be loopback or private.
        infos = socket.getaddrinfo(host, None, socket.AF_UNSPEC, socket.SOCK_STREAM)
        for (_fam, _typ, _proto, _name, sockaddr) in infos:
            ip = sockaddr[0] if isinstance(sockaddr, (list, tuple)) else sockaddr
            if not _is_loopback_or_private_ip(ip):
                raise URLError(
                    f"Host '{host}' resolved to non-local IP {ip}. "
                    "Only loopback (127.x, ::1) or private IPs are allowed. "
                    "Check /etc/hosts and DNS for tampering."
                )
    except socket.gaierror as e:
        raise URLError(f"Could not resolve host '{host}': {e}") from e

# Timeouts (seconds): providers can be slow on first load.
# For search we use streaming (like the Perplexica web UI) so chunks arrive over time;
# chunk_timeout is max seconds to wait between consecutive chunks.
DEFAULT_PROVIDERS_TIMEOUT = 30
DEFAULT_CHUNK_TIMEOUT = 180  # 3 min between chunks (slow LLM); no total limit when streaming


def is_local_url(url_str):
    """Return True only if the URL points to a local host (localhost, 127.0.0.1, ::1, host.docker.internal)."""
    try:
        parsed = urlparse(url_str)
        host = (parsed.hostname or "").strip().lower()
        return host in LOCAL_HOSTS
    except Exception:
        return False


def load_skill_config():
    """Load config.json from skill directory (parent of script dir). Returns dict or None. Only local perplexica_url allowed."""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        skill_dir = os.path.dirname(script_dir)
        config_path = os.path.join(skill_dir, "config.json")
        if not os.path.isfile(config_path):
            return None
        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)
        url = config.get("perplexica_url")
        if url and not is_local_url(url):
            print("❌ config.json perplexica_url must be a local URL (localhost, 127.0.0.1, ::1, or host.docker.internal). No remote URLs.", file=sys.stderr)
            sys.exit(1)
        return config
    except (OSError, json.JSONDecodeError):
        return None


def normalize_base_url(url):
    """Strip trailing slash so we can safely append paths."""
    return url.rstrip("/") if url else url


def fetch_providers(base_url, timeout=DEFAULT_PROVIDERS_TIMEOUT):
    """Fetch available providers and models from Perplexica"""
    base_url = normalize_base_url(base_url)
    try:
        req = Request(f"{base_url}/api/providers")
        req.add_header("Content-Type", "application/json")
        with _http_opener.open(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            return data.get("providers", [])
    except Exception as e:
        print(f"❌ Error fetching providers: {e}", file=sys.stderr)
        print(f"   Make sure Perplexica is running at {base_url}", file=sys.stderr)
        sys.exit(1)


def select_model(providers, model_type="chatModels", preferred=None):
    """Select a model from available providers"""
    for provider in providers:
        models = provider.get(model_type, [])
        if preferred:
            for model in models:
                if preferred.lower() in model.get("key", "").lower():
                    return provider["id"], model["key"]
        if models:
            return provider["id"], models[0]["key"]
    return None, None


def search_streaming(query, base_url, chat_provider_id, chat_model_key,
                     embed_provider_id, embed_model_key, mode="balanced",
                     sources=None, instructions=None, history=None,
                     chunk_timeout=DEFAULT_CHUNK_TIMEOUT):
    """
    Execute search via Perplexica API using streaming (SSE).
    Same as the web UI: server sends chunks so we don't wait for the full response
    and avoid timeouts on long-running quality/deep research.
    """
    base_url = normalize_base_url(base_url)
    if sources is None:
        sources = ["web"]

    payload = {
        "chatModel": {"providerId": chat_provider_id, "key": chat_model_key},
        "embeddingModel": {"providerId": embed_provider_id, "key": embed_model_key},
        "optimizationMode": mode,
        "sources": sources,
        "query": query,
        "stream": True,
    }
    if instructions:
        payload["systemInstructions"] = instructions
    if history:
        payload["history"] = history

    start_time = time.time()
    req = Request(
        f"{base_url}/api/search",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with _http_opener.open(req, timeout=chunk_timeout) as response:
            content_type = response.headers.get_content_type() or ""
            if "text/event-stream" not in content_type:
                # Non-streaming response (e.g. error)
                body = response.read().decode()
                result = json.loads(body)
                result["took_ms"] = int((time.time() - start_time) * 1000)
                result["model_used"] = chat_model_key
                return result

            message_parts = []
            sources_list = []
            buffer = b""

            def process_line(line_str):
                nonlocal sources_list
                if line_str.startswith("data:"):
                    line_str = line_str[5:].strip()
                if not line_str:
                    return None
                try:
                    obj = json.loads(line_str)
                except json.JSONDecodeError:
                    return None
                msg_type = obj.get("type")
                data = obj.get("data")
                if msg_type == "response" and isinstance(data, str):
                    message_parts.append(data)
                elif msg_type == "sources" and isinstance(data, list):
                    sources_list = data
                elif msg_type == "done":
                    return "done"
                elif msg_type == "error":
                    print(f"❌ Search error from server: {data}", file=sys.stderr)
                    sys.exit(1)
                return None

            while True:
                try:
                    chunk = response.read(8192)
                except Exception as read_err:
                    if "timed out" in str(read_err).lower() or "timeout" in str(read_err).lower():
                        print(f"❌ Timeout: no data for {chunk_timeout}s. Increase --timeout.", file=sys.stderr)
                    else:
                        print(f"❌ Read error: {read_err}", file=sys.stderr)
                    sys.exit(1)
                if not chunk:
                    break
                buffer += chunk
                while b"\n" in buffer:
                    line, _, buffer = buffer.partition(b"\n")
                    line_str = line.decode("utf-8", errors="replace").strip()
                    if process_line(line_str) == "done":
                        took_ms = int((time.time() - start_time) * 1000)
                        return {
                            "message": "".join(message_parts),
                            "sources": sources_list,
                            "took_ms": took_ms,
                            "model_used": chat_model_key,
                        }
            if buffer.strip():
                line_str = buffer.decode("utf-8", errors="replace").strip()
                if process_line(line_str) == "done":
                    took_ms = int((time.time() - start_time) * 1000)
                    return {
                        "message": "".join(message_parts),
                        "sources": sources_list,
                        "took_ms": took_ms,
                        "model_used": chat_model_key,
                    }

            took_ms = int((time.time() - start_time) * 1000)
            return {
                "message": "".join(message_parts),
                "sources": sources_list,
                "took_ms": took_ms,
                "model_used": chat_model_key,
            }
    except HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        try:
            error_body = json.loads(e.read().decode())
            print(f"   Details: {error_body}", file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except URLError as e:
        err = str(e.reason) if e.reason else str(e)
        print(f"❌ Connection Error: {err}", file=sys.stderr)
        print(f"   Make sure Perplexica is running at {base_url}", file=sys.stderr)
        if "localhost" in base_url:
            print("   Try --url http://127.0.0.1:3000 if the agent runs in a different network context.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        err = str(e)
        if "timed out" in err.lower() or "timeout" in err.lower():
            print(f"❌ Timeout: {err}", file=sys.stderr)
            print(f"   Use --timeout N (seconds to wait between chunks, e.g. 300).", file=sys.stderr)
        else:
            print(f"❌ Search failed: {err}", file=sys.stderr)
        sys.exit(1)


def format_output(result, query, mode, sources, json_output=False, quiet=False):
    """Format search results for display. If quiet, output only answer + compact sources (no headers)."""
    
    if json_output:
        print(json.dumps(result, indent=2))
        return
    
    answer = result.get("message", result.get("answer", "No answer generated"))
    sources_list = result.get("sources", [])
    took_ms = result.get("took_ms", 0)
    model_used = result.get("model_used", "unknown")
    
    if quiet:
        print(answer)
        if sources_list:
            print("\nSources:")
            for i, source in enumerate(sources_list, 1):
                metadata = source.get("metadata", {})
                title = metadata.get("title", "Untitled")
                url = metadata.get("url", "No URL")
                print(f"[{i}] {title} {url}")
        return
    
    print(f"\n🔍 Query: {query}")
    print(f"⚡ Mode: {mode} | Sources: {', '.join(sources)}")
    print(f"🤖 Model: {model_used} | Time: {took_ms}ms\n")
    print("📄 Answer:")
    print("─" * 60)
    print(answer)
    print("─" * 60)
    
    if sources_list:
        print(f"\n📚 Sources ({len(sources_list)}):")
        for i, source in enumerate(sources_list, 1):
            metadata = source.get("metadata", {})
            title = metadata.get("title", "Untitled")
            url = metadata.get("url", "No URL")
            print(f"[{i}] {title}")
            print(f"    {url}\n")
    else:
        print("\n⚠️  No sources cited")
    
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Perplexica AI-powered search",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "What is quantum computing?"
  %(prog)s "Latest AI developments" --mode quality
  %(prog)s "ML papers" --sources academic
  %(prog)s "Python tips" --json
        """
    )
    
    parser.add_argument("query", help="Search query")
    parser.add_argument("-u", "--url", default="http://localhost:3000",
                        help="Local Perplexica base URL only (default: http://localhost:3000). Allowed: localhost, 127.0.0.1, ::1, host.docker.internal.")
    parser.add_argument("-m", "--mode", choices=["speed", "balanced", "quality"],
                        default="balanced", help="Optimization mode")
    parser.add_argument("-s", "--sources", default="web",
                        help="Search sources: web,academic,discussions (comma-separated)")
    parser.add_argument("--chat-model", help="Chat model key (e.g., gpt-4o-mini)")
    parser.add_argument("--embedding-model", help="Embedding model key")
    parser.add_argument("-i", "--instructions", help="Custom system instructions")
    parser.add_argument("--history", help="Conversation history as JSON array")
    parser.add_argument("-j", "--json", action="store_true", help="Output raw JSON")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Minimal output: answer and sources only (no headers). Use from agents/OpenClaw to reduce clutter.")
    parser.add_argument("--timeout", type=int, default=DEFAULT_CHUNK_TIMEOUT,
                        help=f"Seconds to wait between stream chunks (default: {DEFAULT_CHUNK_TIMEOUT}). Increase if the LLM is slow.")
    
    args = parser.parse_args()
    
    config = load_skill_config()
    base_url = args.url
    if config and config.get("perplexica_url") and args.url == "http://localhost:3000":
        base_url = config["perplexica_url"]
    if not is_local_url(base_url):
        print("❌ Only local Perplexica URLs are allowed (localhost, 127.0.0.1, ::1, or host.docker.internal). No remote URLs.", file=sys.stderr)
        sys.exit(1)
    
    base_url = normalize_base_url(base_url)
    try:
        parsed = urlparse(base_url)
        validate_resolved_host((parsed.hostname or "").strip())
    except URLError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    
    # Parse sources
    sources = [s.strip() for s in args.sources.split(",")]
    valid_sources = {"web", "academic", "discussions"}
    sources = [s for s in sources if s in valid_sources]
    if not sources:
        sources = ["web"]
    
    # Parse history
    history = None
    if args.history:
        try:
            history = json.loads(args.history)
        except json.JSONDecodeError:
            print("❌ Invalid JSON for --history", file=sys.stderr)
            sys.exit(1)
    
    # Fetch providers
    providers = fetch_providers(base_url)
    
    if not providers:
        print("❌ No providers found. Configure at least one model in Perplexica.", file=sys.stderr)
        sys.exit(1)
    
    # Select chat model
    chat_provider_id, chat_model_key = select_model(
        providers, "chatModels", args.chat_model
    )
    
    if not chat_provider_id:
        print("❌ No chat models available. Configure a provider in Perplexica.", file=sys.stderr)
        sys.exit(1)
    
    # Select embedding model
    embed_provider_id, embed_model_key = select_model(
        providers, "embeddingModels", args.embedding_model
    )
    
    if not embed_provider_id:
        print("❌ No embedding models available. Configure a provider in Perplexica.", file=sys.stderr)
        sys.exit(1)
    
    # Execute search (streaming, like the Perplexica web UI, to avoid timeouts)
    result = search_streaming(
        query=args.query,
        base_url=base_url,
        chat_provider_id=chat_provider_id,
        chat_model_key=chat_model_key,
        embed_provider_id=embed_provider_id,
        embed_model_key=embed_model_key,
        mode=args.mode,
        sources=sources,
        instructions=args.instructions,
        history=history,
        chunk_timeout=args.timeout,
    )
    
    # Output results
    format_output(result, args.query, args.mode, sources, args.json, args.quiet)


if __name__ == "__main__":
    main()
