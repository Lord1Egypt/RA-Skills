#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setup.py
News Brief Skill 一键配置向导
运行后自动生成 .env 和 config.yaml
"""

import os
import sys
import time
import requests
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ANSI 颜色
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

CATEGORIES = ["时政", "经济", "社会", "国际", "科技", "体育", "文娱", "军事", "教育", "法治", "环境", "农业"]

# 新闻来源表（展示给用户看，增强信任感）
SOURCES_TABLE = """
  ┌──────┬─────────────────────────────┬──────────────────────────┐
  │ 分类 │ 国际权威媒体                │ 国内权威媒体             │
  ├──────┼─────────────────────────────┼──────────────────────────┤
  │ 时政 │ Reuters, AP News            │ 新华社, 人民网           │
  │ 经济 │ Bloomberg, FT               │ 财联社, 第一财经         │
  │ 社会 │ BBC, CNN                    │ 澎湃新闻, 南方都市报     │
  │ 国际 │ Reuters, AP News            │ 环球时报, 参考消息       │
  │ 科技 │ TechCrunch, The Verge       │ 36氪, 虎嗅              │
  │ 体育 │ ESPN, BBC Sport             │ 懂球帝, 腾讯体育         │
  │ 文娱 │ Variety, Hollywood Reporter │ 娱乐资本论              │
  │ 军事 │ Defense News, Reuters       │ 观察者网                │
  │ 教育 │ Times Higher Education      │ 中国教育报              │
  │ 法治 │ Reuters Legal               │ 法制日报                │
  │ 环境 │ The Guardian                │ 财新环境                │
  │ 农业 │ Reuters Agriculture         │ 农民日报                │
  └──────┴─────────────────────────────┴──────────────────────────┘
"""


def banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════╗
║        News Brief Skill 配置向导         ║
║     每天自动生成你的专属新闻简报          ║
╚══════════════════════════════════════════╝{RESET}
""")


def step(n: int, title: str):
    print(f"\n{BOLD}{CYAN}── 第{n}步：{title} ──{RESET}")


def ok(msg: str):
    print(f"{GREEN}✅ {msg}{RESET}")


def warn(msg: str):
    print(f"{YELLOW}⚠️  {msg}{RESET}")


def err(msg: str):
    print(f"{RED}❌ {msg}{RESET}")


def ask(prompt: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    val  = input(f"{BOLD}{prompt}{hint}: {RESET}").strip()
    return val if val else default


def ask_choice(prompt: str, options: list, default_idx: int = 0) -> str:
    print(f"{BOLD}{prompt}{RESET}")
    for i, opt in enumerate(options):
        marker = f"{GREEN}▶{RESET}" if i == default_idx else " "
        print(f"  {marker} {i+1}. {opt}")
    while True:
        val = input(f"请输入序号 [默认{default_idx+1}]: ").strip()
        if not val:
            return options[default_idx]
        if val.isdigit() and 1 <= int(val) <= len(options):
            return options[int(val) - 1]
        warn("请输入有效序号")


def ask_multi_choice(prompt: str, options: list, max_count: int = 3) -> list:
    print(f"{BOLD}{prompt}（最多{max_count}个，用逗号分隔序号，如: 1,5,12）{RESET}")
    for i, opt in enumerate(options):
        print(f"  {i+1:2d}. {opt}")
    while True:
        val = input(f"请输入序号: ").strip()
        if not val:
            warn("至少选择1个分类")
            continue
        parts = [p.strip() for p in val.replace("，", ",").split(",")]
        selected = []
        valid = True
        for p in parts:
            if p.isdigit() and 1 <= int(p) <= len(options):
                selected.append(options[int(p) - 1])
            else:
                warn(f"无效序号: {p}")
                valid = False
                break
        if not valid:
            continue
        if len(selected) > max_count:
            warn(f"最多选{max_count}个，你选了{len(selected)}个")
            continue
        if selected:
            return list(dict.fromkeys(selected))  # 去重保序


def verify_serper_key(key: str) -> bool:
    """验证 Serper API Key 是否有效"""
    try:
        resp = requests.post(
            "https://serper.dev/news",
            headers={"X-API-KEY": key, "Content-Type": "application/json"},
            json={"q": "technology news", "num": 1},
            timeout=8,
        )
        return resp.status_code == 200
    except Exception:
        return False


def verify_deepseek_key(key: str) -> bool:
    """验证 DeepSeek API Key 是否有效"""
    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat",
                  "messages": [{"role": "user", "content": "hi"}],
                  "max_tokens": 5},
            timeout=8,
        )
        return resp.status_code == 200
    except Exception:
        return False


def setup_api_keys() -> tuple[str, str]:
    step(1, "配置 API Keys")

    print(f"""
{YELLOW}需要两个免费/低价 API Key：

  1. Serper API Key（抓取新闻用）
     • 免费额度：2500次/月（每天1次跑一年都够）
     • 获取地址：{BOLD}https://serper.dev/{RESET}{YELLOW}
     • 注册后在 Dashboard → API Key 复制

  2. DeepSeek API Key（AI摘要/翻译用）
     • 费用：约¥0.02/次简报（极低）
     • 获取地址：{BOLD}https://platform.deepseek.com{RESET}{YELLOW}
     • 注册后在 API Keys → 创建新密钥{RESET}
""")

    # Serper Key
    while True:
        serper_key = ask("请粘贴你的 Serper API Key")
        if not serper_key:
            warn("Serper API Key 不能为空")
            continue
        print("  验证中...", end="", flush=True)
        if verify_serper_key(serper_key):
            print(f"\r{GREEN}✅ Serper API Key 验证通过{RESET}          ")
            break
        else:
            print(f"\r{RED}❌ Serper API Key 无效，请检查后重新输入{RESET}")

    # DeepSeek Key
    while True:
        deepseek_key = ask("请粘贴你的 DeepSeek API Key")
        if not deepseek_key:
            warn("DeepSeek API Key 不能为空")
            continue
        print("  验证中...", end="", flush=True)
        if verify_deepseek_key(deepseek_key):
            print(f"\r{GREEN}✅ DeepSeek API Key 验证通过{RESET}         ")
            break
        else:
            print(f"\r{RED}❌ DeepSeek API Key 无效，请检查后重新输入{RESET}")

    return serper_key, deepseek_key


def setup_categories() -> list:
    step(2, "选择新闻分类")
    print(f"""
{YELLOW}选择你最感兴趣的1-3个新闻分类。
建议选择你每天工作/投资/生活中真正需要关注的领域。

所有新闻均来自以下权威媒体，每天实时抓取，绝不使用小型网站：{RESET}
{CYAN}{SOURCES_TABLE}{RESET}""")
    return ask_multi_choice("可选分类：", CATEGORIES, max_count=3)


def setup_news_count() -> int:
    step(3, "每类抓取条数")
    print(f"""
{YELLOW}每个分类每天抓取几条新闻？
  • 3-5条：精简版，阅读约2分钟
  • 6-8条：标准版，阅读约5分钟（推荐）
  • 9-10条：完整版，阅读约8分钟{RESET}
""")
    val = ask("请输入数字 (3-10)", default="6")
    try:
        n = int(val)
        return max(3, min(10, n))
    except ValueError:
        return 6


def setup_time_range() -> str:
    step(4, "新闻时间范围")
    print(f"""
{YELLOW}抓取多长时间内的新闻？
  • 24小时：每天查看推荐，获取最新资讯
  • 48小时：隔天查看推荐，不会漏掉重要新闻{RESET}
""")
    choice = ask_choice("选择时间范围：", ["24小时（每天看）", "48小时（隔天看）"], default_idx=0)
    val = "24h" if "24" in choice else "48h"
    ok(f"已选择：过去{val.replace('h','')}小时内的新闻")
    return val


def setup_push_time() -> str:
    step(5, "设置每日推送时间")
    print(f"""
{YELLOW}每天几点自动生成简报？输入你希望的时间（24小时制）。
  常用时间：06:00 早起 / 08:00 上班路上（推荐）/ 12:00 午休 / 22:00 睡前{RESET}
""")
    while True:
        val = ask("请输入时间（格式 HH:MM，如 08:00）", default="08:00")
        import re
        if re.match(r"^([01]\d|2[0-3]):([0-5]\d)$", val):
            ok(f"已设置为每天 {val} 推送")
            return val
        warn("格式不正确，请输入如 08:00 / 09:30 / 22:00 这样的格式")


def setup_options() -> dict:
    step(6, "其他选项")
    include_overview = ask("是否包含「今日概览」（3句话总结全部新闻）? [Y/n]", "Y").upper() != "N"
    include_insight  = ask("是否包含「今日洞察」（趋势分析1句话）? [Y/n]", "Y").upper() != "N"
    return {
        "include_overview": include_overview,
        "include_insight":  include_insight,
    }


def write_env(serper_key: str, deepseek_key: str):
    env_path = BASE_DIR / ".env"
    env_path.write_text(
        f"SERPER_API_KEY={serper_key}\n"
        f"DEEPSEEK_API_KEY={deepseek_key}\n",
        encoding="utf-8"
    )
    ok(f".env 已写入：{env_path}")


def write_config(categories: list, news_per_cat: int,
                 time_range: str, push_time: str, options: dict):
    cat_lines = "\n".join([f"  - {c}" for c in categories])
    config_content = f"""# ============================================================
# News Brief Skill 配置文件（由 setup.py 自动生成）
# 如需修改，直接编辑本文件后重新运行 run.py
# ============================================================

# 新闻分类（最多3个）
# 可选：时政 / 经济 / 社会 / 国际 / 科技 / 体育 / 文娱 / 军事 / 教育 / 法治 / 环境 / 农业
categories:
{cat_lines}

# 新闻时间范围：24h=过去24小时 / 48h=过去48小时
time_range: "{time_range}"

# 每个分类抓取几条新闻（3-10）
news_per_category: {news_per_cat}

# 每日推送时间（用于定时任务参考）
push_time: "{push_time}"

# 简报语言：zh=纯中文 / en=纯英文 / both=中英双语
language: zh

# 输出文件保存路径（留空则只打印到终端）
output_dir: "./output"

# 是否包含「今日概览」（3句话总结全部新闻）
include_overview: {str(options['include_overview']).lower()}

# 是否包含「今日洞察」（趋势分析1句话）
include_insight: {str(options['include_insight']).lower()}
"""
    cfg_path = BASE_DIR / "config.yaml"
    cfg_path.write_text(config_content, encoding="utf-8")
    ok(f"config.yaml 已写入：{cfg_path}")


def write_crontab(push_time: str):
    """生成定时任务命令（仅打印，不自动添加）"""
    hour, minute = push_time.split(":")
    cron_line = f"{minute} {hour} * * * cd {BASE_DIR.resolve()} && python run.py >> {BASE_DIR.resolve()}/logs/daily.log 2>&1"
    print(f"""
{CYAN}── 定时运行设置（可选）──{RESET}
如需每天 {push_time} 自动运行，执行以下命令添加定时任务：

  {BOLD}crontab -e{RESET}

然后添加这一行：
  {YELLOW}{cron_line}{RESET}
""")


def main():
    banner()

    print(f"{YELLOW}本向导将帮你完成所有配置，大约需要 3 分钟。{RESET}")
    input(f"\n按 {BOLD}Enter{RESET} 开始配置...")

    # 逐步配置
    serper_key, deepseek_key = setup_api_keys()
    categories   = setup_categories()
    news_per_cat = setup_news_count()
    time_range   = setup_time_range()
    push_time    = setup_push_time()
    options      = setup_options()

    # 写入文件
    print(f"\n{CYAN}{BOLD}── 正在保存配置... ──{RESET}")
    write_env(serper_key, deepseek_key)
    write_config(categories, news_per_cat, time_range, push_time, options)

    # 汇总确认
    print(f"""
{GREEN}{BOLD}╔══════════════════════════════════════════╗
║            🎉 配置完成！                 ║
╚══════════════════════════════════════════╝{RESET}

{BOLD}你的配置：{RESET}
  📰 新闻分类：{' · '.join(categories)}
  📊 每类条数：{news_per_cat} 条
  🕐 时间范围：过去 {time_range.replace('h','小时')}
  ⏰ 推送时间：每天 {push_time}
  📌 今日概览：{'✅' if options['include_overview'] else '❌'}
  💡 今日洞察：{'✅' if options['include_insight'] else '❌'}

{BOLD}立即运行：{RESET}
  {YELLOW}python run.py{RESET}  （.env 自动加载，无需 source）

{BOLD}预览模式（不保存文件）：{RESET}
  {YELLOW}python run.py --preview{RESET}
""")

    write_crontab(push_time)

    # 询问是否立即试跑
    run_now = ask("是否立即运行一次？[Y/n]", "Y")
    if run_now.upper() != "N":
        print(f"\n{CYAN}正在运行，请稍候...{RESET}\n")
        # 把key设到环境变量然后执行
        os.environ["SERPER_API_KEY"]   = serper_key
        os.environ["DEEPSEEK_API_KEY"] = deepseek_key
        os.chdir(BASE_DIR)  # 确保工作目录正确
        os.system(f"python {BASE_DIR / 'run.py'} --preview")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}已取消配置。{RESET}")
        sys.exit(0)
