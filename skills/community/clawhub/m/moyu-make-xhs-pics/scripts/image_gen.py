"""
baoyu-openclaw - 小红书图片生成器
支持两种模式：封面图 和 插图
"""

import os
import requests
import json
from typing import Dict, Optional, Any
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath

# 安装 Pillow: pip install Pillow
try:
    from PIL import Image, ImageDraw, ImageFont
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: Pillow not installed, watermark will not be added")

# ============ 风格定义 ============
STYLES = {
    "warm": {
        "keywords": ["温暖", "友好", "柔和色调", "温馨", "舒适", "暖色"],
        "description": "温暖友好的风格，适合情感类内容"
    },
    "notion": {
        "keywords": ["极简", "手绘线条", "知识感", "专业", "简洁", "扁平化"],
        "description": "极简手绘风格，适合知识干货类内容"
    },
    "fresh": {
        "keywords": ["清新", "自然", "干净", "明亮", "通透", "清爽"],
        "description": "清新自然的风格，适合生活分享类内容"
    }
}

# 布局定义
LAYOUT = "balanced"

# 尺寸定义
DEFAULT_WIDTH = 720
DEFAULT_HEIGHT = 1200

# 水印文字
WATERMARK = "AI 生成"


def generate_prompt(content: str, style: str = "notion", mode: str = "cover") -> str:
    """
    根据内容和风格生成提示词
    
    Args:
        content: 文章内容或标题
        style: 风格 (warm/notion/fresh)
        mode: 模式 (cover/illustration)
            - cover: 封面图，图片是内容的视觉提炼，不包含文字
            - illustration: 插图，图片是某个小节的概括，不包含文字
    """
    if style not in STYLES:
        style = "notion"
    
    style_info = STYLES[style]
    keywords = "，".join(style_info["keywords"][:3])
    
    if mode == "cover":
        # 封面图：内容的视觉提炼，不包含文字
        prompt = f"{content}的视觉概念图，{keywords}风格，现代扁平化设计，简约大气，主体突出，无文字符号，整体画面和谐完整"
    else:
        # 插图：具体场景描绘，避免抽象
        prompt = f"具体场景：{content}。{keywords}风格，扁平化插图，清晰的单个场景画面，有明确的主体事物和简单背景，画面干净易懂，无文字，无抽象图形"
    
    return prompt


def add_watermark(image_path: str, position: str = "右下角") -> str:
    """
    在图片上添加水印
    
    Args:
        image_path: 图片路径
        position: 水印位置 (左下角/右下角)
    
    Returns:
        添加水印后的图片路径
    """
    if not HAS_PIL:
        return image_path
    
    try:
        # 打开图片
        img = Image.open(image_path)
        
        # 创建绘图对象
        draw = ImageDraw.Draw(img)
        
        # 获取图片尺寸
        width, height = img.size
        
        # 尝试使用系统字体，优先使用支持中文的字体
        font_size = max(16, width // 30)
        font_paths = [
            "/System/Library/Fonts/STHeiti Medium.ttc",  # 黑体
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/Helvetica.ttc",
        ]
        
        font = None
        for font_path in font_paths:
            try:
                font = ImageFont.truetype(font_path, font_size)
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # 获取文字尺寸
        bbox = draw.textbbox((0, 0), WATERMARK, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # 计算位置
        padding = 20
        if position == "左下角":
            x = padding
            y = height - text_height - padding
        else:  # 右下角
            x = width - text_width - padding
            y = height - text_height - padding
        
        # 绘制文字（带阴影效果，更清晰）
        shadow_color = (0, 0, 0)
        text_color = (255, 255, 255)
        
        # 阴影
        draw.text((x + 2, y + 2), WATERMARK, fill=shadow_color, font=font)
        # 文字
        draw.text((x, y), WATERMARK, fill=text_color, font=font)
        
        # 保存
        img.save(image_path)
        return image_path
        
    except Exception as e:
        print(f"添加水印失败: {e}")
        return image_path


class MiniMaxProvider:
    """MiniMax 图像生成服务提供商"""
    
    def __init__(self):
        self.api_key = os.getenv('MINIMAX_API_KEY')
        if not self.api_key:
            raise ValueError("MINIMAX_API_KEY 环境变量未设置")
        self.base_url = "https://api.minimaxi.com/v1/image_generation"
    
    def generate(self, prompt: str, style: str, width: int, height: int, mode: str = "cover") -> Dict[str, Any]:
        """生成图像"""
        # MiniMax 使用标准长宽比格式
        if width == 720 and height == 1200:
            aspect_ratio = "2:3"
        elif width == height:
            aspect_ratio = "1:1"
        elif width / height > 1:
            aspect_ratio = "16:9"
        else:
            aspect_ratio = "9:16"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 根据风格优化提示词
        styled_prompt = self._apply_style(prompt, style)
        
        payload = {
            "model": "image-01",
            "prompt": styled_prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": 1,
            "prompt_optimizer": True
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("data", {}).get("image_urls"):
                    image_urls = data["data"]["image_urls"]
                    image_url = image_urls[0]
                    
                    # 下载图片
                    local_path = self._download_image(image_url, prompt)
                    
                    if local_path:
                        # 添加水印
                        local_path = add_watermark(local_path, position="右下角")
                        
                        return {
                            "success": True,
                            "image_url": image_url,
                            "local_path": local_path
                        }
                    else:
                        return {
                            "success": False,
                            "image_url": None,
                            "local_path": None,
                            "error": "下载图片失败"
                        }
                else:
                    return {
                        "success": False,
                        "image_url": None,
                        "local_path": None,
                        "error": f"API 响应中未找到图片链接: {data}"
                    }
            else:
                return {
                    "success": False,
                    "image_url": None,
                    "local_path": None,
                    "error": f"API 请求失败: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "image_url": None,
                "local_path": None,
                "error": f"请求异常: {str(e)}"
            }
    
    def _apply_style(self, prompt: str, style: str) -> str:
        """根据风格调整提示词"""
        style_descriptions = {
            "warm": "温暖色调，柔和光影，温馨氛围",
            "notion": "清新简约，现代设计感，干净利落",
            "fresh": "明亮色彩，生动活泼，清爽风格"
        }
        
        style_desc = style_descriptions.get(style, "")
        if style_desc:
            return f"{prompt}, {style_desc}"
        return prompt
    
    def _download_image(self, url: str, prompt: str) -> Optional[str]:
        """下载图片到本地"""
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                # 生成文件名
                safe_name = "".join(c for c in prompt[:20] if c.isalnum())
                filename = f"minimax_{hash(prompt) % 100000}.png"
                filepath = f"/tmp/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f"下载失败: {e}")
        return None


class DashScopeProvider:
    """阿里百炼图像生成服务提供商"""
    
    def __init__(self):
        self.api_key = os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
        
        # 动态导入 dashscope
        try:
            import dashscope
            from dashscope import ImageSynthesis
            from http import HTTPStatus
            self.dashscope = dashscope
            self.ImageSynthesis = ImageSynthesis
            self.HTTPStatus = HTTPStatus
        except ImportError:
            raise ImportError("请安装 dashscope: pip install dashscope")
        
        self.dashscope.api_key = self.api_key
    
    def generate(self, prompt: str, style: str, width: int, height: int, mode: str = "cover") -> Dict[str, Any]:
        """生成图像"""
        # 风格优化
        styled_prompt = self._apply_style(prompt, style)
        
        size = f"{width}*{height}"
        
        try:
            rsp = self.ImageSynthesis.call(
                api_key=self.api_key,
                model="qwen-image-plus",
                prompt=styled_prompt,
                negative_prompt=" ",
                n=1,
                size=size,
                prompt_extend=True,
                watermark=False
            )
            
            if rsp.status_code == self.HTTPStatus.OK and rsp.output.task_status == 'SUCCEEDED':
                for result in rsp.output.results:
                    # 下载图片
                    local_path = self._download_image(result.url, prompt)
                    
                    if local_path:
                        # 添加水印
                        local_path = add_watermark(local_path, position="右下角")
                        
                        return {
                            "success": True,
                            "image_url": result.url,
                            "local_path": local_path
                        }
                    else:
                        return {
                            "success": False,
                            "image_url": None,
                            "local_path": None,
                            "error": "下载图片失败"
                        }
            else:
                msg = rsp.output.message if rsp.output else "未知错误"
                return {
                    "success": False,
                    "image_url": None,
                    "local_path": None,
                    "error": f"API 调用失败: {msg}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "image_url": None,
                "local_path": None,
                "error": f"请求异常: {str(e)}"
            }
    
    def _apply_style(self, prompt: str, style: str) -> str:
        """根据风格调整提示词"""
        style_descriptions = {
            "warm": "温暖色调，柔和光影，温馨氛围",
            "notion": "清新简约，现代设计感，干净利落",
            "fresh": "明亮色彩，生动活泼，清爽风格"
        }
        
        style_desc = style_descriptions.get(style, "")
        if style_desc:
            return f"{prompt}, {style_desc}"
        return prompt
    
    def _download_image(self, url: str, prompt: str) -> Optional[str]:
        """下载图片到本地"""
        try:
            response = requests.get(url, timeout=60)
            if response.status_code == 200:
                safe_name = "".join(c for c in prompt[:20] if c.isalnum())
                filename = f"dashscope_{hash(prompt) % 100000}.png"
                filepath = f"/tmp/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f"下载失败: {e}")
        return None


def generate_image(
    prompt: str,
    style: str = "notion",
    provider: str = "minimax",
    mode: str = "cover",
    width: int = 720,
    height: int = 1200
) -> Dict[str, Any]:
    """
    生成图像的主要函数
    
    Args:
        prompt: 图像生成的提示词
        style: 风格类型 (warm/notion/fresh)
        provider: 服务提供商 (minimax/dashscope)
        mode: 图像模式
            - cover: 封面图，图片是内容的视觉提炼
            - illustration: 插图，图片是某个小节的概括
        width: 图像宽度
        height: 图像高度
    
    Returns:
        dict: 包含 success, image_url, local_path 的字典
    """
    # 验证尺寸
    if width % 8 != 0 or height % 8 != 0:
        return {
            "success": False,
            "image_url": None,
            "local_path": None,
            "error": f"宽度({width})和高度({height})必须是8的倍数"
        }
    
    # 验证风格
    if style not in STYLES:
        return {
            "success": False,
            "image_url": None,
            "local_path": None,
            "error": f"无效的风格参数，支持: {list(STYLES.keys())}"
        }
    
    # 验证模式
    if mode not in ["cover", "illustration"]:
        return {
            "success": False,
            "image_url": None,
            "local_path": None,
            "error": "无效的模式，支持: cover (封面图), illustration (插图)"
        }
    
    # 生成优化的提示词
    optimized_prompt = generate_prompt(prompt, style, mode)
    
    # 选择提供商
    if provider.lower() == "minimax":
        provider_instance = MiniMaxProvider()
        actual_width, actual_height = width, height
    elif provider.lower() == "dashscope":
        provider_instance = DashScopeProvider()
        # DashScope 只支持特定尺寸
        actual_width, actual_height = 720, 1280
    else:
        return {
            "success": False,
            "image_url": None,
            "local_path": None,
            "error": f"无效的服务提供商，支持: ['minimax', 'dashscope']"
        }
    
    # 生成图像
    return provider_instance.generate(optimized_prompt, style, actual_width, actual_height, mode)


# 测试
if __name__ == "__main__":
    import sys
    
    # 测试
    result = generate_image(
        prompt="AI时代读代码的正确姿势",
        style="notion",
        mode="cover"
    )
    
    print("结果:", result)
