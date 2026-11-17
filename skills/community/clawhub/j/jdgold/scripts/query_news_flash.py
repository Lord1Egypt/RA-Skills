#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================
# ⚠️ 本文件是「京东黄金 (jdgold)」JoyCode Skill 的组成脚本。
# 执行任何脚本前，必须先阅读 Skill 根目录下的 SKILL.md，
# 严格遵循其中的执行契约、安全脱敏铁律与回复规范，
# 请勿脱离 SKILL.md 指引单独运行本脚本。
# ============================================================
"""黄金快讯查询：通过 cf-gold-ai BFF /api/v1/news-flash/query 调用。

调用需携带 accessToken（BFF 已启用鉴权），token 由 jos._valid_access_token() 提供。

触发词："最近发生了什么" / "查看快讯" / "最近什么事件影响金价"
"""
import argparse, json, sys, urllib.error
import bff_client
import jos

# 黄金资讯流场景ID
GOLD_FEED_TAG_ID = 20225


def fetch_news_flash(tag_id=GOLD_FEED_TAG_ID, page_size=10, last_id="") -> dict:
    """调用 BFF 快讯接口。"""
    access_token = jos._valid_access_token()
    data = bff_client.get(
        bff_client.PATH_NEWS_FLASH,
        {"tagId": tag_id, "pageSize": page_size, "lastId": last_id, "accessToken": access_token},
    )
    return data or {}


def _format_publish_time(pt) -> str:
    """格式化发布时间。接口可能返回时间戳(ms)或字符串。"""
    if not pt:
        return ""
    if isinstance(pt, (int, float)):
        from datetime import datetime
        try:
            ts = int(pt) / 1000
            return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        except (OSError, ValueError):
            return str(pt)
    return str(pt)


def render_news_flash(result: dict) -> str:
    """快讯列表展示。"""
    rl = result.get("resultList", [])
    is_end = result.get("isEnd", True)
    if not rl:
        return "暂无黄金快讯数据。"

    lines = ["【最新金融快讯】"]
    for i, item in enumerate(rl, 1):
        content = item.get("content") or item.get("title") or ""
        pt = _format_publish_time(item.get("publishTime"))
        if content:
            lines.append(f"{i}. {content}")
            if pt:
                lines.append(f"   时间：{pt}")
            lines.append("")

    if not is_end:
        lines.append("--- 还有更多快讯 ---")

    lines.append("")
    lines.append("去继续查看：https://m.jdjygold.com/fg/market-news/?type=1&orderFrom=skill")

    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="黄金快讯查询")
    parser.add_argument("--json", action="store_true", help="输出原始 JSON")
    parser.add_argument("--tag-id", type=int, default=GOLD_FEED_TAG_ID, help="场景ID（默认20225黄金资讯流）")
    parser.add_argument("--page-size", type=int, default=10, help="每页条数")
    parser.add_argument("--claw", help="上报客户端 claw 类型（如 codex、openclaw）")
    args = parser.parse_args(argv)
    bff_client.set_claw(args.claw)

    try:
        result = fetch_news_flash(tag_id=args.tag_id, page_size=args.page_size)
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

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    print(render_news_flash(result))
    sys.exit(0)


if __name__ == "__main__":
    main()
