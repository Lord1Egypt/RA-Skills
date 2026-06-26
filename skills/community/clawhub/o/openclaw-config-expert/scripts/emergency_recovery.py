#!/usr/bin/env python3
"""
OpenClaw 紧急恢复脚本
Hermes 专用 - 用于 Gateway 崩溃时的紧急恢复

使用方法:
    python3 emergency_recovery.py recover     # 完整恢复流程
    python3 emergency_recovery.py rollback    # 回滚到备份
    python3 emergency_recovery.py restart     # 重启 Gateway
    python3 emergency_recovery.py status      # 检查状态
"""

import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# 路径配置
OPENCLAW_DIR = Path.home() / ".openclaw"
CONFIG_PATH = OPENCLAW_DIR / "openclaw.json"
BACKUP_PATH = OPENCLAW_DIR / "openclaw.json.bak"
LOGS_DIR = OPENCLAW_DIR / "logs"
RECOVERY_LOG = LOGS_DIR / "emergency-recovery.log"
GATEWAY_PORT = 18789


def log(message: str, level: str = "INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] [{level}] {message}"
    print(log_line)
    
    # 写入日志文件
    try:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        with open(RECOVERY_LOG, 'a', encoding='utf-8') as f:
            f.write(log_line + "\n")
    except Exception as e:
        print(f"警告：无法写入日志文件：{e}")


def check_gateway_status() -> dict:
    """检查 Gateway 状态"""
    result = {
        "running": False,
        "pid": None,
        "port_in_use": False,
        "dashboard_accessible": False
    }
    
    # 检查进程
    try:
        proc_result = subprocess.run(
            ["pgrep", "-f", "openclaw.*gateway"],
            capture_output=True,
            text=True
        )
        if proc_result.returncode == 0 and proc_result.stdout.strip():
            result["running"] = True
            result["pid"] = proc_result.stdout.strip().split("\n")[0]
    except Exception as e:
        log(f"检查进程失败：{e}", "ERROR")
    
    # 检查端口
    try:
        proc_result = subprocess.run(
            ["lsof", "-i", f":{GATEWAY_PORT}"],
            capture_output=True,
            text=True
        )
        if proc_result.returncode == 0:
            result["port_in_use"] = True
    except Exception:
        pass
    
    # 检查 Dashboard 可访问性
    try:
        import urllib.request
        urllib.request.urlopen(f"http://127.0.0.1:{GATEWAY_PORT}", timeout=2)
        result["dashboard_accessible"] = True
    except Exception:
        pass
    
    return result


def find_backup() -> Path:
    """查找最新的备份文件"""
    # 检查标准备份路径
    if BACKUP_PATH.exists():
        return BACKUP_PATH
    
    # 查找时间戳备份
    backup_dir = OPENCLAW_DIR / "backups"
    if backup_dir.exists():
        backups = sorted(
            backup_dir.glob("openclaw.json.*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        if backups:
            return backups[0]
    
    return None


def restore_backup(backup_path: Path = None) -> bool:
    """恢复备份"""
    if backup_path is None:
        backup_path = find_backup()
    
    if backup_path is None or not backup_path.exists():
        log("未找到备份文件", "ERROR")
        return False
    
    try:
        # 验证备份文件
        with open(backup_path, 'r', encoding='utf-8') as f:
            json.load(f)  # 验证 JSON 格式
        
        # 复制备份到配置
        shutil.copy2(backup_path, CONFIG_PATH)
        log(f"配置已回滚到：{backup_path.name}")
        return True
    except json.JSONDecodeError:
        log(f"备份文件损坏：{backup_path}", "ERROR")
        return False
    except Exception as e:
        log(f"恢复失败：{e}", "ERROR")
        return False


def restart_gateway() -> bool:
    """重启 Gateway"""
    try:
        # 停止现有 Gateway
        log("停止现有 Gateway...")
        subprocess.run(
            ["pkill", "-f", "openclaw.*gateway"],
            capture_output=True
        )
        
        # 等待端口释放
        import time
        time.sleep(2)
        
        # 启动 Gateway
        log("启动 Gateway...")
        subprocess.Popen(
            ["openclaw", "gateway", "start"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # 等待启动
        time.sleep(5)
        
        # 验证启动
        status = check_gateway_status()
        if status["dashboard_accessible"]:
            log("Gateway 重启成功")
            return True
        else:
            log("Gateway 启动但 Dashboard 不可访问", "WARNING")
            return False
            
    except Exception as e:
        log(f"重启失败：{e}", "ERROR")
        return False


def recover():
    """完整恢复流程"""
    log("=" * 60)
    log("开始紧急恢复流程")
    log("=" * 60)
    
    # 步骤 1：检查 Gateway 状态
    log("1. 检查 Gateway 状态...")
    status = check_gateway_status()
    
    if status["dashboard_accessible"]:
        log("Gateway 运行正常，无需恢复", "WARNING")
        return
    
    log(f"   - 进程运行：{status['running']} (PID: {status['pid']})")
    log(f"   - 端口占用：{status['port_in_use']}")
    log(f"   - Dashboard: {status['dashboard_accessible']}")
    
    # 步骤 2：查找备份
    log("2. 查找备份文件...")
    backup = find_backup()
    if backup:
        log(f"   ✅ 找到备份：{backup.name}")
    else:
        log("   ❌ 未找到备份文件", "ERROR")
        return
    
    # 步骤 3：回滚配置
    log("3. 回滚配置...")
    if not restore_backup(backup):
        log("   ❌ 回滚失败", "ERROR")
        return
    log("   ✅ 配置已回滚")
    
    # 步骤 4：重启 Gateway
    log("4. 重启 Gateway...")
    if not restart_gateway():
        log("   ❌ 重启失败", "ERROR")
        return
    log("   ✅ Gateway 已重启")
    
    # 步骤 5：验证 Dashboard
    log("5. 验证 Dashboard...")
    final_status = check_gateway_status()
    
    if final_status["dashboard_accessible"]:
        log("=" * 60)
        log("✅ 恢复成功！")
        log("=" * 60)
        log(f"Dashboard: http://127.0.0.1:{GATEWAY_PORT}")
        log(f"日志：{RECOVERY_LOG}")
    else:
        log("=" * 60)
        log("⚠️ 恢复完成但 Dashboard 不可访问")
        log("=" * 60)
        log("请检查日志文件获取更多信息:")
        log(f"  - {RECOVERY_LOG}")
        log(f"  - {LOGS_DIR / 'gateway.log'}")
        log(f"  - {LOGS_DIR / 'gateway.err.log'}")


def rollback():
    """回滚到备份"""
    log("开始回滚操作...")
    
    backup = find_backup()
    if not backup:
        log("未找到备份文件", "ERROR")
        return
    
    if restore_backup(backup):
        log("✅ 回滚成功")
        log(f"已恢复到：{backup.name}")
        log("请手动重启 Gateway: openclaw gateway restart")
    else:
        log("❌ 回滚失败", "ERROR")


def restart():
    """重启 Gateway"""
    log("开始重启 Gateway...")
    
    if restart_gateway():
        log("✅ Gateway 重启成功")
        log(f"Dashboard: http://127.0.0.1:{GATEWAY_PORT}")
    else:
        log("❌ Gateway 重启失败", "ERROR")


def status():
    """检查状态"""
    log("OpenClaw 状态检查")
    log("-" * 40)
    
    status = check_gateway_status()
    
    log(f"Gateway 进程：{'✅ 运行中' if status['running'] else '❌ 未运行'}")
    if status['pid']:
        log(f"  PID: {status['pid']}")
    
    log(f"端口 {GATEWAY_PORT}: {'✅ 占用' if status['port_in_use'] else '❌ 空闲'}")
    log(f"Dashboard: {'✅ 可访问' if status['dashboard_accessible'] else '❌ 不可访问'}")
    
    # 检查配置文件
    if CONFIG_PATH.exists():
        log(f"配置文件：✅ 存在 ({CONFIG_PATH})")
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                config = json.load(f)
            log(f"  格式：✅ 有效 JSON")
            log(f"  Agents: {len(config.get('agents', {}).get('list', []))} 个")
        except json.JSONDecodeError:
            log(f"  格式：❌ JSON 解析错误", "ERROR")
    else:
        log(f"配置文件：❌ 不存在", "ERROR")
    
    # 检查备份
    backup = find_backup()
    if backup:
        log(f"备份文件：✅ 存在 ({backup.name})")
    else:
        log(f"备份文件：❌ 不存在", "WARNING")
    
    log("-" * 40)
    if status['dashboard_accessible']:
        log(f"Dashboard URL: http://127.0.0.1:{GATEWAY_PORT}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "recover":
        recover()
    elif command == "rollback":
        rollback()
    elif command == "restart":
        restart()
    elif command == "status":
        status()
    else:
        print(f"未知命令：{command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
