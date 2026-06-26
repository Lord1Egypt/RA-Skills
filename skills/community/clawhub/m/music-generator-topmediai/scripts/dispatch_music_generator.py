#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dispatcher for /music_generator (TopMediai)
Modes:
  - mode=normal  -> generate lyrics -> submit custom music -> poll preview/full
  - mode=bgm     -> submit auto music with instrumental=1 -> poll preview/full
  - mode=lyrics  -> generate lyrics only
Args:
  --mode (normal|bgm|lyrics)
  --prompt
  --style (default Pop)
  --mv (default v5.0)
  --gender (default male)
"""
import argparse
import json
import sys
import time
from typing import Dict, Any, List
from topmediai_api import generate_lyrics, submit_and_extract_ids, query_tasks


def poll_and_emit(ids: List[str], max_wait_sec: int = 900, interval_sec: int = 8):
    state: Dict[str, Dict[str, Any]] = {
        str(x): {"preview": None, "full": None, "title": None, "song_id": None, "lyric": None}
        for x in ids
    }

    start = time.time()
    while time.time() - start <= max_wait_sec:
        rows = query_tasks(ids)

        for item in rows:
            task_id = str(item.get("id") or item.get("task_id") or "")
            if not task_id or task_id not in state:
                continue
            st = item.get("status")
            audio_url = item.get("audio_url")
            title = item.get("title")
            lyric = item.get("lyric")
            song_id = item.get("song_id")
            fail_code = item.get("fail_code")
            fail_reason = item.get("fail_reason")

            if title and not state[task_id]["title"]:
                state[task_id]["title"] = title
            if lyric and not state[task_id]["lyric"]:
                state[task_id]["lyric"] = lyric
            if song_id and not state[task_id]["song_id"]:
                state[task_id]["song_id"] = song_id

            if fail_code is not None or fail_reason:
                payload = {"status": "failed", "id": task_id, "fail_code": fail_code, "fail_reason": fail_reason}
                if state[task_id]["song_id"]:
                    payload["song_id"] = state[task_id]["song_id"]
                print(json.dumps(payload, ensure_ascii=False))
                sys.stdout.flush()
                state[task_id]["full"] = state[task_id]["full"] or "__failed__"
                continue

            if st == 2 and audio_url and not state[task_id]["preview"]:
                payload = {"status": "preview_ready", "id": task_id, "audio_url": audio_url}
                if state[task_id]["title"]:
                    payload["title"] = state[task_id]["title"]
                if state[task_id]["song_id"]:
                    payload["song_id"] = state[task_id]["song_id"]
                print(json.dumps(payload, ensure_ascii=False))
                sys.stdout.flush()
                state[task_id]["preview"] = audio_url

            if st == 0 and audio_url and not state[task_id]["full"]:
                payload = {"status": "full_ready", "id": task_id, "audio_url": audio_url}
                if state[task_id]["title"]:
                    payload["title"] = state[task_id]["title"]
                if state[task_id]["song_id"]:
                    payload["song_id"] = state[task_id]["song_id"]
                print(json.dumps(payload, ensure_ascii=False))
                sys.stdout.flush()
                state[task_id]["full"] = audio_url

        all_done = True
        for task_id in state:
            if not state[task_id]["full"]:
                all_done = False
                break

        if all_done:
            return

        time.sleep(interval_sec)

    print(json.dumps({"status": "timeout", "ids": ids}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="normal")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--style", default="Pop")
    ap.add_argument("--mv", default="v5.0")
    ap.add_argument("--gender", default="male")
    args = ap.parse_args()

    mode = (args.mode or "normal").lower()

    if mode == "lyrics":
        lyr_res = generate_lyrics(args.prompt)
        lyrics_text = lyr_res.get("text") if isinstance(lyr_res, dict) else None
        if not lyrics_text and isinstance(lyr_res, dict):
            lyrics_text = lyr_res.get("lyrics") or lyr_res.get("lyric")
        if not lyrics_text:
            lyrics_text = lyr_res
        print(json.dumps({"status": "lyrics_ready", "lyrics": lyrics_text}, ensure_ascii=False))
        return

    if mode == "bgm":
        ids = submit_and_extract_ids(
            action="auto",
            prompt=args.prompt,
            style=args.style,
            mv=args.mv,
            instrumental=1,
            gender=args.gender,
        )
        print(json.dumps({"status": "submitted", "ids": ids}, ensure_ascii=False))
        sys.stdout.flush()
        poll_and_emit(ids)
        return

    lyr_res = generate_lyrics(args.prompt)
    lyrics_text = lyr_res.get("text") if isinstance(lyr_res, dict) else None
    if not lyrics_text and isinstance(lyr_res, dict):
        lyrics_text = lyr_res.get("lyrics") or lyr_res.get("lyric")
    if not lyrics_text:
        lyrics_text = lyr_res

    print(json.dumps({"status": "lyrics_ready", "lyrics": lyrics_text}, ensure_ascii=False))
    sys.stdout.flush()

    ids = submit_and_extract_ids(
        action="custom",
        lyrics=str(lyrics_text),
        title="",
        style=args.style,
        mv=args.mv,
        instrumental=0,
        gender=args.gender,
    )
    print(json.dumps({"status": "submitted", "ids": ids}, ensure_ascii=False))
    sys.stdout.flush()
    poll_and_emit(ids)


if __name__ == "__main__":
    main()
