#!/usr/bin/env python3
"""痛点雷达 · Pain-Point Radar 命令行客户端（给 OpenClaw 技能用）。只用 Python 3.8+ 标准库。

给一个产品、品类或品牌，调用 https://linkdigest.dev/api/v1/radar：先看大家在搜什么
（百度、淘宝、Bing / YouTube 的搜索联想），再读小红书 + 抖音（出海：YouTube + TikTok）上
排在前面的内容和热门评论，把相同的痛点、需求、购买顾虑归到一起，由代码数出每一条出现在
几篇里，每条附逐字核对过的原话；有人在搜、读到的内容都没讲的列成「机会」。一次通常
10–20 分钟（读取在服务端排队），本脚本每 15 秒取一次结果，最多等 --timeout 秒。

只连 linkdigest.dev 这一个域名，不读本地文件，不写任何文件。密钥取自 LINKDIGEST_API_KEY。

用法:
  python3 radar.py "扫地机器人"                          # 国内（小红书 + 抖音），输出 Markdown
  python3 radar.py "robot vacuum" --market global        # 出海（YouTube + TikTok），中文报告、英文原话
  python3 radar.py "露营车" --size standard              # 速查 quick 12 篇 / 标准 standard 24 / 深度 deep 48
  python3 radar.py "露营车" --preview                    # 只看搜索需求词（1 积分）
  python3 radar.py "露营车" --format json                # 结构化结果
  python3 radar.py --radar-id <id>                       # 接着取一次已经开始的雷达（不重复扣费）
  python3 radar.py "露营车" --dry-run                    # 只打印将要发送的请求，不联网

退出码: 0 成功；1 其他错误；2 参数或密钥缺失；3 密钥无效(401)；4 积分不够(402，未扣费)；
        6 调用太频繁(429)；7 等待超时（雷达仍在跑，用 --radar-id 接着取）；8 雷达失败（未扣汇总费）
"""

from __future__ import annotations

import argparse
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://linkdigest.dev/api/v1/radar"
KEYS_URL = "https://linkdigest.dev/app/keys"
_SKILL = re.sub(r"[^a-z0-9-]", "", os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).lower())[:48]
USER_AGENT = "linkdigest-openclaw-skill/1.0.0" + (f" ({_SKILL})" if _SKILL else " (radar)")
# The overseas skill defaults to the global market; everything else to cn.
DEFAULT_MARKET = "global" if _SKILL.startswith("overseas") else "cn"
POLL_SECONDS = 15

EXIT_OK, EXIT_ERROR, EXIT_USAGE, EXIT_AUTH, EXIT_PAYMENT = 0, 1, 2, 3, 4
EXIT_RATE_LIMITED, EXIT_TIMEOUT, EXIT_FAILED = 6, 7, 8

_SSL = {"context": None, "certifi": False}


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def _use_certifi() -> bool:
    """python.org Python on macOS ships without CA certificates; try certifi's bundle once."""
    if _SSL["certifi"]:
        return False
    try:
        import certifi  # type: ignore
    except ImportError:
        return False
    _SSL["context"] = ssl.create_default_context(cafile=certifi.where())
    _SSL["certifi"] = True
    return True


def call(method: str, url: str, key: str, body: dict | None = None, timeout: float = 60):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL["context"]) as resp:
            status, raw = resp.status, resp.read()
    except urllib.error.HTTPError as err:
        status, raw = err.code, err.read()
    except urllib.error.URLError as err:
        reason = getattr(err, "reason", err)
        if (isinstance(reason, ssl.SSLCertVerificationError) or "CERTIFICATE_VERIFY_FAILED" in str(err)) and _use_certifi():
            return call(method, url, key, body, timeout)
        raise
    text = raw.decode("utf-8", errors="replace")
    try:
        return status, json.loads(text)
    except ValueError:
        return status, text


def field(payload, name: str, default=None):
    return payload.get(name, default) if isinstance(payload, dict) else default


def fail(status: int, payload) -> int:
    message = str(field(payload, "error") or payload)[:500]
    if status == 400:
        log(f"请求有误 (400): {message}")
        return EXIT_USAGE
    if status == 401:
        log(f"API Key 无效或缺失 (401): {message}\n在 {KEYS_URL} 创建 Key（注册送 10 积分，不用卡），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return EXIT_AUTH
    if status == 402:
        log(f"积分不够 (402 {field(payload, 'error_code', '')})，本次没有扣费: {message}")
        need, left = field(payload, "credits_needed"), field(payload, "credits_left")
        if need is not None:
            log(f"这次至少需要 {need} 积分，账户剩 {left}。")
        for name, label in (("starter_url", "¥9.9 买 50 积分（支付宝，一次性）"), ("buy_url", "加量包"), ("subscribe_url", "订阅")):
            link = field(payload, name)
            if link:
                log(f"{label}: {link}")
        offer = field(payload, "offer_zh")
        if offer:
            log(str(offer))
        return EXIT_PAYMENT
    if status == 404:
        log("没找到这次雷达（id 不对，或不是这个 Key 的账户跑的）。")
        return EXIT_USAGE
    if status == 429:
        log(f"调用太频繁 (429): {message}")
        return EXIT_RATE_LIMITED
    log(f"服务端返回 {status}: {message}")
    return EXIT_ERROR


def _quote(q: dict) -> str:
    gloss = f"（{q['gloss']}）" if q.get("gloss") else ""
    return f"「{q.get('text', '')}」{gloss} · 第 {q.get('note')} 篇"


def emit(summary: dict, fmt: str) -> int:
    status = summary.get("status")
    if status == "failed":
        log(f"雷达没有完成: {summary.get('error') or '未知原因'}（不足 3 篇读成时不收汇总费）")
        return EXIT_FAILED
    if fmt == "json":
        out = dict(summary)
        radar = dict(out.get("radar") or {})
        radar.pop("raw_markdown", None)
        out["radar"] = radar
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        radar = summary.get("radar") or {}
        md = radar.get("raw_markdown")
        if md:
            print(md)
        else:
            posts = radar.get("posts") or summary.get("posts_read") or 0
            print(f"# 痛点雷达：{summary.get('topic')}\n\n{radar.get('summary', '')}\n")
            for key, title in (("pain", "痛点"), ("needs", "需求与卖点"), ("blockers", "购买顾虑"), ("gaps", "机会")):
                points = (radar.get("sections") or {}).get(key) or []
                if points:
                    print(f"## {title}")
                    for p in points:
                        head = f"- {p['label']} — {p['count_posts']}/{posts} 篇" if key != "gaps" else f"- {p['label']}"
                        quote = f" · {_quote(p['quotes'][0])}" if p.get("quotes") else ""
                        print(head + quote)
                    print()
        share = summary.get("share_url")
        if share:
            print(f"\n分享链接（30 天有效，不用登录）：{share}")
    log(f"用了 {summary.get('credits_total', 0)} 积分（估算 {summary.get('estimate', '?')}），读了 {summary.get('posts_read', 0)} 篇。")
    return EXIT_OK


def wait(key: str, radar_id: str, fmt: str, timeout: int) -> int:
    url = f"{API}/{urllib.parse.quote(radar_id, safe='')}"
    deadline = time.monotonic() + timeout
    last = None
    while True:
        try:
            status, payload = call("GET", url, key)
        except (urllib.error.URLError, OSError) as err:
            log(f"取结果时连不上（会重试）: {err}")
            status, payload = 0, None
        if status == 200:
            return emit(payload, fmt)
        if status not in (0, 202):
            return fail(status, payload)
        if status == 202:
            stage = (field(payload, "status"), field(payload, "posts_read"))
            if stage != last:
                log(f"进行中: {stage[0]}，已读 {stage[1] or 0} 篇")
                last = stage
        if time.monotonic() > deadline:
            log(f"等了 {timeout} 秒还没完成（读取在服务端排队）。稍后用 --radar-id {radar_id} 接着取，不会重复扣费。")
            return EXIT_TIMEOUT
        time.sleep(POLL_SECONDS)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="痛点雷达：一个品类，大家在抱怨什么、在搜什么、什么没人回答。")
    ap.add_argument("topic", nargs="?", help="产品、品类或品牌，1–40 个字")
    ap.add_argument("--market", choices=("cn", "global"), default=DEFAULT_MARKET, help="cn：小红书 + 抖音；global：YouTube + TikTok")
    ap.add_argument("--size", choices=("quick", "standard", "deep"), default="quick", help="12 / 24 / 48 篇")
    ap.add_argument("--language", choices=("zh-CN", "en", "ja"), default="zh-CN")
    ap.add_argument("--weekly", action="store_true", help="每周自动再跑一次，并对比变化")
    ap.add_argument("--preview", action="store_true", help="只看搜索需求词（1 积分）")
    ap.add_argument("--format", choices=("markdown", "json"), default="markdown")
    ap.add_argument("--radar-id", help="接着取一次已经开始的雷达")
    ap.add_argument("--timeout", type=int, default=1800, help="最多等多少秒（默认 1800）")
    ap.add_argument("--dry-run", action="store_true", help="只打印请求，不联网")
    a = ap.parse_args(argv)

    if not a.radar_id and not (a.topic or "").strip():
        ap.print_usage(sys.stderr)
        log("请给一个产品、品类或品牌，例如：python3 radar.py \"扫地机器人\"")
        return EXIT_USAGE
    topic = (a.topic or "").strip()
    if len(topic) > 40 or re.search(r"https?://", topic):
        log("topic 是一个品类或品牌名（1–40 个字），不是链接。要读一条链接请用 linkdigest 技能。")
        return EXIT_USAGE
    body = {"topic": topic, "market": a.market} if a.preview else {
        "topic": topic, "market": a.market, "size": a.size, "language": a.language, **({"weekly": True} if a.weekly else {})
    }
    if a.dry_run:
        target = f"{API}/{a.radar_id}" if a.radar_id else (f"{API}/preview" if a.preview else API)
        print(json.dumps({"method": "GET" if a.radar_id else "POST", "url": target, "body": None if a.radar_id else body, "user_agent": USER_AGENT}, ensure_ascii=False))
        return EXIT_OK

    key = os.environ.get("LINKDIGEST_API_KEY", "").strip()
    if not key:
        log(f"没有设置 LINKDIGEST_API_KEY。在 {KEYS_URL} 创建 Key（注册送 10 积分，不用卡），然后 export LINKDIGEST_API_KEY=ld_live_...")
        return EXIT_USAGE
    if a.radar_id:
        return wait(key, a.radar_id, a.format, a.timeout)
    try:
        status, payload = call("POST", f"{API}/preview" if a.preview else API, key, body, timeout=90)
    except (urllib.error.URLError, OSError) as err:
        log(f"连不上 linkdigest.dev: {err}")
        return EXIT_ERROR
    if a.preview:
        if status != 200:
            return fail(status, payload)
        demand = field(payload, "demand", payload)
        if a.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"# 搜索需求：{topic}\n")
            for c in field(demand, "clusters", []) or []:
                print(f"- {c.get('label')}：" + "、".join((c.get("terms") or [])[:10]))
        log(f"用了 {field(payload, 'credits', 1)} 积分。")
        return EXIT_OK
    if status not in (200, 202):
        return fail(status, payload)
    radar_id = field(payload, "radar_id")
    log(f"雷达已开始：{radar_id}，估算约 {field(payload, 'estimate')} 积分，读 {field(payload, 'posts_wanted')} 篇；通常 10–20 分钟。")
    return wait(key, radar_id, a.format, a.timeout)


if __name__ == "__main__":
    sys.exit(main())
