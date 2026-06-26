"""
PAO - Personal AI Operating System

跨设备、去中心化的AI协同系统
"""

import sys
import argparse
import asyncio
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.system_integrator import PAOSystemIntegrator
from src.performance import performance_monitor, memory_optimizer
from deployment.installer import Installer
from deployment.updater import Updater
from deployment.config_wizard import ConfigWizard


def print_banner():
    """打印横幅"""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║     ██╗    ██╗███████╗██╗      ██████╗ ██████╗ ███╗   ███╗║
║     ██║    ██║██╔════╝██║     ██╔════╝██╔═══██╗████╗ ████║║
║     ██║ █╗ ██║█████╗  ██║     ██║     ██║   ██║██╔████╔██║║
║     ██║███╗██║██╔══╝  ██║     ██║     ██║   ██║██║╚██╔╝██║║
║     ╚███╔███╔╝███████╗███████╗╚██████╗╚██████╔╝██║ ╚═╝ ██║║
║      ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝║
║                                                           ║
║     Personal AI Operating System                          ║
║     跨设备、去中心化的AI协同系统                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


async def start_system():
    """启动系统"""
    print("[启动] 初始化PAO系统...")

    system = PAOSystemIntegrator()
    success = await system.initialize()

    if success:
        print(f"[启动] 系统初始化成功!")
        print(f"  设备ID: {system.status.device_id}")
        print(f"  技能数量: {system.status.skills_loaded}")
        print(f"  记忆数量: {system.status.memory_items}")

        # 显示内存使用
        mem_mb = memory_optimizer.get_current_memory_mb()
        print(f"  内存使用: {mem_mb:.2f}MB")

        return system
    else:
        print("[启动] 系统初始化失败!")
        return None


async def stop_system(system: PAOSystemIntegrator):
    """停止系统"""
    if system:
        print("[停止] 关闭PAO系统...")
        await system.stop()
        print("[停止] 系统已关闭")


def cmd_install():
    """安装命令"""
    print("[安装] 开始安装PAO系统...")
    installer = Installer()
    installer.install()


def cmd_update():
    """更新命令"""
    print("[更新] 检查更新...")
    updater = Updater()
    updater.update()


def cmd_config():
    """配置命令"""
    print("[配置] 运行配置向导...")
    wizard = ConfigWizard()
    wizard.run()


def cmd_status():
    """状态命令"""
    async def run():
        system = PAOSystemIntegrator()
        await system.initialize()

        print("=" * 40)
        print("PAO系统状态")
        print("=" * 40)
        print(f"设备ID: {system.status.device_id}")
        print(f"技能数量: {system.status.skills_loaded}")
        print(f"记忆数量: {system.status.memory_items}")
        print(f"同步状态: {system.status.sync_status}")
        print(f"错误数: {len(system.status.errors)}")

        mem_mb = memory_optimizer.get_current_memory_mb()
        print(f"内存使用: {mem_mb:.2f}MB")

        print("=" * 40)

        await system.stop()

    asyncio.run(run())


def cmd_demo():
    """演示命令"""
    async def run():
        print("[演示] 运行系统演示...")

        system = PAOSystemIntegrator()
        await system.initialize()

        # 技能演示
        print("\n[演示] 技能管理演示")
        skills = await system.search_skills("python")
        print(f"  搜索到 {len(skills)} 个Python相关技能")

        # 记忆演示
        print("\n[演示] 记忆系统演示")
        memory_id = await system.store_memory(
            "demo_memory",
            {"content": "这是一个演示记忆", "timestamp": "2026-04-16"},
            priority=3
        )
        print(f"  存储记忆: {memory_id[:8]}...")

        memories = await system.retrieve_memories("演示")
        print(f"  检索到 {len(memories)} 条相关记忆")

        # 上下文演示
        print("\n[演示] 上下文感知演示")
        context = await system.get_current_context()
        print(f"  上下文类型: {len(context.get('contexts', []))} 种")

        print("\n[演示] 演示完成!")

        await system.stop()

    asyncio.run(run())


def main():
    """主入口"""
    parser = argparse.ArgumentParser(
        description="PAO - Personal AI Operating System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # start命令
    subparsers.add_parser("start", help="启动PAO系统")

    # install命令
    subparsers.add_parser("install", help="安装PAO系统")

    # update命令
    subparsers.add_parser("update", help="检查并安装更新")

    # config命令
    subparsers.add_parser("config", help="运行配置向导")

    # status命令
    subparsers.add_parser("status", help="查看系统状态")

    # demo命令
    subparsers.add_parser("demo", help="运行系统演示")

    # stop命令
    subparsers.add_parser("stop", help="停止PAO系统")

    args = parser.parse_args()

    print_banner()

    if args.command == "install":
        cmd_install()
    elif args.command == "update":
        cmd_update()
    elif args.command == "config":
        cmd_config()
    elif args.command == "status":
        cmd_status()
    elif args.command == "demo":
        cmd_demo()
    elif args.command == "start":
        async def run_start():
            system = await start_system()
            if system:
                print("\n[信息] 系统正在运行，按 Ctrl+C 停止...")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    await stop_system(system)
        asyncio.run(run_start())
    elif args.command == "stop":
        print("[信息] 使用 start 命令启动系统后，按 Ctrl+C 停止")
    else:
        # 默认显示状态
        cmd_status()


if __name__ == "__main__":
    main()
