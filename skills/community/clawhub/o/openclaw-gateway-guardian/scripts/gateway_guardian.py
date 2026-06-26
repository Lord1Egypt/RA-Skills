#!/usr/bin/env python3
"""
OpenClaw Gateway Guardian v2 - 网关守护神（优化版）
自动监控、保护和重启 OpenClaw 网关服务
优化目标：最小资源占用、最高效率、智能重启
"""

import os
import sys
import json
import time
import subprocess
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import socket

# ============================================================================
# 轻量级配置
# ============================================================================

CONFIG_DIR = Path.home() / ".openclaw_guardian"
CONFIG_FILE = CONFIG_DIR / "config.json"
LOG_FILE = CONFIG_DIR / "guardian.log"
PID_FILE = CONFIG_DIR / "guardian.pid"
STATE_FILE = CONFIG_DIR / "state.json"

CONFIG_DIR.mkdir(exist_ok=True)

# 默认配置（最小化）
DEFAULT_CONFIG = {
    "gateway": {
        "port": 18789,
        "check_interval": 30,  # 秒
        "max_restarts": 10,
        "restart_delay": 5
    },
    "notifications": {
        "enabled": False
    },
    "logging": {
        "level": "WARNING"  # 减少日志输出
    }
}

# ============================================================================
# 状态管理
# ============================================================================

class StateManager:
    """轻量级状态管理"""
    
    def __init__(self):
        self.state = {
            "last_check": None,
            "consecutive_failures": 0,
            "restart_count": 0,
            "last_restart": None,
            "intentional_stop": False,
            "gateway_pid": None
        }
        self.load()
    
    def load(self):
        """加载状态"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r', encoding='utf-8') as f:
                    self.state = json.load(f)
            except:
                pass
    
    def save(self):
        """保存状态"""
        with open(STATE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2)
    
    def mark_intentional_stop(self):
        """标记为主动关闭"""
        self.state["intentional_stop"] = True
        self.save()
    
    def is_intentional_stop(self) -> bool:
        """是否为主动关闭"""
        return self.state.get("intentional_stop", False)
    
    def reset_intentional_stop(self):
        """重置主动关闭标记"""
        self.state["intentional_stop"] = False
        self.save()

# ============================================================================
# 日志配置（最小化）
# ============================================================================

def setup_logging():
    """配置最小化日志"""
    logging.basicConfig(
        level=logging.WARNING,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8', mode='a'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("GatewayGuardian")

logger = setup_logging()

# ============================================================================
# 健康检查（优化版）
# ============================================================================

class HealthChecker:
    """超轻量级健康检查器"""
    
    def __init__(self, config: Dict):
        self.port = config.get("gateway", {}).get("port", 18789)
        self.interval = config.get("gateway", {}).get("check_interval", config.get("gateway", {}).get("check_interval_seconds", 30))
        self.max_restarts = config.get("gateway", {}).get("max_restarts", config.get("gateway", {}).get("max_restart_attempts", 10))
        self.restart_delay = config.get("gateway", {}).get("restart_delay", config.get("gateway", {}).get("restart_delay_seconds", 5))
        self.failures = 0
        self.restart_count = 0
    
    def check_port(self) -> bool:
        """检查端口（最快方法）"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)  # 缩短超时时间
            result = sock.connect_ex(('127.0.0.1', self.port))
            sock.close()
            return result == 0
        except:
            return False
    
    def check_gateway(self) -> bool:
        """检查网关状态"""
        return self.check_port()
    
    def restart_gateway(self) -> bool:
        """重启网关"""
        try:
            logger.warning("⚠️ 网关异常，正在重启...")
            
            # 使用 openclaw 命令重启
            result = subprocess.run(
                ["openclaw", "gateway", "restart"],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.warning("✅ 网关重启成功")
                self.restart_count += 1
                return True
            else:
                logger.error(f"Gateway restart failed: {result.stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 重启异常：{e}")
            return False
    
    def monitor(self, state: StateManager):
        """监控循环（优化版）"""
        logger.warning(f"🛡️ Gateway Guardian 启动（端口：{self.port}, 间隔：{self.interval}s）")
        
        while True:
            try:
                # 检查是否为主动关闭
                if state.is_intentional_stop():
                    logger.warning("⚠️ 检测到主动关闭，停止监控")
                    break
                
                # 健康检查
                is_healthy = self.check_gateway()
                
                if is_healthy:
                    self.failures = 0
                    time.sleep(self.interval)
                    continue
                
                # 网关异常
                self.failures += 1
                logger.warning(f"⚠️ 网关异常（连续失败：{self.failures}）")
                
                # 达到重启阈值
                if self.failures >= 3:
                    if self.restart_count >= self.max_restarts:
                        logger.error(f"❌ 达到最大重启次数（{self.max_restarts}），停止重启")
                        break
                    
                    # 尝试重启
                    if self.restart_gateway():
                        self.failures = 0
                        time.sleep(self.restart_delay)
                    else:
                        time.sleep(self.interval)
                else:
                    time.sleep(self.interval)
                    
            except KeyboardInterrupt:
                logger.warning("⚠️ 收到中断信号，停止监控")
                break
            except Exception as e:
                logger.error(f"❌ 监控异常：{e}")
                time.sleep(self.interval)

# ============================================================================
# 配置管理
# ============================================================================

def load_config() -> Dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 创建默认配置
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def save_pid(pid: int):
    """保存 PID"""
    with open(PID_FILE, 'w', encoding='utf-8') as f:
        f.write(str(pid))

# ============================================================================
# 命令行
# ============================================================================

def cmd_start():
    """启动守护进程"""
    if PID_FILE.exists():
        with open(PID_FILE, 'r', encoding='utf-8') as f:
            old_pid = f.read().strip()
        logger.error(f"❌ 守护进程已在运行（PID: {old_pid}）")
        return
    
    config = load_config()
    state = StateManager()
    state.reset_intentional_stop()
    
    save_pid(os.getpid())
    
    checker = HealthChecker(config)
    checker.monitor(state)

def cmd_stop():
    """停止守护进程"""
    state = StateManager()
    state.mark_intentional_stop()
    
    if PID_FILE.exists():
        with open(PID_FILE, 'r', encoding='utf-8') as f:
            pid = f.read().strip()
        try:
            os.kill(int(pid), 9)
            logger.warning("⚠️ 守护进程已停止")
        except:
            pass
        finally:
            PID_FILE.unlink(missing_ok=True)
    else:
        logger.warning("⚠️ 守护进程未运行")

def cmd_status():
    """查看状态"""
    if PID_FILE.exists():
        with open(PID_FILE, 'r', encoding='utf-8') as f:
            pid = f.read().strip()
        print(f"✅ 守护进程运行中（PID: {pid}）")
    else:
        print("❌ 守护进程未运行")

def cmd_logs():
    """查看日志"""
    if LOG_FILE.exists():
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("📝 日志文件不存在")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法：python gateway_guardian.py [start|stop|status|logs]")
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "start":
        cmd_start()
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "status":
        cmd_status()
    elif cmd == "logs":
        cmd_logs()
    else:
        print(f"未知命令：{cmd}")

if __name__ == "__main__":
    main()
