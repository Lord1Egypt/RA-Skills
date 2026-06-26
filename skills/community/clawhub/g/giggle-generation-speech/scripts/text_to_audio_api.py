#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
giggle.pro 平台文转音 API 封装脚本
将文本合成为 AI 语音，支持多种音色、情绪和语速
使用方法: python text_to_audio_api.py --text "要合成的文字" [其他参数]
"""

import os
import sys
import time
import json
import argparse
import warnings
warnings.filterwarnings("ignore")
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List

class TaskStatus:
    COMPLETED = "completed"
    FAILED = "failed"
    PROCESSING = "processing"
    PENDING = "pending"


# ── 防重复推送（.sent 文件标记）────────────────────────────────────────────────
def _get_log_dir() -> Path:
    log_dir = Path.home() / '.openclaw' / 'skills' / 'giggle-generation-speech' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir


def _check_sent(task_id: str) -> bool:
    return (_get_log_dir() / f"{task_id}.sent").exists()


def _mark_sent(task_id: str) -> None:
    (_get_log_dir() / f"{task_id}.sent").touch()


def _save_task_text(task_id: str, text: str) -> None:
    try:
        (_get_log_dir() / f"{task_id}.prompt").write_text(text, encoding='utf-8')
    except Exception:
        pass


def _load_task_text(task_id: str, truncate: bool = True) -> Optional[str]:
    try:
        f = _get_log_dir() / f"{task_id}.prompt"
        if f.exists():
            text = f.read_text(encoding='utf-8').strip()
            if truncate:
                return text[:20] + "..." if len(text) > 20 else text
            return text
    except Exception:
        pass
    return None


def _get_query_count(task_id: str) -> int:
    f = _get_log_dir() / f"{task_id}.count"
    try:
        return int(f.read_text().strip()) if f.exists() else 0
    except Exception:
        return 0


def _increment_query_count(task_id: str) -> int:
    f = _get_log_dir() / f"{task_id}.count"
    count = _get_query_count(task_id) + 1
    f.write_text(str(count))
    return count


class TextToAudioAPI:
    """giggle.pro 文转音 API 客户端"""

    BASE_URL = "https://giggle.pro"
    SUBMIT_ENDPOINT = "/api/v1/generation/text-to-audio"
    QUERY_ENDPOINT = "/api/v1/generation/task/query"
    PRESET_TONES_ENDPOINT = "/api/v1/project/preset_tones"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "x-auth": api_key,
            "Content-Type": "application/json"
        }

    def submit(
        self,
        text: str,
        voice_id: str = "Calm_Woman",
        emotion: Optional[str] = None,
        speed: float = 1.0
    ) -> Dict[str, Any]:
        """提交文转音任务"""
        payload = {
            "text": text,
            "voice_id": voice_id,
            "speed": speed
        }
        if emotion:
            payload["emotion"] = emotion

        url = f"{self.BASE_URL}{self.SUBMIT_ENDPOINT}"
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 200:
                raise Exception(f"API错误: {result.get('msg', result.get('message', '未知错误'))}")
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")

    def query_task(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        url = f"{self.BASE_URL}{self.QUERY_ENDPOINT}"
        params = {"task_id": task_id}
        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 200:
                raise Exception(f"API错误: {result.get('msg', result.get('message', '未知错误'))}")
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"查询失败: {str(e)}")

    def get_preset_tones(self) -> Dict[str, Any]:
        """获取可用音色列表"""
        url = f"{self.BASE_URL}{self.PRESET_TONES_ENDPOINT}"
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()
            if result.get("code") != 200:
                raise Exception(f"API错误: {result.get('msg', result.get('message', '未知错误'))}")
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求失败: {str(e)}")

    def wait_for_completion(
        self,
        task_id: str,
        max_wait_time: int = 120,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """轮询等待任务完成"""
        start_time = time.time()
        last_status = ""
        while time.time() - start_time < max_wait_time:
            result = self.query_task(task_id)
            data = result.get("data", {})
            status = data.get("status", "")

            if status != last_status:
                print(f"任务状态: {status}", file=sys.stderr)
                last_status = status

            if status == TaskStatus.COMPLETED:
                print("✓ 任务完成!", file=sys.stderr)
                return result
            elif status == TaskStatus.FAILED:
                err_msg = data.get("err_msg", "未知错误")
                raise Exception(f"任务失败: {err_msg}")

            time.sleep(poll_interval)

        raise Exception(f"等待超时 ({max_wait_time}秒)")

    def extract_audio_url(self, task_result: Dict[str, Any]) -> str:
        """从任务结果中提取音频 URL（文转音通常单条）"""
        data = task_result.get("data", {})
        urls = data.get("urls", [])
        if not urls:
            return ""
        url = urls[0]
        # 在线收听：去掉 attachment，编码 ~
        view_url = url.replace("&response-content-disposition=attachment", "")
        view_url = view_url.replace("?response-content-disposition=attachment&", "?")
        view_url = view_url.replace("?response-content-disposition=attachment", "")
        view_url = view_url.replace("~", "%7E")
        return view_url


def load_api_key() -> str:
    """加载 API Key，从系统环境变量 GIGGLE_API_KEY 读取"""
    api_key = os.getenv("GIGGLE_API_KEY")
    if not api_key:
        print("错误: 未找到 GIGGLE_API_KEY，请设置系统环境变量：", file=sys.stderr)
        print("  export GIGGLE_API_KEY=your_api_key", file=sys.stderr)
        print("  API Key 可在 https://giggle.pro/ 账号设置中获取。", file=sys.stderr)
        sys.exit(1)
    return api_key


def parse_args():
    parser = argparse.ArgumentParser(
        description='giggle.pro 文转音 API - 文本转语音工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--text', type=str, help='要合成的文本内容')
    parser.add_argument('--voice-id', type=str, required=False, help='音色 ID（使用 --list-voices 查看可用音色）')
    parser.add_argument('--emotion', type=str, help='情绪，如 joy、sad、neutral')
    parser.add_argument('--speed', type=float, default=1.0, help='语速倍率，默认 1')
    parser.add_argument('--list-voices', action='store_true', help='获取可用音色列表')
    parser.add_argument('--query', action='store_true', help='查询任务状态')
    parser.add_argument('--task-id', type=str, help='任务 ID（与 --query 配合）')
    parser.add_argument('--poll', action='store_true', help='配合 --query 轮询等待完成')
    parser.add_argument('--no-wait', action='store_true', help='不等待，提交后立即返回')
    parser.add_argument('--max-wait', type=int, default=120, help='最大等待秒数')
    parser.add_argument('--json', action='store_true', help='JSON 格式输出')
    return parser.parse_args()


def main():
    args = parse_args()
    api_key = load_api_key()
    client = TextToAudioAPI(api_key)

    task_id = None
    submitted_at = None

    try:
        # 1. 列出音色
        if args.list_voices:
            result = client.get_preset_tones()
            voices = result.get("data", [])
            if args.json:
                print(json.dumps(voices, ensure_ascii=False, indent=2))
            else:
                print("\n可用音色列表：\n")
                for v in voices:
                    vid = v.get("voice_id", "")
                    name = v.get("name", "")
                    style = v.get("style", "")
                    gender = v.get("gender", "")
                    age = v.get("age", "")
                    lang = v.get("language", "")
                    print(f"  voice_id: {vid}")
                    print(f"    名称: {name} | 风格: {style} | 性别: {gender} | 年龄: {age} | 语言: {lang}")
                    print()
            sys.exit(0)

        # 2. 查询模式
        if args.query:
            if not args.task_id:
                print("错误: 查询模式需要 --task-id", file=sys.stderr)
                sys.exit(1)

            # --poll：同步轮询直到完成（Phase 3 兜底）
            if args.poll:
                try:
                    result = client.wait_for_completion(
                        args.task_id,
                        max_wait_time=args.max_wait,
                        poll_interval=5
                    )
                    if _check_sent(args.task_id):
                        sys.exit(0)
                    _mark_sent(args.task_id)
                    url = client.extract_audio_url(result)
                    text_preview = _load_task_text(args.task_id) or "语音"
                    print(f"🔊 语音已就绪！\n\n「{text_preview}」的配音已完成 ✨\n\n[收听]({url})\n\n如需调整，随时告诉我~")
                except Exception as ex:
                    text_preview = _load_task_text(args.task_id) or "语音"
                    print(f"😔 语音生成遇到了问题\n\n「{text_preview}」未能完成：{ex}\n\n💡 建议调整后重试~")
                sys.exit(0)

            # 单次查询（Cron 轮询）
            count = _increment_query_count(args.task_id)
            if count > 10:
                text_preview = _load_task_text(args.task_id) or "语音"
                print(f"⏰ 语音生成超时\n\n关于「{text_preview}」的合成已等待较长时间，未能完成。\n\n💡 建议重新生成~")
                sys.exit(0)

            result = client.query_task(args.task_id)
            data = result.get("data", {})
            status = data.get("status")

            if status == TaskStatus.COMPLETED:
                if _check_sent(args.task_id):
                    sys.exit(0)
                _mark_sent(args.task_id)
                url = client.extract_audio_url(result)
                text_preview = _load_task_text(args.task_id) or "语音"
                print(f"🔊 语音已就绪！\n\n「{text_preview}」的配音已完成 ✨\n\n[收听]({url})\n\n如需调整，随时告诉我~")
                sys.exit(0)
            elif status == TaskStatus.FAILED:
                text_preview = _load_task_text(args.task_id) or "语音"
                err = data.get("err_msg", "未知错误")
                print(f"😔 语音生成遇到了问题\n\n「{text_preview}」未能完成：{err}\n\n💡 建议调整后重试~")
                sys.exit(0)
            else:
                print(json.dumps({"status": status, "task_id": args.task_id}, ensure_ascii=False))
                sys.exit(0)

        # 3. 提交模式
        if not args.text:
            print("错误: 需要提供 --text 参数", file=sys.stderr)
            sys.exit(1)

        if not args.voice_id:
            print("错误: 需要提供 --voice-id 参数，请先运行 --list-voices 查看可用音色", file=sys.stderr)
            sys.exit(1)

        result = client.submit(
            text=args.text,
            voice_id=args.voice_id,
            emotion=args.emotion,
            speed=args.speed
        )
        task_id = result.get("data", {}).get("task_id")
        submitted_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        _save_task_text(task_id, args.text)
        print(f"✓ 任务已创建 TaskID: {task_id}", file=sys.stderr)

        if args.no_wait:
            print(json.dumps({"status": "started", "task_id": task_id}, ensure_ascii=False))
        else:
            final = client.wait_for_completion(task_id, max_wait_time=args.max_wait)
            url = client.extract_audio_url(final)
            if args.json:
                print(json.dumps({"audio_url": url}, ensure_ascii=False))
            else:
                print(f"🔊 语音已就绪！\n\n[收听]({url})\n")
    except Exception as e:
        print(f"✗ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
