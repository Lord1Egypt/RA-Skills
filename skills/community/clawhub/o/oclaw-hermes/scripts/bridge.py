#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
oclaw-hermes 桥接服务 - 核心控制器

实现 OpenClaw × Hermes × DeerFlow 三平台无缝协作

Author: ruiyongwang
Version: 2.0.0
"""

import os
import json
import subprocess
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class PlatformStatus:
    name: str
    connected: bool
    version: str = ""
    error: str = ""
    details: Dict[str, Any] = None


class OclawHermesBridge:
    """三平台桥接控制器"""
    
    def __init__(self):
        self.openclaw_token = os.getenv("OPENCLAW_TOKEN")
        self.hermes_endpoint = os.getenv("HERMES_ENDPOINT", "http://localhost:8080")
        self.deerflow_url = os.getenv("DEERFLOW_URL", "http://localhost:2026")
    
    def check_openclaw(self) -> PlatformStatus:
        """检查 OpenClaw 连接"""
        try:
            result = subprocess.run(
                ["openclawmp", "list"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                skills = len(result.stdout.strip().split('\n')) if result.stdout else 0
                return PlatformStatus(
                    name="OpenClaw",
                    connected=True,
                    version="v1.0.2",
                    details={"skills_installed": skills}
                )
            return PlatformStatus(name="OpenClaw", connected=False, error="CLI 错误")
        except FileNotFoundError:
            return PlatformStatus(name="OpenClaw", connected=False, error="CLI 未安装")
        except Exception as e:
            return PlatformStatus(name="OpenClaw", connected=False, error=str(e))
    
    def check_hermes(self) -> PlatformStatus:
        """检查 Hermes 连接"""
        try:
            result = subprocess.run(
                ["pgrep", "-f", "hermes"],
                capture_output=True, text=True
            )
            is_running = result.returncode == 0
            return PlatformStatus(
                name="Hermes",
                connected=is_running,
                version="v0.1.0",
                details={"running": is_running}
            )
        except Exception as e:
            return PlatformStatus(name="Hermes", connected=False, error=str(e))
    
    def check_deerflow(self) -> PlatformStatus:
        """检查 DeerFlow 连接"""
        try:
            import requests
            response = requests.get(f"{self.deerflow_url}/health", timeout=5)
            if response.status_code == 200:
                return PlatformStatus(
                    name="DeerFlow",
                    connected=True,
                    version="v0.1.0",
                    details={"health": response.json()}
                )
            return PlatformStatus(name="DeerFlow", connected=False, error=f"HTTP {response.status_code}")
        except ImportError:
            return PlatformStatus(name="DeerFlow", connected=False, error="requests 未安装")
        except Exception as e:
            return PlatformStatus(name="DeerFlow", connected=False, error=str(e))
    
    def status(self) -> Dict[str, Any]:
        """获取完整状态"""
        return {
            "openclaw": self.check_openclaw(),
            "hermes": self.check_hermes(),
            "deerflow": self.check_deerflow(),
            "all_connected": all([
                self.check_openclaw().connected,
                self.check_hermes().connected,
                self.check_deerflow().connected
            ])
        }


def main():
    """命令行入口"""
    import argparse
    parser = argparse.ArgumentParser(description="oclaw-hermes 桥接服务")
    parser.add_argument("command", choices=["status", "start", "stop"])
    args = parser.parse_args()
    
    bridge = OclawHermesBridge()
    
    if args.command == "status":
        status = bridge.status()
        print(json.dumps({
            "openclaw": {
                "connected": status["openclaw"].connected,
                "version": status["openclaw"].version,
                "details": status["openclaw"].details
            },
            "hermes": {
                "connected": status["hermes"].connected,
                "version": status["hermes"].version
            },
            "deerflow": {
                "connected": status["deerflow"].connected,
                "version": status["deerflow"].version
            },
            "all_connected": status["all_connected"]
        }, indent=2, ensure_ascii=False))
    
    elif args.command == "start":
        print("[INFO] 启动 oclaw-hermes 服务...")
        # 启动逻辑
    
    elif args.command == "stop":
        print("[INFO] 停止 oclaw-hermes 服务...")
        # 停止逻辑


if __name__ == "__main__":
    main()
