#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大模型客户端
提供图像分析、OCR、文案创作和多模态对话功能
"""

import os
import base64
from typing import Optional, List, Dict, Any, Generator
from dataclasses import dataclass
from enum import Enum
import requests
from PIL import Image
import io
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class ModelType(str, Enum):
    """支持的模型类型"""
    = ""
    = ""
    = ""


class CopywritingStyle(str, Enum):
    """文案风格"""
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    CREATIVE = "creative"
    INSPIRING = "inspiring"


class PlatformType(str, Enum):
    """社交媒体平台"""
    WECHAT = "wechat"
    WEIBO = "weibo"
    XIAOHONGSHU = "xiaohongshu"
    DOUYIN = "douyin"


class OutputFormat(str, Enum):
    """OCR 输出格式"""
    TEXT = "text"
    STRUCTURED = "structured"
    JSON = "json"


@dataclass
class AnalysisResult:
    """图像分析结果"""
    content: str
    objects: List[str]
    scene: str
    emotion: str
    suggestions: List[str]


@dataclass
class OCRResult:
    """OCR 识别结果"""
    text: str
    confidence: float
    language: str
    structured_data: Optional[Dict[str, Any]] = None


@dataclass
class CopywritingResult:
    """文案创作结果"""
    title: str
    content: str
    tags: List[str]
    word_count: int
    platform: str


class :
    """大模型客户端"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: ModelType = ModelType.,
        timeout: int = 60,
        max_retries: int = 3
    ):
        """
        初始化客户端

        Args:
            api_key:  API Key
            base_url: API Base URL
            default_model: 默认使用的模型
            timeout: 请求超时时间（秒）
            max_retries: 最大重试次数
        """
        self.api_key = api_key or os.getenv("")
        if not self.api_key:
            raise ValueError(" API Key 未设置，请设置环境变量  或传入 api_key 参数")

        self.base_url = base_url or os.getenv("BASE_URL", "https://api.")
        self.default_model = default_model
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _encode_image(self, image_path: str) -> str:
        """
        将图片编码为 base64

        Args:
            image_path: 图片文件路径

        Returns:
            base64 编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def _validate_image(self, image_path: str) -> bool:
        """
        验证图片文件

        Args:
            image_path: 图片文件路径

        Returns:
            是否为有效图片
        """
        try:
            with Image.open(image_path) as img:
                img.verify()
            return True
        except Exception as e:
            raise ValueError(f"无效的图片文件: {e}")

    def _make_request(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[ModelType] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        发起 API 请求

        Args:
            messages: 消息列表
            model: 使用的模型
            temperature: 温度参数
            max_tokens: 最大输出长度
            stream: 是否流式输出

        Returns:
            API 响应结果
        """
        model = model or self.default_model
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": model.value,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        try:
            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API 请求失败: {e}")

    def analyze_image(
        self,
        image_path: str,
        prompt: str = "请详细分析这张图片",
        model: Optional[ModelType] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> AnalysisResult:
        """
        分析图片内容

        Args:
            image_path: 图片文件路径
            prompt: 分析提示词
            model: 使用的模型
            temperature: 温度参数
            max_tokens: 最大输出长度

        Returns:
            分析结果
        """
        self._validate_image(image_path)
        base64_image = self._encode_image(image_path)

        messages = [
            {
                "role": "system",
                "content": "你是一个专业的图像分析助手，能够深度理解图片内容、场景、情感和视觉元素。"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        response = self._make_request(messages, model, temperature, max_tokens)
        content = response["choices"][0]["message"]["content"]

        # 解析结果为结构化数据
        return self._parse_analysis_result(content)

    def _parse_analysis_result(self, content: str) -> AnalysisResult:
        """解析分析结果"""
        # 这里可以添加更复杂的解析逻辑
        return AnalysisResult(
            content=content,
            objects=[],
            scene="",
            emotion="",
            suggestions=[]
        )

    def extract_text(
        self,
        image_path: str,
        output_format: OutputFormat = OutputFormat.TEXT,
        language: str = "auto",
        model: Optional[ModelType] = None
    ) -> OCRResult:
        """
        从图片中提取文字 (OCR)

        Args:
            image_path: 图片文件路径
            output_format: 输出格式
            language: 语言设置
            model: 使用的模型

        Returns:
            OCR 识别结果
        """
        self._validate_image(image_path)
        base64_image = self._encode_image(image_path)

        prompt = f"请提取图片中的所有文字内容"
        if output_format == OutputFormat.STRUCTURED:
            prompt += "，并保持原有的结构和格式。如果是表格，请用 Markdown 表格格式输出。"
        elif output_format == OutputFormat.JSON:
            prompt += "，并以 JSON 格式输出，包含文本内容和位置信息。"

        if language != "auto":
            prompt += f"文字语言为 {language}。"

        messages = [
            {
                "role": "system",
                "content": "你是一个专业的 OCR 文字识别助手，能够精准识别图片中的文字内容。"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]

        response = self._make_request(messages, model, temperature=0.3, max_tokens=4096)
        text = response["choices"][0]["message"]["content"]

        return OCRResult(
            text=text,
            confidence=0.95,  # 实际应用中可以从 API 获取
            language=language,
            structured_data=None
        )

    def generate_copywriting(
        self,
        image_path: Optional[str] = None,
        prompt: str = "",
        style: CopywritingStyle = CopywritingStyle.CREATIVE,
        platform: PlatformType = PlatformType.WECHAT,
        length: str = "medium",
        model: Optional[ModelType] = None,
        temperature: float = 0.8
    ) -> CopywritingResult:
        """
        生成文案

        Args:
            image_path: 图片文件路径（可选）
            prompt: 创作要求
            style: 文案风格
            platform: 目标平台
            length: 文案长度
            model: 使用的模型
            temperature: 温度参数

        Returns:
            文案创作结果
        """
        system_prompt = f"""你是一个专业的文案创作助手，擅长创作{style.value}风格的文案，
目标平台是{platform.value}。文案应该吸引人、简洁有力、突出���心信息。"""

        user_prompt = f"请创作一段{length}长度的文案"
        if prompt:
            user_prompt += f"，要求：{prompt}"

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": []
            }
        ]

        # 如果提供了图片，添加图片内容
        if image_path:
            self._validate_image(image_path)
            base64_image = self._encode_image(image_path)
            messages[1]["content"].append({
                "type": "text",
                "text": user_prompt + "，基于这张图片进行创作。"
            })
            messages[1]["content"].append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            })
        else:
            messages[1]["content"] = user_prompt

        response = self._make_request(messages, model, temperature, max_tokens=2048)
        content = response["choices"][0]["message"]["content"]

        # 生成标题和标签
        title = self._extract_title(content)
        tags = self._extract_tags(content, style)

        return CopywritingResult(
            title=title,
            content=content,
            tags=tags,
            word_count=len(content),
            platform=platform.value
        )

    def _extract_title(self, content: str) -> str:
        """从文案中提取标题"""
        lines = content.split('\n')
        if lines and len(lines[0]) < 50:
            return lines[0].strip()
        return content[:30] + "..."

    def _extract_tags(self, content: str, style: CopywritingStyle) -> List[str]:
        """从文案中提取标签"""
        # 简单的标签生成逻辑
        tags = [style.value]
        if len(content) > 500:
            tags.append("长文")
        else:
            tags.append("短文")
        return tags

    def create_conversation(self) -> 'Conversation':
        """
        创建一个多轮对话会话

        Returns:
            Conversation 对象
        """
        return Conversation(self)


class Conversation:
    """多轮对话会话"""

    def __init__(self, client: ):
        """
        初始化对话会话

        Args:
            client: 实例
        """
        self.client = client
        self.messages = [
            {
                "role": "system",
                "content": "你是一个基于  大模型的多模态 AI 助手，擅长图像分析、OCR 文字提取、文案创作和多模态对话。"
            }
        ]

    def chat(
        self,
        message: str,
        image_path: Optional[str] = None,
        model: Optional[ModelType] = None,
        temperature: float = 0.7
    ) -> str:
        """
        发送消息并获取回复

        Args:
            message: 用户消息
            image_path: 图片文件路径（可选）
            model: 使用的模型
            temperature: 温度参数

        Returns:
            AI 回复
        """
        user_message = {
            "role": "user",
            "content": []
        }

        if image_path:
            self.client._validate_image(image_path)
            base64_image = self.client._encode_image(image_path)
            user_message["content"] = [
                {
                    "type": "text",
                    "text": message
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        else:
            user_message["content"] = message

        self.messages.append(user_message)

        response = self.client._make_request(
            self.messages,
            model,
            temperature,
            max_tokens=2048
        )

        assistant_message = response["choices"][0]["message"]["content"]
        self.messages.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def get_history(self) -> List[Dict[str, Any]]:
        """获取对话历史"""
        return self.messages.copy()

    def clear_history(self) -> None:
        """清空对话历史"""
        self.messages = [
            {
                "role": "system",
                "content": "你是一个基于  大模型的多模态 AI 助手，擅长图像分析、OCR 文字提取、文案创作和多模态对话。"
            }
        ]


def main():
    """测试代码"""
    import sys

    # 初始化客户端
    try:
        client = ()
        print("✓ 客户端初始化成功")
    except ValueError as e:
        print(f"✗ 初始化失败: {e}")
        sys.exit(1)

    # 测试图像分析
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        try:
            result = client.analyze_image(image_path)
            print(f"\n分析结果:\n{result.content}")
        except Exception as e:
            print(f"✗ 分析失败: {e}")


if __name__ == "__main__":
    main()
