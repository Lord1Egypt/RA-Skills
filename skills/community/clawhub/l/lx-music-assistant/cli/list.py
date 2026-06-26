import sqlite3, sys, json, os, subprocess

if sys.stdout.encoding != "utf-8":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Source name mapping
SOURCE_NAMES = {"kw": "酷我", "kg": "酷狗", "tx": "QQ", "wy": "网易云", "mg": "咪咕"}


def get_lx_data_path():
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~/AppData/Roaming"))
    elif sys.platform == "darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
    return os.path.join(base, "lx-music-desktop", "LxDatas", "lx.data.db")


def get_db_path():
    """Get database path, support --db override via CLI args."""
    for i, arg in enumerate(sys.argv):
        if arg == "--db" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return get_lx_data_path()


def open_db(db_path):
    """Open database with error handling."""
    if not os.path.exists(db_path):
        print(json.dumps({"error": f"Database not found: {db_path}"}, ensure_ascii=False))
        sys.exit(1)
    try:
        conn = sqlite3.connect(db_path)
        conn.text_factory = str
        return conn
    except sqlite3.Error as e:
        print(json.dumps({"error": f"Database error: {e}"}, ensure_ascii=False))
        sys.exit(1)


def get_playlists(db_path):
    with open_db(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT id, name, source, sourceListId FROM my_list ORDER BY position")
        result = []
        for row in c.fetchall():
            item = {"id": row[0], "name": row[1], "source": row[2], "sourceId": row[3]}
            # Add song count
            c.execute("SELECT COUNT(*) FROM my_list_music_info_order WHERE listId = ?", (row[0],))
            item["songCount"] = c.fetchone()[0]
            # Add source display name
            item["sourceName"] = SOURCE_NAMES.get(row[2], row[2]) if row[2] else "本地"
            result.append(item)
    return result


def get_playlist_songs(db_path, list_id):
    with open_db(db_path) as conn:
        c = conn.cursor()
        # Verify playlist exists
        c.execute("SELECT id, name FROM my_list WHERE id = ?", (list_id,))
        pl = c.fetchone()
        if not pl:
            print(json.dumps({"error": f"Playlist not found: {list_id}"}, ensure_ascii=False))
            sys.exit(1)
        c.execute(
            'SELECT m.name, m.singer FROM my_list_music_info_order o '
            'JOIN my_list_music_info m ON o.musicInfoId = m.id '
            'WHERE o.listId = ? ORDER BY o."order"',
            (list_id,),
        )
        result = []
        for i, r in enumerate(c.fetchall(), 1):
            result.append({"index": i, "name": r[0], "singer": r[1]})
    return {"playlist": pl[1], "total": len(result), "songs": result}


def play_playlist(db_path, list_id):
    with open_db(db_path) as conn:
        c = conn.cursor()
        c.execute("SELECT source, sourceListId FROM my_list WHERE id = ?", (list_id,))
        row = c.fetchone()
    if not row:
        print(json.dumps({"error": f"Playlist not found: {list_id}"}, ensure_ascii=False))
        sys.exit(1)
    source, sid = row
    if not source or not sid:
        print(json.dumps({"error": "No sourceId for this playlist (local list)"}, ensure_ascii=False))
        sys.exit(1)
    url = f"lxmusic://songlist/play/{source}/{sid}"
    if sys.platform == "win32":
        subprocess.run(["cmd", "/c", "start", url], shell=False)
    elif sys.platform == "darwin":
        subprocess.run(["open", url])
    else:
        subprocess.run(["xdg-open", url])
    print(json.dumps({"action": "play", "source": source, "sourceId": sid, "url": url}, ensure_ascii=False))


def print_help():
    help_text = """LX Music Playlist Tool

Usage:
  python playlist.py                     List all playlists
  python playlist.py songs <list_id>     Show songs in a playlist
  python playlist.py play <list_id>      Play a playlist
  python playlist.py --db <path>         Specify database path
  python playlist.py help                Show this help

Playlist ID can be obtained from the list command."""
    print(help_text)


if __name__ == "__main__":
    db_path = get_db_path()

    # Simple arg parsing (skip --db and its value)
    clean_args = []
    skip_next = False
    for i, a in enumerate(sys.argv[1:]):
        if skip_next:
            skip_next = False
            continue
        if a == "--db":
            skip_next = True
            continue
        clean_args.append(a)

    if not clean_args or clean_args[0] == "list":
        print(json.dumps(get_playlists(db_path), ensure_ascii=False, indent=2))
    elif clean_args[0] == "songs" and len(clean_args) >= 2:
        print(json.dumps(get_playlist_songs(db_path, clean_args[1]), ensure_ascii=False, indent=2))
    elif clean_args[0] == "play" and len(clean_args) >= 2:
        play_playlist(db_path, clean_args[1])
    elif clean_args[0] == "help":
        print_help()
    else:
        print(f"Unknown command: {clean_args[0]}")
        print_help()
