#!/usr/bin/env python3
"""
IndexTTS API 调用脚本 (Windows 版)
完全适配官方文档：https://indextts.cn/main/developer
所有接口统一使用 /api/third/ 前缀
"""

import os
import sys
import json
import argparse
import logging
import requests
from pathlib import Path
from typing import Optional, Dict, Any
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ========== 日志配置 ==========
# Windows 控制台兼容：避免使用 emoji，使用 ASCII 字符
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ========== 核心配置（按文档要求） ==========
BASE_URL = os.getenv("INDEX_BASE_URL", "https://openapi.lipvoice.cn")
API_SIGN = os.getenv("INDEX_API_SIGN")  # 鉴权用 sign，所有接口必需
TIMEOUT = 30  # 请求超时时间（秒）

# 网络重试配置
RETRY_CONFIG = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[429, 500, 502, 503, 504],
)
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=RETRY_CONFIG))


def validate_config() -> None:
    """验证基础配置（所有接口必需 sign）"""
    if not API_SIGN:
        logger.error("Error: INDEX_API_SIGN environment variable not set")
        logger.info("Set via PowerShell: $env:INDEX_API_SIGN='your-api-sign'")
        logger.info("Set via CMD: set INDEX_API_SIGN=your-api-sign")
        sys.exit(1)
    if not BASE_URL:
        logger.error("Error: INDEX_BASE_URL environment variable not set")
        sys.exit(1)


def api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
    files: Optional[Dict] = None
) -> Dict[str, Any]:
    """
    统一 API 请求函数（完全适配文档鉴权规则）
    :param method: HTTP 方法 (GET/POST/DELETE)
    :param endpoint: 接口端点（如 /api/third/reference/list）
    :param data: JSON 请求体（POST 用）
    :param params: URL 查询参数（GET/DELETE 用）
    :param files: 文件上传参数（仅模型创建用）
    :return: 接口返回的 JSON 数据
    """
    url = f"{BASE_URL.rstrip('/')}{endpoint}"
    logger.info(f"Request: {method} {url}")

    # 所有接口统一 Header：必须携带 sign
    headers = {"sign": API_SIGN}

    try:
        if files:
            # 模型创建：multipart/form-data 上传
            response = session.post(
                url,
                headers=headers,
                files=files,
                data=data,
                timeout=TIMEOUT
            )
        else:
            # 其他接口：GET/POST/DELETE 统一处理
            response = session.request(
                method,
                url,
                headers=headers,
                json=data if method in ["POST"] else None,
                params=params if method in ["GET", "DELETE"] else None,
                timeout=TIMEOUT
            )

        # 检查 HTTP 状态码
        response.raise_for_status()

        # 解析响应
        try:
            result = response.json()
        except json.JSONDecodeError:
            logger.warning(f"Warning: API returned non-JSON response: {response.text}")
            result = {"data": response.text, "code": response.status_code}

        logger.debug(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)}")
        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        if hasattr(e, 'response') and e.response:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response body: {e.response.text}")
        raise


# ========== 克隆模型相关接口 ==========

def create_model(model_name: str, file_path: str, describe: Optional[str] = None) -> None:
    """
    模型创建（POST /api/third/reference/upload）
    :param model_name: 模型名称（必需）
    :param file_path: 音频文件路径（必需，支持 mp3/wav/m4a，<50MB，2-60 秒）
    :param describe: 模型描述（可选）
    """
    path = Path(file_path).resolve()
    if not path.exists():
        logger.error(f"Error: File not found - {file_path}")
        sys.exit(1)
    if not path.is_file():
        logger.error(f"Error: Not a file - {file_path}")
        sys.exit(1)

    # 验证文件格式（按文档要求）
    allowed_ext = [".mp3", ".wav", ".m4a"]
    if path.suffix.lower() not in allowed_ext:
        logger.error(f"Error: Unsupported format {path.suffix}, supported: {allowed_ext}")
        sys.exit(1)

    # 构造请求参数（按文档要求）
    form_data = {"name": model_name}
    if describe:
        form_data["describe"] = describe

    try:
        with open(path, 'rb') as f:
            files = {'file': (path.name, f, f'audio/{path.suffix[1:]}')}
            result = api_request('POST', '/api/third/reference/upload', data=form_data, files=files)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result:
            logger.info(f"[SUCCESS] Model created! audioId: {result['data'].get('audioId')}")
    except Exception as e:
        logger.error(f"Failed to create model: {str(e)}")
        sys.exit(1)


def list_models(page: int = 1, page_size: int = 10) -> None:
    """
    模型列表获取（GET /api/third/reference/list）
    :param page: 页码（可选，默认 1）
    :param page_size: 每页条数（可选，默认 10，最大 20）
    """
    if page_size > 20:
        logger.warning("Warning: pageSize max is 20, adjusted to 20")
        page_size = 20

    params = {"page": str(page), "pageSize": str(page_size)}
    try:
        result = api_request('GET', '/api/third/reference/list', params=params)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result and "list" in result["data"]:
            logger.info(f"[SUCCESS] Total {result['data'].get('total', 0)} models, page {page}")
    except Exception as e:
        logger.error(f"Failed to list models: {str(e)}")
        sys.exit(1)


def get_model_detail(audio_id: str) -> None:
    """
    模型详情查询（GET /api/third/reference/detail）
    注意：此接口可能未在所有账户中开放
    :param audio_id: 模型 ID（必需）
    """
    if not audio_id:
        logger.error("Error: audioId is required")
        sys.exit(1)

    params = {"audioId": audio_id}
    try:
        result = api_request('GET', '/api/third/reference/detail', params=params)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result:
            logger.info(f"[SUCCESS] Model detail retrieved")
        elif result.get("code") == 404:
            logger.warning("[WARNING] This endpoint may not be available for your account")
    except Exception as e:
        logger.error(f"Failed to get model detail: {str(e)}")
        sys.exit(1)


def delete_model(audio_id: str) -> None:
    """
    删除模型数据（DELETE /api/third/reference/delete）
    :param audio_id: 模型 ID（必需，从 list-models 获取）
    """
    if not audio_id:
        logger.error("Error: audioId is required")
        sys.exit(1)

    params = {"audioId": audio_id}
    try:
        result = api_request('DELETE', '/api/third/reference/delete', params=params)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0:
            logger.info(f"[SUCCESS] Model {audio_id} deleted (cannot be undone)")
    except Exception as e:
        logger.error(f"Failed to delete model: {str(e)}")
        sys.exit(1)


# ========== 语音合成相关接口 ==========

# ========== 语调参考音频相关接口（用于情感合成） ==========

def create_tts_reference(file_path: str) -> None:
    """
    上传参考音频（POST /api/third/tts/uploadCustom）
    用于 genre=1（语气参考）模式下的情感合成
    注意：参考音频仅保存 24 小时，过期自动清理
    :param file_path: 音频文件路径（必需，支持 mp3/wav/m4a，<50MB）
    """
    path = Path(file_path).resolve()
    if not path.exists():
        logger.error(f"Error: File not found - {file_path}")
        sys.exit(1)
    if not path.is_file():
        logger.error(f"Error: Not a file - {file_path}")
        sys.exit(1)

    allowed_ext = [".mp3", ".wav", ".m4a"]
    if path.suffix.lower() not in allowed_ext:
        logger.error(f"Error: Unsupported format {path.suffix}, supported: {allowed_ext}")
        sys.exit(1)

    try:
        with open(path, 'rb') as f:
            files = {'file': (path.name, f, f'audio/{path.suffix[1:]}')}
            result = api_request('POST', '/api/third/tts/uploadCustom', files=files)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result and "file" in result["data"]:
            emotion_path = result['data']['file'].get('emotionPath')
            logger.info(f"[SUCCESS] Reference audio uploaded! emotionPath: {emotion_path}")
            logger.info("Note: Reference audio expires in 24 hours")
    except Exception as e:
        logger.error(f"Failed to upload reference audio: {str(e)}")
        sys.exit(1)


def list_tts_references() -> None:
    """
    参考音频列表查询（GET /api/third/tts/listCustom）
    查询已上传的语调参考音频（24 小时内有效）
    """
    try:
        result = api_request('GET', '/api/third/tts/listCustom', params={})

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result and "list" in result["data"]:
            ref_list = result["data"]["list"]
            logger.info(f"[SUCCESS] Total {len(ref_list)} reference audios (valid for 24h)")
    except Exception as e:
        logger.error(f"Failed to list reference audios: {str(e)}")
        sys.exit(1)


def delete_tts_reference(emotion_path: str) -> None:
    """
    删除参考音频（POST /api/third/tts/deleteCustom）
    :param emotion_path: 参考音频名称（从 list-tts-references 获取）
    """
    if not emotion_path:
        logger.error("Error: emotionPath is required")
        sys.exit(1)

    try:
        data = {"emotionPath": emotion_path}
        result = api_request('POST', '/api/third/tts/deleteCustom', data=data)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0:
            logger.info(f"[SUCCESS] Reference audio {emotion_path} deleted")
    except Exception as e:
        logger.error(f"Failed to delete reference audio: {str(e)}")
        sys.exit(1)


def tts_create(
    content: str,
    audio_id: str,
    style: str = "1",
    speed: float = 1.0,
    genre: int = 0,
    emotion: Optional[Dict] = None,
    emotion_path: Optional[str] = None
) -> None:
    """
    异步语音合成（POST /api/third/tts/create）
    :param content: 文本内容（必需，最大 5000 字符）
    :param audio_id: 模型 ID（必需）
    :param style: 模型版本（必需，1:基础 2:专业 3:多语言）
    :param speed: 语速（可选，0.5-1.5，默认 1.0）
    :param genre: 模型类别（可选）
                 0=参考原音频（默认，支持所有模型）
                 1=语气参考模式（仅专业模型，使用 ext 情感参数）
                 2=使用参考音频（仅专业模型，需要 emotionPath）
    :param emotion: 情感参数（可选，仅 genre=1 时生效）
    :param emotion_path: 参考音频路径（可选，仅 genre=2 时必需）
    """
    if not content or not audio_id:
        logger.error("Error: content and audioId are required")
        sys.exit(1)
    if len(content) > 5000:
        logger.error("Error: content exceeds max length of 5000 characters")
        sys.exit(1)
    if not (0.5 <= speed <= 1.5):
        logger.error("Error: speed must be between 0.5 and 1.5")
        sys.exit(1)
    style = str(style)
    if style not in ["1", "2", "3"]:
        logger.error("Error: style must be 1(basic), 2(pro), or 3(multilingual)")
        sys.exit(1)

    # genre=2 时必须提供 emotionPath
    if genre == 2 and not emotion_path:
        logger.error("Error: emotionPath is required when genre=2")
        sys.exit(1)

    # 构造请求体（按文档要求）
    data = {
        "content": content,
        "audioId": audio_id,
        "style": style,
        "speed": speed,
        "genre": genre
    }

    # genre=1: 使用情感参数（ext）
    if genre == 1 and emotion:
        data["ext"] = emotion

    # genre=2: 使用参考音频（需要 emotionPath 和 style=2）
    if genre == 2:
        if style != "2":
            logger.warning("Warning: genre=2 requires style=2 (pro model), auto-adjusting")
            data["style"] = "2"
        data["emotionPath"] = emotion_path

    try:
        result = api_request('POST', '/api/third/tts/create', data=data)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result:
            logger.info(f"[SUCCESS] TTS task submitted! taskId: {result['data'].get('taskId')}")
            logger.info("Note: Generated audio expires in 24 hours")
    except Exception as e:
        logger.error(f"Failed to submit TTS task: {str(e)}")
        sys.exit(1)


def tts_list(page: int = 1, page_size: int = 10) -> None:
    """
    语音合成列表查询（GET /api/third/tts/list）
    :param page: 页码（可选，默认 1）
    :param page_size: 每页条数（可选，默认 10，最大 20）
    """
    if page_size > 20:
        logger.warning("Warning: pageSize max is 20, adjusted to 20")
        page_size = 20

    params = {"page": str(page), "pageSize": str(page_size)}
    try:
        result = api_request('GET', '/api/third/tts/list', params=params)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result and "list" in result["data"]:
            logger.info(f"[SUCCESS] Total {result['data'].get('total', 0)} tasks, page {page}")
    except Exception as e:
        logger.error(f"Failed to list TTS tasks: {str(e)}")
        sys.exit(1)


def tts_result(task_id: str) -> None:
    """
    查询 taskID 结果（GET /api/third/tts/result）
    :param task_id: 任务 ID（必需，从 tts-create 获取）
    """
    if not task_id:
        logger.error("Error: taskId is required")
        sys.exit(1)

    params = {"taskId": task_id}
    try:
        result = api_request('GET', '/api/third/tts/result', params=params)

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result:
            # API returns 'voiceUrl' not 'audioUrl'
            if "voiceUrl" in result["data"] and result["data"]["voiceUrl"]:
                logger.info(f"[SUCCESS] Task completed! Download URL: {result['data']['voiceUrl']}")
                logger.info("Note: Add 'sign' header when downloading")
            elif "status" in result["data"]:
                status = result['data']['status']
                status_text = {1: "Processing", 2: "Completed", 3: "Failed"}.get(status, f"Unknown({status})")
                logger.info(f"[INFO] Task status: {status_text}, please retry later")
    except Exception as e:
        logger.error(f"Failed to get task result: {str(e)}")
        sys.exit(1)


def tts_download(task_id: str, output_path: str) -> None:
    """
    下载合成音频（GET /api/third/tts/result + 下载）
    :param task_id: 任务 ID（必需）
    :param output_path: 输出文件路径（必需）
    """
    if not task_id:
        logger.error("Error: taskId is required")
        sys.exit(1)
    if not output_path:
        logger.error("Error: output_path is required")
        sys.exit(1)

    # 先获取下载链接
    params = {"taskId": task_id}
    try:
        result = api_request('GET', '/api/third/tts/result', params=params)
        
        if result.get("code") != 0:
            logger.error(f"Error: Failed to get task result: {result.get('msg', 'Unknown error')}")
            sys.exit(1)
        
        # API returns 'voiceUrl' not 'audioUrl'
        if "data" not in result or "voiceUrl" not in result["data"]:
            logger.error("Error: Task not completed or no audio URL available")
            sys.exit(1)
        
        audio_url = result["data"]["voiceUrl"]
        logger.info(f"Downloading from: {audio_url}")
        
        # 下载音频文件 (支持 header 或 URL params 传递 sign)
        # API 文档要求：header 必须传递 sign，或者把 sign 拼接在 URL 的 params 上
        download_headers = {"sign": API_SIGN}
        
        # 如果 URL 已有 sign 参数，不需要重复添加
        if "?sign=" not in audio_url and "&sign=" not in audio_url:
            # 也可以直接拼接 sign 到 URL（某些下载器可能不支持 header）
            audio_url_with_sign = f"{audio_url}{'&' if '?' in audio_url else '?'}sign={API_SIGN}"
            logger.debug(f"Download URL with sign: {audio_url_with_sign}")
        
        download_response = session.get(audio_url, headers=download_headers, timeout=TIMEOUT)
        download_response.raise_for_status()
        
        # 保存到文件
        output_file = Path(output_path).resolve()
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'wb') as f:
            f.write(download_response.content)
        
        logger.info(f"[SUCCESS] Audio saved to: {output_file}")
        
    except Exception as e:
        logger.error(f"Failed to download audio: {str(e)}")
        sys.exit(1)


# ========== 用户配额相关接口 ==========
# 注意：配额查询接口可能未开放，如返回 404 请使用网页版查看

def get_quota() -> None:
    """
    查询用户配额（GET /api/third/user/quota）
    返回剩余字符额度等信息
    注意：此接口可能未在所有账户中开放
    """
    try:
        result = api_request('GET', '/api/third/user/quota', params={})

        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("code") == 0 and "data" in result:
            logger.info("[SUCCESS] Quota retrieved")
        elif result.get("code") == 404:
            logger.warning("[WARNING] Quota endpoint not available, check via web dashboard")
    except Exception as e:
        logger.error(f"Failed to get quota: {str(e)}")
        sys.exit(1)


# ========== 主函数（命令行入口） ==========

def main():
    validate_config()

    parser = argparse.ArgumentParser(
        description='IndexTTS API CLI Tool (Compatible with Windows)',
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')

    # 1. 模型创建
    create_parser = subparsers.add_parser('create-model', help='Create a voice clone model')
    create_parser.add_argument('model_name', help='Model name (required)')
    create_parser.add_argument('file_path', help='Audio file path (mp3/wav/m4a, <50MB, 2-60s, required)')
    create_parser.add_argument('--describe', help='Model description (optional)')

    # 2. 模型列表获取
    list_parser = subparsers.add_parser('list-models', help='List all voice models')
    list_parser.add_argument('--page', type=int, default=1, help='Page number (default: 1)')
    list_parser.add_argument('--page-size', type=int, default=10, help='Items per page (default: 10, max: 20)')

    # 3. 模型详情查询
    detail_parser = subparsers.add_parser('get-model', help='Get model details by audioId')
    detail_parser.add_argument('audio_id', help='Model ID (audioId, required)')

    # 4. 删除模型数据
    delete_parser = subparsers.add_parser('delete-model', help='Delete a model (cannot be undone)')
    delete_parser.add_argument('audio_id', help='Model ID (audioId, required)')

    # 5. 异步语音合成
    tts_parser = subparsers.add_parser('tts-create', help='Submit an async TTS task')
    tts_parser.add_argument('content', help='Text content to synthesize (max 5000 chars, required)')
    tts_parser.add_argument('audio_id', help='Model ID (audioId, required)')
    tts_parser.add_argument('--style', type=str, default="1", help='Model version: 1=basic(default) 2=pro 3=multilingual')
    tts_parser.add_argument('--speed', type=float, default=1.0, help='Speech speed: 0.5-1.5 (default: 1.0)')
    tts_parser.add_argument('--genre', type=int, default=0, help='Genre: 0=original(default) 1=emotion params 2=reference audio')
    tts_parser.add_argument('--emotion-path', type=str, default=None, help='Reference audio path (emotionPath, required for genre=2)')
    tts_parser.add_argument('--happy', type=float, default=0, help='Happiness level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--angry', type=float, default=0, help='Anger level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--sad', type=float, default=0, help='Sadness level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--afraid', type=float, default=0, help='Fear level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--disgusted', type=float, default=0, help='Disgust level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--melancholic', type=float, default=0, help='Melancholy level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--surprised', type=float, default=0, help='Surprise level (0-1, default: 0, genre=1 only)')
    tts_parser.add_argument('--calm', type=float, default=0, help='Calmness level (0-1, default: 0, genre=1 only)')

    # 6. 语音合成列表查询
    tts_list_parser = subparsers.add_parser('tts-list', help='List TTS tasks')
    tts_list_parser.add_argument('--page', type=int, default=1, help='Page number (default: 1)')
    tts_list_parser.add_argument('--page-size', type=int, default=10, help='Items per page (default: 10, max: 20)')

    # 7. 查询 taskID 结果
    tts_result_parser = subparsers.add_parser('tts-result', help='Get TTS task result by taskId')
    tts_result_parser.add_argument('task_id', help='Task ID (taskId, required)')

    # 8. 下载合成音频
    tts_download_parser = subparsers.add_parser('tts-download', help='Download synthesized audio')
    tts_download_parser.add_argument('task_id', help='Task ID (taskId, required)')
    tts_download_parser.add_argument('output_path', help='Output file path (required)')

    # 9. 查询用户配额
    quota_parser = subparsers.add_parser('quota', help='Check user quota/remaining credits')

    # 10. 上传参考音频（用于情感合成）
    ref_upload_parser = subparsers.add_parser('upload-tts-reference', help='Upload reference audio for emotion TTS (valid 24h)')
    ref_upload_parser.add_argument('file_path', help='Audio file path (mp3/wav/m4a, <50MB, required)')

    # 11. 参考音频列表
    ref_list_parser = subparsers.add_parser('list-tts-references', help='List uploaded reference audios (valid 24h)')

    # 12. 删除参考音频
    ref_delete_parser = subparsers.add_parser('delete-tts-reference', help='Delete a reference audio')
    ref_delete_parser.add_argument('emotion_path', help='Reference audio name (emotionPath, required)')

    args = parser.parse_args()

    try:
        if args.command == 'create-model':
            create_model(args.model_name, args.file_path, args.describe)
        elif args.command == 'list-models':
            list_models(args.page, args.page_size)
        elif args.command == 'get-model':
            get_model_detail(args.audio_id)
        elif args.command == 'delete-model':
            delete_model(args.audio_id)
        elif args.command == 'tts-create':
            emotion = {
                "happy": args.happy,
                "angry": args.angry,
                "sad": args.sad,
                "afraid": args.afraid,
                "disgusted": args.disgusted,
                "melancholic": args.melancholic,
                "surprised": args.surprised,
                "calm": args.calm
            }
            tts_create(args.content, args.audio_id, args.style, args.speed, args.genre, emotion, args.emotion_path)
        elif args.command == 'tts-list':
            tts_list(args.page, args.page_size)
        elif args.command == 'tts-result':
            tts_result(args.task_id)
        elif args.command == 'tts-download':
            tts_download(args.task_id, args.output_path)
        elif args.command == 'quota':
            get_quota()
        elif args.command == 'upload-tts-reference':
            create_tts_reference(args.file_path)
        elif args.command == 'list-tts-references':
            list_tts_references()
        elif args.command == 'delete-tts-reference':
            delete_tts_reference(args.emotion_path)
    except KeyboardInterrupt:
        logger.info("\n[INFO] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()
