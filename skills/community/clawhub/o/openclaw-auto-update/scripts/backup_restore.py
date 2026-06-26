#!/usr/bin/env python3
"""
OpenClaw Update - Backup & Recovery Tool
备份与恢复工具 - 防止文件名冲突，支持多平台

v1.1 Fix:
- 只备份必要数据（配置、凭证、工作区）
- 排除运行时文件（browser/, logs/, *.pid, *.lock）
- 使用 rsync 而非 cp（更可靠）
"""

import os
import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

def get_os_type():
    """检测操作系统"""
    if sys.platform == 'darwin':
        return 'macOS'
    elif sys.platform == 'linux':
        return 'Linux'
    elif sys.platform == 'win32':
        return 'Windows'
    else:
        return 'Unknown'

def generate_unique_backup_name():
    """生成唯一的备份名称（防止冲突）"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f".openclaw.backup.{timestamp}.{random_suffix}"

def check_backup_exists(backup_name):
    """检查备份是否已存在"""
    home = Path.home()
    backup_path = home / backup_name
    return backup_path.exists()

def get_existing_backups():
    """获取所有现有备份"""
    home = Path.home()
    backups = []
    for item in home.iterdir():
        if item.name.startswith('.openclaw.backup.'):
            backups.append({
                'name': item.name,
                'path': str(item),
                'created': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            })
    return sorted(backups, key=lambda x: x['created'], reverse=True)

def create_backup(verbose=True):
    """
    创建备份（只备份必要数据）
    
    备份内容：
    - openclaw.json (配置)
    - credentials/ (凭证)
    - workspace/ (工作区)
    
    排除内容：
    - browser/ (Chrome 数据，经常占用)
    - logs/ (正在写入的日志)
    - *.pid, *.lock (进程锁)
    - __pycache__/ (Python 缓存)
    """
    import random
    import string
    
    os_type = get_os_type()
    home = Path.home()
    
    # 生成唯一备份名称
    backup_name = generate_unique_backup_name()
    backup_path = home / backup_name
    
    # 检查是否冲突（红线：禁止覆盖现有备份）
    max_attempts = 10
    attempt = 0
    while check_backup_exists(backup_name) and attempt < max_attempts:
        if verbose:
            print(f"⚠️  Backup name conflict, generating new name... (attempt {attempt + 1}/{max_attempts})")
            print(f"⚠️  备份名称冲突，正在生成新名称... (第 {attempt + 1}/{max_attempts} 次尝试)")
        backup_name = generate_unique_backup_name()
        backup_path = home / backup_name
        attempt += 1
    
    if attempt >= max_attempts:
        print("❌ Failed to generate unique backup name after multiple attempts")
        print("❌ 多次尝试后仍无法生成唯一的备份名称")
        return None
    
    # 定义要备份的目录和文件
    items_to_backup = [
        'openclaw.json',           # 主配置文件
        'credentials/',            # 凭证目录
        'workspace/',              # 工作区
    ]
    
    # 定义排除模式
    exclude_patterns = [
        'browser/',                # Chrome 数据（经常占用）
        'logs/',                   # 日志文件（正在写入）
        '*.pid',                   # 进程锁
        '*.lock',                  # 锁文件
        '__pycache__/',           # Python 缓存
        '*.pyc',                   # Python 编译文件
        '.DS_Store',              # macOS 系统文件
        'node_modules/',          # npm 依赖（太大）
    ]
    
    # 检查源目录
    openclaw_dir = home / '.openclaw'
    if not openclaw_dir.exists():
        print(f"❌ OpenClaw directory not found: {openclaw_dir}")
        print(f"❌ 未找到 OpenClaw 目录：{openclaw_dir}")
        return None
    
    try:
        if verbose:
            print(f"📦 Creating backup... / 正在创建备份...")
            print(f"   Target / 目标：{backup_path}")
            print(f"   Items / 备份内容：{', '.join(items_to_backup)}")
            print(f"   Excluded / 排除内容：{', '.join(exclude_patterns)}")
        
        # 创建目标目录
        backup_path.mkdir(parents=True, exist_ok=True)
        
        if os_type == 'Windows':
            # Windows PowerShell - 逐个复制
            for item in items_to_backup:
                src = openclaw_dir / item
                dst = backup_path / item
                if src.exists():
                    cmd = f'powershell.exe -Command "Copy-Item -Recurse \'{src}\' \'{dst}\'"'
                    subprocess.run(cmd, shell=True, capture_output=True)
        else:
            # macOS / Linux - 使用 rsync
            rsync_cmd = ['rsync', '-av', '--quiet']
            
            # 添加排除规则
            for pattern in exclude_patterns:
                rsync_cmd.extend(['--exclude', pattern])
            
            # 添加要备份的项目
            for item in items_to_backup:
                src = openclaw_dir / item
                if src.exists():
                    rsync_cmd.append(str(src))
            
            # 添加目标
            rsync_cmd.append(str(backup_path) + '/')
            
            # 执行 rsync
            result = subprocess.run(rsync_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"⚠️  rsync warning: {result.stderr}")
        
        # 验证备份
        if backup_path.exists():
            size = get_dir_size(backup_path)
            if verbose:
                print(f"✅ Backup created successfully! / 备份创建成功！")
                print(f"   Location / 位置：{backup_path}")
                print(f"   Size / 大小：{size:.2f} MB")
                print(f"   Note / 注意：只备份了配置、凭证和工作区（排除了 browser/, logs/ 等运行时文件）")
            return str(backup_name)
        else:
            print(f"❌ Backup verification failed")
            print(f"❌ 备份验证失败")
            return None
            
    except Exception as e:
        print(f"❌ Backup error: {e}")
        print(f"❌ 备份错误：{e}")
        # 清理失败的备份
        if backup_path.exists():
            import shutil
            shutil.rmtree(backup_path, ignore_errors=True)
        return None

def get_dir_size(path):
    """获取目录大小（MB）"""
    total = 0
    try:
        for entry in path.rglob('*'):
            if entry.is_file():
                total += entry.stat().st_size
    except:
        pass
    return total / (1024 * 1024)

def list_backups():
    """列出所有备份"""
    backups = get_existing_backups()
    
    if not backups:
        print("📭 No backups found / 未找到备份")
        return []
    
    print(f"\n📦 Available Backups / 可用备份 ({len(backups)}):")
    print("=" * 60)
    for i, backup in enumerate(backups, 1):
        size = get_dir_size(Path(backup['path']))
        print(f"{i}. {backup['name']}")
        print(f"   Created / 创建时间：{backup['created']}")
        print(f"   Size / 大小：{size:.2f} MB")
        print(f"   Path / 路径：{backup['path']}")
        print()
    
    return backups

def restore_backup(backup_name, verbose=True):
    """恢复备份"""
    os_type = get_os_type()
    home = Path.home()
    backup_path = home / backup_name
    openclaw_dir = home / '.openclaw'
    
    if not backup_path.exists():
        print(f"❌ Backup not found: {backup_name}")
        print(f"❌ 备份不存在：{backup_name}")
        return False
    
    try:
        if verbose:
            print(f"🔄 Restoring backup... / 正在恢复备份...")
            print(f"   Source / 源：{backup_path}")
            print(f"   Target / 目标：{openclaw_dir}")
        
        if os_type == 'Windows':
            # Windows PowerShell
            cmd = f'powershell.exe -Command "Copy-Item -Recurse \'{backup_path}/*\' \'{openclaw_dir}/\'"'
        else:
            # macOS / Linux - rsync
            rsync_cmd = ['rsync', '-av', '--quiet', str(backup_path) + '/', str(openclaw_dir) + '/']
            result = subprocess.run(rsync_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"⚠️  rsync warning: {result.stderr}")
        
        if openclaw_dir.exists():
            if verbose:
                print(f"✅ Backup restored successfully! / 备份恢复成功！")
                print(f"   Location / 位置：{openclaw_dir}")
            return True
        else:
            print(f"❌ Restore verification failed")
            print(f"❌ 恢复验证失败")
            return False
            
    except Exception as e:
        print(f"❌ Restore error: {e}")
        print(f"❌ 恢复错误：{e}")
        return False

def print_help():
    """打印帮助信息"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║  OpenClaw Backup & Recovery Tool v1.1                     ║
║  备份与恢复工具                                            ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  Usage / 用法：                                           ║
║  ────────────────                                         ║
║  python3 backup_restore.py [command]                      ║
║                                                           ║
║  Commands / 命令：                                        ║
║  ────────────────                                         ║
║  backup     - Create backup / 创建备份                    ║
║  list       - List backups / 列出备份                     ║
║  restore    - Restore backup / 恢复备份                   ║
║  help       - Show help / 显示帮助                        ║
║                                                           ║
║  Backup Strategy / 备份策略：                             ║
║  ─────────────────────                                    ║
║  ✅ Backs up: openclaw.json, credentials/, workspace/     ║
║  ❌ Excludes: browser/, logs/, *.pid, *.lock, etc.        ║
║                                                           ║
║  Examples / 示例：                                        ║
║  ────────────────                                         ║
║  python3 backup_restore.py backup                         ║
║  python3 backup_restore.py list                           ║
║  python3 backup_restore.py restore .openclaw.backup.xxx   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")

def main():
    if len(sys.argv) < 2:
        print_help()
        return 1
    
    command = sys.argv[1].lower()
    
    if command == 'backup':
        backup_name = create_backup()
        if backup_name:
            print(f"\n✅ Backup created: {backup_name}")
            print(f"✅ 备份已创建：{backup_name}")
            return 0
        return 1
    
    elif command == 'list':
        list_backups()
        return 0
    
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Please specify backup name / 请指定备份名称")
            print("   Usage: python3 backup_restore.py restore <backup_name>")
            return 1
        backup_name = sys.argv[2]
        if restore_backup(backup_name):
            return 0
        return 1
    
    elif command == 'help':
        print_help()
        return 0
    
    else:
        print(f"❌ Unknown command: {command}")
        print(f"❌ 未知命令：{command}")
        print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
