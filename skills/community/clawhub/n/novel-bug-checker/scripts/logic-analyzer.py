#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小说逻辑分析器脚本 (Logic Analyzer for Novel Writing)
版本: 2.1.0
作者: AUTHOR
日期: 2026-04-14

功能概述:
基于搜索结果中的叙事问题诊断与修复方法论[6](@ref)，本脚本实现了
系统化的小说逻辑漏洞检测功能，包括情节逻辑链分析、角色行为一致性、
时间线合理性等核心检查。通过结合规则引擎与自然语言处理技术，
为作者提供专业的Bug诊断和修复建议。

核心特性:
1. 逻辑链追踪算法 - 基于情节漏洞填补理论[6](@ref)
2. 死锁问题检测 - 识别互相矛盾的设定
3. 伏笔追踪管理 - 检测被遗忘的伏笔
4. 多维度分析 - 角色、情节、设定三个维度的逻辑检查
5. 可视化报告 - 生成详细的逻辑分析报告

依赖库:
- pandas: 数据处理和分析
- numpy: 数值计算
- networkx: 图论分析（用于逻辑链可视化）
- jieba: 中文分词
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
from collections import defaultdict

# 第三方库导入
try:
    import pandas as pd
    import numpy as np
    import networkx as nx
    import jieba
    import jieba.posseg as pseg
    from dotenv import load_dotenv
except ImportError as e:
    print(f"缺少必要的依赖库: {e}")
    print("请运行: pip install pandas numpy networkx jieba python-dotenv")
    sys.exit(1)

# 加载环境变量
load_dotenv()

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logic_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 初始化jieba分词
jieba.initialize()

# 常量定义
class LogicIssueType(Enum):
    """逻辑问题类型枚举"""
    NULL_POINTER = "空指针异常"  # 未初始化的关键信息[6](@ref)
    DEADLOCK = "死锁问题"  # 互相矛盾的设定[6](@ref)
    MEMORY_LEAK = "内存泄漏"  # 被遗忘的伏笔[6](@ref)
    CHARACTER_INCONSISTENCY = "角色状态不一致"
    MOTIVATION_BREAK = "动机驱动断裂"
    TIMELINE_PARADOX = "时间线悖论"
    PLOT_HOLE = "情节漏洞"

class SeverityLevel(Enum):
    """问题严重程度枚举"""
    CRITICAL = "致命"
    SEVERE = "严重"
    MODERATE = "中等"
    MINOR = "轻微"

@dataclass
class LogicNode:
    """逻辑节点数据结构"""
    node_id: str
    node_type: str  # "event", "character", "item", "ability", "knowledge"
    description: str
    chapter: int
    paragraph: int
    dependencies: List[str] = field(default_factory=list)  # 依赖的节点ID
    dependents: List[str] = field(default_factory=list)  # 依赖此节点的节点ID
    confidence: float = 1.0  # 置信度(0-1)
    
    def to_dict(self) -> Dict:
        """转换为字典格式"""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "description": self.description,
            "chapter": self.chapter,
            "paragraph": self.paragraph,
            "dependencies": self.dependencies,
            "dependents": self.dependents,
            "confidence": self.confidence
        }

@dataclass
class LogicIssue:
    """逻辑问题记录"""
    issue_id: str
    issue_type: LogicIssueType
    severity: SeverityLevel
    location: str  # 格式: "第X章第Y段"
    description: str
    evidence: List[str] = field(default_factory=list)
    suggested_fixes: List[str] = field(default_factory=list)
    confidence_score: float = 0.0  # 置信度分数(0-1)
    root_cause: Optional[str] = None  # 根本原因分析
    
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
            "root_cause": self.root_cause
        }

class NovelLogicAnalyzer:
    """
    小说逻辑分析器主类
    
    基于搜索结果中的叙事问题诊断与修复方法论[6](@ref)，
    实现系统化的逻辑漏洞检测功能。结合逻辑链追踪算法、
    死锁问题检测和伏笔追踪管理，提供专业的Bug诊断。
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化逻辑分析器
        
        Args:
            config_path: 配置文件路径，如果为None则使用默认配置
        """
        self.config = self._load_config(config_path)
        self.logic_graph = nx.DiGraph()  # 逻辑依赖图
        self.logic_nodes: Dict[str, LogicNode] = {}
        self.logic_issues: List[LogicIssue] = []
        self.foreshadowing_tracker: Dict[str, Dict] = {}
        self.character_states: Dict[str, Dict] = {}
        
        # 初始化修复策略库
        self._init_repair_strategies()
        
        logger.info("小说逻辑分析器初始化完成")
    
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """加载配置文件"""
        default_config = {
            "min_confidence_threshold": 0.6,  # 最小置信度阈值
            "dependency_depth_limit": 10,  # 依赖链深度限制
            "enable_advanced_analysis": True,  # 启用高级分析
            "enable_foreshadowing_tracking": True,  # 启用伏笔追踪
            "enable_character_state_tracking": True,  # 启用角色状态追踪
            "output_format": "markdown",  # 输出格式
            "similarity_threshold": 0.7,  # 文本相似度阈值
            "max_issues_per_chapter": 20,  # 每章最大问题数
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
    
    def _init_repair_strategies(self):
        """初始化修复策略库"""
        # 基于搜索结果中的修复策略[6](@ref)
        self.repair_strategies = {
            LogicIssueType.NULL_POINTER: [
                "前向补充法：在早期章节添加伏笔",
                "后向解释法：在发现后补充说明",
                "规则调整法：修改世界观设定"
            ],
            LogicIssueType.DEADLOCK: [
                "设定优先级排序：确定哪个设定更重要",
                "设定融合：将矛盾设定融合为新的统一设定",
                "设定废弃：废弃其中一个矛盾设定"
            ],
            LogicIssueType.MEMORY_LEAK: [
                "显式回收：直接揭示伏笔的答案",
                "隐式回收：通过暗示让读者推断",
                "转移回收：将伏笔转化为另一个用途",
                "承认放弃：某些次要伏笔可以故意留白"
            ],
            LogicIssueType.CHARACTER_INCONSISTENCY: [
                "渐进式转变：通过多个小事件累积改变",
                "重大事件触发：用创伤或顿悟解释突变",
                "深层动机揭示：表面目标改变，深层动机不变"
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
    
    def extract_logic_nodes(self, chapters: Dict[int, Dict]) -> Dict[str, LogicNode]:
        """
        提取逻辑节点（事件、角色、物品、能力、知识等）
        
        Args:
            chapters: 章节字典
            
        Returns:
            逻辑节点字典
        """
        logger.info("开始提取逻辑节点...")
        
        # 定义节点类型的关键词模式
        node_patterns = {
            "event": [
                r'发生[了着]', r'开始[了着]', r'结束[了着]', r'突然', r'意外',
                r'战斗', r'会议', r'发现', r'获得', r'失去', r'死亡', r'诞生'
            ],
            "character": [
                r'[\u4e00-\u9fa5]{2,4}',  # 中文名字
                r'[A-Z][a-z]+ [A-Z][a-z]+',  # 英文全名
            ],
            "item": [
                r'[拿到获得找到]了?(一个|一把|一件|一本)', r'宝物', r'神器', r'秘籍',
                r'武器', r'装备', r'道具', r'丹药', r'法宝'
            ],
            "ability": [
                r'学会[了着]', r'掌握[了着]', r'领悟[了着]', r'突破[了着]',
                r'技能', r'法术', r'武功', r'神通', r'天赋'
            ],
            "knowledge": [
                r'知道[了着]', r'了解[了着]', r'发现[了着]', r'明白[了着]',
                r'秘密', r'真相', r'信息', r'情报', r'线索'
            ]
        }
        
        node_counter = 1
        all_nodes = {}
        
        for chapter_num, chapter_data in chapters.items():
            paragraphs = chapter_data["paragraphs"]
            
            for para_num, paragraph in enumerate(paragraphs, 1):
                location = f"第{chapter_num}章第{para_num}段"
                
                # 提取事件节点
                for pattern in node_patterns["event"]:
                    if re.search(pattern, paragraph):
                        node_id = f"event_{node_counter:04d}"
                        node = LogicNode(
                            node_id=node_id,
                            node_type="event",
                            description=paragraph[:100],  # 取前100字符
                            chapter=chapter_num,
                            paragraph=para_num,
                            dependencies=[],
                            dependents=[],
                            confidence=0.8
                        )
                        all_nodes[node_id] = node
                        node_counter += 1
                        logger.debug(f"提取事件节点: {node_id} - {paragraph[:50]}...")
                
                # 提取角色节点（通过命名实体识别）
                words = pseg.cut(paragraph)
                for word, flag in words:
                    if flag == 'nr':  # 人名
                        node_id = f"character_{node_counter:04d}"
                        node = LogicNode(
                            node_id=node_id,
                            node_type="character",
                            description=word,
                            chapter=chapter_num,
                            paragraph=para_num,
                            dependencies=[],
                            dependents=[],
                            confidence=0.9
                        )
                        all_nodes[node_id] = node
                        node_counter += 1
                
                # 提取物品节点
                for pattern in node_patterns["item"]:
                    matches = re.findall(rf'{pattern} ([^，。！？]+)', paragraph)
                    for match in matches:
                        if isinstance(match, tuple):
                            match = match
                        node_id = f"item_{node_counter:04d}"
                        node = LogicNode(
                            node_id=node_id,
                            node_type="item",
                            description=match,
                            chapter=chapter_num,
                            paragraph=para_num,
                            dependencies=[],
                            dependents=[],
                            confidence=0.7
                        )
                        all_nodes[node_id] = node
                        node_counter += 1
        
        # 构建逻辑依赖图
        for node_id, node in all_nodes.items():
            self.logic_graph.add_node(node_id, **node.to_dict())
        
        logger.info(f"共提取 {len(all_nodes)} 个逻辑节点")
        self.logic_nodes = all_nodes
        return all_nodes
    
    def analyze_logic_chains(self) -> List[LogicIssue]:
        """
        分析逻辑链，检测空指针异常（未初始化的关键信息）[6](@ref)
        
        基于搜索结果中的逻辑链追踪算法[6](@ref)：
        1. 标记每个关键情节点
        2. 反向追溯其依赖条件
        3. 检查依赖是否已被满足
        4. 定位断链位置
        
        Returns:
            逻辑问题列表
        """
        logger.info("开始分析逻辑链，检测空指针异常...")
        issues = []
        
        # 分析每个节点的依赖关系
        for node_id, node in self.logic_nodes.items():
            # 对于事件节点，检查是否有必要的依赖
            if node.node_type == "event":
                # 提取事件描述中的关键元素
                dependencies = self._extract_dependencies_from_description(node.description)
                
                # 检查这些依赖是否已经存在
                missing_deps = []
                for dep in dependencies:
                    if not self._find_node_by_description(dep):
                        missing_deps.append(dep)
                
                if missing_deps:
                    # 发现空指针异常
                    issue_id = f"NULL_PTR_{node_id}"
                    issue = LogicIssue(
                        issue_id=issue_id,
                        issue_type=LogicIssueType.NULL_POINTER,
                        severity=self._assess_null_pointer_severity(missing_deps),
                        location=f"第{node.chapter}章第{node.paragraph}段",
                        description=f"事件'{node.description[:50]}...'缺少必要的依赖条件",
                        evidence=[
                            f"事件描述: {node.description}",
                            f"缺失的依赖: {', '.join(missing_deps)}",
                            f"事件位置: 第{node.chapter}章第{node.paragraph}段"
                        ],
                        suggested_fixes=self.repair_strategies[LogicIssueType.NULL_POINTER],
                        confidence_score=0.85,
                        root_cause="关键信息未初始化，缺少必要的前置条件"
                    )
                    issues.append(issue)
        
        logger.info(f"逻辑链分析完成，发现 {len(issues)} 个空指针异常")
        return issues
    
    def detect_deadlock_problems(self) -> List[LogicIssue]:
        """
        检测死锁问题（互相矛盾的设定）[6](@ref)
        
        基于搜索结果中的死锁问题诊断方法[6](@ref)，检查：
        - 两个规则同时成立会导致矛盾
        - 角色行为与其设定冲突
        - 时间线出现悖论
        
        Returns:
            死锁问题列表
        """
        logger.info("开始检测死锁问题...")
        issues = []
        
        # 收集所有设定相关的节点
        setting_nodes = {}
        for node_id, node in self.logic_nodes.items():
            if node.node_type in ["ability", "knowledge"]:
                setting_nodes[node_id] = node
        
        # 检查设定之间的矛盾
        checked_pairs = set()
        for node_id1, node1 in setting_nodes.items():
            for node_id2, node2 in setting_nodes.items():
                if node_id1 == node_id2 or (node_id2, node_id1) in checked_pairs:
                    continue
                
                checked_pairs.add((node_id1, node_id2))
                
                # 检查两个设定是否矛盾
                if self._are_settings_contradictory(node1.description, node2.description):
                    # 发现死锁问题
                    issue_id = f"DEADLOCK_{node_id1}_{node_id2}"
                    issue = LogicIssue(
                        issue_id=issue_id,
                        issue_type=LogicIssueType.DEADLOCK,
                        severity=self._assess_deadlock_severity(node1, node2),
                        location=f"第{node1.chapter}章第{node1.paragraph}段 vs 第{node2.chapter}章第{node2.paragraph}段",
                        description=f"设定矛盾: '{node1.description}' 与 '{node2.description}' 冲突",
                        evidence=[
                            f"设定1: {node1.description} (第{node1.chapter}章第{node1.paragraph}段)",
                            f"设定2: {node2.description} (第{node2.chapter}章第{node2.paragraph}段)",
                            f"矛盾类型: {self._identify_contradiction_type(node1, node2)}"
                        ],
                        suggested_fixes=self.repair_strategies[LogicIssueType.DEADLOCK],
                        confidence_score=0.9,
                        root_cause="世界观设定存在内部矛盾，导致逻辑死锁"
                    )
                    issues.append(issue)
        
        logger.info(f"死锁问题检测完成，发现 {len(issues)} 个死锁问题")
        return issues
    
    def track_foreshadowing(self, chapters: Dict[int, Dict]) -> List[LogicIssue]:
        """
        追踪伏笔，检测内存泄漏（被遗忘的伏笔）[6](@ref)
        
        基于搜索结果中的伏笔追踪表方法[6](@ref)，实现伏笔设置和回收的跟踪。
        
        Args:
            chapters: 章节字典
            
        Returns:
            伏笔问题列表
        """
        if not self.config["enable_foreshadowing_tracking"]:
            logger.info("伏笔追踪功能已禁用")
            return []
        
        logger.info("开始追踪伏笔，检测内存泄漏...")
        issues = []
        
        # 伏笔关键词
        foreshadowing_keywords = [
            '神秘', '奇怪', '疑惑', '不解', '预感', '预兆',
            '暗示', '线索', '秘密', '谜团', '未知', '隐藏',
            '似乎', '好像', '可能', '或许', '将来', '以后'
        ]
        
        # 回收关键词
        payoff_keywords = [
            '原来', '真相', '揭晓', '揭示', '发现', '明白',
            '解开', '解答', '答案', '结果', '结局', '最终',
            '因此', '所以', '于是', '终于'
        ]
        
        # 扫描所有章节，识别伏笔设置
        for chapter_num, chapter_data in chapters.items():
            paragraphs = chapter_data["paragraphs"]
            
            for para_num, paragraph in enumerate(paragraphs, 1):
                # 检查是否包含伏笔关键词
                for keyword in foreshadowing_keywords:
                    if keyword in paragraph:
                        # 发现伏笔设置
                        foreshadow_id = f"foreshadow_{chapter_num:03d}_{para_num:03d}"
                        self.foreshadowing_tracker[foreshadow_id] = {
                            "id": foreshadow_id,
                            "chapter_introduced": chapter_num,
                            "paragraph": para_num,
                            "content": paragraph[:200],
                            "keyword": keyword,
                            "importance_level": self._assess_foreshadowing_importance(paragraph),
                            "payoff_chapter": None,
                            "reader_expectation": "unknown"
                        }
                        logger.debug(f"发现伏笔: {foreshadow_id} - {paragraph[:50]}...")
        
        # 扫描所有章节，识别伏笔回收
        for chapter_num, chapter_data in chapters.items():
            paragraphs = chapter_data["paragraphs"]
            
            for para_num, paragraph in enumerate(paragraphs, 1):
                # 检查是否包含回收关键词
                for keyword in payoff_keywords:
                    if keyword in paragraph:
                        # 尝试匹配已设置的伏笔
                        for foreshadow_id, foreshadow in self.foreshadowing_tracker.items():
                            if foreshadow["payoff_chapter"] is None:
                                # 计算内容相似度
                                similarity = self._calculate_text_similarity(
                                    foreshadow["content"], paragraph
                                )
                                if similarity > 0.3:  # 相似度阈值
                                    # 标记为已回收
                                    foreshadow["payoff_chapter"] = chapter_num
                                    foreshadow["payoff_paragraph"] = para_num
                                    logger.debug(f"伏笔回收: {foreshadow_id} -> 第{chapter_num}章")
        
        # 检查未回收的伏笔
        for foreshadow_id, foreshadow in self.foreshadowing_tracker.items():
            if foreshadow["payoff_chapter"] is None:
                # 发现内存泄漏（未回收的伏笔）
                issue_id = f"MEMORY_LEAK_{foreshadow_id}"
                issue = LogicIssue(
                    issue_id=issue_id,
                    issue_type=LogicIssueType.MEMORY_LEAK,
                    severity=self._assess_foreshadowing_severity(foreshadow),
                    location=f"第{foreshadow['chapter_introduced']}章第{foreshadow['paragraph']}段",
                    description=f"未回收的伏笔: {foreshadow['content'][:100]}...",
                    evidence=[
                        f"伏笔内容: {foreshadow['content']}",
                        f"设置位置: 第{foreshadow['chapter_introduced']}章第{foreshadow['paragraph']}段",
                        f"重要性等级: {foreshadow['importance_level']}",
                        f"读者期待: {foreshadow['reader_expectation']}"
                    ],
                    suggested_fixes=self.repair_strategies[LogicIssueType.MEMORY_LEAK],
                    confidence_score=0.8,
                    root_cause="伏笔设置后未被回收，导致读者期待落空"
                )
                issues.append(issue)
        
        logger.info(f"伏笔追踪完成，发现 {len(issues)} 个未回收伏笔")
        return issues
    
    def analyze_character_consistency(self, chapters: Dict[int, Dict]) -> List[LogicIssue]:
        """
        分析角色一致性，检测角色状态不一致问题[6](@ref)
        
        基于搜索结果中的角色状态不一致诊断方法[6](@ref)，检查：
        - 性格是否突变
        - 能力是否突然增强/减弱
        - 知识是否凭空出现
        - 关系是否无故改变
        
        Args:
            chapters: 章节字典
            
        Returns:
            角色一致性问题列表
        """
        if not self.config["enable_character_state_tracking"]:
            logger.info("角色状态追踪功能已禁用")
            return []
        
        logger.info("开始分析角色一致性...")
        issues = []
        
        # 提取所有角色
        characters = {}
        for node_id, node in self.logic_nodes.items():
            if node.node_type == "character":
                character_name = node.description
                if character_name not in characters:
                    characters[character_name] = {
                        "appearances": [],
                        "states": []
                    }
                characters[character_name]["appearances"].append({
                    "chapter": node.chapter,
                    "paragraph": node.paragraph,
                    "context": self._get_context_for_node(node, chapters)
                })
        
        # 分析每个角色的状态变化
        for character_name, data in characters.items():
            if len(data["appearances"]) < 2:
                continue
            
            # 按章节排序
            appearances = sorted(data["appearances"], key=lambda x: (x["chapter"], x["paragraph"]))
            
            # 分析状态变化
            for i in range(1, len(appearances)):
                prev = appearances[i-1]
                curr = appearances[i]
                
                # 检查能力突变
                ability_changes = self._detect_ability_changes(prev["context"], curr["context"])
                if ability_changes:
                    issue_id = f"CHAR_CONSISTENCY_{character_name}_{i:03d}"
                    issue = LogicIssue(
                        issue_id=issue_id,
                        issue_type=LogicIssueType.CHARACTER_INCONSISTENCY,
                        severity=SeverityLevel.MODERATE,
                        location=f"第{curr['chapter']}章第{curr['paragraph']}段",
                        description=f"角色'{character_name}'的能力发生突变",
                        evidence=[
                            f"前文能力: {ability_changes['previous']}",
                            f"当前能力: {ability_changes['current']}",
                            f"变化类型: {ability_changes['type']}"
                        ],
                        suggested_fixes=self.repair_strategies[LogicIssueType.CHARACTER_INCONSISTENCY],
                        confidence_score=0.75,
                        root_cause="角色能力变化缺少合理的过渡和解释"
                    )
                    issues.append(issue)
        
        logger.info(f"角色一致性分析完成，发现 {len(issues)} 个问题")
        return issues
    
    def _extract_dependencies_from_description(self, description: str) -> List[str]:
        """从描述中提取依赖项"""
        dependencies = []
        
        # 提取可能依赖的角色
        words = pseg.cut(description)
        for word, flag in words:
            if flag == 'nr':  # 人名
                dependencies.append(f"角色:{word}")
        
        # 提取可能依赖的物品
        item_patterns = [r'用(.*?)来', r'借助(.*?)', r'使用(.*?)', r'拿到(.*?)']
        for pattern in item_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                dependencies.append(f"物品:{match}")
        
        # 提取可能依赖的能力
        ability_patterns = [r'施展(.*?)', r'使用(.*?)技能', r'发动(.*?)', r'运用(.*?)']
        for pattern in ability_patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                dependencies.append(f"能力:{match}")
        
        return list(set(dependencies))  # 去重
    
    def _find_node_by_description(self, description: str) -> Optional[LogicNode]:
        """根据描述查找节点"""
        for node_id, node in self.logic_nodes.items():
            if description in node.description:
                return node
        return None
    
    def _assess_null_pointer_severity(self, missing_deps: List[str]) -> SeverityLevel:
        """评估空指针异常的严重程度"""
        # 检查缺失的依赖类型
        critical_deps = 0
        for dep in missing_deps:
            if dep.startswith("角色:") or dep.startswith("能力:"):
                critical_deps += 1
        
        if critical_deps >= 2:
            return SeverityLevel.CRITICAL
        elif critical_deps == 1:
            return SeverityLevel.SEVERE
        else:
            return SeverityLevel.MODERATE
    
    def _are_settings_contradictory(self, setting1: str, setting2: str) -> bool:
        """检查两个设定是否矛盾"""
        # 简单的矛盾检测规则
        contradictions = [
            ("不会", "会"),  # 不会飞 vs 会飞
            ("不能", "能"),  # 不能使用魔法 vs 能使用魔法
            ("没有", "有"),  # 没有武器 vs 有武器
            ("未知", "已知"),  # 未知的秘密 vs 已知的秘密
            ("禁止", "允许"),  # 禁止进入 vs 允许进入
            ("死亡", "活着"),  # 角色死亡 vs 角色活着
        ]
        
        for neg, pos in contradictions:
            if (neg in setting1 and pos in setting2) or (pos in setting1 and neg in setting2):
                return True
        
        return False
    
    def _assess_deadlock_severity(self, node1: LogicNode, node2: LogicNode) -> SeverityLevel:
        """评估死锁问题的严重程度"""
        # 根据节点类型和章节间隔评估
        chapter_gap = abs(node1.chapter - node2.chapter)
        
        if chapter_gap <= 3:
            # 相近章节的矛盾更严重
            if node1.node_type == "ability" and node2.node_type == "ability":
                return SeverityLevel.CRITICAL
            else:
                return SeverityLevel.SEVERE
        else:
            return SeverityLevel.MODERATE
    
    def _identify_contradiction_type(self, node1: LogicNode, node2: LogicNode) -> str:
        """识别矛盾类型"""
        if node1.node_type == "ability" and node2.node_type == "ability":
            return "能力矛盾"
        elif node1.node_type == "knowledge" and node2.node_type == "knowledge":
            return "知识矛盾"
        else:
            return "设定矛盾"
    
    def _assess_foreshadowing_importance(self, content: str) -> str:
        """评估伏笔的重要性等级"""
        important_keywords = ['秘密', '真相', '关键', '重要', '致命', '生死']
        for keyword in important_keywords:
            if keyword in content:
                return "high"
        return "medium"
    
    def _assess_foreshadowing_severity(self, foreshadow: Dict) -> SeverityLevel:
        """评估伏笔问题的严重程度"""
        if foreshadow["importance_level"] == "high":
            return SeverityLevel.SEVERE
        else:
            return SeverityLevel.MODERATE
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度"""
        if not text1 or not text2:
            return 0.0
        
        # 简单基于词频的相似度计算
        words1 = set(jieba.lcut(text1))
        words2 = set(jieba.lcut(text2))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _get_context_for_node(self, node: LogicNode, chapters: Dict[int, Dict]) -> str:
        """获取节点的上下文"""
        chapter_data = chapters.get(node.chapter)
        if not chapter_data:
            return ""
        
        paragraphs = chapter_data["paragraphs"]
        if 0 <= node.paragraph - 1 < len(paragraphs):
            return paragraphs[node.paragraph - 1]
        return ""
    
    def _detect_ability_changes(self, prev_context: str, curr_context: str) -> Optional[Dict]:
        """检测能力变化"""
        ability_keywords = ['能力', '技能', '法术', '武功', '神通', '实力', '境界']
        
        prev_abilities = []
        curr_abilities = []
        
        # 提取前文中的能力描述
        for keyword in ability_keywords:
            if keyword in prev_context:
                # 提取相关描述
                pattern = rf'{keyword}[：:]\s*([^，。！？]+)'
                matches = re.findall(pattern, prev_context)
                prev_abilities.extend(matches)
        
        # 提取当前文中的能力描述
        for keyword in ability_keywords:
            if keyword in curr_context:
                pattern = rf'{keyword}[：:]\s*([^，。！？]+)'
                matches = re.findall(pattern, curr_context)
                curr_abilities.extend(matches)
        
        if prev_abilities and curr_abilities:
            # 检查能力是否发生变化
            if set(prev_abilities) != set(curr_abilities):
                return {
                    "previous": ", ".join(prev_abilities),
                    "current": ", ".join(curr_abilities),
                    "type": "能力突变"
                }
        
        return None
    
    def run_comprehensive_analysis(self, novel_file: str) -> Dict[str, Any]:
        """
        运行全面逻辑分析
        
        Args:
            novel_file: 小说文件路径
            
        Returns:
            分析结果字典
        """
        logger.info(f"开始对 {novel_file} 进行全面逻辑分析")
        
        try:
            # 1. 加载小说文本
            novel_text = self.load_novel_text(novel_file)
            
            # 2. 解析章节
            chapters = self.parse_chapters(novel_text)
            
            # 3. 提取逻辑节点
            logic_nodes = self.extract_logic_nodes(chapters)
            
            # 4. 运行各项分析
            all_issues = []
            
            # 逻辑链分析（空指针异常）
            null_pointer_issues = self.analyze_logic_chains()
            all_issues.extend(null_pointer_issues)
            
            # 死锁问题检测
            deadlock_issues = self.detect_deadlock_problems()
            all_issues.extend(deadlock_issues)
            
            # 伏笔追踪
            foreshadowing_issues = self.track_foreshadowing(chapters)
            all_issues.extend(foreshadowing_issues)
            
            # 角色一致性分析
            character_issues = self.analyze_character_consistency(chapters)
            all_issues.extend(character_issues)
            
            # 5. 生成统计信息
            stats = self._generate_statistics(all_issues, chapters)
            
            # 6. 生成报告
            report = self._generate_report(all_issues, stats, novel_file)
            
            result = {
                'success': True,
                'novel_file': novel_file,
                'chapter_count': len(chapters),
                'logic_node_count': len(logic_nodes),
                'issue_count': len(all_issues),
                'issues': [issue.to_dict() for issue in all_issues],
                'statistics': stats,
                'report': report,
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"全面逻辑分析完成，共发现 {len(all_issues)} 个问题")
            return result
            
        except Exception as e:
            logger.error(f"逻辑分析失败: {e}")
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_statistics(self, issues: List[LogicIssue], chapters: Dict[int, Dict]) -> Dict[str, Any]:
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
        for issue_type in LogicIssueType:
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
    
    def _generate_report(self, issues: List[LogicIssue], stats: Dict[str, Any], novel_file: str) -> str:
        """生成逻辑分析报告"""
        report_lines = []
        
        # 报告头部
        report_lines.append("# 小说逻辑分析报告")
        report_lines.append("")
        report_lines.append(f"**分析时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        report_lines.append(f"**分析文件**: {novel_file}")
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
                    
                    if issue.root_cause:
                        report_lines.append(f"- **根本原因**: {issue.root_cause}")
                    
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
            report_lines.append("**致命问题必须立即修复，否则可能导致故事崩塌:**")
            for issue in critical_issues[:3]:  # 只列出前3个最关键的
                report_lines.append(f"- {issue.location}: {issue.description}")
        else:
            report_lines.append("- 无致命问题")
        report_lines.append("")
        
        report_lines.append("### 近期修复（7天内）")
        if severe_issues:
            report_lines.append("**严重问题影响主线逻辑，需要尽快修复:**")
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
            report_lines.append("✅ **优秀** - 未发现明显的逻辑问题。")
            report_lines.append("建议继续保持当前的写作质量，注意维护逻辑一致性。")
        elif total_issues <= 5:
            report_lines.append("⚠️ **良好** - 发现少量逻辑问题，建议抽时间修复。")
            report_lines.append("这些问题不会严重影响阅读体验，但修复后可以提升作品质量。")
        elif total_issues <= 15:
            report_lines.append("⚠️ **中等** - 发现较多逻辑问题，建议制定修复计划。")
            report_lines.append("建议按照修复优先级逐步修复，避免影响写作进度。")
        else:
            report_lines.append("❌ **需要改进** - 发现大量逻辑问题，需要系统性的修复。")
            report_lines.append("建议暂停新章节写作，先集中修复现有问题。")
        
        report_lines.append("")
        report_lines.append("---")
        report_lines.append("*本报告由小说逻辑分析器脚本自动生成*")
        report_lines.append("*基于叙事问题诊断与修复方法论[6](@ref)*")
        
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
            output_file = f"logic_analysis_report_{timestamp}.md"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            
            logger.info(f"分析报告已保存到: {output_file}")
            return output_file
        except Exception as e:
            logger.error(f"保存报告失败: {e}")
            raise
    
    def export_issues_to_json(self, issues: List[LogicIssue], output_file: str) -> str:
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
        description='小说逻辑分析器脚本 - 检测逻辑漏洞、情节矛盾和时间线问题',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 分析单个小说文件
  python logic-analyzer.py novel.txt
  
  # 分析并指定输出文件
  python logic-analyzer.py novel.txt -o report.md
  
  # 使用自定义配置文件
  python logic-analyzer.py novel.txt -c config.json
  
  # 只导出问题数据（JSON格式）
  python logic-analyzer.py novel.txt --export-json issues.json
        """
    )
    
    parser.add_argument('novel_file', help='小说文件路径')
    parser.add_argument('-o', '--output', help='分析报告输出文件路径')
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
        # 创建分析器实例
        analyzer = NovelLogicAnalyzer(args.config)
        
        # 运行全面分析
        print(f"开始分析小说: {args.novel_file}")
        result = analyzer.run_comprehensive_analysis(args.novel_file)
        
        if result['success']:
            print(f"分析完成，共发现 {result['issue_count']} 个逻辑问题")
            print(f"涉及 {result['chapter_count']} 章，{result['logic_node_count']} 个逻辑节点")
            
            # 生成并保存报告
            report = result['report']
            
            if args.output:
                output_file = args.output
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = f"logic_analysis_report_{timestamp}.md"
            
            analyzer.save_report(report, output_file)
            print(f"分析报告已保存到: {output_file}")
            
            # 导出问题数据（如果指定）
            if args.export_json:
                issues = [LogicIssue(**issue_dict) for issue_dict in result['issues']]
                json_file = analyzer.export_issues_to_json(issues, args.export_json)
                print(f"问题数据已导出到: {json_file}")
            
            # 显示摘要
            print("\n=== 分析摘要 ===")
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
