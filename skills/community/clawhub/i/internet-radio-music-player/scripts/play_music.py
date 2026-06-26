#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
play_music.py - Music stream player via Foobar2000.
Replaces play_music.ps1 (PowerShell had encoding bugs with cp1251).

Commands:
    play [-m MOOD]              Play by mood/genre
    playurl -u URL [-m MOOD]    Play specific URL
    stop                        Stop playback
    status                      Show current stream
    history                     Show playback history
    next                        Next random stream in same mood
    prev                        Previous stream from history

Usage:
    python play_music.py play -m jazz
    python play_music.py playurl -u http://example.com/stream -m ambient
    python play_music.py stop
    python play_music.py status
    python play_music.py history
    python play_music.py next
    python play_music.py prev
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from datetime import datetime

# --- Paths ---
_FOOBAR_PATHS = [
    r"C:\Program Files\foobar2000\foobar2000.exe",
    r"C:\Program Files (x86)\foobar2000\foobar2000.exe",
]
FOOBAR = next((p for p in _FOOBAR_PATHS if os.path.isfile(p)), _FOOBAR_PATHS[0])
# Determine paths: try env vars first, then auto-detect relative to skill dirs
_SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MUSIC_DB_SKILL = os.path.join(os.path.expanduser("~"), ".openclaw", "skills", "internet-radio-music-db")
# Fallback: sibling directory with old slug or alternative install name
_MUSIC_DB_SIBLING_OLD = os.path.join(os.path.dirname(_SKILL_DIR), "music-db")
_MUSIC_DB_SIBLING_NEW = os.path.join(os.path.dirname(_SKILL_DIR), "internet-radio-music-db")
# Try to find music-db state.json
if os.environ.get("MUSIC_DB_PATH"):
    MUSIC_DB_STATE = os.environ["MUSIC_DB_PATH"]
elif os.path.exists(os.path.join(_MUSIC_DB_SKILL, "state.json")):
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SKILL, "state.json")
elif os.path.exists(os.path.join(_MUSIC_DB_SIBLING_NEW, "state.json")):
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SIBLING_NEW, "state.json")
elif os.path.exists(os.path.join(_MUSIC_DB_SIBLING_OLD, "state.json")):
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SIBLING_OLD, "state.json")
else:
    MUSIC_DB_STATE = os.path.join(_MUSIC_DB_SKILL, "state.json")
STATE_FILE = os.path.join(_SKILL_DIR, "state.json")

MIN_BYTES = 8192
TEST_DURATION = 3
MAX_ATTEMPTS = 10
HTTP_TIMEOUT = 8

# Fix encoding for Windows console
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# --- Mood -> Genre mapping ---

ALL_GENRES = [
    "rock", "pop", "jazz", "classical", "electronic", "dance",
    "blues", "metal", "indie", "alternative", "ambient", "latin",
    "reggae", "folk", "soul", "punk", "funk", "disco",
    "house", "techno", "trance", "country", "oldies", "80s",
    "90s", "top-40", "news", "talk", "gospel",
]

MOOD_MAP = [
    (r"sleep|calm|relax|quiet|peaceful|medita", ["ambient", "classical", "nature", "meditation", "piano"]),
    (r"happy|fun|dance|party|energetic|joy", ["dance", "disco", "pop", "funk", "house"]),
    (r"sad|blues|melanchol|depress", ["blues", "jazz", "soul", "ambient"]),
    (r"rock|hard|garage|grunge", ["rock", "metal", "punk", "alternative", "indie"]),
    (r"electronic|synth|lofi|lo-fi|dream|space", ["electronic", "ambient", "house", "techno"]),
    (r"classical|orchestra|symphon|piano|instrument", ["classical"]),
    (r"reggae|tropical|summer|island|ska", ["reggae", "latin", "disco"]),
    (r"hip|rap|rnb|r-n-b|soul", ["soul", "funk", "pop", "disco"]),
    (r"techno|rave|club|trance", ["techno", "house", "trance", "electronic", "dance"]),
    (r"jazz|swing", ["jazz", "blues", "soul"]),
    (r"country|western|кантри", ["country", "folk"]),
    (r"metal|heavy|power|speed|aggress|angry", ["metal", "punk", "rock"]),
    (r"80s?|90s?|retro|nostalg|old|vintage", ["80s", "90s", "oldies", "disco", "pop"]),
    (r"indie|alternat|unusual|experim", ["indie", "alternative"]),
    (r"latin|salsa|bachata|samba|brazil", ["latin"]),
    (r"pop|popular|hit|radio|top", ["pop", "top-40"]),
    (r"work|focus|concentrat|study", ["ambient", "classical", "electronic"]),
    (r"sunset|chill|evening|lounge", ["ambient", "jazz", "indie", "folk", "chill", "lounge", "downtempo", "relaxation"]),
    (r"news|talk|podcast", ["news", "talk"]),
    (r"gospel|church|spirit|pray", ["gospel", "classical", "ambient"]),
]

DEFAULT_GENRES = ["ambient", "electronic", "jazz"]


def get_genres_from_mood(mood):
    m = mood.lower().strip()
    if m in ALL_GENRES:
        return [m]
    for pattern, genres in MOOD_MAP:
        if re.search(pattern, m):
            return genres
    return DEFAULT_GENRES


# --- State management ---

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    return {"History": [], "CurrentGenre": "ambient", "CurrentIndex": 0, "Volume": 50, "CurrentStream": None}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


# --- DB loading ---

def load_db():
    if not os.path.exists(MUSIC_DB_STATE):
        return []
    with open(MUSIC_DB_STATE, "r", encoding="utf-8") as f:
        return json.load(f).get("streams", [])


def _parse_genres_field(val):
    """Разобрать поле genres (строка или список) в список отдельных жанров."""
    if isinstance(val, list):
        return [g.strip().lower() for g in val if g.strip()]
    if isinstance(val, str):
        return [g.strip().lower() for g in val.replace(";", ",").split(",") if g.strip()]
    return []


def _genre_relevance_score(stream, genres):
    """Оценка релевантности потока.
    Критерии сортировки (по приоритету):
      1. Совпадение основного genre (точное = 0, только в genres = 1, нет = inf)
      2. Позиция запрошенного жанра в списке genres (чем раньше — тем лучше)
      3. Количество «лишних» жанров (чем меньше — тем лучше)
      4. Скорость (чем быстрее — тем лучше)
    Возвращает кортеж: (genre_match, позиция, лишние_жанры, -скорость)
    Меньшее значение = более подходящий поток."""
    requested = [g.lower() for g in genres]
    stream_genres = _parse_genres_field(stream.get("genres") or [])

    # Совпадение основного genre: 0 = точное, 1 = только в genres, inf = нет
    main_genre = stream.get("genre", "").lower()
    if main_genre in requested:
        genre_match_level = 0
    elif any(sg in requested for sg in stream_genres):
        genre_match_level = 1
    else:
        return (float("inf"), float("inf"), float("inf"), 0)

    # Минимальная позиция запрошенного жанра в списке genres
    # Если основной genre совпал точно и genres пустой — это идеальное совпадение (position=0)
    matched_in_genres = 0
    min_position = float("inf")
    for idx, sg in enumerate(stream_genres):
        if sg in requested:
            matched_in_genres += 1
            if idx < min_position:
                min_position = idx

    if matched_in_genres == 0:
        # Если совпадение только по основному genre — position=0 (идеально)
        if genre_match_level == 0 and not stream_genres:
            min_position = 0
        else:
            min_position = float("inf")

    extra = len(stream_genres) - matched_in_genres
    speed = stream.get("last_speed_bps") or (stream.get("bitrate") or 0) * 128

    return (genre_match_level, min_position, extra, -speed)


def load_streams_from_db(genres):
    db = load_db()
    result = []
    for s in db:
        if not s.get("available"):
            continue
        # Совпадение по основному полю genre
        genre_match = s.get("genre", "").lower() in [g.lower() for g in genres]
        # Совпадение по списку genres
        stream_genres = _parse_genres_field(s.get("genres") or [])
        genres_match = any(sg in [g.lower() for g in genres] for sg in stream_genres)
        if genre_match or genres_match:
            result.append(s)
    # Сортировка: позиция жанра в списке > точность > скорость
    result.sort(key=lambda s: _genre_relevance_score(s, genres))
    return result


# --- Foobar2000 control ---

def play_foobar(url):
    stop_foobar()
    time.sleep(2)
    subprocess.Popen([FOOBAR, "/stop"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    subprocess.Popen([FOOBAR, "/play", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def stop_foobar():
    subprocess.run(["taskkill", "/f", "/im", "foobar2000.exe"], capture_output=True, timeout=10)


# --- Speed test ---

def check_stream_speed(url):
    import urllib.request
    req = urllib.request.Request(url, headers={
        "User-Agent": "Foobar2000",
        "Icy-MetaData": "0",
    })
    total_bytes = 0
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            while True:
                elapsed = time.time() - start_time
                if elapsed >= TEST_DURATION:
                    break
                chunk = resp.read(4096)
                if not chunk:
                    break
                total_bytes += len(chunk)
    except Exception as e:
        print(f"  FAIL: {e}")
        return False
    elapsed = time.time() - start_time
    speed = total_bytes / max(elapsed, 0.01)
    speed_kb = speed / 1024
    print(f"  Check: {total_bytes} bytes in {elapsed:.1f}s ({speed_kb:.1f} KB/s)")
    return total_bytes >= MIN_BYTES


# --- Duration tracking ---

def update_duration(state):
    stream = state.get("CurrentStream")
    if stream and stream.get("StartedAt"):
        try:
            started = datetime.strptime(stream["StartedAt"], "%Y-%m-%d %H:%M:%S")
            elapsed = datetime.now() - started
            h = elapsed.seconds // 3600
            m = (elapsed.seconds // 60) % 60
            s = elapsed.seconds % 60
            dur_str = f"{h:02d}:{m:02d}:{s:02d}"
            history = state.get("History", [])
            if history:
                history[-1]["Duration"] = dur_str
        except Exception:
            pass


def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# --- Commands ---

def cmd_stop(state):
    update_duration(state)
    state["CurrentStream"] = None
    state["Stopped"] = True
    save_state(state)
    stop_foobar()
    print("STOPPED")


def cmd_status(state):
    stream = state.get("CurrentStream")
    if stream:
        started = datetime.strptime(stream["StartedAt"], "%Y-%m-%d %H:%M:%S")
        elapsed = datetime.now() - started
        h = elapsed.seconds // 3600
        m = (elapsed.seconds // 60) % 60
        s = elapsed.seconds % 60
        print(f"NOW_PLAYING: {stream['Name']}")
        print(f"Genre: {stream['Genre']}")
        print(f"Url: {stream['Url']}")
        print(f"Started at: {stream['StartedAt']}")
        print(f"Elapsed: {h:02d}:{m:02d}:{s:02d}")
    else:
        print("NO_STREAM")


def cmd_history(state):
    history = state.get("History", [])
    if not history:
        print("History empty")
        return
    print(f"{'Time':<22} {'Genre':<10} {'Duration':>8}  Stream")
    print("-" * 100)
    for h in history:
        dur = h.get("Duration", "") or ""
        note = h.get("Note", "")
        line = f"{h['Time']:<22} {h['Genre']:<10} {dur:>8}  {h['Name']}"
        if note:
            line += f"  [{note}]"
        print(line)
    print(f"\nTotal entries: {len(history)}")


def cmd_next(state):
    update_duration(state)
    current_genre_str = state.get("CurrentGenre", "ambient")
    genres = get_genres_from_mood(current_genre_str)
    streams = load_streams_from_db(genres)
    if not streams:
        print("No streams available")
        sys.exit(1)
    current_url = state.get("CurrentStream", {}).get("Url", "")
    candidates = [s for s in streams if s["url"] != current_url]
    if not candidates:
        candidates = streams
    # streams уже отсортированы по релевантности в load_streams_from_db
    # Просто берём первый (самый релевантный) из кандидатов
    if candidates is not streams:
        # Отсортируем кандидатов так же по релевантности
        candidates.sort(key=lambda s: _genre_relevance_score(s, genres))
    stream = candidates[0]
    play_foobar(stream["url"])
    state["CurrentGenre"] = genres[0]
    state["History"].append({
        "Time": now_str(),
        "Genre": genres[0],
        "Name": stream["name"],
        "Url": stream["url"],
        "Duration": None,
    })
    state["CurrentStream"] = {
        "Url": stream["url"],
        "Name": stream["name"],
        "Genre": stream["genre"],
        "StartedAt": now_str(),
    }
    save_state(state)
    print(f"SWITCHED to: {stream['name']} [{stream['genre']}]")


def cmd_prev(state):
    update_duration(state)
    history = state.get("History", [])
    if len(history) < 2:
        print("No previous stream in history")
        sys.exit(1)
    history = history[:-1]
    state["History"] = history
    prev = history[-1]
    prev_name = prev.get("Name", "")
    if not prev_name:
        print("No stream name in history entry")
        sys.exit(1)
    # Look up current URL in DB by stream name (URLs may change over time)
    db = load_db()
    url = None
    genre = prev.get("Genre", "")
    for s in db:
        if s.get("name", "").lower() == prev_name.lower() and s.get("available"):
            url = s["url"]
            genre = s.get("genre", genre)
            break
    # Fallback: partial name match
    if not url:
        for s in db:
            if prev_name.lower() in s.get("name", "").lower() and s.get("available"):
                url = s["url"]
                genre = s.get("genre", genre)
                break
    # Fallback: use old URL from history (may be stale)
    if not url:
        url = prev.get("Url")
        if url:
            print(f"  WARNING: stream '{prev_name}' not found in DB, using stale URL from history")
        else:
            print(f"No URL found for '{prev_name}' in DB or history")
            sys.exit(1)
    play_foobar(url)
    state["CurrentStream"] = {
        "Url": url,
        "Name": prev_name,
        "Genre": genre,
        "StartedAt": now_str(),
    }
    save_state(state)
    print(f"PREVIOUS: {prev_name} [{genre}]")


def cmd_resume(state):
    """Resume the last played stream from full history (not limited to today)."""
    history = state.get("History", [])
    if not history:
        print("No history — nothing to resume")
        sys.exit(1)
    last = history[-1]
    last_name = last.get("Name", "")
    if not last_name:
        print("No stream name in last history entry")
        sys.exit(1)
    # Look up current URL in DB by stream name
    db = load_db()
    url = None
    genre = last.get("Genre", "")
    for s in db:
        if s.get("name", "").lower() == last_name.lower() and s.get("available"):
            url = s["url"]
            genre = s.get("genre", genre)
            break
    # Fallback: partial name match
    if not url:
        for s in db:
            if last_name.lower() in s.get("name", "").lower() and s.get("available"):
                url = s["url"]
                genre = s.get("genre", genre)
                break
    # Fallback: use old URL from history
    if not url:
        url = last.get("Url")
        if url:
            print(f"  WARNING: stream '{last_name}' not found in DB, using stale URL from history")
        else:
            print(f"No URL found for '{last_name}' in DB or history")
            sys.exit(1)
    play_foobar(url)
    state["History"].append({
        "Time": now_str(),
        "Genre": genre,
        "Name": last_name,
        "Url": url,
        "Duration": None,
    })
    state["CurrentStream"] = {
        "Url": url,
        "Name": last_name,
        "Genre": genre,
        "StartedAt": now_str(),
    }
    save_state(state)
    print(f"RESUMED: {last_name} [{genre}]")


def cmd_playurl(state, url, mood="ambient"):
    update_duration(state)
    resolved_genre = mood if mood else "ambient"
    url_name = re.sub(r"^https?://", "", url).split("/")[0]
    db = load_db()
    for s in db:
        if s.get("url") == url:
            resolved_genre = s["genre"]
            url_name = s["name"]
            break
    play_foobar(url)
    state["History"].append({
        "Time": now_str(),
        "Genre": resolved_genre,
        "Name": url_name,
        "Url": url,
        "Duration": None,
    })
    state["CurrentStream"] = {
        "Url": url,
        "Name": url_name,
        "Genre": resolved_genre,
        "StartedAt": now_str(),
    }
    save_state(state)
    print(f"PLAYING: {url_name} [{resolved_genre}]")
    print(f"Url: {url}")


def cmd_play(state, mood):
    # Resume last stopped stream if no mood specified
    if not mood and state.get("Stopped") and state.get("History"):
        state["Stopped"] = False
        save_state(state)
        cmd_resume(state)
        return
    if not mood:
        mood = "ambient"
    genres = get_genres_from_mood(mood)
    streams = load_streams_from_db(genres)
    if not streams:
        print(f"No working streams for mood: {mood} (tried genres: {', '.join(genres)})")
        sys.exit(1)
    state["CurrentGenre"] = genres[0]
    stream = None
    max_att = min(MAX_ATTEMPTS, len(streams))
    for i, s in enumerate(streams[:max_att]):
        print(f"  [{i+1}/{max_att}] Testing: {s['name']} [{s['genre']}]")
        if check_stream_speed(s["url"]):
            stream = s
            print("  OK")
            break
        else:
            print("  TOO SLOW, skipping")
    if not stream:
        print(f"ERROR: No working streams for mood: {mood} (all {len(streams)} streams failed speed test)")
        sys.exit(1)
    play_foobar(stream["url"])
    state["History"].append({
        "Time": now_str(),
        "Genre": genres[0],
        "Name": stream["name"],
        "Url": stream["url"],
        "Duration": None,
        "Note": f"Mood: {mood}",
    })
    state["CurrentStream"] = {
        "Url": stream["url"],
        "Name": stream["name"],
        "Genre": stream["genre"],
        "StartedAt": now_str(),
    }
    save_state(state)
    state["Stopped"] = False
    save_state(state)
    print(f"PLAYING: {stream['name']}")
    print(f"Genre: {stream['genre']}")
    print(f"Url: {stream['url']}")


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description="Music stream player")
    parser.add_argument("command", help="Command: play, playurl, stop, status, history, next, prev")
    parser.add_argument("-m", "--mood", default=None, help="Mood/genre (omit to resume last stopped)")
    parser.add_argument("-u", "--url", default="", help="Stream URL (for playurl)")
    parser.add_argument("-v", "--volume", type=int, default=50, help="Volume")
    args = parser.parse_args()

    cmd = args.command.lower().strip()
    state = load_state()
    state["Volume"] = args.volume

    if cmd in ("stop", "pause"):
        cmd_stop(state)
    elif cmd in ("status", "what", "playing", "now"):
        cmd_status(state)
    elif cmd in ("history", "list", "log"):
        cmd_history(state)
    elif cmd in ("next", "skip", "forward"):
        cmd_next(state)
    elif cmd in ("prev", "previous", "back"):
        cmd_prev(state)
    elif cmd in ("resume", "last", "again"):
        cmd_resume(state)
    elif cmd == "playurl":
        if not args.url:
            print("Error: --url required for playurl")
            sys.exit(1)
        cmd_playurl(state, args.url, args.mood)
    elif cmd == "play":
        cmd_play(state, args.mood)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
