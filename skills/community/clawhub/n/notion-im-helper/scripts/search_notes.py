"""Search Notion pages/blocks by keyword using the Notion Search API."""
import os
import sys
import json
import time
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = os.environ.get("NOTION_API_KEY", "")
BASE_URL = "https://api.notion.com/v1"


def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }


def search(query, page_size=10):
    """Search using Notion Search API with retry on rate limit."""
    body = {
        "query": query,
        "page_size": page_size,
        "sort": {
            "direction": "descending",
            "timestamp": "last_edited_time",
        },
    }
    for attempt in range(3):
        data = json.dumps(body).encode()
        req = urllib.request.Request(
            f"{BASE_URL}/search",
            data=data,
            headers=get_headers(),
            method="POST",
        )
        try:
            resp = urllib.request.urlopen(req)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(1.5 * (attempt + 1))
                continue
            error_body = e.read().decode()
            try:
                err_data = json.loads(error_body)
                message = err_data.get("message", str(e))
            except Exception:
                message = str(e)
            return {"error": True, "code": e.code, "message": message}
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
                continue
            return {"error": True, "message": str(e)}

    return {"error": True, "message": "Rate limited after retries"}


def extract_snippet(result):
    """Extract a readable snippet from a search result."""
    obj_type = result.get("object", "")
    title = ""

    if obj_type == "page":
        props = result.get("properties", {})
        for key, val in props.items():
            if val.get("type") == "title":
                rich = val.get("title", [])
                if rich:
                    title = rich[0].get("plain_text", "")
                break

        # Try to get a hint of the last edited time
        last_edited = result.get("last_edited_time", "")
        if last_edited and len(last_edited) > 10:
            last_edited = last_edited[:10]  # YYYY-MM-DD

        return title, last_edited

    return "", ""


def format_results(results):
    """Format search results into a user-friendly string."""
    if not results:
        return "🔍 没有找到相关记录~"

    lines = ["🔍 搜索结果："]
    for i, result in enumerate(results, 1):
        title, date = extract_snippet(result)
        if title:
            date_str = f" ({date})" if date else ""
            lines.append(f"{i}. {title}{date_str}")
        else:
            # Fallback: show URL if available
            url = result.get("url", "")
            if url:
                lines.append(f"{i}. {url[-40:]}")

    return "\n".join(lines)


def main():
    if not API_KEY:
        print("ERROR|CONFIG")
        return

    keyword = sys.argv[1] if len(sys.argv) > 1 else ""
    if not keyword:
        print("ERROR| 请提供搜索关键词，例如：搜: 缓存")
        return

    result = search(keyword)
    if result.get("error"):
        code = result.get("code", 0)
        if code == 401 or "Unauthorized" in result.get("message", ""):
            print("ERROR|AUTH")
        elif code == 429:
            print("ERROR|RATE_LIMIT")
        else:
            print("ERROR|NETWORK")
        return

    results = result.get("results", [])
    formatted = format_results(results)
    print(f"OK|{formatted}")


if __name__ == "__main__":
    main()
