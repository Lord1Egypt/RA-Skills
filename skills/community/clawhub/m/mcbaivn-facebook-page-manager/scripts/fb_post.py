#!/usr/bin/env python3
"""
Facebook Page Manager - Post Script
Supports: text post, photo post, video, carousel, story, scheduled posts
"""

import argparse
import json
import sys
import time
import os
import requests
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────────
GRAPH_API = "https://graph.facebook.com/v19.0"


def get_config():
    """Load token & page_id from env or fb_config.json"""
    config_path = os.path.join(os.path.dirname(__file__), "fb_config.json")
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {
        "access_token": os.environ.get("FB_ACCESS_TOKEN", ""),
        "page_id": os.environ.get("FB_PAGE_ID", ""),
    }


def api(method, endpoint, **kwargs):
    cfg = get_config()
    url = f"{GRAPH_API}/{endpoint}"
    params = kwargs.pop("params", {})
    params["access_token"] = cfg["access_token"]
    resp = getattr(requests, method)(url, params=params, **kwargs)
    data = resp.json()
    if "error" in data:
        print(f"❌ API Error: {data['error']['message']}")
        sys.exit(1)
    return data


# ── Post Types ───────────────────────────────────────────────────────────────

def post_text(page_id, message, scheduled_time=None):
    """Đăng bài text thuần"""
    payload = {"message": message}
    if scheduled_time:
        payload["scheduled_publish_time"] = scheduled_time
        payload["published"] = "false"
    result = api("post", f"{page_id}/feed", data=payload)
    return result


def post_photo(page_id, message, image_paths, scheduled_time=None):
    """Đăng 1 ảnh hoặc carousel nhiều ảnh"""
    cfg = get_config()

    if len(image_paths) == 1:
        # Single photo post
        with open(image_paths[0], "rb") as f:
            payload = {"caption": message}
            if scheduled_time:
                payload["scheduled_publish_time"] = scheduled_time
                payload["published"] = "false"
            result = api("post", f"{page_id}/photos",
                         data=payload, files={"source": f})
        return result
    else:
        # Carousel: upload each photo unpublished then combine
        photo_ids = []
        for path in image_paths:
            with open(path, "rb") as f:
                r = api("post", f"{page_id}/photos",
                        data={"published": "false"},
                        files={"source": f})
                photo_ids.append(r["id"])
                print(f"  ✅ Uploaded {path} → {r['id']}")

        attached = [{"media_fbid": pid} for pid in photo_ids]
        payload = {
            "message": message,
            "attached_media": json.dumps(attached),
        }
        if scheduled_time:
            payload["scheduled_publish_time"] = scheduled_time
            payload["published"] = "false"
        result = api("post", f"{page_id}/feed", data=payload)
        return result


def post_video(page_id, message, video_path, scheduled_time=None, is_reel=False):
    """Upload và đăng video / Reels"""
    cfg = get_config()
    endpoint = f"{page_id}/videos"

    with open(video_path, "rb") as f:
        payload = {
            "description": message,
        }
        if is_reel:
            payload["video_type"] = "REELS"
        if scheduled_time:
            payload["scheduled_publish_time"] = scheduled_time
            payload["published"] = "false"
        result = api("post", endpoint, data=payload, files={"source": f})
    return result


def post_story_photo(page_id, image_path):
    """Đăng Story ảnh"""
    with open(image_path, "rb") as f:
        result = api("post", f"{page_id}/photo_stories",
                     files={"source": f})
    return result


def post_story_video(page_id, video_path):
    """Đăng Story video"""
    with open(video_path, "rb") as f:
        result = api("post", f"{page_id}/video_stories",
                     data={"upload_phase": "single"},
                     files={"source": f})
    return result


# ── Schedule Management ───────────────────────────────────────────────────────

def list_scheduled(page_id):
    """Xem danh sách bài hẹn giờ"""
    result = api("get", f"{page_id}/scheduled_posts",
                 params={"fields": "id,message,scheduled_publish_time,story"})
    posts = result.get("data", [])
    if not posts:
        print("📭 Không có bài hẹn giờ nào.")
        return
    print(f"\n📅 Có {len(posts)} bài hẹn giờ:\n")
    for p in posts:
        ts = p.get("scheduled_publish_time", "N/A")
        if isinstance(ts, int):
            ts = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
        msg = (p.get("message") or p.get("story") or "")[:80]
        print(f"  ID: {p['id']}")
        print(f"  ⏰ {ts}")
        print(f"  💬 {msg}")
        print()


def delete_post(post_id):
    """Xóa bài (kể cả scheduled)"""
    result = api("delete", post_id)
    return result


def reschedule_post(post_id, new_timestamp):
    """Đổi giờ đăng bài đã hẹn"""
    result = api("post", post_id,
                 data={"scheduled_publish_time": new_timestamp,
                       "published": "false"})
    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

def parse_schedule(s):
    """Parse '2024-12-25 10:00' → Unix timestamp"""
    dt = datetime.strptime(s, "%Y-%m-%d %H:%M")
    return int(dt.timestamp())


def main():
    parser = argparse.ArgumentParser(
        description="Facebook Page Manager CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Đăng text
  python fb_post.py text --message "Hello World!"

  # Đăng ảnh + caption
  python fb_post.py photo --message "Caption đây" --images photo.jpg

  # Carousel (nhiều ảnh)
  python fb_post.py photo --message "Caption" --images a.jpg b.jpg c.jpg

  # Video/Reels
  python fb_post.py video --message "Caption" --video clip.mp4 --reel

  # Story ảnh
  python fb_post.py story --type photo --media story.jpg

  # Story video
  python fb_post.py story --type video --media story.mp4

  # Hẹn giờ đăng
  python fb_post.py text --message "Bài hẹn giờ" --schedule "2024-12-25 08:00"

  # Xem danh sách scheduled
  python fb_post.py list-scheduled

  # Xóa bài
  python fb_post.py delete --post-id 123456789

  # Đổi giờ đăng
  python fb_post.py reschedule --post-id 123456789 --schedule "2024-12-26 09:00"
        """
    )

    sub = parser.add_subparsers(dest="cmd")

    # text
    p_text = sub.add_parser("text", help="Đăng bài text")
    p_text.add_argument("--message", required=True)
    p_text.add_argument("--schedule", help="Hẹn giờ: 'YYYY-MM-DD HH:MM'")

    # photo / carousel
    p_photo = sub.add_parser("photo", help="Đăng ảnh / carousel")
    p_photo.add_argument("--message", required=True)
    p_photo.add_argument("--images", nargs="+", required=True)
    p_photo.add_argument("--schedule", help="Hẹn giờ: 'YYYY-MM-DD HH:MM'")

    # video
    p_video = sub.add_parser("video", help="Đăng video / Reels")
    p_video.add_argument("--message", required=True)
    p_video.add_argument("--video", required=True)
    p_video.add_argument("--reel", action="store_true", help="Upload dạng Reels")
    p_video.add_argument("--schedule", help="Hẹn giờ: 'YYYY-MM-DD HH:MM'")

    # story
    p_story = sub.add_parser("story", help="Đăng Story ảnh hoặc video")
    p_story.add_argument("--type", choices=["photo", "video"], required=True)
    p_story.add_argument("--media", required=True, help="Đường dẫn file")

    # list-scheduled
    sub.add_parser("list-scheduled", help="Xem danh sách bài hẹn giờ")

    # delete
    p_del = sub.add_parser("delete", help="Xóa bài")
    p_del.add_argument("--post-id", required=True)

    # reschedule
    p_re = sub.add_parser("reschedule", help="Đổi giờ đăng")
    p_re.add_argument("--post-id", required=True)
    p_re.add_argument("--schedule", required=True, help="'YYYY-MM-DD HH:MM'")

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        sys.exit(0)

    cfg = get_config()
    page_id = cfg.get("page_id", "")
    if not cfg.get("access_token"):
        print("❌ Chưa có Access Token! Xem references/get-token.md để lấy token.")
        sys.exit(1)

    # ── Dispatch ──────────────────────────────────────────────────────────────

    if args.cmd == "text":
        ts = parse_schedule(args.schedule) if args.schedule else None
        result = post_text(page_id, args.message, ts)
        label = "Bài hẹn giờ" if ts else "Bài đã đăng"
        print(f"✅ {label}! ID: {result.get('id')}")

    elif args.cmd == "photo":
        ts = parse_schedule(args.schedule) if args.schedule else None
        result = post_photo(page_id, args.message, args.images, ts)
        label = "Carousel hẹn giờ" if len(args.images) > 1 else "Ảnh đã đăng"
        if ts:
            label += " (scheduled)"
        print(f"✅ {label}! ID: {result.get('id') or result.get('post_id')}")

    elif args.cmd == "video":
        ts = parse_schedule(args.schedule) if args.schedule else None
        result = post_video(page_id, args.message, args.video, ts, args.reel)
        label = "Reels" if args.reel else "Video"
        print(f"✅ {label} đã upload! ID: {result.get('id')}")

    elif args.cmd == "story":
        if args.type == "photo":
            result = post_story_photo(page_id, args.media)
        else:
            result = post_story_video(page_id, args.media)
        print(f"✅ Story đã đăng! ID: {result.get('id')}")

    elif args.cmd == "list-scheduled":
        list_scheduled(page_id)

    elif args.cmd == "delete":
        result = delete_post(args.post_id)
        print(f"✅ Đã xóa bài {args.post_id}: {result}")

    elif args.cmd == "reschedule":
        ts = parse_schedule(args.schedule)
        result = reschedule_post(args.post_id, ts)
        print(f"✅ Đã đổi lịch bài {args.post_id}!")


if __name__ == "__main__":
    main()
