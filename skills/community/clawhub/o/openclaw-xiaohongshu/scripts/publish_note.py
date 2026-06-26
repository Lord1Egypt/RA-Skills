#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书笔记发布脚本

功能：发布图文笔记、视频笔记
参数：
  -i, --images: 图片路径列表
  -t, --title: 笔记标题 (最多 20 字)
  -c, --content: 正文内容 (最多 2000 字)
  -e, --tags: 标签列表
  -v, --category: 分类 (可选)
  -p, --publish: 是否立即发布 (默认保存为草稿)
"""

import os
import json
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 常量定义
MAX_TITLE_LENGTH = 20
MAX_CONTENT_LENGTH = 2000
MAX_IMAGES = 9
MIN_IMAGES = 1
MAX_FILE_SIZE_MB = 10  # 10MB


class XiaohongshuNote:
    """小红书笔记模型"""
    
    def __init__(
        self,
        title: str,
        content: str,
        images: Optional[List[str]] = None,
        video: Optional[str] = None,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        is_publish: bool = False
    ):
        self.title = title
        self.content = content
        self.images = images or []
        self.video = video
        self.tags = tags or []
        self.category = category
        self.is_publish = is_publish
    
    def validate(self) -> bool:
        """验证笔记数据"""
        errors = []
        
        # 标题验证
        if not self.title:
            errors.append("标题不能为空")
        elif len(self.title) > MAX_TITLE_LENGTH:
            errors.append(f"标题长度不能超过 {MAX_TITLE_LENGTH} 字，当前 {len(self.title)} 字")
        
        # 内容验证
        if not self.content:
            errors.append("正文内容不能为空")
        elif len(self.content) > MAX_CONTENT_LENGTH:
            errors.append(f"内容长度不能超过 {MAX_CONTENT_LENGTH} 字，当前 {len(self.content)} 字")
        
        # 图片验证
        if self.images:
            if len(self.images) > MAX_IMAGES or len(self.images) < MIN_IMAGES:
                errors.append(f"图片数量必须在 {MIN_IMAGES}-{MAX_IMAGES} 张之间")
            
            for img_path in self.images:
                if not os.path.exists(img_path):
                    errors.append(f"图片不存在：{img_path}")
                else:
                    file_size_mb = os.path.getsize(img_path) / (1024 * 1024)
                    if file_size_mb > MAX_FILE_SIZE_MB:
                        errors.append(f"图片过大 ({file_size_mb:.2f}MB)，最大 {MAX_FILE_SIZE_MB}MB: {img_path}")
        
        # 视频验证
        elif self.video:
            if not os.path.exists(self.video):
                errors.append(f"视频文件不存在：{self.video}")
            else:
                file_size_mb = os.path.getsize(self.video) / (1024 * 1024)
                if file_size_mb > MAX_FILE_SIZE_MB:
                    errors.append(f"视频过大 ({file_size_mb:.2f}MB)，最大 {MAX_FILE_SIZE_MB}MB: {self.video}")
        
        # 至少要有图片或视频
        if not self.images and not self.video:
            errors.append("至少需要提供图片或视频之一")
        
        if errors:
            for err in errors:
                logger.error(f"验证失败：{err}")
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        data = {
            "title": self.title,
            "content": self.content,
            "is_draft": not self.is_publish,
        }
        
        if self.images:
            data["images"] = self.images
        
        if self.video:
            data["video"] = self.video
        
        if self.tags:
            data["tags"] = self.tags
        
        if self.category:
            data["category"] = self.category
        
        return data
    
    def to_json(self) -> str:
        """转换为 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


def upload_images(image_paths: List[str]) -> List[str]:
    """上传图片到小红书服务器（模拟）
    
    实际的图片上传需要通过小红书 API，这里需要实现:
    1. 请求小红书图片上传接口
    2. 获取 CDN URL 列表
    3. 返回图片 URL 列表
    """
    logger.info(f"开始上传 {len(image_paths)} 张图片")
    
    # 这里应该调用小红书 API 上传图片
    # 由于模拟演示，我们返回虚拟 URL
    uploaded_urls = []
    
    for img_path in image_paths:
        if os.path.exists(img_path):
            # 实际场景：调用小红书 API upload_image(img_path)
            # 返回 CDN_URL
            logger.info(f"✓ 上传成功：{os.path.basename(img_path)}")
            # uploaded_urls.append(CDN_URL)
            uploaded_urls.append(
                f"https://xiaohongshu-cdn.com/image/{os.path.basename(img_path)}"
            )
        
        # CDN_URL
    
    return uploaded_urls


def upload_video(video_path: str) -> str:
    """上传视频到小红书服务器（模拟）
    
    实际实现：
    1. 分片上传视频
    2. 等待转码完成
    3. 返回视频 URL
    """
    logger.info(f"开始上传视频：{os.path.basename(video_path)}")
    
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"视频文件不存在：{video_path}")
    
    # 实际场景：调用小红书 API upload_video(video_path)
    # 返回 CDN_URL
    video_url = f"https://xiaohongshu-cdn.com/video/{os.path.basename(video_path)}"
    logger.info(f"✓ 上传成功：{os.path.basename(video_path)}")
    
    return video_url


def create_note(note_data: Dict[str, Any]) -> str:
    """创建小红书笔记（模拟）
    
    实际实现：
    1. 请求小红书笔记创建 API
    2. 返回笔记 ID
    3. 如果 is_publish=False，则为草稿;
       如果 is_publish=True，则发布笔记
    """
    logger.info("创建小红书笔记...")
    
    # 实际场景：调用小红书 API create_note(note_data)
    # 返回 note_id
    import random
    note_id = f"note_{random.randint(1000, 9999)}"
    
    if note_data.get('is_draft', True):
        logger.info(f"✓ 笔记已保存为草稿，ID: {note_id}")
    else:
        logger.info(f"✓ 笔记已发布，ID: {note_id}")
    
    return note_id


def publish_note(
    title: str,
    content: str,
    images: Optional[List[str]] = None,
    video: Optional[str] = None,
    tags: Optional[List[str]] = None,
    category: Optional[str] = None,
    is_publish: bool = False
) -> Dict[str, Any]:
    """发布笔记的主函数
    
    参数：
        title: 标题
        content: 正文内容
        images: 图片路径列表
        video: 视频路径
        tags: 标签列表
        category: 分类
        is_publish: 是否立即发布
    
    返回:
        笔记 ID 和状态
    """
    # 创建笔记对象
    note = XiaohongshuNote(
        title=title,
        content=content,
        images=images,
        video=video,
        tags=tags,
        category=category,
        is_publish=is_publish
    )
    
    # 验证
    if not note.validate():
        return {
            "success": False,
            "message": "笔记验证失败"
        }
    
    # 准备数据
    if images:
        uploaded_urls = upload_images(images)
    else:
        uploaded_urls = None
    
    if video:
        video_url = upload_video(video)
    else:
        video_url = None
    
    # 构建笔记数据
    note_data = note.to_dict()
    if uploaded_urls:
        note_data["images"] = uploaded_urls
    if video_url:
        note_data["video"] = video_url
    
    # 创建笔记
    note_id = create_note(note_data)
    
    return {
        "success": True,
        "note_id": note_id,
        "is_draft": not is_publish,
        "message": "笔记发布成功"
    }


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="发布小红书图文或视频笔记"
    )
    
    parser.add_argument(
        "-i", "--images",
        nargs="+",
        help="图片路径列表 (1-9 张)"
    )
    
    parser.add_argument(
        "-v", "--video",
        help="视频文件路径"
    )
    
    parser.add_argument(
        "-t", "--title",
        required=True,
        help="笔记标题 (最多 20 字)"
    )
    
    parser.add_argument(
        "-c", "--content",
        required=True,
        help="正文内容 (最多 2000 字)"
    )
    
    parser.add_argument(
        "-e", "--tags",
        nargs="+",
        help="标签列表"
    )
    
    parser.add_argument(
        "-a", "--category",
        help="分类 (可选)"
    )
    
    parser.add_argument(
        "-p", "--publish",
        action="store_true",
        help="立即发布 (默认保存为草稿)"
    )
    
    args = parser.parse_args()
    
    # 调用发布函数
    result = publish_note(
        title=args.title,
        content=args.content,
        images=args.images,
        video=args.video,
        tags=args.tags,
        category=args.category,
        is_publish=args.publish
    )
    
    # 输出结果
    if result["success"]:
        print(f"\n{'='*50}")
        print(f"✓ 笔记发布成功!")
        print(f"  ID: {result['note_id']}")
        print(f"  状态：{ '发布' if not result['is_draft'] else '草稿'}")
        print(f"{'='*50}")
    else:
        print(f"\n{'='*50}")
        print(f"✗ 发布失败:")
        print(f"  {result['message']}")
        print(f"{'='*50}")
        exit(1)


if __name__ == "__main__":
    main()
