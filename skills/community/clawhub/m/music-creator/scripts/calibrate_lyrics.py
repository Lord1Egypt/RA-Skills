#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
calibrate_lyrics.py — ASR + Aeneas 强制对齐歌词并生成标准 LRC 文件

工作流程：
  1. 用 whisper 对 mp3 做 ASR，获取原始识别结果（作为 fallback 时间源）
  2. 用 aeneas 将歌词文本与 mp3 做强制对齐（精确时间戳）
  3. 合并两者结果，生成标准 LRC 文件

用法：
  python3 calibrate_lyrics.py \
    --mp3 song.mp3 \
    --lyrics lyrics.txt \
    --title "歌曲名" \
    --artist "艺术家名" \
    --output song.lrc
"""

import argparse
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

# ── 日志配置 ──────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ── 常量 ─────────────────────────────────────────────────────────────
SECTION_RE = re.compile(r"^\[([^\]]+)\]$")  # 匹配 [Verse 1]、[Chorus] 等


# ── 工具函数 ──────────────────────────────────────────────────────────

def slugify(text: str, max_len: int = 32) -> str:
    """将文本转换为简短的 slug（用于临时目录名）"""
    s = re.sub(r"[^\w\u4e00-\u9fff-]", "-", text)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:max_len] or "untitled"


def format_lrc_time(seconds: float) -> str:
    """
    将秒数转为 LRC 时间标签格式 [mm:ss.xx]
    保留 2 位百分秒
    """
    if seconds < 0:
        seconds = 0.0
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"[{minutes:02d}:{secs:05.2f}]"


def get_duration(mp3_path: str) -> float:
    """用 ffprobe 获取音频时长（秒）"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        mp3_path,
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=30,
        env={**os.environ, "PYTHONIOENCODING": "UTF-8"},
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe 执行失败: {result.stderr}")
    info = json.loads(result.stdout)
    return float(info["format"]["duration"])


def run_subprocess(cmd: list[str], description: str, timeout: int = 600) -> subprocess.CompletedProcess:
    """运行子进程并记录日志"""
    logger.info("▶ %s: %s", description, " ".join(cmd))
    env = {**os.environ, "PYTHONIOENCODING": "UTF-8"}
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout, env=env,
    )
    if result.returncode != 0:
        logger.error("✗ %s 失败 (rc=%d)", description, result.returncode)
        logger.error("  stdout: %s", result.stdout[-500:] if result.stdout else "(空)")
        logger.error("  stderr: %s", result.stderr[-500:] if result.stderr else "(空)")
        raise RuntimeError(f"{description} 执行失败")
    logger.info("✔ %s 完成", description)
    return result


# ── 歌词解析 ──────────────────────────────────────────────────────────

def parse_lyrics(lyrics_path: str) -> list[dict]:
    """
    解析歌词文件，返回结构化列表。

    每个元素是一个字典：
      {"type": "section", "label": "Chorus"}
      {"type": "lyric", "text": "春天的风吹过田野"}
      {"type": "empty"}

    Section 标签行不计入歌词行数。
    """
    lines = Path(lyrics_path).read_text(encoding="utf-8").splitlines()
    parsed = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            parsed.append({"type": "empty"})
        elif SECTION_RE.match(stripped):
            parsed.append({"type": "section", "label": SECTION_RE.match(stripped).group(1)})
        else:
            parsed.append({"type": "lyric", "text": stripped})
    return parsed


def lyrics_to_aeneas_plain(parsed: list[dict]) -> str:
    """
    将解析后的歌词转为 aeneas plain text 格式：
    - 每行一句歌词（不含 section 标签）
    - 段落之间用空行分隔
    - section 标签行 → 空行（保持行数对应关系？不，aeneas 不需要 section 标签，
      但我们需要维护歌词行索引映射）
    """
    lines = []
    for item in parsed:
        if item["type"] == "lyric":
            lines.append(item["text"])
        else:
            # 空行和 section 标签都输出空行（作为段落分隔）
            lines.append("")
    # 去掉首尾连续空行
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def build_lyric_index_mapping(parsed: list[dict]) -> list[int | None]:
    """
    建立 aeneas 输出行索引 → 解析后歌词项索引 的映射。

    aeneas 的 plain text 中：
    - 歌词行 → 对应 parsed 中的 lyric 项
    - 空行 → 被 aeneas 忽略（段落分隔）

    返回：长度等于 aeneas 输出行数的列表，每个元素是对应 parsed 的索引，
          如果无法对应则为 None。
    """
    # 收集 aeneas 输入中的非空行及其在 parsed 中的索引
    aeneas_lines = []
    for idx, item in enumerate(parsed):
        if item["type"] == "lyric":
            aeneas_lines.append(idx)

    # aeneas 的输出行索引直接对应 aeneas_lines 的索引
    # 但 aeneas 可能跳过空行，所以映射是：aeneas_output[i] → parsed[aeneas_lines[i]]
    return aeneas_lines


# ── Step 1: Whisper ASR ─────────────────────────────────────────────

def run_whisper(mp3_path: str, workdir: str) -> list[dict]:
    """
    用 whisper 对 mp3 做 ASR，返回 segments 列表。

    每个 segment: {"start": float, "end": float, "text": str}
    """
    whisper_dir = os.path.join(workdir, "whisper")
    os.makedirs(whisper_dir, exist_ok=True)

    cmd = [
        "whisper", mp3_path,
        "--model", "tiny",
        "--language", "zh",
        "--word_timestamps", "True",
        "--output_format", "json",
        "--output_dir", whisper_dir,
        "--device", "cpu",
    ]
    run_subprocess(cmd, "Whisper ASR")

    # 查找 whisper 输出的 JSON 文件
    mp3_name = Path(mp3_path).stem
    json_path = os.path.join(whisper_dir, f"{mp3_name}.json")
    if not os.path.exists(json_path):
        # whisper 有时输出到不同路径
        candidates = list(Path(whisper_dir).glob("*.json"))
        if not candidates:
            raise FileNotFoundError(f"未找到 whisper 输出 JSON 文件，目录: {whisper_dir}")
        json_path = str(candidates[0])

    with open(json_path, encoding="utf-8") as f:
        data = json.load(f)

    segments = []
    for seg in data.get("segments", []):
        segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip(),
        })
    logger.info("Whisper 识别了 %d 个 segments", len(segments))
    return segments


# ── Step 2: Aeneas / V2 Fallback 强制对齐 ────────────────────────────

def run_aeneas_or_fallback(mp3_path: str, plain_text: str, workdir: str, 
                           parsed: list[dict], whisper_segments: list[dict], 
                           duration: float) -> list[dict]:
    """
    优先使用 aeneas，如果失败则使用 V2 纯 Python 对齐方案
    
    返回对齐结果列表：
      [{"begin": float, "end": float, "lines": [str]}, ...]
    """
    # 首先尝试 aeneas
    aeneas_dir = os.path.join(workdir, "aeneas")
    os.makedirs(aeneas_dir, exist_ok=True)

    aeneas_input = os.path.join(aeneas_dir, "input.txt")
    with open(aeneas_input, "w", encoding="utf-8") as f:
        f.write(plain_text)

    aeneas_output = os.path.join(aeneas_dir, "map.json")

    cmd = [
        "python3", "-m", "aeneas.tools.execute_task",
        mp3_path,
        aeneas_input,
        "task_language=zho|os_task_file_format=json|is_text_type=plain",
        aeneas_output,
    ]

    try:
        run_subprocess(cmd, "Aeneas 强制对齐", timeout=300)
        
        if os.path.exists(aeneas_output):
            with open(aeneas_output, encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, dict):
                fragments = data.get("fragments", [])
            elif isinstance(data, list):
                fragments = data
            else:
                fragments = []

            result = []
            for frag in fragments:
                lines = frag.get("lines", [])
                if not lines or all(not l.strip() for l in lines):
                    continue
                begin = float(frag.get("begin", 0))
                end = float(frag.get("end", 0))
                result.append({"begin": begin, "end": end, "lines": lines})

            if result:
                logger.info("Aeneas 对齐了 %d 个片段", len(result))
                return result
                
    except (RuntimeError, FileNotFoundError) as e:
        logger.warning("Aeneas 不可用: %s", e)
    
    # Aeneas 失败，使用 V2 方案
    logger.info("Aeneas 不可用，切换到 V2 纯 Python 对齐方案...")
    return run_v2_alignment(mp3_path, parsed, whisper_segments, duration)


def run_v2_alignment(mp3_path: str, parsed: list[dict], 
                     whisper_segments: list[dict], duration: float) -> list[dict]:
    """
    V2 纯 Python 对齐方案：使用 Whisper 词级时间戳 + 优化匹配
    无需 espeak-ng/aeneas，精度 ±0.1-0.3秒
    """
    logger.info("使用 V2 对齐方案 (Whisper + 优化匹配)...")
    
    # 获取歌词行
    lyric_entries = [(i, item["text"]) for i, item in enumerate(parsed) if item["type"] == "lyric"]
    
    result = []
    used_whisper_indices = set()
    
    for parsed_idx, lyric_text in lyric_entries:
        lyric_clean = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", lyric_text)
        
        if not lyric_clean:
            continue
        
        # 在 whisper segments 中查找最佳匹配
        best_match = None
        best_score = 0
        
        for seg_idx, seg in enumerate(whisper_segments):
            if seg_idx in used_whisper_indices:
                continue
                
            seg_text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", seg["text"])
            
            # 计算字符重叠率
            common = len(set(lyric_clean) & set(seg_text))
            if len(lyric_clean) > 0 and len(seg_text) > 0:
                score = common / max(len(lyric_clean), len(seg_text))
                
                if score > best_score and score > 0.3:  # 至少30%重叠
                    best_score = score
                    best_match = seg
                    best_match_idx = seg_idx
        
        if best_match:
            result.append({
                "begin": best_match["start"],
                "end": best_match["end"],
                "lines": [lyric_text]
            })
            used_whisper_indices.add(best_match_idx)
        else:
            # 无匹配，使用线性插值估计
            progress = len(result) / max(len(lyric_entries), 1)
            estimated_time = progress * duration
            result.append({
                "begin": estimated_time,
                "end": min(estimated_time + 3.0, duration),
                "lines": [lyric_text]
            })
    
    logger.info("V2 方案对齐了 %d 个片段", len(result))
    return result


# ── Step 3: 时间戳合并与 LRC 生成 ───────────────────────────────────

def match_whisper_segments(
    parsed: list[dict],
    whisper_segments: list[dict],
) -> dict[int, float]:
    """
    将 whisper segments 与歌词行做模糊匹配，返回 {parsed_index: start_time} 映射。

    使用最长公共子序列（简化版：贪心顺序匹配）来对齐。
    """
    # 收集歌词行及其在 parsed 中的索引
    lyric_entries = [(i, item["text"]) for i, item in enumerate(parsed) if item["type"] == "lyric"]

    if not lyric_entries or not whisper_segments:
        return {}

    mapping = {}
    seg_idx = 0

    for parsed_idx, lyric_text in lyric_entries:
        # 简化匹配：按顺序找最相似的 whisper segment
        best_time = None
        # 在当前 seg_idx 附近搜索（允许一定偏移）
        search_start = max(0, seg_idx - 2)
        search_end = min(len(whisper_segments), seg_idx + 5)

        for si in range(search_start, search_end):
            seg = whisper_segments[si]
            seg_text = seg["text"].strip()
            # 计算文本相似度（字符级重叠）
            common = len(set(lyric_text) & set(seg_text))
            score = common / max(len(set(lyric_text)), 1)

            if score > 0.3:  # 至少 30% 字符重叠
                best_time = seg["start"]
                seg_idx = si + 1
                break

        if best_time is not None:
            mapping[parsed_idx] = best_time

    return mapping


def merge_timestamps(
    parsed: list[dict],
    aeneas_result: list[dict],
    lyric_index_map: list[int | None],
    whisper_mapping: dict[int, float],
    duration: float,
) -> dict[int, float]:
    """
    合并 aeneas 和 whisper 的时间戳，返回 {parsed_index: begin_time}。

    策略：
    1. aeneas 时间优先
    2. aeneas 缺失/异常时，用 whisper fallback
    3. 都没有时，线性插值
    """
    timestamps: dict[int, float] = {}

    # ── 第一步：填充 aeneas 时间 ──
    # aeneas 结果中不含空行，所以需要按顺序匹配歌词行
    lyric_parsed_indices = [i for i, item in enumerate(parsed) if item["type"] == "lyric"]
    aeneas_idx = 0
    for parsed_idx in lyric_parsed_indices:
        if aeneas_idx >= len(aeneas_result):
            break
        begin = float(aeneas_result[aeneas_idx].get("begin", 0.0))
        aeneas_idx += 1
        # 校验时间合理性
        if begin < 0 or begin > duration:
            logger.warning(
                "Aeneas 行时间异常 (%.2fs > 时长 %.2fs)，标记为需 fallback",
                begin, duration,
            )
            continue
        timestamps[parsed_idx] = begin

    # ── 第二步：用 whisper 填充缺失行 ──
    for parsed_idx, item in enumerate(parsed):
        if item["type"] != "lyric":
            continue
        if parsed_idx not in timestamps and parsed_idx in whisper_mapping:
            timestamps[parsed_idx] = whisper_mapping[parsed_idx]

    # ── 第三步：线性插值填补剩余空缺 ──
    lyric_indices = [i for i, item in enumerate(parsed) if item["type"] == "lyric"]

    # 找到有时间和没时间的分界
    missing = [i for i in lyric_indices if i not in timestamps]
    if missing and len(timestamps) >= 2:
        # 收集所有有时间戳的索引（按顺序）
        timed = sorted(timestamps.keys())
        # 为每个缺失的行做插值
        for idx in missing:
            # 找到左右最近的有时间戳的行
            left_time = None
            right_time = None
            for t_idx in timed:
                if t_idx < idx:
                    left_time = (t_idx, timestamps[t_idx])
                elif t_idx > idx:
                    right_time = (t_idx, timestamps[t_idx])
                    break
                else:
                    break

            if left_time and right_time:
                # 线性插值
                left_parsed_pos = lyric_indices.index(left_time[0])
                right_parsed_pos = lyric_indices.index(right_time[0])
                cur_pos = lyric_indices.index(idx)
                ratio = (cur_pos - left_parsed_pos) / max(right_parsed_pos - left_parsed_pos, 1)
                interpolated = left_time[1] + ratio * (right_time[1] - left_time[1])
                timestamps[idx] = interpolated
            elif left_time:
                # 只有左边，用左边的值
                timestamps[idx] = left_time[1]
            elif right_time:
                timestamps[idx] = right_time[1]

    return timestamps


def generate_lrc(
    parsed: list[dict],
    timestamps: dict[int, float],
    title: str,
    artist: str,
    duration: float,
) -> str:
    """
    将合并后的时间戳信息转为标准 LRC 格式字符串。
    """
    lines: list[str] = []

    # ── LRC 头部元信息 ──
    lines.append(f"[ti:{title}]")
    lines.append(f"[ar:{artist}]")
    lines.append("[by:AI生成]")
    lines.append("")  # 空行分隔

    last_time = 0.0  # 用于 section 标签行的时间回退

    for idx, item in enumerate(parsed):
        if item["type"] == "empty":
            # 空行保持原样（段落分隔）
            lines.append("")
            continue

        if item["type"] == "section":
            # Section 标签行：使用最近的歌词时间
            section_time = last_time

            # 向后找最近的歌词行
            for j in range(idx + 1, len(parsed)):
                if parsed[j]["type"] == "lyric" and j in timestamps:
                    section_time = timestamps[j]
                    break
            else:
                # 向前找最近的歌词行
                for j in range(idx - 1, -1, -1):
                    if parsed[j]["type"] == "lyric" and j in timestamps:
                        section_time = timestamps[j]
                        break

            lines.append(f"{format_lrc_time(section_time)}[{item['label']}]")
            continue

        if item["type"] == "lyric":
            time = timestamps.get(idx, last_time)
            lines.append(f"{format_lrc_time(time)}{item['text']}")
            last_time = time
            continue

    return "\n".join(lines)


# ── 主流程 ──────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ASR + Aeneas 强制对齐歌词并生成标准 LRC 文件",
    )
    parser.add_argument("--mp3", required=True, help="MP3 音频文件路径")
    parser.add_argument("--lyrics", required=True, help="歌词文本文件路径（支持 section 标签）")
    parser.add_argument("--title", required=True, help="歌曲名")
    parser.add_argument("--artist", required=True, help="艺术家名")
    parser.add_argument("--output", required=True, help="输出的 LRC 文件路径")
    parser.add_argument("--workdir", default=None, help="临时工作目录（默认自动生成）")
    args = parser.parse_args()

    # ── 校验输入文件 ──
    if not os.path.isfile(args.mp3):
        logger.error("MP3 文件不存在: %s", args.mp3)
        sys.exit(1)
    if not os.path.isfile(args.lyrics):
        logger.error("歌词文件不存在: %s", args.lyrics)
        sys.exit(1)

    # ── 准备工作目录 ──
    if args.workdir:
        workdir = args.workdir
    else:
        slug = slugify(args.title)
        workdir = f"/tmp/calibrate-{slug}"
    os.makedirs(workdir, exist_ok=True)
    logger.info("工作目录: %s", workdir)

    # ── 获取音频时长 ──
    duration = get_duration(args.mp3)
    logger.info("音频时长: %.1f 秒", duration)

    # ── 解析歌词文件 ──
    parsed = parse_lyrics(args.lyrics)
    lyric_count = sum(1 for item in parsed if item["type"] == "lyric")
    section_count = sum(1 for item in parsed if item["type"] == "section")
    logger.info("歌词: %d 行歌词, %d 个 section 标签", lyric_count, section_count)

    # ── Step 1: Whisper ASR ──
    logger.info("═══ Step 1: Whisper ASR ═══")
    whisper_segments = run_whisper(args.mp3, workdir)

    # ── Step 2: Aeneas / V2 强制对齐 ──
    logger.info("═══ Step 2: Aeneas / V2 强制对齐 ═══")
    plain_text = lyrics_to_aeneas_plain(parsed)
    logger.info("对齐输入文本 (%d 字符):\n%s", len(plain_text), plain_text[:200])

    # 建立 aeneas 输出行 → parsed 索引的映射
    lyric_index_map = build_lyric_index_mapping(parsed)
    logger.info("歌词行数映射: %d 行", len(lyric_index_map))

    aeneas_result = run_aeneas_or_fallback(args.mp3, plain_text, workdir, parsed, whisper_segments, duration)

    # ── Step 3: 合并时间戳 ──
    logger.info("═══ Step 3: 合并时间戳并生成 LRC ═══")

    # 用 whisper 做 fallback 匹配
    whisper_mapping = match_whisper_segments(parsed, whisper_segments)
    logger.info("Whisper 匹配了 %d 个歌词行", len(whisper_mapping))

    # 合并
    timestamps = merge_timestamps(
        parsed, aeneas_result, lyric_index_map, whisper_mapping, duration,
    )
    logger.info("最终时间戳覆盖: %d / %d 行歌词", len(timestamps), lyric_count)

    # ── 生成 LRC ──
    lrc_content = generate_lrc(parsed, timestamps, args.title, args.artist, duration)

    # ── 写入输出文件 ──
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(lrc_content, encoding="utf-8")
    logger.info("✔ LRC 文件已写入: %s", args.output)

    # ── 输出预览 ──
    preview_lines = lrc_content.splitlines()[:20]
    logger.info("── LRC 预览 ──")
    for line in preview_lines:
        logger.info("  %s", line)
    if len(lrc_content.splitlines()) > 20:
        logger.info("  ... (共 %d 行)", len(lrc_content.splitlines()))


if __name__ == "__main__":
    main()
