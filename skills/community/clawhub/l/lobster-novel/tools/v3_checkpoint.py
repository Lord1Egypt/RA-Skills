#!/usr/bin/env python3
"""
V3 进度检查器 —— 每次开始写新章前运行此脚本

功能：
1. 检查当前章节数，判断是否需要做批次LLM质控
2. 输出批次的改进清单（P1项）
3. 更新进度文件

用法：
  python3 tools/v3_checkpoint.py
"""
import sys, os, json
from pathlib import Path

NOVEL_DIR = Path(os.environ.get("NOVEL_DIR", "."))
TRACK_FILE = NOVEL_DIR / "continuity" / "v3_track.md"
CHAPTER_DIR = NOVEL_DIR / "chapters" / "volume_03"
BATCH_SIZE = 10

def count_v3_chapters():
    """统计已写的V3章节数"""
    if not CHAPTER_DIR.exists():
        return 0
    return len(list(CHAPTER_DIR.glob("Ch*.md")))

def parse_track():
    """解析跟踪文件"""
    if not TRACK_FILE.exists():
        return {"current_batch": 0, "last_batch_reviewed": 0}
    
    text = TRACK_FILE.read_text(encoding="utf-8")
    data = {}
    for line in text.split("\n"):
        if ":" in line and not line.strip().startswith("-"):
            key, val = line.split(":", 1)
            data[key.strip()] = val.strip()
    
    return {
        "current_batch": int(data.get("current_batch", "0")),
        "last_batch_reviewed": int(data.get("last_batch_reviewed", "0")),
        "chapter_count": int(data.get("chapter_count", "0")),
    }

def main():
    chapter_count = count_v3_chapters()
    track = parse_track()
    current_batch = (chapter_count // BATCH_SIZE) + (1 if chapter_count % BATCH_SIZE > 0 else 0)
    
    print(f"📊 V3 进度检查")
    print(f"  已写章节: {chapter_count}")
    print(f"  当前批次: 批{current_batch}")
    print(f"  上次LLM审查: 批{track['last_batch_reviewed']}")
    print()
    
    # 判断是否需要做批次审查
    if chapter_count > 0 and chapter_count % BATCH_SIZE == 0 and track["last_batch_reviewed"] < current_batch:
        print("⚠️  ⚠️  ⚠️  需要执行 LLM 批次质控！ ⚠️  ⚠️  ⚠️")
        print(f"  已写满 {BATCH_SIZE} 章（批{current_batch}），但上次审查是批{track['last_batch_reviewed']}")
        print(f"  → 请先跑 LLM 批次审查，再继续写下一章")
        print()
        print("  审查完成后，更新 v3_track.md：")
        print(f"    last_batch_reviewed: {current_batch}")
        sys.exit(1)
    
    # 正常——可以继续写
    if chapter_count % BATCH_SIZE == 0 and chapter_count > 0:
        print(f"✅ 批{current_batch} 已通过LLM审查，可以继续")
    else:
        next_batch_start = (chapter_count // BATCH_SIZE) * BATCH_SIZE + 1
        next_batch_end = next_batch_start + BATCH_SIZE - 1
        remaining = BATCH_SIZE - (chapter_count % BATCH_SIZE)
        print(f"✅ 可以继续写（批{current_batch}，还剩{remaining}章到批审查）")
        print(f"  当前进度: Ch{chapter_count:03d} / 目标: Ch{next_batch_end:03d}")
    
    # 输出当前批次改进清单
    track_text = TRACK_FILE.read_text(encoding="utf-8") if TRACK_FILE.exists() else ""
    if f"批{current_batch}（Ch" in track_text:
        start = track_text.find(f"批{current_batch}（Ch")
        end = track_text.find("\n##", start)
        if end == -1:
            end = len(track_text)
        print(f"\n📋 批{current_batch} 改进清单:")
        print(track_text[start:end])
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
