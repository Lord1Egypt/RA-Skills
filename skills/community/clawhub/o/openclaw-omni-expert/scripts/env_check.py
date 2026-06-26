#!/usr/bin/env python3
"""
OpenClaw 环境检测工具
自动检测系统环境是否满足 OpenClaw 安装和运行的最低要求
"""

import os
import sys
import json
import platform
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


class EnvironmentChecker:
    """环境检测器"""

    def __init__(self):
        self.results = {
            "system": {},
            "hardware": {},
            "software": {},
            "network": {},
            "recommendations": []
        }

    def check_all(self) -> Dict:
        """执行所有检测项"""
        print("开始检测 OpenClaw 安装环境...")

        self._check_system()
        self._check_hardware()
        self._check_software()
        self._check_network()
        self._check_ports()
        self._generate_recommendations()

        return self.results

    def _check_system(self):
        """检测系统信息"""
        print("检测操作系统...")
        system = platform.system()
        release = platform.release()
        version = platform.version()

        self.results["system"] = {
            "os": system,
            "release": release,
            "version": version,
            "machine": platform.machine(),
            "python_version": platform.python_version(),
            "status": "pass"
        }

        # 系统兼容性检查
        if system == "Windows":
            # Windows 必须使用 WSL2
            try:
                result = subprocess.run(
                    ["wsl", "--status"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode != 0:
                    self.results["system"]["status"] = "fail"
                    self.results["system"]["reason"] = "Windows 需要安装 WSL2"
            except FileNotFoundError:
                self.results["system"]["status"] = "fail"
                self.results["system"]["reason"] = "Windows 需要安装 WSL2"
        elif system == "Darwin":
            # macOS 版本要求
            version_parts = version.split(".")
            major_version = int(version_parts[0])
            if major_version < 12:
                self.results["system"]["status"] = "warning"
                self.results["system"]["reason"] = "macOS 版本建议 12+"
        elif system == "Linux":
            # Linux 发行版检查
            try:
                with open("/etc/os-release", "r") as f:
                    os_release = f.read()
                    if "Ubuntu" in os_release:
                        version_info = [line for line in os_release.split("\n")
                                      if line.startswith("VERSION_ID")]
                        if version_info:
                            version_id = version_info[0].split('"')[1]
                            major_ver = int(version_id.split(".")[0])
                            if major_ver < 20:
                                self.results["system"]["status"] = "warning"
                                self.results["system"]["reason"] = "Ubuntu 版本建议 20.04+"
            except Exception:
                pass

    def _check_hardware(self):
        """检测硬件配置"""
        print("检测硬件配置...")

        # 内存检测
        try:
            if platform.system() == "Darwin":  # macOS
                result = subprocess.run(
                    ["sysctl", "-n", "hw.memsize"],
                    capture_output=True,
                    text=True
                )
                total_memory = int(result.stdout.strip()) // (1024**3)
            elif platform.system() == "Linux":
                result = subprocess.run(
                    ["free", "-g"],
                    capture_output=True,
                    text=True
                )
                lines = result.stdout.split("\n")
                mem_line = [l for l in lines if l.startswith("Mem:")][0]
                total_memory = int(mem_line.split()[1])
            else:  # Windows
                import ctypes
                kernel32 = ctypes.windll.kernel32
                total_memory = kernel32.GlobalMemoryStatusEx().ullTotalPhys // (1024**3)
        except Exception:
            total_memory = 0

        # CPU 检测
        cpu_count = os.cpu_count() or 0

        # 磁盘空间检测
        try:
            disk_usage = shutil.disk_usage(Path.home())
            free_disk_gb = disk_usage.free // (1024**3)
        except Exception:
            free_disk_gb = 0

        # GPU 检测(可选)
        gpu_info = self._detect_gpu()

        self.results["hardware"] = {
            "memory_gb": total_memory,
            "memory_status": self._check_memory(total_memory),
            "cpu_cores": cpu_count,
            "cpu_status": self._check_cpu(cpu_count),
            "free_disk_gb": free_disk_gb,
            "disk_status": self._check_disk(free_disk_gb),
            "gpu": gpu_info,
            "status": self._evaluate_hardware(total_memory, cpu_count, free_disk_gb)
        }

    def _check_software(self):
        """检测软件依赖"""
        print("检测软件依赖...")

        software = {}

        # Node.js 检测
        node_version = self._get_command_version("node", "--version")
        if node_version:
            major_version = self._extract_major_version(node_version)
            node_status = "pass" if major_version >= 22 else "fail"
            software["nodejs"] = {
                "version": node_version,
                "major_version": major_version,
                "status": node_status
            }
            if node_status == "fail":
                software["nodejs"]["reason"] = "Node.js 要求 v22+"
        else:
            software["nodejs"] = {
                "status": "fail",
                "reason": "未安装 Node.js"
            }

        # npm 检测
        npm_version = self._get_command_version("npm", "--version")
        software["npm"] = {
            "installed": npm_version is not None,
            "version": npm_version if npm_version else "未安装"
        }

        # Git 检测
        git_version = self._get_command_version("git", "--version")
        software["git"] = {
            "installed": git_version is not None,
            "version": git_version if git_version else "未安装"
        }

        # Python 检测
        software["python"] = {
            "version": platform.python_version(),
            "status": "pass"
        }

        # 构建工具检测(Linux/macOS)
        if platform.system() != "Windows":
            build_tools = []
            if self._command_exists("gcc"):
                build_tools.append("gcc")
            if self._command_exists("make"):
                build_tools.append("make")
            if self._command_exists("cmake"):
                build_tools.append("cmake")
            software["build_tools"] = build_tools

        # OpenClaw 检测
        openclaw_version = self._get_command_version("openclaw", "--version")
        if openclaw_version:
            software["openclaw"] = {
                "installed": True,
                "version": openclaw_version,
                "status": "pass"
            }
        else:
            software["openclaw"] = {
                "installed": False,
                "status": "warning",
                "reason": "OpenClaw 未安装"
            }

        self.results["software"] = software

    def _check_network(self):
        """检测网络连接"""
        print("检测网络连接...")

        network = {}

        # 检测 npm 官方源连接
        try:
            import urllib.request
            urllib.request.urlopen("https://registry.npmjs.org/", timeout=5)
            network["npm_registry"] = {
                "status": "pass",
                "source": "官方源"
            }
        except Exception:
            # 尝试国内镜像
            try:
                urllib.request.urlopen("https://registry.npmmirror.com/", timeout=5)
                network["npm_registry"] = {
                    "status": "pass",
                    "source": "国内镜像"
                }
            except Exception:
                network["npm_registry"] = {
                    "status": "fail",
                    "reason": "无法连接 npm 源"
                }

        # 检测 GitHub 连接
        try:
            urllib.request.urlopen("https://github.com/", timeout=5)
            network["github"] = {
                "status": "pass"
            }
        except Exception:
            network["github"] = {
                "status": "warning",
                "reason": "无法连接 GitHub"
            }

        self.results["network"] = network

    def _check_ports(self):
        """检测端口占用"""
        print("检测端口占用...")

        port = 18789  # OpenClaw 默认端口
        port_status = {
            "port": port,
            "occupied": False,
            "process": None
        }

        try:
            if platform.system() == "Darwin" or platform.system() == "Linux":
                result = subprocess.run(
                    ["lsof", "-i", f":{port}"],
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    lines = result.stdout.strip().split("\n")[1:]
                    if lines:
                        port_status["occupied"] = True
                        port_status["process"] = lines[0].strip()
            elif platform.system() == "Windows":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True
                )
                if str(port) in result.stdout:
                    port_status["occupied"] = True
        except Exception:
            pass

        self.results["ports"] = port_status

    def _generate_recommendations(self):
        """生成优化建议"""
        recommendations = []

        # Node.js 版本建议
        if self.results["software"].get("nodejs", {}).get("status") == "fail":
            recommendations.append({
                "priority": "high",
                "issue": "Node.js 版本不满足要求",
                "solution": "升级到 Node.js v22 或更高版本",
                "commands": self._get_nodejs_upgrade_commands()
            })

        # 内存建议
        if self.results["hardware"]["memory_gb"] < 4:
            recommendations.append({
                "priority": "medium",
                "issue": "内存偏低",
                "solution": "建议升级到 4GB 以上内存",
                "note": "当前配置仅适合轻量使用"
            })

        # 磁盘空间建议
        if self.results["hardware"]["free_disk_gb"] < 10:
            recommendations.append({
                "priority": "high",
                "issue": "磁盘空间不足",
                "solution": "清理磁盘或扩容至至少 10GB 可用空间"
            })

        # 网络建议
        if self.results["network"].get("npm_registry", {}).get("status") == "fail":
            recommendations.append({
                "priority": "high",
                "issue": "无法连接 npm 源",
                "solution": "配置代理或使用国内镜像源",
                "commands": ["npm config set registry https://registry.npmmirror.com"]
            })

        # OpenClaw 安装建议
        if not self.results["software"].get("openclaw", {}).get("installed"):
            recommendations.append({
                "priority": "info",
                "issue": "OpenClaw 未安装",
                "solution": "运行安装脚本: bash scripts/install_openclaw.sh"
            })

        self.results["recommendations"] = recommendations

    def _get_command_version(self, command: str, version_flag: str) -> str:
        """获取命令版本"""
        try:
            result = subprocess.run(
                [command, version_flag],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _command_exists(self, command: str) -> bool:
        """检查命令是否存在"""
        return shutil.which(command) is not None

    def _extract_major_version(self, version_str: str) -> int:
        """提取主版本号"""
        import re
        match = re.search(r'(\d+)', version_str)
        if match:
            return int(match.group(1))
        return 0

    def _check_memory(self, memory_gb: int) -> str:
        """检查内存状态"""
        if memory_gb >= 8:
            return "excellent"
        elif memory_gb >= 4:
            return "good"
        elif memory_gb >= 2:
            return "minimal"
        else:
            return "insufficient"

    def _check_cpu(self, cpu_cores: int) -> str:
        """检查 CPU 状态"""
        if cpu_cores >= 8:
            return "excellent"
        elif cpu_cores >= 4:
            return "good"
        elif cpu_cores >= 2:
            return "minimal"
        else:
            return "insufficient"

    def _check_disk(self, disk_gb: int) -> str:
        """检查磁盘状态"""
        if disk_gb >= 50:
            return "excellent"
        elif disk_gb >= 20:
            return "good"
        elif disk_gb >= 10:
            return "minimal"
        else:
            return "insufficient"

    def _evaluate_hardware(self, memory: int, cpu: int, disk: int) -> str:
        """综合评估硬件状态"""
        if (memory >= 4 and cpu >= 2 and disk >= 10):
            return "pass"
        elif (memory >= 2 and cpu >= 2 and disk >= 5):
            return "warning"
        else:
            return "fail"

    def _detect_gpu(self) -> Dict:
        """检测 GPU 信息"""
        gpu_info = {"available": False}
        try:
            if platform.system() == "Linux":
                result = subprocess.run(
                    ["lspci", "|", "grep", "-i", "nvidia"],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                if result.stdout:
                    gpu_info["available"] = True
                    gpu_info["model"] = result.stdout.strip()
        except Exception:
            pass
        return gpu_info

    def _get_nodejs_upgrade_commands(self) -> List[str]:
        """获取 Node.js 升级命令"""
        system = platform.system()
        if system == "Darwin":
            return [
                "brew install node@22",
                "brew link node@22"
            ]
        elif system == "Linux":
            return [
                "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash",
                "source ~/.bashrc",
                "nvm install 22",
                "nvm use 22"
            ]
        else:
            return [
                "访问 https://nodejs.org 下载 Node.js v22 LTS 安装包"
            ]


def print_report(results: Dict):
    """打印检测报告"""
    print("\n" + "="*60)
    print("OpenClaw 环境检测报告")
    print("="*60 + "\n")

    # 系统信息
    print("【系统信息】")
    print(f"操作系统: {results['system']['os']} {results['system']['release']}")
    print(f"架构: {results['system']['machine']}")
    print(f"Python: {results['system']['python_version']}")
    print(f"状态: {results['system']['status'].upper()}")
    if results['system'].get('reason'):
        print(f"原因: {results['system']['reason']}")
    print()

    # 硬件信息
    print("【硬件配置】")
    print(f"内存: {results['hardware']['memory_gb']} GB ({results['hardware']['memory_status']})")
    print(f"CPU: {results['hardware']['cpu_cores']} 核 ({results['hardware']['cpu_status']})")
    print(f"磁盘空间: {results['hardware']['free_disk_gb']} GB 可用 ({results['hardware']['disk_status']})")
    if results['hardware']['gpu']['available']:
        print(f"GPU: {results['hardware']['gpu'].get('model', '未知')}")
    print(f"硬件综合状态: {results['hardware']['status'].upper()}")
    print()

    # 软件依赖
    print("【软件依赖】")
    nodejs = results['software'].get('nodejs', {})
    if nodejs:
        print(f"Node.js: {nodejs.get('version', '未安装')} - {nodejs['status'].upper()}")
        if nodejs.get('reason'):
            print(f"  原因: {nodejs['reason']}")

    npm = results['software'].get('npm', {})
    print(f"npm: {npm.get('version', '未安装')}")

    git = results['software'].get('git', {})
    print(f"Git: {git.get('version', '未安装')}")

    openclaw = results['software'].get('openclaw', {})
    if openclaw.get('installed'):
        print(f"OpenClaw: {openclaw['version']} - 已安装")
    else:
        print(f"OpenClaw: 未安装")
    print()

    # 网络连接
    print("【网络连接】")
    npm_reg = results['network'].get('npm_registry', {})
    print(f"npm 源: {npm_reg.get('status', 'unknown').upper()} ({npm_reg.get('source', '未知')})")

    github = results['network'].get('github', {})
    print(f"GitHub: {github.get('status', 'unknown').upper()}")
    print()

    # 端口占用
    print("【端口占用】")
    port_info = results.get('ports', {})
    if port_info.get('occupied'):
        print(f"端口 {port_info['port']}: 被占用")
        print(f"  进程: {port_info['process']}")
    else:
        print(f"端口 {port_info['port']}: 可用")
    print()

    # 优化建议
    if results.get('recommendations'):
        print("【优化建议】")
        for idx, rec in enumerate(results['recommendations'], 1):
            priority_icon = {"high": "🔴", "medium": "🟡", "info": "🔵"}
            print(f"{idx}. {priority_icon.get(rec['priority'], '⚪')} [{rec['priority'].upper()}] {rec['issue']}")
            print(f"   解决方案: {rec['solution']}")
            if rec.get('commands'):
                print("   命令:")
                for cmd in rec['commands']:
                    print(f"     {cmd}")
            print()

    # 总体评估
    print("="*60)
    overall_status = evaluate_overall_status(results)
    print(f"总体评估: {overall_status['message']}")
    print("="*60)


def evaluate_overall_status(results: Dict) -> Dict:
    """评估总体状态"""
    critical_failures = []
    warnings = []

    # 检查关键项
    if results['system']['status'] == 'fail':
        critical_failures.append("系统不兼容")

    if results['hardware']['status'] == 'fail':
        critical_failures.append("硬件配置不足")

    if results['software'].get('nodejs', {}).get('status') == 'fail':
        critical_failures.append("Node.js 版本不满足要求")

    if results['network'].get('npm_registry', {}).get('status') == 'fail':
        critical_failures.append("网络连接问题")

    if results['hardware']['status'] == 'warning':
        warnings.append("硬件配置偏低")

    if results['system']['status'] == 'warning':
        warnings.append("系统版本建议升级")

    if critical_failures:
        return {
            "status": "fail",
            "message": "环境不满足安装要求，需要先解决以下问题:\n  - " + "\n  - ".join(critical_failures),
            "can_install": False
        }
    elif warnings:
        return {
            "status": "warning",
            "message": "环境基本满足要求，但有以下警告:\n  - " + "\n  - ".join(warnings),
            "can_install": True
        }
    else:
        return {
            "status": "pass",
            "message": "环境完全满足安装要求，可以开始安装 OpenClaw",
            "can_install": True
        }


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 环境检测工具")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果")
    parser.add_argument("--quiet", action="store_true", help="静默模式,仅输出 JSON")

    args = parser.parse_args()

    checker = EnvironmentChecker()
    results = checker.check_all()

    if args.json or args.quiet:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print_report(results)

    # 返回退出码
    overall = evaluate_overall_status(results)
    if overall['can_install']:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
