#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理同歌手+同歌名的重复文件
策略：保留最大的文件（无损），把小的移到 _低音质备份/
- 软删除：mv 到 _低音质备份/ 同一歌手目录，不物理删除
- 记录日志到 _已删除_时间戳/日志.log
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

TARGET = Path('/volume4/media2/音乐_整理')
AUDIO_EXTS = {'.mp3', '.flac', '.wav', '.m4a', '.ogg', '.ape'}
BACKUP = TARGET / '_低音质备份'
LOG_DIR = TARGET / f'_已删除_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

# 同歌手+同歌名重复列表（来自 2026-06-19 09:27 复查报告）
# 格式：(歌手, 歌名, 要删除的文件名)
DUP_LIST = [
    ("杨臣刚", "老鼠爱大米", "杨臣刚 - 老鼠爱大米.mp3"),       # 11.8MB -> 保留 wav 51.2MB
    ("费玉清", "一剪梅", "费玉清 - 一剪梅.mp3"),              # 10.6MB -> 保留 wav 38.3MB
    ("草东没有派对", "山海", "草东没有派对 - 山海.wav"),        # 36.9MB -> 保留 flac 75.2MB
    ("陈柯宇", "生僻字", "陈柯宇 - 生僻字.mp3"),              # 8.4MB -> 保留 wav 36.7MB
    ("戴佩妮", "你要的爱", "戴佩妮 - 你要的爱.mp3"),          # 13.3MB -> 保留 wav 40.6MB
    ("戴羽彤", "来迟", "戴羽彤 - 来迟.wav"),                  # 39.3MB -> 保留 flac 75.1MB
    ("The Band Perry", "If I Die Young", "The Band Perry - If I Die Young.mp3"),  # 8.6MB -> 保留 wav 36.5MB
    ("汤潮", "狼爱上羊", "汤潮 - 狼爱上羊.mp3"),              # 11.4MB -> 保留 wav 49.7MB
    ("唐磊", "丁香花", "唐磊 - 丁香花.mp3"),                  # 10.3MB -> 保留 wav 44.8MB
    ("屠洪刚", "霸王别姬", "屠洪刚 - 霸王别姬.mp3"),          # 11.7MB -> 保留 wav 66.3MB
    ("Ingrid Michaelson", "Everybody", "Ingrid Michaelson - Everybody.mp3"),      # 8.1MB -> 保留 wav 35.4MB
    ("萧亚轩", "突然想起你", "萧亚轩 - 突然想起你.mp3"),      # 9.9MB -> 保留 wav 40.2MB
    ("格格", "生日祝福歌", "格格 - 生日祝福歌.mp3"),          # 7.8MB -> 保留 flac 23.9MB
    ("茄子蛋", "浪子回头", "茄子蛋 - 浪子回头.mp3"),          # 11.2MB -> 保留 wav 45.0MB
    ("八三夭乐团", "想见你想见你想见你", "八三夭乐团 - 想见你想见你想见你.mp3"),  # 9.2MB -> 保留 flac 78.8MB
    ("海来阿木", "烟雨人间", "海来阿木 - 烟雨人间.wav"),      # 36.1MB -> 保留 flac 45.1MB
    ("海来阿木", "阿果吉曲", "海来阿木 - 阿果吉曲.mp3"),      # 8.7MB -> 保留 wav 38.8MB
    ("海来阿木", "孤身的人", "海来阿木 - 孤身的人.flac"),      # 29.8MB -> 保留 wav 44.9MB
    ("海来阿木", "浮生记", "海来阿木 - 浮生记.wav"),          # 33.6MB -> 保留 flac 40.8MB
    ("胡66", "空空如也", "胡66 - 空空如也.wav"),              # 35.6MB -> 保留 flac 70.9MB
]


def find_singer_dir(singer):
    """找歌手目录（在某个字母目录下）"""
    for letter_dir in TARGET.iterdir():
        if not letter_dir.is_dir():
            continue
        if letter_dir.name.startswith('_') or letter_dir.name == '其他':
            continue
        singer_dir = letter_dir / singer
        if singer_dir.is_dir():
            return singer_dir
    return None


def move_safely(src, backup_singer_dir, log_lines):
    """软删除：移动到 _低音质备份/对应歌手目录"""
    backup_singer_dir.mkdir(parents=True, exist_ok=True)
    dst = backup_singer_dir / src.name
    # 避免覆盖
    i = 0
    while dst.exists():
        i += 1
        dst = backup_singer_dir / f"{src.stem}__{i}{src.suffix}"
    shutil.move(str(src), str(dst))
    size_mb = dst.stat().st_size / 1024 / 1024
    log_lines.append(f"  ✓ {src.relative_to(TARGET)} ({size_mb:.1f}MB) → {dst.relative_to(TARGET)}")
    return dst


def main():
    print(f"=== 音乐库去重（软删除）===")
    print(f"目标：{TARGET}")
    print(f"备份目录：{BACKUP}")
    print(f"日志目录：{LOG_DIR}")
    print()

    # 第一遍：dry-run
    if '--apply' not in sys.argv:
        print("【DRY-RUN 模式】将移动以下 20 个文件到 _低音质备份/：\n")
        total_size = 0
        ok_count = 0
        for singer, song, fname in DUP_LIST:
            singer_dir = find_singer_dir(singer)
            if not singer_dir:
                print(f"  ⚠️  找不到歌手目录: {singer}")
                continue
            src = singer_dir / fname
            if not src.exists():
                print(f"  ⚠️  文件不存在: {src.relative_to(TARGET)}")
                continue
            size_mb = src.stat().st_size / 1024 / 1024
            total_size += size_mb
            ok_count += 1
            print(f"  • {singer} - {song}")
            print(f"    {src.relative_to(TARGET)} ({size_mb:.1f}MB)")
        print(f"\n总结：{ok_count}/{len(DUP_LIST)} 个文件可移动，预计释放 {total_size:.1f}MB")
        print(f"\n加 --apply 参数实际执行")
        return

    # 第二遍：实际执行
    print("【执行模式】开始移动...\n")
    LOG_DIR.mkdir(exist_ok=True)
    log_path = LOG_DIR / '日志.log'
    log_lines = [
        f"音乐库去重日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"策略：保留最大文件，移动其他到 _低音质备份/（软删除）",
        f"",
    ]

    moved = 0
    failed = 0
    for singer, song, fname in DUP_LIST:
        singer_dir = find_singer_dir(singer)
        if not singer_dir:
            log_lines.append(f"❌ 找不到歌手目录: {singer} - {song}")
            failed += 1
            continue
        src = singer_dir / fname
        if not src.exists():
            log_lines.append(f"❌ 文件不存在: {src.relative_to(TARGET)}")
            failed += 1
            continue
        backup_singer = BACKUP / singer_dir.parent.name / singer
        try:
            move_safely(src, backup_singer, log_lines)
            moved += 1
        except Exception as e:
            log_lines.append(f"❌ 移动失败: {src.relative_to(TARGET)}: {e}")
            failed += 1

    log_lines.append(f"\n=== 总结 ===")
    log_lines.append(f"成功: {moved}")
    log_lines.append(f"失败: {failed}")
    log_lines.append(f"脚本：/root/.openclaw/workspace/scripts/dedup_music.py")
    log_lines.append(f"回退方法：手动从 _低音质备份/ 移回原位即可")

    log_text = '\n'.join(log_lines)
    log_path.write_text(log_text, encoding='utf-8')
    print(log_text)
    print(f"\n日志写入：{log_path}")


if __name__ == '__main__':
    main()
