#!/usr/bin/env python3
"""
回滚系统 - 列出可用备份 + 还原
用法:
  python3 rollback.py list              # 列出所有备份
  python3 rollback.py restore <timestamp> # 还原指定版本
"""
import os
import sys
import subprocess
import json
from pathlib import Path

BACKUP_DIR = Path.home() / ".openclaw" / "backups"

def list_backups():
    """列出所有备份"""
    backups = sorted(BACKUP_DIR.glob("openclaw_*.tar.gz"), reverse=True)
    
    if not backups:
        return []
    
    result = []
    for b in backups:
        # 从文件名提取时间
        name = b.stem  # openclaw_20260403_202824
        parts = name.replace("openclaw_", "").split("_")
        if len(parts) >= 2:
            date_str = parts[0]  # 20260403
            time_str = parts[1]  # 202824
            formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]} {time_str[:2]}:{time_str[2:4]}:{time_str[4:]}"
        else:
            formatted = name
        
        size = subprocess.run(
            ["du", "-h", str(b)],
            capture_output=True, text=True
        ).stdout.split()[0]
        
        result.append({
            "name": name,
            "file": str(b),
            "time": formatted,
            "size": size
        })
    
    return result

def diff_backup(timestamp):
    """预览备份与当前配置的差异"""
    import tarfile
    import tempfile
    
    backup_file = BACKUP_DIR / f"openclaw_{timestamp}.tar.gz"
    if not backup_file.exists():
        return f"❌ 备份不存在"
    
    openclaw_dir = Path.home() / ".openclaw"
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # 解压备份到临时目录
        subprocess.run(["tar", "-xzf", str(backup_file), "-C", tmpdir], capture_output=True)
        backup_extract = Path(tmpdir) / ".openclaw"
        
        # 对比关键配置文件
        configs = ["openclaw.json", "memory/2026-04-03.md", "workspace/MEMORY.md"]
        diffs = []
        
        for cfg in configs:
            current = openclaw_dir / cfg
            backup = backup_extract / cfg
            
            if backup.exists():
                c_content = current.read_text(errors='ignore') if current.exists() else "[不存在]"
                b_content = backup.read_text(errors='ignore')
                
                if c_content != b_content:
                    diffs.append(f"📝 {cfg}\n  当前: {len(c_content)}字节 | 备份: {len(b_content)}字节")
                else:
                    diffs.append(f"✅ {cfg} (相同)")
        
        if not diffs:
            return f"📂 备份与当前无差异"
        
        return "\n".join(diffs) or "无显著差异"

def restore_backup(timestamp):
    """还原指定备份"""
    backup_file = BACKUP_DIR / f"openclaw_{timestamp}.tar.gz"
    
    if not backup_file.exists():
        return f"❌ 备份不存在: openclaw_{timestamp}.tar.gz"
    
    # 先停止gateway
    print("🛑 停止 Gateway...")
    subprocess.run(["systemctl", "--user", "stop", "openclaw-gateway"], capture_output=True)
    subprocess.run(["systemctl", "--user", "stop", "vector-search"], capture_output=True)
    subprocess.run(["systemctl", "--user", "stop", "openclaw-gateway-guardian"], capture_output=True)
    
    openclaw_dir = Path.home() / ".openclaw"
    
    # 备份当前状态
    current_backup = openclaw_dir / f"pre_rollback_{timestamp}.tar.gz"
    print("📦 备份当前状态...")
    subprocess.run(
        ["tar", "-czf", str(current_backup), "-C", str(openclaw_dir.parent), openclaw_dir.name, "--exclude=backups"],
        capture_output=True
    )
    
    # 解压还原
    print("🔄 还原到备份...")
    result = subprocess.run(
        ["tar", "-xzf", str(backup_file), "-C", str(openclaw_dir.parent)],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        return f"❌ 还原失败: {result.stderr}"
    
    # 重启服务
    print("🚀 重启服务...")
    subprocess.run(["systemctl", "--user", "start", "openclaw-gateway"], capture_output=True)
    subprocess.run(["systemctl", "--user", "start", "vector-search"], capture_output=True)
    subprocess.run(["systemctl", "--user", "start", "openclaw-gateway-guardian"], capture_output=True)
    
    return f"✅ 成功还原到 {timestamp}，当前状态已备份到 pre_rollback_{timestamp}.tar.gz"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: rollback.py list|diff <timestamp>|restore <timestamp>")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "list":
        backups = list_backups()
        for b in backups:
            print(f"{b['time']} | {b['size']} | {b['name']}")
    elif cmd == "diff" and len(sys.argv) >= 3:
        print(diff_backup(sys.argv[2]))
    elif cmd == "restore" and len(sys.argv) >= 3:
        print(restore_backup(sys.argv[2]))
    else:
        print("用法: rollback.py list|diff <timestamp>|restore <timestamp>")
