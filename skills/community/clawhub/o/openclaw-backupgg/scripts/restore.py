#!/usr/bin/env python3
"""
OpenClaw 恢复脚本
从备份压缩包恢复工作区
"""

import os
import sys
import zipfile
from pathlib import Path
from datetime import datetime

WORKSPACE = Path.home() / ".openclaw" / "workspace"


def restore_backup(backup_path, dry_run=False):
    """从备份恢复"""
    backup_path = Path(backup_path).expanduser()
    
    if not backup_path.exists():
        print(f"❌ 备份文件不存在：{backup_path}")
        sys.exit(1)
    
    if not backup_path.suffix == ".zip":
        print(f"❌ 不是有效的 ZIP 文件：{backup_path}")
        sys.exit(1)
    
    print(f"\n🔄 准备恢复 OpenClaw 工作区")
    print(f"📦 备份文件：{backup_path}")
    print(f"📁 目标位置：{WORKSPACE}")
    
    if dry_run:
        print("\n🔍 预览备份内容:")
        with zipfile.ZipFile(backup_path, "r") as zipf:
            for name in zipf.namelist()[:20]:
                print(f"  {name}")
            if len(zipf.namelist()) > 20:
                print(f"  ... 共 {len(zipf.namelist())} 个文件")
        return
    
    # 确认恢复
    print("\n⚠️  恢复操作将覆盖现有文件!")
    confirm = input("确认恢复？[y/N] > ").strip().lower()
    if confirm != "y":
        print("已取消")
        sys.exit(0)
    
    # 确保工作区存在
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    
    restored_count = 0
    with zipfile.ZipFile(backup_path, "r") as zipf:
        # 找到根目录
        names = zipf.namelist()
        root_dir = names[0].split("/")[0] if names else ""
        
        for name in names:
            if name.endswith("/"):
                continue
            
            # 跳过根目录前缀
            rel_path = name[len(root_dir) + 1:] if root_dir else name
            
            # 跳过清单文件
            if rel_path == "BACKUP_MANIFEST.txt":
                continue
            
            # 🔒 安全修复：防止 ZipSlip 攻击
            # 检查路径是否包含 ".." 或绝对路径
            if ".." in rel_path or rel_path.startswith("/"):
                print(f"  ⚠️  跳过可疑路径：{rel_path}")
                continue
            
            # 确保目标路径在工作区内
            target_path = (WORKSPACE / rel_path).resolve()
            if not str(target_path).startswith(str(WORKSPACE.resolve())):
                print(f"  ⚠️  跳过路径穿越攻击：{rel_path}")
                continue
            
            # 创建父目录
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 解压文件
            with zipf.open(name) as src:
                with open(target_path, "wb") as dst:
                    dst.write(src.read())
            
            restored_count += 1
            print(f"  ✓ {rel_path}")
    
    print(f"\n✅ 恢复完成! 共恢复 {restored_count} 个文件")
    print(f"📁 工作区：{WORKSPACE}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OpenClaw 恢复工具")
    parser.add_argument("backup", nargs="?", help="备份文件路径")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览备份内容")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用备份")
    
    args = parser.parse_args()
    
    if args.list:
        # 列出桌面备份文件
        desktop = Path.home() / "Desktop"
        backups = list(desktop.glob("openclaw-backup-*.zip"))
        if backups:
            print("\n📦 可用备份:")
            for b in sorted(backups, reverse=True)[:10]:
                stat = b.stat()
                size = stat.st_size / 1024 / 1024
                mtime = datetime.fromtimestamp(stat.st_mtime)
                print(f"  {b.name} ({size:.1f} MB) - {mtime.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("未找到备份文件")
        return
    
    if not args.backup:
        # 找最新的备份
        desktop = Path.home() / "Desktop"
        backups = sorted(desktop.glob("openclaw-backup-*.zip"), reverse=True)
        if backups:
            args.backup = str(backups[0])
            print(f"使用最新备份：{args.backup}")
        else:
            print("❌ 未指定备份文件，也未找到可用备份")
            sys.exit(1)
    
    restore_backup(args.backup, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
