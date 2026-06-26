#!/usr/bin/env python3
"""
OWS 媒体文件处理
支持图片和视频的上传、验证、压缩
"""

import os
import sys
import json
import pathlib
from datetime import datetime

STATE_DIR = pathlib.Path(__file__).resolve().parent.parent / "state"
MEDIA_DIR = STATE_DIR / "media"
IMAGES_DIR = MEDIA_DIR / "images"
VIDEOS_DIR = MEDIA_DIR / "videos"

# 配置
MAX_IMAGES = 3
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_VIDEO_DURATION = 30  # 30秒
ALLOWED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.webp']
ALLOWED_VIDEO_FORMATS = ['.mp4', '.mov', '.webm']

def init_media_dirs():
    """初始化媒体目录"""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

def validate_image(image_path):
    """验证图片"""
    path = pathlib.Path(image_path)
    
    # 检查格式
    if path.suffix.lower() not in ALLOWED_IMAGE_FORMATS:
        return False, f"不支持的图片格式: {path.suffix}"
    
    # 检查大小
    size = path.stat().st_size
    if size > MAX_IMAGE_SIZE:
        return False, f"图片大小超过限制: {size/1024/1024:.1f}MB > 5MB"
    
    return True, "OK"

def validate_video(video_path):
    """验证视频"""
    path = pathlib.Path(video_path)
    
    # 检查格式
    if path.suffix.lower() not in ALLOWED_VIDEO_FORMATS:
        return False, f"不支持的视频格式: {path.suffix}"
    
    # 检查大小
    size = path.stat().st_size
    if size > MAX_VIDEO_SIZE:
        return False, f"视频大小超过限制: {size/1024/1024:.1f}MB > 50MB"
    
    # 检查时长（需要 ffprobe）
    try:
        import subprocess
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
             '-of', 'default=noprint_wrappers=1:nokey=1', str(video_path)],
            capture_output=True, text=True, timeout=10
        )
        duration = float(result.stdout.strip())
        if duration > MAX_VIDEO_DURATION:
            return False, f"视频时长超过限制: {duration:.1f}秒 > 30秒"
    except Exception as e:
        # 如果 ffprobe 不可用，跳过时长检查
        pass
    
    return True, "OK"

def save_bid_media(bid_id, images=None, video=None):
    """保存投标媒体文件"""
    init_media_dirs()
    
    result = {
        "bid_id": bid_id,
        "images": [],
        "video": None,
        "errors": []
    }
    
    # 处理图片
    if images:
        if len(images) > MAX_IMAGES:
            result["errors"].append(f"图片数量超过限制: {len(images)} > {MAX_IMAGES}")
            images = images[:MAX_IMAGES]
        
        bid_image_dir = IMAGES_DIR / bid_id
        bid_image_dir.mkdir(parents=True, exist_ok=True)
        
        for i, img_path in enumerate(images, 1):
            valid, msg = validate_image(img_path)
            if valid:
                ext = pathlib.Path(img_path).suffix
                dest = bid_image_dir / f"image_{i}{ext}"
                # 复制文件（实际应用中可能使用对象存储）
                import shutil
                shutil.copy2(img_path, dest)
                result["images"].append(str(dest))
            else:
                result["errors"].append(f"图片{i}: {msg}")
    
    # 处理视频
    if video:
        valid, msg = validate_video(video)
        if valid:
            bid_video_dir = VIDEOS_DIR / bid_id
            bid_video_dir.mkdir(parents=True, exist_ok=True)
            ext = pathlib.Path(video).suffix
            dest = bid_video_dir / f"video{ext}"
            import shutil
            shutil.copy2(video, dest)
            result["video"] = str(dest)
        else:
            result["errors"].append(f"视频: {msg}")
    
    return result

def get_media_score(bid_id):
    """计算媒体展示得分"""
    score = {
        "images_score": 0,
        "video_score": 0,
        "total_media_score": 0,
        "max_images_score": 10,
        "max_video_score": 10
    }
    
    # 计算图片得分
    bid_image_dir = IMAGES_DIR / bid_id
    if bid_image_dir.exists():
        image_count = len(list(bid_image_dir.glob("*")))
        # 每张图片 3.33 分，最多 10 分
        score["images_score"] = min(image_count * 3.33, 10)
    
    # 计算视频得分
    bid_video_dir = VIDEOS_DIR / bid_id
    if bid_video_dir.exists():
        videos = list(bid_video_dir.glob("*"))
        if videos:
            score["video_score"] = 10
    
    score["total_media_score"] = score["images_score"] + score["video_score"]
    
    return score

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="OWS 媒体文件处理")
    parser.add_argument("action", choices=["save", "score", "validate"])
    parser.add_argument("--bid-id", required=True, help="投标ID")
    parser.add_argument("--images", nargs="*", help="图片文件路径")
    parser.add_argument("--video", help="视频文件路径")
    
    args = parser.parse_args()
    
    if args.action == "save":
        result = save_bid_media(args.bid_id, args.images, args.video)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif args.action == "score":
        score = get_media_score(args.bid_id)
        print(json.dumps(score, indent=2, ensure_ascii=False))
    
    elif args.action == "validate":
        errors = []
        if args.images:
            for img in args.images:
                valid, msg = validate_image(img)
                if not valid:
                    errors.append(f"{img}: {msg}")
        if args.video:
            valid, msg = validate_video(args.video)
            if not valid:
                errors.append(f"{args.video}: {msg}")
        
        if errors:
            print("❌ 验证失败:")
            for e in errors:
                print(f"  - {e}")
        else:
            print("✅ 媒体文件验证通过")

if __name__ == "__main__":
    main()