#!/usr/bin/env python3
"""简报生成器（渠道无关，P1-12）。

核心输出为纯文本 + 轻量 markdown，长度受 config.output.max_push_bytes 限制。
渠道特定格式（HTML 邮件、富文本卡片等）由通知适配器负责，不进核心。

用法:
    python3 scripts/summary.py brief    # 简报（用于推送）
    python3 scripts/summary.py full     # 完整摘要
"""

import json
import sys
from urllib.parse import urlparse

from common import paths, config, history, yamlmini, timeutil


def load_state():
    f = paths.resolve("state.json")
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return {}


def load_latest_log():
    d = paths.resolve("logs")
    empty = {"key_factors": [], "sources": [], "summary": {}}
    if not d.exists():
        return empty
    files = sorted([f for f in d.iterdir() if f.suffix in (".yaml", ".yml")],
                   key=lambda f: f.name, reverse=True)
    if not files:
        return empty
    docs = yamlmini.load_all(files[0].read_text(encoding="utf-8"))
    doc = docs[-1] if docs else {}
    return {
        "key_factors": doc.get("key_factors", []) or [],
        "sources": doc.get("sources", []) or [],
        "summary": doc.get("summary", {}) or {},
    }


_LEGACY_IMPACT = {"bullish": "利多", "bearish": "利空", "mixed": "多空交织",
                  "neutral": "中性", "slightly_bullish": "偏多",
                  "slightly_bearish": "偏空"}


def impact_zh(impact):
    # 兼容旧英文枚举；新值已是中文，直接返回
    return _LEGACY_IMPACT.get(impact, impact or "未知")


def domain_of(url):
    try:
        return urlparse(url).netloc or url
    except Exception:
        return url


def generate_brief(max_bytes=None):
    cfg = config.load()
    if max_bytes is None:
        max_bytes = int(cfg.get("output", {}).get("max_push_bytes", 2000))
    state = load_state()
    log = load_latest_log()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")

    lines = ["黄金追踪 · 简报", ""]
    lines.append("更新时间: {}".format(timeutil.now_iso(tz)[:16]))

    price = state.get("current_price")
    if price:
        chg_pct = state.get("change_pct", 0) or 0
        lines.append("")
        lines.append("当前金价: ${:,.2f}（较上次 {:+.2f}%）".format(price, chg_pct))
        if state.get("data_stale"):
            lines.append("注意: 数据可能过期")
    else:
        lines.append("")
        lines.append("当前金价: no_data")

    if log.get("summary", {}).get("focus"):
        lines.append("")
        lines.append("核心判断: {}".format(log["summary"]["focus"]))

    factors = log.get("key_factors", [])
    if factors:
        lines.append("")
        lines.append("关键因素:")
        for i, f in enumerate(factors[:4], 1):
            title = f.get("factor", "no_data")
            reasoning = f.get("reasoning", "no_data")
            lines.append("{}. [{}] {}".format(i, impact_zh(f.get("impact")), title))
            lines.append("   {}".format(reasoning))

    src_names = list(dict.fromkeys(domain_of(s) for s in log.get("sources", [])))
    if src_names:
        lines.append("")
        lines.append("信息来源: {}".format(" · ".join(src_names[:3])))

    text = "\n".join(lines)
    if len(text.encode("utf-8")) > max_bytes:
        text = _truncate(text, max_bytes)
    return text


def _truncate(text, max_bytes):
    b = text.encode("utf-8")
    if len(b) <= max_bytes:
        return text
    cut = b[:max_bytes].decode("utf-8", errors="ignore")
    return cut + "\n…(截断)"


def generate_full():
    state = load_state()
    log = load_latest_log()
    tz = config.dig(config.load(), "general.timezone", "Asia/Shanghai")

    lines = [
        "# 黄金追踪 — 完整摘要",
        "生成时间: {}".format(timeutil.now_iso(tz)),
        "",
        "## 核心数据",
    ]
    price = state.get("current_price")
    if price:
        lines.append("- 金价: ${:,.2f}".format(price))
        cny = state.get("price_cny_per_gram")
        lines.append("- 人民币: {}/克".format(cny if cny else "no_data"))
        lines.append("- 汇率: {}".format(state.get("usd_cny", "no_data")))
        lines.append("- 变动: {:+.2f} ({:+.2f}%)".format(
            state.get("change_abs", 0) or 0, state.get("change_pct", 0) or 0))
    else:
        lines.append("- no_data")

    focus = log.get("summary", {}).get("focus")
    if focus:
        lines.append("")
        lines.append("## 核心判断")
        lines.append(focus)

    factors = log.get("key_factors", [])
    lines.append("")
    lines.append("## 关键因素（含逻辑链）")
    for i, f in enumerate(factors, 1):
        lines.append("{}. {} [{}]".format(i, f.get("factor", "no_data"), impact_zh(f.get("impact"))))
        lines.append("   - {}".format(f.get("reasoning", "no_data")))
        for s in (f.get("sources") or []):
            lines.append("     - {}".format(s))

    lines.append("")
    lines.append("## 信息来源")
    for s in log.get("sources", []):
        lines.append("- {}".format(s))

    return "\n".join(lines)


def main():
    paths.ensure_env()
    mode = sys.argv[1] if len(sys.argv) > 1 else "brief"
    if mode == "brief":
        print(generate_brief())
    elif mode == "full":
        print(generate_full())
    else:
        print("用法: {} [brief|full]".format(sys.argv[0]))
        sys.exit(1)


if __name__ == "__main__":
    main()
