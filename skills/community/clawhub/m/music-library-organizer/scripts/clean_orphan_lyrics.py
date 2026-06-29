#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理孤儿歌词（有 .lrc 没有同目录音频）
- 真软删除：mv 到 _已删除_孤儿歌词_时间戳/
- 然后检查空目录，删除（也是软删除）
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

TARGET = Path('/volume4/media2/音乐')
AUDIO_EXTS = {'.mp3', '.flac', '.wav', '.m4a', '.ogg', '.ape'}
TS = datetime.now().strftime('%Y%m%d_%H%M%S')
TRASH_BASE = Path(f'/volume4/media2/_trash_orphan_lyrics_{TS}')
LOG_PATH = Path(f'/volume4/media2/_trash_orphan_lyrics_{TS}.log')


def scan_orphans():
    """扫描孤儿歌词目录（有.lrc没音频）"""
    orphan_dirs = {}
    for root, dirs, files in os.walk(TARGET):
        rel = Path(root).relative_to(TARGET)
        if any(p.startswith('_') or p.startswith('.') for p in rel.parts):
            continue
        if root == str(TARGET):
            continue
        audio_files = [f for f in files if Path(f).suffix.lower() in AUDIO_EXTS]
        lrc_files = [f for f in files if f.lower().endswith('.lrc')]
        if lrc_files and not audio_files:
            orphan_dirs[Path(root)] = lrc_files
    return orphan_dirs


def main():
    print(f"=== 孤儿歌词清理 ===")
    print(f"目标: {TARGET}")
    print(f"软删除位置: {TRASH_BASE}/")
    print(f"日志: {LOG_PATH}")
    print()

    orphan_dirs = scan_orphans()
    total_lrc = sum(len(v) for v in orphan_dirs.values())
    print(f"孤儿歌词: {total_lrc} 个 ({len(orphan_dirs)} 个目录)")
    print(f"预计节省空间: ~{total_lrc * 4 / 1024:.1f} MB（按平均 4KB/歌词估算）")

    if total_lrc == 0:
        print("✅ 没有孤儿歌词，无需清理")
        return

    # 抽样
    print("\n前 5 个样本：")
    for d, files in list(orphan_dirs.items())[:5]:
        rel = d.relative_to(TARGET)
        print(f"  📁 {rel}/ ({len(files)} 个 .lrc)")

    if '--apply' not in sys.argv:
        print(f"\n加 --apply 参数实际执行（mv 到 {TRASH_BASE}/）")
        return

    # 实际执行
    TRASH_BASE.mkdir(exist_ok=True)
    moved_lrc = 0
    failed = 0
    log_lines = [
        f"孤儿歌词清理日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"目标: {TARGET}",
        f"策略: mv 歌词到 {TRASH_BASE}/（软删除，可恢复）",
        f"",
    ]

    # 移动所有孤儿歌词到 TRASH_BASE
    for d, files in orphan_dirs.items():
        rel = d.relative_to(TARGET)
        for f in files:
            src = d / f
            # 在 TRASH_BASE 下保持目录结构
            dst = TRASH_BASE / rel / f
            try:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                moved_lrc += 1
            except Exception as e:
                failed += 1
                log_lines.append(f"  ❌ 失败: {src.relative_to(TARGET)} - {e}")

    log_lines.append(f"\n=== 歌词清理阶段 ===")
    log_lines.append(f"成功移动: {moved_lrc}/{total_lrc}")
    log_lines.append(f"失败: {failed}")

    # 第二步：清理空目录
    print(f"\n=== 第二步：清理空目录 ===")
    empty_dirs = []
    for root, dirs, files in os.walk(TARGET, topdown=False):
        rel = Path(root).relative_to(TARGET)
        if any(p.startswith('_') or p.startswith('.') for p in rel.parts):
            continue
        if root == str(TARGET):
            continue
        if not dirs and not files:
            empty_dirs.append(Path(root))

    log_lines.append(f"\n=== 空目录清理阶段 ===")
    log_lines.append(f"扫描到空目录: {len(empty_dirs)} 个")

    moved_dir = 0
    for d in sorted(empty_dirs, key=lambda x: -len(x.parts)):
        rel = d.relative_to(TARGET)
        try:
            trash_dst = TRASH_BASE / rel
            trash_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(trash_dst))
            moved_dir += 1
            if moved_dir <= 5 or moved_dir % 100 == 0:
                log_lines.append(f"  ✓ 空目录: {rel}")
        except Exception as e:
            log_lines.append(f"  ⚠️  跳过: {rel} - {e}")

    log_lines.append(f"\n=== 总结 ===")
    log_lines.append(f"歌词移动: {moved_lrc}/{total_lrc}")
    log_lines.append(f"空目录移动: {moved_dir}/{len(empty_dirs)}")
    log_lines.append(f"软删除位置: {TRASH_BASE}/")
    log_lines.append(f"回退: 从 {TRASH_BASE}/ 移回原位即可")

    log_text = '\n'.join(log_lines)
    LOG_PATH.write_text(log_text, encoding='utf-8')
    print(log_text)
    print(f"\n日志: {LOG_PATH}")


if __name__ == '__main__':
    main()