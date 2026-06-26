#!/usr/bin/env python3
"""
OpenClaw 自动修复工具
自动修复常见的安装和配置问题
支持 Windows/Linux/macOS 三大平台
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class OpenClawFixer:
    """OpenClaw 修复器"""

    def __init__(self):
        self.home_dir = Path.home()
        self.openclaw_dir = self.home_dir / ".openclaw"
        self.backup_dir = self.home_dir / "openclaw-backup"
        self.log_file = self.openclaw_dir / "fix_log.txt"

        self.fix_results = []

    def auto_fix(self, issues: List[Dict]):
        """自动修复问题"""
        if not issues:
            print("✅ 没有需要修复的问题")
            return True

        print(f"\n检测到 {len(issues)} 个问题,开始自动修复...\n")

        # 按严重程度排序
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_issues = sorted(issues, key=lambda x: severity_order.get(x["severity"], 99))

        for issue in sorted_issues:
            print(f"修复: {issue['issue']}")

            try:
                if issue["category"] == "dependencies":
                    success = self._fix_dependencies(issue)
                elif issue["category"] == "permissions":
                    success = self._fix_permissions(issue)
                elif issue["category"] == "network":
                    success = self._fix_network(issue)
                elif issue["category"] == "configuration":
                    success = self._fix_configuration(issue)
                elif issue["category"] == "service":
                    success = self._fix_service(issue)
                elif issue["category"] == "filesystem":
                    success = self._fix_filesystem(issue)
                else:
                    success = False

                self.fix_results.append({
                    "issue": issue["issue"],
                    "success": success
                })

                if success:
                    print("  ✅ 修复成功")
                else:
                    print(f"  ❌ 修复失败,请手动执行: {issue['solution']}")

            except Exception as e:
                print(f"  ❌ 修复失败: {e}")
                self.fix_results.append({
                    "issue": issue["issue"],
                    "success": False,
                    "error": str(e)
                })

            print()

        # 输出修复总结
        self._print_summary()

    def _fix_dependencies(self, issue: Dict) -> bool:
        """修复依赖问题"""
        if "Node.js" in issue["issue"]:
            return self._upgrade_nodejs()
        elif "Git" in issue["issue"]:
            return self._install_git()
        elif "Python" in issue["issue"]:
            return self._install_python()
        return False

    def _upgrade_nodejs(self) -> bool:
        """升级 Node.js"""
        print("  正在升级 Node.js...")

        system = sys.platform

        try:
            if system == "darwin":  # macOS
                # 使用 Homebrew
                subprocess.run(["brew", "install", "node@22"], check=True)
                subprocess.run(["brew", "link", "node@22"], check=True)

            elif system.startswith("linux"):
                # 使用 nvm
                nvm_dir = self.home_dir / ".nvm"
                if not nvm_dir.exists():
                    print("  安装 nvm...")
                    subprocess.run(
                        "curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash",
                        shell=True,
                        check=True
                    )

                # 安装 Node.js 22
                bash_rc = self.home_dir / ".bashrc"
                zsh_rc = self.home_dir / ".zshrc"

                if zsh_rc.exists():
                    shell = "zsh"
                    rc_file = zsh_rc
                else:
                    shell = "bash"
                    rc_file = bash_rc

                # 加载 nvm 并安装
                subprocess.run(
                    f'. {rc_file} && nvm install 22 && nvm use 22 && nvm alias default 22',
                    shell=True,
                    check=True
                )

            elif system == "win32":  # Windows
                print("  Windows 需要手动升级 Node.js")
                print("  请访问 https://nodejs.org 下载 v22 LTS 安装包")
                print("  或运行: .\\scripts\\install_openclaw.ps1")
                return False

            # 验证升级
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            version = result.stdout.strip()
            print(f"  Node.js 版本: {version}")

            return True

        except Exception as e:
            print(f"  升级失败: {e}")
            return False

    def _install_git(self) -> bool:
        """安装 Git"""
        print("  正在安装 Git...")

        system = sys.platform

        try:
            if system == "darwin":
                subprocess.run(["brew", "install", "git"], check=True)
            elif system.startswith("linux"):
                # 检测发行版
                if Path("/etc/debian_version").exists():
                    subprocess.run(["sudo", "apt-get", "install", "-y", "git"], check=True)
                elif Path("/etc/redhat-release").exists():
                    subprocess.run(["sudo", "yum", "install", "-y", "git"], check=True)
            elif system == "win32":
                # Windows 使用 winget 或 chocolatey
                if shutil.which("winget"):
                    subprocess.run(["winget", "install", "--id", "Git.Git", "-e", "--silent"], check=True)
                elif shutil.which("choco"):
                    subprocess.run(["choco", "install", "git", "-y"], check=True)
                else:
                    print("  请访问 https://git-scm.com/download/win 下载安装")
                    return False

            # 验证安装
            result = subprocess.run(["git", "--version"], capture_output=True, text=True)
            print(f"  {result.stdout.strip()}")

            return True

        except Exception as e:
            print(f"  安装失败: {e}")
            return False

    def _install_python(self) -> bool:
        """安装 Python"""
        print("  正在安装 Python...")

        system = sys.platform

        try:
            if system == "darwin":
                subprocess.run(["brew", "install", "python@3.11"], check=True)
            elif system.startswith("linux"):
                if Path("/etc/debian_version").exists():
                    subprocess.run(["sudo", "apt-get", "install", "-y", "python3.11"], check=True)
                elif Path("/etc/redhat-release").exists():
                    subprocess.run(["sudo", "yum", "install", "-y", "python3"], check=True)
            elif system == "win32":
                # Windows 使用 winget 或 chocolatey
                if shutil.which("winget"):
                    subprocess.run(
                        ["winget", "install", "Python.Python.3.11", "--silent"],
                        check=True
                    )
                elif shutil.which("choco"):
                    subprocess.run(["choco", "install", "python", "-y"], check=True)

            # 验证安装
            result = subprocess.run(["python3", "--version"], capture_output=True, text=True)
            print(f"  {result.stdout.strip()}")

            return True

        except Exception as e:
            print(f"  安装失败: {e}")
            return False

    def _fix_permissions(self, issue: Dict) -> bool:
        """修复权限问题"""
        print("  正在修复权限...")

        system = sys.platform

        try:
            if system == "win32":
                # Windows 权限处理
                print("  Windows 权限修复:以管理员身份运行 PowerShell")
                print("  或运行: .\\scripts\\install_openclaw.ps1 --reinstall")
                return False

            # Linux/macOS 权限修复
            # 修复 openclaw 目录权限
            if self.openclaw_dir.exists():
                subprocess.run(
                    ["chown", "-R", str(os.getlogin()), str(self.openclaw_dir)],
                    check=True
                )
                print(f"  修复 {self.openclaw_dir} 权限")

            # 修复 npm 全局目录权限
            try:
                npm_prefix = subprocess.check_output(
                    ["npm", "config", "get", "prefix"],
                    text=True
                ).strip()
            except:
                npm_prefix = ""

            if npm_prefix in ["/usr", "/usr/local"]:
                # 配置用户级安装目录
                user_npm_dir = self.home_dir / ".npm-global"
                user_npm_dir.mkdir(exist_ok=True)

                subprocess.run(
                    ["npm", "config", "set", "prefix", str(user_npm_dir)],
                    check=True
                )

                # 添加到 PATH
                shell_rc = self.home_dir / ".zshrc" if (self.home_dir / ".zshrc").exists() else self.home_dir / ".bashrc"

                with open(shell_rc, 'a') as f:
                    if f".npm-global/bin" not in shell_rc.read_text():
                        f.write(f"\nexport PATH=\"$HOME/.npm-global/bin:$PATH\"\n")

                print(f"  配置用户级 npm 目录: {user_npm_dir}")

            return True

        except Exception as e:
            print(f"  修复失败: {e}")
            return False

    def _fix_network(self, issue: Dict) -> bool:
        """修复网络问题"""
        print("  正在修复网络配置...")

        try:
            # 配置国内镜像源
            subprocess.run(
                ["npm", "config", "set", "registry", "https://registry.npmmirror.com"],
                check=True
            )
            print("  已配置 npm 国内镜像源")

            # 清理 npm 缓存
            subprocess.run(["npm", "cache", "clean", "--force"], check=True)
            print("  已清理 npm 缓存")

            return True

        except Exception as e:
            print(f"  修复失败: {e}")
            return False

    def _fix_configuration(self, issue: Dict) -> bool:
        """修复配置问题"""
        print("  正在修复配置...")

        try:
            if "配置文件不存在" in issue["issue"]:
                # 运行 onboard 向导
                subprocess.run(["openclaw", "onboard"], check=True)

            elif "JSON 格式错误" in issue["issue"]:
                # 备份并删除损坏的配置
                backup_path = self.backup_dir / f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json.bak"
                shutil.copy(self.config_file, backup_path)
                print(f"  已备份损坏的配置到: {backup_path}")

                # 重新初始化配置
                self.config_file.unlink()
                subprocess.run(["openclaw", "onboard"], check=True)

            elif "未配置 AI 模型" in issue["issue"]:
                print("  请手动运行: openclaw configure --model")
                return False

            elif "未配置通讯频道" in issue["issue"]:
                print("  请手动运行: openclaw channels login")
                return False

            return True

        except Exception as e:
            print(f"  修复失败: {e}")
            return False

    def _fix_service(self, issue: Dict) -> bool:
        """修复服务问题"""
        print("  正在修复服务...")

        try:
            if "Gateway 服务未运行" in issue["issue"]:
                # 启动 Gateway
                subprocess.run(["openclaw", "gateway", "start"], check=True)
                print("  Gateway 已启动")

            elif "OpenClaw 未安装" in issue["issue"]:
                # 运行安装脚本
                system = sys.platform
                if system == "win32":
                    install_script = Path(__file__).parent / "install_openclaw.ps1"
                    subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", str(install_script)], check=True)
                else:
                    install_script = Path(__file__).parent / "install_openclaw.sh"
                    subprocess.run(["bash", str(install_script)], check=True)
                print("  OpenClaw 已安装")

            elif "端口被占用" in issue["issue"]:
                # 检查占用进程
                if sys.platform == "win32":
                    # Windows
                    result = subprocess.run(
                        ["netstat", "-ano"],
                        capture_output=True,
                        text=True
                    )
                    if "18789" in result.stdout:
                        print("  请手动终止占用进程:")
                        print("  1. 查找进程: netstat -ano | findstr :18789")
                        print("  2. 终止进程: taskkill /PID <进程ID> /F")
                        return False
                else:
                    # Linux/macOS
                    result = subprocess.run(
                        ["lsof", "-i", ":18789"],
                        capture_output=True,
                        text=True
                    )

                    if result.stdout:
                        lines = result.stdout.strip().split("\n")[1:]
                        if lines:
                            pid = lines[0].split()[1]
                            print(f"  检测到占用进程 PID: {pid}")

                            # 终止进程
                            subprocess.run(["kill", pid], check=True)
                            print(f"  已终止进程 {pid}")

                            # 启动服务
                            subprocess.run(["openclaw", "gateway", "start"], check=True)
                            print("  Gateway 已重新启动")

            return True

        except Exception as e:
            print(f"  修复失败: {e}")
            return False

    def _fix_filesystem(self, issue: Dict) -> bool:
        """修复文件系统问题"""
        print("  正在修复文件系统问题...")

        try:
            if "文件或目录不存在" in issue["issue"]:
                # 重新安装 OpenClaw
                subprocess.run(["npm", "install", "-g", "openclaw@latest"], check=True)
                print("  OpenClaw 已重新安装")

            return True

        except Exception as e:
            print(f"  修复失败: {e}")
            return False

    def _print_summary(self):
        """打印修复总结"""
        print("\n" + "="*70)
        print("修复总结")
        print("="*70 + "\n")

        total = len(self.fix_results)
        successful = sum(1 for r in self.fix_results if r["success"])
        failed = total - successful

        print(f"总计: {total} 个问题")
        print(f"✅ 成功: {successful} 个")
        print(f"❌ 失败: {failed} 个")

        if failed > 0:
            print("\n失败的修复:")
            for result in self.fix_results:
                if not result["success"]:
                    print(f"  - {result['issue']}")
                    if "error" in result:
                        print(f"    错误: {result['error']}")

        print("\n" + "="*70)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 自动修复工具")
    parser.add_argument("--fix-all", action="store_true", help="修复所有检测到的问题")
    parser.add_argument("--fix", help="修复特定类别的问题 (dependencies/permissions/network/config/service)")
    parser.add_argument("--backup", action="store_true", help="创建备份")
    parser.add_argument("--restore", help="从备份恢复 (指定备份文件路径)")

    args = parser.parse_args()

    fixer = OpenClawFixer()

    if args.restore:
        # 恢复备份
        backup_path = Path(args.restore)
        if backup_path.exists():
            print(f"从备份恢复: {backup_path}")
            shutil.copy(backup_path, fixer.config_file)
            print("✅ 恢复成功")
        else:
            print(f"❌ 备份文件不存在: {backup_path}")
        sys.exit(0)

    if args.backup:
        # 创建备份
        backup_dir = fixer.backup_dir
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"full_backup_{timestamp}"

        if fixer.openclaw_dir.exists():
            shutil.copytree(fixer.openclaw_dir, backup_path)
            print(f"✅ 已创建备份: {backup_path}")
        else:
            print("❌ OpenClaw 目录不存在")
        sys.exit(0)

    if args.fix_all:
        # 先运行诊断
        from diagnose import OpenClawDiagnoser
        diagnoser = OpenClawDiagnoser()
        diagnostics = diagnoser.run_full_diagnosis()

        # 修复所有问题
        fixer.auto_fix(diagnostics["issues"])

    elif args.fix:
        # 修复特定类别
        from diagnose import OpenClawDiagnoser
        diagnoser = OpenClawDiagnoser()
        diagnostics = diagnoser.run_full_diagnosis()

        # 筛选指定类别
        issues = [i for i in diagnostics["issues"] if i["category"] == args.fix]

        if issues:
            fixer.auto_fix(issues)
        else:
            print(f"未找到类别 '{args.fix}' 的问题")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
