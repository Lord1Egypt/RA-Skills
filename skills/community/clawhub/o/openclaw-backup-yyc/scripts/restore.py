#!/usr/bin/env python3
"""
OpenClaw 数据恢复工具

恢复步骤：
1. 将旧文件夹重命名（添加时间戳后缀）
2. 解压备份文件到原位置
3. 显示恢复结果

使用方法：
    python restore.py                           # 列出备份并让用户选择
    python restore.py --index 3                 # 直接恢复第3个备份
    python restore.py backup.tar.gz             # 恢复指定备份
    python restore.py --confirm backup.tar.gz   # 恢复前确认
    python restore.py --list                    # 仅列出可用备份
"""

import argparse
import os
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path


def find_openclaw_dir():
    """自动检测 OpenClaw 目录"""
    default_path = Path.home() / ".openclaw"
    
    if default_path.exists():
        return default_path
    
    env_path = os.environ.get("OPENCLAW_DIR")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    
    print("❌ 错误：未找到 OpenClaw 目录")
    sys.exit(1)


def get_restore_items():
    """获取需要恢复的项目"""
    return [
        {"name": "workspace", "desc": "工作空间"},
        {"name": "agents", "desc": "多代理配置"},
        {"name": "cron", "desc": "定时任务"},
        {"name": "media", "desc": "媒体缓存"},
    ]


def print_banner():
    """打印横幅"""
    print("\n" + "=" * 60)
    print("📥 OpenClaw 数据恢复工具")
    print("=" * 60 + "\n")


def find_latest_backup(openclaw_dir):
    """查找最新备份"""
    backups = sorted(openclaw_dir.glob("OpenClaw-Backup-YYC-*.tar.gz"), reverse=True)
    return backups[0] if backups else None


def list_available_backups(openclaw_dir, show_table=True):
    """列出可用备份（表格格式）"""
    backups = sorted(openclaw_dir.glob("OpenClaw-Backup-YYC-*.tar.gz"), reverse=True)
    
    if not backups:
        print("❌ 未找到备份文件")
        print("   请将备份文件上传到 ~/.openclaw/ 目录")
        return None
    
    if not show_table:
        return backups
    
    # ANSI 加粗代码
    BOLD = "\033[1m"
    RESET = "\033[0m"
    
    print(f"\n📋 可用备份（共 {len(backups)} 个）：")
    print()
    
    # 表头 - 宽度适配完整文件名（41字符）
    separator = "|------|---------------------------------------------|-----------|--------------------|------------|"
    header = "| 序号 | 备份文件名                                  | 大小      | 时间               | 备注       |"
    print(separator)
    print(f"{BOLD}{header}{RESET}")
    print(separator)
    
    # 表格内容
    for i, backup in enumerate(backups, 1):
        stat = backup.stat()
        size_mb = stat.st_size / 1024 / 1024
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        
        # 文件名完整显示
        name_display = backup.name
        size_str = f"{size_mb:.2f} MB"
        
        # 最新备份加粗
        if i == 1:
            remark = "⭐ 最新"
            row = f"{BOLD}|  {i:>2}  | {name_display:<45} | {size_str:<9} | {mtime:<18} | {remark:<10} |{RESET}"
        else:
            remark = ""
            row = f"|  {i:>2}  | {name_display:<45} | {size_str:<9} | {mtime:<18} | {remark:<10} |"
        print(row)
    
    print(separator)
    print()
    
    return backups


def rename_old_folder(folder_path):
    """重命名旧文件夹"""
    if not folder_path.exists():
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    new_name = f"{folder_path.name}-{timestamp}"
    new_path = folder_path.parent / new_name
    
    print(f"  📁 重命名: {folder_path.name} -> {new_name}")
    folder_path.rename(new_path)
    
    return new_path


def restore(openclaw_dir, backup_file=None, confirm=False, backup_index=None):
    """执行恢复"""
    print_banner()
    print(f"📁 OpenClaw 目录: {openclaw_dir}\n")
    
    # 查找备份文件
    if backup_file:
        backup_path = openclaw_dir / backup_file if not Path(backup_file).is_absolute() else Path(backup_file)
    elif backup_index is not None:
        # 用户指定序号恢复
        backups = list_available_backups(openclaw_dir, show_table=False)
        if not backups:
            return
        if backup_index < 1 or backup_index > len(backups):
            print(f"❌ 无效的序号: {backup_index}，请输入 1-{len(backups)} 之间的数字")
            return
        backup_path = backups[backup_index - 1]
        print(f"📌 已选择备份: {backup_path.name}\n")
    else:
        backups = list_available_backups(openclaw_dir)
        if not backups:
            return
        # 让用户选择序号
        print("请输入序号选择要恢复的备份（直接回车选择最新备份）：")
        try:
            user_input = input("序号: ").strip()
            if user_input == "":
                backup_index = 1
            else:
                backup_index = int(user_input)
            
            if backup_index < 1 or backup_index > len(backups):
                print(f"❌ 无效的序号: {backup_index}，请输入 1-{len(backups)} 之间的数字")
                return
            
            backup_path = backups[backup_index - 1]
            print(f"\n📌 已选择备份: {backup_path.name}\n")
        except ValueError:
            print("❌ 请输入有效的数字序号")
            return
    
    if not backup_path.exists():
        print(f"❌ 备份文件不存在: {backup_path}")
        return
    
    # 确认恢复
    if confirm:
        print(f"⚠️  即将恢复: {backup_path.name}")
        response = input("   确认继续？(y/N): ")
        if response.lower() != "y":
            print("   已取消恢复")
            return
    
    print("=" * 60)
    print("第 1 步：重命名现有文件夹")
    print("=" * 60 + "\n")
    
    items = get_restore_items()
    renamed = {}
    
    for item in items:
        folder_path = openclaw_dir / item["name"]
        if folder_path.exists():
            new_path = rename_old_folder(folder_path)
            if new_path:
                renamed[item["name"]] = new_path
        else:
            print(f"  ⏭️  跳过: {item['name']} (不存在)")
    
    print("\n" + "=" * 60)
    print("第 2 步：解压备份文件")
    print("=" * 60 + "\n")
    
    # 创建临时目录
    temp_dir = openclaw_dir / f".restore-temp-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    temp_dir.mkdir(exist_ok=True)
    
    # 用于存储解压出的配置文件信息
    restored_config_files = []
    
    try:
        # 解压
        print(f"  📦 解压: {backup_path.name}")
        with tarfile.open(backup_path, "r:gz") as tar:
            tar.extractall(temp_dir)
        
        # 恢复文件
        print("\n  恢复文件：")
        
        # 查找 openclaw.json（可能有时间戳后缀）
        # ⚠️ 不覆盖当前的 openclaw.json，改为解压出来保存为带时间戳的文件
        config_files = list(temp_dir.glob("openclaw.json*"))
        restore_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        for cf in config_files:
            if cf.name == "openclaw.json":
                # 备份中的原始配置文件，保存为 openclaw.json.restored-{timestamp}
                dest = openclaw_dir / f"openclaw.json.restored-{restore_timestamp}"
                shutil.copy2(cf, dest)
                restored_config_files.append(dest.name)
                print(f"    📄 {dest.name} (从备份解压，未覆盖当前配置)")
            elif cf.name.startswith("openclaw.json."):
                # 备份中带时间戳的配置文件，保持原时间戳
                dest = openclaw_dir / cf.name
                shutil.copy2(cf, dest)
                restored_config_files.append(dest.name)
                print(f"    📄 {dest.name} (从备份解压)")
        
        # 恢复目录
        for item in items:
            src = temp_dir / item["name"]
            dest = openclaw_dir / item["name"]
            if src.exists():
                shutil.copytree(src, dest)
                print(f"    ✅ {item['name']}/")
            else:
                print(f"    ⏭️  {item['name']}/ (备份中不存在)")
        
    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
    
    # 输出结果
    print("\n" + "=" * 60)
    print("✅ 恢复完成！")
    print("=" * 60)
    
    if restored_config_files:
        print("\n📄 配置文件已解压（未覆盖当前配置）：")
        for cf in restored_config_files:
            print(f"   ~/.openclaw/{cf}")
    
    if renamed:
        print("\n📁 旧文件夹已重命名：")
        for name, path in renamed.items():
            print(f"   {path}")
    
    print("\n" + "⚠️ " * 20)
    print("\n【重要提醒】")
    print("1. ⚠️ 当前 openclaw.json 未被覆盖，如需使用备份配置，请手动替换")
    print("2. 请重启 OpenClaw Gateway 使配置生效")
    print("   命令: openclaw gateway restart")
    print("3. 旧文件夹已重命名，确认无误后可手动删除")
    print("4. 如需回滚，可将重命名的文件夹改回原名")
    print("\n" + "⚠️ " * 20 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 数据恢复工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python restore.py                           # 列出备份并让用户选择
  python restore.py --index 3                 # 直接恢复第3个备份
  python restore.py backup.tar.gz             # 恢复指定备份文件
  python restore.py --confirm backup.tar.gz   # 恢复前确认
  python restore.py --list                    # 仅列出可用备份
        """
    )
    parser.add_argument("backup_file", nargs="?", help="备份文件名")
    parser.add_argument("--confirm", "-c", action="store_true", help="恢复前确认")
    parser.add_argument("--list", "-l", action="store_true", help="列出可用备份")
    parser.add_argument("--index", "-i", type=int, help="指定恢复的备份序号")
    
    args = parser.parse_args()
    
    openclaw_dir = find_openclaw_dir()
    
    if args.list:
        list_available_backups(openclaw_dir)
    elif args.index:
        restore(openclaw_dir, backup_index=args.index, confirm=args.confirm)
    else:
        restore(openclaw_dir, args.backup_file, args.confirm)


if __name__ == "__main__":
    main()