#!/usr/bin/env python3
"""
MLX Whisper 转录 + 翻译本地后端服务器

功能：
- 分块转录音频文件（mlx_whisper），支持进度查询
- 本地 LLM 翻译（mlx-lm / Qwen2.5）
- 文件上传或本地路径两种方式
"""

import os
import sys
import json
import time
import uuid
import asyncio
import subprocess
import threading
import tempfile
import shutil
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional, Dict, Any, List
from aiohttp import web

# ─── 音频格式转换 ─────────────────────────────────────────

# soundfile 支持读写的格式（不含 mp3/m4a/aac）
SF_SUPPORTED = {'.wav', '.flac', '.ogg', '.opus', '.aiff', '.aif', '.au', '.raw', '.paf', '.svx', '.nist', '.voc', '.ircam', '.w64', '.mat4', '.mat5', '.pvf', '.xi', '.htk', '.sds', '.avr', '.wavex', '.sd2', '.caf'}

def ensure_wav(audio_path: str) -> str:
    """如果音频格式不被 soundfile 支持（如 m4a/mp3），用 afconvert 转为 WAV。
    返回临时 WAV 路径或原始路径（如果格式已支持）。"""
    ext = Path(audio_path).suffix.lower()
    if ext in SF_SUPPORTED:
        return audio_path

    # 用 macOS 内置 afconvert 转换
    tmp_wav = tempfile.mktemp(suffix=".wav")
    try:
        subprocess.run(
            ["afconvert", "-f", "WAVE", "-d", "LEI16", audio_path, tmp_wav],
            check=True, capture_output=True, text=True,
        )
        return tmp_wav
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"音频格式转换失败 ({ext})：{e.stderr.strip() if e.stderr else e}")

def cleanup_wav(wav_path: str, original_path: str):
    """如果 wav_path 是临时转换文件，删除它"""
    if wav_path != original_path and os.path.exists(wav_path):
        try:
            os.unlink(wav_path)
        except OSError:
            pass

# ─── 全局状态 ────────────────────────────────────────────

# 转录任务存储
tasks_store: Dict[str, Dict[str, Any]] = {}

# 翻译模型缓存
_translate_model = None
_translate_tokenizer = None
_translate_model_id: Optional[str] = None

# 上传文件临时目录
UPLOAD_DIR = tempfile.mkdtemp(prefix="whisper_upload_")

# 脚本所在目录 → 项目根目录 → models/ 目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
MODELS_DIR = os.path.join(PROJECT_DIR, "models")

# 默认 Whisper 模型路径（项目内 models/whisper-large-v3-turbo）
DEFAULT_WHISPER_MODEL = os.path.join(MODELS_DIR, "whisper-large-v3-turbo")

# 默认翻译模型路径（项目内 models/Qwen2.5-3B-Instruct-4bit）
DEFAULT_TRANSLATE_MODEL = os.path.join(MODELS_DIR, "Qwen2.5-3B-Instruct-4bit")

# Whisper 模型缓存
_whisper_model_cache: Dict[str, Any] = {}

# 可用翻译模型列表（项目内本地路径）
AVAILABLE_TRANSLATE_MODELS = [
    {"id": os.path.join(MODELS_DIR, "Qwen2.5-3B-Instruct-4bit"), "name": "Qwen2.5-3B (4-bit, 推荐)", "size": "~2GB"},
    {"id": os.path.join(MODELS_DIR, "Qwen2.5-7B-Instruct-4bit"), "name": "Qwen2.5-7B (4-bit, 更高质量)", "size": "~4GB"},
    {"id": os.path.join(MODELS_DIR, "Qwen2.5-1.5B-Instruct-4bit"), "name": "Qwen2.5-1.5B (4-bit, 最快)", "size": "~1GB"},
]

# 语言名称映射
LANGUAGE_NAMES = {
    "ja": "日语", "zh": "中文", "en": "英语", "ko": "韩语",
    "fr": "法语", "de": "德语", "es": "西班牙语", "ru": "俄语",
    "pt": "葡萄牙语", "it": "意大利语", "ar": "阿拉伯语",
    "hi": "印地语", "th": "泰语", "vi": "越南语",
    "nl": "荷兰语", "pl": "波兰语", "sv": "瑞典语", "tr": "土耳其语",
}


# ─── 工具函数 ────────────────────────────────────────────

def fmt_srt_time(seconds: float) -> str:
    """格式化秒数为 SRT 时间格式 HH:MM:SS,mmm"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int(round((seconds - int(seconds)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def get_chunk_start(chunk_idx: int, chunk_sec: int, overlap_sec: int) -> float:
    """计算第 N 个 chunk 在完整音频中的起始时间（秒）"""
    effective_step = chunk_sec - overlap_sec
    return chunk_idx * effective_step


# ─── 转录核心逻辑 ──────────────────────────────────────

def run_transcription(task_id: str):
    """在后台线程中运行分块转录"""
    task = tasks_store.get(task_id)
    if not task:
        return

    try:
        from mlx_whisper import transcribe as whisper_transcribe

        audio_path = task["file_path"]
        model_path = task["model"]
        language = task["language"]
        chunk_sec = task["chunk_sec"]
        overlap_sec = task["overlap_sec"]

        # 格式转换：m4a/mp3 等格式用 afconvert 转为 WAV
        task["status"] = "loading"
        wav_path = ensure_wav(audio_path)

        # 读取音频信息
        info = sf.info(wav_path)
        sr = info.samplerate
        total_frames = info.frames
        total_dur = total_frames / sr

        effective_step = chunk_sec - overlap_sec
        total_chunks = max(1, int(np.ceil(total_dur / effective_step)))

        task["duration"] = total_dur
        task["total_chunks"] = total_chunks
        task["skipped_chunk_indexes"] = []

        all_segments = []
        seg_counter = 0

        for chunk_idx in range(total_chunks):
            if task.get("cancelled"):
                task["status"] = "cancelled"
                return

            chunk_start = get_chunk_start(chunk_idx, chunk_sec, overlap_sec)
            chunk_end = min(chunk_start + chunk_sec, total_dur)

            if chunk_start >= total_dur:
                break

            # 加载该 chunk 的音频
            start_frame = int(chunk_start * sr)
            end_frame = int(chunk_end * sr)

            try:
                data, _ = sf.read(wav_path, dtype="float32", start=start_frame, stop=end_frame)
                if data.ndim > 1:
                    data = data.mean(axis=1)
            except Exception as e:
                print(f"[WARN] Chunk {chunk_idx+1}/{total_chunks}: 读取失败 - {e}")
                task["skipped_chunk_indexes"].append(chunk_idx)
                task["current_chunk"] = chunk_idx + 1
                task["skipped_chunks"] = len(task["skipped_chunk_indexes"])
                continue

            # 转录该 chunk
            try:
                result = whisper_transcribe(
                    data.astype(np.float32),
                    path_or_hf_repo=model_path,
                    language=language if language != "auto" else None,
                    temperature=0.0,
                    condition_on_previous_text=False,
                    word_timestamps=True,
                    verbose=False,
                )
            except Exception as e:
                print(f"[WARN] Chunk {chunk_idx+1}/{total_chunks}: 转录失败 - {e}")
                task["skipped_chunk_indexes"].append(chunk_idx)
                task["current_chunk"] = chunk_idx + 1
                task["skipped_chunks"] = len(task["skipped_chunk_indexes"])
                del data
                import gc; gc.collect()
                continue

            segs = result.get("segments", [])

            # 计算 chunk 的有效范围（排除重叠区域）
            if chunk_idx == 0:
                effective_start = 0.0
            else:
                effective_start = chunk_start + overlap_sec

            if chunk_idx == total_chunks - 1:
                effective_end = total_dur
            else:
                effective_end = chunk_start + effective_step

            # 将该 chunk 的段添加到全局列表，只保留有效范围内的段
            for seg in segs:
                text = seg["text"].strip()
                if not text:
                    continue

                # 段的时间戳是相对于 chunk 开始的，需要加上偏移
                global_start = seg["start"] + chunk_start
                global_end = seg["end"] + chunk_start

                # 只保留有效范围内的段（避免重复）
                if global_start < effective_start - 0.5:
                    continue
                if global_start >= effective_end + 0.5:
                    continue

                seg_counter += 1
                all_segments.append({
                    "index": seg_counter,
                    "startTime": round(global_start, 2),
                    "endTime": round(global_end, 2),
                    "text": text,
                })

            # 更新进度
            task["current_chunk"] = chunk_idx + 1
            task["progress"] = min(99, int((chunk_idx + 1) / total_chunks * 100))
            task["segments"] = all_segments

            print(f"[INFO] Chunk {chunk_idx+1}/{total_chunks}: "
                  f"{len(segs)} segments, effective [{effective_start:.0f}-{effective_end:.0f}s], "
                  f"total {len(all_segments)} segments")

            del data, result
            import gc; gc.collect()

        # 转录完成
        task["status"] = "completed"
        task["progress"] = 100
        task["segments"] = all_segments
        task["completed_at"] = time.time()
        cleanup_wav(wav_path, audio_path)
        print(f"[DONE] Task {task_id}: {len(all_segments)} segments, "
              f"skipped {len(task['skipped_chunk_indexes'])} chunks")

    except Exception as e:
        print(f"[ERROR] Task {task_id}: {e}")
        import traceback
        traceback.print_exc()
        task["status"] = "failed"
        task["error"] = str(e)
        try:
            cleanup_wav(wav_path if 'wav_path' in dir() else audio_path, audio_path)
        except Exception:
            pass


# ─── 翻译核心逻辑 ──────────────────────────────────────

def load_translate_model(model_id: str):
    """加载翻译模型（lazy load）"""
    global _translate_model, _translate_tokenizer, _translate_model_id

    if _translate_model and _translate_model_id == model_id:
        return _translate_model, _translate_tokenizer

    print(f"[INFO] Loading translate model: {model_id}...")
    import mlx_lm
    model, tokenizer = mlx_lm.load(model_id)
    _translate_model = model
    _translate_tokenizer = tokenizer
    _translate_model_id = model_id
    print(f"[INFO] Translate model loaded: {model_id}")
    return model, tokenizer


def do_translate(segments: List[Dict], source_language: str, target_language: str, model_id: str) -> List[Dict]:
    """执行翻译"""
    import mlx_lm

    model, tokenizer = load_translate_model(model_id)

    src_name = LANGUAGE_NAMES.get(source_language, source_language)
    tgt_name = LANGUAGE_NAMES.get(target_language, target_language)

    # 将所有文本拼接成批量翻译 prompt
    lines = []
    for i, seg in enumerate(segments):
        lines.append(f"第{i+1}行：{seg['text']}")

    user_msg = (
        f"请将以下文本从{src_name}翻译为{tgt_name}。"
        f"保持原文的行数和顺序，每行对应一条翻译结果，不要添加序号或额外说明：\n\n"
        + "\n".join(lines)
    )

    # 构建 chat prompt
    messages = [
        {"role": "system", "content": "你是一个专业的翻译助手。请将用户提供的文本准确翻译为目标语言，只输出翻译结果，不要添加解释或额外内容。"},
        {"role": "user", "content": user_msg},
    ]

    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

    result = mlx_lm.generate(
        model, tokenizer, prompt,
        max_tokens=4096,
        verbose=False,
    )

    # 解析翻译结果
    translated_lines = []
    for line in result.strip().split("\n"):
        line = line.strip()
        # 去掉可能的 "第N行：" 前缀
        if line.startswith("第") and "行：" in line:
            line = line.split("行：", 1)[1].strip()
        elif line.startswith("第") and "行:" in line:
            line = line.split("行:", 1)[1].strip()
        if line:
            translated_lines.append(line)

    # 匹配回各 segment
    translated_segments = []
    for i, seg in enumerate(segments):
        translated_text = translated_lines[i] if i < len(translated_lines) else seg["text"]
        translated_segments.append({
            **seg,
            "translatedText": translated_text,
        })

    return translated_segments


# ─── HTTP 路由 ──────────────────────────────────────────

async def health_handler(request: web.Request) -> web.Response:
    """健康检查"""
    return web.json_response({
        "status": "ok",
        "whisper_model": DEFAULT_WHISPER_MODEL,
        "translate_model_loaded": _translate_model is not None,
        "translate_model": _translate_model_id,
    })


async def models_handler(request: web.Request) -> web.Response:
    """返回可用翻译模型列表"""
    return web.json_response({"models": AVAILABLE_TRANSLATE_MODELS})


async def upload_handler(request: web.Request) -> web.Response:
    """上传音频文件"""
    reader = await request.multipart()
    field = await reader.next()
    if not field or not field.filename:
        return web.json_response({"error": "No file uploaded"}, status=400)

    # 保存到临时目录
    suffix = Path(field.filename).suffix or ".wav"
    temp_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}{suffix}")
    with open(temp_path, "wb") as f:
        while True:
            chunk = await field.read_chunk(8192)
            if not chunk:
                break
            f.write(chunk)

    return web.json_response({
        "file_path": temp_path,
        "file_name": field.filename,
        "file_size": os.path.getsize(temp_path),
    })


async def transcribe_handler(request: web.Request) -> web.Response:
    """启动转录任务"""
    body = await request.json()

    file_path = body.get("file_path")
    if not file_path or not os.path.isfile(file_path):
        return web.json_response({"error": "file_path 不存在"}, status=400)

    model = body.get("model") or DEFAULT_WHISPER_MODEL
    language = body.get("language", "auto")
    chunk_sec = int(body.get("chunk_sec", 150))
    overlap_sec = int(body.get("overlap_sec", 20))

    # 创建任务
    task_id = uuid.uuid4().hex[:12]
    tasks_store[task_id] = {
        "id": task_id,
        "file_path": file_path,
        "file_name": os.path.basename(file_path),
        "model": model,
        "language": language,
        "chunk_sec": chunk_sec,
        "overlap_sec": overlap_sec,
        "status": "queued",
        "progress": 0,
        "current_chunk": 0,
        "total_chunks": 0,
        "skipped_chunks": 0,
        "skipped_chunk_indexes": [],
        "segments": [],
        "duration": 0,
        "error": None,
        "cancelled": False,
        "created_at": time.time(),
        "completed_at": None,
    }

    # 在后台线程中运行转录
    loop = asyncio.get_event_loop()
    thread = threading.Thread(target=run_transcription, args=(task_id,), daemon=True)
    thread.start()

    return web.json_response({"task_id": task_id})


async def task_status_handler(request: web.Request) -> web.Response:
    """查询任务状态"""
    task_id = request.match_info["task_id"]
    task = tasks_store.get(task_id)
    if not task:
        return web.json_response({"error": "Task not found"}, status=404)

    # 不返回文件路径等敏感信息
    response = {
        "id": task["id"],
        "file_name": task["file_name"],
        "model": task["model"],
        "language": task["language"],
        "chunk_sec": task["chunk_sec"],
        "overlap_sec": task["overlap_sec"],
        "status": task["status"],
        "progress": task["progress"],
        "current_chunk": task["current_chunk"],
        "total_chunks": task["total_chunks"],
        "skipped_chunks": task["skipped_chunks"],
        "skipped_chunk_indexes": task["skipped_chunk_indexes"],
        "segments": task["segments"],
        "duration": task["duration"],
        "error": task["error"],
        "completed_at": task["completed_at"],
    }
    return web.json_response(response)


async def cancel_task_handler(request: web.Request) -> web.Response:
    """取消任务"""
    task_id = request.match_info["task_id"]
    task = tasks_store.get(task_id)
    if not task:
        return web.json_response({"error": "Task not found"}, status=404)

    task["cancelled"] = True
    task["status"] = "cancelled"
    return web.json_response({"status": "cancelled"})


async def translate_handler(request: web.Request) -> web.Response:
    """翻译接口"""
    body = await request.json()

    segments = body.get("segments", [])
    if not segments:
        return web.json_response({"error": "No segments provided"}, status=400)

    source_language = body.get("source_language", "ja")
    target_language = body.get("target_language", "zh")
    model_id = body.get("model") or DEFAULT_TRANSLATE_MODEL

    try:
        # 在线程池中执行翻译（mlx-lm 是阻塞的）
        loop = asyncio.get_event_loop()
        translated = await loop.run_in_executor(
            None, do_translate, segments, source_language, target_language, model_id
        )
        return web.json_response({"translated_segments": translated})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return web.json_response({"error": str(e)}, status=500)


# ─── CORS 中间件 ────────────────────────────────────────

@web.middleware
async def cors_middleware(request: web.Request, handler):
    """CORS 中间件，允许前端跨域访问"""
    if request.method == "OPTIONS":
        response = web.Response(status=204)
    else:
        response = await handler(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# ─── 启动服务器 ────────────────────────────────────────

def create_app() -> web.Application:
    app = web.Application(middlewares=[cors_middleware])
    app.router.add_get("/api/health", health_handler)
    app.router.add_get("/api/models", models_handler)
    app.router.add_post("/api/upload", upload_handler)
    app.router.add_post("/api/transcribe", transcribe_handler)
    app.router.add_get("/api/tasks/{task_id}", task_status_handler)
    app.router.add_post("/api/tasks/{task_id}/cancel", cancel_task_handler)
    app.router.add_post("/api/translate", translate_handler)
    return app


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    print(f"╔══════════════════════════════════════════╗")
    print(f"║  MLX Whisper 转录 + 翻译服务器          ║")
    print(f"║  http://localhost:{port:<5}                  ║")
    print(f"║  默认模型: whisper-large-v3-turbo       ║")
    print(f"║  翻译模型: Qwen2.5-3B-Instruct-4bit     ║")
    print(f"╚══════════════════════════════════════════╝")
    web.run_app(create_app(), host="0.0.0.0", port=port, print=None)
