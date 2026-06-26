#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, USLT, ID3NoHeaderError


def fetch_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8", "ignore"))


def pick_lyric_text(payload):
    if isinstance(payload, dict):
        for key in ("lyric", "lrc", "text", "data"):
            val = payload.get(key)
            if isinstance(val, str) and val.strip():
                return val
            if isinstance(val, dict):
                for sub in ("lyric", "lrc", "text"):
                    sval = val.get(sub)
                    if isinstance(sval, str) and sval.strip():
                        return sval
    if isinstance(payload, str):
        return payload
    return ""


def main():
    if len(sys.argv) != 6:
        print("usage: embed_metadata.py <mp3-path> <port> <song-json> <cover-url> <lyric-endpoint>", file=sys.stderr)
        sys.exit(1)

    mp3_path, port, song_json, cover_url, lyric_endpoint = sys.argv[1:]
    song = json.loads(song_json)

    try:
        tags = ID3(mp3_path)
    except ID3NoHeaderError:
        tags = ID3()

    tags.delall("TIT2")
    tags.delall("TPE1")
    tags.delall("TALB")
    tags.delall("USLT")
    tags.delall("APIC")

    title = str(song.get("name", "")).strip()
    artist = str(song.get("artist", "")).strip()
    album = str(song.get("album", "")).strip()

    if title:
        tags.add(TIT2(encoding=3, text=title))
    if artist:
        tags.add(TPE1(encoding=3, text=[artist]))
    if album:
        tags.add(TALB(encoding=3, text=album))

    lyric_text = ""
    if lyric_endpoint:
        try:
            lyric_payload = fetch_json(lyric_endpoint)
            lyric_text = pick_lyric_text(lyric_payload).strip()
        except Exception:
            lyric_text = ""
    if lyric_text:
        tags.add(USLT(encoding=3, lang="chi", desc="", text=lyric_text))

    if cover_url:
        try:
            req = urllib.request.Request(cover_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp:
                cover_data = resp.read()
                ctype = resp.headers.get_content_type() or "image/jpeg"
            if cover_data:
                tags.add(APIC(encoding=3, mime=ctype, type=3, desc="Cover", data=cover_data))
        except Exception:
            pass

    tags.save(mp3_path, v2_version=3)
    print(json.dumps({"ok": True, "path": mp3_path, "title": title, "artist": artist, "album": album, "embedded_lyrics": bool(lyric_text), "embedded_cover": bool(cover_url)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
