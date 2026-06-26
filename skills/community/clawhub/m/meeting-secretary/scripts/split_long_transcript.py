#!/usr/bin/env python3
"""
长会议转录文本智能分段脚本

用于将数万字的会议转录文本智能分段为多个逻辑段落，
便于AI进行高质量分析。

分段策略:
1. 语义边界识别（主题转换）
2. 时间戳边界（如果有）
3. 发言者切换（如果有标注）
4. 适当段落长度（2000-4000字/段）
"""

import argparse
import re
import sys
from pathlib import Path


def split_by_timestamps(text):
    """
    按时间戳分段（适用于带时间戳的转录）

    Args:
        text: 包含时间戳的转录文本

    Returns:
        分段列表，每段包含时间范围和文本
    """
    segments = []

    # 匹配时间戳格式: [00:15:23 - 00:17:45] 或 [00:15:23]
    timestamp_pattern = r'\[(\d{2}:\d{2}:\d{2})(\s*-\s*\d{2}:\d{2}:\d{2})?\]'

    parts = re.split(timestamp_pattern, text)

    current_segment = {"start": None, "end": None, "text": ""}

    i = 0
    while i < len(parts):
        if re.match(timestamp_pattern, parts[i] if i < len(parts) else ""):
            # 这是时间戳
            if current_segment["text"]:
                segments.append(current_segment.copy())

            timestamp = parts[i]
            current_segment = {"start": timestamp, "end": None, "text": ""}
            i += 1
        else:
            # 这是文本内容
            current_segment["text"] += parts[i] if i < len(parts) else ""
            i += 1

    if current_segment["text"]:
        segments.append(current_segment)

    return segments


def split_by_speaker(text):
    """
    按发言者分段（适用于有发言者标注的转录）

    Args:
        text: 包含发言者标注的文本

    Returns:
        按发言者分段的列表
    """
    segments = []

    # 常见发言者标注格式:
    # - 张三: 内容
    # - [张三]: 内容
    # - 张三说: 内容
    speaker_patterns = [
        r'^([^\s:]+):\s*(.+)$',  # 张三: 内容
        r'^\[([^\]]+)\]:\s*(.+)$',  # [张三]: 内容
        r'^([^\s:]+)说[:：]\s*(.+)$',  # 张三说: 内容
    ]

    lines = text.split('\n')
    current_speaker = None
    current_text = ""

    for line in lines:
        matched = False
        for pattern in speaker_patterns:
            match = re.match(pattern, line)
            if match:
                # 保存上一段
                if current_speaker and current_text:
                    segments.append({
                        "speaker": current_speaker,
                        "text": current_text.strip()
                    })

                # 开始新段落
                current_speaker = match.group(1)
                current_text = match.group(2)
                matched = True
                break

        if not matched:
            current_text += "\n" + line

    # 保存最后一段
    if current_speaker and current_text:
        segments.append({
            "speaker": current_speaker,
            "text": current_text.strip()
        })

    return segments


def split_by_semantic_boundaries(text, min_length=1500, max_length=4000):
    """
    按语义边界智能分段

    Args:
        text: 转录文本
        min_length: 最小段落长度（字数）
        max_length: 最大段落长度（字数）

    Returns:
        分段列表
    """
    segments = []

    # 语义边界标记（通常表示话题转换）
    boundary_markers = [
        r'。\n\n',  # 句号+空行
        r'！\n\n',  # 感叹号+空行
        r'？\n\n',  # 问号+空行
        r'\n\n+',   # 多个空行
        r'接下来',   # 话题转换词
        r'另外',     # 话题转换词
        r'然后',     # 话题转换词
        r'总的来说',  # 总结词
        r'综上所述',  # 总结词
    ]

    # 首先尝试按明确边界分割
    split_pattern = '|'.join(boundary_markers)
    parts = re.split(f'({split_pattern})', text)

    current_segment = ""

    for part in parts:
        if len(current_segment) + len(part) < max_length:
            current_segment += part
        else:
            # 当前段落已达到最大长度
            if len(current_segment) > min_length:
                segments.append(current_segment.strip())
                current_segment = part
            else:
                # 段落太短，继续累积
                current_segment += part

    # 添加最后一段
    if current_segment.strip():
        segments.append(current_segment.strip())

    return segments


def split_long_meeting_transcript(text, method="auto", output_dir=None):
    """
    智能分段长会议转录

    Args:
        text: 会议转录文本
        method: 分段方法 ("auto", "timestamp", "speaker", "semantic")
        output_dir: 输出目录

    Returns:
        分段信息
    """
    print(f"正在分析会议转录（字数: {len(text)}）...")

    # 自动检测最佳分段方法
    if method == "auto":
        # 检测是否有时间戳
        if re.search(r'\[\d{2}:\d{2}:\d{2}', text):
            method = "timestamp"
            print("检测到时间戳，使用时间戳分段")
        # 检测是否有发言者标注
        elif re.search(r'^([^\s:]+):\s*', text, re.MULTILINE):
            method = "speaker"
            print("检测到发言者标注，使用发言者分段")
        else:
            method = "semantic"
            print("使用语义边界分段")

    # 执行分段
    if method == "timestamp":
        segments = split_by_timestamps(text)
    elif method == "speaker":
        segments = split_by_speaker(text)
    else:
        segments = split_by_semantic_boundaries(text)

    print(f"共分为 {len(segments)} 个段落")

    # 保存分段结果
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # 保存分段索引文件
        index_file = output_path / "segments_index.md"
        with open(index_file, "w", encoding="utf-8") as f:
            f.write("# 会议分段索引\n\n")
            f.write(f"总段数: {len(segments)}\n\n")

            for i, seg in enumerate(segments):
                if isinstance(seg, dict):
                    title = seg.get("speaker") or seg.get("start", f"段落{i+1}")
                    content = seg.get("text", str(seg))
                else:
                    title = f"段落{i+1}"
                    content = seg

                f.write(f"## {title}\n")
                f.write(f"- 文件: segment_{i+1:03d}.txt\n")
                f.write(f"- 长度: {len(content)} 字\n\n")

                # 保存单独的段落文件
                segment_file = output_path / f"segment_{i+1:03d}.txt"
                with open(segment_file, "w", encoding="utf-8") as sf:
                    sf.write(content)

        print(f"分段结果已保存到: {output_dir}")
        print(f"索引文件: {index_file}")

    return {
        "method": method,
        "count": len(segments),
        "segments": segments
    }


def main():
    parser = argparse.ArgumentParser(description="长会议转录智能分段工具")
    parser.add_argument("input_file", help="输入转录文本文件")
    parser.add_argument("--method", "-m", choices=["auto", "timestamp", "speaker", "semantic"],
                       default="auto", help="分段方法（默认: auto）")
    parser.add_argument("--output", "-o", help="输出目录")

    args = parser.parse_args()

    # 读取输入文件
    try:
        with open(args.input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"错误: 无法读取文件 {args.input_file}: {e}")
        sys.exit(1)

    # 执行分段
    result = split_long_meeting_transcript(
        text,
        method=args.method,
        output_dir=args.output
    )

    print(f"\n分段完成!")
    print(f"方法: {result['method']}")
    print(f"段数: {result['count']}")


if __name__ == "__main__":
    main()
