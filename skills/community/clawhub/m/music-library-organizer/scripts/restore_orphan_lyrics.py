#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
恢复孤儿歌词：从 _trash_orphan_lyrics_20260619_094517/ 移回 /volume4/media2/音乐/
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

TRASH = Path('/volume4/media2/_trash_orphan_lyrics_20260619_094517')
TARGET = Path('/volume4/media2/音乐')
LOG_PATH = Path('/volume4/media2/音乐_整理/_restored_lyrics.log')


def main():
    print(f"=== 恢复孤儿歌词 ===")
    print(f"来源: {TRASH}")
    print(f"目标: {TARGET}")
    print(f"日志: {LOG_PATH}")
    print()

    if not TRASH.exists():
        print(f"❌ 软删除位置不存在: {TRASH}")
        return

    # 扫描所有需要恢复的文件
    files_to_restore = list(TRASH.rglob('*.lrc'))
    dirs_to_restore = [d for d in TRASH.rglob('*') if d.is_dir()]
    print(f"扫描到: {len(files_to_restore)} 个 .lrc, {len(dirs_to_restore)} 个目录")

    if '--apply' not in sys.argv:
        # DRY-RUN: 检查目标位置是否有同名冲突
        conflicts = 0
        for f in files_to_restore:
            rel = f.relative_to(TRASH)
            dst = TARGET / rel
            if dst.exists():
                conflicts += 1
                if conflicts <= 5:
                    print(f"  ⚠️  冲突: {rel} 已存在")
        print(f"\n冲突数: {conflicts}")
        print(f"\n加 --apply 参数实际执行")
        return

    # 实际执行恢复
    moved = 0
    failed = 0
    skipped = 0
    log_lines = [
        f"恢复孤儿歌词日志 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"来源: {TRASH}",
        f"目标: {TARGET}",
        f"",
    ]

    # 先恢复所有 .lrc 文件
    for f in sorted(files_to_restore):
        rel = f.relative_to(TRASH)
        dst = TARGET / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            if dst.exists():
                skipped += 1
                log_lines.append(f"  ⚠️  跳过（已存在）: {rel}")
            else:
                shutil.move(str(f), str(dst))
                moved += 1
        except Exception as e:
            failed += 1
            log_lines.append(f"  ❌ 失败: {rel} - {e}")

    # 清理 _trash 里剩下的空目录
    empty_dirs_removed = 0
    for d in sorted(TRASH.rglob('*'), key=lambda x: -len(x.parts)):
        if d.is_dir():
            try:
                d.rmdir()
                empty_dirs_removed += 1
            except OSError:
                pass  # 非空，跳过

    # 最后尝试移除 TRASH 本身
    if not any(TRASH.iterdir()):
        try:
            TRASH.rmdir()
            log_lines.append(f"\n清理空 trash 目录: {TRASH}")
        except:
            pass

    log_lines.append(f"\n=== 总结 ===")
    log_lines.append(f"成功恢复: {moved}")
    log_lines.append(f"跳过（已存在）: {skipped}")
    log_lines.append(f"失败: {failed}")
    log_lines.append(f"清理空目录: {empty_dirs_removed}")

    log_text = '\n'.join(log_lines)
    LOG_PATH.write_text(log_text, encoding='utf-8')
    print(log_text)
    print(f"\n日志: {LOG_PATH}")


if __name__ == '__main__':
    main()