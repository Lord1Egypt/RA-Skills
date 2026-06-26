#!/usr/bin/env python3
"""
猫眼电影新片抓取脚本 v2 — 纯数据采集，不做过滤
抓取正在热映 + 即将上映的全部电影，每部获取详细信息，输出结构化 JSON
用法：python3 tools/maoyan_movies.py [--compact]
"""

import json
import time
import random
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

# ── 配置 ──────────────────────────────────────────
COMING_LIST_URL = "https://m.maoyan.com/ajax/comingList?ci=10&token=&limit=100"
ON_INFO_URL = "https://m.maoyan.com/ajax/movieOnInfoList"
DETAIL_URL = "https://m.maoyan.com/ajax/detailmovie?movieId={movie_id}"

USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
)
DELAY_MIN = 0.3
DELAY_MAX = 0.5
MAX_RETRIES = 2
CST = timezone(timedelta(hours=8))


def ts_now():
    return datetime.now(CST).isoformat()


def fetch_json(url, timeout=15):
    """带重试的 HTTP GET -> JSON"""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < MAX_RETRIES:
                time.sleep(1 * (attempt + 1))
            else:
                sys.stderr.write(f"  ⚠️ 请求失败: {url[:60]} — {e}\n")
                return None


def get_movie_list(data, key="movieList"):
    """从 API 响应中提取电影列表（兼容不同字段名）"""
    if not data:
        return []
    if key in data and data[key]:
        return data[key]
    # comingList API 返回的是 "coming" 字段
    if "coming" in data and data["coming"]:
        return data["coming"]
    return []


def get_movie_detail(movie_id):
    """获取单部电影详情，失败时返回空 dict"""
    url = DETAIL_URL.format(movie_id=movie_id)
    try:
        data = fetch_json(url)
        if data and "detailMovie" in data:
            return data["detailMovie"]
    except Exception:
        pass
    return {}


def collect_all_movies():
    """收集所有电影（去重），返回 basic 信息 dict"""
    all_movies = {}  # id -> {minimal info}

    # 1. 正在热映
    sys.stderr.write("📡 获取正在热映列表...\n")
    data = fetch_json(ON_INFO_URL)
    if data:
        for m in get_movie_list(data, "movieList"):
            mid = m.get("id")
            if mid:
                all_movies[mid] = {
                    "nm": m.get("nm", ""),
                    "rt": m.get("rt", ""),
                    "sc": m.get("sc", 0),
                    "star": m.get("star", ""),
                    "showInfo": m.get("showInfo", ""),
                    "wish": m.get("wish", 0),
                    "source": "now_showing",
                }

    # 2. 即将上映
    sys.stderr.write("📡 获取即将上映列表...\n")
    data = fetch_json(COMING_LIST_URL)
    if data:
        for m in get_movie_list(data, "coming"):
            mid = m.get("id")
            if mid and mid not in all_movies:
                all_movies[mid] = {
                    "nm": m.get("nm", ""),
                    "rt": m.get("rt", ""),
                    "sc": m.get("sc", 0),
                    "star": m.get("star", ""),
                    "showInfo": m.get("showInfo", ""),
                    "wish": m.get("wish", 0),
                    "source": "coming",
                }

    sys.stderr.write(f"📊 共获取 {len(all_movies)} 部电影（去重后）\n")
    return all_movies


def enrich_movies(all_movies):
    """为每部电影获取详情，输出 now_showing 和 coming 两个列表"""
    now_showing = []
    coming = []
    total = len(all_movies)
    fail_count = 0

    for i, (mid, info) in enumerate(all_movies.items()):
        sys.stderr.write(f"\r🔍 {i+1}/{total} {info['nm']}...")
        sys.stderr.flush()

        detail = get_movie_detail(mid)

        # 构建输出条目
        entry = {
            "nm": info["nm"],
            "rt": info.get("rt", ""),
            "sc": info.get("sc", 0),
            "star": info.get("star", ""),
            "showInfo": info.get("showInfo", ""),
            "wish": info.get("wish", 0),
        }

        if detail:
            entry["cat"] = detail.get("cat", "") or ""
            entry["dra"] = detail.get("dra", "") or ""
            entry["dur"] = detail.get("dur", 0) or 0
            entry["src"] = detail.get("src", "") or ""
            entry["dir"] = detail.get("dir", "") or ""
            # 额外字段
            entry["vd"] = detail.get("vd", "") or ""  # 视频预告
            entry["ver"] = detail.get("ver", "") or ""  # 版本（IMAX/CINITY/重映）
            entry["publishDate"] = detail.get("publishDate", "") or ""  # 实际发版日
        else:
            fail_count += 1
            entry["cat"] = ""
            entry["dra"] = ""
            entry["dur"] = 0
            entry["src"] = ""
            entry["dir"] = ""

        if info["source"] == "now_showing":
            now_showing.append(entry)
        else:
            coming.append(entry)

        time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))

    sys.stderr.write(f"\n✅ 详情获取完毕，成功: {total - fail_count}，失败: {fail_count}\n")
    return now_showing, coming


def main():
    compact = "--compact" in sys.argv

    all_movies = collect_all_movies()
    now_showing, coming = enrich_movies(all_movies)

    output = {
        "scan_time": ts_now(),
        "now_showing": now_showing,
        "coming": coming,
        "stats": {
            "now_showing_count": len(now_showing),
            "coming_count": len(coming),
            "total": len(now_showing) + len(coming),
        },
    }

    if compact:
        json.dump(output, sys.stdout, ensure_ascii=False, separators=(",", ":"))
    else:
        json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
