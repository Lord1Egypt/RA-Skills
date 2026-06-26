#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDClaw 多模态 API 客户端

提供访问 MDClaw OpenClaw API 的 Python 客户端，支持：
- 文字转语音 (TTS)
- 文生图 (Text to Image)
- 文生视频 (Text to Video)
- 图生视频 (Image to Video)
- 图片上传
- 全网搜索 / 天气查询 / 网页总结
"""

import requests
import time
import os
from typing import Dict, Any, Optional


class MDClawClient:
    """MDClaw 多模态 API 客户端"""

    # 网关地址
    GATEWAY_URL = "https://backend.appmiaoda.com/projects/supabase287606411725160448/functions/v1/openclaw-skill-gateway"

    def __init__(self, api_key: str = None):
        """
        初始化客户端

        Args:
            api_key: MDClaw API Key（可选，默认从环境变量读取）

        Raises:
            ValueError: 当未提供 API Key 且环境变量中也未设置时
        """
        self.api_key = api_key or os.getenv('MDCLAW_API_KEY')

        if not self.api_key:
            raise ValueError(
                "请设置 MDClaw API Key：\n"
                "1. 环境变量：MDCLAW_API_KEY\n"
                "2. 或传入 api_key 参数\n"
                "3. 或注册账号：client.agent_register('用户名', '密码')"
            )

    # ========== 核心调用 ==========

    def _call(self, skill_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用 MDClaw 技能

        Args:
            skill_id: 技能名称
            parameters: 参数字典

        Returns:
            API 响应结果
        """
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "skill_id": skill_id,
            "parameters": parameters
        }

        response = requests.post(self.GATEWAY_URL, json=payload, headers=headers)
        return response.json()

    # ========== 账号管理 ==========

    def agent_register(self, username: str, password: str) -> Dict[str, Any]:
        """
        注册新账号

        Args:
            username: 用户名
            password: 密码

        Returns:
            注册结果，包含 api_key
        """
        result = self._call("agent_register", {
            "username": username,
            "password": password
        })

        if result.get('success'):
            api_key = result.get('result', {}).get('api_key')
            if api_key:
                self.api_key = api_key
                # 保存到环境变量持久化由用户自行处理

        return result

    def agent_login(self, username: str, password: str) -> Dict[str, Any]:
        """
        登录已有账号

        Args:
            username: 用户名
            password: 密码

        Returns:
            登录结果，包含 api_key
        """
        result = self._call("agent_login", {
            "username": username,
            "password": password
        })

        if result.get('success'):
            api_key = result.get('result', {}).get('api_key')
            if api_key:
                self.api_key = api_key

        return result

    # ========== 文字转语音 ==========

    def text_to_speech(
        self,
        text: str,
        model: Optional[str] = None,
        voice_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        文字转语音

        Args:
            text: 需要合成的文本内容（最大1000字符）
            model: 模型（默认: speech-2.8-hd）
            voice_id: 音色 ID（默认: male-qn-qingse）

        Returns:
            包含 audio_url 的结果
        """
        parameters = {"text": text}
        if model is not None:
            parameters["model"] = model
        if voice_id is not None:
            parameters["voice_id"] = voice_id
        return self._call("text_to_speech", parameters)

    # ========== 文生图 ==========

    def text_to_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        aspect_ratio: Optional[str] = None,
        n: Optional[int] = None,
        prompt_optimizer: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        文生图

        Args:
            prompt: 图像描述
            model: 模型名称（可选，默认: image-01）
            aspect_ratio: 宽高比（"1:1", "16:9", "4:3", "3:2", "2:3", "3:4", "9:16"）
            n: 生成数量（1-9）
            prompt_optimizer: 是否使用提示词优化器

        Returns:
            包含 image_urls 列表的结果
        """
        parameters = {"prompt": prompt}
        if model is not None:
            parameters["model"] = model
        if aspect_ratio is not None:
            parameters["aspect_ratio"] = aspect_ratio
        if n is not None:
            parameters["n"] = n
        if prompt_optimizer is not None:
            parameters["prompt_optimizer"] = prompt_optimizer
        return self._call("text_to_image", parameters)

    # ========== 文生视频 ==========

    def text_to_video(
        self,
        prompt: str,
        model: Optional[str] = None,
        duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        文生视频（异步）

        Args:
            prompt: 视频描述
            model: 模型（默认: MiniMax-Hailuo-02）
            duration: 时长（6 或 10 秒）

        Returns:
            包含 task_id 的结果，需用 video_status 查询进度

        Note:
            不要传递 resolution 参数，否则 API 不返回 task_id
        """
        parameters = {"prompt": prompt}
        if model is not None:
            parameters["model"] = model
        if duration is not None:
            parameters["duration"] = duration
        return self._call("text_to_video", parameters)

    # ========== 图生视频 ==========

    def image_to_video(
        self,
        image: str,
        prompt: Optional[str] = None,
        model: Optional[str] = None,
        duration: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        图生视频（异步）

        Args:
            image: 参考图片 URL（必填）
            prompt: 视频描述（可选）
            model: 模型（默认: MiniMax-Hailuo-02）
            duration: 时长（6 或 10 秒）

        Returns:
            包含 task_id 的结果，需用 video_status 查询进度
        """
        parameters = {"image": image}
        if prompt is not None:
            parameters["prompt"] = prompt
        if model is not None:
            parameters["model"] = model
        if duration is not None:
            parameters["duration"] = duration
        return self._call("image_to_video", parameters)

    # ========== 图片上传 ==========

    def upload_image(self, file_path: str) -> Dict[str, Any]:
        """
        上传本地图片并返回 URL

        Args:
            file_path: 本地图片路径

        Returns:
            包含 image_url 的结果
        """
        if not os.path.exists(file_path):
            return {"success": False, "error": f"文件不存在: {file_path}"}

        import mimetypes
        mime_type = mimetypes.guess_type(file_path)[0] or "image/jpeg"

        with open(file_path, 'rb') as f:
            file_data = f.read()

        headers = {"X-API-Key": self.api_key}
        files = {'file': (os.path.basename(file_path), file_data, mime_type)}
        upload_url = self.GATEWAY_URL.replace("openclaw-skill-gateway", "upload")

        try:
            response = requests.post(upload_url, headers=headers, files=files)
            result = response.json()
            if result.get('success'):
                return result
            return self._call("upload_image", {
                "file_name": os.path.basename(file_path),
                "content_type": mime_type
            })
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========== 视频任务查询 ==========

    def video_status(self, task_id: str) -> Dict[str, Any]:
        """
        查询视频任务状态

        Args:
            task_id: 任务 ID

        Returns:
            状态结果。status 取值: Preparing / Queueing / Processing / Success / Fail
            成功时 result.url 为视频下载链接
        """
        return self._call("video_status", {"task_id": task_id})

    def wait_for_video(
        self,
        task_id: str,
        max_wait: int = 240,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """
        等待视频生成完成

        Args:
            task_id: 任务 ID
            max_wait: 最大等待时间（秒），默认 4 分钟
            poll_interval: 轮询间隔（秒）

        Returns:
            最终状态结果，成功时包含 video_url

        Raises:
            TimeoutError: 超时
            Exception: 视频生成失败
        """
        elapsed = 0
        while elapsed < max_wait:
            result = self.video_status(task_id)

            if not result.get('success'):
                time.sleep(poll_interval)
                elapsed += poll_interval
                continue

            status = result.get('result', {}).get('status')

            if status == 'Success':
                return result
            elif status == 'Fail':
                error = result.get('result', {}).get('error', 'Unknown error')
                raise Exception(f"视频生成失败: {error}")

            time.sleep(poll_interval)
            elapsed += poll_interval

        raise TimeoutError(f"视频生成超时，已等待 {max_wait} 秒")

    # ========== 辅助功能 ==========

    def ai_search(self, query: str) -> Dict[str, Any]:
        """AI 驱动的全网搜索"""
        return self._call("ai_search", {"query": query})

    def weather_query(self, city: str) -> Dict[str, Any]:
        """查询城市天气"""
        return self._call("weather_query", {"city": city})

    def web_summary(self, url: str) -> Dict[str, Any]:
        """网页总结"""
        return self._call("web_summary", {"url": url})

    # ========== 便捷下载方法 ==========

    def generate_image_and_download(
        self,
        prompt: str,
        output_path: str,
        aspect_ratio: str = "9:16"
    ) -> bool:
        """
        生成图片并下载到本地

        Args:
            prompt: 图片描述
            output_path: 输出文件路径
            aspect_ratio: 宽高比

        Returns:
            是否成功
        """
        result = self.text_to_image(prompt, aspect_ratio=aspect_ratio)

        if not result.get('success'):
            print(f"文生图失败: {result.get('error')}")
            return False

        image_urls = result.get('result', {}).get('image_urls', [])
        if not image_urls:
            print("未返回图片 URL")
            return False

        try:
            response = requests.get(image_urls[0])
            response.raise_for_status()
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"图片已保存: {output_path}")
            return True
        except Exception as e:
            print(f"下载图片失败: {e}")
            return False

    def generate_video_and_download(
        self,
        image_url: str,
        prompt: str = None,
        output_path: str = None,
        duration: int = 6,
        wait: bool = True
    ) -> Optional[str]:
        """
        生成视频并可选下载到本地

        Args:
            image_url: 参考图片 URL
            prompt: 视频描述
            output_path: 输出文件路径（可选）
            duration: 时长
            wait: 是否等待视频生成完成

        Returns:
            视频 URL 或本地文件路径，失败返回 None
        """
        result = self.image_to_video(image_url, prompt, duration=duration)

        if not result.get('success'):
            print(f"图生视频失败: {result.get('error')}")
            return None

        task_id = result.get('result', {}).get('task_id')
        if not task_id:
            print("未返回 task_id")
            return None

        print(f"任务已提交，task_id: {task_id}")

        if wait:
            print("等待视频生成...")
            final_result = self.wait_for_video(task_id)
            video_url = final_result.get('result', {}).get('url')

            if video_url and output_path:
                try:
                    response = requests.get(video_url)
                    response.raise_for_status()
                    os.makedirs(os.path.dirname(output_path), exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                    print(f"视频已保存: {output_path}")
                    return output_path
                except Exception as e:
                    print(f"下载视频失败: {e}")
                    return video_url

            return video_url

        return task_id
