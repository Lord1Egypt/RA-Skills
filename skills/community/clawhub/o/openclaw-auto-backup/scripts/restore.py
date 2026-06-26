#!/usr/bin/env python3
"""
Auto Backup - Restore Script
恢复备份的配置文件

Usage: python3 restore.py --version backup-20260310-195545 [--dry-run]

Security: 防止 ZipSlip 路径遍历攻击
"""

import json
import os
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
WORKSPACE = Path.home() / ".openclaw" / "workspace"
BACKUP_DIR = Path.home() / ".openclaw" / "backups"
CONFIG_FILE = SCRIPT_DIR / "../config/backup-config.json"

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def load_config():
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        log_error(f"配置文件不存在：{CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_backups():
    """列出所有备份"""
    if not BACKUP_DIR.exists():
        return []
    
    backups = []
    for f in BACKUP_DIR.glob("backup-*.tar.gz"):
        stat = f.stat()
        backups.append({
            'name': f.name,
            'path': f,
            'size': stat.st_size,
            'mtime': datetime.fromtimestamp(stat.st_mtime)
        })
    
    return sorted(backups, key=lambda x: x['mtime'], reverse=True)

def is_safe_path(base_path: Path, target_path: Path) -> bool:
    """
    检查目标路径是否安全（防止 ZipSlip 攻击）
    
    Security: 确保提取的文件不会跳出目标目录
    """
    try:
        # 解析绝对路径
        base_resolved = base_path.resolve()
        target_resolved = target_path.resolve()
        
        # 检查目标路径是否在基础路径内
        return str(target_resolved).startswith(str(base_resolved))
    except Exception:
        return False

def safe_extract(tar: tarfile.TarFile, dest_path: Path) -> list:
    """
    安全提取 tar 文件（防止 ZipSlip 攻击）
    
    Security:
    1. 验证每个成员的路径
    2. 跳过绝对路径和包含 .. 的路径
    3. 确保提取后路径在目标目录内
    """
    extracted = []
    
    for member in tar.getmembers():
        member_path = dest_path / member.name
        
        # 安全检查 1: 跳过绝对路径
        if os.path.isabs(member.name):
            log_warning(f"跳过绝对路径：{member.name}")
            continue
        
        # 安全检查 2: 跳过包含 .. 的路径
        if '..' in member.name:
            log_warning(f"跳过危险路径：{member.name}")
            continue
        
        # 安全检查 3: 验证解析后的路径
        if not is_safe_path(dest_path, member_path):
            log_warning(f"跳过不安全路径：{member.name}")
            continue
        
        # 安全检查 4: 跳过符号链接（防止链接到外部文件）
        if member.issym() or member.islnk():
            log_warning(f"跳过符号链接：{member.name}")
            continue
        
        # 安全提取
        try:
            tar.extract(member, dest_path)
            extracted.append(member.name)
        except Exception as e:
            log_error(f"提取失败 {member.name}: {e}")
    
    return extracted

def restore_backup(version: str, dry_run: bool = False):
    """恢复指定版本的备份"""
    backup_file = BACKUP_DIR / version
    
    # 验证备份文件
    if not backup_file.exists():
        log_error(f"备份文件不存在：{backup_file}")
        log_info("可用备份：")
        backups = list_backups()
        for b in backups[:10]:
            print(f"  - {b['name']} ({b['mtime'].strftime('%Y-%m-%d %H:%M')})")
        sys.exit(1)
    
    if not tarfile.is_tarfile(backup_file):
        log_error(f"无效的备份文件：{backup_file}")
        sys.exit(1)
    
    log_info(f"准备恢复备份：{version}")
    
    if dry_run:
        log_warning("[模拟运行] 不实际恢复")
        with tarfile.open(backup_file, 'r:gz') as tar:
            members = tar.getnames()
            log_info(f"备份包含 {len(members)} 个文件：")
            for m in members[:20]:
                print(f"  - {m}")
            if len(members) > 20:
                print(f"  ... 还有 {len(members) - 20} 个文件")
        return
    
    # 创建临时目录
    temp_dir = BACKUP_DIR / f".restore-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # 安全解压备份
        log_info("解压备份文件...")
        with tarfile.open(backup_file, 'r:gz') as tar:
            extracted = safe_extract(tar, temp_dir)
            log_info(f"安全提取 {len(extracted)} 个文件")
        
        # 读取清单（修复：使用 manifest.json 而非 backup-manifest.json）
        manifest_file = temp_dir / "manifest.json"
        if not manifest_file.exists():
            log_error("备份清单不存在 (manifest.json)")
            sys.exit(1)
        
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # 恢复文件
        log_info(f"恢复 {manifest.get('fileCount', len(manifest.get('files', [])))} 个文件...")
        restored = 0
        
        for file_info in manifest.get('files', []):
            # 处理路径（支持相对路径）
            if isinstance(file_info, str):
                rel_path = file_info
            else:
                rel_path = file_info.get('path', file_info.get('name', ''))
            
            # 安全检查：确保路径不包含 ..
            if '..' in rel_path or os.path.isabs(rel_path):
                log_warning(f"跳过不安全路径：{rel_path}")
                continue
            
            src = temp_dir / rel_path
            dst = WORKSPACE / rel_path
            
            if src.exists():
                # 备份当前版本
                if dst.exists():
                    backup_current = dst.with_suffix(f".backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}")
                    backup_current.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dst, backup_current)
                    log_info(f"已备份当前版本：{backup_current.name}")
                
                # 恢复文件
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                log_success(f"已恢复：{rel_path}")
                restored += 1
            else:
                log_warning(f"文件不存在，跳过：{rel_path}")
        
        log_success(f"恢复完成！共恢复 {restored}/{manifest.get('fileCount', len(manifest.get('files', [])))} 个文件")
        log_warning("建议重启 OpenClaw 网关以应用恢复的配置")
        
    except Exception as e:
        log_error(f"恢复失败：{e}")
        raise
    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            log_info("已清理临时文件")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='恢复 Auto Backup 备份')
    parser.add_argument('--version', required=True, help='要恢复的备份版本 (如：backup-20260310-195545)')
    parser.add_argument('--dry-run', action='store_true', help='模拟运行，不实际恢复')
    parser.add_argument('--list', action='store_true', help='列出所有可用备份')
    
    args = parser.parse_args()
    
    if args.list:
        log_info("可用备份：")
        backups = list_backups()
        if not backups:
            log_warning("没有找到备份")
            return
        
        for i, b in enumerate(backups, 1):
            size_kb = b['size'] / 1024
            mtime = b['mtime'].strftime('%Y-%m-%d %H:%M')
            marker = " ← 当前选择" if b['name'] == args.version else ""
            print(f"{i:2d}. {b['name']:<40} {size_kb:>8.1f} KB  {mtime}{marker}")
        return
    
    restore_backup(args.version, args.dry_run)

if __name__ == "__main__":
    main()
