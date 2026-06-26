#!/usr/bin/env python3
"""
Online OCR using SiliconFlow DeepSeek-OCR API
支持本地图片和 URL，包含图像预处理功能
"""

import os
import sys
import json
import re
import base64
import requests
import time
from pathlib import Path
from io import BytesIO

# 图像处理库
try:
    from PIL import Image, ImageEnhance, ImageFilter
    import numpy as np
    IMAGE_PROCESSING_AVAILABLE = True
except ImportError:
    IMAGE_PROCESSING_AVAILABLE = False


class ImagePreprocessor:
    """图像预处理类，提供多种预处理方法以提升 OCR 识别率"""
    
    def __init__(self, config=None):
        """
        初始化预处理配置
        config: dict, 包含预处理选项
            - resize_max_size: int, 最大边长，超过则等比例缩放（默认 2000）
            - enhance_contrast: float, 对比度增强系数（1.0=不变, >1增强, <1降低，默认 1.5）
            - sharpen: float, 锐化强度（0=不锐化, 1-2 锐化，默认 0.5）
            - denoise: bool, 是否去噪（默认 True）
            - to_grayscale: bool, 是否转灰度（默认 True）
            - binarize: bool, 是否二值化（默认 False）
            - binarize_threshold: int, 二值化阈值 0-255（默认 128）
        """
        self.config = {
            'resize_max_size': 2000,
            'enhance_contrast': 1.5,
            'sharpen': 0.5,
            'denoise': True,
            'to_grayscale': True,
            'binarize': False,
            'binarize_threshold': 128,
        }
        if config:
            self.config.update(config)
        
        if not IMAGE_PROCESSING_AVAILABLE:
            raise RuntimeError("图像处理库未安装，请安装 Pillow 和 numpy")
    
    def load_image(self, image_path):
        """加载图像"""
        return Image.open(image_path)
    
    def resize_image(self, img):
        """等比例缩放图像，保持宽高比"""
        max_size = self.config['resize_max_size']
        width, height = img.size
        
        if max(width, height) <= max_size:
            return img
        
        if width > height:
            new_width = max_size
            new_height = int(height * max_size / width)
        else:
            new_height = max_size
            new_width = int(width * max_size / height)
        
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    def enhance_contrast(self, img):
        """增强对比度"""
        factor = self.config['enhance_contrast']
        if factor == 1.0:
            return img
        enhancer = ImageEnhance.Contrast(img)
        return enhancer.enhance(factor)
    
    def sharpen_image(self, img):
        """锐化图像"""
        factor = self.config['sharpen']
        if factor <= 0:
            return img
        # 使用 ImageFilter 锐化
        sharpened = img.filter(ImageFilter.SHARPEN)
        # 多次锐化以增强效果
        for _ in range(int(factor) - 1):
            sharpened = sharpened.filter(ImageFilter.SHARPEN)
        return sharpened
    
    def denoise_image(self, img):
        """去噪处理"""
        if not self.config['denoise']:
            return img
        
        # 中值滤波去噪
        if img.mode in ('L', 'RGB', 'RGBA'):
            return img.filter(ImageFilter.MedianFilter(size=3))
        return img
    
    def to_grayscale(self, img):
        """转换为灰度图"""
        if not self.config['to_grayscale']:
            return img
        if img.mode in ('L', 'LA', 'P', '1'):
            return img.convert('L')
        return img.convert('L')
    
    def binarize(self, img):
        """二值化"""
        if not self.config['binarize']:
            return img
        threshold = self.config['binarize_threshold']
        return img.point(lambda p: 255 if p > threshold else 0, mode='1').convert('L')
    
    def preprocess(self, image_path):
        """
        完整预处理流程
        返回: PIL Image 对象
        """
        img = self.load_image(image_path)
        
        # 1. 调整大小
        img = self.resize_image(img)
        
        # 2. 去噪
        img = self.denoise_image(img)
        
        # 3. 转灰度
        img = self.to_grayscale(img)
        
        # 4. 增强对比度
        img = self.enhance_contrast(img)
        
        # 5. 锐化
        img = self.sharpen_image(img)
        
        # 6. 二值化（可选）
        img = self.binarize(img)
        
        return img
    
    def preprocess_to_base64(self, image_path, format='PNG'):
        """
        预处理并转换为 base64
        返回: base64 字符串
        """
        img = self.preprocess(image_path)
        
        # 转换为字节流
        buffered = BytesIO()
        img.save(buffered, format=format)
        img_bytes = buffered.getvalue()
        
        return base64.b64encode(img_bytes).decode('utf-8')


class OnlineOCR:
    def __init__(self, config_path=None):
        """
        初始化 OnlineOCR
        config_path: 可选，配置文件路径。默认使用 skill 目录下的 config.json
        """
        # 确定 skill 目录
        self.skill_dir = Path(__file__).parent.parent
        
        # 确定配置文件路径
        if config_path is None:
            config_path = self.skill_dir / "config.json"
        self.config_path = Path(config_path)
        
        # 从配置文件读取（必须存在）
        self.config = self._load_config()
        
        # 提取配置值
        self.api_key = self.config.get("apiKey", "").strip()
        self.base_url = self.config.get("baseUrl", "https://api.siliconflow.cn/v1")
        self.model = self.config.get("model", "deepseek-ai/DeepSeek-OCR")
        
        # 初始化图像预处理器
        preprocess_config = self.config.get("preprocess", {})
        self.preprocessor = ImagePreprocessor(preprocess_config)
        
        # 验证 API key
        if not self.api_key:
            raise ValueError(
                f"未找到 API key。请在 skill 目录下的 config.json 文件中设置 'apiKey' 字段。\n"
                f"配置文件路径: {self.config_path}"
            )
    
    def _load_config(self):
        """从 JSON 文件加载配置（必须存在）"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"配置文件不存在: {self.config_path}\n"
                f"请创建该文件并填入 API key，格式示例:\n"
                f'{{\n  "apiKey": "your-siliconflow-api-key-here"\n}}'
            )
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"配置文件 JSON 格式错误: {e}")
        except Exception as e:
            raise RuntimeError(f"读取配置文件失败: {e}")

    def recognize(self, image_input):
        """
        识别图片文字
        image_input: 图片路径或 URL
        """
        # 判断输入类型
        if image_input.startswith(('http://', 'https://')):
            # URL 方式
            image_url = image_input
            image_data = None
        else:
            # 本地文件
            if not os.path.exists(image_input):
                return {'success': False, 'error': f'文件不存在: {image_input}'}
            
            # 使用预处理器处理图片并转为 base64
            try:
                image_data = self.preprocessor.preprocess_to_base64(image_input)
                image_url = None
            except Exception as e:
                return {'success': False, 'error': f'图像预处理失败: {e}'}
        
        # 构建请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # 使用标准 DeepSeek-OCR prompt
        ocr_prompt = "<image>\n<|grounding|>OCR this image."
        
        # 构建请求
        payload = {
            "model": self.model,
            "stream": False,
            "max_tokens": 4096,
            "temperature": 0.0,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.0,
        }
        
        if image_url:
            payload["messages"] = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url}
                        },
                        {
                            "type": "text",
                            "text": ocr_prompt
                        }
                    ]
                }
            ]
        else:
            # base64 编码
            payload["messages"] = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_data}"}
                        },
                        {
                            "type": "text",
                            "text": ocr_prompt
                        }
                    ]
                }
            ]
        
        # 重试机制（最多5次）
        max_retries = 5
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                
                if response.status_code != 200:
                    if response.status_code in (401, 403):
                        return {
                            'success': False,
                            'error': f'API 认证失败: HTTP {response.status_code}',
                            'details': response.text[:300]
                        }
                    elif attempt < max_retries - 1:
                        time.sleep(1)  # 等待后重试
                        continue
                    else:
                        return {
                            'success': False,
                            'error': f'API 请求失败: HTTP {response.status_code}',
                            'details': response.text[:500]
                        }
                
                result = response.json()
                
                # 提取文本
                if 'choices' in result and result['choices']:
                    content = result['choices'][0]['message']['content'].strip()
                    
                    # 使用正则提取 <|ref|>...</|ref|> 标签内的文本
                    # DeepSeek-OCR 可能返回带标签的内容
                    texts = re.findall(r'<\|ref\|>(.*?)<\|/ref\|>', content, flags=re.DOTALL)
                    if texts:
                        text = '\n'.join(texts).strip()
                    else:
                        # 如果没有标签，直接使用完整内容
                        text = content
                    
                    return {
                        'success': True,
                        'text': text,
                        'engine': 'deepseek-ocr',
                        'model': self.model,
                        'usage': result.get('usage', {})
                        }
                else:
                    return {'success': False, 'error': 'API 返回格式异常', 'raw': result}
                    
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return {'success': False, 'error': f'请求异常: {e}'}
            except Exception as e:
                return {'success': False, 'error': f'处理异常: {e}'}
        
        return {'success': False, 'error': '重试5次后仍失败'}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python ocr.py <图片路径或URL> [--json]")
        sys.exit(1)
    
    image_input = sys.argv[1]
    json_output = '--json' in sys.argv
    
    try:
        processor = OnlineOCR()
        result = processor.recognize(image_input)
        
        if json_output:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result['success']:
                print(f"✅ OCR 识别成功（引擎: {result.get('engine')}）")
                print("=" * 60)
                print(result['text'])
                print("=" * 60)
            else:
                print(f"❌ {result.get('error')}")
                sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)
