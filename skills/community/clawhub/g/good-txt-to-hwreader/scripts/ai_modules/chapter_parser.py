#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 章节识别模块
使用 LLM 智能识别各种格式的章节标题
"""

import json
import re
import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 导入 LLM 客户端
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.llm_client import LLMClient, get_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ChapterInfo:
    """章节信息"""
    line_number: int
    title: str
    original: str
    confidence: float
    chapter_number: Optional[int] = None


@dataclass
class ChapterParseResult:
    """章节解析结果"""
    chapter_format: str
    chapters: List[ChapterInfo]
    total_chapters: int
    success: bool


# 章节识别 Prompt 模板
CHAPTER_PARSE_PROMPT = """# 角色
你是一个专业的文本结构分析专家，擅长识别各种格式的章节标题。

# 任务
分析以下文本的章节结构，识别所有章节标题。

# 常见章节格式
1. 标准格式：第X章/节/回 标题
2. 英文格式：Chapter X: Title
3. 数字格式：1. 标题 / 一、标题
4. 古风格式：卷X、篇X、楔子、尾声
5. 特殊格式：【章节名】、《章节名》
6. 无编号：纯标题行（需根据上下文判断）

# 识别原则
1. 章节标题通常独立成行
2. 章节标题前后可能有空行
3. 章节标题通常较短（<50字）
4. 章节标题通常不包含对话内容
5. 注意区分章节标题和正文中的类似文本

# 输出格式（仅输出 JSON，不要其他内容）
{{"chapter_format": "识别到的章节格式类型", "chapters": [{{"line_number": 行号, "title": "章节标题", "original": "原始文本", "confidence": 0.0-1.0, "chapter_number": 章节序号或null}}], "total_chapters": 总章节数}}

# 待分析文本（前5000字样本）
{text_sample}"""

# 章节标题规范化 Prompt 模板
CHAPTER_NORMALIZE_PROMPT = """# 角色
你是一个专业的文本规范化专家。

# 任务
将以下章节标题规范化为统一格式。

# 规范化规则
1. 统一格式：第X章 标题
2. 移除多余空格和特殊字符
3. 保留原标题的语义
4. 处理被广告干扰的标题

# 输出格式（仅输出 JSON，不要其他内容）
{{"original": "原标题", "normalized": "规范化后的标题", "chapter_number": 章节序号, "title": "章节名称"}

# 待处理标题
{title}"""


class AIChapterParser:
    """AI 章节识别器"""
    
    def __init__(self, config: Dict, llm_client: Optional[LLMClient] = None):
        self.config = config.get('ai_enhancement', {}).get('chapter_detection', {})
        self.enabled = self.config.get('enabled', False)  # 默认关闭
        self.sample_size = self.config.get('sample_size', 5000)
        self.confidence_threshold = self.config.get('confidence_threshold', 0.8)
        
        # LLM 客户端
        self.llm = llm_client or get_client(config)
        
        # 统计信息
        self.total_processed = 0
        self.chapters_found = 0
    
    def parse(self, text: str) -> ChapterParseResult:
        """解析文本章节结构"""
        if not self.enabled:
            logger.info("AI 章节识别已禁用，使用规则引擎")
            return self._rule_parse(text)
        
        # 获取文本样本
        sample = text[:self.sample_size] if len(text) > self.sample_size else text
        
        # AI 分析
        prompt = CHAPTER_PARSE_PROMPT.format(text_sample=sample)
        response = self.llm.call(prompt)
        
        if not response.success:
            logger.error(f"LLM 调用失败: {response.error}")
            return self._rule_parse(text)
        
        return self._parse_ai_response(response.content, text)
    
    def _rule_parse(self, text: str) -> ChapterParseResult:
        """规则引擎解析章节"""
        lines = text.split('\n')
        chapters = []
        
        # 章节模式
        chapter_patterns = [
            # 标准格式
            (r'^第([一二三四五六七八九十百千万零\d]+)[章节回]\s*(.*)$', 'standard'),
            # 英文格式
            (r'^Chapter\s*(\d+)[:\.\s]*(.*)$', 'english'),
            # 数字格式
            (r'^(\d+)[\.、\s]+(.{1,30})$', 'numbered'),
            # 古风格式
            (r'^[卷篇部]\s*([一二三四五六七八九十\d]+)[\s：:]+(.*)$', 'ancient'),
            # 楔子/尾声
            (r'^(楔子|序章|引子|尾声|后记|终章)\s*(.*)$', 'special'),
        ]
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) > 50:
                continue
            
            for pattern, fmt in chapter_patterns:
                match = re.match(pattern, line, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    chapter_num = self._parse_chinese_number(groups[0]) if fmt in ['standard', 'ancient'] else int(groups[0]) if groups[0].isdigit() else None
                    title = groups[1] if len(groups) > 1 else ''
                    
                    chapters.append(ChapterInfo(
                        line_number=i,
                        title=title.strip(),
                        original=line,
                        confidence=0.9,
                        chapter_number=chapter_num
                    ))
                    break
        
        self.chapters_found += len(chapters)
        self.total_processed += 1
        
        return ChapterParseResult(
            chapter_format='rule_detected',
            chapters=chapters,
            total_chapters=len(chapters),
            success=True
        )
    
    def _parse_ai_response(self, content: str, text: str) -> ChapterParseResult:
        """解析 AI 响应"""
        try:
            content = content.strip()
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content
                content = content.rsplit('```', 1)[0] if '```' in content else content
            
            data = json.loads(content)
            
            chapters = []
            for item in data.get('chapters', []):
                confidence = item.get('confidence', 0.0)
                if confidence >= self.confidence_threshold:
                    chapters.append(ChapterInfo(
                        line_number=item.get('line_number', 0),
                        title=item.get('title', ''),
                        original=item.get('original', ''),
                        confidence=confidence,
                        chapter_number=item.get('chapter_number')
                    ))
            
            self.chapters_found += len(chapters)
            self.total_processed += 1
            
            return ChapterParseResult(
                chapter_format=data.get('chapter_format', 'unknown'),
                chapters=chapters,
                total_chapters=len(chapters),
                success=True
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            return self._rule_parse(text)
    
    def normalize_title(self, title: str) -> Dict:
        """规范化章节标题"""
        prompt = CHAPTER_NORMALIZE_PROMPT.format(title=title)
        response = self.llm.call(prompt)
        
        if not response.success:
            return {
                'original': title,
                'normalized': title,
                'chapter_number': None,
                'title': title
            }
        
        try:
            content = response.content.strip()
            if content.startswith('```'):
                content = content.split('\n', 1)[1] if '\n' in content else content
                content = content.rsplit('```', 1)[0] if '```' in content else content
            
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                'original': title,
                'normalized': title,
                'chapter_number': None,
                'title': title
            }
    
    def _parse_chinese_number(self, num_str: str) -> Optional[int]:
        """解析中文数字"""
        chinese_nums = {
            '零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
            '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
            '十': 10, '百': 100, '千': 1000, '万': 10000
        }
        
        # 纯数字
        if num_str.isdigit():
            return int(num_str)
        
        # 简单中文数字
        if num_str in chinese_nums:
            return chinese_nums[num_str]
        
        # 复杂中文数字（简化处理）
        result = 0
        for char in num_str:
            if char in chinese_nums:
                result += chinese_nums[char]
        
        return result if result > 0 else None
    
    def stats(self) -> Dict:
        """获取统计信息"""
        return {
            'enabled': self.enabled,
            'total_processed': self.total_processed,
            'chapters_found': self.chapters_found,
            'avg_chapters_per_text': self.chapters_found / self.total_processed if self.total_processed > 0 else 0
        }


def normalize_text_chapters(text: str, result: ChapterParseResult) -> Tuple[str, Dict]:
    """规范化文本中的章节标题"""
    if not result.success or not result.chapters:
        return text, {'normalized': 0}
    
    lines = text.split('\n')
    normalized_count = 0
    
    for chapter in result.chapters:
        if chapter.line_number < len(lines):
            # 简单规范化：统一格式
            if chapter.chapter_number:
                new_title = f"第{chapter.chapter_number}章 {chapter.title}"
                lines[chapter.line_number] = new_title
                normalized_count += 1
    
    return '\n'.join(lines), {'normalized': normalized_count}
