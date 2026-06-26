#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI runner for Musicful API (reads .env in skill root):
Examples:
  # auto generate music
  python3 scripts/run_musicful.py auto --style "Happy songs" --mv v3.5

  # custom with lyrics
  python3 scripts/run_musicful.py custom --lyrics "..." --title "My Song" --style Pop

  # generate lyrics only
  python3 scripts/run_musicful.py lyrics --prompt "关于星空的歌词"

  # query tasks
  python3 scripts/run_musicful.py query --ids abc,def,ghi

  # generate mp4
  python3 scripts/run_musicful.py mp4 --id abc
"""
import argparse, json, sys
from typing import List
from musicful_api import (
    generate_lyrics,
    generate_music_auto,
    generate_music_with_lyrics,
    query_tasks,
    generate_mp4,
)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_auto = sub.add_parser("auto")
    p_auto.add_argument("--style", default="Happy songs")
    p_auto.add_argument("--mv", default="MFV2.0")
    p_auto.add_argument("--instrumental", type=int, default=0)
    p_auto.add_argument("--gender", default="male")

    p_custom = sub.add_parser("custom")
    p_custom.add_argument("--lyrics", required=True)
    p_custom.add_argument("--title", default="")
    p_custom.add_argument("--style", default="Happy songs")
    p_custom.add_argument("--mv", default="MFV2.0")
    p_custom.add_argument("--instrumental", type=int, default=0)
    p_custom.add_argument("--gender", default="male")

    p_lyr = sub.add_parser("lyrics")
    p_lyr.add_argument("--prompt", required=True)

    p_q = sub.add_parser("query")
    p_q.add_argument("--ids", required=True, help=",-separated task ids")

    p_mp4 = sub.add_parser("mp4")
    p_mp4.add_argument("--id", required=True)

    args = ap.parse_args()

    if args.cmd == "auto":
        ids = generate_music_auto(style=args.style, mv=args.mv, instrumental=args.instrumental, gender=args.gender)
        print(json.dumps({"ids": ids}, ensure_ascii=False))
        return

    if args.cmd == "custom":
        ids = generate_music_with_lyrics(
            lyrics=args.lyrics, title=args.title, style=args.style, mv=args.mv,
            instrumental=args.instrumental, gender=args.gender,
        )
        print(json.dumps({"ids": ids}, ensure_ascii=False))
        return

    if args.cmd == "lyrics":
        res = generate_lyrics(args.prompt)
        print(json.dumps(res, ensure_ascii=False))
        return

    if args.cmd == "query":
        ids: List[str] = [s for s in args.ids.split(",") if s]
        res = query_tasks(ids)
        print(json.dumps(res, ensure_ascii=False))
        return

    if args.cmd == "mp4":
        res = generate_mp4(args.id)
        print(json.dumps(res, ensure_ascii=False))
        return


if __name__ == "__main__":
    main()
