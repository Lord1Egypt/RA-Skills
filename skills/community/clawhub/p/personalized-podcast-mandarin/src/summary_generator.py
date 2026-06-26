# -*- coding: utf-8 -*-
"""
生成摘要展示器
格式化展示播客生成结果，提供生成内容的透明度和可读性
"""

from typing import Dict, Any, List, Optional
from datetime import datetime


class SummaryGenerator:
    """
    生成摘要展示器

    在播客生成完成后，格式化展示：
    - 内容概览（主题、风格、时长）
    - Research 亮点（hook、核心洞察、引用来源）
    - 段落结构（每段时长、对话模式）
    - 输出文件路径
    """

    def __init__(self, result: Dict[str, Any]):
        """
        Args:
            result: PodcastPipeline.generate() 的返回结果
        """
        self.result = result
        self.research = result.get("research", {})
        self.script = result.get("script", [])

    def generate_summary(self, verbose: bool = True) -> str:
        """
        生成完整摘要

        Args:
            verbose: 是否包含详细信息

        Returns:
            格式化的摘要文本
        """
        lines = []

        # 头部
        lines.extend(self._header_section())
        lines.append("")

        # Research 亮点
        lines.extend(self._research_section())
        lines.append("")

        # 段落结构
        lines.extend(self._structure_section())
        lines.append("")

        # 输出文件
        lines.extend(self._output_section())

        if verbose:
            lines.append("")
            lines.extend(self._stats_section())

        return "\n".join(lines)

    def _header_section(self) -> List[str]:
        """生成头部信息"""
        style = self.result.get("style", "深度对谈")
        source = self.result.get("source", "未知主题")
        source_type = self.result.get("source_type", "topic")

        # 截断过长的主题
        if len(source) > 30:
            source_display = source[:27] + "..."
        else:
            source_display = source

        # 计算总时长
        total_duration = sum(
            seg.get("estimated_duration_sec", 0) or seg.get("word_count", 0) / 250 * 60
            for seg in self.script
        )
        duration_min = int(total_duration / 60)

        lines = [
            "=" * 60,
            "🎙️ 播客生成完成",
            "=" * 60,
            "",
            f"📌 主题: {source_display}",
            f"🏷️ 风格: {style}",
            f"⏱️ 预估时长: 约{duration_min}分钟",
        ]

        return lines

    def _research_section(self) -> List[str]:
        """生成 Research 亮点部分"""
        lines = ["🔍 内容亮点"]
        lines.append("-" * 40)

        # Hook
        hook = self.research.get("hook", "")
        if hook:
            lines.append(f"💡 开场钩子: {hook}")
            lines.append("")

        # 核心洞察
        central_insight = self.research.get("central_insight", "")
        if central_insight:
            # 截断过长的洞察
            if len(central_insight) > 50:
                insight_display = central_insight[:47] + "..."
            else:
                insight_display = central_insight
            lines.append(f"🎯 核心洞察: {insight_display}")
            lines.append("")

        # 关键引用来源
        materials = self.research.get("enriched_materials", [])
        if materials:
            lines.append("📚 参考来源:")
            sources = set()
            for mat in materials[:3]:  # 最多显示3个来源
                source = mat.get("source", "")
                if source and source not in sources:
                    sources.add(source)
                    # 截断过长的来源名
                    if len(source) > 40:
                        source = source[:37] + "..."
                    lines.append(f"   • {source}")

        return lines

    def _structure_section(self) -> List[str]:
        """生成段落结构部分"""
        lines = ["📝 内容结构"]
        lines.append("-" * 40)

        if not self.script:
            lines.append("   （无段落信息）")
            return lines

        for i, segment in enumerate(self.script, 1):
            seg_id = segment.get("segment_id", f"seg_{i:02d}")
            word_count = segment.get("word_count", 0)
            duration_sec = segment.get("estimated_duration_sec", 0)

            # 计算时长（分钟）
            if duration_sec:
                duration_min = int(duration_sec / 60)
            else:
                duration_min = int(word_count / 250)  # 假设每分钟250字

            # 获取对话模式
            lines_data = segment.get("lines", [])
            speaker_a_count = sum(1 for line in lines_data if line.get("speaker") == "A")
            speaker_b_count = sum(1 for line in lines_data if line.get("speaker") == "B")

            # 获取摘要（如有）
            summary = segment.get("summary", "")
            if summary and len(summary) > 30:
                summary = summary[:27] + "..."

            lines.append(f"第{i}段 ({duration_min}分钟)")
            if summary:
                lines.append(f"   {summary}")
            lines.append(f"   对话: A说{speaker_a_count}句, B说{speaker_b_count}句")
            lines.append("")

        return lines

    def _output_section(self) -> List[str]:
        """生成输出文件部分"""
        lines = ["📁 输出文件"]
        lines.append("-" * 40)

        session_id = self.result.get("session_id", "unknown")

        # 音频文件
        audio_path = self.result.get("audio_path")
        if audio_path:
            lines.append(f"🎧 音频: {audio_path}")

        # JSON 文件
        json_path = self.result.get("json_path", f"./output/podcast_{session_id}.json")
        lines.append(f"📄 数据: {json_path}")

        # Markdown 文件
        md_path = self.result.get("markdown_path", f"./output/podcast_{session_id}.md")
        lines.append(f"📝 文稿: {md_path}")

        return lines

    def _stats_section(self) -> List[str]:
        """生成统计信息部分"""
        lines = ["📊 生成统计"]
        lines.append("-" * 40)

        # 总字数
        total_words = sum(seg.get("word_count", 0) for seg in self.script)
        lines.append(f"总字数: {total_words} 字")

        # 对话行数
        total_lines = sum(len(seg.get("lines", [])) for seg in self.script)
        lines.append(f"对话行数: {total_lines} 句")

        # 段落数
        lines.append(f"段落数: {len(self.script)} 段")

        # 生成时间
        timestamp = self.result.get("timestamp", "")
        if timestamp:
            lines.append(f"生成时间: {timestamp}")

        return lines

    def print_summary(self, verbose: bool = True):
        """打印摘要到控制台"""
        print(self.generate_summary(verbose))
