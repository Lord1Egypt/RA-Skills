#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理空目录（v2: 真正软删除，移到 _已删除_时间戳/）
不复用上次的脚本，因为上次描述和实际不一致。
"""
import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

TARGET = Path('/volume4/media2/音乐_整理')
TS = datetime.now().strftime('%Y%m%d_%H%M%S')
TRASH_BASE = TARGET / f'_已删除_空目录_{TS}'
LOG_PATH = TARGET / f'_已删除_空目录_{TS}.log'


def main():
    print(f"=== 空目录清理（真软删除）===")
    print(f"目标: {TARGET}")
    print(f"软删除位置: {TRASH_BASE}/")
    print(f"日志: {LOG_PATH}")
    print()

    # 跳过一些系统/隐藏目录
    skip_prefixes = ('_', '.')

    # 收集所有空目录
    empty_dirs = []
    for root, dirs, files in os.walk(TARGET, topdown=False):
        rel = Path(root).relative_to(TARGET)
        if any(part.startswith(skip_prefixes) for part in rel.parts):
            continue
        if root == str(TARGET):
            continue
        if not dirs and not files:
            empty_dirs.append(Path(root))

    print(f"扫描到空目录: {len(empty_dirs)} 个")

    if len(empty_dirs) == 0:
        print("✅ 没有空目录，无需清理")
        return

    # 按顶层字母分类
    by_letter = {}
    for d in empty_dirs:
        rel = str(d.relative_to(TARGET))
        letter = rel.split('/')[0] if '/' in rel else rel
        by_letter.setdefault(letter, []).append(d)

    print(f"分布在 {len(by_letter)} 个顶层目录下")
    if '--apply' not in sys.argv:
        for letter in sorted(by_letter.keys()):
            print(f"  {letter}: {len(by_letter[letter])} 个空目录")
        print(f"\n加 --apply 参数实际执行（软删除到 {TRASH_BASE}/）")
        return

    # 实际执行：软删除到 _已删除_空目录_时间戳/
    TRASH_BASE.mkdir(exist_ok=True)
    moved = 0
    failed = 0
    log_lines = [
        f"空目录清理日志 v2（真软删除）- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"目标: {TARGET}",
        f"策略: mv 空目录到 {TRASH_BASE}/（软删除，可恢复）",
        f"",
    ]

    # 深度优先：先处理深层
    for d in sorted(empty_dirs, key=lambda x: -len(x.parts)):
        rel = d.relative_to(TARGET)
        try:
            # 在 _已删除_空目录_时间戳/ 下重建相对路径
            trash_dst = TRASH_BASE / rel
            trash_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(d), str(trash_dst))
            moved += 1
            if moved <= 20 or moved % 100 == 0:
                log_lines.append(f"  ✓ {rel}")
        except Exception as e:
            failed += 1
            log_lines.append(f"  ⚠️  失败: {rel} - {e}")

    log_lines.append(f"\n=== 总结 ===")
    log_lines.append(f"成功软删除: {moved}")
    log_lines.append(f"失败: {failed}")
    log_lines.append(f"软删除位置: {TRASH_BASE}/")
    log_lines.append(f"回退方法: 从 {TRASH_BASE}/ 移回原位即可")
    log_lines.append(f"脚本: /root/.openclaw/workspace/scripts/cleanup_empty_dirs_v2.py")

    log_text = '\n'.join(log_lines)
    LOG_PATH.write_text(log_text, encoding='utf-8')
    print(log_text)
    print(f"\n日志: {LOG_PATH}")


if __name__ == '__main__':
    main()