#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说节奏分析器脚本 (Rhythm Analyzer for Novel Writing)
版本: 2.0.0
作者: AUTHOR
日期: 2026-04-14

功能概述:
基于搜索结果中的叙事节奏检测理论和方法论[6](@ref)[7](@ref)[8](@ref)，本脚本实现了
系统化的小说节奏分析功能，包括节奏多样性检测、平衡性评估、渐进性分析、
情感起伏监控等核心检查。通过结合傅里叶变换等数学手段[8](@ref)和AI驱动的
节奏特征提取，为作者提供专业的节奏诊断和调整建议。

核心特性:
1. 叙事节奏量化表征 - 基于展示和告知两种叙述形式的自动识别[8](@ref)
2. 节奏多样性分析 - 检测节奏变化是否丰富多样[6](@ref)
3. 情感节奏评估 - 分析情感起伏是否自然合理[6](@ref)[7](@ref)
4. 高潮铺垫检测 - 检查高潮前是否有足够铺垫[6](@ref)
5. 节奏过渡分析 - 评估节奏变化是否突兀[6](@ref)
6. 多维度节奏检测 - 情节、情感、信息三个维度的节奏分析

依赖库:
- pandas: 数据处理和分析
- numpy: 数值计算和傅里叶变换[8](@ref)
- scipy: 科学计算和信号处理
- jieba: 中文分词
- matplotlib: 数据可视化
- textblob: 情感分析
"""

import os
import sys
import json
import re
import math
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from collections import defaultdict, Counter
import statistics

# 第三方库导入
try:
    import pandas as pd
    import numpy as np
    from scipy import signal, fft
    import jieba
    import jieba.posseg as pseg
    import matplotlib.pyplot as plt
    from matplotlib import cm
    from textblob import TextBlob
    from textblob.translate import Translator
except ImportError as e:
    print(f"缺少必要的依赖库: {e}")
    print("请运行: pip install pandas numpy scipy jieba matplotlib textblob")
    sys.exit(1)

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rhythm_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 初始化jieba分词
jieba.initialize()

# 常量定义
class RhythmIssueType(Enum):
    """节奏问题类型枚举"""
    MONOTONOUS_RHYTHM = "节奏单调"  # 节奏变化不足
    UNBALANCED_RHYTHM = "节奏失衡"  # 节奏分布不均
    ABRUPT_TRANSITION = "过渡突兀"  # 节奏变化突然
    LACKING_BUILDUP = "铺垫不足"  # 高潮前缺少铺垫
    EMOTIONAL_FLAT = "情感平淡"  # 情感起伏不足
    INFO_DENSITY_ISSUE = "信息密度问题"  # 信息节奏不合理
    PACE_MISMATCH = "节奏类型不匹配"  # 节奏与小说类型不匹配
    DIALOGUE_RHYTHM_ISSUE = "对话节奏问题"  # 对话节奏不自然

class SeverityLevel(Enum):
    """问题严重程度枚举"""
    CRITICAL = "致命"
    SEVERE = "严重"
    MODERATE = "中等"
    MINOR = "轻微"

class NarrativeMode(Enum):
    """叙述模式枚举"""
    SHOWING = "展示"  # 直接展示场景和动作
    TELLING = "告知"  # 叙述者告知信息
    DIALOGUE = "对话"  # 角色对话
    DESCRIPTION = "描述"  # 环境或人物描述
    REFLECTION = "反思"  # 内心独白或反思

@dataclass
class RhythmSegment:
    """节奏分段数据结构"""
    segment_id: str
    start_chapter: int
    start_paragraph: int
    end_chapter: int
    end_paragraph: int
    narrative_mode: NarrativeMode
    text_content: str
    word_count: int
    sentence_count: int
    dialogue_ratio: float  # 对话占比
    description_ratio: float  # 描述占比
    action_ratio: float  # 动作占比
    emotional_intensity: float  # 情感强度(0-1)
    pace_score: float  # 节奏评分(0-1, 越高节奏越快)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "segment_id": self.segment_id,
            "start_location": f"第{self.start_chapter}章第{self.start_paragraph}段",
            "end_location": f"第{self.end_chapter}章第{self.end_paragraph}段",
            "narrative_mode": self.narrative_mode.value,
            "word_count": self.word_count,
            "sentence_count": self.sentence_count,
            "dialogue_ratio": self.dialogue_ratio,
            "description_ratio": self.description_ratio,
            "action_ratio": self.action_ratio,
            "emotional_intensity": self.emotional_intensity,
            "pace_score": self.pace_score
        }

@dataclass
class RhythmIssue:
    """节奏问题记录"""
    issue_id: str
    issue_type: RhythmIssueType
    severity: SeverityLevel
    location: str  # 格式: "第X章第Y段-第Z章第W段"
    description: str
    evidence: List[str] = field(default_factory=list)
    suggested_fixes: List[str] = field(default_factory=list)
    confidence_score: float = 0.0  # 置信度分数(0-1)
    rhythm_metrics: Dict[str, float] = field(default_factory=dict)  # 相关节奏指标
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "issue_id": self.issue_id,
            "issue_type": self.issue_type.value,
            "severity": self.severity.value,
            "location": self.location,
            "description": self.description,
            "evidence": self.evidence,
            "suggested_fixes": self.suggested_fixes,
            "confidence_score": self.confidence_score,
            "rhythm_metrics": self.rhythm_metrics
        }

class NovelRhythmAnalyzer:
    """
    小说节奏分析器主类
    
    基于搜索结果中的叙事节奏检测理论和方法论[6](@ref)[7](@ref)[8](@ref)，
    实现系统化的节奏问题检测功能。结合傅里叶变换等数学手段[8](@ref)
    和AI驱动的节奏特征提取，提供专业的节奏诊断和调整建议。
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化节奏分析器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config = self._load_config(config_path)
        self.rhythm_segments: List[RhythmSegment] = []
        self.rhythm_issues: List[RhythmIssue] = []
        self.narrative_sequence: List[NarrativeMode] = []  # 叙述模式序列
        self.pace_sequence: List[float] = []  # 节奏评分序列
        self.emotional_sequence: List[float] = []  # 情感强度序列
        
        # 小说类型特定的节奏标准
        self.genre_standards = self._init_genre_standards()
        
        # 初始化调整策略库
        self._init_adjustment_strategies()
        
        logger.info("小说节奏分析器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        default_config = {
            "segment_size_words": 500,  # 分段大小（字数）
            "min_segment_words": 100,  # 最小分段字数
            "max_segment_words": 1000,  # 最大分段字数
            "pace_threshold_low": 0.3,  # 慢节奏阈值
            "pace_threshold_high": 0.7,  # 快节奏阈值
            "emotional_variance_threshold": 0.15,  # 情感方差阈值
            "transition_smoothness_threshold": 0.5,  # 过渡平滑度阈值
            "climax_buildup_min_segments": 3,  # 高潮前最小铺垫段数
            "enable_fourier_analysis": True,  # 启用傅里叶分析[8](@ref)
            "enable_emotional_analysis": True,  # 启用情感分析
            "enable_genre_specific_analysis": True,  # 启用类型特定分析
            "output_format": "markdown",  # 输出格式
            "visualization_enabled": True,  # 启用可视化
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
                logger.info(f"从 {config_path} 加载用户配置")
            except Exception as e:
                logger.warning(f"加载配置文件失败: {e}, 使用默认配置")
        
        return default_config
    
    def _init_genre_standards(self) -> Dict[str, Dict]:
        """初始化小说类型特定的节奏标准"""
        # 基于搜索结果中的不同类型小说节奏特点[6](@ref)
        standards = {
            "玄幻": {
                "battle_density": 0.4,  # 战斗情节密度
                "cultivation_pace": 0.3,  # 修炼情节节奏
                "clan_complexity": 0.6,  # 宗门情节复杂度
                "treasure_fluctuation": 0.5,  # 宝物情节起伏度
                "design_points": [
                    "战斗情节要密集",
                    "修炼情节要平稳",
                    "宗门情节要复杂",
                    "宝物情节要起伏"
                ]
            },
            "科幻": {
                "tech_pace": 0.7,  # 科技情节节奏
                "ethics_depth": 0.6,  # 伦理情节深度
                "future_forward": 0.8,  # 未来情节前瞻性
                "exploration_mystery": 0.5,  # 探索情节神秘度
                "design_points": [
                    "科技情节要紧凑",
                    "伦理情节要深沉",
                    "未来情节要前瞻",
                    "探索情节要神秘"
                ]
            },
            "悬疑": {
                "clue_density": 0.6,  # 线索密度
                "tension_buildup": 0.7,  # 紧张感积累
                "reveal_timing": 0.5,  # 揭示时机
                "red_herring_ratio": 0.3,  # 红鲱鱼比例
            },
            "爱情": {
                "emotional_fluctuation": 0.8,  # 情感起伏
                "relationship_progression": 0.4,  # 关系进展节奏
                "conflict_intensity": 0.5,  # 冲突强度
                "resolution_pace": 0.6,  # 解决节奏
            },
            "武侠": {
                "action_density": 0.7,  # 动作密度
                "martial_arts_pace": 0.5,  # 武功节奏
                "sect_politics": 0.4,  # 门派政治
                "revenge_arc": 0.6,  # 复仇弧线
            }
        }
        return standards
    
    def _init_adjustment_strategies(self):
        """初始化节奏调整策略库"""
        # 基于搜索结果中的节奏调整工具箱[6](@ref)
        self.adjustment_strategies = {
            RhythmIssueType.MONOTONOUS_RHYTHM: [
                "增加情节密度：添加更多情节事件",
                "调整叙事模式比例：增加展示性叙述，减少告知性叙述",
                "引入子情节：添加与主线相关但节奏不同的子情节",
                "改变段落长度：交替使用长短段落创造节奏变化"
            ],
            RhythmIssueType.UNBALANCED_RHYTHM: [
                "重新分配情节强度：将高强度情节分散到不同章节",
                "调整情感分布：确保情感高潮均匀分布",
                "平衡信息密度：避免信息过载集中在少数段落",
                "优化对话与叙述比例：根据场景需要调整对话占比"
            ],
            RhythmIssueType.ABRUPT_TRANSITION: [
                "添加过渡段落：在节奏变化处插入缓冲内容",
                "使用连接词和短语：通过语言手段平滑过渡",
                "调整段落顺序：重新安排段落使节奏变化更渐进",
                "增加铺垫内容：为重大变化提前做准备"
            ],
            RhythmIssueType.LACKING_BUILDUP: [
                "增加铺垫段落：在高潮前添加更多准备内容",
                "强化伏笔：提前暗示即将发生的重要事件",
                "渐进增强紧张感：逐步提高情节的紧张程度",
                "延长准备阶段：给读者更多时间期待高潮"
            ],
            RhythmIssueType.EMOTIONAL_FLAT: [
                "增加情感波动：引入更多情感起伏",
                "强化角色反应：让角色对事件有更强烈的情感反应",
                "添加内心独白：展示角色的内心情感变化",
                "使用情感强烈的语言：选择更具情感色彩的词汇"
            ],
            RhythmIssueType.INFO_DENSITY_ISSUE: [
                "分散信息释放：将重要信息分散到多个段落",
                "简化复杂解释：用更易懂的方式呈现复杂信息",
                "增加示例和比喻：通过具体例子帮助理解",
                "调整信息节奏：交替使用信息密集和轻松的段落"
            ]
        }
    
    def load_novel_text(self, file_path: str) -> str:
        """
        加载小说文本
        
        Args:
            file_path: 小说文件路径
            
        Returns:
            小说文本内容
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"成功加载小说文件: {file_path}, 长度: {len(content)} 字符")
            return content
        except Exception as e:
            logger.error(f"加载小说文件失败: {e}")
            raise
    
    def parse_chapters(self, novel_text: str) -> Dict[int, Dict]:
        """
        解析小说章节
        
        Args:
            novel_text: 小说文本
            
        Returns:
            章节字典 {章节编号: {"title": 标题, "content": 内容, "paragraphs": 段落列表}}
        """
        chapters = {}
        
        # 使用正则表达式匹配章节标题
        chapter_patterns = [
            r'第[零一二三四五六七八九十百千万\d]+章[：:]?\s*(.*?)\n',
            r'Chapter\s+[\dIVXLCDM]+\s*[:：]?\s*(.*?)\n',
            r'CHAPTER\s+[\dIVXLCDM]+\s*[:：]?\s*(.*?)\n',
            r'^\s*(\d+)\.\s+(.*?)$',
        ]
        
        lines = novel_text.split('\n')
        current_chapter = 0
        current_title = ""
        current_content = []
        current_paragraphs = []
        
        for i, line in enumerate(lines):
            is_chapter_start = False
            chapter_title = ""
            
            for pattern in chapter_patterns:
                match = re.match(pattern, line)
                if match:
                    is_chapter_start = True
                    if len(match.groups()) > 0:
                        chapter_title = match.group(1) if match.group(1) else f"第{current_chapter+1}章"
                    break
            
            if is_chapter_start:
                # 保存前一章内容
                if current_chapter > 0 and current_content:
                    chapters[current_chapter] = {
                        "title": current_title,
                        "content": '\n'.join(current_content),
                        "paragraphs": current_paragraphs
                    }
                
                # 开始新章节
                current_chapter += 1
                current_title = chapter_title
                current_content = [f"# {chapter_title}"]
                current_paragraphs = []
                logger.debug(f"发现第 {current_chapter} 章: {chapter_title}")
            else:
                if line.strip():  # 非空行
                    current_content.append(line)
                    current_paragraphs.append(line)
                else:
                    # 空行表示段落分隔
                    if current_content and current_content[-1] != "":
                        current_content.append("")
        
        # 保存最后一章
        if current_chapter > 0 and current_content:
            chapters[current_chapter] = {
                "title": current_title,
                "content": '\n'.join(current_content),
                "paragraphs": current_paragraphs
            }
        
        # 如果没有检测到章节，将整个文本作为第1章
        if not chapters:
            paragraphs = [p for p in novel_text.split('\n\n') if p.strip()]
            chapters[1] = {
                "title": "第1章",
                "content": novel_text,
                "paragraphs": paragraphs
            }
            logger.warning("未检测到章节结构，将整个文本作为第1章")
        
        logger.info(f"解析完成，共 {len(chapters)} 章")
        return chapters
    
    def segment_narrative(self, chapters: Dict[int, Dict]) -> List[RhythmSegment]:
        """
        分割叙事文本为节奏分析段
        
        基于搜索结果中的叙事节奏量化表征方法[8](@ref)，
        将文本分割为适合节奏分析的段落，并识别叙述模式。
        
        Args:
            chapters: 章节字典
            
        Returns:
            节奏分段列表
        """
        logger.info("开始分割叙事文本...")
        
        segments = []
        segment_counter = 1
        segment_size = self.config["segment_size_words"]
        
        for chapter_num, chapter_data in chapters.items():
            paragraphs = chapter_data["paragraphs"]
            current_segment_text = []
            current_word_count = 0
            start_paragraph = 1
            
            for para_num, paragraph in enumerate(paragraphs, 1):
                # 计算段落字数
                para_words = len(jieba.lcut(paragraph))
                
                # 如果当前段累计字数超过阈值，或者这是新章节的开始
                if (current_word_count + para_words > segment_size and current_word_count > self.config["min_segment_words"]) or \
                   (current_segment_text and chapter_num != segments[-1].end_chapter if segments else False):
                    
                    # 创建新分段
                    segment_text = " ".join(current_segment_text)
                    segment_id = f"segment_{segment_counter:04d}"
                    
                    # 分析分段特征
                    narrative_mode = self._identify_narrative_mode(segment_text)
                    dialogue_ratio = self._calculate_dialogue_ratio(segment_text)
                    description_ratio = self._calculate_description_ratio(segment_text)
                    action_ratio = self._calculate_action_ratio(segment_text)
                    emotional_intensity = self._calculate_emotional_intensity(segment_text)
                    pace_score = self._calculate_pace_score(segment_text, narrative_mode)
                    
                    segment = RhythmSegment(
                        segment_id=segment_id,
                        start_chapter=chapter_num,
                        start_paragraph=start_paragraph,
                        end_chapter=chapter_num,
                        end_paragraph=para_num - 1,
                        narrative_mode=narrative_mode,
                        text_content=segment_text,
                        word_count=current_word_count,
                        sentence_count=segment_text.count('。') + segment_text.count('！') + segment_text.count('？'),
                        dialogue_ratio=dialogue_ratio,
                        description_ratio=description_ratio,
                        action_ratio=action_ratio,
                        emotional_intensity=emotional_intensity,
                        pace_score=pace_score
                    )
                    
                    segments.append(segment)
                    self.narrative_sequence.append(narrative_mode)
                    self.pace_sequence.append(pace_score)
                    self.emotional_sequence.append(emotional_intensity)
                    
                    # 重置当前段
                    segment_counter += 1
                    current_segment_text = [paragraph]
                    current_word_count = para_words
                    start_paragraph = para_num
                else:
                    # 添加到当前段
                    current_segment_text.append(paragraph)
                    current_word_count += para_words
            
            # 处理最后一分段
            if current_segment_text:
                segment_text = " ".join(current_segment_text)
                segment_id = f"segment_{segment_counter:04d}"
                
                narrative_mode = self._identify_narrative_mode(segment_text)
                dialogue_ratio = self._calculate_dialogue_ratio(segment_text)
                description_ratio = self._calculate_description_ratio(segment_text)
                action_ratio = self._calculate_action_ratio(segment_text)
                emotional_intensity = self._calculate_emotional_intensity(segment_text)
                pace_score = self._calculate_pace_score(segment_text, narrative_mode)
                
                segment = RhythmSegment(
                    segment_id=segment_id,
                    start_chapter=chapter_num,
                    start_paragraph=start_paragraph,
                    end_chapter=chapter_num,
                    end_paragraph=len(paragraphs),
                    narrative_mode=narrative_mode,
                    text_content=segment_text,
                    word_count=current_word_count,
                    sentence_count=segment_text.count('。') + segment_text.count('！') + segment_text.count('？'),
                    dialogue_ratio=dialogue_ratio,
                    description_ratio=description_ratio,
                    action_ratio=action_ratio,
                    emotional_intensity=emotional_intensity,
                    pace_score=pace_score
                )
                
                segments.append(segment)
                self.narrative_sequence.append(narrative_mode)
                self.pace_sequence.append(pace_score)
                self.emotional_sequence.append(emotional_intensity)
        
        logger.info(f"叙事分割完成，共 {len(segments)} 个分段")
        self.rhythm_segments = segments
        return segments
    
    def _identify_narrative_mode(self, text: str) -> NarrativeMode:
        """
        识别叙述模式
        
        基于搜索结果中的展示和告知两种叙述形式的自动识别方法[8](@ref)，
        判断文本段的主要叙述模式。
        
        Args:
            text: 文本内容
            
        Returns:
            叙述模式
        """
        # 识别对话
        dialogue_patterns = [r'["「](.*?)["」]', r'说道[:：]', r'问道[:：]', r'回答[:：]']
        dialogue_count = 0
        for pattern in dialogue_patterns:
            dialogue_count += len(re.findall(pattern, text))
        
        if dialogue_count > 0 and len(text) > 0:
            dialogue_ratio = dialogue_count / (text.count('。') + text.count('！') + text.count('？') + 1)
            if dialogue_ratio > 0.3:
                return NarrativeMode.DIALOGUE
        
        # 识别描述
        description_keywords = ['的', '地', '得', '着', '了', '过', '是', '有', '在']
        description_count = sum(1 for word in jieba.lcut(text) if word in description_keywords)
        
        if description_count / len(text) > 0.2:
            return NarrativeMode.DESCRIPTION
        
        # 识别动作
        action_keywords = ['跑', '走', '跳', '打', '杀', '攻', '防', '施', '放', '用']
        action_count = sum(1 for word in jieba.lcut(text) if word in action_keywords)
        
        if action_count > 0:
            return NarrativeMode.SHOWING
        
        # 识别反思
        reflection_keywords = ['想', '思考', '考虑', '觉得', '认为', '感觉', '回忆', '想起']
        reflection_count = sum(1 for word in jieba.lcut(text) if word in reflection_keywords)
        
        if reflection_count > 0:
            return NarrativeMode.REFLECTION
        
        # 默认告知模式
        return NarrativeMode.TELLING
    
    def _calculate_dialogue_ratio(self, text: str) -> float:
        """计算对话占比"""
        dialogue_patterns = [r'["「](.*?)["」]', r'说道[:：]', r'问道[:：]', r'回答[:：]']
        dialogue_chars = 0
        
        for pattern in dialogue_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                dialogue_chars += len(match)
        
        total_chars = len(text)
        return dialogue_chars / total_chars if total_chars > 0 else 0.0
    
    def _calculate_description_ratio(self, text: str) -> float:
        """计算描述占比"""
        # 描述性词汇
        desc_keywords = ['美丽', '高大', '宽阔', '明亮', '黑暗', '安静', '热闹', '古老', '现代']
        desc_count = 0
        
        words = jieba.lcut(text)
        for word in words:
            if word in desc_keywords:
                desc_count += 1
        
        return desc_count / len(words) if len(words) > 0 else 0.0
    
    def _calculate_action_ratio(self, text: str) -> float:
        """计算动作占比"""
        action_keywords = ['跑', '走', '跳', '打', '杀', '攻', '防', '施', '放', '用', '攻击', '防御', '施展']
        action_count = 0
        
        words = jieba.lcut(text)
        for word in words:
            if word in action_keywords:
                action_count += 1
        
        return action_count / len(words) if len(words) > 0 else 0.0
    
    def _calculate_emotional_intensity(self, text: str) -> float:
        """
        计算情感强度
        
        基于情感词典和文本分析，评估文本段的情感强度。
        
        Args:
            text: 文本内容
            
        Returns:
            情感强度(0-1)
        """
        # 情感关键词词典
        emotional_keywords = {
            'positive': ['高兴', '快乐', '喜悦', '兴奋', '幸福', '爱', '喜欢', '美好', '完美', '成功'],
            'negative': ['悲伤', '痛苦', '难过', '愤怒', '恨', '讨厌', '可怕', '恐怖', '失败', '死亡'],
            'intense': ['突然', '猛烈', '激烈', '强烈', '剧烈', '疯狂', '狂暴', '激烈', '震撼']
        }
        
        words = jieba.lcut(text)
        emotional_score = 0.0
        
        for word in words:
            if word in emotional_keywords['positive']:
                emotional_score += 0.1
            elif word in emotional_keywords['negative']:
                emotional_score += 0.15  # 负面情感通常更强
            elif word in emotional_keywords['intense']:
                emotional_score += 0.2
        
        # 标点符号的情感强度
        exclamation_count = text.count('！')
        question_count = text.count('？')
        emotional_score += exclamation_count * 0.05
        emotional_score += question_count * 0.03
        
        # 归一化到0-1范围
        emotional_score = min(1.0, emotional_score)
        
        return emotional_score
    
    def _calculate_pace_score(self, text: str, narrative_mode: NarrativeMode) -> float:
        """
        计算节奏评分
        
        基于句子长度、词汇密度和叙述模式评估节奏快慢。
        
        Args:
            text: 文本内容
            narrative_mode: 叙述模式
            
        Returns:
            节奏评分(0-1, 越高节奏越快)
        """
        # 句子数量
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.5  # 默认中等节奏
        
        # 平均句子长度
        avg_sentence_length = sum(len(s) for s in sentences) / len(sentences)
        
        # 短句比例（短句通常节奏更快）
        short_sentences = [s for s in sentences if len(s) < 15]
        short_sentence_ratio = len(short_sentences) / len(sentences)
        
        # 动作动词比例
        action_verbs = ['跑', '走', '跳', '打', '杀', '攻', '防', '冲', '飞', '逃']
        words = jieba.lcut(text)
        action_verb_count = sum(1 for word in words if word in action_verbs)
        action_verb_ratio = action_verb_count / len(words) if len(words) > 0 else 0
        
        # 根据叙述模式调整基准
        mode_adjustment = {
            NarrativeMode.SHOWING: 0.3,  # 展示模式通常节奏较快
            NarrativeMode.TELLING: -0.2,  # 告知模式通常节奏较慢
            NarrativeMode.DIALOGUE: 0.1,  # 对话模式节奏中等偏快
            NarrativeMode.DESCRIPTION: -0.3,  # 描述模式节奏较慢
            NarrativeMode.REFLECTION: -0.4  # 反思模式节奏最慢
        }
        
        # 计算基础节奏评分
        base_score = 0.5
        base_score += short_sentence_ratio * 0.3  # 短句比例影响
        base_score += action_verb_ratio * 0.2  # 动作动词比例影响
        base_score -= (avg_sentence_length / 100) * 0.2  # 长句减慢节奏
        
        # 应用叙述模式调整
        base_score += mode_adjustment.get(narrative_mode, 0)
        
        # 确保在0-1范围内
        return max(0.0, min(1.0, base_score))
    
    def analyze_rhythm_diversity(self) -> List[RhythmIssue]:
        """
        分析节奏多样性
        
        基于搜索结果中的节奏检查清单[6](@ref)，检测节奏是否多样，
        避免节奏单调的问题。
        
        Returns:
            节奏多样性问题列表
        """
        logger.info("开始分析节奏多样性...")
        issues = []
        
        if len(self.pace_sequence) < 3:
            logger.warning("分段数量不足，无法进行有效的节奏多样性分析")
            return issues
        
        # 计算节奏变化的统计指标
        pace_variance = statistics.variance(self.pace_sequence) if len(self.pace_sequence) > 1 else 0
        pace_range = max(self.pace_sequence) - min(self.pace_sequence) if self.pace_sequence else 0
        
        # 检测节奏单调问题
        if pace_variance < 0.02:  # 节奏变化方差太小
            issue_id = f"RHYTHM_MONOTONOUS_{len(issues)+1:03d}"
            issue = RhythmIssue(
                issue_id=issue_id,
                issue_type=RhythmIssueType.MONOTONOUS_RHYTHM,
                severity=self._assess_monotony_severity(pace_variance),
                location=f"全篇",
                description=f"节奏变化不足，整体节奏较为单调",
                evidence=[
                    f"节奏变化方差: {pace_variance:.4f} (阈值: 0.02)",
                    f"节奏范围: {pace_range:.2f}",
                    f"平均节奏评分: {statistics.mean(self.pace_sequence):.2f}",
                    f"节奏序列长度: {len(self.pace_sequence)} 段"
                ],
                suggested_fixes=self.adjustment_strategies[RhythmIssueType.MONOTONOUS_RHYTHM],
                confidence_score=0.8,
                rhythm_metrics={
                    "pace_variance": pace_variance,
                    "pace_range": pace_range,
                    "avg_pace": statistics.mean(self.pace_sequence)
                }
            )
            issues.append(issue)
        
        # 检测叙述模式多样性
        mode_counter = Counter(self.narrative_sequence)
        if len(mode_counter) < 3:  # 叙述模式种类太少
            issue_id = f"NARRATIVE_MONOTONOUS_{len(issues)+1:03d}"
            issue = RhythmIssue(
                issue_id=issue_id,
                issue_type=RhythmIssueType.MONOTONOUS_RHYTHM,
                severity=SeverityLevel.MODERATE,
                location=f"全篇",
                description=f"叙述模式单一，缺乏变化",
                evidence=[
                    f"使用的叙述模式种类: {len(mode_counter)} 种",
                    f"模式分布: {dict(mode_counter)}",
                    f"主要模式: {mode_counter.most_common(1)[0].value if mode_counter else '无'}"
                ],
                suggested_fixes=[
                    "增加展示性叙述比例",
                    "引入更多对话场景",
                    "交替使用不同叙述模式",
                    "在描述性段落中加入动作元素"
                ],
                confidence_score=0.7,
                rhythm_metrics={
                    "mode_count": len(mode_counter),
                    "mode_distribution": dict(mode_counter)
                }
            )
            issues.append(issue)
        
        logger.info(f"节奏多样性分析完成，发现 {len(issues)} 个问题")
        return issues
    
    def analyze_rhythm_balance(self) -> List[RhythmIssue]:
        """
        分析节奏平衡性
        
        基于搜索结果中的节奏检查清单[6](@ref)，检测节奏是否平衡，
        避免节奏分布不均的问题。
        
        Returns:
            节奏平衡性问题列表
        """
        logger.info("开始分析节奏平衡性...")
        issues = []
        
        if len(self.pace_sequence) < 5:
            logger.warning("分段数量不足，无法进行有效的节奏平衡性分析")
            return issues
        
        # 将节奏序列分成三部分（开头、中间、结尾）
        third = len(self.pace_sequence) // 3
        first_third = self.pace_sequence[:third]
        middle_third = self.pace_sequence[third:2*third]
        last_third = self.pace_sequence[2*third:]
        
        # 计算各部分的平均节奏
        avg_first = statistics.mean(first_third) if first_third else 0.5
        avg_middle = statistics.mean(middle_third) if middle_third else 0.5
        avg_last = statistics.mean(last_third) if last_third else 0.5
        
        # 检测节奏分布不均
        max_diff = max(abs(avg_first - avg_middle), abs(avg_middle - avg_last), abs(avg_first - avg_last))
        
        if max_diff > 0.3:  # 各部分节奏差异太大
            issue_id = f"RHYTHM_UNBALANCED_{len(issues)+1:03d}"
            issue = RhythmIssue(
                issue_id=issue_id,
                issue_type=RhythmIssueType.UNBALANCED_RHYTHM,
                severity=self._assess_imbalance_severity(max_diff),
                location=f"全篇",
                description=f"节奏分布不均，各部分节奏差异过大",
                evidence=[
                    f"开头部分平均节奏: {avg_first:.2f}",
                    f"中间部分平均节奏: {avg_middle:.2f}",
                    f"结尾部分平均节奏: {avg_last:.2f}",
                    f"最大节奏差异: {max_diff:.2f} (阈值: 0.3)",
                    f"节奏分布: 开头{len(first_third)}段, 中间{len(middle_third)}段, 结尾{len(last_third)}段"
                ],
                suggested_fixes=self.adjustment_strategies[RhythmIssueType.UNBALANCED_RHYTHM],
                confidence_score=0.75,
                rhythm_metrics={
                    "avg_pace_first": avg_first,
                    "avg_pace_middle": avg_middle,
                    "avg_pace_last": avg_last,
                    "max_pace_diff": max_diff
                }
            )
            issues.append(issue)
        
        # 检测快慢节奏段落分布
        fast_segments = [i for i, pace in enumerate(self.pace_sequence) if pace > self.config["pace_threshold_high"]]
        slow_segments = [i for i, pace in enumerate(self.pace_sequence) if pace < self.config["pace_threshold_low"]]
        
        # 检查快节奏段落是否过于集中
        if fast_segments:
            fast_clusters = self._find_clusters(fast_segments)
            if len(fast_clusters) < len(fast_segments) / 3:  # 快节奏段落过于集中
                issue_id = f"FAST_RHYTHM_CLUSTERED_{len(issues)+1:03d}"
                issue = RhythmIssue(
                    issue_id=issue_id,
                    issue_type=RhythmIssueType.UNBALANCED_RHYTHM,
                    severity=SeverityLevel.MODERATE,
                    location=self._get_cluster_locations(fast_clusters, self.rhythm_segments),
                    description=f"快节奏段落过于集中，缺乏分布平衡",
                    evidence=[
                        f"快节奏段落总数: {len(fast_segments)}",
                        f"快节奏集群数量: {len(fast_clusters)}",
                        f"集群分布: {fast_clusters}",
                        f"建议将快节奏段落更均匀地分布"
                    ],
                    suggested_fixes=[
                        "分散高强度情节到不同章节",
                        "在快节奏集群间插入缓冲段落",
                        "重新安排情节顺序以平衡节奏",
                        "将部分快节奏情节移到其他位置"
                    ],
                    confidence_score=0.7,
                    rhythm_metrics={
                        "fast_segment_count": len(fast_segments),
                        "fast_cluster_count": len(fast_clusters)
                    }
                )
                issues.append(issue)
        
        logger.info(f"节奏平衡性分析完成，发现 {len(issues)} 个问题")
        return issues
    
    def analyze_rhythm_transitions(self) -> List[RhythmIssue]:
        """
        分析节奏过渡
        
        基于搜索结果中的节奏检查清单[6](@ref)，检测节奏过渡是否自然，
        避免节奏变化突兀的问题[6](@ref)。
        
        Returns:
            节奏过渡问题列表
        """
        logger.info("开始分析节奏过渡...")
        issues = []
        
        if len(self.pace_sequence) < 3:
            logger.warning("分段数量不足，无法进行有效的节奏过渡分析")
            return issues
        
        # 计算节奏变化梯度
        pace_gradients = []
        for i in range(1, len(self.pace_sequence)):
            gradient = abs(self.pace_sequence[i] - self.pace_sequence[i-1])
            pace_gradients.append(gradient)
        
        # 检测突兀的节奏变化
        abrupt_transitions = []
        for i, gradient in enumerate(pace_gradients):
            if gradient > self.config["transition_smoothness_threshold"]:
                abrupt_transitions.append(i)
        
        for transition_idx in abrupt_transitions:
            segment_idx = transition_idx + 1  # 梯度对应的是从i-1到i的变化
            if segment_idx < len(self.rhythm_segments):
                segment = self.rhythm_segments[segment_idx]
                prev_segment = self.rhythm_segments[segment_idx-1]
                
                issue_id = f"ABRUPT_TRANSITION_{len(issues)+1:03d}"
                issue = RhythmIssue(
                    issue_id=issue_id,
                    issue_type=RhythmIssueType.ABRUPT_TRANSITION,
                    severity=self._assess_transition_severity(pace_gradients[transition_idx]),
                    location=f"{prev_segment.start_chapter}章{prev_segment.start_paragraph}段-{segment.end_chapter}章{segment.end_paragraph}段",
                    description=f"节奏变化突兀，从{prev_segment.pace_score:.2f}突然变化到{segment.pace_score:.2f}",
                    evidence=[
                        f"前一段落节奏: {prev_segment.pace_score:.2f}",
                        f"当前段落节奏: {segment.pace_score:.2f}",
                        f"变化幅度: {pace_gradients[transition_idx]:.2f} (阈值: {self.config['transition_smoothness_threshold']})",
                        f"前一段落模式: {prev_segment.narrative_mode.value}",
                        f"当前段落模式: {segment.narrative_mode.value}"
                    ],
                    suggested_fixes=self.adjustment_strategies[RhythmIssueType.ABRUPT_TRANSITION],
                    confidence_score=0.85,
                    rhythm_metrics={
                        "previous_pace": prev_segment.pace_score,
                        "current_pace": segment.pace_score,
                        "gradient": pace_gradients[transition_idx]
                    }
                )
                issues.append(issue)
        
        logger.info(f"节奏过渡分析完成，发现 {len(issues)} 个突兀过渡")
        return issues
    
    def analyze_climax_buildup(self) -> List[RhythmIssue]:
        """
        分析高潮铺垫
        
        基于搜索结果中的节奏检查清单[6](@ref)，检测高潮前是否有足够铺垫[6](@ref)，
        高潮后是否有适当缓冲[6](@ref)。
        
        Returns:
            高潮铺垫问题列表
        """
        logger.info("开始分析高潮铺垫...")
        issues = []
        
        if len(self.pace_sequence) < 10:
            logger.warning("分段数量不足，无法进行有效的高潮铺垫分析")
            return issues
        
        # 识别可能的节奏高潮（节奏评分峰值）
        pace_peaks = self._find_pace_peaks(self.pace_sequence)
        
        for peak_idx in pace_peaks:
            if peak_idx >= len(self.rhythm_segments):
                continue
            
            peak_segment = self.rhythm_segments[peak_idx]
            
            # 检查高潮前的铺垫
            buildup_segments = self._analyze_buildup_before_peak(peak_idx)
            
            if buildup_segments["insufficient"]:
                issue_id = f"LACKING_BUILDUP_{len(issues)+1:03d}"
                issue = RhythmIssue(
                    issue_id=issue_id,
                    issue_type=RhythmIssueType.LACKING_BUILDUP,
                    severity=self._assess_buildup_severity(buildup_segments),
                    location=f"第{peak_segment.start_chapter}章第{peak_segment.start_paragraph}段附近",
                    description=f"高潮段落前铺垫不足，可能影响情感冲击力",
                    evidence=[
                        f"高潮段落节奏评分: {peak_segment.pace_score:.2f}",
                        f"高潮前铺垫段数: {buildup_segments['count']}",
                        f"建议最小铺垫段数: {self.config['climax_buildup_min_segments']}",
                        f"铺垫段平均节奏: {buildup_segments['avg_pace']:.2f}",
                        f"铺垫段情感强度: {buildup_segments['avg_emotion']:.2f}"
                    ],
                    suggested_fixes=self.adjustment_strategies[RhythmIssueType.LACKING_BUILDUP],
                    confidence_score=0.8,
                    rhythm_metrics={
                        "peak_pace": peak_segment.pace_score,
                        "buildup_count": buildup_segments["count"],
                        "buildup_avg_pace": buildup_segments["avg_pace"],
                        "buildup_avg_emotion": buildup_segments["avg_emotion"]
                    }
                )
                issues.append(issue)
            
            # 检查高潮后的缓冲
            buffer_segments = self._analyze_buffer_after_peak(peak_idx)
            
            if buffer_segments["insufficient"]:
                issue_id = f"LACKING_BUFFER_{len(issues)+1:03d}"
                issue = RhythmIssue(
                    issue_id=issue_id,
                    issue_type=RhythmIssueType.ABRUPT_TRANSITION,
                    severity=SeverityLevel.MODERATE,
                    location=f"第{peak_segment.end_chapter}章第{peak_segment.end_paragraph}段之后",
                    description=f"高潮段落后缓冲不足，节奏下降过快",
                    evidence=[
                        f"高潮段落节奏评分: {peak_segment.pace_score:.2f}",
                        f"高潮后缓冲段数: {buffer_segments['count']}",
                        f"缓冲段平均节奏: {buffer_segments['avg_pace']:.2f}",
                        f"建议添加更多缓冲段落让读者情绪平稳过渡"
                    ],
                    suggested_fixes=[
                        "在高潮后添加反思或总结段落",
                        "引入轻松的子情节作为缓冲",
                        "增加角色对话来平复情绪",
                        "使用描述性段落降低节奏"
                    ],
                    confidence_score=0.7,
                    rhythm_metrics={
                        "peak_pace": peak_segment.pace_score,
                        "buffer_count": buffer_segments["count"],
                        "buffer_avg_pace": buffer_segments["avg_pace"]
                    }
                )
                issues.append(issue)
        
        logger.info(f"高潮铺垫分析完成，发现 {len(issues)} 个问题")
        return issues
    
    def analyze_emotional_rhythm(self) -> List[RhythmIssue]:
        """
        分析情感节奏
        
        基于搜索结果中的情感节奏合理性检查[6](@ref)和小说AI检测理论[7](@ref)，
        分析情感起伏是否自然合理。
        
        Returns:
            情感节奏问题列表
        """
        if not self.config["enable_emotional_analysis"]:
            logger.info("情感分析功能已禁用")
            return []
        
        logger.info("开始分析情感节奏...")
        issues = []
        
        if len(self.emotional_sequence) < 5:
            logger.warning("分段数量不足，无法进行有效的情感节奏分析")
            return issues
        
        # 计算情感变化的统计指标
        emotional_variance = statistics.variance(self.emotional_sequence) if len(self.emotional_sequence) > 1 else 0
        emotional_range = max(self.emotional_sequence) - min(self.emotional_sequence) if self.emotional_sequence else 0
        
        # 检测情感平淡问题
        if emotional_variance < self.config["emotional_variance_threshold"]:
            issue_id = f"EMOTIONAL_FLAT_{len(issues)+1:03d}"
            issue = RhythmIssue(
                issue_id=issue_id,
                issue_type=RhythmIssueType.EMOTIONAL_FLAT,
                severity=self._assess_emotional_flatness_severity(emotional_variance),
                location=f"全篇",
                description=f"情感起伏不足，整体情感较为平淡",
                evidence=[
                    f"情感变化方差: {emotional_variance:.4f} (阈值: {self.config['emotional_variance_threshold']})",
                    f"情感强度范围: {emotional_range:.2f}",
                    f"平均情感强度: {statistics.mean(self.emotional_sequence):.2f}",
                    f"情感高峰数量: {len([e for e in self.emotional_sequence if e > 0.7])}"
                ],
                suggested_fixes=self.adjustment_strategies[RhythmIssueType.EMOTIONAL_FLAT],
                confidence_score=0.8,
                rhythm_metrics={
                    "emotional_variance": emotional_variance,
                    "emotional_range": emotional_range,
                    "avg_emotion": statistics.mean(self.emotional_sequence)
                }
            )
            issues.append(issue)
        
        # 检测情感变化模式
        emotional_peaks = self._find_emotional_peaks(self.emotional_sequence)
        
        # 检查情感高峰分布
        if emotional_peaks:
            peak_distances = []
            for i in range(1, len(emotional_peaks)):
                distance = emotional_peaks[i] - emotional_peaks[i-1]
                peak_distances.append(distance)
            
            if peak_distances:
                avg_peak_distance = statistics.mean(peak_distances)
                if avg_peak_distance < 5:  # 情感高峰过于密集
                    issue_id = f"EMOTIONAL_PEAKS_DENSE_{len(issues)+1:03d}"
                    issue = RhythmIssue(
                        issue_id=issue_id,
                        issue_type=RhythmIssueType.EMOTIONAL_FLAT,
                        severity=SeverityLevel.MODERATE,
                        location=self._get_peak_locations(emotional_peaks, self.rhythm_segments),
                        description=f"情感高峰过于密集，可能降低情感冲击力",
                        evidence=[
                            f"情感高峰数量: {len(emotional_peaks)}",
                            f"平均高峰间距: {avg_peak_distance:.1f} 段",
                            f"建议最小间距: 8-10段",
                            f"情感高峰分布: {emotional_peaks}"
                        ],
                        suggested_fixes=[
                            "分散情感高潮到不同章节",
                            "降低次要情感高峰的强度",
                            "延长情感积累过程",
                            "合并相近的情感高峰"
                        ],
                        confidence_score=0.75,
                        rhythm_metrics={
                            "peak_count": len(emotional_peaks),
                            "avg_peak_distance": avg_peak_distance,
                            "peak_indices": emotional_peaks
                        }
                    )
                    issues.append(issue)
        
        logger.info(f"情感节奏分析完成，发现 {len(issues)} 个问题")
        return issues
    
    def analyze_genre_specific_rhythm(self, genre: str = "玄幻") -> List[RhythmIssue]:
        """
        分析类型特定的节奏
        
        基于搜索结果中的不同类型小说节奏特点[6](@ref)，
        检查节奏是否符合所选小说类型的特点。
        
        Args:
            genre: 小说类型，默认为"玄幻"
            
        Returns:
            类型特定节奏问题列表
        """
        if not self.config["enable_genre_specific_analysis"]:
            logger.info("类型特定分析功能已禁用")
            return []
        
        logger.info(f"开始分析{genre}类型特定的节奏...")
        issues = []
        
        if genre not in self.genre_standards:
            logger.warning(f"不支持的小说类型: {genre}，跳过类型特定分析")
            return issues
        
        genre_standard = self.genre_standards[genre]
        
        # 分析对话比例（不同类型对对话的要求不同）
        dialogue_ratios = [seg.dialogue_ratio for seg in self.rhythm_segments]
        avg_dialogue_ratio = statistics.mean(dialogue_ratios) if dialogue_ratios else 0
        
        # 玄幻小说通常对话比例较低，动作和描述比例较高
        if genre == "玄幻" and avg_dialogue_ratio > 0.4:
            issue_id = f"GENRE_DIALOGUE_HIGH_{len(issues)+1:03d}"
            issue = RhythmIssue(
                issue_id=issue_id,
                issue_type=RhythmIssueType.PACE_MISMATCH,
                severity=SeverityLevel.MODERATE,
                location=f"全篇",
                description=f"{genre}类型小说对话比例偏高，可能影响节奏特点",
                evidence=[
                    f"平均对话比例: {avg_dialogue_ratio:.2f}",
                    f"{genre}类型建议对话比例: <0.3",
                    f"设计要点: {genre_standard['design_points']}",
                    f"当前节奏可能不符合{genre}类型的典型特点"
                ],
                suggested_fixes=[
                    "减少对话段落，增加动作描写",
                    "将部分对话转化为叙述",
                    "增加修炼、战斗等类型特色情节",
                    "调整对话与叙述的比例"
                ],
                confidence_score=0.7,
                rhythm_metrics={
                    "avg_dialogue_ratio": avg_dialogue_ratio,
                    "genre_standard": genre_standard
                }
            )
            issues.append(issue)
        
        # 分析动作比例
        action_ratios = [seg.action_ratio for seg in self.rhythm_segments]
        avg_action_ratio = statistics.mean(action_ratios) if action_ratios else 0
        
        if genre == "玄幻" and avg_action_ratio < 0.2:
            issue_id = f"GENRE_ACTION_LOW_{len(issues)+1:03d}"
            issue = RhythmIssue(
                issue_id=issue_id,
                issue_type=RhythmIssueType.PACE_MISMATCH,
                severity=SeverityLevel.MODERATE,
                location=f"全篇",
                description=f"{genre}类型小说动作比例偏低，可能缺乏类型特色",
                evidence=[
                    f"平均动作比例: {avg_action_ratio:.2f}",
                    f"{genre}类型建议动作比例: >0.25",
                    f"设计要点: {genre_standard['design_points']}",
                    f"玄幻小说通常需要较高的动作密度"
                ],
                suggested_fixes=[
                    "增加战斗和动作场景",
                    "在描述中加入更多动作元素",
                    "提高情节的动作强度",
                    "添加修炼突破等动作性情节"
                ],
                confidence_score=0.7,
                rhythm_metrics={
                    "avg_action_ratio": avg_action_ratio,
                    "genre_standard": genre_standard
                }
            )
            issues.append(issue)
        
        logger.info(f"{genre}类型特定节奏分析完成，发现 {len(issues)} 个问题")
        return issues
    
    def _assess_monotony_severity(self, pace_variance: float) -> SeverityLevel:
        """评估节奏单调的严重程度"""
        if pace_variance < 0.01:
            return SeverityLevel.SEVERE
        elif pace_variance < 0.02:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR
    
    def _assess_imbalance_severity(self, max_diff: float) -> SeverityLevel:
        """评估节奏失衡的严重程度"""
        if max_diff > 0.4:
            return SeverityLevel.SEVERE
        elif max_diff > 0.3:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR
    
    def _assess_transition_severity(self, gradient: float) -> SeverityLevel:
        """评估过渡突兀的严重程度"""
        if gradient > 0.7:
            return SeverityLevel.SEVERE
        elif gradient > 0.5:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR
    
    def _assess_buildup_severity(self, buildup_segments: Dict) -> SeverityLevel:
        """评估铺垫不足的严重程度"""
        if buildup_segments["count"] == 0:
            return SeverityLevel.SEVERE
        elif buildup_segments["count"] < 2:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR
    
    def _assess_emotional_flatness_severity(self, variance: float) -> SeverityLevel:
        """评估情感平淡的严重程度"""
        if variance < 0.05:
            return SeverityLevel.SEVERE
        elif variance < 0.15:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR
    
    def _find_clusters(self, indices: List[int], max_gap: int = 2) -> List[List[int]]:
        """在索引列表中查找集群"""
        if not indices:
            return []
        
        indices.sort()
        clusters = []
        current_cluster = [indices[0]]
        
        for i in range(1, len(indices)):
            if indices[i] - indices[i-1] <= max_gap:
                current_cluster.append(indices[i])
            else:
                clusters.append(current_cluster)
                current_cluster = [indices[i]]
        
        clusters.append(current_cluster)
        return clusters
    
    def _get_cluster_locations(self, clusters: List[List[int]], segments: List[RhythmSegment]) -> str:
        """获取集群位置描述"""
        if not clusters:
            return "未知位置"
        
        # 只取第一个集群的位置
        first_cluster = clusters
        if not first_cluster:
            return "未知位置"
        
        first_idx = first_cluster
        last_idx = first_cluster[-1]
        
        if first_idx < len(segments) and last_idx < len(segments):
            first_seg = segments[first_idx]
            last_seg = segments[last_idx]
            return f"第{first_seg.start_chapter}章第{first_seg.start_paragraph}段-第{last_seg.end_chapter}章第{last_seg.end_paragraph}段"
        
        return "位置计算错误"
    
    def _find_pace_peaks(self, pace_sequence: List[float], threshold: float = 0.7) -> List[int]:
        """查找节奏高峰"""
        peaks = []
        for i in range(1, len(pace_sequence) - 1):
            if pace_sequence[i] > pace_sequence[i-1] and pace_sequence[i] > pace_sequence[i+1]:
                if pace_sequence[i] > threshold:
                    peaks.append(i)
        
        return peaks
    
    def _find_emotional_peaks(self, emotional_sequence: List[float], threshold: float = 0.6) -> List[int]:
        """查找情感高峰"""
        peaks = []
        for i in range(1, len(emotional_sequence) - 1):
            if emotional_sequence[i] > emotional_sequence[i-1] and emotional_sequence[i] > emotional_sequence[i+1]:
                if emotional_sequence[i] > threshold:
                    peaks.append(i)
        
        return peaks
    
    def _get_peak_locations(self, peak_indices: List[int], segments: List[RhythmSegment]) -> str:
        """获取高峰位置描述"""
        if not peak_indices:
            return "无高峰"
        
        locations = []
        for idx in peak_indices[:3]:  # 只取前3个高峰
            if idx < len(segments):
                seg = segments[idx]
                locations.append(f"第{seg.start_chapter}章")
        
        if locations:
            return ", ".join(set(locations))  # 去重
        return "位置计算错误"
    
    def _analyze_buildup_before_peak(self, peak_idx: int, lookback: int = 10) -> Dict[str, Any]:
        """分析高潮前的铺垫"""
        start_idx = max(0, peak_idx - lookback)
        buildup_segments = self.rhythm_segments[start_idx:peak_idx]
        
        if not buildup_segments:
            return {
                "count": 0,
                "avg_pace": 0,
                "avg_emotion": 0,
                "insufficient": True
            }
        
        pace_scores = [seg.pace_score for seg in buildup_segments]
        emotion_scores = [seg.emotional_intensity for seg in buildup_segments]
        
        return {
            "count": len(buildup_segments),
            "avg_pace": statistics.mean(pace_scores) if pace_scores else 0,
            "avg_emotion": statistics.mean(emotion_scores) if emotion_scores else 0,
            "insufficient": len(buildup_segments) < self.config["climax_buildup_min_segments"]
        }
    
    def _analyze_buffer_after_peak(self, peak_idx: int, lookahead: int = 5) -> Dict[str, Any]:
        """分析高潮后的缓冲"""
        end_idx = min(len(self.rhythm_segments), peak_idx + lookahead + 1)
        buffer_segments = self.rhythm_segments[peak_idx+1:end_idx]
        
        if not buffer_segments:
            return {
                "count": 0,
                "avg_pace": 0,
                "insufficient": True
            }
        
        pace_scores = [seg.pace_score for seg in buffer_segments]
        
        # 检查缓冲是否足够（节奏是否逐渐下降）
        if len(pace_scores) >= 2:
            pace_decline = pace_scores[0] - pace_scores[-1]
            insufficient = pace_decline > 0.4  # 节奏下降太快
        else:
            insufficient = True
        
        return {
            "count": len(buffer_segments),
            "avg_pace": statistics.mean(pace_scores) if pace_scores else 0,
            "insufficient": insufficient
        }
    
    def perform_fourier_analysis(self) -> Dict[str, Any]:
        """
        执行傅里叶分析
        
        基于搜索结果中的傅里叶变换等数学手段[8](@ref)，
        从叙述形式的时间序列中提取与叙事节奏相对应的特征量[8](@ref)。
        
        Returns:
            傅里叶分析结果
        """
        if not self.config["enable_fourier_analysis"]:
            logger.info("傅里叶分析功能已禁用")
            return {}
        
        logger.info("开始执行傅里叶分析...")
        
        if len(self.pace_sequence) < 10:
            logger.warning("节奏序列太短，无法进行有效的傅里叶分析")
            return {}
        
        # 将节奏序列转换为数值数组
        pace_array = np.array(self.pace_sequence)
        
        # 执行傅里叶变换
        n = len(pace_array)
        fft_result = fft.fft(pace_array)
        fft_freq = fft.fftfreq(n)
        
        # 计算幅度谱
        amplitude_spectrum = np.abs(fft_result)
        
        # 找到主要频率成分
        # 忽略直流分量（索引0）
        significant_indices = np.where(amplitude_spectrum[1:] > np.mean(amplitude_spectrum[1:]))[0] + 1
        significant_frequencies = fft_freq[significant_indices]
        significant_amplitudes = amplitude_spectrum[significant_indices]
        
        # 分析节奏周期性
        dominant_freq_idx = np.argmax(amplitude_spectrum[1:]) + 1
        dominant_frequency = fft_freq[dominant_freq_idx]
        dominant_period = 1 / abs(dominant_frequency) if dominant_frequency != 0 else 0
        
        result = {
            "sequence_length": n,
            "dominant_frequency": float(dominant_frequency),
            "dominant_period": float(dominant_period),
            "significant_frequencies": significant_frequencies.tolist(),
            "significant_amplitudes": significant_amplitudes.tolist(),
            "rhythm_regularity": float(np.std(amplitude_spectrum[1:])),
            "has_rhythmic_pattern": len(significant_frequencies) > 0
        }
        
        logger.info(f"傅里叶分析完成，主导周期: {dominant_period:.2f} 段")
        return result
    
    def generate_visualization(self, output_dir: str = "rhythm_visualization") -> List[str]:
        """
        生成节奏可视化图表
        
        Args:
            output_dir: 输出目录
            
        Returns:
            生成的图表文件路径列表
        """
        if not self.config["visualization_enabled"]:
            logger.info("可视化功能已禁用")
            return []
        
        logger.info("开始生成节奏可视化图表...")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        output_files = []
        
        # 1. 节奏评分时序图
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(self.pace_sequence)), self.pace_sequence, 'b-', linewidth=2, label='节奏评分')
        plt.axhline(y=self.config["pace_threshold_high"], color='r', linestyle='--', alpha=0.5, label='快节奏阈值')
        plt.axhline(y=self.config["pace_threshold_low"], color='g', linestyle='--', alpha=0.5, label='慢节奏阈值')
        plt.xlabel('段落序号')
        plt.ylabel('节奏评分')
        plt.title('小说节奏变化时序图')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        pace_chart_path = os.path.join(output_dir, "pace_timeline.png")
        plt.savefig(pace_chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        output_files.append(pace_chart_path)
        
        # 2. 情感强度时序图
        plt.figure(figsize=(12, 6))
        plt.plot(range(len(self.emotional_sequence)), self.emotional_sequence, 'r-', linewidth=2, label='情感强度')
        plt.axhline(y=0.5, color='gray', linestyle='--', alpha=0.3, label='中等情感')
        plt.xlabel('段落序号')
        plt.ylabel('情感强度')
        plt.title('小说情感变化时序图')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        emotion_chart_path = os.path.join(output_dir, "emotion_timeline.png")
        plt.savefig(emotion_chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        output_files.append(emotion_chart_path)
        
        # 3. 叙述模式分布图
        mode_counts = Counter(self.narrative_sequence)
        modes = [m.value for m in mode_counts.keys()]
        counts = list(mode_counts.values())
        
        plt.figure(figsize=(10, 6))
        colors = plt.cm.Set3(np.linspace(0, 1, len(modes)))
        plt.bar(modes, counts, color=colors)
        plt.xlabel('叙述模式')
        plt.ylabel('出现次数')
        plt.title('叙述模式分布图')
        plt.xticks(rotation=45)
        
        for i, count in enumerate(counts):
            plt.text(i, count + 0.5, str(count), ha='center')
        
        mode_chart_path = os.path.join(output_dir, "narrative_modes.png")
        plt.savefig(mode_chart_path, dpi=150, bbox_inches='tight')
        plt.close()
        output_files.append(mode_chart_path)
        
        # 4. 节奏与情感关系散点图
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(self.pace_sequence, self.emotional_sequence, 
                             c=range(len(self.pace_sequence)), cmap='viridis', 
                             alpha=0.6, s=50)
        plt.colorbar(scatter, label='段落序号')
        plt.xlabel('节奏评分')
        plt.ylabel('情感强度')
        plt.title('节奏与情感关系散点图')
        plt.grid(True, alpha=0.3)
        
        correlation = np.corrcoef(self.pace_sequence, self.emotional_sequence)[0, 1]
        plt.text(0.05, 0.95, f'相关系数: {correlation:.3f}', 
                transform=plt.gca().transAxes, fontsize=12,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        scatter_path = os.path.join(output_dir, "pace_emotion_scatter.png")
        plt.savefig(scatter_path, dpi=150, bbox_inches='tight')
        plt.close()
        output_files.append(scatter_path)
        
        # 5. 节奏变化梯度图
        if len(self.pace_sequence) > 1:
            pace_gradients = np.abs(np.diff(self.pace_sequence))
            
            plt.figure(figsize=(12, 6))
            plt.plot(range(len(pace_gradients)), pace_gradients, 'orange', linewidth=2, label='节奏变化梯度')
            plt.axhline(y=self.config["transition_smoothness_threshold"], 
                       color='r', linestyle='--', alpha=0.7, label='突兀阈值')
            plt.xlabel('过渡序号')
            plt.ylabel('节奏变化梯度')
            plt.title('节奏变化梯度图（检测突兀过渡）')
            plt.legend()
            plt.grid(True, alpha=0.3)
            
            gradient_path = os.path.join(output_dir, "pace_gradients.png")
            plt.savefig(gradient_path, dpi=150, bbox_inches='tight')
            plt.close()
            output_files.append(gradient_path)
        
        logger.info(f"可视化图表生成完成，共 {len(output_files)} 个文件")
        return output_files
    
    def run_comprehensive_analysis(self, novel_file: str, genre: str = "玄幻") -> Dict[str, Any]:
        """
        运行全面节奏分析
        
        Args:
            novel_file: 小说文件路径
            genre: 小说类型
            
        Returns:
            分析结果字典
        """
        logger.info(f"开始对 {novel_file} 进行全面节奏分析，类型: {genre}")
        
        try:
            # 1. 加载小说文本
            novel_text = self.load_novel_text(novel_file)
            
            # 2. 解析章节
            chapters = self.parse_chapters(novel_text)
            
            # 3. 分割叙事文本
            rhythm_segments = self.segment_narrative(chapters)
            
            # 4. 运行各项节奏分析
            all_issues = []
            
            # 节奏多样性分析
            diversity_issues = self.analyze_rhythm_diversity()
            all_issues.extend(diversity_issues)
            
            # 节奏平衡性分析
            balance_issues = self.analyze_rhythm_balance()
            all_issues.extend(balance_issues)
            
            # 节奏过渡分析
            transition_issues = self.analyze_rhythm_transitions()
            all_issues.extend(transition_issues)
            
            # 高潮铺垫分析
            climax_issues = self.analyze_climax_buildup()
            all_issues.extend(climax_issues)
            
            # 情感节奏分析
            emotional_issues = self.analyze_emotional_rhythm()
            all_issues.extend(emotional_issues)
            
            # 类型特定节奏分析
            genre_issues = self.analyze_genre_specific_rhythm(genre)
            all_issues.extend(genre_issues)
            
            # 5. 执行傅里叶分析
            fourier_results = self.perform_fourier_analysis()
            
            # 6. 生成统计信息
            stats = self._generate_statistics(all_issues, chapters, rhythm_segments)
            
            # 7. 生成可视化图表
            visualization_files = self.generate_visualization()
            
            # 8. 生成报告
            report = self._generate_report(all_issues, stats, fourier_results, novel_file, genre)
            
            result = {
                'success': True,
                'novel_file': novel_file,
                'genre': genre,
                'chapter_count': len(chapters),
                'segment_count': len(rhythm_segments),
                'issue_count': len(all_issues),
                'issues': [issue.to_dict() for issue in all_issues],
                'fourier_analysis': fourier_results,
                'statistics': stats,
                'visualization_files': visualization_files,
                'report': report,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"全面节奏分析完成，共发现 {len(all_issues)} 个节奏问题")
            return result
            
        except Exception as e:
            logger.error(f"节奏分析失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_statistics(self, issues: List[RhythmIssue], chapters: Dict[int, Dict], segments: List[RhythmSegment]) -> Dict[str, Any]:
        """生成统计信息"""
        stats = {
            'total_issues': len(issues),
            'issues_by_type': {},
            'issues_by_severity': {},
            'segment_statistics': {},
            'chapter_count': len(chapters),
            'total_segments': len(segments),
            'avg_segments_per_chapter': len(segments) / max(len(chapters), 1)
        }
        
        # 按类型统计
        for issue_type in RhythmIssueType:
            type_issues = [i for i in issues if i.issue_type == issue_type]
            stats['issues_by_type'][issue_type.value] = len(type_issues)
        
        # 按严重程度统计
        for severity in SeverityLevel:
            severity_issues = [i for i in issues if i.severity == severity]
            stats['issues_by_severity'][severity.value] = len(severity_issues)
        
        # 分段统计
        if segments:
            pace_scores = [seg.pace_score for seg in segments]
            emotion_scores = [seg.emotional_intensity for seg in segments]
            dialogue_ratios = [seg.dialogue_ratio for seg in segments]
            
            stats['segment_statistics'] = {
                'avg_pace_score': statistics.mean(pace_scores) if pace_scores else 0,
                'avg_emotion_score': statistics.mean(emotion_scores) if emotion_scores else 0,
                'avg_dialogue_ratio': statistics.mean(dialogue_ratios) if dialogue_ratios else 0,
                'pace_variance': statistics.variance(pace_scores) if len(pace_scores) > 1 else 0,
                'emotion_variance': statistics.variance(emotion_scores) if len(emotion_scores) > 1 else 0,
                'fast_segments': len([p for p in pace_scores if p > self.config["pace_threshold_high"]]),
                'slow_segments': len([p for p in pace_scores if p < self.config["pace_threshold_low"]])
            }
        
        return stats
    
    def _generate_report(self, issues: List[RhythmIssue], stats: Dict[str, Any], 
                        fourier_results: Dict[str, Any], novel_file: str, genre: str) -> str:
        """生成节奏分析报告"""
        report_lines = []
        
        # 报告头部
        report_lines.append("# 小说节奏分析报告")
        report_lines.append("")
        report_lines.append(f"**分析时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append(f"**分析文件**: {novel_file}")
        report_lines.append(f"**小说类型**: {genre}")
        report_lines.append(f"**章节数量**: {stats['chapter_count']}")
        report_lines.append(f"**分析分段**: {stats['total_segments']}")
        report_lines.append(f"**发现问题总数**: {stats['total_issues']}")
        report_lines.append("")
        
        # 统计摘要
        report_lines.append("## 统计摘要")
        report_lines.append("")
        
        # 节奏指标统计
        report_lines.append("### 节奏指标统计")
        seg_stats = stats.get('segment_statistics', {})
        if seg_stats:
            report_lines.append(f"- 平均节奏评分: {seg_stats.get('avg_pace_score', 0):.3f}")
            report_lines.append(f"- 平均情感强度: {seg_stats.get('avg_emotion_score', 0):.3f}")
            report_lines.append(f"- 平均对话比例: {seg_stats.get('avg_dialogue_ratio', 0):.3f}")
            report_lines.append(f"- 节奏变化方差: {seg_stats.get('pace_variance', 0):.4f}")
            report_lines.append(f"- 情感变化方差: {seg_stats.get('emotion_variance', 0):.4f}")
            report_lines.append(f"- 快节奏分段: {seg_stats.get('fast_segments', 0)} 个")
            report_lines.append(f"- 慢节奏分段: {seg_stats.get('slow_segments', 0)} 个")
        report_lines.append("")
        
        # 傅里叶分析结果
        if fourier_results:
            report_lines.append("### 傅里叶分析结果[8](@ref)")
            report_lines.append(f"- 主导周期: {fourier_results.get('dominant_period', 0):.2f} 段")
            report_lines.append(f"- 节奏规律性: {fourier_results.get('rhythm_regularity', 0):.4f}")
            report_lines.append(f"- 是否有节奏模式: {'是' if fourier_results.get('has_rhythmic_pattern') else '否'}")
            report_lines.append("")
        
        # 按问题类型统计
        report_lines.append("### 按问题类型统计")
        for issue_type, count in stats['issues_by_type'].items():
            report_lines.append(f"- {issue_type}: {count} 个")
        report_lines.append("")
        
        # 按严重程度统计
        report_lines.append("### 按严重程度统计")
        for severity, count in stats['issues_by_severity'].items():
            report_lines.append(f"- {severity}问题: {count} 个")
        report_lines.append("")
        
        # 详细问题列表
        report_lines.append("## 详细问题列表")
        report_lines.append("")
        
        # 按严重程度分组
        severity_groups = {}
        for issue in issues:
            severity = issue.severity.value
            if severity not in severity_groups:
                severity_groups[severity] = []
            severity_groups[severity].append(issue)
        
        # 按严重程度从高到低排序
        severity_order = ['致命', '严重', '中等', '轻微']
        for severity in severity_order:
            if severity in severity_groups:
                report_lines.append(f"### {severity}问题")
                report_lines.append("")
                
                for issue in severity_groups[severity]:
                    report_lines.append(f"#### {issue.issue_id}")
                    report_lines.append(f"- **类型**: {issue.issue_type.value}")
                    report_lines.append(f"- **位置**: {issue.location}")
                    report_lines.append(f"- **描述**: {issue.description}")
                    report_lines.append(f"- **置信度**: {issue.confidence_score:.2f}")
                    
                    if issue.rhythm_metrics:
                        report_lines.append("- **节奏指标**:")
                        for metric, value in issue.rhythm_metrics.items():
                            if isinstance(value, float):
                                report_lines.append(f"  - {metric}: {value:.3f}")
                            else:
                                report_lines.append(f"  - {metric}: {value}")
                    
                    if issue.evidence:
                        report_lines.append("- **证据**:")
                        for evidence in issue.evidence:
                            report_lines.append(f"  - {evidence}")
                    
                    if issue.suggested_fixes:
                        report_lines.append("- **修复建议**:")
                        for fix in issue.suggested_fixes:
                            report_lines.append(f"  - {fix}")
                    
                    report_lines.append("")
        
        # 节奏调整建议
        report_lines.append("## 节奏调整建议")
        report_lines.append("")
        
        # 基于节奏检查清单[6](@ref)提供建议
        report_lines.append("### 基于节奏检查清单的建议[6](@ref)")
        report_lines.append("")
        
        checklist_items = [
            "1. 节奏是否多样？ - 确保节奏有足够的变化",
            "2. 节奏是否平衡？ - 避免节奏分布不均",
            "3. 节奏是否渐进？ - 节奏变化应该自然渐进",
            "4. 情节节奏是否合理？ - 根据情节重要性调整节奏",
            "5. 情感节奏是否合理？ - 情感起伏要自然[7](@ref)",
            "6. 信息节奏是否合理？ - 信息释放要有节奏感",
            "7. 高潮前是否有铺垫？ - 确保高潮前有足够积累[6](@ref)",
            "8. 高潮后是否有缓冲？ - 高潮后要给读者喘息时间[6](@ref)",
            "9. 节奏过渡是否自然？ - 避免突兀的节奏变化[6](@ref)",
            "10. 节奏变化是否突兀？ - 变化应该有过渡"
        ]
        
        for item in checklist_items:
            report_lines.append(f"- {item}")
        report_lines.append("")
        
        # 类型特定建议
        if genre in self.genre_standards:
            report_lines.append(f"### {genre}类型节奏特点[6](@ref)")
            genre_std = self.genre_standards[genre]
            for point in genre_std.get('design_points', []):
                report_lines.append(f"- {point}")
            report_lines.append("")
        
        # 总结与改进建议
        report_lines.append("## 总结与改进建议")
        report_lines.append("")
        
        total_issues = stats['total_issues']
        if total_issues == 0:
            report_lines.append("✅ **优秀** - 未发现明显的节奏问题。")
            report_lines.append("建议继续保持当前的节奏控制水平，注意维护节奏多样性。")
        elif total_issues <= 5:
            report_lines.append("⚠️ **良好** - 发现少量节奏问题，建议抽时间优化。")
            report_lines.append("这些问题不会严重影响阅读体验，但优化后可以提升作品流畅度。")
        elif total_issues <= 15:
            report_lines.append("⚠️ **中等** - 发现较多节奏问题，建议制定优化计划。")
            report_lines.append("建议按照问题严重程度逐步优化，重点关注节奏过渡和高潮铺垫。")
        else:
            report_lines.append("❌ **需要改进** - 发现大量节奏问题，需要系统性的优化。")
            report_lines.append("建议重新审视整体节奏结构，重点关注节奏多样性和平衡性。")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("*本报告由小说节奏分析器脚本自动生成*")
        report_lines.append("*基于叙事节奏检测理论和方法论[6](@ref)[7](@ref)[8](@ref)*")
        
        return '\n'.join(report_lines)
    
    def save_report(self, report: str, output_file: Optional[str] = None) -> str:
        """
        保存分析报告
        
        Args:
            report: 报告内容
            output_file: 输出文件路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"rhythm_analysis_report_{timestamp}.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"分析报告已保存到: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"保存报告失败: {e}")
            raise

def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='小说节奏分析器脚本 - 检测叙事节奏、情感起伏和节奏过渡问题',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析单个小说文件
  python rhythm-analyzer.py novel.txt
  
  # 分析并指定小说类型
  python rhythm-analyzer.py novel.txt --genre 科幻
  
  # 分析并指定输出文件
  python rhythm-analyzer.py novel.txt -o report.md
  
  # 使用自定义配置文件
  python rhythm-analyzer.py novel.txt -c config.json
  
  # 生成可视化图表
  python rhythm-analyzer.py novel.txt --visualize
        """
    )
    
    parser.add_argument('novel_file', help='小说文件路径')
    parser.add_argument('-g', '--genre', default='玄幻', help='小说类型（玄幻/科幻/悬疑/爱情/武侠）')
    parser.add_argument('-o', '--output', help='分析报告输出文件路径')
    parser.add_argument('-c', '--config', help='配置文件路径')
    parser.add_argument('--visualize', action='store_true', help='生成可视化图表')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志信息')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 检查文件是否存在
    if not os.path.exists(args.novel_file):
        print(f"错误: 文件 '{args.novel_file}' 不存在")
        sys.exit(1)
    
    # 检查小说类型是否支持
    supported_genres = ['玄幻', '科幻', '悬疑', '爱情', '武侠']
    if args.genre not in supported_genres:
        print(f"警告: 小说类型 '{args.genre}' 不在支持列表中，将使用默认分析")
        print(f"支持的类型: {', '.join(supported_genres)}")
    
    try:
        # 创建分析器实例
        analyzer = NovelRhythmAnalyzer(args.config)
        
        # 运行全面分析
        print(f"开始分析小说: {args.novel_file}")
        print(f"小说类型: {args.genre}")
        result = analyzer.run_comprehensive_analysis(args.novel_file, args.genre)
        
        if result['success']:
            print(f"分析完成，共发现 {result['issue_count']} 个节奏问题")
            print(f"涉及 {result['chapter_count']} 章，{result['segment_count']} 个分段")
            
            # 生成并保存报告
            report = result['report']
            
            if args.output:
                output_file = args.output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"rhythm_analysis_report_{timestamp}.md"
            
            analyzer.save_report(report, output_file)
            print(f"分析报告已保存到: {output_file}")
            
            # 显示可视化信息
            if args.visualize and result.get('visualization_files'):
                print(f"可视化图表已生成: {len(result['visualization_files'])} 个文件")
                for file_path in result['visualization_files']:
                    print(f"  - {file_path}")
            
            # 显示摘要
            print("\n=== 分析摘要 ===")
            stats = result['statistics']
            
            print(f"问题类型分布:")
            for issue_type, count in stats['issues_by_type'].items():
                print(f"  {issue_type}: {count}")
            
            print(f"\n严重程度分布:")
            for severity, count in stats['issues_by_severity'].items():
                print(f"  {severity}: {count}")
            
            # 显示节奏指标
            seg_stats = stats.get('segment_statistics', {})
            if seg_stats:
                print(f"\n节奏指标:")
                print(f"  平均节奏评分: {seg_stats.get('avg_pace_score', 0):.3f}")
                print(f"  平均情感强度: {seg_stats.get('avg_emotion_score', 0):.3f}")
                print(f"  节奏变化方差: {seg_stats.get('pace_variance', 0):.4f}")
            
            # 显示傅里叶分析结果
            fourier = result.get('fourier_analysis', {})
            if fourier:
                print(f"\n傅里叶分析[8](@ref):")
                print(f"  主导周期: {fourier.get('dominant_period', 0):.2f} 段")
                print(f"  节奏规律性: {fourier.get('rhythm_regularity', 0):.4f}")
            
            # 显示最严重的问题
            severe_issues = [i for i in result['issues'] if i['severity'] in ['致命', '严重']]
            if severe_issues:
                print(f"\n⚠️ 发现 {len(severe_issues)} 个严重问题，建议优先处理:")
                for issue in severe_issues[:3]:
                    print(f"  - {issue['location']}: {issue['description']}")
            
        else:
            print(f"分析失败: {result['error']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n分析被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"分析过程中发生错误: {e}")
        logger.exception("分析失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
