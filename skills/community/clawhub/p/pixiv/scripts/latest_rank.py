#!/usr/bin/env python3
"""
稳定获取 Pixiv 日榜前50（今日优先，自动回退到最近可用日期）。
默认仅拉取榜单信息，不下载图片。
"""

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

import requests


def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "_", name).strip() or "untitled"


def fetch_daily_ranking(limit: int = 50, lookback_days: int = 7, proxy: str | None = None):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://www.pixiv.net/",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
    )
    if proxy:
        session.proxies.update({"http": proxy, "https": proxy})

    base_url = "https://www.pixiv.net/ranking.php"

    for days_ago in range(lookback_days + 1):
        target_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y%m%d")
        params = {
            "mode": "daily",
            "content": "illust",
            "format": "json",
            "date": target_date,
            "p": 1,
        }

        try:
            resp = session.get(base_url, params=params, timeout=20)
            if resp.status_code != 200:
                print(f"[{target_date}] 请求失败: HTTP {resp.status_code}")
                continue

            data = resp.json()
            contents = data.get("contents", [])
            if not contents:
                err = data.get("error") or "无榜单数据"
                print(f"[{target_date}] 不可用: {err}")
                continue

            return target_date, contents[:limit], session
        except requests.RequestException as e:
            print(f"[{target_date}] 网络错误: {e}")
        except ValueError:
            print(f"[{target_date}] 返回非JSON")

    raise RuntimeError(f"最近 {lookback_days + 1} 天都未获取到可用日榜")


def main():
    parser = argparse.ArgumentParser(description="获取 Pixiv 日榜前50（今日优先，自动回退）")
    parser.add_argument("--limit", type=int, default=50, help="返回条数，默认50")
    parser.add_argument("--lookback", type=int, default=7, help="最多回退天数，默认7")
    parser.add_argument("--proxy", default=None, help="可选代理，如 http://127.0.0.1:7890")
    parser.add_argument("--download", action="store_true", help="是否下载封面图")
    parser.add_argument("--out", default="./downloads/latest_rank", help="下载目录")
    parser.add_argument("--save-json", default="", help="可选：保存榜单JSON文件路径")
    args = parser.parse_args()

    rank_date, items, session = fetch_daily_ranking(
        limit=args.limit,
        lookback_days=args.lookback,
        proxy=args.proxy,
    )

    print(f"使用榜单日期: {rank_date}，共 {len(items)} 条")

    result = []
    out_dir = Path(args.out)
    if args.download:
        out_dir.mkdir(parents=True, exist_ok=True)

    for idx, item in enumerate(items, 1):
        title = item.get("title", "")
        user_name = item.get("user_name", "")
        illust_id = str(item.get("illust_id", ""))
        # ranking.php 的 url 通常已是可下载图片链接（不保证原图）
        image_url = item.get("url", "")

        row = {
            "rank": idx,
            "title": title,
            "author": user_name,
            "illust_id": illust_id,
            "image_url": image_url,
            "page_url": f"https://www.pixiv.net/artworks/{illust_id}" if illust_id else "",
        }
        result.append(row)
        print(f"{idx:02d}. {title} - {user_name} ({illust_id})")

        if args.download and image_url:
            ext = Path(image_url.split("?")[0]).suffix or ".jpg"
            filename = f"{idx:02d}_{sanitize_filename(title)}_{illust_id}{ext}"
            save_path = out_dir / filename
            if save_path.exists():
                continue
            try:
                img_resp = session.get(image_url, timeout=20)
                if img_resp.status_code == 200:
                    save_path.write_bytes(img_resp.content)
                else:
                    print(f"   下载失败 HTTP {img_resp.status_code}: {image_url}")
            except requests.RequestException as e:
                print(f"   下载失败: {e}")

    if args.save_json:
        Path(args.save_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.save_json).write_text(
            json.dumps({"date": rank_date, "items": result}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"已保存JSON: {args.save_json}")


if __name__ == "__main__":
    main()
