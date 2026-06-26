#!/usr/bin/env python3
"""
audio_transcriber.py — 音频转录工具

将音频文件转为带时间戳的文字，供追忆分析和人格档案使用。

支持格式：mp3 / m4a / wav / ogg / flac / aac
典型来源：微信语音消息、生前访谈录音、家庭录音、电话录音

依赖：
  pip install openai-whisper
  （首次运行会自动下载所选模型，small 约 244MB，建议中文使用 small 或 medium）

用法：
  # 单个文件
  python audio_transcriber.py --file interview.m4a --speaker "爷爷"

  # 批量处理目录（微信语音导出场景）
  python audio_transcriber.py --dir ./voice_messages/ --speaker "爷爷" --format chat

  # 访谈录音（完整转录 + 分析提示）
  python audio_transcriber.py --file interview.mp3 --speaker "奶奶" --mode interview

  # 指定模型大小（默认 small，medium 准确率更高但慢）
  python audio_transcriber.py --file audio.mp3 --model medium
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


SUPPORTED_FORMATS = {".mp3", ".m4a", ".wav", ".ogg", ".flac", ".aac", ".wma", ".opus"}

# Whisper 模型选项说明
MODEL_INFO = {
    "tiny":   "最快，准确率较低，适合快速预览",
    "base":   "较快，基础准确率",
    "small":  "推荐默认，速度与准确率均衡（约 244MB）",
    "medium": "准确率更高，适合重要访谈（约 769MB）",
    "large":  "最高准确率，较慢（约 1550MB）",
}


# ── Whisper 加载 ──────────────────────────────────────────────────────────────

def load_whisper(model_name: str):
    """加载 Whisper 模型，未安装时给出明确提示。"""
    try:
        import whisper
        print(f"[加载] Whisper 模型：{model_name}（首次运行需下载）")
        return whisper.load_model(model_name)
    except ImportError:
        print(
            "\n[错误] 未安装 openai-whisper。\n"
            "请先运行：pip install openai-whisper\n"
            "（如需 GPU 加速，还需安装 torch：pip install torch）\n"
        )
        sys.exit(1)


# ── 转录 ──────────────────────────────────────────────────────────────────────

def transcribe_file(model, filepath: str, language: str = "zh") -> dict:
    """
    转录单个音频文件。
    返回 {text, segments, language, duration}
    """
    print(f"[转录] {os.path.basename(filepath)} ...")
    result = model.transcribe(
        filepath,
        language=language if language != "auto" else None,
        task="transcribe",
        verbose=False,
    )
    return {
        "text": result["text"].strip(),
        "segments": result.get("segments", []),
        "language": result.get("language", language),
        "duration": result["segments"][-1]["end"] if result.get("segments") else 0,
    }


def transcribe_directory(model, dirpath: str, language: str = "zh") -> list[dict]:
    """批量转录目录下所有音频文件，按文件名排序。"""
    files = sorted([
        os.path.join(dirpath, f)
        for f in os.listdir(dirpath)
        if Path(f).suffix.lower() in SUPPORTED_FORMATS
    ])
    if not files:
        print(f"[警告] 目录中没有支持的音频文件：{dirpath}")
        return []

    print(f"[扫描] 找到 {len(files)} 个音频文件")
    results = []
    for f in files:
        try:
            result = transcribe_file(model, f, language)
            result["filename"] = os.path.basename(f)
            results.append(result)
        except Exception as e:
            print(f"[跳过] {os.path.basename(f)}：{e}")
    return results


# ── 格式化输出 ────────────────────────────────────────────────────────────────

def format_single_transcript(result: dict, speaker: str, mode: str) -> str:
    """格式化单文件转录结果。"""
    filename = result.get("filename", "audio")
    duration = result.get("duration", 0)
    lang = result.get("language", "zh")

    lines = [
        f"# {speaker} 的音频转录",
        "",
        f"**文件**：{filename}",
        f"**时长**：{_fmt_duration(duration)}",
        f"**检测语言**：{lang}",
        f"**转录时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
    ]

    if mode == "interview":
        lines += _format_interview(result, speaker)
    else:
        lines += _format_plain(result, speaker)

    lines += [
        "",
        "---",
        f"*本转录由 Whisper 自动生成，可能存在误字，请校对后使用。*",
        f"*转录内容标注为 [本人口述] 或 [音频转录] 后可上传至纪念档案。*",
    ]
    return "\n".join(lines)


def format_batch_transcript(results: list[dict], speaker: str, fmt: str) -> str:
    """格式化批量转录结果。"""
    total_duration = sum(r.get("duration", 0) for r in results)
    all_text = " ".join(r["text"] for r in results if r.get("text"))

    lines = [
        f"# {speaker} 的音频批量转录",
        "",
        f"**文件数**：{len(results)} 个",
        f"**总时长**：{_fmt_duration(total_duration)}",
        f"**转录时间**：{datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
    ]

    if fmt == "chat":
        # 类聊天记录格式，适合微信语音消息
        lines.append("## 语音消息记录\n")
        for r in results:
            if r.get("text"):
                fname = r.get("filename", "")
                # 尝试从文件名提取时间（微信语音文件名常含时间戳）
                time_hint = _extract_time_from_filename(fname)
                prefix = f"[{time_hint}] " if time_hint else ""
                lines.append(f"**{speaker}**{' ' + prefix if prefix else ''}")
                lines.append(f"> {r['text']}")
                lines.append("")
    else:
        # 完整转录格式
        lines += ["## 完整转录文本\n", all_text, ""]
        lines += ["## 逐文件明细\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"### 文件 {i}：{r.get('filename', '')}")
            lines.append(r.get("text", "[无内容]"))
            lines.append("")

    # 语言分析提示
    lines += [
        "---",
        "",
        "## 分析提示（供档案建立参考）",
        "",
        "以下内容可从转录文本中提取，用于填充 persona.md 的 Layer 2：",
        "",
        "- 高频词/短句（候选口头禅）",
        "- 句子平均长度（话多/话少）",
        '- 语气词使用（"嗯""哦""啊"等）',
        "- 方言词汇",
        "",
        "*转录完成后，可将本文件内容粘贴给 AI，请求提取语言特征并更新档案。*",
        f"*来源标注建议：[音频转录，{datetime.now().strftime('%Y-%m-%d')}]*",
    ]
    return "\n".join(lines)


def _format_plain(result: dict, speaker: str) -> list[str]:
    """纯文本格式：全文 + 带时间戳的分段。"""
    lines = ["## 完整文本\n", result["text"], ""]
    segs = result.get("segments", [])
    if segs:
        lines += ["## 分段文本（含时间戳）\n"]
        for seg in segs:
            start = _fmt_duration(seg["start"])
            text = seg["text"].strip()
            if text:
                lines.append(f"`{start}` {text}")
        lines.append("")
    return lines


def _format_interview(result: dict, speaker: str) -> list[str]:
    """访谈格式：全文 + 分段 + 空白记录区。"""
    lines = _format_plain(result, speaker)
    lines += [
        "## 访谈笔记（人工补充）\n",
        "<!-- 在这里记录重要段落的背景信息、情绪状态、跑题内容等 -->",
        "",
        "**关键段落：**",
        "",
        "**情绪状态观察：**",
        "",
        "**待追问内容：**",
        "",
    ]
    return lines


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def _fmt_duration(seconds: float) -> str:
    """将秒数格式化为 mm:ss 或 hh:mm:ss。"""
    if seconds <= 0:
        return "0:00"
    s = int(seconds)
    h, remainder = divmod(s, 3600)
    m, sec = divmod(remainder, 60)
    if h:
        return f"{h}:{m:02d}:{sec:02d}"
    return f"{m}:{sec:02d}"


def _extract_time_from_filename(filename: str) -> Optional[str]:
    """尝试从文件名提取时间信息（微信语音文件名常含时间戳）。"""
    import re
    # 匹配 YYYYMMDD_HHMMSS 或 YYYYMMDD 格式
    m = re.search(r"(\d{4})(\d{2})(\d{2})[_-](\d{2})(\d{2})(\d{2})", filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)} {m.group(4)}:{m.group(5)}"
    m = re.search(r"(\d{4})(\d{2})(\d{2})", filename)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="音频转录工具 — 将音频转为文字供纪念档案使用",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="\n".join([f"  {k:<8} {v}" for k, v in MODEL_INFO.items()]),
    )

    src = parser.add_mutually_exclusive_group(required=True)
    src.add_argument("--file", help="单个音频文件路径")
    src.add_argument("--dir", help="批量处理：音频文件所在目录")

    parser.add_argument("--speaker", default="",
                        help="说话人姓名（用于输出标注）")
    parser.add_argument("--lang", default="zh",
                        help="语言代码，默认 zh（中文）；auto = 自动检测")
    parser.add_argument("--model", default="small",
                        choices=list(MODEL_INFO.keys()),
                        help="Whisper 模型大小（默认 small）")
    parser.add_argument("--mode", default="plain",
                        choices=["plain", "interview"],
                        help="单文件输出格式：plain=纯转录，interview=访谈格式（含笔记区）")
    parser.add_argument("--format", default="transcript",
                        choices=["transcript", "chat"],
                        dest="fmt",
                        help="批量输出格式：transcript=完整转录，chat=类聊天记录")
    parser.add_argument("--output", help="输出 Markdown 文件路径（默认输出到控制台）")

    args = parser.parse_args()

    model = load_whisper(args.model)
    speaker = args.speaker or "说话人"

    if args.file:
        if not os.path.exists(args.file):
            print(f"[错误] 找不到文件：{args.file}")
            sys.exit(1)
        ext = Path(args.file).suffix.lower()
        if ext not in SUPPORTED_FORMATS:
            print(f"[错误] 不支持的格式：{ext}（支持：{', '.join(SUPPORTED_FORMATS)}）")
            sys.exit(1)

        result = transcribe_file(model, args.file, args.lang)
        result["filename"] = os.path.basename(args.file)
        report = format_single_transcript(result, speaker, args.mode)

    else:  # --dir
        if not os.path.isdir(args.dir):
            print(f"[错误] 找不到目录：{args.dir}")
            sys.exit(1)
        results = transcribe_directory(model, args.dir, args.lang)
        if not results:
            sys.exit(1)
        report = format_batch_transcript(results, speaker, args.fmt)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[输出] 转录结果已保存到 {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
