#!/usr/bin/env python3
"""
Memory Files Compact Script
用于 heartbeat 定期执行：
1. 备份 memory/*.md 内容到 memory-indexer
2. 精简原 .md 文件到合理大小

用法：
    python3 memory_compact.py [--memory-dir PATH] [--indexer-dir PATH] [--max-size KB]

选项：
    --memory-dir PATH   Memory 文件目录 (默认: ~/.openclaw/workspace/memory)
    --indexer-dir PATH  memory-indexer 目录 (默认: ~/.openclaw/workspace/skills/memory-indexer)
    --max-size KB      精简后最大 KB 数 (默认: 10)
"""

import os
import sys
import argparse
from pathlib import Path

# 默认配置
DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
DEFAULT_INDEXER_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "memory-indexer"
DEFAULT_MAX_SIZE_KB = 10


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Memory Files Compact - 备份并精简 Memory 文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 memory_compact.py                           # 使用默认配置
    python3 memory_compact.py --max-size 20            # 精简后最大 20KB
    python3 memory_compact.py --memory-dir /path/to/memory
    python3 memory_compact.py --indexer-dir /path/to/indexer --max-size 15
        """
    )
    parser.add_argument(
        "--memory-dir", "-m",
        type=Path,
        default=DEFAULT_MEMORY_DIR,
        help=f"Memory 文件目录 (默认: {DEFAULT_MEMORY_DIR})"
    )
    parser.add_argument(
        "--indexer-dir", "-i",
        type=Path,
        default=DEFAULT_INDEXER_DIR,
        help=f"memory-indexer 目录 (默认: {DEFAULT_INDEXER_DIR})"
    )
    parser.add_argument(
        "--auto-snapshot", "-a",
        action="store_true",
        help="在精简前自动创建快照"
    )
    parser.add_argument(
        "--max-size", "-M",
        type=int,
        default=DEFAULT_MAX_SIZE_KB,
        help=f"精简后最大 KB 数 (默认: {DEFAULT_MAX_SIZE_KB})"
    )
    return parser.parse_args()


# 解析命令行参数获取配置
args = parse_args()
MEMORY_DIR = args.memory_dir
MEMORY_INDEXER_DIR = args.indexer_dir
MAX_SIZE_KB = args.max_size


def extract_key_sections(content):
    """提取关键段落，保留标题和摘要"""
    lines = content.split('\n')
    kept_lines = []
    
    # 保留前 100 行或前 5KB
    kept_lines = lines[:150]
    kept_content = '\n'.join(kept_lines)
    
    # 如果原文件更长，添加截断标记
    if len(content) > MAX_SIZE_KB * 1024:
        kept_content += f"\n\n> ... (原始文件 {len(content)} 字符，已精简)"
    
    return kept_content


def compact_memory_file(md_path, max_size_kb=MAX_SIZE_KB):
    """精简 memory .md 文件"""
    file_size = md_path.stat().st_size
    max_bytes = max_size_kb * 1024
    
    if file_size <= max_bytes:
        print(f"  ✓ {md_path.name} already small ({file_size / 1024:.1f}KB)")
        return False
    
    # 读取内容
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取关键部分
    kept_content = extract_key_sections(content)
    
    # 写回
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(kept_content)
    
    new_size = len(kept_content.encode('utf-8'))
    print(f"  ✓ Compacted {md_path.name}: {file_size / 1024:.1f}KB -> {new_size / 1024:.1f}KB")
    return True


def backup_to_indexer(md_path):
    """将 memory 文件添加到 memory-indexer"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if len(content) < 100:
        return
    
    # 调用 memory-indexer add
    import subprocess
    cmd = [
        sys.executable,
        str(MEMORY_INDEXER_DIR / "memory-indexer.py"),
        "add",
        content,
        "memory-backup",
        md_path.stem,
        "--keywords", "15"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"  ✓ Indexed: {md_path.name} ({len(content)} chars)")
        else:
            print(f"  ✗ Indexer error: {result.stderr[:100]}")
    except Exception as e:
        print(f"  ✗ Failed to index: {e}")


def main():
    global MEMORY_DIR, MEMORY_INDEXER_DIR
    
    print("📦 Memory Files Compact")
    print("=" * 40)
    
    # 自动快照：如果指定了 --auto-snapshot 参数
    if hasattr(args, 'auto_snapshot') and args.auto_snapshot:
        print("🔄 自动快照模式：正在创建快照...")
        snapshot_script = MEMORY_INDEXER_DIR / "memory_snapshot.py"
        if snapshot_script.exists():
            import subprocess
            result = subprocess.run(
                ["python3", str(snapshot_script), "create", "auto_compact"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("  ✅ 快照已创建")
            else:
                print(f"  ⚠️ 快照创建失败: {result.stderr[:100]}")
        else:
            print("  ⚠️ memory_snapshot.py 不存在，跳过快照")
        print()
    
    # 获取所有 .md 文件
    md_files = sorted(MEMORY_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    print(f"Found {len(md_files)} memory files")
    
    # 只处理较大的文件（超过 5KB）
    large_files = [f for f in md_files if f.stat().st_size > 5 * 1024]
    print(f"Processing {len(large_files)} large files (>5KB)")
    
    for md_file in large_files:
        print(f"\n📄 {md_file.name}")
        
        # 备份到 indexer
        backup_to_indexer(md_file)
        
        # 精简文件
        compact_memory_file(md_file)
    
    print("\n✅ Done!")


if __name__ == "__main__":
    main()
