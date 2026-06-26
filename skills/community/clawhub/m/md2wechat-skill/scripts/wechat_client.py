"""
微信公众号 API 客户端（独立精简版）

提供封面图上传、正文图片上传、创建草稿三个核心能力。
此版本已从原项目解耦，不依赖 src.core.settings 等内部模块。
"""

import os
import io
import time
import tempfile
import hashlib
import logging
import re
from pathlib import Path
from typing import Dict, Optional

from wechatpy import WeChatClient
from wechatpy.exceptions import WeChatClientException

logger = logging.getLogger("md2wechat")


class WeChatSkillClient:
    """精简的微信公众号客户端，专注于草稿箱发布流程"""

    def __init__(self, appid: str, secret: str):
        """
        Args:
            appid: 微信公众号 AppID
            secret: 微信公众号 AppSecret
        """
        if not appid or not secret:
            raise ValueError("微信公众号 AppID 和 Secret 必须设置")

        self.appid = appid
        self.secret = secret
        self.client = WeChatClient(appid, secret)
        self.token_cache = {
            'token': None,
            'expires_at': 0
        }

    def _ensure_token(self):
        """确保 access_token 有效"""
        now = time.time()
        if not self.token_cache['token'] or now >= self.token_cache['expires_at'] - 300:
            try:
                self.client.fetch_access_token()
                self.token_cache['token'] = self.client.access_token
                self.token_cache['expires_at'] = now + 7200
                logger.info("✅ access_token 刷新成功")
            except WeChatClientException as e:
                logger.error(f"❌ 获取 access_token 失败：{e}")
                if e.errcode == 40164:
                    ip_match = re.search(r'invalid ip ([\d\.]+)', e.errmsg)
                    ip_str = ip_match.group(1) if ip_match else "您的公网IP"
                    raise Exception(
                        f"安全拦截：当前服务器公网 IP ({ip_str}) 未加入公众号白名单。\n"
                        f"👉 请登录微信公众平台 →【开发】→【基本配置】→【IP白名单】中添加此 IP 后重试。"
                    )
                raise e

    def upload_image(self, image_path: str) -> Optional[str]:
        """
        上传图片到微信服务器（永久素材），用于封面图

        Returns:
            media_id 或 None
        """
        self._ensure_token()

        if not os.path.exists(image_path):
            logger.warning(f"⚠️ 图片文件不存在：{image_path}")
            return None

        logger.info(f"🚀 正在上传封面素材: {os.path.basename(image_path)} ...")
        try:
            with open(image_path, 'rb') as f:
                result = self.client.material.add('image', f)
                media_id = result['media_id']
                logger.info(f"✅ 封面素材上传成功，media_id: {media_id}")
                return media_id
        except WeChatClientException as e:
            logger.error(f"❌ 上传图片失败：{e}")
            return None

    def upload_content_image(self, image_path: str) -> Optional[str]:
        """
        上传图文正文内嵌图片，返回微信图片 URL

        此接口上传的图片不占用素材库数量限制。

        Returns:
            微信图片 URL 或 None
        """
        self._ensure_token()

        if not os.path.exists(image_path):
            print(f"图片文件不存在：{image_path}")
            return None

        try:
            import requests
            url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={self.client.access_token}"
            with open(image_path, 'rb') as f:
                files = {'media': f}
                resp = requests.post(url, files=files)
                result = resp.json()

            if 'url' in result:
                img_url = result['url']
                logger.info(f"✅ 正文图片上传成功: {os.path.basename(image_path)}")
                return img_url
            else:
                logger.error(f"❌ 正文图片上传失败: {result}")
                return None
        except Exception as e:
            logger.error(f"❌ 正文图片上传异常：{e}")
            return None

    def create_draft(self, article: Dict, cover_media_id: str = None) -> Optional[str]:
        """
        创建微信草稿

        Args:
            article: 文章字典，需包含 title 和 content 字段
            cover_media_id: 封面图的 media_id（可选，若不传则自动生成默认封面）

        Returns:
            草稿 media_id 或 None
        """
        self._ensure_token()

        # 如果没有封面图，自动生成并上传默认封面
        if not cover_media_id:
            print("🖼️  未指定封面图，自动生成默认封面...")
            default_cover_path = self._generate_default_cover()
            if default_cover_path:
                cover_media_id = self.upload_image(default_cover_path)
                # 清理临时文件
                try:
                    os.remove(default_cover_path)
                except Exception:
                    pass

            if not cover_media_id:
                print("⚠️  默认封面上传失败，草稿可能创建失败")

        # 构建文章数据
        import re
        
        # 标题：支持 emoji，最大 64 字符
        title = article['title']
        # 移除微信可能不兼容的特殊字符（保留 emoji 和中文）
        title = re.sub(r'[\x00-\x1f\x7f]', '', title)  # 移除控制字符
        if len(title) > 64:
            title = title[:64]
        
        # author 最长 8 字节（中文算 3 字节），安全起见限制 4 个中文字符
        author = (article.get('author', '') or '')[:4]
        
        # 摘要：支持 emoji，最大 120 字符
        digest = self._generate_digest(article.get('content', ''), max_length=120)
        # 移除 HTML 标签和控制字符，保留 emoji 和中文
        digest = re.sub(r'<[^>]+>', '', digest)
        digest = re.sub(r'[\n\r\t\x00-\x1f\x7f]', ' ', digest)
        digest = digest.strip()
        if len(digest) > 120:
            digest = digest[:120]

        articles = [{
            'title': title,
            'author': author,
            'digest': digest,
            'content': article['content'],
            'content_source_url': article.get('original_link', ''),
            'thumb_media_id': cover_media_id or '',
            'need_open_comment': 1,
            'only_fans_can_comment': 0,
            'show_cover_pic': 1 if cover_media_id else 0
        }]
        
        print(f"[DEBUG] 提交标题：{title} (长度:{len(title)})")
        print(f"[DEBUG] 提交作者：{author}")
        print(f"[DEBUG] 提交摘要：{digest} (长度:{len(digest)})")

        try:
            # wechatpy 不直接支持 draft API，使用原始 HTTP 调用
            import requests
            import json
            url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.client.access_token}"
            payload = {
                'articles': articles
            }
            # 显式使用 UTF-8 编码发送 JSON
            resp = requests.post(
                url, 
                data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                headers={'Content-Type': 'application/json; charset=utf-8'}
            )
            result = resp.json()
            
            if 'media_id' in result:
                media_id = result['media_id']
                print(f"✅ 草稿创建成功，media_id：{media_id}")
                return media_id
            else:
                print(f"❌ 创建草稿失败：{result}")
                return None
        except Exception as e:
            print(f"❌ 创建草稿异常：{e}")
            return None

    @staticmethod
    def _generate_default_cover() -> Optional[str]:
        """
        生成一张简单的默认封面图（800x450 蓝色纯色 PNG）

        Returns:
            临时文件路径或 None
        """
        try:
            from PIL import Image
            img = Image.new('RGB', (800, 450), color=(74, 144, 226))
            tmp_path = os.path.join(tempfile.gettempdir(), 'md2wechat_default_cover.png')
            img.save(tmp_path, 'PNG')
            print(f"✅ 默认封面已生成")
            return tmp_path
        except ImportError:
            print("⚠️  生成默认封面需要 Pillow 库，请运行: pip install pillow")
            return None
        except Exception as e:
            print(f"⚠️  生成默认封面失败: {e}")
            return None

    def test_connection(self) -> bool:
        """测试连接"""
        try:
            self._ensure_token()
            print("✅ 微信公众号连接测试成功！")
            return True
        except Exception as e:
            print(f"❌ 连接测试失败：{e}")
            return False

    @staticmethod
    def _generate_digest(content: str, max_length: int = 100) -> str:
        """从 HTML 内容中生成纯文本摘要"""
        text = re.sub(r'<[^>]+>', '', content)
        if len(text) > max_length:
            return text[:max_length] + '...'
        return text
