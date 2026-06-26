#!/usr/bin/env python3
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Dict

import requests

DEFAULT_BASE_URL = "https://api.senseaudio.cn"
DEFAULT_MODEL = "Seedance-Pro-1.5"
DEFAULT_DURATION = 12
DEFAULT_RESOLUTION = "720p"
DEFAULT_INTERVAL = 30
DEFAULT_TIMEOUT = 600


@dataclass
class VideoRequest:
    final_video_prompt: str
    orientation: str = "portrait"

    @property
    def ratio(self) -> str:
        if self.orientation == "portrait":
            return "9:16"
        if self.orientation == "landscape":
            return "16:9"
        raise ValueError("orientation must be 'portrait' or 'landscape'")


class SenseAudioVideoClient:
    def __init__(self) -> None:
        self.base_url = os.environ.get("SENSEAUDIO_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self.api_key = os.environ.get("SENSEAUDIO_API_KEY", "").strip()
        self.model = DEFAULT_MODEL
        if not self.api_key:
            raise RuntimeError("缺少配置：SENSEAUDIO_API_KEY")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def create_video(self, request: VideoRequest) -> str:
        prompt = (request.final_video_prompt or "").strip()
        if not prompt:
            raise RuntimeError("final_video_prompt 不能为空")
        payload = {
            "model": self.model,
            "content": [{"type": "text", "text": prompt}],
            "duration": DEFAULT_DURATION,
            "resolution": DEFAULT_RESOLUTION,
            "ratio": request.ratio,
            "provider_specific": {"generate_audio": True},
        }
        resp = requests.post(
            f"{self.base_url}/v1/video/create",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        body = resp.json()
        if not resp.ok:
            raise RuntimeError(f"视频任务创建失败: status={resp.status_code}, body={body}")
        task_id = str(body.get("task_id") or "").strip()
        if not task_id:
            raise RuntimeError(f"视频任务创建失败: {body}")
        return task_id

    def get_video_status(self, task_id: str) -> Dict[str, Any]:
        clean_task_id = (task_id or "").strip()
        if not clean_task_id:
            raise RuntimeError("task_id 不能为空")
        resp = requests.get(
            f"{self.base_url}/v1/video/status",
            headers=self._headers(),
            params={"id": clean_task_id},
            timeout=30,
        )
        body = resp.json()
        if not resp.ok:
            raise RuntimeError(f"查询视频状态失败: status={resp.status_code}, body={body}")
        return body

    def format_status_text(self, status_body: Dict[str, Any]) -> str:
        status = str(status_body.get("status") or "unknown").strip().lower()
        progress = status_body.get("progress")
        task_id = status_body.get("task_id") or status_body.get("id") or ""
        video_url = str(status_body.get("video_url") or "").strip()
        error_message = str(status_body.get("error_message") or "").strip()

        if status == "completed" and video_url:
            return video_url
        if status == "failed":
            return f"视频生成失败: {error_message or 'unknown error'}"
        if progress is None:
            return f"任务 {task_id} 当前状态: {status}"
        return f"任务 {task_id} 当前状态: {status}，进度 {progress}%"

    def poll_video_url(self, task_id: str, interval: int = DEFAULT_INTERVAL, timeout: int = DEFAULT_TIMEOUT) -> str:
        start = time.time()
        last_status: Dict[str, Any] = {}
        while True:
            status_body = self.get_video_status(task_id)
            last_status = status_body
            status = str(status_body.get("status") or "").strip().lower()
            video_url = str(status_body.get("video_url") or "").strip()
            error_message = str(status_body.get("error_message") or "").strip()

            if status == "completed" and video_url:
                return video_url
            if status == "failed":
                raise RuntimeError(f"视频生成失败: {error_message or 'unknown error'}")
            if time.time() - start >= timeout:
                raise RuntimeError(
                    f"视频生成超时: task_id={task_id}, last_status={last_status.get('status') or 'unknown'}"
                )
            time.sleep(max(1, int(interval)))
