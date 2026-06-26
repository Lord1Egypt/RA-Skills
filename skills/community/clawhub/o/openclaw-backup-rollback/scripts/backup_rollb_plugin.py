#!/usr/bin/env python3
"""
OpenClaw Backup & Rollback 插件
- /backup         : 立即执行备份
- /backup list    : 列出所有备份
- /rollback       : 弹出选择界面
- /backup restore <timestamp>: 还原指定版本
"""
import os
import sys
import json
import tarfile
import subprocess
from pathlib import Path
from datetime import datetime

PLUGIN_DIR = Path(__file__).parent
HOME = Path.home()
BACKUP_DIR = HOME / ".openclaw" / "backups"
OPENCLAW_DIR = HOME / ".openclaw"
MAX_BACKUPS = 96

def log(msg):
    print(f"[backup-rollback] {msg}", file=sys.stderr)

def get_backup_list():
    """获取备份列表"""
    backups = sorted(BACKUP_DIR.glob("openclaw_*.tar.gz"), reverse=True)
    result = []
    for b in backups:
        name = b.stem.replace("openclaw_", "")
        date_part, time_part = name.split("_")
        ts = f"{date_part[:4]}-{date_part[4:6]}-{date_part[6:]} {time_part[:2]}:{time_part[2:4]}:{time_part[4:]}"
        size = subprocess.run(["du", "-h", str(b)], capture_output=True, text=True).stdout.split()[0]
        result.append({"timestamp": name, "time": ts, "size": size, "file": str(b)})
    return result

def do_backup():
    """执行备份"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"openclaw_{timestamp}.tar.gz"
    
    exclude = [
        "--exclude=node_modules",
        "--exclude=.cache",
        "--exclude=agents/*/node_modules",
        "--exclude=workspace/skills/*/node_modules",
        "--exclude=backups",
        "--exclude=*/logs",
        "--exclude=*.log",
        "--exclude=media",
    ]
    
    cmd = ["tar", "-czf", str(backup_file), "-C", str(OPENCLAW_DIR.parent), OPENCLAW_DIR.name] + exclude
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0 and backup_file.exists():
        size = subprocess.run(["du", "-h", str(backup_file)], capture_output=True, text=True).stdout.split()[0]
        log(f"Backup OK: {backup_file} ({size})")
        
        # 清理旧备份
        backups = sorted(BACKUP_DIR.glob("openclaw_*.tar.gz"), reverse=True)
        for old in backups[MAX_BACKUPS:]:
            old.unlink()
        
        return {"ok": True, "file": str(backup_file), "size": size, "time": timestamp}
    else:
        return {"ok": False, "error": result.stderr}

def do_restore(timestamp):
    """还原指定备份"""
    backup_file = BACKUP_DIR / f"openclaw_{timestamp}.tar.gz"
    if not backup_file.exists():
        return {"ok": False, "error": f"备份不存在: {timestamp}"}
    
    # 备份当前状态
    pre_backup = BACKUP_DIR / f"pre_rollback_{timestamp}.tar.gz"
    exclude = ["--exclude=backups", "--exclude=media"]
    subprocess.run(
        ["tar", "-czf", str(pre_backup), "-C", str(OPENCLAW_DIR.parent), OPENCLAW_DIR.name] + exclude,
        capture_output=True
    )
    
    # 停止服务
    for svc in ["openclaw-gateway", "vector-search", "openclaw-gateway-guardian"]:
        subprocess.run(["systemctl", "--user", "stop", svc], capture_output=True)
    
    # 解压还原
    result = subprocess.run(
        ["tar", "-xzf", str(backup_file), "-C", str(OPENCLAW_DIR.parent)],
        capture_output=True, text=True
    )
    
    # 重启服务
    subprocess.run(["systemctl", "--user", "start", "openclaw-gateway"], capture_output=True)
    
    return {"ok": True, "pre_backup": str(pre_backup), "restored": timestamp}

def handle_command(cmd, args=""):
    """处理命令"""
    if cmd == "backup":
        if not args or args == "list":
            backups = get_backup_list()
            return {"action": "list", "backups": backups[:10]}
        elif args.startswith("restore "):
            timestamp = args.replace("restore ", "").strip()
            return do_restore(timestamp)
        else:
            return do_backup()
    elif cmd == "rollback":
        backups = get_backup_list()
        return {"action": "select", "backups": backups[:10]}
    
    return {"ok": False, "error": "Unknown command"}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: backup_rollb_plugin.py <command> [args]"}))
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2] if len(sys.argv) > 2 else ""
    
    result = handle_command(cmd, args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
