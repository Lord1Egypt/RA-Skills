#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: match_top_tracks.py <artist> [song1] [song2] ...", file=sys.stderr)
    sys.exit(1)

artist = sys.argv[1]
songs = sys.argv[2:]
script_dir = Path(__file__).resolve().parent
mopidy_script = script_dir / "mopidy.sh"
base_cmd = [str(mopidy_script), "search"]

matches = []
for song in songs:
    query = f"{artist} {song}"
    try:
        raw = subprocess.check_output(base_cmd + [query], text=True)
        data = json.loads(raw)
        tracks = data.get("result", [{}])[0].get("tracks", [])
    except Exception:
        tracks = []

    chosen = None
    song_l = song.lower()
    artist_l = artist.lower()

    for t in tracks:
        t_name = (t.get("name") or "").lower()
        artists = " ".join((a.get("name") or "") for a in t.get("artists") or []).lower()
        if song_l in t_name and artist_l in artists:
            chosen = {
                "requested": song,
                "uri": t.get("uri"),
                "name": t.get("name"),
                "artist": ", ".join((a.get("name") or "") for a in t.get("artists") or [])
            }
            break

    if chosen is None and tracks:
        t = tracks[0]
        chosen = {
            "requested": song,
            "uri": t.get("uri"),
            "name": t.get("name"),
            "artist": ", ".join((a.get("name") or "") for a in t.get("artists") or [])
        }

    matches.append(chosen or {"requested": song, "uri": None, "name": None, "artist": None})

print(json.dumps(matches, indent=2))
