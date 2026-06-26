#!/usr/bin/env python3
"""
OpenClaw 数据备份工具

备份内容:
1. openclaw.json(主配置文件)
2. workspace/(工作空间)
3. agents/(多代理配置)
4. cron/(定时任务)
5. media/(媒体缓存)

使用方法:
    python backup.py              # 执行备份
    python backup.py --list       # 列出已有备份
    python backup.py --output /path  # 指定输出目录
"""

import argparse
import json
import os
import shutil
import sys
import tarfile
from datetime import datetime
from pathlib import Path


def find_openclaw_dir():
    """自动检测 OpenClaw 目录"""
    # 默认路径
    default_path = Path.home() / ".openclaw"

    if default_path.exists():
        return default_path

    # 检查环境变量
    env_path = os.environ.get("OPENCLAW_DIR")
    if env_path and Path(env_path).exists():
        return Path(env_path)

    print("❌ 错误:未找到 OpenClaw 目录")
    print("   请确保 OpenClaw 已安装,或设置 OPENCLAW_DIR 环境变量")
    sys.exit(1)


def get_backup_items(openclaw_dir):
    """获取备份项目列表"""
    return [
        {
            "name": "openclaw.json",
            "path": openclaw_dir / "openclaw.json",
            "type": "file",
            "desc": "主配置文件",
        },
        {
            "name": "workspace",
            "path": openclaw_dir / "workspace",
            "type": "dir",
            "desc": "工作空间(MEMORY.md、Skills等)",
        },
        {
            "name": "agents",
            "path": openclaw_dir / "agents",
            "type": "dir",
            "desc": "多代理配置",
        },
        {
            "name": "cron",
            "path": openclaw_dir / "cron",
            "type": "dir",
            "desc": "定时任务数据",
        },
        {
            "name": "media",
            "path": openclaw_dir / "media",
            "type": "dir",
            "desc": "媒体缓存",
        },
    ]


def print_banner():
    """打印横幅"""
    print("\n" + "=" * 60)
    print("📦 OpenClaw 数据备份工具")
    print("=" * 60 + "\n")


def print_backup_info(openclaw_dir):
    """打印备份信息"""
    items = get_backup_items(openclaw_dir)

    print("📋 备份内容:\n")
    print(f"{'目录/文件':<20} {'状态':<10} {'说明'}")
    print("-" * 60)

    for item in items:
        exists = "✅ 存在" if item["path"].exists() else "❌ 不存在"
        print(f"{item['name']:<20} {exists:<10} {item['desc']}")

    print()


def backup(openclaw_dir, output_dir=None, quiet=False):
    """执行备份"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_filename = f"OpenClaw-Backup-YYC-{timestamp}.tar.gz"

    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = openclaw_dir

    backup_file = output_path / backup_filename

    if not quiet:
        print_banner()
        print(f"📁 OpenClaw 目录: {openclaw_dir}\n")
        print_backup_info(openclaw_dir)

    # 创建临时目录
    temp_dir = openclaw_dir / f".backup-temp-{timestamp}"
    temp_dir.mkdir(exist_ok=True)

    items = get_backup_items(openclaw_dir)
    backed_up = []

    try:
        for item in items:
            if not item["path"].exists():
                if not quiet:
                    print(f"  ⚠️  跳过: {item['name']} (不存在)")
                continue

            dest = temp_dir / item["name"]

            if item["type"] == "file":
                # 文件:添加时间戳后缀
                if item["name"] == "openclaw.json":
                    shutil.copy2(item["path"], temp_dir / f"openclaw.json.{timestamp}")
                else:
                    shutil.copy2(item["path"], dest)
            else:
                # 目录:完整复制
                shutil.copytree(item["path"], dest)

            backed_up.append(item["name"])
            if not quiet:
                print(f"  ✅ 已备份: {item['name']}")

        # 打包压缩
        if not quiet:
            print(f"\n📦 正在打包压缩...")

        with tarfile.open(backup_file, "w:gz") as tar:
            for name in backed_up:
                item_path = temp_dir / name
                if item_path.exists():
                    tar.add(item_path, arcname=name)
                # 检查带时间戳的配置文件
                config_with_ts = temp_dir / f"openclaw.json.{timestamp}"
                if config_with_ts.exists():
                    tar.add(config_with_ts, arcname=f"openclaw.json.{timestamp}")

    finally:
        # 清理临时目录
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

    # 输出结果
    print("\n" + "=" * 60)
    print("✅ 备份完成！")
    print("=" * 60)
    print(f"\n📁 备份文件: {backup_file}")
    print(f"📦 文件大小: {backup_file.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"📅 备份时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 获取出口 IP（多个备用服务）
    import subprocess
    ip_services = [
        "https://ip.tag.gg/ip.php",
        "https://ifconfig.me",
        "https://api.ipify.org",
        "https://ip.sb",
        "https://myip.ipip.net",
        "https://ipinfo.io/ip",
    ]
    server_ip = "服务器IP"
    for service in ip_services:
        try:
            result = subprocess.run(['curl', '-s', '--connect-timeout', '3', service], capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                server_ip = result.stdout.strip()
                break
        except:
            continue

    print("\n" + "=" * 60)
    print("📥 SCP 下载命令")
    print("=" * 60)
    print(f"scp root@{server_ip}:{backup_file} ./")

    print("\n" + "⚠️ " * 20)
    print("\n【重要提醒】")
    print("1. 请立即下载备份文件到本地，避免服务器故障导致数据丢失")
    print("2. 本工具只备份 ~/.openclaw/ 目录下的默认文件")
    print("3. 如果您有其他自定义路径的数据，请自行确认备份")
    print("\n" + "⚠️ " * 20 + "\n")


def list_backups(openclaw_dir):
    """列出已有备份"""
    backups = sorted(openclaw_dir.glob("OpenClaw-Backup-YYC-*.tar.gz"), reverse=True)

    if not backups:
        print("暂无备份文件")
        return

    print("\n📋 已有备份:\n")
    print(f"{'文件名':<40} {'大小':<12} {'时间'}")
    print("-" * 70)

    for backup in backups:
        stat = backup.stat()
        size_mb = stat.st_size / 1024 / 1024
        mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{backup.name:<40} {size_mb:.2f} MB    {mtime}")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 数据备份工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python backup.py                  # 执行备份
  python backup.py --list           # 列出已有备份
  python backup.py --output /tmp    # 指定输出目录
        """
    )
    parser.add_argument("--list", action="store_true", help="列出已有备份")
    parser.add_argument("--output", "-o", help="指定输出目录")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")

    args = parser.parse_args()

    openclaw_dir = find_openclaw_dir()

    if args.list:
        list_backups(openclaw_dir)
    else:
        backup(openclaw_dir, args.output, args.quiet)


if __name__ == "__main__":
    main()