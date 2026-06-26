#!/usr/bin/env python3
"""
OpenClaw 备份脚本
一键备份工作区重要文件
"""

import os
import sys
import zipfile
import hashlib
import shutil
from datetime import datetime
from pathlib import Path

# 配置
WORKSPACE = Path.home() / ".openclaw" / "workspace"
OUTPUT_DIR = Path.home() / "Desktop"  # 默认输出到桌面

# 必选备份内容（相对于 workspace）
REQUIRED_ITEMS = [
    "MEMORY.md",
    "memory",
    "skills",
    "SOUL.md",
    "IDENTITY.md",
    "USER.md",
    "AGENTS.md",
    "TOOLS.md",
    "HEARTBEAT.md",
]

# 可选备份内容
OPTIONAL_ITEMS = {
    "docs": "文档目录",
    "logs": "日志文件",
    "tasks": "任务文件",
    "knowledge": "知识库",
    "BOOTSTRAP.md": "启动配置",
}


def get_file_hash(filepath):
    """计算文件 SHA256 哈希"""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def interactive_select():
    """交互式选择备份内容"""
    print("\n🔐 OpenClaw 备份工具")
    print("=" * 50)
    print("\n🟢 必选内容（始终包含）:")
    for item in REQUIRED_ITEMS:
        exists = "✓" if (WORKSPACE / item).exists() else "✗"
        print(f"  [{exists}] {item}")
    
    print("\n🟡 可选内容（按数字选择，空格分隔，回车确认）:")
    for i, (item, desc) in enumerate(OPTIONAL_ITEMS.items(), 1):
        exists = "✓" if (WORKSPACE / item).exists() else "✗"
        print(f"  [{i}] [{exists}] {item} - {desc}")
    
    print("\n  [a] 全选  [n] 全不选  [q] 退出")
    
    while True:
        choice = input("\n请选择 > ").strip().lower()
        
        if choice == "q":
            sys.exit(0)
        elif choice == "a":
            return list(OPTIONAL_ITEMS.keys())
        elif choice == "n":
            return []
        elif choice == "":
            return []
        else:
            selected = []
            for num in choice.split():
                try:
                    idx = int(num) - 1
                    if 0 <= idx < len(OPTIONAL_ITEMS):
                        selected.append(list(OPTIONAL_ITEMS.keys())[idx])
                except ValueError:
                    pass
            if selected:
                return selected
            print("无效选择，请重新输入")


def create_backup(selected_optional=None):
    """创建备份"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_name = f"openclaw-backup-{timestamp}"
    backup_zip = OUTPUT_DIR / f"{backup_name}.zip"
    
    print(f"\n📦 开始备份 OpenClaw 工作区")
    print(f"📁 工作区：{WORKSPACE}")
    print(f"💾 输出：{backup_zip}")
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 收集要备份的文件
    files_to_backup = []
    manifest_lines = ["OpenClaw Backup Manifest", "=" * 50, f"Created: {datetime.now().isoformat()}", ""]
    
    # 添加必选内容
    manifest_lines.append("🟢 REQUIRED ITEMS:")
    for item in REQUIRED_ITEMS:
        src_path = WORKSPACE / item
        if src_path.exists():
            if src_path.is_file():
                files_to_backup.append((src_path, item))
                file_hash = get_file_hash(src_path)
                manifest_lines.append(f"  [FILE] {item} ({file_hash[:16]}...)")
            else:
                for root, dirs, files in os.walk(src_path):
                    for file in files:
                        file_path = Path(root) / file
                        rel_path = file_path.relative_to(WORKSPACE)
                        files_to_backup.append((file_path, str(rel_path)))
                manifest_lines.append(f"  [DIR]  {item}/")
        else:
            manifest_lines.append(f"  [SKIP] {item} (不存在)")
    
    # 添加可选内容
    if selected_optional:
        manifest_lines.append("\n🟡 OPTIONAL ITEMS:")
        for item in selected_optional:
            src_path = WORKSPACE / item
            if src_path.exists():
                if src_path.is_file():
                    files_to_backup.append((src_path, item))
                    file_hash = get_file_hash(src_path)
                    manifest_lines.append(f"  [FILE] {item} ({file_hash[:16]}...)")
                else:
                    for root, dirs, files in os.walk(src_path):
                        for file in files:
                            file_path = Path(root) / file
                            rel_path = file_path.relative_to(WORKSPACE)
                            files_to_backup.append((file_path, str(rel_path)))
                    manifest_lines.append(f"  [DIR]  {item}/")
            else:
                manifest_lines.append(f"  [SKIP] {item} (不存在)")
    
    print(f"\n📊 共 {len(files_to_backup)} 个文件待备份...")
    
    # 创建压缩包
    with zipfile.ZipFile(backup_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for src_path, arc_name in files_to_backup:
            try:
                zipf.write(src_path, f"{backup_name}/{arc_name}")
            except Exception as e:
                print(f"⚠️  备份失败 {arc_name}: {e}")
    
    # 添加清单文件
    manifest_content = "\n".join(manifest_lines)
    with zipfile.ZipFile(backup_zip, "a") as zipf:
        zipf.writestr(f"{backup_name}/BACKUP_MANIFEST.txt", manifest_content)
    
    # 计算备份文件哈希
    backup_hash = get_file_hash(backup_zip)
    
    print(f"\n✅ 备份完成!")
    print(f"📦 文件：{backup_zip}")
    print(f"🔐 SHA256: {backup_hash}")
    print(f"📄 包含清单：BACKUP_MANIFEST.txt")
    
    return backup_zip, backup_hash


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 备份工具")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互式选择备份内容")
    parser.add_argument("--output", "-o", type=str, help="输出目录路径")
    parser.add_argument("--required-only", "-r", action="store_true", help="仅备份必选内容")
    
    args = parser.parse_args()
    
    if args.output:
        global OUTPUT_DIR
        OUTPUT_DIR = Path(args.output)
    
    if args.required_only:
        selected = []
        print("\n🟢 快速备份模式：仅备份必选内容")
    else:
        # 默认：交互式选择
        selected = interactive_select()
    
    create_backup(selected)


if __name__ == "__main__":
    main()
