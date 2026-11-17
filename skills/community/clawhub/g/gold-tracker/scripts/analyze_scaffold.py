#!/usr/bin/env python3
"""分析脚手架：从 state.json 生成预填的分析日志骨架，LLM 只填推理内容。

消除手写 YAML 模板的结构错误（run_id / timestamp / price_data 自动填充）。
输出追加到 logs/YYYY-MM-DD.yaml（多文档）。LLM 填完 key_factors 后运行 analyze_check.py。

用法:
    python3 scripts/analyze_scaffold.py
"""

import json
import sys

from common import paths, config, atomic, timeutil


def load_state():
    f = paths.resolve("state.json")
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return {}


def build_skeleton(state, tz):
    now = timeutil.now(tz)
    price_usd = state.get("current_price") or 0.0
    price_cny = state.get("price_cny_per_gram") or 0.0
    usd_cny = state.get("usd_cny") or 0.0
    fx_src = (state.get("sources") or {}).get("fx", "")
    return (
        "---\n"
        'run_id: "{run_id}"\n'
        'timestamp: "{ts}"\n'
        "price_data:\n"
        "  gold:\n"
        "    price_usd: {price_usd}\n"
        "    price_cny: {price_cny}\n"
        "  fx:\n"
        "    usd_cny: {usd_cny}\n"
        '    source: "{fx_src}"\n'
        "summary:\n"
        '  focus: "TODO: 一句话核心判断"\n'
        "key_factors:\n"
        '  - factor: "TODO"\n'
        '    impact: "中性"\n'
        '    reasoning: "TODO: 因为X → 所以Y → 对金价影响Z"\n'
        "    sources:\n"
        '      - "TODO: https://..."\n'
        '  - factor: "TODO"\n'
        '    impact: "中性"\n'
        '    reasoning: "TODO"\n'
        "    sources:\n"
        '      - "TODO: https://..."\n'
        "sources:\n"
        '  - "TODO: https://..."\n'
        '  - "TODO: https://..."\n'
    ).format(run_id=now.strftime("%Y%m%d-%H%M"), ts=now.isoformat(),
             price_usd=price_usd, price_cny=price_cny, usd_cny=usd_cny, fx_src=fx_src)


def main():
    paths.ensure_env()
    cfg = config.load()
    tz = config.dig(cfg, "general.timezone", "Asia/Shanghai")
    skeleton = build_skeleton(load_state(), tz)

    day = timeutil.today_str(tz)
    f = paths.resolve("logs") / (day + ".yaml")
    f.parent.mkdir(parents=True, exist_ok=True)
    existing = f.read_text(encoding="utf-8") if f.exists() else ""
    body = (existing.rstrip() + "\n" + skeleton + "\n") if existing.strip() else (skeleton + "\n")
    atomic.atomic_write_text(f, body)

    print(skeleton)
    print("\n[已写入] {}".format(f.relative_to(paths.ROOT)))
    print("[下一步] 填好 key_factors 后运行: python3 scripts/analyze_check.py")


if __name__ == "__main__":
    main()
