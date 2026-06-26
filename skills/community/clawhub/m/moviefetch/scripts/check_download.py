#!/usr/bin/env python3
"""
homeflix / check_download
Queries qBittorrent Web UI for download progress of a movie.
Uses fuzzy title matching since torrent names include year/quality tags.
"""
import json
import os
import sys
import requests

QBIT_URL      = os.environ.get("QBIT_URL", "http://localhost:8080")
QBIT_USERNAME = os.environ.get("QBIT_USERNAME", "admin")
QBIT_PASSWORD = os.environ.get("QBIT_PASSWORD", "")

# qBittorrent state → human label
STATE_MAP = {
    "downloading":      "Downloading",
    "stalledDL":        "Stalled (no seeds)",
    "uploading":        "Seeding",
    "stalledUP":        "Seeding (idle)",
    "pausedDL":         "Paused",
    "pausedUP":         "Complete (paused)",
    "queuedDL":         "Queued",
    "checkingDL":       "Checking",
    "missingFiles":     "Missing files",
    "error":            "Error",
    "moving":           "Moving to Plex",
}


def login(session: requests.Session):
    resp = session.post(
        f"{QBIT_URL}/api/v2/auth/login",
        data={"username": QBIT_USERNAME, "password": QBIT_PASSWORD},
        timeout=5,
    )
    if resp.text.strip() != "Ok.":
        raise RuntimeError(f"qBittorrent login failed: {resp.text}")


def get_torrents(session: requests.Session):
    resp = session.get(f"{QBIT_URL}/api/v2/torrents/info", timeout=5)
    resp.raise_for_status()
    return resp.json()


def fuzzy_match(title: str, torrents: list):
    """Return the best matching torrent by word overlap (case-insensitive)."""
    title_words = set(title.lower().split())
    best, best_score = None, 0
    for t in torrents:
        torrent_words = set(t["name"].lower().replace(".", " ").split())
        score = len(title_words & torrent_words)
        if score > best_score:
            best, best_score = t, score
    # Require at least half the query words to match
    if best_score >= max(1, len(title_words) // 2):
        return best
    return None


def format_eta(seconds: int) -> str:
    if seconds < 0 or seconds > 86400 * 7:
        return "unknown"
    h, rem = divmod(seconds, 3600)
    m, s   = divmod(rem, 60)
    if h:
        return f"{h}h {m}m"
    if m:
        return f"{m}m {s}s"
    return f"{s}s"


def main():
    try:
        input_data = json.loads(sys.argv[1])
        title = input_data.get("movie_title", "").strip()
        if not title:
            print(json.dumps({"error": "movie_title is required"}))
            return

        session = requests.Session()
        login(session)
        torrents = get_torrents(session)

        match = fuzzy_match(title, torrents)
        if not match:
            print(json.dumps({"found": False, "message": f"No active torrent found for '{title}'"}))
            return

        state_label = STATE_MAP.get(match["state"], match["state"])
        progress    = round(match["progress"] * 100, 1)

        print(json.dumps({
            "found":    True,
            "name":     match["name"],
            "state":    state_label,
            "progress": progress,
            "eta":      format_eta(match.get("eta", -1)),
            "size_gb":  round(match["size"] / 1e9, 2),
        }))

    except Exception as e:
        print(json.dumps({"error": str(e)}))


if __name__ == "__main__":
    main()
