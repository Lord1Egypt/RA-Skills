#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金早报查询：通过 cf-gold-ai BFF /api/v1/morning-report/query 调用。"""
import argparse, json, sys, urllib.error
import bff_client
import jos


def fetch_morning_report(page_size=20) -> dict:
    """调用 BFF 早报接口，返回业务 data。"""
    access_token = jos._valid_access_token()
    data = bff_client.get(
        bff_client.PATH_MORNING_REPORT,
        {"accessToken": access_token, "pageSize": page_size},
    )
    return data or {}


def render_morning_report_list(data: dict) -> str:
    """多条早报列表展示。"""
    items = data.get("articleList") or data.get("list") or data.get("morningReportList") or []
    # 过滤掉"高客早报"标签的文章，只保留社区早报
    items = [it for it in items if not (it.get("label") == "高客早报" or (it.get("trackExt") and it.get("trackExt", {}).get("label") == "高客早报"))]
    if not items:
        return "暂无黄金早报数据。"
    lines = []
    for i, item in enumerate(items, 1):
        title = item.get("title") or item.get("titleName") or f"早报#{i}"
        date_str = item.get("publishDate") or item.get("publishTime") or ""
        jump_url = item.get("jumpUrl") or item.get("url") or ""
        content = item.get("content") or ""
        lines.append("【黄金早报】")
        lines.append(title)
        if date_str:
            lines.append(f"日期：{date_str}")
        if content:
            lines.append("")
            lines.append("核心要点：")
            lines.append(content[:200] + "..." if len(content) > 200 else content)
        if jump_url:
            lines.append("")
            lines.append(f"查看原文：{jump_url}")
        lines.append("---")
    return "\n".join(lines)


def render_morning_report(data: dict) -> str:
    """单条早报展示（取第一条）。"""
    items = data.get("articleList") or data.get("list") or data.get("morningReportList") or []
    if not items:
        return "暂无黄金早报数据。"
    item = items[0]
    title = item.get("title") or item.get("titleName") or "黄金早报"
    date_str = item.get("publishDate") or item.get("publishTime") or ""
    jump_url = item.get("jumpUrl") or item.get("url") or ""
    content = item.get("content") or ""

    lines = ["【黄金早报】"]
    lines.append(title)
    if date_str:
        lines.append(f"日期：{date_str}")
    if content:
        lines.append("")
        lines.append("核心要点：")
        lines.append(content[:300] + "..." if len(content) > 300 else content)
    if jump_url:
        lines.append("")
        lines.append(f"查看原文：{jump_url}")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="黄金早报查询")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--all", action="store_true", help="输出多条早报列表")
    parser.add_argument("--page-size", type=int, default=20, help="每页条数")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args(argv)
    bff_client.set_claw(args.claw)

    try:
        data = fetch_morning_report(page_size=args.page_size)
    except urllib.error.URLError as e:
        print(f"[内部] 网络错误: {e}", file=sys.stderr)
        print("查询暂时失败，请稍后重试")
        sys.exit(3)
    except bff_client.BffError as e:
        if getattr(e, "code", None) == 403:
            print(e.message)
            sys.exit(3)
        print(f"[内部] {e}", file=sys.stderr)
        print("查询暂时失败，请稍后重试")
        sys.exit(3)
    except RuntimeError as e:
        print(f"[内部] {e}", file=sys.stderr)
        print("查询暂时失败，请稍后重试")
        sys.exit(3)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        sys.exit(0)

    if args.all:
        print(render_morning_report_list(data))
    else:
        print(render_morning_report(data))
    sys.exit(0)


if __name__ == "__main__":
    main()
