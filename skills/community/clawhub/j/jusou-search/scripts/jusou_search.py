#!/usr/bin/env python3
"""聚搜GO 统一搜索（零依赖）：一个 Key 调 8 个搜索引擎。

用法：
  JUSOU_API_KEY=jsk_xxx python3 jusou_search.py "搜索词" [--engine exa]
      [--engines baidu,bocha] [--num 5] [--depth basic|advanced|deep]
      [--time-range day|week|month|year] [--merge]

输出：结果打到 stdout（每条 标题/链接/摘要），本次扣分与剩余积分打到 stderr。
退出码：0 成功；2 参数/鉴权/余额等业务错误（原因打到 stderr）。
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("JUSOU_BASE_URL", "https://jusouai.cn").rstrip("/")


def main() -> int:
    ap = argparse.ArgumentParser(description="聚搜GO 统一搜索")
    ap.add_argument("query", help="搜索词")
    ap.add_argument("--engine", default="", help="指定一个引擎，如 exa / baidu / bocha")
    ap.add_argument("--engines", default="", help="多引擎同时搜，逗号分隔，如 baidu,exa")
    ap.add_argument("--num", type=int, default=5, help="每个引擎返回条数 1-10（默认 5）")
    ap.add_argument("--timeout", type=int, default=60, help="请求超时秒数（默认 60）")
    ap.add_argument("--depth", default="basic", choices=["basic", "advanced", "deep"])
    ap.add_argument("--time-range", default="", choices=["", "day", "week", "month", "year"])
    ap.add_argument("--merge", action="store_true", help="多引擎结果合并去重")
    a = ap.parse_args()

    if a.engine and a.engines:
        print("--engine 与 --engines 只能选一个", file=sys.stderr)
        return 2
    key = os.environ.get("JUSOU_API_KEY", "").strip()
    if not key:
        print("缺少环境变量 JUSOU_API_KEY（在 https://jusouai.cn 控制台获取）", file=sys.stderr)
        return 2

    body = {"query": a.query, "num_results": a.num, "depth": a.depth}
    if a.engine:
        body["engine"] = a.engine
    if a.engines:
        body["engines"] = [s.strip() for s in a.engines.split(",") if s.strip()]
    if a.time_range:
        body["time_range"] = a.time_range
    if a.merge:
        body["merge"] = True

    req = urllib.request.Request(
        BASE + "/v1/search", method="POST",
        data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=a.timeout) as r:
            out = json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            msg = json.loads(e.read()).get("error", {}).get("message", "")
        except Exception:
            msg = ""
        print(f"调用失败 HTTP {e.code}：{msg}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"调用失败：{e}", file=sys.stderr)
        return 2

    results = out.get("results")
    if not isinstance(results, list):
        by = out.get("by_engine") or {}
        results = []
        for eng, blk in by.items():
            if isinstance(blk, dict) and blk.get("error"):
                print(f"[{eng}] 失败：{blk.get('error')}", file=sys.stderr)
            for x in (blk or {}).get("results") or []:
                results.append(x)
    for i, x in enumerate(results, 1):
        title = (x.get("title") or "").strip()
        url = x.get("url") or ""
        snip = (x.get("snippet") or x.get("content") or "").strip().replace("\n", " ")
        if title and title != url:
            print(f"{i}. {title}\n   {url}\n   {snip[:200]}")
        else:                                   # 个别结果上游没给标题，只打一行链接
            print(f"{i}. {url}\n   {snip[:200]}")
    b = out.get("billing") or {}
    if b:
        print(f"-- {b.get('summary', '')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
