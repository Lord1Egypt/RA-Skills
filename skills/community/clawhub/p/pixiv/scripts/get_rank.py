#!/usr/bin/env python3
"""下载 Pixiv 日榜前50（自动回退到最近可用日期）。"""

from datetime import datetime, timedelta
from pathlib import Path
import re

import requests
import yaml


def safe_name(s: str) -> str:
    return re.sub(r'[\\/:*?"<>|]+', "_", s).strip() or "untitled"


with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

pixiv_cfg = config.get("pixiv", {})
download_dir = Path(pixiv_cfg.get("download_dir", "./downloads")) / "daily_rank"
download_dir.mkdir(parents=True, exist_ok=True)

session = requests.Session()
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Cookie": pixiv_cfg.get("cookie", ""),
        "Referer": "https://www.pixiv.net/",
    }
)
proxy = pixiv_cfg.get("proxy")
if proxy:
    session.proxies.update({"http": proxy, "https": proxy})

print("正在获取Pixiv日榜（今日优先，自动回退）...")
rank_items = []
used_date = None

for d in range(8):
    date = (datetime.now() - timedelta(days=d)).strftime("%Y%m%d")
    url = "https://www.pixiv.net/ranking.php"
    params = {"mode": "daily", "content": "illust", "format": "json", "p": 1, "date": date}
    try:
        resp = session.get(url, params=params, timeout=20)
        if resp.status_code != 200:
            print(f"[{date}] 请求失败：HTTP {resp.status_code}")
            continue
        data = resp.json()
        rank_items = data.get("contents", [])[:50]
        if rank_items:
            used_date = date
            break
        print(f"[{date}] 无榜单数据：{data.get('error', 'unknown')}")
    except Exception as e:
        print(f"[{date}] 请求异常：{e}")

if not rank_items:
    raise SystemExit("最近8天都没有可用日榜，退出。")

print(f"使用榜单日期：{used_date}，获取到{len(rank_items)}个作品")

for idx, item in enumerate(rank_items, 1):
    try:
        title = item.get("title", "")
        illust_id = str(item.get("illust_id", ""))
        img_url = item.get("url", "")

        if not img_url:
            print(f"第{idx}个作品无图片地址，跳过")
            continue

        ext = Path(img_url.split("?")[0]).suffix or ".jpg"
        save_path = download_dir / f"{idx:02d}_{safe_name(title)}_{illust_id}{ext}"
        if save_path.exists():
            print(f"第{idx}个作品已存在，跳过")
            continue

        print(f"正在下载第{idx}个作品：{title}")
        img_resp = session.get(img_url, timeout=20)
        if img_resp.status_code == 200:
            save_path.write_bytes(img_resp.content)
            print(f"下载完成：{save_path}")
        else:
            print(f"下载失败（HTTP {img_resp.status_code}）：{title}")
    except Exception as e:
        print(f"第{idx}个作品下载失败：{e}")

print(f"日榜下载完成！图片保存在：{download_dir}")
