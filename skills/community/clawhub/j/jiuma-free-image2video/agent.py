#!/usr/bin/env python3
"""
九马AI图生视频工具
输入提示词和图片，生成视频并返回URL
"""
import argparse
import os.path
from pathlib import Path
from utils import get_jiuma_api_key, jiuma_request, output_result

SUBMIT_API = "https://api.jiuma.com/api/imageVideo/add"
CHECK_STATUS_API = "https://api.jiuma.com/api/imageVideo/status"

MIME_MAP = {
    # 图片
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.jpe': 'image/jpeg',
    '.jfif': 'image/jpeg',
    '.pjpeg': 'image/jpeg',
    '.pjp': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
    '.svgz': 'image/svg+xml',
    '.ico': 'image/x-icon',
    '.tiff': 'image/tiff',
    '.tif': 'image/tiff',
    '.heic': 'image/heic',
    '.heif': 'image/heif',
    '.avif': 'image/avif',
    '.apng': 'image/apng',
}

headers = {
    "X-Secret-Key": get_jiuma_api_key()
}


def get_image_param(image_str, image_pos='first', request_data=None, image_files=None):
    if not image_str:
        return request_data, image_files
    ext = Path(image_str).suffix.lower()
    if ext not in MIME_MAP:
        return request_data, image_files
    if (image_str.startswith(('http://', 'https://', 'ftp://', '//')) or
            '://' in image_str or
            image_str.startswith('www.')):
        request_data[f"{image_pos}_image_url"] = image_str
    elif os.path.exists(image_str):
        print(f"content_type: {MIME_MAP[ext]}")
        f = open(image_str, 'rb')
        image_files[f"{image_pos}_image_file"] = (os.path.basename(image_str), f, MIME_MAP[ext])


    return request_data, image_files


def submit_image2video(text, first_image, end_image, width, height):
    """
    返回结构
    status: 状态
    message: 返回消息
    data: 数据结构体
    task_id: 任务ID(根据此任务ID查询制作进度)
    示例
    {
      "status": "success",
      "message": "图生视频任务提交成功",
      "data": {
        "task_id": "202603263844232132"
      }
    }
    """
    if not text:
        output_result({
            "status": "error",
            "message": "请输入需要生成的视频的描述",
            "data": {}
        })
        return

    if not first_image:
        output_result({
            "status": "error",
            "message": "请输入生成的视频的首帧图片",
            "data": {}
        })
        return

    if width > 832 or height > 832:
        output_result({
            "status": "error",
            "message": "输出图片最大尺寸限制在832以内",
            "data": {}
        })
        return

    # 1. 提交生成请求
    request_data = {
        "tips": text,
        "width": width,
        "height": height
    }
    image_files = {}
    # 获取首帧
    request_data, image_files = get_image_param(first_image, 'first', request_data, image_files)
    # 获取尾帧
    request_data, image_files = get_image_param(end_image, 'end', request_data, image_files)
    data, message = jiuma_request(SUBMIT_API, data=request_data, headers=headers, files=image_files)
    if not data:
        return
    task_id = data.get("task_id")

    if not task_id:
        output_result({
            "status": "error",
            "message": "API未返回任务ID",
            "data": data
        })
        return

    output_result({
        "status": "success",
        "message": "图生视频任务提交成功",
        "data": {
            "task_id": task_id,
            "width": width,
            "height": height,
            "text": text,
            "first_image": first_image,
            "end_image": end_image
        }
    })
    return


def check_task_status(task_id):
    """
    返回结构
    status: 处理结果，success|pending|running|failed
    message: 返回消息
    data: 数据结构体
    task_id: 任务ID
    video_url: 视频链接(如status为success)
    示例
    {
      "status": "success",
      "message": "视频生成成功",
      "data": {
        "video_url": "https://cache.jiuma.com/static/uploads/20260326/69c4cc0c043e1.mp4",
        "task_id": "20260326486039011"
      }
    }
    """
    if not task_id:
        output_result({
            "status": "error",
            "message": "任务ID不能为空",
            "data": {}
        })
        return None

    data, message = jiuma_request(CHECK_STATUS_API, data={"task_id": task_id}, headers=headers)
    if not data:
        return
    task_status = data.get("task_status", "").upper()

    if task_status == 'SUCCEEDED':
        video_url = data.get('video_url')
        if not video_url:
            output_result({
                "status": "error",
                "message": "API未返回图片URL",
                "data": data
            })
            return None

        output_result({
            "status": "success",
            "message": "视频生成成功",
            "data": {
                "video_url": video_url,
                "task_id": task_id,
                "download_link": video_url
            }
        })
    elif task_status == 'PENDING':
        output_result({
            "status": "pending",
            "message": "图生视频任务排队中，请耐心等待",
            "data": {
                "task_id": task_id,
                "status": "pending"
            }
        })
    elif task_status == 'RUNNING':
        output_result({
            "status": "pending",
            "message": "图生视频任务执行中，请耐心等待",
            "data": {
                "task_id": task_id,
                "status": "running"
            }
        })
    else:
        output_result({
            "status": "failed",
            "message": f"视频生成失败: {message}",
            "data": {
                "task_id": task_id,
                "status": "failed"
            }
        })


def main():
    parser = argparse.ArgumentParser(description="九马AI免费图生视频工具",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    # 主要参数组
    parser.add_argument('--text', type=str, default="", help="图生视频提示词，对视频的描述")
    parser.add_argument('--first_image', type=str, default='', help="首帧图片")
    parser.add_argument('--end_image', type=str, default='', help="尾帧图片")
    parser.add_argument('--width', type=int, default=832, help="输出视频的宽，最大832")
    parser.add_argument('--height', type=int, default=480, help="输出视频的高，最大832")
    parser.add_argument('--task_id', type=str, default='', help="图生视频执行任务ID")

    # 操作参数
    parser.add_argument('--check', action='store_true', help="检查生成状态")
    parser.add_argument('--submit', action='store_true', help="提交图生视频制作")

    args = parser.parse_args()

    if args.submit:
        submit_image2video(args.text, args.first_image, args.end_image, args.width, args.height)
    elif args.check:
        check_task_status(args.task_id)
    else:
        print("""
九马AI免费图生视频工具 v1.0
==========================

使用方法:
1. 提交视频生成任务:
   python3 agent.py --submit --text "图片描述" --first_image /data/test.png --end_image https://example.com/test.png --width 832 --height 480

2. 查询任务状态:
   python3 agent.py --check --task_id "任务ID"

参数说明:
--submit        提交视频生成任务
--text          视频的描述文本（必需）
--first_image   视频的首帧图片,可以是本地图片或远程链接（必选）
--end_image     视频的尾帧图片,可以是本地图片或远程链接
--width         视频宽度（可选，默认832，最大832）
--height        视频高度（可选，默认480，最大832）
--check         查询任务生成状态
--task_id       任务ID（与--check一起使用）

示例:
首帧
python3 agent.py --submit --text "一只可爱的小猫在草地上玩耍" --first_image /data/first_image.png --width 832 --height 480
首尾帧
python3 agent.py --submit --text "一只可爱的小猫在草地上玩耍" --first_image /data/first_image.png --end_image https://exmaple.com/end_frame_image.png --width 832 --height 480
python3 agent.py --check --task_id "202603263844232132"

注意:
- 最大视频尺寸为832x832
- 图片生成可能需要等待，请使用--check参数查询状态
- 生成的图片URL可以直接在浏览器中打开下载
        """.strip())


if __name__ == '__main__':
    main()
