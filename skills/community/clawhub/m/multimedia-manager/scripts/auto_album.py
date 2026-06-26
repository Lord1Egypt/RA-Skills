#!/usr/bin/env python3
"""Auto-create smart albums by clustering images on date/tags/category."""

import sys
import os
import json
from collections import defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from image_db import (get_db, init_db, search_images, create_album,
                      add_to_album, list_albums)


def cluster_by_date(conn) -> dict:
    """Group images by date for date-based albums."""
    images = search_images(conn, limit=1000)
    by_date = defaultdict(list)
    for img in images:
        date = (img.get("taken_at") or img.get("created_at") or "")[:10]
        if date:
            by_date[date].append(img)
    return {d: imgs for d, imgs in by_date.items() if len(imgs) >= 3}


def cluster_by_tag_theme(conn) -> dict:
    """Group images by common tag themes."""
    images = search_images(conn, limit=1000)
    themes = {
        "家庭时光": {"家庭", "孩子", "宝宝", "小孩", "女孩", "男孩", "亲子", "family"},
        "户外风景": {"户外", "风景", "自然", "天空", "草地", "公园", "海边", "山"},
        "美食甜品": {"美食", "食物", "甜品", "冰淇淋", "水果", "蛋糕", "饮料"},
        "科技插画": {"科技", "AI", "技术", "插画", "图表", "架构", "网络"},
        "旅行记录": {"旅行", "旅游", "城市", "景点", "纽约", "建筑"},
        "运动活动": {"运动", "帆船", "骑行", "跑步", "游泳", "球"},
        "动物萌宠": {"动物", "猫", "狗", "企鹅", "鸟", "马", "宠物"},
    }
    result = defaultdict(list)
    for img in images:
        try:
            img_tags = set(json.loads(img.get("tags", "[]")))
        except (json.JSONDecodeError, TypeError):
            img_tags = set()
        desc = (img.get("description") or "").lower()
        for theme_name, keywords in themes.items():
            if img_tags & keywords or any(k in desc for k in keywords):
                result[theme_name].append(img)
                break
    return {name: imgs for name, imgs in result.items() if len(imgs) >= 2}


def cluster_by_person(conn) -> dict:
    """Group images by detected people/faces."""
    images = search_images(conn, limit=1000)
    by_person = defaultdict(list)
    for img in images:
        try:
            faces = json.loads(img.get("face_names", "[]"))
        except (json.JSONDecodeError, TypeError):
            faces = []
        for face in faces:
            if face and face not in ("未知",):
                by_person[face].append(img)
    return {p: imgs for p, imgs in by_person.items() if len(imgs) >= 2}


def auto_create_albums(dry_run=False):
    init_db()
    conn = get_db()
    existing = {a["name"] for a in list_albums(conn)}
    created = []

    tag_clusters = cluster_by_tag_theme(conn)
    for name, images in tag_clusters.items():
        album_name = f"📁 {name}"
        if album_name not in existing:
            if not dry_run:
                aid = create_album(conn, album_name, f"自动创建：{name}主题")
                for img in images:
                    add_to_album(conn, aid, img["id"])
            created.append({"name": album_name, "count": len(images)})

    person_clusters = cluster_by_person(conn)
    for person, images in person_clusters.items():
        album_name = f"👤 {person}"
        if album_name not in existing:
            if not dry_run:
                aid = create_album(conn, album_name, f"自动创建：{person}的照片")
                for img in images:
                    add_to_album(conn, aid, img["id"])
            created.append({"name": album_name, "count": len(images)})

    date_clusters = cluster_by_date(conn)
    for date, images in sorted(date_clusters.items(), reverse=True)[:5]:
        album_name = f"📅 {date}"
        if album_name not in existing:
            if not dry_run:
                aid = create_album(conn, album_name, f"自动创建：{date}的照片")
                for img in images:
                    add_to_album(conn, aid, img["id"])
            created.append({"name": album_name, "count": len(images)})

    conn.close()
    return created


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Auto-create smart albums")
    p.add_argument("--dry-run", action="store_true", help="Preview without creating")
    args = p.parse_args()
    results = auto_create_albums(dry_run=args.dry_run)
    prefix = "[DRY RUN] " if args.dry_run else ""
    for r in results:
        print(f"{prefix}Created: {r['name']} ({r['count']} images)")
    if not results:
        print("No new albums to create.")
