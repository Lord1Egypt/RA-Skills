#!/usr/bin/env python3
"""Add an artist to kpop-tracker config (V2.1.0).

Supports new architecture:
- chinese_members: List of Chinese members with Weibo accounts
- taiwan_fan_sources: Taiwan fan community sources
- youtube: Official YouTube channel
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 4:
        print("Usage: add_artist.py <config_path> <name> <group> [keywords] [instagram] [x] [youtube] [weverse] [berriz] [chinese_members] [taiwan_fan_sources]")
        print('Example: add_artist.py config.json "I-DLE" "I-DLE" "I-DLE,아이들,idle" "https://www.instagram.com/i_dle_official/" "https://x.com/official_i_dle" "https://www.youtube.com/@G_I_DLE" "" "https://berriz.in/i-dle" "雨琦:@Song_Yuqi"')
        sys.exit(1)

    config_path = Path(sys.argv[1])
    name = sys.argv[2]
    group = sys.argv[3]
    keywords = sys.argv[4].split(",") if len(sys.argv) > 4 else [name]
    instagram = sys.argv[5] if len(sys.argv) > 5 else ""
    x_url = sys.argv[6] if len(sys.argv) > 6 else ""
    youtube = sys.argv[7] if len(sys.argv) > 7 else ""
    weverse = sys.argv[8] if len(sys.argv) > 8 else ""
    berriz = sys.argv[9] if len(sys.argv) > 9 else ""
    chinese_members_str = sys.argv[10] if len(sys.argv) > 10 else ""
    taiwan_fan_sources = sys.argv[11].split(",") if len(sys.argv) > 11 else []

    # Load config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Check duplicate
    for artist in config["artists"]:
        if artist["name"] == name and artist["group"] == group:
            print(f"SKIP: already exists")

            sys.exit(0)

    # Parse chinese members
    chinese_members = []
    if chinese_members_str:
        for member_str in chinese_members_str.split(","):
            if ":" in member_str:
                name_part, weibo_part = member_str.split(":", 1)
                chinese_members.append({
                    "name": name_part.strip(),
                    "weibo": weibo_part.strip()
                })

    # Add artist
    artist = {
        "name": name,
        "group": group,
        "keywords": keywords,
        "chinese_members": chinese_members,
        "sources": {
            "instagram": instagram,
            "x": x_url,
            "youtube": youtube,
            "weverse": weverse,
            "berriz": berriz,
            "taiwan_fan_sources": [a for a in taiwan_fan_sources if a]
        }
    }
    config["artists"].append(artist)

    # Save
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    safe = lambda s: s.encode("ascii", "replace").decode("ascii") if s else "(none)"
    print(f"OK: Added {safe(name)} ({safe(group)})")
    print(f"    Keywords: {len(keywords)} items")
    print(f"    IG: {instagram or '(none)'}")
    print(f"    X: {x_url or '(none)'}")
    print(f"    YouTube: {youtube or '(none)'}")
    print(f"    Weverse: {weverse or '(none)'}")
    print(f"    Berriz: {berriz or '(none)'}")
    print(f"    Chinese members: {len(chinese_members)}")
    print(f"    Taiwan fan sources: {len(taiwan_fan_sources)}")
    
    # Show chinese members detail
    for member in chinese_members:
        print(f"      - {member['name']}: {member['weibo']}")


if __name__ == "__main__":
    main()
