#!/usr/bin/env python3
import argparse
import json
import sys

RISK_KEYWORDS = [
    "转账", "红包", "付款", "验证码", "密码", "token", "cookie",
    "忽略", "立刻", "马上", "客服", "官方通知"
]


def fail(msg: str, code: int = 1):
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)


def score(text: str):
    t = text.lower()
    hits = [k for k in RISK_KEYWORDS if k.lower() in t]
    s = min(100, len(hits) * 18)
    if any(k in t for k in ["转账", "红包", "验证码", "token", "cookie", "私发"]):
        s = min(100, s + 30)
    level = "高风险伪造" if s >= 70 else ("存疑" if s >= 35 else "待核验")
    return {"risk_score": s, "risk_level": level, "keyword_hits": hits}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    args = ap.parse_args()
    if not args.text.strip():
        fail("--text cannot be empty")
    print(json.dumps(score(args.text), ensure_ascii=False))


if __name__ == "__main__":
    main()
