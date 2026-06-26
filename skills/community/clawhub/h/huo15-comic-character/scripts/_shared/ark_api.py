"""火山方舟 API 薄封装：Seedream 4.0 图 / Seedance 2.0 视频 / 豆包大模型 TTS.

2026-04 核对。文档：
- Seedance: https://www.volcengine.com/docs/82379/1520757
- Seedream: doubao-seedream-4-0-250828
- TTS: https://www.volcengine.com/docs/6561/97465
"""
from __future__ import annotations

import base64
import os
import pathlib
import time

import requests

try:
    from config import ENDPOINTS, MODELS
except ImportError:  # 兼容直接运行
    ENDPOINTS = {
        "ark_base": "https://ark.cn-beijing.volces.com/api/v3",
    }
    MODELS = {
        "image": "doubao-seedream-4-0-250828",
        "video": "doubao-seedance-2-0-260128",
        "video_fast": "doubao-seedance-2-0-fast-260128",
        "tts": "doubao-tts-bigtts",
    }


class ArkClient:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("ARK_API_KEY", "")
        if not self.api_key:
            raise RuntimeError("缺少 ARK_API_KEY 环境变量")
        self.base_url = ENDPOINTS["ark_base"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    # ------------ 图像（Seedream 4.0）------------
    def generate_image(
        self,
        prompt: str,
        reference_images: list[str] | None = None,
        size: str = "1024x1792",
        model: str | None = None,
    ) -> str:
        """文生图 / 图生图。返回第一张图片 URL.

        reference_images 传文件路径或 URL，会自动转 data URI.
        """
        content = [{"type": "text", "text": prompt}]
        for img in reference_images or []:
            content.append({
                "type": "image_url",
                "image_url": {"url": self._image_to_data_uri(img)},
            })
        body = {
            "model": model or MODELS["image"],
            "content": content,
            "size": size,
            "watermark": False,
        }
        resp = requests.post(
            f"{self.base_url}/images/generations",
            headers=self.headers,
            json=body,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        # 兼容两种响应结构
        if "data" in data and data["data"]:
            return data["data"][0].get("url", "")
        if "url" in data:
            return data["url"]
        raise RuntimeError(f"image response no url: {data}")

    # ------------ 视频（Seedance 2.0）------------
    def submit_video(
        self,
        prompt: str,
        first_frame: str | None = None,
        last_frame: str | None = None,
        reference_image: str | None = None,
        reference_video: str | None = None,
        reference_audio: str | None = None,
        duration: int = 5,
        ratio: str = "9:16",
        resolution: str = "720p",
        generate_audio: bool = False,
        return_last_frame: bool = False,
        fast: bool = False,
        seed: int | None = None,
    ) -> str:
        """提交视频任务，返回 task_id.

        支持多种输入模态：first_frame / last_frame（首尾帧模式）/ reference_image /
        reference_video / reference_audio。同一请求最多 9 图、3 视频、3 音频。
        """
        content: list[dict] = [{"type": "text", "text": prompt}]

        def _add_img(path: str, role: str):
            content.append({
                "type": "image_url",
                "image_url": {"url": self._image_to_data_uri(path)},
                "role": role,
            })

        if first_frame:
            _add_img(first_frame, "first_frame")
        if last_frame:
            _add_img(last_frame, "last_frame")
        if reference_image:
            _add_img(reference_image, "reference_image")
        if reference_video:
            content.append({
                "type": "video_url",
                "video_url": {"url": reference_video if reference_video.startswith("http") else reference_video},
                "role": "reference_video",
            })
        if reference_audio:
            content.append({
                "type": "audio_url",
                "audio_url": {"url": reference_audio},
                "role": "reference_audio",
            })

        body: dict = {
            "model": MODELS["video_fast" if fast else "video"],
            "content": content,
            "ratio": ratio,
            "resolution": resolution,
            "duration": duration,
            "watermark": False,
            "return_last_frame": return_last_frame,
            "generate_audio": generate_audio,
        }
        if seed is not None:
            body["seed"] = seed

        resp = requests.post(
            f"{self.base_url}/contents/generations/tasks",
            headers=self.headers,
            json=body,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["id"]

    def poll_video(self, task_id: str, timeout_s: int = 900, interval_s: int = 10) -> dict:
        """轮询视频任务，完成返回完整 dict（含 content.video_url / usage.total_tokens）."""
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            time.sleep(interval_s)
            resp = requests.get(
                f"{self.base_url}/contents/generations/tasks/{task_id}",
                headers=self.headers,
                timeout=30,
            )
            data = resp.json()
            status = data.get("status")
            if status == "succeeded":
                return data
            if status == "failed":
                raise RuntimeError(f"视频任务失败: {data}")
        raise TimeoutError(f"视频任务 {task_id} 超时（{timeout_s}s）")

    def download_video(self, url: str, out_path: pathlib.Path) -> pathlib.Path:
        out_path = pathlib.Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(url, stream=True, timeout=300)
        with open(out_path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return out_path

    # ------------ 语音（豆包大模型 TTS）------------
    def tts(
        self,
        text: str,
        voice: str = "zh_female_sinong_conversation_wvae_bigtts",
        out_path: pathlib.Path | str = "out.wav",
        speed: float = 1.0,
        emotion: str | None = None,
    ) -> pathlib.Path:
        """豆包 TTS 合成，写入 out_path.

        voice 是音色 ID，格式 zh_{gender}_{name}_conversation_wvae_bigtts.
        完整音色见 https://www.volcengine.com/docs/6561/97465.

        注意：TTS 可能需要单独的 appid/cluster 凭证（走 openspeech.bytedance.com），
        此处用 ark OpenAI 兼容接口作为简化，实际项目请核对授权方式。
        """
        body = {
            "model": MODELS["tts"],
            "input": text,
            "voice": voice,
            "speed": speed,
            "response_format": "wav",
        }
        if emotion:
            body["emotion"] = emotion

        resp = requests.post(
            f"{self.base_url}/audio/speech",
            headers=self.headers,
            json=body,
            timeout=60,
        )
        resp.raise_for_status()
        out = pathlib.Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(resp.content)
        return out

    # ------------ 工具 ------------
    @staticmethod
    def _image_to_data_uri(path_or_url: str) -> str:
        if path_or_url.startswith(("http://", "https://", "data:")):
            return path_or_url
        p = pathlib.Path(path_or_url)
        ext = p.suffix.lower().lstrip(".") or "jpeg"
        if ext == "jpg":
            ext = "jpeg"
        b64 = base64.b64encode(p.read_bytes()).decode()
        return f"data:image/{ext};base64,{b64}"


def cost_from_video_response(data: dict, resolution: str = "720p") -> float:
    """从视频响应中精确计算成本（按 token）."""
    from config import PRICING
    tokens = data.get("usage", {}).get("total_tokens", 0)
    return round(tokens * PRICING["video_per_mtoken"] / 1_000_000, 3)
