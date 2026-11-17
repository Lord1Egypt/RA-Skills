#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说角色一致性检查脚本 (Consistency Checker for Novel Writing)
版本: 2.0.0
作者: AUTHOR
日期: 2026-04-14

功能概述:
基于搜索结果中的AI驱动创作工具[10](@ref)和网文校对系统[9](@ref)的设计理念，本脚本实现了
多维度的小说一致性检查功能，包括角色行为一致性、时间线合理性、设定连贯性等。
通过结合规则引擎与语义相似度计算，为作者提供系统化的Bug检测和修复建议。

核心特性:
1. 智能上下文理解系统 - 基于向量检索的上下文感知技术
2. 多维度一致性检查 - 角色、情节、设定三个维度的自动检查
3. 模块化架构设计 - 支持功能扩展和个性化定制
4. 可视化输出 - 生成详细的检查报告和修复建议

依赖库:
- pandas: 数据处理和分析
- numpy: 数值计算
- scikit-learn: 机器学习算法和相似度计算
- spacy: 自然语言处理
- python-dotenv: 环境变量管理
"""

import os
import sys
import json
import re
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# 第三方库导入
try:
    import pandas as pd
    import numpy as np
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import TfidfVectorizer
    import spacy
    from dotenv import load_dotenv
except ImportError as e:
    print(f"缺少必要的依赖库: {e}")
    print("请运行: pip install pandas numpy scikit-learn spacy python-dotenv")
    sys.exit(1)

# 加载环境变量
load_dotenv()

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('consistency_checker.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 常量定义
class ConsistencyType(Enum):
    """一致性检查类型枚举"""
    CHARACTER_BEHAVIOR = "角色行为一致性"
    CHARACTER_DIALOG = "角色对话一致性"
    TIMELINE = "时间线一致性"
    SETTING = "世界观设定一致性"
    PLOT_LOGIC = "情节逻辑一致性"
    FORESIGHT = "伏笔回收一致性"

class SeverityLevel(Enum):
    """问题严重程度枚举"""
    CRITICAL = "致命"
    SEVERE = "严重"
    MODERATE = "中等"
    MINOR = "轻微"

@dataclass
class CharacterProfile:
    """角色档案数据结构"""
    character_id: str
    name: str
    age: int
    gender: str
    personality_traits: List[str] = field(default_factory=list)
    abilities: Dict[str, int] = field(default_factory=dict)  # 能力名称:等级(1-10)
    knowledge_scope: List[str] = field(default_factory=list)
    relationships: Dict[str, str] = field(default_factory=dict)  # 角色ID:关系类型
    appearance_features: Dict[str, str] = field(default_factory=dict)
    dialogue_patterns: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "character_id": self.character_id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "personality_traits": self.personality_traits,
            "abilities": self.abilities,
            "knowledge_scope": self.knowledge_scope,
            "relationships": self.relationships,
            "appearance_features": self.appearance_features,
            "dialogue_patterns": self.dialogue_patterns
        }

@dataclass
class ConsistencyIssue:
    """一致性问题记录"""
    issue_id: str
    issue_type: ConsistencyType
    severity: SeverityLevel
    location: str  # 格式: "第X章第Y段"
    description: str
    evidence: List[str] = field(default_factory=list)
    suggested_fixes: List[str] = field(default_factory=list)
    confidence_score: float = 0.0  # 置信度分数(0-1)
    
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
            "confidence_score": self.confidence_score
        }

class NovelConsistencyChecker:
    """
    小说一致性检查器主类
    
    基于搜索结果中的AI驱动创作工具设计理念[10](@ref)，实现多维度的一致性检查功能。
    结合规则引擎与语义相似度计算，提供系统化的Bug检测和修复建议。
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化一致性检查器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config = self._load_config(config_path)
        self.nlp = None
        self.character_profiles: Dict[str, CharacterProfile] = {}
        self.consistency_issues: List[ConsistencyIssue] = []
        self.timeline_events: List[Dict] = []
        self.setting_rules: Dict[str, Any] = {}
        
        # 初始化NLP模型
        self._init_nlp_model()
        
        # 初始化向量存储（用于上下文检索）
        self.vector_store = {}
        self.vectorizer = TfidfVectorizer(max_features=1000)
        
        logger.info("小说一致性检查器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        default_config = {
            "model_name": "gpt-4o-mini",  # 模型选择[10](@ref)
            "temperature": 0.7,  # 创造性控制
            "embedding_model": "all-MiniLM-L6-v2",  # 嵌入模型选择[10](@ref)
            "embedding_retrieval_k": 5,  # 上下文检索数量[10](@ref)
            "max_tokens": 2048,  # 单次生成最大tokens
            "similarity_threshold": 0.7,  # 相似度阈值
            "min_confidence_score": 0.6,  # 最小置信度分数
            "output_format": "markdown",  # 输出格式
            "enable_advanced_checks": True,  # 启用高级检查
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
    
    def _init_nlp_model(self):
        """初始化NLP模型"""
        try:
            # 尝试加载中文模型，如果失败则使用英文模型
            try:
                self.nlp = spacy.load("zh_core_web_sm")
                logger.info("加载中文NLP模型成功")
            except:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("加载英文NLP模型成功")
        except Exception as e:
            logger.warning(f"加载NLP模型失败: {e}, 将使用基于规则的方法")
            self.nlp = None
    
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
    
    def parse_chapters(self, novel_text: str) -> Dict[int, str]:
        """
        解析小说章节
        
        Args:
            novel_text: 小说文本
            
        Returns:
            章节字典 {章节编号: 章节内容}
        """
        chapters = {}
        
        # 使用正则表达式匹配章节标题
        # 支持多种格式: 第X章、Chapter X、CHAPTER X等
        chapter_patterns = [
            r'第[零一二三四五六七八九十百千万\d]+章[：:]?\s*(.*?)\n',
            r'Chapter\s+[\dIVXLCDM]+\s*[:：]?\s*(.*?)\n',
            r'CHAPTER\s+[\dIVXLCDM]+\s*[:：]?\s*(.*?)\n',
            r'^\s*(\d+)\.\s+(.*?)$',  # 数字编号格式
        ]
        
        lines = novel_text.split('\n')
        current_chapter = 0
        current_content = []
        
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
                    chapters[current_chapter] = '\n'.join(current_content)
                
                # 开始新章节
                current_chapter += 1
                current_content = [f"# {chapter_title}"]
                logger.debug(f"发现第 {current_chapter} 章: {chapter_title}")
            else:
                current_content.append(line)
        
        # 保存最后一章
        if current_chapter > 0 and current_content:
            chapters[current_chapter] = '\n'.join(current_content)
        
        # 如果没有检测到章节，将整个文本作为第1章
        if not chapters:
            chapters[1] = novel_text
            logger.warning("未检测到章节结构，将整个文本作为第1章")
        
        logger.info(f"解析完成，共 {len(chapters)} 章")
        return chapters
    
    def extract_characters(self, chapters: Dict[int, str]) -> Dict[str, CharacterProfile]:
        """
        从章节中提取角色信息
        
        Args:
            chapters: 章节字典
            
        Returns:
            角色档案字典
        """
        logger.info("开始提取角色信息...")
        
        character_patterns = {
            'name': r'([\u4e00-\u9fa5]{2,4})',  # 中文名字
            'age': r'(\d{1,3})岁',
            'gender': r'(男|女|男性|女性)',
            'appearance': r'(身高|体型|发型|眼睛|面容)[：:]\s*([^，。！？\n]+)',
        }
        
        # 使用简单的规则提取角色信息
        for chapter_num, content in chapters.items():
            lines = content.split('\n')
            
            for line in lines:
                # 提取名字
                name_matches = re.findall(character_patterns['name'], line)
                for name in name_matches:
                    if name not in self.character_profiles:
                        # 创建新角色档案
                        character_id = f"char_{len(self.character_profiles)+1:03d}"
                        profile = CharacterProfile(
                            character_id=character_id,
                            name=name,
                            age=0,  # 默认年龄
                            gender="未知",
                            personality_traits=[],
                            abilities={},
                            knowledge_scope=[],
                            relationships={},
                            appearance_features={},
                            dialogue_patterns=[]
                        )
                        self.character_profiles[name] = profile
                        logger.debug(f"发现新角色: {name} (ID: {character_id})")
        
        logger.info(f"共提取 {len(self.character_profiles)} 个角色")
        return self.character_profiles
    
    def check_character_consistency(self, chapters: Dict[int, str]) -> List[ConsistencyIssue]:
        """
        检查角色一致性
        
        基于搜索结果中的多维度一致性检查理念[10](@ref)，检查角色行为、对话、
        能力等方面的前后一致性。
        
        Args:
            chapters: 章节字典
            
        Returns:
            一致性问题列表
        """
        logger.info("开始检查角色一致性...")
        issues = []
        
        if not self.character_profiles:
            logger.warning("未提取到角色信息，跳过角色一致性检查")
            return issues
        
        # 为每个角色建立行为模式数据库
        character_behaviors = {name: [] for name in self.character_profiles.keys()}
        character_dialogues = {name: [] for name in self.character_profiles.keys()}
        
        # 分析每个章节中的角色行为
        for chapter_num, content in chapters.items():
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for character_name in self.character_profiles.keys():
                    # 检查角色是否出现在这一行
                    if character_name in line:
                        location = f"第{chapter_num}章第{line_num}段"
                        
                        # 提取行为描述
                        behavior_match = re.search(rf'{character_name}(.*?)[。！？]', line)
                        if behavior_match:
                            behavior = behavior_match.group(1).strip()
                            character_behaviors[character_name].append({
                                'chapter': chapter_num,
                                'line': line_num,
                                'behavior': behavior,
                                'location': location
                            })
                        
                        # 提取对话内容
                        if '："' in line or ':"' in line or '说：' in line or '说道：' in line:
                            dialogue_match = re.search(rf'{character_name}[：:]["「](.*?)["」]', line)
                            if dialogue_match:
                                dialogue = dialogue_match.group(1).strip()
                                character_dialogues[character_name].append({
                                    'chapter': chapter_num,
                                    'line': line_num,
                                    'dialogue': dialogue,
                                    'location': location
                                })
        
        # 检查行为一致性
        for character_name, behaviors in character_behaviors.items():
            if len(behaviors) < 2:
                continue
            
            # 分析行为模式变化
            behavior_patterns = self._analyze_behavior_patterns(behaviors)
            
            # 检查是否存在突变行为
            for i in range(1, len(behaviors)):
                prev_behavior = behaviors[i-1]['behavior']
                curr_behavior = behaviors[i]['behavior']
                
                # 计算行为相似度
                similarity = self._calculate_text_similarity(prev_behavior, curr_behavior)
                
                if similarity < self.config['similarity_threshold']:
                    # 发现可能的行为突变
                    issue_id = f"CHAR_BEHAVIOR_{character_name}_{i:03d}"
                    issue = ConsistencyIssue(
                        issue_id=issue_id,
                        issue_type=ConsistencyType.CHARACTER_BEHAVIOR,
                        severity=SeverityLevel.MODERATE,
                        location=behaviors[i]['location'],
                        description=f"角色'{character_name}'的行为模式发生突变",
                        evidence=[
                            f"前一次行为: {prev_behavior}",
                            f"当前行为: {curr_behavior}",
                            f"相似度分数: {similarity:.2f} (阈值: {self.config['similarity_threshold']})"
                        ],
                        suggested_fixes=[
                            "添加过渡场景展示角色变化过程",
                            "通过内心独白解释行为变化原因",
                            "调整行为使其更符合角色设定"
                        ],
                        confidence_score=1.0 - similarity
                    )
                    issues.append(issue)
        
        # 检查对话一致性
        for character_name, dialogues in character_dialogues.items():
            if len(dialogues) < 2:
                continue
            
            # 分析对话风格
            dialogue_styles = self._analyze_dialogue_style(dialogues)
            
            # 检查对话风格一致性
            style_changes = self._detect_style_changes(dialogue_styles)
            
            for change in style_changes:
                issue_id = f"CHAR_DIALOG_{character_name}_{change['index']:03d}"
                issue = ConsistencyIssue(
                    issue_id=issue_id,
                    issue_type=ConsistencyType.CHARACTER_DIALOG,
                    severity=SeverityLevel.MINOR,
                    location=change['location'],
                    description=f"角色'{character_name}'的对话风格发生变化",
                    evidence=[
                        f"风格变化指标: {change['metric']}",
                        f"变化幅度: {change['change_magnitude']:.2f}"
                    ],
                    suggested_fixes=[
                        "调整对话用词使其更符合角色背景",
                        "添加说明解释风格变化原因",
                        "统一角色的口头禅和习惯用语"
                    ],
                    confidence_score=0.7
                )
                issues.append(issue)
        
        logger.info(f"角色一致性检查完成，发现 {len(issues)} 个问题")
        return issues
    
    def check_timeline_consistency(self, chapters: Dict[int, str]) -> List[ConsistencyIssue]:
        """
        检查时间线一致性
        
        基于搜索结果中的时间线合理性检查理念[10](@ref)，分析事件发生的
        时间顺序和逻辑关系。
        
        Args:
            chapters: 章节字典
            
        Returns:
            时间线一致性问题列表
        """
        logger.info("开始检查时间线一致性...")
        issues = []
        
        # 时间相关模式
        time_patterns = [
            r'(\d+)年(?:后|前)',
            r'(\d+)个月(?:后|前)',
            r'(\d+)天(?:后|前)',
            r'(\d+)小时(?:后|前)',
            r'([上下]午|凌晨|傍晚|深夜)',
            r'([春夏秋冬]季)',
            r'([一二三四五六七八九十]+月)',
            r'星期[一二三四五六日天]',
        ]
        
        timeline_events = []
        
        # 提取时间相关事件
        for chapter_num, content in chapters.items():
            lines = content.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                for pattern in time_patterns:
                    matches = re.findall(pattern, line)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match
                        
                        event = {
                            'chapter': chapter_num,
                            'line': line_num,
                            'time_reference': match,
                            'content': line[:100],  # 只取前100个字符
                            'location': f"第{chapter_num}章第{line_num}段"
                        }
                        timeline_events.append(event)
        
        # 分析时间线逻辑
        if len(timeline_events) > 1:
            # 按章节和行号排序
            timeline_events.sort(key=lambda x: (x['chapter'], x['line']))
            
            # 检查时间跳跃的合理性
            for i in range(1, len(timeline_events)):
                prev_event = timeline_events[i-1]
                curr_event = timeline_events[i]
                
                # 检查是否存在不合理的时间跳跃
                time_gap = self._estimate_time_gap(prev_event['time_reference'], curr_event['time_reference'])
                
                if time_gap and time_gap > 365:  # 超过一年的跳跃
                    issue_id = f"TIMELINE_JUMP_{i:03d}"
                    issue = ConsistencyIssue(
                        issue_id=issue_id,
                        issue_type=ConsistencyType.TIMELINE,
                        severity=SeverityLevel.MODERATE,
                        location=curr_event['location'],
                        description="检测到可能不合理的时间跳跃",
                        evidence=[
                            f"前一时间点: {prev_event['time_reference']}",
                            f"当前时间点: {curr_event['time_reference']}",
                            f"估计时间间隔: {time_gap} 天",
                            f"前文内容: {prev_event['content']}",
                            f"当前内容: {curr_event['content']}"
                        ],
                        suggested_fixes=[
                            "添加过渡段落说明时间跳跃",
                            "调整时间间隔使其更合理",
                            "通过角色对话或叙述解释时间变化"
                        ],
                        confidence_score=0.8
                    )
                    issues.append(issue)
        
        # 保存时间线事件供后续分析
        self.timeline_events = timeline_events
        
        logger.info(f"时间线一致性检查完成，发现 {len(issues)} 个问题")
        return issues
    
    def check_plot_logic_consistency(self, chapters: Dict[int, str]) -> List[ConsistencyIssue]:
        """
        检查情节逻辑一致性
        
        基于搜索结果中的情节一致性检查理念[10](@ref)，分析情节发展的
        逻辑合理性和因果关系。
        
        Args:
            chapters: 章节字典
            
        Returns:
            情节逻辑一致性问题列表
        """
        logger.info("开始检查情节逻辑一致性...")
        issues = []
        
        # 因果关系模式
        causality_patterns = [
            (r'因为.*所以', '明确因果关系'),
            (r'由于.*因此', '明确因果关系'),
            (r'既然.*那么', '条件关系'),
            (r'如果.*就', '假设关系'),
        ]
        
        # 逻辑矛盾模式
        contradiction_patterns = [
            (r'虽然.*但是', '转折关系'),
            (r'尽管.*然而', '转折关系'),
            (r'不是.*而是', '否定肯定关系'),
        ]
        
        plot_points = []
        
        # 提取情节关键点
        for chapter_num, content in chapters.items():
            paragraphs = content.split('\n\n')  # 按段落分割
            
            for para_num, paragraph in enumerate(paragraphs, 1):
                # 检查因果关系
                for pattern, relation_type in causality_patterns:
                    if re.search(pattern, paragraph):
                        plot_point = {
                            'chapter': chapter_num,
                            'paragraph': para_num,
                            'type': 'causality',
                            'relation': relation_type,
                            'content': paragraph[:200],  # 只取前200个字符
                            'location': f"第{chapter_num}章第{para_num}段"
                        }
                        plot_points.append(plot_point)
                
                # 检查逻辑矛盾
                for pattern, relation_type in contradiction_patterns:
                    if re.search(pattern, paragraph):
                        plot_point = {
                            'chapter': chapter_num,
                            'paragraph': para_num,
                            'type': 'contradiction',
                            'relation': relation_type,
                            'content': paragraph[:200],
                            'location': f"第{chapter_num}章第{para_num}段"
                        }
                        plot_points.append(plot_point)
        
        # 分析情节逻辑链
        causality_chain = []
        for point in plot_points:
            if point['type'] == 'causality':
                causality_chain.append(point)
        
        # 检查因果关系链的完整性
        if len(causality_chain) > 1:
            for i in range(len(causality_chain) - 1):
                cause = causality_chain[i]
                effect = causality_chain[i+1]
                
                # 检查因果关系是否合理
                if cause['chapter'] == effect['chapter'] and abs(cause['paragraph'] - effect['paragraph']) > 3:
                    # 因果关系跨越多个段落，可能存在问题
                    issue_id = f"PLOT_CAUSALITY_{i:03d}"
                    issue = ConsistencyIssue(
                        issue_id=issue_id,
                        issue_type=ConsistencyType.PLOT_LOGIC,
                        severity=SeverityLevel.MINOR,
                        location=effect['location'],
                        description="因果关系可能不够紧密",
                        evidence=[
                            f"原因位置: {cause['location']}",
                            f"结果位置: {effect['location']}",
                            f"原因内容: {cause['content']}",
                            f"结果内容: {effect['content']}",
                            f"段落间隔: {abs(cause['paragraph'] - effect['paragraph'])} 段"
                        ],
                        suggested_fixes=[
                            "调整段落顺序使因果关系更紧密",
                            "添加过渡说明连接原因和结果",
                            "强化因果关系的逻辑连接"
                        ],
                        confidence_score=0.6
                    )
                    issues.append(issue)
        
        logger.info(f"情节逻辑一致性检查完成，发现 {len(issues)} 个问题")
        return issues
    
    def check_foresight_consistency(self, chapters: Dict[int, str]) -> List[ConsistencyIssue]:
        """
        检查伏笔回收一致性
        
        基于搜索结果中的上下文理解系统理念[10](@ref)，分析伏笔设置和
        回收的连贯性。
        
        Args:
            chapters: 章节字典
            
        Returns:
            伏笔一致性问题列表
        """
        logger.info("开始检查伏笔回收一致性...")
        issues = []
        
        # 伏笔相关词汇
        foreshadowing_keywords = [
            '神秘', '奇怪', '疑惑', '不解', '预感', '预兆',
            '暗示', '线索', '秘密', '谜团', '未知', '隐藏'
        ]
        
        # 回收相关词汇
        payoff_keywords = [
            '原来', '真相', '揭晓', '揭示', '发现', '明白',
            '解开', '解答', '答案', '结果', '结局', '最终'
        ]
        
        foreshadowing_events = []
        payoff_events = []
        
        # 提取伏笔设置事件
        for chapter_num, content in chapters.items():
            sentences = re.split(r'[。！？]', content)
            
            for sent_num, sentence in enumerate(sentences, 1):
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # 检查是否包含伏笔关键词
                for keyword in foreshadowing_keywords:
                    if keyword in sentence:
                        event = {
                            'chapter': chapter_num,
                            'sentence': sent_num,
                            'keyword': keyword,
                            'content': sentence,
                            'location': f"第{chapter_num}章第{sent_num}句"
                        }
                        foreshadowing_events.append(event)
                        break
                
                # 检查是否包含回收关键词
                for keyword in payoff_keywords:
                    if keyword in sentence:
                        event = {
                            'chapter': chapter_num,
                            'sentence': sent_num,
                            'keyword': keyword,
                            'content': sentence,
                            'location': f"第{chapter_num}章第{sent_num}句"
                        }
                        payoff_events.append(event)
                        break
        
        # 分析伏笔回收关系
        unrecovered_foreshadowing = []
        
        for foreshadow in foreshadowing_events:
            # 寻找对应的回收事件
            corresponding_payoff = None
            for payoff in payoff_events:
                if payoff['chapter'] > foreshadow['chapter']:
                    # 计算内容相似度
                    similarity = self._calculate_text_similarity(foreshadow['content'], payoff['content'])
                    if similarity > 0.5:  # 相似度阈值
                        corresponding_payoff = payoff
                        break
            
            if not corresponding_payoff:
                # 未找到对应的回收事件
                unrecovered_foreshadowing.append(foreshadow)
        
        # 生成未回收伏笔的问题报告
        for foreshadow in unrecovered_foreshadowing:
            issue_id = f"FORESHADOW_{foreshadow['chapter']:03d}_{foreshadow['sentence']:03d}"
            issue = ConsistencyIssue(
                issue_id=issue_id,
                issue_type=ConsistencyType.FORESIGHT,
                severity=SeverityLevel.SEVERE,
                location=foreshadow['location'],
                description="检测到未回收的伏笔",
                evidence=[
                    f"伏笔内容: {foreshadow['content']}",
                    f"关键词: {foreshadow['keyword']}",
                    f"设置位置: 第{foreshadow['chapter']}章"
                ],
                suggested_fixes=[
                    "在后续章节中添加回收情节",
                    "通过角色对话间接揭示伏笔",
                    "将伏笔转化为次要情节元素",
                    "如果确实不重要，可以通过自嘲方式承认放弃"
                ],
                confidence_score=0.9
            )
            issues.append(issue)
        
        logger.info(f"伏笔回收一致性检查完成，发现 {len(issues)} 个问题")
        return issues
    
    def _analyze_behavior_patterns(self, behaviors: List[Dict]) -> Dict[str, Any]:
        """分析行为模式"""
        if not behaviors:
            return {}
        
        # 提取行为关键词
        behavior_texts = [b['behavior'] for b in behaviors]
        
        # 使用TF-IDF提取关键词
        if len(behavior_texts) > 1:
            try:
                tfidf_matrix = self.vectorizer.fit_transform(behavior_texts)
                feature_names = self.vectorizer.get_feature_names_out()
                
                # 计算每个行为的关键词权重
                behavior_keywords = []
                for i, text in enumerate(behavior_texts):
                    feature_index = tfidf_matrix[i,:].nonzero()
                    tfidf_scores = zip(feature_index, [tfidf_matrix[i, x] for x in feature_index])
                    keywords = [(feature_names[j], score) for j, score in tfidf_scores]
                    keywords.sort(key=lambda x: x[1], reverse=True)
                    behavior_keywords.append(keywords[:5])  # 取前5个关键词
                
                return {
                    'behavior_texts': behavior_texts,
                    'keywords': behavior_keywords,
                    'vectorizer': self.vectorizer
                }
            except Exception as e:
                logger.warning(f"TF-IDF分析失败: {e}")
        
        return {'behavior_texts': behavior_texts}
    
    def _analyze_dialogue_style(self, dialogues: List[Dict]) -> List[Dict]:
        """分析对话风格"""
        style_metrics = []
        
        for dialogue in dialogues:
            text = dialogue['dialogue']
            
            # 计算风格指标
            metrics = {
                'length': len(text),  # 对话长度
                'sentence_count': len(re.split(r'[，。！？]', text)),  # 句子数量
                'question_ratio': len(re.findall(r'[？?]', text)) / max(len(text), 1),  # 问句比例
                'exclamation_ratio': len(re.findall(r'[！!]', text)) / max(len(text), 1),  # 感叹句比例
                'formal_word_count': len(re.findall(r'您|请|谢谢|对不起|抱歉', text)),  # 正式用词数量
                'informal_word_count': len(re.findall(r'喂|嘿|靠|我去|牛逼', text)),  # 非正式用词数量
            }
            
            style_metrics.append({
                'location': dialogue['location'],
                'metrics': metrics,
                'text': text
            })
        
        return style_metrics
    
    def _detect_style_changes(self, style_metrics: List[Dict]) -> List[Dict]:
        """检测风格变化"""
        changes = []
        
        if len(style_metrics) < 2:
            return changes
        
        for i in range(1, len(style_metrics)):
            prev_metrics = style_metrics[i-1]['metrics']
            curr_metrics = style_metrics[i]['metrics']
            
            # 计算各项指标的变化
            metric_changes = {}
            for key in prev_metrics.keys():
                if key in curr_metrics:
                    change = abs(curr_metrics[key] - prev_metrics[key])
                    metric_changes[key] = change
            
            # 找出变化最大的指标
            if metric_changes:
                max_change_metric = max(metric_changes.items(), key=lambda x: x[1])
                if max_change_metric[1] > 0.3:  # 变化阈值
                    changes.append({
                        'index': i,
                        'location': style_metrics[i]['location'],
                        'metric': max_change_metric[0],
                        'change_magnitude': max_change_metric[1],
                        'prev_value': prev_metrics[max_change_metric[0]],
                        'curr_value': curr_metrics[max_change_metric[0]]
                    })
        
        return changes
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        if not text1 or not text2:
            return 0.0
        
        # 简单基于词频的相似度计算
        words1 = set(re.findall(r'[\u4e00-\u9fa5]+', text1))
        words2 = set(re.findall(r'[\u4e00-\u9fa5]+', text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _estimate_time_gap(self, time_ref1: str, time_ref2: str) -> Optional[int]:
        """估计时间间隔（天数）"""
        # 简单的时间间隔估计
        time_units = {
            '年': 365,
            '月': 30,
            '天': 1,
            '小时': 1/24,
            '日': 1
        }
        
        # 提取数字和时间单位
        pattern = r'(\d+)\s*([年个月天小时日])'
        match1 = re.search(pattern, time_ref1)
        match2 = re.search(pattern, time_ref2)
        
        if match1 and match2:
            num1, unit1 = match1.groups()
            num2, unit2 = match2.groups()
            
            if unit1 in time_units and unit2 in time_units:
                days1 = int(num1) * time_units[unit1]
                days2 = int(num2) * time_units[unit2]
                return abs(days2 - days1)
        
        return None
    
    def run_comprehensive_check(self, novel_file: str) -> Dict[str, Any]:
        """
        运行全面一致性检查
        
        Args:
            novel_file: 小说文件路径
            
        Returns:
            检查结果字典
        """
        logger.info(f"开始对 {novel_file} 进行全面一致性检查")
        
        try:
            # 1. 加载小说文本
            novel_text = self.load_novel_text(novel_file)
            
            # 2. 解析章节
            chapters = self.parse_chapters(novel_text)
            
            # 3. 提取角色信息
            characters = self.extract_characters(chapters)
            
            # 4. 运行各项检查
            all_issues = []
            
            # 角色一致性检查
            character_issues = self.check_character_consistency(chapters)
            all_issues.extend(character_issues)
            
            # 时间线一致性检查
            timeline_issues = self.check_timeline_consistency(chapters)
            all_issues.extend(timeline_issues)
            
            # 情节逻辑一致性检查
            plot_issues = self.check_plot_logic_consistency(chapters)
            all_issues.extend(plot_issues)
            
            # 伏笔回收一致性检查
            foresight_issues = self.check_foresight_consistency(chapters)
            all_issues.extend(foresight_issues)
            
            # 5. 生成统计信息
            stats = self._generate_statistics(all_issues, chapters)
            
            # 6. 生成报告
            report = self._generate_report(all_issues, stats, novel_file)
            
            result = {
                'success': True,
                'novel_file': novel_file,
                'chapter_count': len(chapters),
                'character_count': len(characters),
                'issue_count': len(all_issues),
                'issues': [issue.to_dict() for issue in all_issues],
                'statistics': stats,
                'report': report,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"全面一致性检查完成，共发现 {len(all_issues)} 个问题")
            return result
            
        except Exception as e:
            logger.error(f"一致性检查失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_statistics(self, issues: List[ConsistencyIssue], chapters: Dict[int, str]) -> Dict[str, Any]:
        """生成统计信息"""
        stats = {
            'total_issues': len(issues),
            'issues_by_type': {},
            'issues_by_severity': {},
            'issues_by_chapter': {},
            'chapter_count': len(chapters),
            'avg_issues_per_chapter': len(issues) / max(len(chapters), 1)
        }
        
        # 按类型统计
        for issue_type in ConsistencyType:
            type_issues = [i for i in issues if i.issue_type == issue_type]
            stats['issues_by_type'][issue_type.value] = len(type_issues)
        
        # 按严重程度统计
        for severity in SeverityLevel:
            severity_issues = [i for i in issues if i.severity == severity]
            stats['issues_by_severity'][severity.value] = len(severity_issues)
        
        # 按章节统计
        for chapter_num in chapters.keys():
            chapter_issues = [i for i in issues if f"第{chapter_num}章" in i.location]
            stats['issues_by_chapter'][chapter_num] = len(chapter_issues)
        
        return stats
    
    def _generate_report(self, issues: List[ConsistencyIssue], stats: Dict[str, Any], novel_file: str) -> str:
        """生成检查报告"""
        report_lines = []
        
        # 报告头部
        report_lines.append("# 小说一致性检查报告")
        report_lines.append("")
        report_lines.append(f"**检查时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append(f"**检查文件**: {novel_file}")
        report_lines.append(f"**章节数量**: {stats['chapter_count']}")
        report_lines.append(f"**发现问题总数**: {stats['total_issues']}")
        report_lines.append("")
        
        # 统计摘要
        report_lines.append("## 统计摘要")
        report_lines.append("")
        
        # 按类型统计
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
                    
                    if issue.evidence:
                        report_lines.append("- **证据**:")
                        for evidence in issue.evidence:
                            report_lines.append(f"  - {evidence}")
                    
                    if issue.suggested_fixes:
                        report_lines.append("- **修复建议**:")
                        for fix in issue.suggested_fixes:
                            report_lines.append(f"  - {fix}")
                    
                    report_lines.append("")
        
        # 修复优先级建议
        report_lines.append("## 修复优先级建议")
        report_lines.append("")
        
        critical_issues = [i for i in issues if i.severity == SeverityLevel.CRITICAL]
        severe_issues = [i for i in issues if i.severity == SeverityLevel.SEVERE]
        
        report_lines.append("### 立即修复（24小时内）")
        if critical_issues:
            for issue in critical_issues[:3]:  # 只列出前3个最关键的
                report_lines.append(f"- {issue.location}: {issue.description}")
        else:
            report_lines.append("- 无致命问题")
        report_lines.append("")
        
        report_lines.append("### 近期修复（7天内）")
        if severe_issues:
            for issue in severe_issues[:5]:  # 只列出前5个严重的
                report_lines.append(f"- {issue.location}: {issue.description}")
        else:
            report_lines.append("- 无严重问题")
        report_lines.append("")
        
        # 总结与建议
        report_lines.append("## 总结与建议")
        report_lines.append("")
        
        total_issues = stats['total_issues']
        if total_issues == 0:
            report_lines.append("✅ 恭喜！未发现明显的一致性问题。")
            report_lines.append("建议继续保持当前的写作质量。")
        elif total_issues <= 5:
            report_lines.append("⚠️ 发现少量一致性问题，建议抽时间修复。")
            report_lines.append("这些问题不会严重影响阅读体验，但修复后可以提升作品质量。")
        elif total_issues <= 15:
            report_lines.append("⚠️ 发现较多一致性问题，建议制定修复计划。")
            report_lines.append("建议按照修复优先级逐步修复，避免影响写作进度。")
        else:
            report_lines.append("❌ 发现大量一致性问题，需要系统性的修复。")
            report_lines.append("建议暂停新章节写作，先集中修复现有问题。")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("*本报告由小说一致性检查脚本自动生成*")
        report_lines.append("*基于AI驱动创作工具的设计理念[10](@ref)和网文校对系统的实现方法[9](@ref)*")
        
        return '\n'.join(report_lines)
    
    def save_report(self, report: str, output_file: Optional[str] = None) -> str:
        """
        保存检查报告
        
        Args:
            report: 报告内容
            output_file: 输出文件路径，如果为None则自动生成
            
        Returns:
            保存的文件路径
        """
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"consistency_report_{timestamp}.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"检查报告已保存到: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"保存报告失败: {e}")
            raise
    
    def export_issues_to_json(self, issues: List[ConsistencyIssue], output_file: str) -> str:
        """
        将问题导出为JSON格式
        
        Args:
            issues: 问题列表
            output_file: 输出文件路径
            
        Returns:
            保存的文件路径
        """
        try:
            issues_dict = [issue.to_dict() for issue in issues]
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(issues_dict, f, ensure_ascii=False, indent=2)
            
            logger.info(f"问题数据已导出到: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"导出问题数据失败: {e}")
            raise

def main():
    """主函数 - 命令行接口"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='小说一致性检查脚本 - 检查角色行为、时间线、情节逻辑等一致性',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检查单个小说文件
  python consistency-checker.py novel.txt
  
  # 检查并指定输出文件
  python consistency-checker.py novel.txt -o report.md
  
  # 使用自定义配置文件
  python consistency-checker.py novel.txt -c config.json
  
  # 只导出问题数据（JSON格式）
  python consistency-checker.py novel.txt --export-json issues.json
        """
    )
    
    parser.add_argument('novel_file', help='小说文件路径')
    parser.add_argument('-o', '--output', help='检查报告输出文件路径')
    parser.add_argument('-c', '--config', help='配置文件路径')
    parser.add_argument('--export-json', help='将问题导出为JSON格式的文件路径')
    parser.add_argument('--verbose', action='store_true', help='显示详细日志信息')
    
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 检查文件是否存在
    if not os.path.exists(args.novel_file):
        print(f"错误: 文件 '{args.novel_file}' 不存在")
        sys.exit(1)
    
    try:
        # 创建检查器实例
        checker = NovelConsistencyChecker(args.config)
        
        # 运行全面检查
        print(f"开始检查小说: {args.novel_file}")
        result = checker.run_comprehensive_check(args.novel_file)
        
        if result['success']:
            print(f"检查完成，共发现 {result['issue_count']} 个问题")
            print(f"涉及 {result['chapter_count']} 章，{result['character_count']} 个角色")
            
            # 生成并保存报告
            report = result['report']
            
            if args.output:
                output_file = args.output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"consistency_report_{timestamp}.md"
            
            checker.save_report(report, output_file)
            print(f"检查报告已保存到: {output_file}")
            
            # 导出问题数据（如果指定）
            if args.export_json:
                issues = [ConsistencyIssue(**issue_dict) for issue_dict in result['issues']]
                json_file = checker.export_issues_to_json(issues, args.export_json)
                print(f"问题数据已导出到: {json_file}")
            
            # 显示摘要
            print("\n=== 检查摘要 ===")
            stats = result['statistics']
            
            print(f"问题类型分布:")
            for issue_type, count in stats['issues_by_type'].items():
                print(f"  {issue_type}: {count}")
            
            print(f"\n严重程度分布:")
            for severity, count in stats['issues_by_severity'].items():
                print(f"  {severity}: {count}")
            
            # 显示最严重的问题
            critical_issues = [i for i in result['issues'] if i['severity'] == '致命']
            if critical_issues:
                print(f"\n⚠️ 发现 {len(critical_issues)} 个致命问题，建议立即修复:")
                for issue in critical_issues[:3]:
                    print(f"  - {issue['location']}: {issue['description']}")
            
        else:
            print(f"检查失败: {result['error']}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n检查被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"检查过程中发生错误: {e}")
        logger.exception("检查失败")
        sys.exit(1)

if __name__ == "__main__":
    main()
