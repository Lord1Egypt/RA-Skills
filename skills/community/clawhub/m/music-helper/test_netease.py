#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试网易云 API"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

from netease_api import search_song, get_lyric, get_top_songs, format_song_info

print("=" * 60)
print("🎵 网易云音乐 API 测试")
print("=" * 60)

print("\n🔍 搜索测试：晴天")
results = search_song("晴天", limit=3)
print(f"找到 {len(results)} 首")

if results:
    song = results[0]
    print(format_song_info(song))
    
    # 测试歌词
    song_id = song.get("id", 186016)
    print(f"\n📝 歌词：")
    lyric = get_lyric(song_id)
    print(lyric[:200] + "..." if len(lyric) > 200 else lyric)

print("\n\n🔥 飙升榜前 5 首:")
top = get_top_songs(playlist_id=3778678)
for i, s in enumerate(top[:5], 1):
    name = s.get("name", "未知")
    artists = ", ".join([a.get("name", "") for a in s.get("artists", [])])
    print(f"{i}. 《{name}》- {artists}")

print("\n✅ 测试完成!")
