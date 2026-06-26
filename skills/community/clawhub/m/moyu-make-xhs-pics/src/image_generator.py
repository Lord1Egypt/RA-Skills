"""
图片生成模块
"""

import os
import requests
from typing import Dict, Any, Optional

from .types import ImageResult, STYLES


class ImageGenerator:
    """图片生成器"""
    
    def __init__(self, provider: str = "minimax"):
        """
        初始化
        
        Args:
            provider: API 提供商 ("minimax" 或 "dashscope")
            
        Raises:
            ValueError: provider 不支持或 API key 未设置
        """
        self.provider = provider.lower()
        
        if self.provider == "minimax":
            self.api_key = os.getenv('MINIMAX_API_KEY')
            if not self.api_key:
                raise ValueError("MINIMAX_API_KEY 环境变量未设置")
            self.base_url = "https://api.minimaxi.com/v1/image_generation"
            
        elif self.provider == "dashscope":
            self.api_key = os.getenv('DASHSCOPE_API_KEY')
            if not self.api_key:
                raise ValueError("DASHSCOPE_API_KEY 环境变量未设置")
            self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
            
        else:
            raise ValueError(f"不支持的 provider: {provider}")
    
    def generate(
        self,
        prompt: str,
        style: str,
        mode: str = "cover"
    ) -> ImageResult:
        """
        生成图片
        
        Args:
            prompt: 提示词
            style: 风格类型
            mode: 图片模式 ("cover", "illustration", "decoration")
            
        Returns:
            ImageResult
        """
        if self.provider == "minimax":
            return self._generate_minimax(prompt, style)
        else:
            return self._generate_dashscope(prompt, style)
    
    def _generate_minimax(self, prompt: str, style: str) -> ImageResult:
        """MiniMax API"""
        # 优化提示词
        styled_prompt = self._apply_style(prompt, style)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "image-01",
            "prompt": styled_prompt,
            "aspect_ratio": "2:3",
            "response_format": "url",
            "n": 1,
            "prompt_optimizer": True
        }
        
        try:
            response = requests.post(
                self.base_url, 
                json=payload, 
                headers=headers, 
                timeout=120
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data is None:
                        return ImageResult(
                            success=False,
                            image_url=None,
                            local_path=None,
                            error=f"API 返回空数据: {response.text[:200]}"
                        )
                except Exception as e:
                    return ImageResult(
                        success=False,
                        image_url=None,
                        local_path=None,
                        error=f"JSON 解析失败: {str(e)}, 响应: {response.text[:200]}"
                    )
                
                if data and data.get("data", {}).get("image_urls"):
                    image_url = data["data"]["image_urls"][0]
                    local_path = self._download_image(image_url, prompt)
                    
                    if local_path:
                        return ImageResult(
                            success=True,
                            image_url=image_url,
                            local_path=local_path,
                            error=None
                        )
                
                return ImageResult(
                    success=False,
                    image_url=None,
                    local_path=None,
                    error=f"API 响应中未找到图片链接: {data}"
                )
            else:
                return ImageResult(
                    success=False,
                    image_url=None,
                    local_path=None,
                    error=f"API 请求失败: {response.status_code}"
                )
                
        except Exception as e:
            return ImageResult(
                success=False,
                image_url=None,
                local_path=None,
                error=f"请求异常: {str(e)}"
            )
    
    def _generate_dashscope(self, prompt: str, style: str) -> ImageResult:
        """阿里百炼 API"""
        try:
            from dashscope import ImageSynthesis
            from http import HTTPStatus
            import dashscope
        except ImportError:
            return ImageResult(
                success=False,
                image_url=None,
                local_path=None,
                error="请安装 dashscope: pip install dashscope"
            )
        
        # 设置 API URL（重要！）
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
        
        # 优化提示词
        styled_prompt = self._apply_style(prompt, style)
        
        try:
            rsp = ImageSynthesis.call(
                api_key=self.api_key,
                model="qwen-image",
                prompt=styled_prompt,
                negative_prompt=" ",
                n=1,
                size="1024*1707",
                prompt_extend=True,
                watermark=False
            )
            
            if rsp.status_code == HTTPStatus.OK and rsp.output.task_status == 'SUCCEEDED':
                result = rsp.output.results[0]
                local_path = self._download_image(result.url, prompt)
                
                if local_path:
                    return ImageResult(
                        success=True,
                        image_url=result.url,
                        local_path=local_path,
                        error=None
                    )
                
                return ImageResult(
                    success=False,
                    image_url=None,
                    local_path=None,
                    error="下载图片失败"
                )
            else:
                msg = rsp.output.message if rsp.output else "未知错误"
                return ImageResult(
                    success=False,
                    image_url=None,
                    local_path=None,
                    error=f"API 调用失败: {msg}"
                )
                
        except Exception as e:
            return ImageResult(
                success=False,
                image_url=None,
                local_path=None,
                error=f"请求异常: {str(e)}"
            )
    
    def _apply_style(self, prompt: str, style: str) -> str:
        """根据风格调整提示词"""
        style_descriptions = {
            "fresh": "清新、自然、干净、明亮、通透",
            "warm": "温暖、友好、柔和、温馨、暖色",
            "notion": "极简、手绘、专业、知识感、扁平化",
            "cute": "可爱、卡通、萌趣、活泼、卡通风格"
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
                filename = f"moyu_{abs(hash(prompt)) % 100000}.png"
                filepath = f"/tmp/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                return filepath
        except Exception as e:
            print(f"下载失败: {e}")
        return None
