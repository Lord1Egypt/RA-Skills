#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
只重新匹配歌词（不动音乐）
针对音乐已整理好的目录，对"无匹配-保留原位"的歌词做增强匹配
"""
import os
import re
import sys
import shutil
from pathlib import Path

TARGET = Path('/volume4/media2/音乐_整理')
LYRIC_EXTS = {'.lrc', '.txt'}
AUDIO_EXTS = {'.flac', '.ape', '.wav', '.mp3', '.m4a', '.aac', '.ogg', '.opus', '.wma', '.aiff', '.aif'}


def sanitize_filename(name):
    if not name:
        return name
    if isinstance(name, str):
        name = name.replace('\x00', '')
    name = re.sub(r'[\\/:*?"<>|\r\n\t]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name


def find_music_for_lyric(lpath, music_index, music_by_singer, music_by_artist_title):
    """智能找歌词对应的音乐"""
    fname = os.path.basename(lpath)
    stem = Path(fname).stem
    parent = os.path.dirname(lpath)
    parent_singer = os.path.basename(parent).lower()

    # 规则 1：同目录同名
    for ae in AUDIO_EXTS:
        cand = os.path.join(parent, f"{stem}{ae}")
        if os.path.exists(cand):
            return os.path.join(parent, f"{stem}{ae}")

    # 规则 2：清理后（去编号、补空格）匹配
    candidates = [stem]
    candidates.append(sanitize_filename(stem))
    candidates.append(re.sub(r'^\d{2,5}-', '', stem).strip())
    candidates.append(re.sub(r'\s*-\s*', ' - ', stem).strip())

    for cand in candidates:
        cand_lower = cand.lower()
        if cand_lower in music_index:
            return music_index[cand_lower]

    # 规则 3：歌词 "歌手-歌名" + 父目录歌手旁证
    if '-' in stem and ' - ' not in stem:
        parts = stem.split('-', 1)
        cand_singer = parts[0].strip().lower()
        cand_title = parts[1].strip()
        if cand_singer == parent_singer:
            # 在该歌手目录下找歌名匹配
            key = (cand_singer, cand_title.lower())
            if key in music_by_artist_title:
                return music_by_artist_title[key]
            # 去编号后再匹配
            cand_title_clean = re.sub(r'^\d{2,5}-', '', cand_title).strip()
            key = (cand_singer, cand_title_clean.lower())
            if key in music_by_artist_title:
                return music_by_artist_title[key]

    # 规则 4：歌词 "歌曲-歌手" 反向
    if '-' in stem:
        parts = stem.split('-', 1)
        cand_song = parts[0].strip().lower()
        cand_artist = parts[1].strip().lower()
        if cand_artist == parent_singer:
            key = (cand_artist, cand_song)
            if key in music_by_artist_title:
                return music_by_artist_title[key]

    # 规则 5：跨歌手同名匹配（极端情况）
    stem_lower = stem.lower()
    if stem_lower in music_index:
        return music_index[stem_lower]

    return None


def main():
    print("建立音乐索引...")
    music_index = {}  # 主名 → 路径
    music_by_artist_title = {}  # (歌手_lower, 歌名_lower) → 路径

    for root, dirs, files in os.walk(TARGET):
        if '_低音质备份' in root:
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in AUDIO_EXTS:
                stem = Path(f).stem
                music_index[stem.lower()] = os.path.join(root, f)
                if ' - ' in stem:
                    artist, title = stem.split(' - ', 1)
                    artist_l = artist.strip().lower()
                    title_l = re.sub(r'^\d{2,5}-', '', title).strip().lower()
                    music_by_artist_title[(artist_l, title_l)] = os.path.join(root, f)

    print(f"音乐索引: {len(music_index)} 条")

    # 找所有歌词
    print("\n扫描歌词...")
    lyric_files = []
    for root, dirs, files in os.walk(TARGET):
        if '_低音质备份' in root:
            continue
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in LYRIC_EXTS:
                lyric_files.append(os.path.join(root, f))

    print(f"歌词总数: {len(lyric_files)}")

    # 智能匹配
    moves = []
    no_match = []
    already_ok = 0

    for lpath in lyric_files:
        stem = Path(lpath).stem
        parent = os.path.dirname(lpath)
        # 检查同目录同名（已正确）
        in_same = any(os.path.exists(os.path.join(parent, f"{stem}{ae}")) for ae in AUDIO_EXTS)
        if in_same:
            already_ok += 1
            continue

        music = find_music_for_lyric(lpath, music_index, music_by_artist_title, music_by_artist_title)
        if music:
            moves.append((lpath, music))
        else:
            no_match.append(lpath)

    print(f"\n已正确匹配（同目录）: {already_ok}")
    print(f"待移动（找到匹配）: {len(moves)}")
    print(f"保留原位（无匹配）: {len(no_match)}")

    if not moves:
        print("\n无需移动")
        return

    print(f"\n样例移动（前 10 个）:")
    for src, dst in moves[:10]:
        print(f"  {os.path.relpath(src, TARGET)} → {os.path.relpath(dst, TARGET)}")

    # 询问确认
    if '--apply' not in sys.argv:
        print(f"\n加 --apply 参数执行实际移动")
        return

    print(f"\n开始移动...")
    moved_ok = 0
    for src, music in moves:
        src_p = Path(src)
        music_p = Path(music)
        # 目标：music 同目录，歌词主名 = music 主名（保持一致）
        target = music_p.parent / src_p.name
        # 避免覆盖
        i = 0
        while target.exists():
            i += 1
            target = music_p.parent / f"{src_p.stem}__{i}{src_p.suffix}"
        try:
            shutil.move(str(src_p), str(target))
            moved_ok += 1
        except Exception as e:
            print(f"  失败: {src} → {target}: {e}")

    print(f"\n移动成功: {moved_ok}/{len(moves)}")


if __name__ == '__main__':
    main()