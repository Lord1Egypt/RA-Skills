#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 新手一站式引导 - 主脚本
环境检测、安装检查、Skills 推荐、渠道配置、使用教程
"""

import argparse
import subprocess
import sys
import os
import json
import platform
from datetime import datetime

# 颜色输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'━' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'━' * 60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.RESET}")

# 环境检测
def check_env():
    """检测系统环境"""
    print_header("🔍 环境检测报告")
    
    results = {}
    all_passed = True
    
    # Node.js 检测
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=5)
        node_version = result.stdout.strip()
        if node_version:
            print_success(f"Node.js: {node_version}")
            results['node'] = node_version
        else:
            print_error("Node.js: 未安装")
            all_passed = False
    except FileNotFoundError:
        print_error("Node.js: 未安装（需要 >= 18.0.0）")
        all_passed = False
    except Exception as e:
        print_error(f"Node.js: 检测失败 - {e}")
        all_passed = False
    
    # npm 检测
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True, timeout=5)
        npm_version = result.stdout.strip()
        if npm_version:
            print_success(f"npm: {npm_version}")
            results['npm'] = npm_version
        else:
            print_error("npm: 未安装")
            all_passed = False
    except FileNotFoundError:
        print_error("npm: 未安装（需要 >= 8.0.0）")
        all_passed = False
    except Exception as e:
        print_error(f"npm: 检测失败 - {e}")
        all_passed = False
    
    # 系统信息
    system = platform.system()
    release = platform.release()
    machine = platform.machine()
    print_success(f"系统：{system} {release} ({machine})")
    results['system'] = f"{system} {release} ({machine})"
    
    # Python 版本
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print_success(f"Python: {python_version}")
    results['python'] = python_version
    
    # 工作目录
    workspace = os.path.expanduser("~/.openclaw/workspace")
    if os.path.exists(workspace):
        print_success(f"工作目录：{workspace}")
        results['workspace'] = workspace
    else:
        print_warning(f"工作目录不存在：{workspace}")
        results['workspace'] = None
    
    # 结论
    print(f"\n{Colors.BOLD}📋 结论：{Colors.RESET}", end="")
    if all_passed:
        print_success("环境正常，可以安装/使用 OpenClaw")
    else:
        print_error("环境不完整，请先安装缺失的组件")
        print_info("安装 Node.js: https://nodejs.org/")
    
    return results, all_passed

# 安装状态检查
def check_install():
    """检查 OpenClaw 安装状态"""
    print_header("📦 OpenClaw 安装状态")
    
    results = {}
    all_good = True
    
    # OpenClaw CLI 检测
    try:
        result = subprocess.run(['openclaw', '--version'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print_success(f"OpenClaw CLI: 已安装 ({version})")
            results['cli'] = version
        else:
            print_error("OpenClaw CLI: 未安装")
            all_good = False
    except FileNotFoundError:
        print_error("OpenClaw CLI: 未安装")
        print_info("安装命令：npm install -g openclaw")
        all_good = False
    except Exception as e:
        print_error(f"OpenClaw CLI: 检测失败 - {e}")
        all_good = False
    
    # Gateway 状态
    try:
        result = subprocess.run(['openclaw', 'gateway', 'status'], capture_output=True, text=True, timeout=10)
        if 'running' in result.stdout.lower() or result.returncode == 0:
            print_success("Gateway: 运行中")
            results['gateway'] = 'running'
        else:
            print_warning("Gateway: 未运行")
            print_info("启动命令：openclaw gateway start")
            results['gateway'] = 'stopped'
    except Exception as e:
        print_warning(f"Gateway: 状态检测失败 - {e}")
        results['gateway'] = 'unknown'
    
    # Workspace 检查
    workspace = os.path.expanduser("~/.openclaw/workspace")
    if os.path.exists(workspace):
        print_success(f"Workspace: {workspace}")
        results['workspace'] = workspace
        
        # 检查关键文件
        key_files = ['SOUL.md', 'AGENTS.md', 'TOOLS.md']
        for file in key_files:
            filepath = os.path.join(workspace, file)
            if os.path.exists(filepath):
                print_success(f"  └─ {file}: 存在")
            else:
                print_warning(f"  └─ {file}: 不存在")
    else:
        print_warning(f"Workspace: 不存在 ({workspace})")
        results['workspace'] = None
    
    # 已安装 Skills
    try:
        result = subprocess.run(['clawhub', 'list'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = [l for l in result.stdout.strip().split('\n') if l.strip() and not l.startswith('-')]
            skill_count = len(lines)
            print_success(f"已安装 Skills: {skill_count} 个")
            results['skills_count'] = skill_count
            if skill_count > 0:
                print_info("前 5 个 Skills:")
                for line in lines[:5]:
                    print(f"    • {line.strip()}")
        else:
            print_warning("已安装 Skills: 无法获取列表")
            results['skills_count'] = 0
    except Exception as e:
        print_warning(f"Skills 列表：检测失败 - {e}")
        results['skills_count'] = 0
    
    # 结论
    print(f"\n{Colors.BOLD}📋 结论：{Colors.RESET}", end="")
    if all_good and results.get('gateway') == 'running':
        print_success("OpenClaw 已正确安装并运行")
    elif all_good:
        print_warning("OpenClaw 已安装，但 Gateway 未运行")
    else:
        print_error("OpenClaw 未正确安装")
    
    return results, all_good

# Skills 推荐
def recommend(user_type='beginner'):
    """推荐 Skills"""
    print_header("🎒 Skills 推荐")
    
    # 预设套餐
    packages = {
        'beginner': {
            'name': '新手套餐',
            'skills': [
                ('game-deals', '限免游戏查询', '⭐⭐⭐⭐⭐'),
                ('weather', '天气查询', '⭐⭐⭐⭐⭐'),
                ('rss-aggregator', 'RSS 阅读', '⭐⭐⭐⭐'),
                ('password-generator', '密码生成', '⭐⭐⭐⭐'),
                ('unit-converter', '单位转换', '⭐⭐⭐⭐'),
            ]
        },
        'developer': {
            'name': '开发者套餐',
            'skills': [
                ('git-essentials', 'Git 工具集', '⭐⭐⭐⭐⭐'),
                ('json-formatter', 'JSON 格式化', '⭐⭐⭐⭐⭐'),
                ('ocr-local', '本地 OCR', '⭐⭐⭐⭐'),
                ('pdf-toolkit-pro', 'PDF 工具', '⭐⭐⭐⭐'),
                ('system-monitor-pro', '系统监控', '⭐⭐⭐⭐'),
                ('ssh-manager', 'SSH 管理', '⭐⭐⭐⭐'),
                ('docker-helper', 'Docker 助手', '⭐⭐⭐'),
                ('code-runner', '代码运行', '⭐⭐⭐'),
            ]
        },
        'automation': {
            'name': '自动化套餐',
            'skills': [
                ('cron-manager', '定时任务', '⭐⭐⭐⭐⭐'),
                ('reminder-skill', '提醒助手', '⭐⭐⭐⭐⭐'),
                ('webhook-handler', 'Webhook 处理', '⭐⭐⭐⭐'),
                ('email-sender', '邮件发送', '⭐⭐⭐⭐'),
                ('calendar-manager', '日历管理', '⭐⭐⭐⭐'),
                ('notification-skill', '通知推送', '⭐⭐⭐⭐'),
            ]
        },
        'content': {
            'name': '内容创作套餐',
            'skills': [
                ('novel-generator', '小说生成', '⭐⭐⭐⭐'),
                ('book-writer', '书籍写作', '⭐⭐⭐⭐'),
                ('social-media-post', '社媒发布', '⭐⭐⭐⭐'),
                ('image-generator', '图片生成', '⭐⭐⭐'),
            ]
        }
    }
    
    pkg = packages.get(user_type, packages['beginner'])
    
    print_info(f"用户类型：{pkg['name']}")
    print()
    
    for i, (slug, desc, rating) in enumerate(pkg['skills'], 1):
        print(f"  {i}. {Colors.BOLD}{slug}{Colors.RESET}")
        print(f"     描述：{desc}")
        print(f"     推荐：{rating}")
        print()
    
    # 安装命令
    skill_slugs = ' '.join([s[0] for s in pkg['skills']])
    print(f"{Colors.BOLD}📦 一键安装命令：{Colors.RESET}")
    print(f"  clawhub install {skill_slugs}")
    
    return pkg['skills']

# 渠道配置引导
def channel_setup(channel):
    """渠道配置引导"""
    print_header(f"💬 {channel} 渠道配置")
    
    guides = {
        'telegram': {
            'steps': [
                "打开 Telegram，搜索 @BotFather",
                "发送 /newbot 创建机器人",
                "设置机器人名称（如：My Assistant Bot）",
                "设置机器人用户名（如：my_assistant_bot）",
                "获取 API Token（格式：123456:ABC-DEF...）",
            ],
            'config_cmd': 'openclaw configure --section telegram',
            'help_url': 'https://docs.openclaw.ai/channels/telegram'
        },
        'whatsapp': {
            'steps': [
                "OpenClaw 会显示二维码",
                "打开手机 WhatsApp",
                "点击右上角菜单 → 已连接的设备",
                "扫描二维码",
            ],
            'config_cmd': 'openclaw configure --section whatsapp',
            'help_url': 'https://docs.openclaw.ai/channels/whatsapp'
        },
        'discord': {
            'steps': [
                "打开 Discord 开发者门户：https://discord.com/developers/applications",
                "点击 'New Application' 创建应用",
                "进入 'Bot' 标签，点击 'Add Bot'",
                "复制 Bot Token",
                "进入 'OAuth2' → 'URL Generator'，选择 'bot' 作用域",
                "使用生成的链接邀请机器人到你的服务器",
            ],
            'config_cmd': 'openclaw configure --section discord',
            'help_url': 'https://docs.openclaw.ai/channels/discord'
        },
        'webchat': {
            'steps': [
                "WebChat 默认已启用",
                "访问 OpenClaw Web 界面即可使用",
                "无需额外配置",
            ],
            'config_cmd': '无需配置',
            'help_url': 'https://docs.openclaw.ai/channels/webchat'
        }
    }
    
    guide = guides.get(channel, guides['telegram'])
    
    print(f"{Colors.BOLD}📱 配置步骤：{Colors.RESET}\n")
    for i, step in enumerate(guide['steps'], 1):
        print(f"  {i}. {step}")
    
    print(f"\n{Colors.BOLD}⚙️ 配置命令：{Colors.RESET}")
    print(f"  {guide['config_cmd']}")
    
    print(f"\n{Colors.BOLD}📖 帮助文档：{Colors.RESET}")
    print(f"  {guide['help_url']}")

# 使用教程
def tutorial():
    """使用教程"""
    print_header("📖 OpenClaw 使用教程")
    
    print(f"{Colors.BOLD}🔧 基础命令{Colors.RESET}\n")
    
    commands = [
        ("openclaw help", "查看帮助"),
        ("openclaw status", "查看状态"),
        ("openclaw gateway start", "启动 Gateway"),
        ("openclaw gateway stop", "停止 Gateway"),
        ("openclaw gateway restart", "重启 Gateway"),
        ("clawhub install <skill>", "安装 skill"),
        ("clawhub list", "列出已安装 skills"),
        ("clawhub update --all", "更新所有 skills"),
        ("clawhub search <query>", "搜索 skills"),
    ]
    
    for cmd, desc in commands:
        print(f"  {Colors.CYAN}{cmd:<35}{Colors.RESET} {desc}")
    
    print(f"\n{Colors.BOLD}💬 常用场景示例{Colors.RESET}\n")
    
    examples = [
        ("天气查询", ["今天天气怎么样？", "北京明天会下雨吗？"]),
        ("限免游戏", ["今天有什么免费游戏？", "Steam 喜加一", "Epic 免费游戏"]),
        ("密码生成", ["生成一个 16 位密码", "创建一个强密码"]),
        ("单位转换", ["100 美元等于多少人民币", "1 英里等于多少公里"]),
        ("RSS 阅读", ["查看今天的科技新闻", "获取最新的 AI 资讯"]),
    ]
    
    for scenario, msgs in examples:
        print(f"  {Colors.BOLD}{scenario}{Colors.RESET}")
        for msg in msgs:
            print(f"    • {msg}")
        print()
    
    print(f"{Colors.BOLD}📚 学习资源{Colors.RESET}\n")
    print("  • 官方文档：https://docs.openclaw.ai")
    print("  • GitHub: https://github.com/openclaw/openclaw")
    print("  • ClawHub: https://clawhub.ai")
    print("  • Discord 社区：https://discord.com/invite/clawd")

# 一键完成
def run_all():
    """一键完成所有步骤"""
    print_header("🚀 OpenClaw 新手一站式引导")
    print("这将引导你完成：环境检测 → 安装检查 → Skills 推荐 → 使用教程\n")
    
    input("按 Enter 键开始...")
    
    # 1. 环境检测
    check_env()
    input("\n按 Enter 键继续...")
    
    # 2. 安装检查
    check_install()
    input("\n按 Enter 键继续...")
    
    # 3. Skills 推荐
    print("\n请选择用户类型：")
    print("  1. 新手用户")
    print("  2. 开发者")
    print("  3. 自动化爱好者")
    print("  4. 内容创作者")
    
    choice = input("\n请输入选项 (1-4，默认 1): ").strip()
    type_map = {'1': 'beginner', '2': 'developer', '3': 'automation', '4': 'content'}
    user_type = type_map.get(choice, 'beginner')
    
    recommend(user_type)
    input("\n按 Enter 键继续...")
    
    # 4. 使用教程
    tutorial()
    
    print_header("🎉 引导完成")
    print("现在你已经了解了 OpenClaw 的基础知识！")
    print("\n下一步建议：")
    print("  1. 安装推荐的 Skills")
    print("  2. 配置聊天渠道（Telegram/WhatsApp/Discord）")
    print("  3. 开始使用 OpenClaw 助手")
    print("\n有任何问题，随时运行此脚本或查看官方文档。")

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 新手一站式引导",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 交互式引导
  python3 quickstart.py --interactive

  # 环境检测
  python3 quickstart.py --check-env

  # 安装检查
  python3 quickstart.py --check-install

  # Skills 推荐
  python3 quickstart.py --recommend --type beginner

  # 渠道配置引导
  python3 quickstart.py --channel-setup telegram

  # 使用教程
  python3 quickstart.py --tutorial

  # 一键完成
  python3 quickstart.py --all
        """
    )
    
    parser.add_argument('--interactive', action='store_true', help='交互式引导')
    parser.add_argument('--check-env', action='store_true', help='环境检测')
    parser.add_argument('--check-install', action='store_true', help='安装状态检查')
    parser.add_argument('--recommend', action='store_true', help='Skills 推荐')
    parser.add_argument('--type', type=str, default='beginner', 
                        choices=['beginner', 'developer', 'automation', 'content'],
                        help='用户类型 (默认：beginner)')
    parser.add_argument('--channel-setup', type=str, metavar='CHANNEL',
                        choices=['telegram', 'whatsapp', 'discord', 'webchat'],
                        help='渠道配置引导')
    parser.add_argument('--tutorial', action='store_true', help='使用教程')
    parser.add_argument('--all', action='store_true', help='一键完成所有步骤')
    
    args = parser.parse_args()
    
    if args.interactive:
        run_all()
    elif args.check_env:
        check_env()
    elif args.check_install:
        check_install()
    elif args.recommend:
        recommend(args.type)
    elif args.channel_setup:
        channel_setup(args.channel_setup)
    elif args.tutorial:
        tutorial()
    elif args.all:
        run_all()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
