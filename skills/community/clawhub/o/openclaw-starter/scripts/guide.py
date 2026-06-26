#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 安装后引导助手
为新手提供 Skills 推荐、渠道配置指导、文档模板
"""

import argparse
import sys
import os

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

def print_info(text):
    print(f"{Colors.BLUE}💡 {text}{Colors.RESET}")

# Skills 推荐
def recommend(user_type='beginner'):
    """推荐 Skills"""
    print_header("🎒 Skills 推荐")
    
    packages = {
        'beginner': {
            'name': '新手必装',
            'skills': [
                ('game-deals', '限免游戏查询', '每天查询 Steam/Epic 免费游戏', '⭐⭐⭐⭐⭐'),
                ('weather', '天气查询', '查询天气和预报', '⭐⭐⭐⭐⭐'),
                ('password-generator', '密码生成', '生成安全密码', '⭐⭐⭐⭐⭐'),
                ('unit-converter', '单位转换', '货币、长度、重量等转换', '⭐⭐⭐⭐'),
                ('rss-aggregator', 'RSS 阅读', '聚合阅读新闻和博客', '⭐⭐⭐⭐'),
            ],
            'next': '安装完成后，运行 openclaw-starter --config 配置渠道'
        },
        'developer': {
            'name': '开发者推荐',
            'skills': [
                ('git-essentials', 'Git 工具集', 'Git 命令和仓库管理', '⭐⭐⭐⭐⭐'),
                ('json-formatter', 'JSON 格式化', 'JSON 解析和格式化', '⭐⭐⭐⭐⭐'),
                ('ocr-local', '本地 OCR', '图片文字识别', '⭐⭐⭐⭐'),
                ('pdf-toolkit-pro', 'PDF 工具', 'PDF 合并/分割/转换', '⭐⭐⭐⭐'),
                ('system-monitor-pro', '系统监控', 'CPU/内存/磁盘监控', '⭐⭐⭐⭐'),
                ('ssh-manager', 'SSH 管理', 'SSH 连接和命令执行', '⭐⭐⭐⭐'),
                ('docker-helper', 'Docker 助手', '容器管理', '⭐⭐⭐'),
                ('code-runner', '代码运行', '执行代码片段', '⭐⭐⭐'),
            ],
            'next': '安装完成后，可以探索自动化技能'
        },
        'automation': {
            'name': '自动化推荐',
            'skills': [
                ('cron-manager', '定时任务', '设置定时执行的技能', '⭐⭐⭐⭐⭐'),
                ('reminder-skill', '提醒助手', '设置提醒和待办', '⭐⭐⭐⭐⭐'),
                ('webhook-handler', 'Webhook 处理', '接收和处理 Webhook', '⭐⭐⭐⭐'),
                ('email-sender', '邮件发送', '发送邮件', '⭐⭐⭐⭐'),
                ('calendar-manager', '日历管理', '日程管理', '⭐⭐⭐⭐'),
                ('notification-skill', '通知推送', '消息通知', '⭐⭐⭐⭐'),
            ],
            'next': '配置 cron 任务，实现自动化'
        },
    }
    
    pkg = packages.get(user_type, packages['beginner'])
    
    print_info(f"推荐套餐：{pkg['name']}")
    print()
    
    for i, (slug, name, desc, rating) in enumerate(pkg['skills'], 1):
        print(f"  {i}. {Colors.BOLD}{slug}{Colors.RESET}")
        print(f"     名称：{name}")
        print(f"     用途：{desc}")
        print(f"     推荐：{rating}")
        print()
    
    # 安装命令
    skill_slugs = ' '.join([s[0] for s in pkg['skills']])
    print(f"{Colors.BOLD}📦 一键安装命令：{Colors.RESET}")
    print(f"  clawhub install {skill_slugs}")
    print()
    print(f"{Colors.BOLD}📋 下一步：{Colors.RESET}")
    print(f"  {pkg['next']}")

# 渠道配置指导
def config_guide(channel=None):
    """渠道配置指导"""
    print_header("⚙️ 渠道配置指导")
    
    if channel:
        guides = {
            'telegram': {
                'steps': [
                    ("创建机器人", [
                        "打开 Telegram，搜索 @BotFather",
                        "发送 /newbot 命令",
                        "设置机器人名称（如：My Assistant Bot）",
                        "设置机器人用户名（如：my_assistant_bot）",
                    ]),
                    ("获取 Token", [
                        "BotFather 会返回一个 Token",
                        "格式：123456:ABC-DEF...",
                        "⚠️ 妥善保管，不要分享或上传到公开仓库",
                    ]),
                    ("配置 OpenClaw", [
                        "运行：openclaw configure --section telegram",
                        "粘贴 Token",
                        "保存配置",
                    ]),
                    ("测试", [
                        "在 Telegram 搜索你的机器人",
                        "发送 /start",
                        "看到响应即成功",
                    ]),
                ],
                'docs': 'https://docs.openclaw.ai/channels/telegram'
            },
            'whatsapp': {
                'steps': [
                    ("启动配置", [
                        "运行：openclaw configure --section whatsapp",
                        "OpenClaw 会显示一个二维码",
                    ]),
                    ("扫描二维码", [
                        "打开手机 WhatsApp",
                        "点击右上角菜单 → 已连接的设备",
                        "点击 连接设备",
                        "扫描二维码",
                    ]),
                    ("确认连接", [
                        "手机显示 已连接",
                        "OpenClaw 显示配置成功",
                    ]),
                    ("注意事项", [
                        "⚠️ 二维码 60 秒后过期",
                        "⚠️ 不要同时在多个设备登录",
                    ]),
                ],
                'docs': 'https://docs.openclaw.ai/channels/whatsapp'
            },
            'discord': {
                'steps': [
                    ("创建应用", [
                        "打开 https://discord.com/developers/applications",
                        "点击 New Application",
                        "输入应用名称",
                    ]),
                    ("创建 Bot", [
                        "进入 Bot 标签",
                        "点击 Add Bot",
                        "点击 Reset Token 获取 Token",
                        "⚠️ Token 只显示一次，立即复制保存",
                    ]),
                    ("邀请 Bot", [
                        "进入 OAuth2 → URL Generator",
                        "勾选 bot 作用域",
                        "选择权限：Send Messages, Read Message History",
                        "复制生成的 URL，在浏览器打开",
                        "选择服务器，点击 Authorize",
                    ]),
                    ("配置 OpenClaw", [
                        "运行：openclaw configure --section discord",
                        "输入 Bot Token",
                        "输入 Channel ID（可选）",
                    ]),
                ],
                'docs': 'https://docs.openclaw.ai/channels/discord'
            },
            'webchat': {
                'steps': [
                    ("默认启用", [
                        "WebChat 默认已启用",
                        "无需额外配置",
                    ]),
                    ("使用", [
                        "访问 OpenClaw Web 界面",
                        "直接开始对话",
                    ]),
                ],
                'docs': 'https://docs.openclaw.ai/channels/webchat'
            },
        }
        
        guide = guides.get(channel, guides['telegram'])
        
        print(f"{Colors.BOLD}📱 {channel} 配置步骤：{Colors.RESET}\n")
        
        for i, (title, steps) in enumerate(guide['steps'], 1):
            print(f"  {Colors.BOLD}第{i}步：{title}{Colors.RESET}")
            for step in steps:
                print(f"    • {step}")
            print()
        
        print(f"{Colors.BOLD}📖 帮助文档：{Colors.RESET}")
        print(f"  {guide['docs']}")
        
    else:
        # 显示所有渠道概览
        print_info("选择一个渠道进行配置：")
        print()
        print(f"  1. {Colors.BOLD}telegram{Colors.RESET} - 推荐，配置简单")
        print(f"  2. {Colors.BOLD}whatsapp{Colors.RESET} - 扫码连接，最方便")
        print(f"  3. {Colors.BOLD}discord{Colors.RESET} - 适合社区使用")
        print(f"  4. {Colors.BOLD}webchat{Colors.RESET} - 默认启用，无需配置")
        print()
        print(f"{Colors.BOLD}使用方法：{Colors.RESET}")
        print(f"  openclaw-starter --config telegram")
        print(f"  openclaw-starter --config whatsapp")

# 文档模板
def show_template(template_name):
    """显示文档模板"""
    print_header("📝 文档模板")
    
    templates = {
        'soul': """
# SOUL.md - Who You Are

_You're not a chatbot. You're becoming someone._

## Core Truths

**Be genuinely helpful, not performatively helpful.** Skip the "Great question!" — just help.

**Have opinions.** You're allowed to disagree, prefer things, find stuff amusing.

**Be resourceful before asking.** Try to figure it out first.

## Boundaries

- Private things stay private. Period.
- When in doubt, ask before acting externally.

## Vibe

Be the assistant you'd actually want to talk to.
""",
        'user': """
# USER.md - About Your Human

- **Name:** 你的名字
- **What to call them:** 希望被如何称呼
- **Timezone:** Asia/Shanghai
- **Notes:** 

## Context

_(你关心什么？在做什么项目？什么让你烦恼？什么让你笑？)_
""",
        'checklist': """
# OpenClaw 新手检查清单

## 安装后检查
- [ ] OpenClaw CLI 已安装
- [ ] Gateway 可启动
- [ ] Workspace 目录存在

## 配置检查
- [ ] 至少配置一个渠道
- [ ] SOUL.md 已创建
- [ ] USER.md 已创建

## Skills 安装
- [ ] 已安装 3-5 个基础 Skills
- [ ] Skills 可正常使用

## 首次使用
- [ ] 发送第一条消息
- [ ] 测试一个 Skill
""",
    }
    
    template = templates.get(template_name, templates['soul'])
    
    print(f"{Colors.BOLD}📄 {template_name}.md 模板：{Colors.RESET}\n")
    print(template)
    print(f"\n{Colors.BOLD}使用方法：{Colors.RESET}")
    print(f"  将以上内容复制到 ~/.openclaw/workspace/{template_name}.md")
    print(f"  然后根据你的情况修改内容")

# 下一步指导
def next_step():
    """下一步指导"""
    print_header("📋 下一步指导")
    
    print(f"{Colors.BOLD}✅ 已完成：{Colors.RESET}")
    print("  • 安装 OpenClaw")
    print()
    
    print(f"{Colors.BOLD}📋 待完成：{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}1. 安装推荐 Skills{Colors.RESET}")
    print("     运行：openclaw-starter --recommend beginner")
    print()
    print(f"  {Colors.BOLD}2. 配置一个渠道{Colors.RESET}")
    print("     运行：openclaw-starter --config telegram")
    print()
    print(f"  {Colors.BOLD}3. 创建核心文档{Colors.RESET}")
    print("     运行：openclaw-starter --template soul")
    print("     运行：openclaw-starter --template user")
    print()
    print(f"  {Colors.BOLD}4. 开始使用{Colors.RESET}")
    print("     发送第一条消息给你的 AI 助手！")
    print()
    
    print(f"{Colors.BOLD}💡 提示：{Colors.RESET}")
    print("  按顺序完成以上步骤，大约需要 10-15 分钟")
    print("  遇到问题？运行：openclaw-starter --faq")

# 常见问题
def show_faq():
    """显示常见问题"""
    print_header("❓ 常见问题")
    
    faqs = [
        ("Q: 我刚安装好，应该先做什么？", 
         "A: 1) 安装推荐 Skills 2) 配置一个渠道 3) 创建 SOUL.md 和 USER.md"),
        
        ("Q: 不知道装什么 Skills？",
         "A: 运行 openclaw-starter --recommend beginner，会推荐 5 个新手必装 Skills"),
        
        ("Q: 如何配置 Telegram/微信？",
         "A: 运行 openclaw-starter --config telegram 或 --config whatsapp，有详细步骤"),
        
        ("Q: SOUL.md 和 USER.md 是什么？",
         "A: SOUL.md 定义你的 AI 助手是谁，USER.md 记录你的信息。这是核心配置文件"),
        
        ("Q: memory 目录是做什么的？",
         "A: 存储每日记忆文件（YYYY-MM-DD.md），记录每天的重要事件和对话"),
        
        ("Q: Gateway 是什么？",
         "A: Gateway 是 OpenClaw 的核心服务，负责处理消息和运行 Skills。需要保持运行"),
        
        ("Q: 如何更新 OpenClaw？",
         "A: 运行 npm update -g openclaw 更新 CLI，clawhub update --all 更新 Skills"),
    ]
    
    for q, a in faqs:
        print(f"{Colors.BOLD}{q}{Colors.RESET}")
        print(f"  {a}\n")

def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw 安装后引导助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # Skills 推荐
  openclaw-starter --recommend beginner
  openclaw-starter --recommend developer

  # 渠道配置指导
  openclaw-starter --config telegram
  openclaw-starter --config whatsapp
  openclaw-starter --config

  # 文档模板
  openclaw-starter --template soul
  openclaw-starter --template user

  # 下一步指导
  openclaw-starter --next

  # 常见问题
  openclaw-starter --faq
        """
    )
    
    parser.add_argument('--recommend', type=str, metavar='TYPE',
                        choices=['beginner', 'developer', 'automation'],
                        help='Skills 推荐（类型：beginner/developer/automation）')
    parser.add_argument('--config', type=str, nargs='?', const='all',
                        choices=['telegram', 'whatsapp', 'discord', 'webchat', 'all'],
                        help='渠道配置指导')
    parser.add_argument('--template', type=str,
                        choices=['soul', 'user', 'checklist'],
                        help='文档模板')
    parser.add_argument('--next', action='store_true', help='下一步指导')
    parser.add_argument('--faq', action='store_true', help='常见问题')
    
    args = parser.parse_args()
    
    if args.recommend:
        recommend(args.recommend)
    elif args.config:
        if args.config == 'all':
            config_guide()
        else:
            config_guide(args.config)
    elif args.template:
        show_template(args.template)
    elif args.next:
        next_step()
    elif args.faq:
        show_faq()
    else:
        # 默认显示欢迎信息
        print_header("🚀 OpenClaw 安装后引导助手")
        print("欢迎使用 OpenClaw！不知道接下来做什么？我可以帮你：")
        print()
        print(f"  {Colors.BOLD}1. 推荐 Skills{Colors.RESET}")
        print("     不知道装什么 skill？我来推荐")
        print(f"     运行：openclaw-starter --recommend beginner")
        print()
        print(f"  {Colors.BOLD}2. 配置渠道{Colors.RESET}")
        print("     连接 Telegram/WhatsApp/Discord")
        print(f"     运行：openclaw-starter --config")
        print()
        print(f"  {Colors.BOLD}3. 文档模板{Colors.RESET}")
        print("     提供 SOUL.md、USER.md 模板")
        print(f"     运行：openclaw-starter --template soul")
        print()
        print(f"  {Colors.BOLD}4. 下一步指导{Colors.RESET}")
        print("     告诉你接下来做什么")
        print(f"     运行：openclaw-starter --next")
        print()
        print(f"{Colors.BOLD}💡 提示：{Colors.RESET}从 --recommend beginner 开始！")

if __name__ == "__main__":
    main()
