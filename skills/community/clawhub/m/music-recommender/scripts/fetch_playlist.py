#!/usr/bin/env python3
"""Fetch NetEase Cloud Music playlist tracks.

Usage: python3 fetch_playlist.py <playlist_id>

Output: JSON array of {name, artists, album} to stdout.
"""

import json
import sys
import urllib.request
import urllib.parse


def fetch_playlist(playlist_id: str) -> list[dict]:
    url = f"https://music.163.com/api/v6/playlist/detail?id={playlist_id}&n=1000"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://music.163.com/",
        "Cookie": "os=pc;",
    }
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())

    playlist = data.get("playlist", {})
    name = playlist.get("name", "Unknown")
    track_count = playlist.get("trackCount", 0)
    tracks_raw = playlist.get("tracks", [])

    result = []
    for t in tracks_raw:
        artists = "/".join(a.get("name", "") for a in t.get("ar", []))
        result.append({
            "name": t.get("name", ""),
            "artists": artists,
            "album": t.get("al", {}).get("name", ""),
            "id": t.get("id", ""),
        })

    # Print metadata to stderr, JSON data to stdout
    print(f"Playlist: {name} | Tracks: {track_count} | Fetched: {len(result)}", file=sys.stderr)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_playlist.py <playlist_id>", file=sys.stderr)
        sys.exit(1)

    playlist_id = sys.argv[1]
    tracks = fetch_playlist(playlist_id)
    print(json.dumps(tracks, ensure_ascii=False, indent=2))
