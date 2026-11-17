#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台AI信息源 — CLI 入口
=========================
一次调用查询 快手 / 公众号 / B站 / 视频号 / 小红书 中任意一个、多个或全部平台，
输出终端表格 + AI 情报调查 + 统一 HTML 日报。

共享逻辑全部在 feed_core.py，本文件只负责参数解析与编排。
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from feed_core import (  # noqa: E402
    BOLD, CYAN, DEFAULT_OUTPUT_DIR, GREEN, PLATFORMS, PLATFORM_ORDER, RED, REPORT_PREFIX,
    RESET, SKILL_NAME, YELLOW, check_date_available, disable_color, display_width,
    format_number, generate_report, get_api_key, global_latest_date,
    install_subscription, latest_available_date, make_session, open_in_browser, pad,
    parse_date_arg, print_api_key_help, print_data_unavailable_notice,
    print_intelligence_briefing, print_platform_table, remove_subscription,
    resolve_platforms, results_to_json, run_platform, show_subscription, spec_slug,
    use_stderr_for_logs, warn,
)


# ─── 参数解析辅助 ──────────────────────────────────────────────────────────────────
def split_list(value):
    """逗号 / 顿号 / 竖线分隔的字符串 → 列表"""
    return [t.strip() for t in re.split(r"[,，、|]+", value or "") if t.strip()]


def parse_platform_keywords(spec):
    """
    --platform-keywords "bili:AI,大模型;xhs:AI绘画"
    → {"bili": ["AI", "大模型"], "xhs": ["AI绘画"]}
    """
    overrides = {}
    for chunk in re.split(r"[;；]+", spec or ""):
        chunk = chunk.strip()
        if not chunk:
            continue
        platform_part, sep, kw_part = chunk.replace("：", ":").partition(":")
        if not sep:
            raise ValueError(
                f"--platform-keywords 格式应为 平台:关键词1,关键词2，收到: {chunk}"
            )
        keywords = split_list(kw_part)
        if not keywords:
            raise ValueError(f"--platform-keywords 中 {platform_part} 未指定关键词")
        for slug in resolve_platforms(platform_part):
            overrides[slug] = keywords
    return overrides


def keywords_for(slug, global_keywords, overrides):
    """逐平台覆盖 > 全局关键词 > 平台默认关键词"""
    if slug in overrides:
        return list(overrides[slug])
    if global_keywords:
        return list(global_keywords)
    return list(PLATFORMS[slug]["default_keywords"])


def resolve_window(args, slugs):
    """
    确定查询窗口，返回 (start_date, end_date, display_date, nav_date, start_time, end_time)
    nav_date 恒为单个 YYYY-MM-DD，供报告内的日期前后翻页使用。
    """
    start_time = (args.start_time or "").strip() or None
    end_time = (args.end_time or "").strip() or None

    if args.latest:
        end_date = global_latest_date(slugs)
        return end_date, end_date, end_date, end_date, None, None

    if start_time and end_time:
        start_date, end_date = start_time[:10], end_time[:10]
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
        display = start_date if start_date == end_date else f"{start_date}~{end_date}"
        return start_date, end_date, display, end_date, start_time, end_time

    date_val = (args.date or "").strip() or datetime.now().strftime("%Y-%m-%d")
    try:
        start_date, end_date, display = parse_date_arg(date_val)
    except ValueError:
        raise SystemExit(
            f"日期格式错误: {date_val}，应为 YYYY-MM-DD 或 YYYY-MM-DD~YYYY-MM-DD"
        )
    return start_date, end_date, display, end_date, None, None


# ─── 输出 ─────────────────────────────────────────────────────────────────────────
def print_banner(slugs):
    names = " · ".join(PLATFORMS[s]["name"] for s in slugs)
    lines = [f"{SKILL_NAME} · 日报生成", names]
    inner = max(display_width(t) for t in lines) + 6
    bar = "═" * inner
    body = "".join(f"  ║   {pad(t, inner - 3)}║\n" for t in lines)
    sys.stdout.write(f"{CYAN()}{BOLD()}\n  ╔{bar}╗\n{body}  ╚{bar}╝{RESET()}\n\n")
    sys.stdout.flush()


def print_summary(results, report_path, display_date):
    """结构化摘要：跨平台对比表 + 报告地址 + 订阅提醒"""
    ok = [r for r in results if r["articles"]]
    total = sum(r["stats"]["total"] for r in ok)

    cols = (10, 8, 10, 14, 12)
    rule = "─" * sum(cols)
    head = (pad("平台", cols[0]) + pad("分类", cols[1], ">") + pad("数量", cols[2], ">")
            + pad("头部指标", cols[3], ">") + pad("总互动", cols[4], ">"))

    sys.stdout.write(f"\n{GREEN()}{BOLD()}✓ 完成!{RESET()}\n\n")
    sys.stdout.write(f"  {BOLD()}平台数据速览{RESET()}  （{display_date}）\n")
    sys.stdout.write(f"  {head}\n  {rule}\n")
    for r in ok:
        cfg = PLATFORMS[r["slug"]]
        st = r["stats"]
        row = (pad(cfg["name"], cols[0])
               + pad(f"{len(r['clusters'])}个", cols[1], ">")
               + pad(f"{st['total']}{cfg['unit']}", cols[2], ">")
               + pad(f"{format_number(st['avg_primary'])}{st['avg_label'][2:]}", cols[3], ">")
               + pad(format_number(st["total_engagement"]), cols[4], ">"))
        sys.stdout.write(f"  {row}\n")
    sys.stdout.write(f"  {rule}\n")
    sys.stdout.write(f"  合计: {len(ok)} 个平台 · {total} 条内容\n")

    skipped = [r for r in results if not r["articles"]]
    if skipped:
        sys.stdout.write(f"\n  {YELLOW()}{BOLD()}未获取到数据的平台{RESET()}\n")
        for r in skipped:
            sys.stdout.write(f"  · {r.get('reason') or PLATFORMS[r['slug']]['name']}\n")

    if report_path:
        sys.stdout.write(f"\n  {BOLD()}日报地址{RESET()}: {report_path}\n")

    sys.stdout.write(
        f"\n  {CYAN()}订阅每日推送{RESET()}: "
        f"python3 scripts/multi_ai_feed.py --platform <平台> --keywords <关键词> --subscribe\n"
    )
    sys.stdout.flush()


# ─── 主流程 ───────────────────────────────────────────────────────────────────────
def build_parser():
    valid = "、".join(f"{PLATFORMS[s]['name']}({PLATFORMS[s]['short']})" for s in PLATFORM_ORDER)
    parser = argparse.ArgumentParser(
        prog="multi_ai_feed.py",
        description=f"{SKILL_NAME} — 快手 / 公众号 / B站 / 视频号 / 小红书 AI 爆款内容聚合日报",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
可选平台: all（全部）、{valid}

示例:
  python3 multi_ai_feed.py --platform all --latest
  python3 multi_ai_feed.py --platform bili,xhs --latest
  python3 multi_ai_feed.py --platform 快手 --keywords "AI绘画,AI教程" --date 2026-08-30
  python3 multi_ai_feed.py --platform all --latest --platform-keywords "bili:AI,大模型;xhs:AI绘画"
  python3 multi_ai_feed.py --platform all --latest --json
  python3 multi_ai_feed.py --platform all --latest --no-intel --no-open
  python3 multi_ai_feed.py --subscribe
  python3 multi_ai_feed.py --show-subscription
  python3 multi_ai_feed.py --unsubscribe

⚠️ 数据每日 15:00 / 16:00 更新前一天内容，目标日期无数据时不会调用任何接口。
        """,
    )
    parser.add_argument("--platform", default="all",
                        help=f"平台范围: all 或逗号分隔 (默认: all)。可选: {valid}")
    parser.add_argument("--keywords", help="全局搜索关键词，逗号分隔 (默认: 各平台内置关键词)")
    parser.add_argument("--platform-keywords",
                        help='逐平台覆盖关键词，格式 "bili:AI,大模型;xhs:AI绘画"')
    parser.add_argument("--count", type=int, default=0,
                        help="单平台目标条数 (默认: 各平台推荐值)")
    parser.add_argument("--date", help="指定日期 YYYY-MM-DD，或区间 YYYY-MM-DD~YYYY-MM-DD (默认: 今天)")
    parser.add_argument("--start-time", help="自定义开始时间 YYYY-MM-DD HH:MM:SS (覆盖 --date 推算)")
    parser.add_argument("--end-time", help="自定义结束时间 YYYY-MM-DD HH:MM:SS (覆盖 --date 推算)")
    parser.add_argument("--latest", action="store_true",
                        help="自动使用各平台共同的最新可查日期（跳过无数据区间，不扣积分）")
    parser.add_argument("--top-n", type=int, default=5, help="每平台最大分类数 (默认: 5)")
    parser.add_argument("--no-intel", action="store_true", help="关闭 AI 情报调查")
    parser.add_argument("--output-dir", help=f"输出目录 (默认: {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--api-key", help="API Key (不传则读取环境变量 REDFOX_API_KEY)")
    parser.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    parser.add_argument("--json", action="store_true",
                        help="stdout 只输出归一化 JSON（进度日志转到 stderr），供 Agent 二次加工")
    parser.add_argument("--no-color", action="store_true", help="关闭 ANSI 颜色")
    parser.add_argument("--subscribe", action="store_true",
                        help="安装每日定时任务，固化当前 --platform / --keywords")
    parser.add_argument("--unsubscribe", action="store_true", help="卸载定时任务")
    parser.add_argument("--show-subscription", action="store_true", help="查看当前订阅状态")
    return parser


def main():
    args = build_parser().parse_args()

    if args.no_color or args.json:
        disable_color()
    if args.json:
        use_stderr_for_logs()

    # ── 订阅管理（不取数）──
    if args.show_subscription:
        show_subscription()
        return 0
    if args.unsubscribe:
        return 0 if remove_subscription() else 1
    if args.subscribe:
        return 0 if install_subscription(args.platform, args.keywords) else 1

    # ── 平台解析 ──
    try:
        slugs = resolve_platforms(args.platform)
    except ValueError as e:
        sys.stdout.write(f"{RED()}[✗]{RESET()} {e}\n")
        return 2

    try:
        overrides = parse_platform_keywords(args.platform_keywords)
    except ValueError as e:
        sys.stdout.write(f"{RED()}[✗]{RESET()} {e}\n")
        return 2

    global_keywords = split_list(args.keywords)
    intel_enabled = not args.no_intel

    if not args.json:
        print_banner(slugs)

    # ── 查询窗口 ──
    try:
        start_date, end_date, display_date, nav_date, start_time, end_time = resolve_window(args, slugs)
    except ValueError as e:
        sys.stdout.write(f"{RED()}[✗]{RESET()} {e}\n")
        return 2

    # ── 数据可用性预检：目标日期无数据时 0 次接口调用 ──
    unavailable = [s for s in slugs
                   if not check_date_available(end_date, PLATFORMS[s]["update_hour"])[0]]
    if len(unavailable) == len(slugs):
        print_data_unavailable_notice(display_date, slugs)
        if args.json:
            sys.stdout.write(json.dumps({
                "skill": SKILL_NAME,
                "date": display_date,
                "error": "data_unavailable",
                "latest_available": global_latest_date(slugs),
                "platforms": [
                    {"slug": s, "name": PLATFORMS[s]["name"],
                     "latest_available": latest_available_date(PLATFORMS[s]["update_hour"])}
                    for s in slugs
                ],
            }, ensure_ascii=False, indent=2) + "\n")
            sys.stdout.flush()
        return 0
    for s in unavailable:
        cfg = PLATFORMS[s]
        warn(f"{cfg['name']} {end_date} 数据尚未更新（最新可查 "
             f"{latest_available_date(cfg['update_hour'])}），本次跳过")

    # ── API Key ──
    api_key = get_api_key(cli_key=args.api_key)
    if not api_key:
        print_api_key_help()
        return 1
    session = make_session(api_key)

    # ── 逐平台执行 ──
    results = []
    for slug in slugs:
        cfg = PLATFORMS[slug]
        keywords = keywords_for(slug, global_keywords, overrides)
        target = args.count if args.count > 0 else cfg["page_size"]
        others = tuple(PLATFORMS[s]["name"] for s in slugs if s != slug)
        results.append(run_platform(
            session, slug, keywords, target, start_date, end_date,
            other_platform_names=others, intel_enabled=intel_enabled,
            top_n=args.top_n, start_time=start_time, end_time=end_time,
        ))
        r = results[-1]
        if not r["articles"]:
            warn(r.get("reason") or f"{cfg['name']} 未获取到内容")
            continue
        if not args.json:
            print_platform_table(slug, r["clusters"])
            if r.get("briefing"):
                print_intelligence_briefing(r["briefing"])

    # ── JSON 模式：只输出结构化数据 ──
    if args.json:
        sys.stdout.write(json.dumps(
            results_to_json(results, display_date, slugs), ensure_ascii=False, indent=2
        ) + "\n")
        sys.stdout.flush()
        return 0

    # ── 生成报告 ──
    ok = [r for r in results if r["articles"]]
    report_path = None
    if not ok:
        warn("所有平台均未获取到内容，未生成 HTML 日报")
        sys.stdout.write(
            f"\n{YELLOW()}  提示：本 Skill 仅收录各平台 AI 相关内容。"
            f"如需全量数据，请访问 redfox.hk{RESET()}\n"
        )
        print_summary(results, None, display_date)
        return 0

    output_dir = Path(args.output_dir).expanduser() if args.output_dir else DEFAULT_OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{REPORT_PREFIX}_{spec_slug(slugs)}_{nav_date}.html"
    report_path = output_dir / filename

    html = generate_report(ok, display_date, nav_date, slugs, intel_enabled=intel_enabled)
    report_path.write_text(html, encoding="utf-8")
    sys.stdout.write(f"{GREEN()}[✓]{RESET()} 日报已生成: {report_path}\n")
    sys.stdout.flush()

    # ── 浏览器 ──
    if not args.no_open:
        open_in_browser(str(report_path))

    print_summary(results, report_path, display_date)
    return 0


if __name__ == "__main__":
    sys.exit(main())
