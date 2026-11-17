#!/usr/bin/env python3
"""L2 多引擎真实反爬穿透测试（2026-09-06 · v1.4.2 实测）。

目标矩阵：
  bot.sannysoft.com      webdriver/自动化特征检测（金标准）
  cloudflare /cdn-cgi/trace   Cloudflare 放行判定
  zhihu.com/hot          curl 403 反爬拦截（UA/TLS 指纹层）
  36kr.com / toutiao.com JS 重渲染 + 反爬
  jianshu.com            JS 渲染动态内容
对照：example.com（无防护基线）

引擎对照：patchright（stealth 注入）vs 原生 chromium（裸奔对照）
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "/sandbox/workspace/skills/infoseek/scripts")
import l2_renderer as lr

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36")

TARGETS = [
    {"name": "example(基线)", "url": "https://example.com", "expect": "Example Domain"},
    {"name": "cloudflare_trace", "url": "https://www.cloudflare.com/cdn-cgi/trace",
     "expect_key": "fl=", "expect_in": True},
    {"name": "zhihu_hot(403目标)", "url": "https://www.zhihu.com/hot",
     "expect_in": False, "expect_key": "机器人验证"},
    {"name": "sannysoft_bot检测", "url": "https://bot.sannysoft.com", "expect": "Antibot"},
    {"name": "jianshu_JS渲染", "url": "https://www.jianshu.com", "expect_key": "简书"},
    {"name": "36kr_JS渲染", "url": "https://36kr.com", "expect_key": "36氪"},
    {"name": "toutiao_JS渲染", "url": "https://www.toutiao.com", "expect_key": "首页"},
]


def analyze(name, url, html, el):
    out = {"url": url, "engine": el, "len": len(html), "title": "",
           "hit_expect": None, "blocked": False, "note": ""}
    if not html:
        out["note"] = "EMPTY(降级L1)"
        return out
    import re
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    out["title"] = m.group(1).strip()[:60] if m else ""
    lo = html.lower()
    # 拦截特征
    for kw in ("checking your browser", "cf-challenge", "just a moment",
               "captcha", "验证码", "访问过于频繁", "安全验证", "robot check",
               "请开启js", "verify you are human"):
        if kw.lower() in lo:
            out["blocked"] = True
            out["note"] = f"拦截特征:{kw}"
            break
    # 目标命中判定
    exp = None
    for t in TARGETS:
        if t["name"] == name:
            exp = t
            break
    if exp:
        key = exp.get("expect_key") or exp.get("expect")
        if key:
            if exp.get("expect_in", True):
                out["hit_expect"] = key.lower() in lo
            else:
                out["hit_expect"] = key.lower() not in lo
    # sannysoft 专项：仅统计 class 含 failed 的检测行（result passed 不算）
    if "sannysoft" in url:
        frows = re.findall(r'<td[^>]*>(.*?)</td>\s*<td[^>]*class="failed"[^>]*>', html, re.S)
        out["note"] = f"FAIL项={len(frows)}"
        for n in frows[:6]:
            out["note"] += "| " + re.sub(r'<[^>]+>|\s+', '', n)[:26]
    return out


def run_one(url, render, el_name, timeout=25):
    t0 = time.time()
    try:
        html = render(url, timeout)
    except Exception as e:
        return {"url": url, "engine": el_name, "error": str(e)[:100], "secs": round(time.time() - t0, 1)}
    return {"html": html, "secs": round(time.time() - t0, 1)}


def main():
    results = []
    print("=" * 90)
    print("引擎可用性:", {k: v["available"] for k, v in lr.engine_status().items()})
    print("=" * 90)
    for t in TARGETS:
        name, url = t["name"], t["url"]
        # 1) 默认路由（default 场景：patchright 实际命中）
        r1 = run_one(url, lr.render_html, "route(patchright)")
        if "error" in r1:
            print(f"\n[{name}] 路由失败: {r1['error']}"); continue
        row = analyze(name, url, r1.get("html", ""), "route(patchright)")
        row["secs"] = r1["secs"]
        print(f"\n[{name}] {url}")
        print(f"  route: len={row['len']} title={row['title']!r} hit={row['hit_expect']} {row['note']} ({row['secs']}s)")
        results.append({"target": name, **row})
        # 2) sannysoft/zhihu 加裸 chromium 对照
        if name in ("sannysoft_bot检测", "zhihu_hot(403目标)", "cloudflare_trace"):
            r2 = run_one(url, lr._render_chromium, "chromium裸")
            row2 = analyze(name, url, r2.get("html", ""), "chromium裸")
            row2["secs"] = r2["secs"]
            print(f"  chromium裸对照: len={row2['len']} hit={row2['hit_expect']} {row2['note']} ({row2['secs']}s)")
            results.append({"target": name + "_裸", **row2})
    with open("/tmp/l2_pen_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n结果已存 /tmp/l2_pen_results.json")


if __name__ == "__main__":
    main()
