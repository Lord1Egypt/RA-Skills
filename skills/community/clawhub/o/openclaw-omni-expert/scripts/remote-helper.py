#!/usr/bin/env python3
"""
OpenClaw 远程安装助手
帮助远程安装、诊断和修复 OpenClaw
支持 SSH 连接、批量操作、安全验证
"""

import os
import sys
import json
import subprocess
import paramiko
import getpass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class RemoteHelper:
    """远程助手"""

    def __init__(self):
        self.connections = {}
        self.scripts_dir = Path(__file__).parent
        self.local_backup_dir = Path.home() / "openclaw-remote-backup"

    def add_host(self, hostname: str, username: str, port: int = 22,
                 password: Optional[str] = None, key_file: Optional[str] = None):
        """添加远程主机"""
        self.connections[hostname] = {
            "hostname": hostname,
            "username": username,
            "port": port,
            "password": password,
            "key_file": key_file
        }
        print(f"✓ 已添加主机: {username}@{hostname}:{port}")

    def connect(self, hostname: str) -> paramiko.SSHClient:
        """连接到远程主机"""
        if hostname not in self.connections:
            raise ValueError(f"未找到主机: {hostname}")

        config = self.connections[hostname]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if config["key_file"]:
                # 使用密钥认证
                private_key = paramiko.RSAKey.from_private_key_file(config["key_file"])
                ssh.connect(
                    hostname=config["hostname"],
                    port=config["port"],
                    username=config["username"],
                    pkey=private_key,
                    timeout=30
                )
            else:
                # 使用密码认证
                ssh.connect(
                    hostname=config["hostname"],
                    port=config["port"],
                    username=config["username"],
                    password=config["password"],
                    timeout=30
                )

            print(f"✓ 已连接到: {config['username']}@{config['hostname']}")
            return ssh

        except Exception as e:
            print(f"✗ 连接失败: {e}")
            raise

    def execute_command(self, ssh: paramiko.SSHClient, command: str,
                       timeout: int = 300) -> Tuple[int, str, str]:
        """执行远程命令"""
        print(f"执行: {command}")

        stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
        exit_code = stdout.channel.recv_exit_status()
        output = stdout.read().decode('utf-8', errors='ignore')
        error = stderr.read().decode('utf-8', errors='ignore')

        return exit_code, output, error

    def upload_file(self, ssh: paramiko.SSHClient, local_path: str,
                   remote_path: str) -> bool:
        """上传文件到远程主机"""
        print(f"上传: {local_path} -> {remote_path}")

        try:
            sftp = ssh.open_sftp()
            sftp.put(local_path, remote_path)
            sftp.close()
            print(f"✓ 上传成功")
            return True
        except Exception as e:
            print(f"✗ 上传失败: {e}")
            return False

    def download_file(self, ssh: paramiko.SSHClient, remote_path: str,
                     local_path: str) -> bool:
        """从远程主机下载文件"""
        print(f"下载: {remote_path} -> {local_path}")

        try:
            sftp = ssh.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
            print(f"✓ 下载成功")
            return True
        except Exception as e:
            print(f"✗ 下载失败: {e}")
            return False

    def check_environment(self, hostname: str):
        """检查远程环境"""
        print(f"\n{'='*60}")
        print(f"检查远程环境: {hostname}")
        print(f"{'='*60}\n")

        ssh = self.connect(hostname)

        try:
            # 检测操作系统
            print("检测操作系统...")
            exit_code, output, error = self.execute_command(ssh, "uname -a")
            if exit_code == 0:
                print(f"✓ 操作系统: {output.strip()}")
            else:
                print(f"✗ 检测失败: {error}")

            # 检查 Node.js
            print("\n检查 Node.js...")
            exit_code, output, error = self.execute_command(ssh, "node --version 2>/dev/null || echo 'not installed'")
            if exit_code == 0:
                version = output.strip()
                if "not installed" in version:
                    print(f"✗ Node.js 未安装")
                else:
                    print(f"✓ Node.js: {version}")
                    # 检查版本是否满足要求
                    major = int(version.replace('v', '').split('.')[0]) if 'v' in version else 0
                    if major < 22:
                        print(f"⚠ 版本过低,需要 v22+")
            else:
                print(f"✗ 检查失败: {error}")

            # 检查 Git
            print("\n检查 Git...")
            exit_code, output, error = self.execute_command(ssh, "git --version 2>/dev/null || echo 'not installed'")
            if exit_code == 0:
                version = output.strip()
                if "not installed" in version:
                    print(f"✗ Git 未安装")
                else:
                    print(f"✓ Git: {version}")
            else:
                print(f"✗ 检测失败: {error}")

            # 检查 OpenClaw
            print("\n检查 OpenClaw...")
            exit_code, output, error = self.execute_command(ssh, "openclaw --version 2>/dev/null || echo 'not installed'")
            if exit_code == 0:
                version = output.strip()
                if "not installed" in version:
                    print(f"✗ OpenClaw 未安装")
                else:
                    print(f"✓ OpenClaw: {version}")
            else:
                print(f"✗ 检测失败: {error}")

            # 检查内存
            print("\n检查内存...")
            exit_code, output, error = self.execute_command(ssh, "free -h 2>/dev/null || echo 'N/A'")
            if exit_code == 0:
                print(f"✓ 内存信息:\n{output}")
            else:
                print(f"⚠ 无法获取内存信息")

            # 检查磁盘空间
            print("\n检查磁盘空间...")
            exit_code, output, error = self.execute_command(ssh, "df -h ~ 2>/dev/null || echo 'N/A'")
            if exit_code == 0:
                print(f"✓ 磁盘空间:\n{output}")
            else:
                print(f"⚠ 无法获取磁盘信息")

        finally:
            ssh.close()

        print(f"\n{'='*60}")
        print(f"环境检查完成")
        print(f"{'='*60}\n")

    def remote_install(self, hostname: str, platform: str = "auto"):
        """远程安装 OpenClaw"""
        print(f"\n{'='*60}")
        print(f"远程安装 OpenClaw: {hostname}")
        print(f"{'='*60}\n")

        ssh = self.connect(hostname)

        try:
            # 自动检测平台
            if platform == "auto":
                print("检测目标平台...")
                exit_code, output, error = self.execute_command(ssh, "uname -s")
                if exit_code == 0:
                    os_name = output.strip().lower()
                    if os_name == "linux":
                        # 进一步检测发行版
                        exit_code, output, error = self.execute_command(
                            ssh, "cat /etc/os-release 2>/dev/null | grep -i '^ID=' | cut -d'=' -f2 | tr -d '\"'"
                        )
                        if exit_code == 0:
                            distro = output.strip()
                            print(f"✓ 检测到: {distro}")
                    elif os_name == "darwin":
                        platform = "macos"
                        print(f"✓ 检测到: macOS")
                    elif "mingw" in os_name or "msys" in os_name:
                        platform = "windows"
                        print(f"✓ 检测到: Windows (Git Bash)")
                else:
                    print(f"⚠ 无法检测平台,假设为 Linux")
                    platform = "linux"

            # 上传安装脚本
            print("\n上传安装脚本...")

            if platform == "windows":
                script_name = "install_openclaw.ps1"
                remote_script = "/tmp/install_openclaw.ps1"
            else:
                script_name = "install_openclaw.sh"
                remote_script = "/tmp/install_openclaw.sh"

            local_script = self.scripts_dir / script_name

            if not local_script.exists():
                print(f"✗ 本地脚本不存在: {local_script}")
                return

            if not self.upload_file(ssh, str(local_script), remote_script):
                return

            # 设置执行权限 (非 Windows)
            if platform != "windows":
                self.execute_command(ssh, f"chmod +x {remote_script}")

            # 执行安装
            print("\n开始远程安装 (这可能需要几分钟)...")
            print("-" * 60)

            if platform == "windows":
                # PowerShell 执行
                command = f"powershell -ExecutionPolicy Bypass -File {remote_script}"
            else:
                # Bash 执行
                command = f"bash {remote_script}"

            exit_code, output, error = self.execute_command(ssh, command, timeout=600)

            print("-" * 60)

            if exit_code == 0:
                print(f"\n✓ 安装成功!\n")
                print(output)
            else:
                print(f"\n✗ 安装失败 (退出码: {exit_code})\n")
                print("错误输出:")
                print(error)

            # 验证安装
            print("\n验证安装...")
            exit_code, output, error = self.execute_command(ssh, "openclaw --version 2>/dev/null")
            if exit_code == 0:
                print(f"✓ OpenClaw 版本: {output.strip()}")
            else:
                print(f"✗ 验证失败")

            # 清理临时文件
            print(f"\n清理临时文件: {remote_script}")
            self.execute_command(ssh, f"rm -f {remote_script}")

        finally:
            ssh.close()

        print(f"\n{'='*60}")
        print(f"远程安装完成")
        print(f"{'='*60}\n")

    def remote_diagnose(self, hostname: str, download_logs: bool = True):
        """远程诊断"""
        print(f"\n{'='*60}")
        print(f"远程诊断: {hostname}")
        print(f"{'='*60}\n")

        ssh = self.connect(hostname)

        try:
            # 上传诊断脚本
            diagnose_script = "diagnose.py"
            remote_script = "/tmp/diagnose.py"

            local_script = self.scripts_dir / diagnose_script

            if not self.upload_file(ssh, str(local_script), remote_script):
                return

            # 执行诊断
            print("运行诊断...")
            exit_code, output, error = self.execute_command(
                ssh, f"python3 {remote_script} --json", timeout=120
            )

            if exit_code == 0:
                print("\n✓ 诊断结果:")
                try:
                    diagnosis = json.loads(output)
                    print(json.dumps(diagnosis, indent=2, ensure_ascii=False))

                    # 保存到本地
                    self.local_backup_dir.mkdir(parents=True, exist_ok=True)
                    report_file = self.local_backup_dir / f"diagnosis_{hostname}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                    with open(report_file, 'w') as f:
                        json.dump(diagnosis, f, indent=2)
                    print(f"\n✓ 诊断报告已保存: {report_file}")

                except json.JSONDecodeError:
                    print(output)
            else:
                print(f"✗ 诊断失败: {error}")

            # 下载日志
            if download_logs:
                print("\n下载日志文件...")
                log_dir = Path.home() / ".openclaw" / "logs"
                remote_logs = [
                    "~/.openclaw/logs/gateway.err.log",
                    "~/.openclaw/logs/gateway.out.log",
                    "~/.openclaw/logs/install.log"
                ]

                for remote_log in remote_logs:
                    # 检查文件是否存在
                    exit_code, _, _ = self.execute_command(ssh, f"test -f {remote_log} && echo 'exists' || echo 'not exists'")

                    if "exists" in _:
                        log_name = Path(remote_log).name
                        local_log = self.local_backup_dir / f"{hostname}_{log_name}"
                        self.download_file(ssh, remote_log, str(local_log))
                    else:
                        print(f"  - {remote_log}: 不存在")

            # 清理
            self.execute_command(ssh, f"rm -f {remote_script}")

        finally:
            ssh.close()

        print(f"\n{'='*60}")
        print(f"远程诊断完成")
        print(f"{'='*60}\n")

    def remote_fix(self, hostname: str, fix_category: Optional[str] = None):
        """远程修复"""
        print(f"\n{'='*60}")
        print(f"远程修复: {hostname}")
        print(f"{'='*60}\n")

        ssh = self.connect(hostname)

        try:
            # 上传修复脚本
            fix_script = "fix_issues.py"
            remote_script = "/tmp/fix_issues.py"

            local_script = self.scripts_dir / fix_script

            if not self.upload_file(ssh, str(local_script), remote_script):
                return

            # 执行修复
            if fix_category:
                print(f"修复类别: {fix_category}")
                command = f"python3 {remote_script} --fix {fix_category}"
            else:
                print("修复所有问题...")
                command = f"python3 {remote_script} --fix-all"

            exit_code, output, error = self.execute_command(ssh, command, timeout=300)

            if exit_code == 0:
                print("\n✓ 修复成功!\n")
                print(output)
            else:
                print(f"\n✗ 修复失败\n")
                print(error)

            # 清理
            self.execute_command(ssh, f"rm -f {remote_script}")

        finally:
            ssh.close()

        print(f"\n{'='*60}")
        print(f"远程修复完成")
        print(f"{'='*60}\n")

    def batch_operation(self, hostnames: List[str], operation: str, **kwargs):
        """批量操作多台主机"""
        print(f"\n{'='*60}")
        print(f"批量操作: {operation}")
        print(f"目标主机: {len(hostnames)} 台")
        print(f"{'='*60}\n")

        results = {}

        for hostname in hostnames:
            try:
                print(f"\n[{hostname}] 开始处理...\n")
                results[hostname] = {"status": "success", "message": ""}

                if operation == "check":
                    self.check_environment(hostname)
                elif operation == "install":
                    self.remote_install(hostname, kwargs.get('platform', 'auto'))
                elif operation == "diagnose":
                    self.remote_diagnose(hostname, kwargs.get('download_logs', True))
                elif operation == "fix":
                    self.remote_fix(hostname, kwargs.get('fix_category'))

                results[hostname]["status"] = "success"
                results[hostname]["message"] = "操作成功"

            except Exception as e:
                print(f"✗ 失败: {e}\n")
                results[hostname] = {
                    "status": "failed",
                    "message": str(e)
                }

        # 输出汇总
        print(f"\n{'='*60}")
        print(f"批量操作完成")
        print(f"{'='*60}\n")

        success_count = sum(1 for r in results.values() if r["status"] == "success")
        failed_count = len(results) - success_count

        print(f"总计: {len(results)} 台")
        print(f"成功: {success_count} 台")
        print(f"失败: {failed_count} 台")

        if failed_count > 0:
            print("\n失败的主机:")
            for hostname, result in results.items():
                if result["status"] == "failed":
                    print(f"  - {hostname}: {result['message']}")

        print(f"\n{'='*60}\n")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 远程安装助手")
    parser.add_argument("operation", choices=["check", "install", "diagnose", "fix"],
                       help="操作类型")
    parser.add_argument("--host", help="远程主机 (格式: user@hostname 或 hostname)")
    parser.add_argument("--port", type=int, default=22, help="SSH 端口")
    parser.add_argument("--username", help="用户名")
    parser.add_argument("--password", help="密码 (不推荐,建议使用密钥)")
    parser.add_argument("--key-file", help="SSH 私钥文件路径")
    parser.add_argument("--platform", choices=["auto", "linux", "macos", "windows"],
                       default="auto", help="目标平台 (仅 install 需要)")
    parser.add_argument("--fix-category", help="修复类别 (仅 fix 需要)")
    parser.add_argument("--no-download-logs", action="store_true",
                       help="不下载日志 (仅 diagnose 需要)")
    parser.add_argument("--batch", help="批量操作的主机列表文件")

    args = parser.parse_args()

    helper = RemoteHelper()

    # 添加主机
    if args.batch:
        # 批量模式
        with open(args.batch, 'r') as f:
            hostnames = [line.strip() for line in f if line.strip()]

        for hostname in hostnames:
            if '@' in hostname:
                username, hostname = hostname.split('@', 1)
                helper.add_host(hostname, username, args.port, args.password, args.key_file)
            else:
                username = args.username or getpass.getpass(f"{hostname} 用户名: ")
                helper.add_host(hostname, username, args.port, args.password, args.key_file)

        helper.batch_operation(hostnames, args.operation,
                             platform=args.platform,
                             fix_category=args.fix_category,
                             download_logs=not args.no_download_logs)

    else:
        # 单机模式
        if not args.host:
            parser.error("--host 或 --batch 是必需的")

        # 解析主机
        if '@' in args.host:
            username, hostname = args.host.split('@', 1)
        else:
            hostname = args.host
            username = args.username or getpass.getpass(f"{hostname} 用户名: ")

        if not args.password and not args.key_file:
            args.password = getpass.getpass(f"{username}@{hostname} 密码: ")

        helper.add_host(hostname, username, args.port, args.password, args.key_file)

        # 执行操作
        if args.operation == "check":
            helper.check_environment(hostname)
        elif args.operation == "install":
            helper.remote_install(hostname, args.platform)
        elif args.operation == "diagnose":
            helper.remote_diagnose(hostname, not args.no_download_logs)
        elif args.operation == "fix":
            helper.remote_fix(hostname, args.fix_category)


if __name__ == "__main__":
    main()
