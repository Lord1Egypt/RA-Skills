#!/usr/bin/env python3
"""
OpenClaw 故障诊断工具
自动分析安装日志、服务状态、配置文件,定位常见问题
"""

import os
import sys
import json
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class OpenClawDiagnoser:
    """OpenClaw 诊断器"""

    def __init__(self):
        self.home_dir = Path.home()
        self.openclaw_dir = self.home_dir / ".openclaw"
        self.log_dir = self.openclaw_dir / "logs"
        self.config_file = self.openclaw_dir / "openclaw.json"

        self.issues = []
        self.diagnostics = {
            "timestamp": datetime.now().isoformat(),
            "system": {},
            "service": {},
            "configuration": {},
            "logs": {},
            "issues": []
        }

    def run_full_diagnosis(self, log_file: Optional[str] = None) -> Dict:
        """执行完整诊断"""
        print("开始诊断 OpenClaw...")

        self._check_service_status()
        self._check_configuration()
        self._analyze_logs(log_file)
        self._check_dependencies()
        self._check_network()
        self._check_permissions()

        self.diagnostics["issues"] = self.issues

        return self.diagnostics

    def _check_service_status(self):
        """检查服务状态"""
        print("检查服务状态...")

        service_status = {}

        # 检查 openclaw 命令
        try:
            result = subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                service_status["openclaw_installed"] = True
                service_status["version"] = result.stdout.strip()
            else:
                service_status["openclaw_installed"] = False
        except Exception:
            service_status["openclaw_installed"] = False

        # 检查网关服务
        try:
            result = subprocess.run(
                ["openclaw", "gateway", "status"],
                capture_output=True,
                text=True,
                timeout=10
            )
            service_status["gateway_output"] = result.stdout
            service_status["gateway_error"] = result.stderr

            if "running" in result.stdout.lower():
                service_status["gateway_running"] = True
            else:
                service_status["gateway_running"] = False
        except Exception as e:
            service_status["gateway_running"] = False
            service_status["gateway_check_error"] = str(e)

        # 检查端口占用
        port_status = self._check_port(18789)
        service_status["port_18789"] = port_status

        self.diagnostics["service"] = service_status

        # 分析问题
        if not service_status.get("openclaw_installed"):
            self.issues.append({
                "category": "service",
                "severity": "critical",
                "issue": "OpenClaw 未安装",
                "solution": "运行安装脚本: bash scripts/install_openclaw.sh"
            })

        if service_status.get("openclaw_installed") and not service_status.get("gateway_running"):
            self.issues.append({
                "category": "service",
                "severity": "high",
                "issue": "Gateway 服务未运行",
                "solution": "执行: openclaw gateway start"
            })

    def _check_configuration(self):
        """检查配置文件"""
        print("检查配置文件...")

        config_status = {
            "config_exists": False,
            "valid_json": False,
            "model_configured": False,
            "channels_configured": False
        }

        if self.config_file.exists():
            config_status["config_exists"] = True

            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                config_status["valid_json"] = True

                # 检查模型配置
                if "model" in config:
                    model = config["model"]
                    if "provider" in model and model["provider"]:
                        config_status["model_configured"] = True
                    else:
                        self.issues.append({
                            "category": "configuration",
                            "severity": "high",
                            "issue": "未配置 AI 模型",
                            "solution": "运行: openclaw configure --model"
                        })

                # 检查频道配置
                if "channels" in config:
                    channels = config["channels"]
                    if channels and len(channels) > 0:
                        config_status["channels_configured"] = True
                    else:
                        self.issues.append({
                            "category": "configuration",
                            "severity": "medium",
                            "issue": "未配置通讯频道",
                            "solution": "运行: openclaw channels login"
                        })

            except json.JSONDecodeError:
                config_status["valid_json"] = False
                self.issues.append({
                    "category": "configuration",
                    "severity": "critical",
                    "issue": "配置文件 JSON 格式错误",
                    "solution": "备份并重新生成配置文件"
                })
        else:
            self.issues.append({
                "category": "configuration",
                "severity": "high",
                "issue": "配置文件不存在",
                "solution": "运行: openclaw onboard"
            })

        self.diagnostics["configuration"] = config_status

    def _analyze_logs(self, log_file: Optional[str] = None):
        """分析日志文件"""
        print("分析日志文件...")

        log_analysis = {
            "log_files": [],
            "error_patterns": []
        }

        # 查找日志文件
        if log_file and Path(log_file).exists():
            log_files = [Path(log_file)]
        elif self.log_dir.exists():
            log_files = list(self.log_dir.glob("*.log"))
        else:
            log_files = []

        for log_path in log_files:
            log_files.append(str(log_path))

            try:
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # 搜索错误模式
                patterns = {
                    "EACCES": "权限不足",
                    "ENOENT": "文件或目录不存在",
                    "ETIMEDOUT": "网络超时",
                    "ECONNREFUSED": "连接被拒绝",
                    "ERR_UNSUPPORTED_DIR_IMPORT": "Node.js 版本过低",
                    "spawn EINVAL": "Windows 兼容性问题",
                    "permission denied": "权限被拒绝",
                    "Address already in use": "端口被占用"
                }

                for pattern, description in patterns.items():
                    if pattern in content:
                        log_analysis["error_patterns"].append({
                            "pattern": pattern,
                            "description": description,
                            "file": str(log_path)
                        })

                        # 生成问题报告
                        self._generate_issue_from_pattern(pattern, description)

            except Exception as e:
                log_analysis["error"] = str(e)

        self.diagnostics["logs"] = log_analysis

    def _check_dependencies(self):
        """检查依赖"""
        print("检查依赖...")

        dependencies = {
            "nodejs": self._get_command_version("node"),
            "npm": self._get_command_version("npm"),
            "git": self._get_command_version("git"),
            "python": self._get_command_version("python3")
        }

        # Node.js 版本检查
        node_version = dependencies.get("nodejs", "")
        if node_version:
            major_version = self._extract_major_version(node_version)
            if major_version < 22:
                self.issues.append({
                    "category": "dependencies",
                    "severity": "critical",
                    "issue": f"Node.js 版本过低 ({node_version})",
                    "solution": "升级到 Node.js v22 或更高版本"
                })

        self.diagnostics["dependencies"] = dependencies

    def _check_network(self):
        """检查网络"""
        print("检查网络...")

        network_status = {}

        # 检查 npm 源
        try:
            result = subprocess.run(
                ["npm", "config", "get", "registry"],
                capture_output=True,
                text=True,
                timeout=5
            )
            network_status["npm_registry"] = result.stdout.strip()

            # 测试连接
            try:
                import urllib.request
                urllib.request.urlopen(network_status["npm_registry"], timeout=3)
                network_status["npm_connection"] = "ok"
            except Exception:
                network_status["npm_connection"] = "failed"
                self.issues.append({
                    "category": "network",
                    "severity": "high",
                    "issue": "无法连接 npm 源",
                    "solution": "配置国内镜像或检查网络连接"
                })
        except Exception as e:
            network_status["npm_check_error"] = str(e)

        # 检查 GitHub
        try:
            import urllib.request
            urllib.request.urlopen("https://github.com/", timeout=3)
            network_status["github_connection"] = "ok"
        except Exception:
            network_status["github_connection"] = "failed"
            self.issues.append({
                "category": "network",
                "severity": "medium",
                "issue": "无法连接 GitHub",
                "solution": "配置代理或检查网络"
            })

        self.diagnostics["network"] = network_status

    def _check_permissions(self):
        """检查权限"""
        print("检查权限...")

        permissions = {}

        # 检查 openclaw 目录权限
        if self.openclaw_dir.exists():
            stat_info = self.openclaw_dir.stat()
            permissions["openclaw_dir_writable"] = os.access(self.openclaw_dir, os.W_OK)

            if not permissions["openclaw_dir_writable"]:
                self.issues.append({
                    "category": "permissions",
                    "severity": "critical",
                    "issue": f"{self.openclaw_dir} 不可写",
                    "solution": f"修复权限: chown -R $USER:$USER {self.openclaw_dir}"
                })
        else:
            permissions["openclaw_dir_exists"] = False

        self.diagnostics["permissions"] = permissions

    def _generate_issue_from_pattern(self, pattern: str, description: str):
        """根据错误模式生成问题报告"""
        if pattern in ["EACCES", "permission denied"]:
            self.issues.append({
                "category": "permissions",
                "severity": "high",
                "issue": description,
                "solution": "修复文件权限或使用 sudo 安装"
            })
        elif pattern == "ENOENT":
            self.issues.append({
                "category": "filesystem",
                "severity": "high",
                "issue": description,
                "solution": "检查文件路径或重新安装"
            })
        elif pattern == "ETIMEDOUT":
            self.issues.append({
                "category": "network",
                "severity": "high",
                "issue": description,
                "solution": "配置 npm 镜像源或检查网络"
            })
        elif pattern == "ERR_UNSUPPORTED_DIR_IMPORT":
            self.issues.append({
                "category": "dependencies",
                "severity": "critical",
                "issue": description,
                "solution": "升级 Node.js 到 v22+"
            })
        elif pattern == "Address already in use":
            self.issues.append({
                "category": "service",
                "severity": "medium",
                "issue": description,
                "solution": "终止占用进程或修改端口配置"
            })

    def _check_port(self, port: int) -> Dict:
        """检查端口占用"""
        port_info = {
            "port": port,
            "occupied": False,
            "process": None
        }

        try:
            if sys.platform == "darwin" or sys.platform.startswith("linux"):
                result = subprocess.run(
                    ["lsof", "-i", f":{port}"],
                    capture_output=True,
                    text=True
                )
                if result.stdout:
                    port_info["occupied"] = True
                    lines = result.stdout.strip().split("\n")[1:2]
                    if lines:
                        port_info["process"] = lines[0].strip()
            elif sys.platform == "win32":
                result = subprocess.run(
                    ["netstat", "-ano"],
                    capture_output=True,
                    text=True
                )
                if str(port) in result.stdout:
                    port_info["occupied"] = True
        except Exception:
            pass

        return port_info

    def _get_command_version(self, command: str) -> Optional[str]:
        """获取命令版本"""
        try:
            result = subprocess.run(
                [command, "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _extract_major_version(self, version_str: str) -> int:
        """提取主版本号"""
        match = re.search(r'(\d+)', version_str)
        if match:
            return int(match.group(1))
        return 0


def print_diagnosis_report(diagnostics: Dict):
    """打印诊断报告"""
    print("\n" + "="*70)
    print("OpenClaw 诊断报告")
    print("="*70 + "\n")

    # 服务状态
    print("【服务状态】")
    service = diagnostics.get("service", {})
    print(f"OpenClaw 已安装: {'是' if service.get('openclaw_installed') else '否'}")
    if service.get('openclaw_installed'):
        print(f"版本: {service.get('version', 'unknown')}")
    print(f"Gateway 运行中: {'是' if service.get('gateway_running') else '否'}")
    print(f"端口 18789: {'被占用' if service.get('port_18789', {}).get('occupied') else '可用'}")
    print()

    # 配置状态
    print("【配置状态】")
    config = diagnostics.get("configuration", {})
    print(f"配置文件存在: {'是' if config.get('config_exists') else '否'}")
    print(f"JSON 格式有效: {'是' if config.get('valid_json') else '否'}")
    print(f"模型已配置: {'是' if config.get('model_configured') else '否'}")
    print(f"频道已配置: {'是' if config.get('channels_configured') else '否'}")
    print()

    # 日志分析
    print("【日志分析】")
    logs = diagnostics.get("logs", {})
    log_files = logs.get("log_files", [])
    if log_files:
        print(f"找到 {len(log_files)} 个日志文件")
    error_patterns = logs.get("error_patterns", [])
    if error_patterns:
        print(f"检测到 {len(error_patterns)} 个错误模式:")
        for pattern in error_patterns:
            print(f"  - {pattern['description']} ({pattern['pattern']})")
    else:
        print("未检测到错误模式")
    print()

    # 依赖状态
    print("【依赖状态】")
    deps = diagnostics.get("dependencies", {})
    for name, version in deps.items():
        print(f"{name}: {version if version else '未安装'}")
    print()

    # 问题列表
    issues = diagnostics.get("issues", [])
    if issues:
        print("【检测到的问题】")
        severity_order = ["critical", "high", "medium", "low"]
        severity_icons = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }

        for issue in sorted(issues, key=lambda x: severity_order.index(x["severity"])):
            icon = severity_icons.get(issue["severity"], "⚪")
            print(f"{icon} [{issue['severity'].upper()}] {issue['issue']}")
            print(f"   解决方案: {issue['solution']}")
            print()
    else:
        print("【检测到的问题】")
        print("✅ 未检测到问题")
        print()

    print("="*70)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 故障诊断工具")
    parser.add_argument("--log", help="指定要分析的日志文件路径")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式结果")
    parser.add_argument("--fix", action="store_true", help="诊断后自动修复")

    args = parser.parse_args()

    diagnoser = OpenClawDiagnoser()
    diagnostics = diagnoser.run_full_diagnosis(args.log)

    if args.json:
        print(json.dumps(diagnostics, indent=2, ensure_ascii=False))
    else:
        print_diagnosis_report(diagnostics)

    # 自动修复
    if args.fix:
        print("\n尝试自动修复问题...")
        from fix_issues import OpenClawFixer
        fixer = OpenClawFixer()
        fixer.auto_fix(diagnostics["issues"])

    # 返回退出码
    critical_issues = [i for i in diagnostics["issues"] if i["severity"] == "critical"]
    if critical_issues:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
