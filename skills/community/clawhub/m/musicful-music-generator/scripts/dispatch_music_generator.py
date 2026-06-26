#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dispatcher for /music_generator
Modes:
  - mode=normal  → auto pipeline: generate lyrics → submit → preview (status=2) → full (status=0)
  - mode=bgm     → pure music (instrumental=1): submit → preview → full
  - mode=lyrics  → lyrics only: immediately return lyrics
Args:
  --mode (normal|bgm|lyrics)
  --prompt
  --style (default Pop)
  --mv (default MFV2.0)
  --gender (default male)
"""
import argparse, json, time
from typing import List
from musicful_api import generate_lyrics, generate_music_auto, generate_music_with_lyrics, query_tasks


def poll_two_phase(ids: List[str], max_wait_sec: int = 900, interval_sec: int = 8):
    start = time.time()
    id_keys = [str(x) for x in ids]
    results = {k: {"preview": None, "full": None, "title": None, "lyric": None} for k in id_keys}
    while time.time() - start <= max_wait_sec:
        res = query_tasks(ids)
        all_full = True
        for item in res:
            k = str(item.get("id") or item.get("task_id") or "")
            if not k:
                continue
            st = item.get("status")
            au = item.get("audio_url")
            ti = item.get("title")
            ly = item.get("lyric") or item.get("lyrics")
            if ti and not results[k]["title"]:
                results[k]["title"] = ti
            if ly and not results[k]["lyric"]:
                results[k]["lyric"] = ly
            if st == 2 and (not results[k]["preview"]) and au:
                results[k]["preview"] = au
            if st == 0 and (not results[k]["full"]) and au:
                results[k]["full"] = au
        for k in id_keys:
            if not results[k]["full"]:
                all_full = False
                break
        if all_full:
            break
        time.sleep(interval_sec)
    return {"results": results}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="normal")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--style", default="Pop")
    ap.add_argument("--mv", default="MFV2.0")
    ap.add_argument("--gender", default="male")
    args = ap.parse_args()

    mode = (args.mode or "normal").lower()

    if mode == "lyrics":
        lyr_res = generate_lyrics(args.prompt)
        lyrics_text = lyr_res.get("text") or lyr_res.get("lyrics") or lyr_res.get("lyric") or lyr_res
        print(json.dumps({"status": "lyrics_ready", "lyrics": lyrics_text}, ensure_ascii=False))
        return

    if mode == "bgm":
        # pure music, no lyrics
        ids = generate_music_auto(prompt=args.prompt, style=args.style, mv=args.mv, instrumental=1, gender=args.gender)
        print(json.dumps({"status": "submitted", "ids": ids}, ensure_ascii=False))
        # Emit per-id events as they become available
        state = {str(x): {"preview": None, "full": None} for x in ids}
        start = time.time()
        max_wait_sec = 900
        interval_sec = 8
        while time.time() - start <= max_wait_sec:
            res = poll_two_phase(ids)
            results = res.get("results", {})
            all_full = True
            for k, v in results.items():
                if v.get("preview") and not state[k]["preview"]:
                    payload = {"status": "preview_ready", "id": k, "audio_url": v["preview"]}
                    if v.get("title"):
                        payload["title"] = v["title"]
                    print(json.dumps(payload, ensure_ascii=False))
                    state[k]["preview"] = v["preview"]
                if v.get("full") and not state[k]["full"]:
                    payload = {"status": "full_ready", "id": k, "audio_url": v["full"]}
                    if v.get("title"):
                        payload["title"] = v["title"]
                    print(json.dumps(payload, ensure_ascii=False))
                    state[k]["full"] = v["full"]
                if not state[k]["full"]:
                    all_full = False
            if all_full:
                break
            time.sleep(interval_sec)
        return

    # normal: generate lyrics then submit with lyrics
    lyr_res = generate_lyrics(args.prompt)
    lyrics_text = lyr_res.get("text") or lyr_res.get("lyrics") or lyr_res.get("lyric") or lyr_res
    print(json.dumps({"status": "lyrics_ready", "lyrics": lyrics_text}, ensure_ascii=False))
    ids = generate_music_with_lyrics(lyrics=str(lyrics_text), title="", style=args.style, mv=args.mv,
                                     instrumental=0, gender=args.gender)
    print(json.dumps({"status": "submitted", "ids": ids}, ensure_ascii=False))
    # Emit per-id events
    state = {str(x): {"preview": None, "full": None} for x in ids}
    start = time.time()
    max_wait_sec = 900
    interval_sec = 8
    while time.time() - start <= max_wait_sec:
        res = poll_two_phase(ids)
        results = res.get("results", {})
        all_full = True
        for k, v in results.items():
            if v.get("preview") and not state[k]["preview"]:
                payload = {"status": "preview_ready", "id": k, "audio_url": v["preview"]}
                if v.get("title"):
                    payload["title"] = v["title"]
                print(json.dumps(payload, ensure_ascii=False))
                state[k]["preview"] = v["preview"]
            if v.get("full") and not state[k]["full"]:
                payload = {"status": "full_ready", "id": k, "audio_url": v["full"]}
                if v.get("title"):
                    payload["title"] = v["title"]
                print(json.dumps(payload, ensure_ascii=False))
                state[k]["full"] = v["full"]
            if not state[k]["full"]:
                all_full = False
        if all_full:
            break
        time.sleep(interval_sec)


if __name__ == "__main__":
    main()
