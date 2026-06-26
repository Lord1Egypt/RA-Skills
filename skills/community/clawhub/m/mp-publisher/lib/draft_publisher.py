#!/usr/bin/env python3
"""
微信公众号草稿发布脚本
======================
将文章发布到公众号草稿箱

用法:
    python draft_publisher.py <article_file> <image_dir>
    python draft_publisher.py --test

环境变量:
    WECHAT_APP_ID - 公众号AppID（必需）
    WECHAT_APP_SECRET - 公众号AppSecret（必需）
"""

import os
import sys
import re
import requests
import base64
import time
from pathlib import Path

# ============================================================================
# 配置
# ============================================================================

APP_ID = os.environ.get("WECHAT_APP_ID", "")
APP_SECRET = os.environ.get("WECHAT_APP_SECRET", "")

ACCESS_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"
UPLOAD_IMAGE_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"
CREATE_DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"

# ============================================================================
# 微信API封装
# ============================================================================

class WeChatAPI:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None
        self.token_expire_time = 0
    
    def get_access_token(self) -> str:
        """获取access_token"""
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token
        
        url = f"{ACCESS_TOKEN_URL}?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        
        response = requests.get(url, timeout=30)
        result = response.json()
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            self.token_expire_time = time.time() + result.get("expires_in", 7200) - 300
            return self.access_token
        else:
            raise Exception(f"获取access_token失败: {result}")
    
    def upload_image(self, image_path: str) -> str:
        """上传图片，返回media_id"""
        token = self.get_access_token()
        url = f"{UPLOAD_IMAGE_URL}?access_token={token}&type=image"
        
        with open(image_path, "rb") as f:
            files = {"media": (os.path.basename(image_path), f, "image/png")}
            response = requests.post(url, files=files, timeout=60)
        
        result = response.json()
        
        if "media_id" in result:
            print(f"[OK] 上传图片: {os.path.basename(image_path)} -> {result['media_id']}")
            return result["media_id"]
        else:
            raise Exception(f"上传图片失败: {result}")
    
    def create_draft(self, articles: list) -> str:
        """创建草稿，返回media_id"""
        token = self.get_access_token()
        url = f"{CREATE_DRAFT_URL}?access_token={token}"
        
        data = {"articles": articles}
        
        response = requests.post(url, json=data, timeout=60)
        result = response.json()
        
        if "media_id" in result:
            return result["media_id"]
        else:
            raise Exception(f"创建草稿失败: {result}")


# ============================================================================
# 文章处理
# ============================================================================

def parse_article(article_path: str) -> dict:
    """解析文章文件"""
    with open(article_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 提取标题（第一个 # 开头的行）
    lines = content.strip().split("\n")
    title = ""
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break
    
    if not title:
        raise Exception("无法提取文章标题")
    
    # 移除标题行和状态标记
    body_lines = []
    for line in lines:
        if line.startswith("# "):
            continue
        if line.strip().startswith("<!-- STATUS:"):
            continue
        body_lines.append(line)
    
    body = "\n".join(body_lines).strip()
    
    return {"title": title, "content": body}


def insert_images(content: str, image_dir: str, api: WeChatAPI) -> tuple:
    """
    插入图片到文章中
    
    Returns:
        (content_with_images, thumb_media_id)
    """
    # 查找配图文件
    cover_path = None
    image_paths = []
    
    # 尝试不同的命名模式
    possible_covers = ["cover.png", "article_cover.png"]
    possible_images = ["image1.png", "image2.png", "image3.png"]
    
    for name in possible_covers:
        path = os.path.join(image_dir, name)
        if os.path.exists(path):
            cover_path = path
            break
    
    for name in possible_images:
        path = os.path.join(image_dir, name)
        if os.path.exists(path):
            image_paths.append(path)
    
    # 如果没找到标准命名，尝试其他文件
    if not cover_path:
        files = sorted(Path(image_dir).glob("*.png"))
        if files:
            cover_path = str(files[0])
            image_paths = [str(f) for f in files[1:4]]
    
    if not cover_path:
        raise Exception(f"未找到封面图片: {image_dir}")
    
    # 上传封面
    thumb_media_id = api.upload_image(cover_path)
    
    # 上传内页图片
    image_media_ids = []
    for path in image_paths:
        media_id = api.upload_image(path)
        image_media_ids.append(media_id)
    
    # 替换配图标记
    for i, media_id in enumerate(image_media_ids):
        placeholder = f"【配图{i+1}】"
        img_tag = f'<img src="https://mmbiz.qpic.cn/mmbiz_png/{media_id}/0" alt="配图{i+1}" style="width:100%;"/>'
        content = content.replace(placeholder, img_tag)
    
    # 清理未使用的配图标记
    content = re.sub(r"【配图\d】", "", content)
    
    # 转换Markdown为HTML（简化版）
    content = markdown_to_html(content)
    
    return content, thumb_media_id


def markdown_to_html(text: str) -> str:
    """简化的Markdown转HTML"""
    # 段落
    paragraphs = text.split("\n\n")
    html_parts = []
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        
        # 标题
        if p.startswith("## "):
            html_parts.append(f"<h2>{p[3:]}</h2>")
        elif p.startswith("### "):
            html_parts.append(f"<h3>{p[4:]}</h3>")
        # 列表
        elif p.startswith("- ") or p.startswith("* "):
            items = p.split("\n")
            list_items = [f"<li>{item[2:]}</li>" for item in items if item.startswith(("- ", "* "))]
            html_parts.append(f"<ul>{''.join(list_items)}</ul>")
        # 普通段落
        else:
            # 粗体
            p = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", p)
            # 斜体
            p = re.sub(r"\*(.+?)\*", r"<em>\1</em>", p)
            # 代码
            p = re.sub(r"`(.+?)`", r"<code>\1</code>", p)
            html_parts.append(f"<p>{p}</p>")
    
    return "\n".join(html_parts)


# ============================================================================
# 主函数
# ============================================================================

def create_draft(article_path: str, image_dir: str) -> str:
    """创建草稿，返回media_id"""
    
    if not APP_ID or not APP_SECRET:
        raise Exception("未配置 WECHAT_APP_ID 或 WECHAT_APP_SECRET")
    
    api = WeChatAPI(APP_ID, APP_SECRET)
    
    # 解析文章
    article = parse_article(article_path)
    print(f"[INFO] 文章标题: {article['title']}")
    
    # 插入图片
    content, thumb_media_id = insert_images(article["content"], image_dir, api)
    
    # 创建草稿
    draft_data = {
        "title": article["title"],
        "author": "",
        "digest": article["content"][:120].replace("\n", " ") + "...",
        "content": content,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 0,
        "only_fans_can_comment": 0
    }
    
    media_id = api.create_draft([draft_data])
    print(f"[SUCCESS] 草稿创建成功: {media_id}")
    
    # 更新文章状态
    with open(article_path, "a", encoding="utf-8") as f:
        f.write(f"\n\n<!-- STATUS: 已入草稿箱 -->\n")
    
    return media_id


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    
    if sys.argv[1] == "--test":
        # 测试API连接
        if not APP_ID or not APP_SECRET:
            print("[ERROR] 未配置环境变量")
            return 1
        
        try:
            api = WeChatAPI(APP_ID, APP_SECRET)
            token = api.get_access_token()
            print(f"[OK] API连接成功, token: {token[:20]}...")
            return 0
        except Exception as e:
            print(f"[ERROR] {e}")
            return 1
    
    if len(sys.argv) < 3:
        print("用法: python draft_publisher.py <article_file> <image_dir>")
        return 1
    
    article_path = sys.argv[1]
    image_dir = sys.argv[2]
    
    try:
        media_id = create_draft(article_path, image_dir)
        print(f"\n[完成] 草稿 media_id: {media_id}")
        return 0
    except Exception as e:
        print(f"[ERROR] {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
