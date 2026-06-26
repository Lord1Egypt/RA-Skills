#!/usr/bin/env python3
"""Notion utilities for music-weekly skill.

Config is read from ~/.config/music-weekly/config.json:

    {
      "notion_api_key": "ntn_...",
      "notion_db_id": "33b75a20-...",
      "delivery_channel": "qqbot",
      "delivery_target": "qqbot:c2c:用户ID",
      "notion_api_version": "2025-09-03",
      "covers_dir": "/path/to/covers",
      "media_dir": "/path/to/media",
      "history_log": "/path/to/music-recommended-log.md"
    }

Environment variable NOTION_KEY also works as fallback.
"""

import json, os, re, time, urllib.request, urllib.parse

# --- Config loading ---
CONFIG_PATH = os.path.expanduser("~/.config/music-weekly/config.json")

def _load_config():
    defaults = {
        "notion_api_version": "2025-09-03",
        "delivery_channel": "qqbot",
        "delivery_target": "",
        "covers_dir": os.path.expanduser("~/.openclaw/workspace/covers"),
        "media_dir": os.path.expanduser("~/.openclaw/media/qqbot"),
        "history_log": os.path.expanduser("~/.openclaw/workspace/music-recommended-log.md"),
    }
    try:
        with open(CONFIG_PATH) as f:
            user_cfg = json.load(f)
            defaults.update(user_cfg)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return defaults

CONFIG = _load_config()
NOTION_KEY = os.environ.get("NOTION_KEY") or CONFIG.get("notion_api_key", "")
DB_ID = CONFIG.get("notion_db_id", "")
API_VERSION = CONFIG.get("notion_api_version", "2025-09-03")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Notion-Version": API_VERSION,
    "Content-Type": "application/json",
}


# --- Helpers ---

def get_config():
    """Return the full config dict (useful for reading delivery settings)."""
    return dict(CONFIG)


# --- API helpers ---

def _api(method, path, data=None):
    if not NOTION_KEY:
        print("ERROR: Notion API key not configured.")
        print(f"Set NOTION_KEY env var or write config to {CONFIG_PATH}")
        return None
    url = f"https://api.notion.com/v1{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(url, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  HTTP {e.code}: {err[:300]}")
        return None


def _config_check():
    if not DB_ID:
        print("ERROR: notion_db_id not configured.")
        return False
    if not NOTION_KEY:
        print("ERROR: notion_api_key not configured.")
        return False
    return True


# --- Public API ---

def get_artwork_from_apple_link(apple_url):
    """Fetch 600x600 album artwork from Apple Music URL."""
    if not apple_url:
        return None
    m = re.search(r'/(\d+)$', apple_url)
    if not m:
        return None
    album_id = m.group(1)
    time.sleep(0.2)
    url = f"https://itunes.apple.com/lookup?id={album_id}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "iTunes/12.12.2 (Mac OS X; 10.15.7)"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            if data.get("resultCount", 0) > 0:
                art = data["results"][0].get("artworkUrl100", "")
                if art:
                    return art.replace("100x100bb", "600x600bb")
    except Exception as e:
        print(f"  iTunes lookup failed for {album_id}: {e}")
    return None


def create_record(properties):
    """
    Create a Notion page in the music weekly database.

    Args:
        properties: dict of property_name -> value.

    Returns:
        response dict from Notion API, or None on failure.
    """
    if not _config_check():
        return None

    notion_props = {}
    for key, val in properties.items():
        if key == "名称":
            notion_props[key] = {"title": [{"text": {"content": val}}]}
        elif key == "封面URL":
            if isinstance(val, str) and val.startswith("http"):
                notion_props[key] = {
                    "files": [{
                        "type": "external",
                        "name": "cover.jpg",
                        "external": {"url": val}
                    }]
                }
            elif isinstance(val, dict) and "files" in val:
                notion_props[key] = val
        elif key == "Apple Music链接":
            notion_props[key] = {"url": val}
        elif key in ("发行日期", "推送日期"):
            notion_props[key] = {"date": {"start": val}}
        elif key == "综合评分":
            notion_props[key] = {"number": val}
        elif key in ("收听状态", "流派", "专辑类型", "个人喜欢程度"):
            notion_props[key] = {"select": {"name": val}}
        elif key == "音乐分布":
            notion_props[key] = {"multi_select": [{"name": v} for v in val]}
        elif isinstance(val, dict):
            notion_props[key] = val
        else:
            notion_props[key] = {"rich_text": [{"text": {"content": str(val)}}]}

    return _api("POST", f"/databases/{DB_ID}/pages", {
        "parent": {"database_id": DB_ID},
        "properties": notion_props,
    })


def update_cover_url(page_id, artwork_url):
    """Update an existing record's 封面URL (files type)."""
    if not _config_check():
        return None
    return _api("PATCH", f"/pages/{page_id}", {
        "properties": {
            "封面URL": {
                "files": [{
                    "type": "external",
                    "name": "cover.jpg",
                    "external": {"url": artwork_url}
                }]
            }
        }
    })


def query_all():
    """Query ALL records from the database."""
    if not _config_check():
        return []
    results = []
    cursor = None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        resp = _api("POST", f"/data_sources/{DB_ID}/query", body)
        if not resp:
            break
        results.extend(resp.get("results", []))
        if resp.get("has_more"):
            cursor = resp.get("next_cursor")
        else:
            break
    return results


def search_itunes(artist, album):
    """Search iTunes for an album, return result dict or None."""
    query = urllib.parse.quote(f"{artist} {album}")
    url = f"https://itunes.apple.com/search?term={query}&entity=album&limit=1"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "iTunes/12.12.2 (Mac OS X; 10.15.7)"}
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            if data.get("resultCount", 0) > 0:
                r = data["results"][0]
                return {
                    "artist": r.get("artistName", ""),
                    "album": r.get("collectionName", ""),
                    "release_date": r.get("releaseDate", "").split("T")[0],
                    "artwork_url": r.get("artworkUrl100", "").replace("100x100bb", "600x600bb"),
                    "apple_music_url": r.get("collectionViewUrl", ""),
                    "track_count": r.get("trackCount", 0),
                    "copyright": r.get("copyright", ""),
                    "genre": r.get("primaryGenreName", ""),
                }
    except Exception as e:
        print(f"  iTunes search failed: {e}")
    return None


# --- CLI ---
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "search":
        result = search_itunes(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "artwork":
        url = get_artwork_from_apple_link(sys.argv[2])
        print(url or "Not found")
    elif len(sys.argv) > 1 and sys.argv[1] == "backfill":
        records = query_all()
        fixed = 0
        for item in records:
            props = item.get("properties", {})
            files = props.get("封面URL", {}).get("files", [])
            apple_link = ""
            name = ""
            for k, v in props.items():
                t = v.get("type", "")
                if t == "title":
                    name = "".join(ts.get("plain_text", "") for ts in v.get("title", []))
                elif t == "url" and k == "Apple Music链接":
                    apple_link = v.get("url") or ""
            if not files and apple_link:
                art = get_artwork_from_apple_link(apple_link)
                if art:
                    update_cover_url(item["id"], art)
                    print(f"Fixed: {name}")
                    fixed += 1
                    time.sleep(0.35)
        print(f"\nFixed {fixed} records")
    elif len(sys.argv) > 1 and sys.argv[1] == "config":
        cfg = get_config()
        # Show config without sensitive values
        cfg_show = dict(cfg)
        if cfg_show.get("notion_api_key"):
            cfg_show["notion_api_key"] = cfg_show["notion_api_key"][:10] + "..." 
        print(json.dumps(cfg_show, indent=2, ensure_ascii=False))
    elif len(sys.argv) > 1 and sys.argv[1] == "config-path":
        print(CONFIG_PATH)
    else:
        print("Usage: python3 notion_utils.py search|artwork|backfill|config [args]")
