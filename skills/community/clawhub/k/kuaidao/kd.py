#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快导(KD) - 短视频脚本批量生成与管理

使用方法:
    kd run --platform xiaohongshu              # 执行完整任务链
    kd step --platform xiaohongshu --step 6    # 执行单个子任务
    kd rules --platform xiaohongshu            # 更新平台规则
    kd config show                             # 查看配置
"""

import sys
import os
import argparse
from pathlib import Path

# Windows 编码修复 - 必须在所有导入之前
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 添加scripts目录到路径
SCRIPT_DIR = Path(__file__).parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from config_manager import ConfigManager
from script_generator import ScriptGenerator


def main():
    parser = argparse.ArgumentParser(
        description="快导(KD) - 短视频脚本批量生成与管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    kd run --platform xiaohongshu                    # 执行完整任务链
    kd run --platform xiaohongshu --duration "2-3min" # 指定时长
    kd step --platform xiaohongshu --step 6          # 执行单个子任务
    kd rules --platform xiaohongshu                  # 更新平台规则
    kd config show                                   # 查看配置
    kd config validate                               # 验证配置
    kd config set-keywords --platform xiaohongshu --keywords "美食,探店"
    kd config set-external-keywords --keywords "food,cooking"
    kd config set copy_library_path "F:\\文案库\\"
    kd config set report_space_id "7627134963053235418"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # run 命令
    run_parser = subparsers.add_parser("run", help="执行完整任务链（10步）")
    run_parser.add_argument("--platform", required=True, 
                           choices=["xiaohongshu", "douyin", "shipinhao"],
                           help="目标平台")
    run_parser.add_argument("--duration", 
                           help="总时长（如：2-3min, 1min）")
    run_parser.add_argument("--count", type=int, default=5,
                           help="生成脚本数量（默认5）")
    
    # step 命令
    step_parser = subparsers.add_parser("step", help="执行单个子任务")
    step_parser.add_argument("--platform", required=True,
                            choices=["xiaohongshu", "douyin", "shipinhao"],
                            help="目标平台")
    step_parser.add_argument("--step", type=int, required=True,
                            choices=range(1, 11),
                            help="子任务编号（1-10）")
    
    # rules 命令
    rules_parser = subparsers.add_parser("rules", help="更新平台规则")
    rules_parser.add_argument("--platform", required=True,
                             choices=["xiaohongshu", "douyin", "shipinhao"],
                             help="目标平台")
    
    # config 命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_subparsers = config_parser.add_subparsers(dest="config_cmd")
    
    # config show
    show_parser = config_subparsers.add_parser("show", help="查看配置")
    show_parser.add_argument("--platform",
                            choices=["xiaohongshu", "douyin", "shipinhao"],
                            help="指定平台")
    
    # config validate
    validate_parser = config_subparsers.add_parser("validate", help="验证配置")
    validate_parser.add_argument("--platform",
                                 choices=["xiaohongshu", "douyin", "shipinhao"],
                                 help="指定平台")
    
    # config set
    set_parser = config_subparsers.add_parser("set", help="设置配置项")
    set_parser.add_argument("key", help="配置键名")
    set_parser.add_argument("value", help="配置值")
    
    # config set-keywords
    keywords_parser = config_subparsers.add_parser("set-keywords", help="设置平台关键词")
    keywords_parser.add_argument("--platform", required=True,
                                choices=["xiaohongshu", "douyin", "shipinhao"],
                                help="目标平台")
    keywords_parser.add_argument("--keywords", required=True,
                                help="关键词列表（逗号分隔）")
    
    # config set-external-keywords
    ext_keywords_parser = config_subparsers.add_parser("set-external-keywords",
                                                         help="设置外网关键词")
    ext_keywords_parser.add_argument("--keywords", required=True,
                                    help="关键词列表（逗号分隔）")
    
    # refs 命令
    refs_parser = subparsers.add_parser("refs", help="文案库管理")
    refs_subparsers = refs_parser.add_subparsers(dest="refs_cmd")
    
    # refs show
    refs_show_parser = refs_subparsers.add_parser("show", help="查看文案库")
    refs_show_parser.add_argument("--platform", required=True,
                                 choices=["xiaohongshu", "douyin", "shipinhao"],
                                 help="目标平台")
    
    # setup 命令
    setup_parser = subparsers.add_parser("setup", help="安装和配置")
    setup_parser.add_argument("--check-deps", action="store_true",
                             help="检查依赖")
    setup_parser.add_argument("--install-deps", action="store_true",
                             help="安装依赖")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # 处理命令
    if args.command == "run":
        return cmd_run(args)
    elif args.command == "step":
        return cmd_step(args)
    elif args.command == "rules":
        return cmd_rules(args)
    elif args.command == "config":
        return cmd_config(args)
    elif args.command == "refs":
        return cmd_refs(args)
    elif args.command == "setup":
        return cmd_setup(args)
    
    return 0


def cmd_run(args):
    """执行完整任务链"""
    print(f"🚀 启动快导系列任务")
    print(f"   平台: {args.platform}")
    if args.duration:
        print(f"   时长: {args.duration}")
    print(f"   脚本数: {args.count}")
    print()
    
    # TODO: 实现完整任务链
    print("⚠️  完整任务链执行功能开发中...")
    print("   当前可用: kd step --platform {} --step <编号>".format(args.platform))
    
    return 0


def cmd_step(args):
    """执行单个子任务"""
    print(f"🚀 执行子任务 {args.step}")
    print(f"   平台: {args.platform}")
    print()
    
    # TODO: 实现单个子任务执行
    step_names = {
        1: "搜索目标平台爆款",
        2: "读取平台规则",
        3: "搜索外网平台",
        4: "同质化检查",
        5: "格式检查",
        6: "生成脚本",
        7: "合理性检查",
        8: "更新文案库",
        9: "全面检查对比",
        10: "提交报告"
    }
    
    print(f"   任务: {step_names.get(args.step, '未知')}")
    print("⚠️  单个子任务执行功能开发中...")
    print("   当前可用Python API:")
    print("   from kd import ScriptGenerator")
    print("   gen = ScriptGenerator(platform='{}')".format(args.platform))
    
    return 0


def cmd_rules(args):
    """更新平台规则"""
    print(f"📝 更新平台规则")
    print(f"   平台: {args.platform}")
    print()
    
    # TODO: 实现规则更新
    print("⚠️  规则更新功能开发中...")
    print("   请手动编辑: references/platform_rules/{}_rules.md".format(args.platform))
    
    return 0


def cmd_config(args):
    """配置管理"""
    config = ConfigManager()
    
    if not hasattr(args, 'config_cmd') or not args.config_cmd:
        print("📋 配置管理")
        print()
        print("可用子命令:")
        print("   kd config show              查看配置")
        print("   kd config validate          验证配置")
        print("   kd config set <key> <val>   设置配置")
        print("   kd config set-keywords      设置平台关键词")
        print("   kd config set-external-keywords 设置外网关键词")
        return 0
    
    if args.config_cmd == "show":
        print("📋 当前配置")
        print()
        print(config.get_all())
        
    elif args.config_cmd == "validate":
        print("✅ 验证配置")
        print()
        # TODO: 实现配置验证
        print("⚠️  配置验证功能开发中...")
        
    elif args.config_cmd == "set":
        print(f"⚙️  设置配置: {args.key} = {args.value}")
        # TODO: 实现配置设置
        print("⚠️  配置设置功能开发中...")
        
    elif args.config_cmd == "set-keywords":
        keywords = [k.strip() for k in args.keywords.split(",")]
        print(f"⚙️  设置 {args.platform} 关键词: {keywords}")
        # TODO: 实现关键词设置
        print("⚠️  关键词设置功能开发中...")
        print("   请手动编辑: config/platforms.json")
        
    elif args.config_cmd == "set-external-keywords":
        keywords = [k.strip() for k in args.keywords.split(",")]
        print(f"⚙️  设置外网关键词: {keywords}")
        # TODO: 实现外网关键词设置
        print("⚠️  外网关键词设置功能开发中...")
        print("   请手动编辑: config/platforms.json")
    
    return 0


def cmd_refs(args):
    """文案库管理"""
    if not hasattr(args, 'refs_cmd') or not args.refs_cmd:
        print("📚 文案库管理")
        print()
        print("可用子命令:")
        print("   kd refs show --platform <平台>  查看文案库")
        return 0
    
    if args.refs_cmd == "show":
        print(f"📚 查看 {args.platform} 文案库")
        print()
        # TODO: 实现文案库查看
        print("⚠️  文案库查看功能开发中...")
    
    return 0


def cmd_setup(args):
    """安装和配置"""
    print("🔧 安装和配置")
    print()
    
    if args.check_deps:
        print("检查依赖...")
        # TODO: 实现依赖检查
        print("⚠️  依赖检查功能开发中...")
        
    elif args.install_deps:
        print("安装依赖...")
        # TODO: 实现依赖安装
        print("⚠️  依赖安装功能开发中...")
        print("   请手动安装: pip install openpyxl")
        
    else:
        print("首次使用配置指南:")
        print()
        print("1. 设置文案库路径:")
        print('   kd config set copy_library_path "F:\\vlog\\JT\\idea\\"')
        print()
        print("2. 设置飞书空间ID:")
        print("   kd config set report_space_id \"你的空间ID\"")
        print()
        print("3. 配置平台关键词:")
        print("   kd config set-keywords --platform xiaohongshu \\")
        print('     --keywords "美食,探店,农家菜,采摘"')
        print()
        print("4. 验证配置:")
        print("   kd config validate")
        print()
        print("5. 执行快导任务:")
        print("   kd run --platform xiaohongshu")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
