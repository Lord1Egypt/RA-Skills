"""Optional, local-only faster-whisper transcription. ASR is not listening."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path

from workspace import (DEFAULT_ROOT, Workspace, configure_console, inside, now,
                       reject_link_chain, write_json_new, write_text_new)


def srt_time(seconds):
    milliseconds = max(0, round(float(seconds) * 1000))
    hours, remainder = divmod(milliseconds, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    seconds, milliseconds = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def transcribe(workspace, args):
    source = inside(workspace.root, args.input)
    if not source.is_file():
        raise ValueError("--input 必须是工作区内一个实际存在的文件")
    model_path = Path(args.model)
    model_path = reject_link_chain(model_path if model_path.is_absolute() else workspace.root / model_path)
    if not model_path.is_dir():
        raise ValueError("--model 必须是已有的本地 faster-whisper 模型目录；本工具不会下载模型")
    for filename in ("model.bin", "config.json", "tokenizer.json"):
        file = reject_link_chain(model_path / filename)
        if not file.is_file():
            raise ValueError(f"本地模型缺少 {filename}；请自行准备完整模型。本工具不会联网补齐")
    target = workspace.output(args.out)
    # Offline flags affect this process only. A local tokenizer is required above
    # because otherwise some package versions may try to retrieve it separately.
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("未安装可选依赖 faster-whisper；请按工具命令文档安装后重试") from exc
    model = WhisperModel(str(model_path), device=args.device, compute_type=args.compute_type, local_files_only=True)
    # Reserve a new version only after model loading succeeds.
    target.mkdir(parents=True, exist_ok=False)
    result = {"schema_version": 1, "created_at": now(), "source": workspace.relative(source), "model_directory_name": model_path.name, "faster_whisper_version": importlib.metadata.version("faster-whisper"), "device_requested": args.device, "compute_type": args.compute_type, "language_requested": args.language, "vad_filter": args.vad_filter, "status": "started", "listening_status": "not_listened", "reviewed": False, "subtitle_status": "machine_draft_requires_listening", "segments": [], "warnings": ["ASR 不是实际试听；风声、音乐、重叠说话或静音可能导致漏字与幻觉，字幕需逐句听音核对。"]}
    try:
        segments, info = model.transcribe(str(source), language=None if args.language == "auto" else args.language, vad_filter=args.vad_filter, beam_size=5)
        result["detected_language"] = info.language
        result["language_probability"] = info.language_probability
        result["duration_seconds"] = info.duration
        for segment in segments:
            result["segments"].append({"id": segment.id, "start": segment.start, "end": segment.end, "text": segment.text.strip(), "avg_logprob": segment.avg_logprob, "no_speech_prob": segment.no_speech_prob, "compression_ratio": segment.compression_ratio, "listening_status": "not_listened", "reviewed": False})
        result["status"] = "transcribed_not_listened"
    except Exception as exc:
        result["status"] = "failed_partial_transcription"
        result["error"] = str(exc)
        write_json_new(target / "transcript.json", result)
        raise RuntimeError(f"转写失败；已保存部分记录：{workspace.relative(target / 'transcript.json')}；{exc}") from exc
    blocks = []
    for index, segment in enumerate(result["segments"], 1):
        text = segment["text"].replace("\r", " ").replace("\n", " ")
        blocks.append(f"{index}\n{srt_time(segment['start'])} --> {srt_time(segment['end'])}\n{text}\n")
    write_text_new(target / "transcript.srt", "\n".join(blocks))
    write_json_new(target / "transcript.json", result)
    return {"json": workspace.relative(target / "transcript.json"), "srt": workspace.relative(target / "transcript.srt"), "segment_count": len(result["segments"]), "listening_status": "not_listened", "reviewed": False}


def main():
    configure_console()
    parser = argparse.ArgumentParser(description="可选本地 ASR；只使用已有本地模型，不下载，不代表试听")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--input", required=True, help="工作区内的单个音频或视频文件")
    parser.add_argument("--model", required=True, help="完整本地 faster-whisper 模型目录；相对路径基于工作区")
    parser.add_argument("--out", required=True, help="工作区内新的输出目录，不能在素材中")
    parser.add_argument("--language", default="zh", help="语言代码，例如 zh；auto 为自动识别")
    parser.add_argument("--device", choices=("cpu", "cuda", "auto"), default="cpu")
    parser.add_argument("--compute-type", default="int8", help="默认 CPU int8；请选已安装运行时支持的类型")
    parser.add_argument("--vad-filter", action="store_true", help="启用可选 VAD；默认关闭，不能替代听音核对")
    args = parser.parse_args()
    try:
        result = transcribe(Workspace(args.root), args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, RuntimeError) as exc:
        parser.exit(1, f"错误：{exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
