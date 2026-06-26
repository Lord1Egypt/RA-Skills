#!/usr/bin/env python3
"""
memory-booster 记忆归档器
扫描 30 天前的日记 → 提取关键条目 → 追加到 MEMORY.md → 删除已归档日记 → 重建语义索引
"""
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")

# 从 config_loader 获取路径
from config_loader import load_config, get_memory_files, get_memory_md_path
MEMORY_DIRS_RAW, CHROMA_DB_DIR = load_config()
MEMORY_DIRS = [Path(d) for d in MEMORY_DIRS_RAW]
MEMORY_MD = Path(get_memory_md_path(MEMORY_DIRS_RAW)) if get_memory_md_path(MEMORY_DIRS_RAW) else None
ARCHIVE_DIR = Path(MEMORY_DIRS_RAW[0]) / "archive" if MEMORY_DIRS_RAW else None

# 要提取的行类型
ENTRY_PATTERNS = {
    "DECISION": re.compile(r"^[-\s]*[\*\-]\s*\*\*DECISION:\*\*", re.IGNORECASE),
    "DATA": re.compile(r"^[-\s]*[\*\-]\s*\*\*DATA:\*\*", re.IGNORECASE),
    "ISSUE": re.compile(r"^[-\s]*[\*\-]\s*\*\*ISSUE:\*\*", re.IGNORECASE),
    "NEXT": re.compile(r"^[-\s]*[\*\-]\s*\*\*NEXT:\*\*", re.IGNORECASE),
    "FILE": re.compile(r"^[-\s]*[\*\-]\s*\*\*FILE:\*\*", re.IGNORECASE),
    "LINK": re.compile(r"^[-\s]*[\*\-]\s*\*\*LINK:\*\*", re.IGNORECASE),
}
# 也匹配无 ** 包裹的简写
LOOSE_PATTERNS = {
    "DECISION": re.compile(r"^\s*[-*]\s*DECISION\s*:", re.IGNORECASE),
    "DATA": re.compile(r"^\s*[-*]\s*DATA\s*:", re.IGNORECASE),
    "ISSUE": re.compile(r"^\s*[-*]\s*ISSUE\s*:", re.IGNORECASE),
    "NEXT": re.compile(r"^\s*[-*]\s*NEXT\s*:", re.IGNORECASE),
}


def find_archivable_diary(cutoff_date):
    """返回需要归档的日记文件列表"""
    archivable = []
    for mem_dir in MEMORY_DIRS:
        if not mem_dir.is_dir():
            continue
        for fpath in mem_dir.iterdir():
            if not fpath.name.endswith(".md"):
                continue
            if fpath.name == "MEMORY.md":
                continue
            # 尝试从文件名解析日期
            try:
                fdate = datetime.strptime(fpath.name.replace(".md", ""), "%Y-%m-%d")
                if fdate < cutoff_date:
                    archivable.append(fpath)
            except ValueError:
                continue
    return sorted(set(archivable))


def extract_entries(fpath):
    """从日记中提取关键条目"""
    entries = {k: [] for k in ENTRY_PATTERNS}
    try:
        with open(fpath, "r") as f:
            lines = f.readlines()
    except Exception:
        return entries

    current_section = None
    for line in lines:
        line_stripped = line.strip()
        matched = False
        for key, pat in ENTRY_PATTERNS.items():
            if pat.search(line_stripped):
                entries[key].append(line_stripped)
                matched = True
                break
        if not matched:
            for key, pat in LOOSE_PATTERNS.items():
                if pat.search(line_stripped):
                    entries[key].append(line_stripped)
                    break
    return entries


def append_to_memory(section_title, entries_by_type, source_file):
    """把归档条目追加到 MEMORY.md 对应段落"""
    if not MEMORY_MD.exists():
        print(f"  ⚠️  MEMORY.md 不存在，跳过写入")
        return False

    # 读取文件
    with open(MEMORY_MD, "r") as f:
        lines = f.readlines()

    # 找段落位置
    insert_idx, end_idx = find_section_in_memory(section_title, lines)
    if insert_idx is None:
        # 段落不存在，追加到文件末尾
        with open(MEMORY_MD, "a") as f:
            f.write(f"\n{section_title}\n")
            f.write(f"（归档自 {source_file}，{datetime.now().strftime('%Y-%m-%d')}）\n\n")
            for key in ["DECISION", "DATA", "NEXT", "ISSUE", "FILE", "LINK"]:
                for entry in entries_by_type.get(key, []):
                    f.write(f"- {entry}\n")
            f.write("\n")
        print(f"  ✅ 新增段落 {section_title} 到 MEMORY.md")
        return True

    # 插入到段落末尾（下一个 ## 之前）
    new_lines = []
    new_lines.append(f"\n# 归档自 {source_file}（{datetime.now().strftime('%Y-%m-%d')}）\n")
    for key in ["DECISION", "DATA", "NEXT", "ISSUE", "FILE", "LINK"]:
        for entry in entries_by_type.get(key, []):
            new_lines.append(f"- {entry}\n")

    if new_lines:
        # 在 end_idx 之前插入
        before = lines[:insert_idx + 1]
        after = lines[end_idx:] if end_idx else []
        final = before + ["\n"] + new_lines + ["\n"] + after
        with open(MEMORY_MD, "w") as f:
            f.writelines(final)
        print(f"  ✅ 追加到 {section_title}")
        return True

    print(f"  ⚠️  段落存在但无内容可追加")
    return False


def find_section_in_memory(section_title, lines):
    """在 MEMORY.md 行列表中找到 ## 或 ### 段落的插入位置"""
    for i, line in enumerate(lines):
        if line.strip() == section_title:
            # 找下一个 ##/### 或文件结尾
            for j in range(i + 1, len(lines)):
                if lines[j].startswith("##") and j != i:
                    return i, j
            return i, len(lines)
    return None, None


def rebuild_index():
    """重建语义索引"""
    print("\n🔄 重建语义索引...")
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "index_memory.py"), "--force"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            print("  ✅ 索引重建完成")
            return True
        else:
            print(f"  ⚠️  索引重建失败: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ⚠️  索引重建异常: {e}")
        return False


def archive(cutoff_days=30, dry_run=False):
    cutoff = datetime.now() - timedelta(days=cutoff_days)
    print(f"📦 记忆归档开始")
    print(f"   截止日期: {cutoff.strftime('%Y-%m-%d')}（{cutoff_days} 天前）")
    print(f"   模式: {'模拟运行（不修改文件）' if dry_run else '正式归档'}\n")

    archivable = find_archivable_diary(cutoff)
    if not archivable:
        print("✅ 没有需要归档的日记")
        return

    print(f"📋 找到 {len(archivable)} 个日记文件需要归档:\n")
    for f in archivable:
        print(f"   - {f.name}  ({f.parent.name})")
    print()

    if dry_run:
        print("💡 使用 archive_memory.py --exec 正式执行归档")
        return

    confirm = input("确认归档以上文件？(y/N): ")
    if confirm.lower() != "y":
        print("❌ 已取消")
        return

    # 创建归档备份目录
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    archived = []
    extracted_count = 0

    for fpath in archivable:
        print(f"\n📝 处理: {fpath.name}")
        entries = extract_entries(fpath)

        total = sum(len(v) for v in entries.values())
        if total == 0:
            print(f"  ⚠️  未找到关键条目，跳过归档")
            continue

        print(f"  📊 提取: DECISION×{len(entries['DECISION'])} DATA×{len(entries['DATA'])} "
              f"NEXT×{len(entries['NEXT'])} ISSUE×{len(entries['ISSUE'])}")

        # 追加到 MEMORY.md（按日期归类到对应段落）
        # 简化策略：追加到 MEMORY.md 末尾的「归档」段落
        section = "## 归档记忆"
        ok = append_to_memory(section, entries, fpath.name)
        if ok:
            extracted_count += total

            # 备份后删除
            backup_path = ARCHIVE_DIR / fpath.name
            import shutil
            shutil.copy2(fpath, backup_path)
            fpath.unlink()
            archived.append(fpath.name)
            print(f"  ✅ 已归档 + 备份到 {backup_path}")

    print(f"\n📊 归档完成:")
    print(f"   - 处理文件: {len(archived)} 个")
    print(f"   - 提取条目: {extracted_count} 条")
    print(f"   - 备份位置: {ARCHIVE_DIR}")

    # 重建索引
    if archived:
        rebuild_index()

    print(f"\n✅ 归档完成！")


if __name__ == "__main__":
    dry = "--dry" in sys.argv or "-n" in sys.argv
    exec_mode = "--exec" in sys.argv
    if not exec_mode and not dry:
        print("用法:")
        print("  --dry     模拟运行，不修改文件")
        print("  --exec    正式执行归档")
        print()
        print("建议先运行: archive_memory.py --dry")
        sys.exit(0)
    archive(dry_run=dry)
