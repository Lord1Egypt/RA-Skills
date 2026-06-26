#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator: generate → show lyrics (if auto) → poll tasks → emit preview (status=2) → emit full mp3 (status=0)
Usage examples:
  # Auto: generate lyrics first, then song
  python3 scripts/run_and_watch.py auto --prompt "为我的同事创作一首歌，中文，励志，流行"

  # Custom: user-provided lyrics; skip lyrics generation
  python3 scripts/run_and_watch.py custom --lyrics "完整歌词..." --title "同路人" --style Pop
"""
import argparse, json, sys, time
from typing import List
from musicful_api import generate_lyrics, generate_music_auto, generate_music_with_lyrics, query_tasks


def poll_two_phase(ids: List[str], max_wait_sec: int = 900, interval_sec: int = 8):
    """Poll per id until preview (status=2) and full (status=0).
    Returns: { results: {id: {preview, full, title, lyric}}, snapshots: [...] }
    Emits nothing; printing is handled by caller.
    """
    start = time.time()
    # Normalize ids to str keys
    id_keys = [str(x) for x in ids]
    results = {k: {"preview": None, "full": None, "title": None, "lyric": None} for k in id_keys}
    snapshots = []
    while time.time() - start <= max_wait_sec:
        res = query_tasks(ids)
        snapshots.append(res)
        all_full_or_done = True
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
            # determine if this id is done
        for k in id_keys:
            if not results[k]["full"]:
                all_full_or_done = False
                break
        if all_full_or_done:
            break
        time.sleep(interval_sec)
    return {"results": results, "snapshots": snapshots}


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)

    p_auto = sub.add_parser("auto")
    p_auto.add_argument("--prompt", required=True)
    p_auto.add_argument("--style", default="Pop")
    p_auto.add_argument("--mv", default="MFV2.0")
    p_auto.add_argument("--instrumental", type=int, default=0)
    p_auto.add_argument("--gender", default="male")

    p_custom = sub.add_parser("custom")
    p_custom.add_argument("--lyrics", required=True)
    p_custom.add_argument("--title", default="")
    p_custom.add_argument("--style", default="Pop")
    p_custom.add_argument("--mv", default="MFV2.0")
    p_custom.add_argument("--instrumental", type=int, default=0)
    p_custom.add_argument("--gender", default="male")

    args = ap.parse_args()

    if args.mode == "auto":
        # Step 1: generate lyrics first and print
        lyr_res = generate_lyrics(args.prompt)
        # Normalize: lyr_res may contain text/title variations; try common keys
        lyrics_text = lyr_res.get("text") or lyr_res.get("lyrics") or lyr_res.get("lyric") or lyr_res
        out_lyr = {"status": "lyrics_ready", "lyrics": lyrics_text}
        print(json.dumps(out_lyr, ensure_ascii=False))
        sys.stdout.flush()

        # Step 2: submit auto music (no lyrics for instrumental=1; else use custom w/ lyrics)
        if int(args.instrumental) == 1 or not lyrics_text:
            ids = generate_music_auto(style=args.style, mv=args.mv, instrumental=args.instrumental, gender=args.gender)
        else:
            ids = generate_music_with_lyrics(lyrics=str(lyrics_text), title="", style=args.style, mv=args.mv,
                                             instrumental=args.instrumental, gender=args.gender)
        print(json.dumps({"status": "submitted", "ids": ids}, ensure_ascii=False))
        sys.stdout.flush()

        # Step 3: poll two-phase and emit per-id preview/full when available
        state = {str(x): {"preview": None, "full": None} for x in ids}
        start = time.time()
        max_wait_sec = 900
        interval_sec = 8
        while time.time() - start <= max_wait_sec:
            res = poll_two_phase(ids)
            results = res.get("results", {})
            all_full = True
            for k, v in results.items():
                # preview event per id
                if v.get("preview") and not state[k]["preview"]:
                    payload = {"status": "preview_ready", "id": k, "audio_url": v["preview"]}
                    if v.get("title"):
                        payload["title"] = v["title"]
                    print(json.dumps(payload, ensure_ascii=False))
                    sys.stdout.flush()
                    state[k]["preview"] = v["preview"]
                # full event per id
                if v.get("full") and not state[k]["full"]:
                    payload = {"status": "full_ready", "id": k, "audio_url": v["full"]}
                    if v.get("title"):
                        payload["title"] = v["title"]
                    print(json.dumps(payload, ensure_ascii=False))
                    sys.stdout.flush()
                    state[k]["full"] = v["full"]
                if not state[k]["full"]:
                    all_full = False
            if all_full:
                break
            time.sleep(interval_sec)
        return

    if args.mode == "custom":
        # Direct submit with provided lyrics
        ids = generate_music_with_lyrics(lyrics=args.lyrics, title=args.title, style=args.style, mv=args.mv,
                                         instrumental=args.instrumental, gender=args.gender)
        print(json.dumps({"status": "submitted", "ids": ids}, ensure_ascii=False))
        sys.stdout.flush()
        # Poll and emit per-id events
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
                    sys.stdout.flush()
                    state[k]["preview"] = v["preview"]
                if v.get("full") and not state[k]["full"]:
                    payload = {"status": "full_ready", "id": k, "audio_url": v["full"]}
                    if v.get("title"):
                        payload["title"] = v["title"]
                    print(json.dumps(payload, ensure_ascii=False))
                    sys.stdout.flush()
                    state[k]["full"] = v["full"]
                if not state[k]["full"]:
                    all_full = False
            if all_full:
                break
            time.sleep(interval_sec)
        return


if __name__ == "__main__":
    main()
