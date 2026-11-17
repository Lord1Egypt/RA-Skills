#!/usr/bin/env python3
"""
F2: SearXNG 本地实例管理模块
- Docker 优先 / pip 兜底 双路径安装
- 强制绑定 127.0.0.1:8888（仅本地回循环接）
- 启动、停止、状态、健康检查
- 依赖 venv 虚拟环境隔离，不污染系统 Python
"""

import json
import os
import secrets
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urljoin

# 不生成 __pycache__（死规则 13）
sys.dont_write_bytecode = True

# 依赖检查须早于第三方 import，避免用户只看到裸 ModuleNotFoundError
try:
    from version_util import require_dependencies
except ImportError:
    from .version_util import require_dependencies

require_dependencies(("aiohttp", "yaml"))

import aiohttp
import yaml

# SearXNG 密钥：首次启动时生成并持久化到本地，后续启动复用。
# 原因：每次随机生成会导致旧实例配置失效，用户需重新配置端口、引擎等。
_SECRET_PATH = os.path.expanduser("~/.workbuddy/output/.searxng_secret")


def _load_or_create_secret() -> str:
    """加载已有 Secret，不存在则生成并持久化"""
    try:
        if os.path.exists(_SECRET_PATH):
            with open(_SECRET_PATH, "r", encoding="utf-8") as f:
                val = f.read().strip()
                if len(val) >= 16:
                    return val
    except Exception:
        pass
    # 不存在或无效，重新生成
    val = secrets.token_hex(16)
    try:
        os.makedirs(os.path.dirname(_SECRET_PATH), exist_ok=True)
        with open(_SECRET_PATH, "w", encoding="utf-8", newline="") as f:
            f.write(val)
    except Exception:
        pass
    return val


SEARXNG_SECRET = _load_or_create_secret()

# ============================================================
# 配置管理
# ============================================================

DEFAULT_CONFIG = {
    "searxng": {
        "enabled": True,
        "host": "127.0.0.1",
        "port": 8888,
        "install_method": "docker",
        "docker": {
            "image": "searxng/searxng:latest",
            "container_name": "privacy-search-searxng",
            "auto_remove": True,
        },
        "pip": {
            "use_venv": True,
            "venv_path": "~/.workbuddy/output/.privacy-search-venv",
        },
    }
}


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件（合并默认值）"""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f) or {}
        # 合并默认值
        merged = {**DEFAULT_CONFIG, **user_config}
        for key in DEFAULT_CONFIG:
            if key in user_config and isinstance(DEFAULT_CONFIG[key], dict):
                merged[key] = {**DEFAULT_CONFIG[key], **user_config[key]}
        return merged
    except FileNotFoundError:
        return DEFAULT_CONFIG.copy()


# ============================================================
# Docker 安装方式
# ============================================================

class DockerManager:
    """Docker 方式管理 SearXNG"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config["searxng"]["docker"]
        self.host = config["searxng"]["host"]
        self.port = config["searxng"]["port"]
        self.image = self.config["image"]
        self.container_name = self.config["container_name"]
        self.auto_remove = self.config.get("auto_remove", True)

    def _run(self, cmd: list, check: bool = True) -> subprocess.CompletedProcess:
        """执行 Docker 命令"""
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if check and result.returncode != 0:
            raise RuntimeError(f"Docker 命令失败: {result.stderr.strip()}")
        return result

    def is_docker_available(self) -> bool:
        """检查 Docker 是否可用"""
        try:
            result = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def is_container_running(self) -> bool:
        """检查容器是否正在运行"""
        try:
            result = self._run(
                ["docker", "ps", "--filter", f"name={self.container_name}", "--format", "{{.Names}}"],
                check=False,
            )
            return self.container_name in result.stdout
        except Exception:
            return False

    def install(self) -> bool:
        """安装 SearXNG（拉取镜像）"""
        if not self.is_docker_available():
            return False

        try:
            # 拉取最新镜像
            print(f"🔍 拉取镜像: {self.image}")
            self._run(["docker", "pull", self.image])
            return True
        except Exception as e:
            print(f"❌ 镜像拉取失败: {e}")
            return False

    def start(self) -> bool:
        """启动 SearXNG 容器"""
        if self.is_container_running():
            print(f"✅ 容器 {self.container_name} 已在运行")
            return True

        try:
            cmd = [
                "docker", "run", "-d",
                "--name", self.container_name,
                "-p", f"{self.host}:{self.port}:8080",
                "--restart", "unless-stopped",
            ]
            # SearXNG 需要的环境变量
            cmd.extend([
                "-e", "SEARXNG_BASE_URL=http://127.0.0.1:8888/",
                "-e", "SEARXNG_BIND_ADDRESS=127.0.0.1",
                "-e", f"SEARXNG_SECRET={SEARXNG_SECRET}",
            ])
            if self.auto_remove:
                cmd.append("--rm")
            cmd.append(self.image)

            self._run(cmd)
            # 等待启动
            if self._wait_for_healthy():
                print(f"✅ SearXNG 启动成功: http://{self.host}:{self.port}")
                return True
            else:
                print("❌ SearXNG 启动超时")
                return False
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return False

    def stop(self) -> bool:
        """停止容器"""
        if not self.is_container_running():
            print(f"⚠️ 容器 {self.container_name} 未运行")
            return True

        try:
            self._run(["docker", "stop", self.container_name])
            print(f"✅ 容器 {self.container_name} 已停止")
            return True
        except Exception as e:
            print(f"❌ 停止失败: {e}")
            return False

    def status(self) -> Dict[str, Any]:
        """返回容器状态"""
        return {
            "running": self.is_container_running(),
            "container_name": self.container_name,
            "image": self.image,
            "host": self.host,
            "port": self.port,
            "docker_available": self.is_docker_available(),
        }

    def _wait_for_healthy(self, timeout: int = 30) -> bool:
        """等待服务可用"""
        url = f"http://{self.host}:{self.port}/search?q=test&format=json"
        start = time.time()
        while time.time() - start < timeout:
            try:
                import urllib.request
                with urllib.request.urlopen(url, timeout=2) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                pass
            time.sleep(1)
        return False


# ============================================================
# pip 安装方式（venv 隔离）
# ============================================================

class PipManager:
    """pip 方式管理 SearXNG（venv 隔离）"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config["searxng"]["pip"]
        self.host = config["searxng"]["host"]
        self.port = config["searxng"]["port"]
        self.use_venv = self.config.get("use_venv", True)
        self.venv_path = os.path.expanduser(self.config.get("venv_path", "~/.workbuddy/output/.privacy-search-venv"))
        self.server_process: Optional[subprocess.Popen] = None

    def _in_venv(self) -> bool:
        """检查是否在 venv 中"""
        return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

    def _ensure_venv(self) -> str:
        """确保 venv 存在，返回 python 路径"""
        python_path = os.path.join(self.venv_path, "bin", "python.exe") if os.name == "nt" else os.path.join(self.venv_path, "bin", "python")
        pip_path = os.path.join(self.venv_path, "bin", "pip.exe") if os.name == "nt" else os.path.join(self.venv_path, "bin", "pip")

        if not os.path.exists(self.venv_path):
            print(f"📦 创建虚拟环境: {self.venv_path}")
            subprocess.run([sys.executable, "-m", "venv", self.venv_path], check=True)

        return python_path

    def install(self) -> bool:
        """安装 SearXNG 到 venv"""
        try:
            python_path = self._ensure_venv()
            pip_path = os.path.join(self.venv_path, "bin", "pip.exe") if os.name == "nt" else os.path.join(self.venv_path, "bin", "pip")
            print(f"📥 安装 SearXNG 到 {self.venv_path}")
            subprocess.run([pip_path, "install", "searxng"], check=True, timeout=120)
            return True
        except Exception as e:
            print(f"❌ 安装失败: {e}")
            return False

    def start(self) -> bool:
        """启动 SearXNG 服务"""
        try:
            python_path = self._ensure_venv()
            pip_path = os.path.join(self.venv_path, "bin", "pip.exe") if os.name == "nt" else os.path.join(self.venv_path, "bin", "pip")

            # 检查 searxng 是否已安装
            result = subprocess.run(
                [python_path, "-c", "import searxng; print('ok')"],
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                if not self.install():
                    return False

            # 启动服务
            self.server_process = subprocess.Popen(
                [python_path, "-m", "searxng"],
                env={
                    **os.environ,
                    "SEARXNG_BIND_ADDRESS": self.host,
                    "SEARXNG_PORT": str(self.port),
                    "SEARXNG_SECRET": SEARXNG_SECRET,
                    "SEARXNG_BASE_URL": f"http://{self.host}:{self.port}/",
                },
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # 等待启动
            if self._wait_for_healthy():
                print(f"✅ SearXNG 启动成功: http://{self.host}:{self.port}")
                return True
            else:
                print("❌ 启动超时")
                return False
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return False

    def stop(self) -> bool:
        """停止服务"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=10)
            self.server_process = None
            print("✅ SearXNG 已停止")
            return True
        return False

    def status(self) -> Dict[str, Any]:
        """返回服务状态"""
        return {
            "running": self.server_process is not None and self.server_process.poll() is None,
            "venv_path": self.venv_path,
            "host": self.host,
            "port": self.port,
        }

    def _wait_for_healthy(self, timeout: int = 30) -> bool:
        """等待服务可用"""
        url = f"http://{self.host}:{self.port}/search?q=test&format=json"
        start = time.time()
        while time.time() - start < timeout:
            try:
                import urllib.request
                with urllib.request.urlopen(url, timeout=2) as resp:
                    if resp.status == 200:
                        return True
            except Exception:
                pass
            time.sleep(1)
        return False


# ============================================================
# 统一入口
# ============================================================

class SearXNGManager:
    """SearXNG 统一管理器"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.docker_manager = DockerManager(config)
        self.pip_manager = PipManager(config)
        self.method = config["searxng"].get("install_method", "docker")
        # V1.2: 与 search.py 共享同一开关语义（P0-4）
        self.enabled = bool(config["searxng"].get("enabled", True))

    def install(self) -> bool:
        """安装 SearXNG"""
        if self.method == "docker":
            return self.docker_manager.install()
        else:
            return self.pip_manager.install()

    def start(self) -> bool:
        """启动 SearXNG"""
        if self.method == "docker":
            return self.docker_manager.start()
        else:
            return self.pip_manager.start()

    def stop(self) -> bool:
        """停止 SearXNG"""
        if self.method == "docker":
            return self.docker_manager.stop()
        else:
            return self.pip_manager.stop()

    def status(self) -> Dict[str, Any]:
        """获取状态"""
        if self.method == "docker":
            info = self.docker_manager.status()
        else:
            info = self.pip_manager.status()
        # enabled 置于首位，便于排查「搜索时 searxng 被跳过」的原因
        return {"enabled": self.enabled, "method": self.method, **info}


# ============================================================
# CLI 入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="SearXNG 本地实例管理")
    parser.add_argument("action", choices=["install", "start", "stop", "status"], help="操作")
    parser.add_argument("--config", help="配置文件路径")
    parser.add_argument("--method", choices=["docker", "pip"], help="安装方式（覆盖配置）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")

    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    # V1.2: searxng.enabled 开关真正生效（P0-4）
    # 关闭时拒绝执行 install/start，避免与 search.py 的引擎筛选行为不一致
    if not bool(config["searxng"].get("enabled", True)) and args.action in ("install", "start"):
        msg = "SearXNG 已在配置中禁用（searxng.enabled: false），请先改为 true 再执行此操作"
        if args.json:
            print(json.dumps({"ok": False, "enabled": False, "message": msg},
                             ensure_ascii=False, indent=2))
        else:
            print(f"⚠️  {msg}")
        sys.exit(2)

    # 覆盖安装方式
    if args.method:
        config["searxng"]["install_method"] = args.method

    manager = SearXNGManager(config)
    result = None

    if args.action == "install":
        success = manager.install()
        print(f"{'✅ 安装成功' if success else '❌ 安装失败'}")
    elif args.action == "start":
        success = manager.start()
        print(f"{'✅ 启动成功' if success else '❌ 启动失败'}")
    elif args.action == "stop":
        success = manager.stop()
        print(f"{'✅ 停止成功' if success else '❌ 停止失败'}")
    elif args.action == "status":
        result = manager.status()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            for k, v in result.items():
                print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
