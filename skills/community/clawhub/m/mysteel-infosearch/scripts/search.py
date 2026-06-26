#!/usr/bin/env python3
"""
Mysteel Info Search API Client

Queries the Mysteel AI search API for commodity industry news and information.
Supports industry dynamics, market news, policy changes, corporate announcements, etc.

Usage:
    python search.py "<query_text>"

Examples:
    python search.py "钢铁行业最新动态"
    python search.py "铜价异动原因分析"
"""

import sys
import json
import argparse
from pathlib import Path

API_URL = "https://mcp.mysteel.com/mcp/info/ai-search/search"
DEFAULT_SOURCE = "MyClaw模式"
SCRIPT_DIR = Path(__file__).parent.resolve()
SKILL_DIR = SCRIPT_DIR.parent
API_KEY_FILE = SKILL_DIR / "references" / "api_key.md"


def load_api_key() -> str | None:
    """
    Load API key from file.
    Returns the API key if found and valid, None otherwise.
    """
    try:
        if API_KEY_FILE.exists():
            content = API_KEY_FILE.read_text(encoding="utf-8").strip()
            lines = content.splitlines()
            if len(lines) >= 1 and lines[0] and not lines[0].startswith("YOUR_API_KEY"):
                return lines[0].strip()
    except Exception:
        # File read error, return None
        pass
    return None


def search_info(
    text: str,
    api_key: str,
    index_search: bool = False,
    info_search: bool = True,
    static_knowledge_enable: bool = True
) -> dict:
    """
    Query the Mysteel info search API.
    Returns the API response as a dictionary.
    """
    payload = {
        "source": DEFAULT_SOURCE,
        "text": text,
        "indexSearchEnable": index_search,
        "infoSearchEnable": info_search,
        "staticKnowledgeEnable": static_knowledge_enable
    }

    headers = {
        "Content-Type": "application/json",
        "token": api_key
    }

    try:
        import urllib.request
        import urllib.error

        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        try:
            error_data = json.loads(error_body)
            message = error_data.get("message") or error_data.get("error") or error_body
        except json.JSONDecodeError:
            message = error_body
        return {
            "error": True,
            "status_code": e.code,
            "message": message
        }
    except urllib.error.URLError as e:
        return {
            "error": True,
            "message": f"URL Error: {e.reason}"
        }
    except json.JSONDecodeError as e:
        return {
            "error": True,
            "message": f"JSON Parse Error: {e}"
        }
    except TimeoutError:
        return {
            "error": True,
            "message": "Request timeout (30s)"
        }
    except Exception as e:
        return {
            "error": True,
            "message": f"Request Error: {e}"
        }


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Mysteel Info Search API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python search.py "钢铁行业最新动态"
    python search.py "铜价异动原因分析"
    python search.py "房地产政策对钢材需求的影响"
        """
    )

    parser.add_argument("text", nargs="?", help="Query text to search")
    parser.add_argument("--raw", action="store_true", help="Output raw JSON response")

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.text:
        print("Error: Query text is required.", file=sys.stderr)
        print('Usage: python search.py "<query_text>" [--raw]', file=sys.stderr)
        sys.exit(1)

    # Load API key from file
    api_key = load_api_key()
    if not api_key:
        print("Error: API key is required. Please save it in references/api_key.md", file=sys.stderr)
        sys.exit(1)

    result = search_info(args.text, api_key, index_search=False, info_search=True, static_knowledge_enable=True)

    if result.get("error"):
        print(f"Error: {result.get('message', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    # Pretty print the response
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()