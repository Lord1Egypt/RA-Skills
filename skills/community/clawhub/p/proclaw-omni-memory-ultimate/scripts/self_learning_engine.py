#!/usr/bin/env python3
"""
自学习引擎 (Self-Learning Engine)
实现AI Agent的主动学习机制

核心概念：
- 问题生成器：主动提出问题
- 探索机制：主动寻找答案
- 知识构建：构建概念和理论
- 假设验证：假设-验证-修正循环

设计理念：
真正的学习不是被动接收信息，
而是主动提出问题、探索答案、构建知识。
"""

import json
import os
import math
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Set, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict


class QuestionType(Enum):
    """问题类型"""
    WHAT = "what"           # 是什么：定义性问题
    WHY = "why"             # 为什么：因果性问题
    HOW = "how"             # 怎么做：方法性问题
    WHAT_IF = "what_if"     # 如果：假设性问题
    HOW_BETTER = "how_better"  # 如何更好：优化性问题
    CONNECTION = "connection"  # 关联：关系性问题


class ExplorationStatus(Enum):
    """探索状态"""
    PROPOSED = "proposed"
    EXPLORING = "exploring"
    HYPOTHESIS = "hypothesis"
    VERIFYING = "verifying"
    CONFIRMED = "confirmed"
    DISPROVED = "disproved"
    OPEN = "open"


class KnowledgeSourceType(Enum):
    """知识来源类型"""
    SELF_DERIVED = "self_derived"      # 自我推导
    EXTERNAL = "external"              # 外部获取
    INFERRED = "inferred"              # 推断得出
    EMERGED = "emerged"                # 涌现产生
    VALIDATED = "validated"            # 验证确认


@dataclass
class LearningQuestion:
    """学习问题"""
    id: str
    type: QuestionType
    content: str                   # 问题内容
    context: str                   # 问题上下文
    priority: float                # 优先级
    difficulty: float              # 难度估计
    
    status: ExplorationStatus
    hypothesis: Optional[str]      # 假设答案
    answer: Optional[str]          # 实际答案
    confidence: float              # 置信度
    
    related_questions: List[str]   # 相关问题
    dependencies: List[str]        # 依赖的问题
    
    created_time: str
    explored_time: Optional[str] = None
    resolved_time: Optional[str] = None
    
    # 学习成果
    knowledge_gained: List[str] = field(default_factory=list)
    insights: List[str] = field(default_factory=list)


@dataclass
class KnowledgeConcept:
    """知识概念"""
    id: str
    name: str
    definition: str
    properties: Dict[str, Any]
    relationships: Dict[str, str]   # 关系：{概念ID: 关系类型}
    examples: List[str]
    counterexamples: List[str]
    
    source: KnowledgeSourceType
    confidence: float
    validation_count: int
    
    created_time: str
    last_updated: str
    
    def update_confidence(self, delta: float) -> None:
        """更新置信度"""
        self.confidence = max(0, min(1, self.confidence + delta))
        self.last_updated = datetime.now().isoformat()


@dataclass
class Hypothesis:
    """假设"""
    id: str
    statement: str                 # 假设陈述
    prediction: str                # 预测
    test_method: str               # 测试方法
    
    status: ExplorationStatus
    evidence_for: List[str]        # 支持证据
    evidence_against: List[str]    # 反对证据
    
    confidence: float
    test_count: int
    
    created_time: str
    tested_time: Optional[str] = None


@dataclass
class LearningPath:
    """学习路径"""
    id: str
    topic: str
    questions: List[str]           # 问题ID列表
    concepts: List[str]            # 概念ID列表
    
    progress: float
    depth: float                   # 深入程度
    breadth: float                 # 广度
    
    started_time: str
    estimated_completion: Optional[str] = None


class SelfLearningEngine:
    """
    自学习引擎
    
    实现AI Agent的主动学习
    """
    
    def __init__(self, storage_path: str = "./memory/learning"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        
        # 问题系统
        self.questions: Dict[str, LearningQuestion] = {}
        self.question_queue: List[str] = []  # 待探索的问题队列
        
        # 知识系统
        self.concepts: Dict[str, KnowledgeConcept] = {}
        self.concept_graph: Dict[str, Set[str]] = defaultdict(set)  # 概念关联图
        
        # 假设系统
        self.hypotheses: Dict[str, Hypothesis] = {}
        
        # 学习路径
        self.learning_paths: Dict[str, LearningPath] = {}
        
        # 学习策略
        self.learning_strategies = self._init_learning_strategies()
        
        # 问题生成器
        self.question_generators = self._init_question_generators()
        
        # 探索回调
        self.exploration_callbacks: Dict[str, Callable] = {}
        
        # 统计
        self.stats = {
            'total_questions_generated': 0,
            'total_questions_resolved': 0,
            'total_hypotheses_tested': 0,
            'total_concepts_built': 0,
            'total_knowledge_gained': 0,
            'learning_efficiency': 0.5
        }
        
        self._load_state()
    
    def _init_learning_strategies(self) -> Dict[str, Dict]:
        """初始化学习策略"""
        return {
            'depth_first': {
                'description': '深入探索单一主题',
                'question_weight': {'what': 0.2, 'why': 0.4, 'how': 0.3, 'what_if': 0.1}
            },
            'breadth_first': {
                'description': '广泛探索多个主题',
                'question_weight': {'what': 0.5, 'why': 0.2, 'how': 0.2, 'what_if': 0.1}
            },
            'hypothesis_driven': {
                'description': '基于假设驱动学习',
                'question_weight': {'what_if': 0.4, 'why': 0.3, 'how': 0.2, 'what': 0.1}
            },
            'connection_focused': {
                'description': '专注于发现关联',
                'question_weight': {'connection': 0.5, 'what_if': 0.2, 'why': 0.2, 'how': 0.1}
            }
        }
    
    def _init_question_generators(self) -> Dict[QuestionType, Callable]:
        """初始化问题生成器"""
        return {
            QuestionType.WHAT: self._generate_what_question,
            QuestionType.WHY: self._generate_why_question,
            QuestionType.HOW: self._generate_how_question,
            QuestionType.WHAT_IF: self._generate_what_if_question,
            QuestionType.HOW_BETTER: self._generate_how_better_question,
            QuestionType.CONNECTION: self._generate_connection_question
        }
    
    # ==================== 核心学习循环 ====================
    
    def learning_cycle(self, context: Dict = None) -> Dict:
        """
        执行一个完整的学习循环
        
        问题生成 → 探索 → 假设 → 验证 → 知识构建
        """
        cycle_result = {
            'cycle_id': datetime.now().strftime('%Y%m%d%H%M%S'),
            'timestamp': datetime.now().isoformat(),
            'stages': {}
        }
        
        # Stage 1: 问题生成
        question_generation = self._generate_questions(context)
        cycle_result['stages']['question_generation'] = question_generation
        
        # Stage 2: 选择问题探索
        if self.question_queue:
            exploration = self._explore_question()
            cycle_result['stages']['exploration'] = exploration
            
            # Stage 3: 形成假设
            if exploration.get('findings'):
                hypothesis_formation = self._form_hypothesis(exploration)
                cycle_result['stages']['hypothesis_formation'] = hypothesis_formation
                
                # Stage 4: 验证假设
                if hypothesis_formation.get('hypothesis_id'):
                    validation = self._validate_hypothesis(
                        hypothesis_formation['hypothesis_id']
                    )
                    cycle_result['stages']['validation'] = validation
                    
                    # Stage 5: 知识构建
                    if validation.get('result'):
                        knowledge_building = self._build_knowledge(
                            exploration, 
                            hypothesis_formation, 
                            validation
                        )
                        cycle_result['stages']['knowledge_building'] = knowledge_building
        
        self._update_learning_efficiency(cycle_result)
        self._save_state()
        return cycle_result
    
    # ==================== 问题生成 ====================
    
    def _generate_questions(self, context: Dict = None) -> Dict:
        """生成问题"""
        result = {
            'new_questions': [],
            'total_in_queue': len(self.question_queue)
        }
        
        # 基于上下文生成问题
        if context:
            questions = self._context_based_generation(context)
            result['new_questions'].extend(questions)
        
        # 基于知识缺口生成问题
        gap_questions = self._gap_based_generation()
        result['new_questions'].extend(gap_questions)
        
        # 基于好奇心驱动生成问题
        curiosity_questions = self._curiosity_driven_generation()
        result['new_questions'].extend(curiosity_questions)
        
        # 添加到队列
        for qid in result['new_questions']:
            if qid not in self.question_queue:
                self.question_queue.append(qid)
        
        self.stats['total_questions_generated'] += len(result['new_questions'])
        
        return result
    
    def _context_based_generation(self, context: Dict) -> List[str]:
        """基于上下文生成问题"""
        questions = []
        
        # 从上下文提取主题
        topics = context.get('topics', [])
        for topic in topics[:2]:
            # 生成定义性问题
            q = self._generate_what_question(topic)
            if q:
                questions.append(q.id)
        
        return questions
    
    def _gap_based_generation(self) -> List[str]:
        """基于知识缺口生成问题"""
        questions = []
        
        # 检查概念图谱中的缺口
        for concept_id, concept in self.concepts.items():
            # 如果概念置信度低，生成验证性问题
            if concept.confidence < 0.5:
                q = LearningQuestion(
                    id=f"q_why_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
                    type=QuestionType.WHY,
                    content=f"为什么 {concept.name} 的定义是正确的？",
                    context=f"验证概念: {concept.name}",
                    priority=0.7,
                    difficulty=0.5,
                    status=ExplorationStatus.PROPOSED,
                    hypothesis=None,
                    answer=None,
                    confidence=0,
                    related_questions=[],
                    dependencies=[],
                    created_time=datetime.now().isoformat()
                )
                self.questions[q.id] = q
                questions.append(q.id)
        
        return questions[:3]
    
    def _curiosity_driven_generation(self) -> List[str]:
        """好奇心驱动的问题生成"""
        questions = []
        
        # 随机选择一个概念进行深入
        if self.concepts:
            concept = random.choice(list(self.concepts.values()))
            q = self._generate_what_if_question(concept.name)
            if q:
                questions.append(q.id)
        
        # 探索概念间的连接
        if len(self.concepts) >= 2:
            concepts = random.sample(list(self.concepts.keys()), 2)
            q = self._generate_connection_question(
                self.concepts[concepts[0]].name,
                self.concepts[concepts[1]].name
            )
            if q:
                questions.append(q.id)
        
        return questions
    
    def _generate_what_question(self, topic: str) -> Optional[LearningQuestion]:
        """生成"是什么"问题"""
        q = LearningQuestion(
            id=f"q_what_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=QuestionType.WHAT,
            content=f"{topic} 是什么？",
            context=f"探索主题: {topic}",
            priority=0.6,
            difficulty=0.3,
            status=ExplorationStatus.PROPOSED,
            hypothesis=None,
            answer=None,
            confidence=0,
            related_questions=[],
            dependencies=[],
            created_time=datetime.now().isoformat()
        )
        self.questions[q.id] = q
        return q
    
    def _generate_why_question(self, topic: str = "这个现象") -> Optional[LearningQuestion]:
        """生成"为什么"问题"""
        q = LearningQuestion(
            id=f"q_why_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=QuestionType.WHY,
            content=f"为什么 {topic} 会发生？",
            context="因果探索",
            priority=0.7,
            difficulty=0.6,
            status=ExplorationStatus.PROPOSED,
            hypothesis=None,
            answer=None,
            confidence=0,
            related_questions=[],
            dependencies=[],
            created_time=datetime.now().isoformat()
        )
        self.questions[q.id] = q
        return q
    
    def _generate_how_question(self, topic: str = "这个任务") -> Optional[LearningQuestion]:
        """生成"怎么做"问题"""
        q = LearningQuestion(
            id=f"q_how_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=QuestionType.HOW,
            content=f"如何完成 {topic}？",
            context="方法探索",
            priority=0.6,
            difficulty=0.5,
            status=ExplorationStatus.PROPOSED,
            hypothesis=None,
            answer=None,
            confidence=0,
            related_questions=[],
            dependencies=[],
            created_time=datetime.now().isoformat()
        )
        self.questions[q.id] = q
        return q
    
    def _generate_what_if_question(self, topic: str) -> Optional[LearningQuestion]:
        """生成"如果"问题"""
        scenarios = ["改变一个参数", "添加新条件", "移除限制", "反向思考"]
        scenario = random.choice(scenarios)
        
        q = LearningQuestion(
            id=f"q_wif_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=QuestionType.WHAT_IF,
            content=f"如果对 {topic} {scenario}，会发生什么？",
            context="假设性探索",
            priority=0.5,
            difficulty=0.7,
            status=ExplorationStatus.PROPOSED,
            hypothesis=None,
            answer=None,
            confidence=0,
            related_questions=[],
            dependencies=[],
            created_time=datetime.now().isoformat()
        )
        self.questions[q.id] = q
        return q
    
    def _generate_how_better_question(self, topic: str = "当前方法") -> Optional[LearningQuestion]:
        """生成"如何更好"问题"""
        q = LearningQuestion(
            id=f"q_hbt_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=QuestionType.HOW_BETTER,
            content=f"如何让 {topic} 变得更好？",
            context="优化探索",
            priority=0.6,
            difficulty=0.6,
            status=ExplorationStatus.PROPOSED,
            hypothesis=None,
            answer=None,
            confidence=0,
            related_questions=[],
            dependencies=[],
            created_time=datetime.now().isoformat()
        )
        self.questions[q.id] = q
        return q
    
    def _generate_connection_question(self, topic1: str, topic2: str) -> Optional[LearningQuestion]:
        """生成关联问题"""
        q = LearningQuestion(
            id=f"q_con_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            type=QuestionType.CONNECTION,
            content=f"{topic1} 和 {topic2} 之间有什么关系？",
            context="关联探索",
            priority=0.5,
            difficulty=0.5,
            status=ExplorationStatus.PROPOSED,
            hypothesis=None,
            answer=None,
            confidence=0,
            related_questions=[],
            dependencies=[],
            created_time=datetime.now().isoformat()
        )
        self.questions[q.id] = q
        return q
    
    # ==================== 探索机制 ====================
    
    def _explore_question(self) -> Dict:
        """探索问题"""
        if not self.question_queue:
            return {'status': 'no_questions'}
        
        # 选择优先级最高的问题
        qid = max(self.question_queue, 
                 key=lambda x: self.questions[x].priority if x in self.questions else 0)
        
        question = self.questions[qid]
        question.status = ExplorationStatus.EXPLORING
        question.explored_time = datetime.now().isoformat()
        
        # 执行探索
        exploration_result = self._execute_exploration(question)
        
        # 更新问题状态
        if exploration_result.get('findings'):
            question.status = ExplorationStatus.HYPOTHESIS
            question.insights.extend(exploration_result.get('insights', []))
        
        # 从队列移除
        self.question_queue.remove(qid)
        
        return {
            'question_id': qid,
            'question_type': question.type.value,
            'findings': exploration_result.get('findings', []),
            'insights': exploration_result.get('insights', [])
        }
    
    def _execute_exploration(self, question: LearningQuestion) -> Dict:
        """执行探索"""
        result = {
            'findings': [],
            'insights': []
        }
        
        # 检查是否有注册的探索回调
        callback = self.exploration_callbacks.get(question.type.value)
        if callback:
            callback_result = callback(question)
            result['findings'].extend(callback_result.get('findings', []))
            result['insights'].extend(callback_result.get('insights', []))
        
        # 默认探索逻辑
        # 基于问题类型进行不同的探索
        if question.type == QuestionType.WHAT:
            result['findings'].append(f"关于 '{question.content}' 的定义探索")
            result['insights'].append("需要构建清晰的定义")
        
        elif question.type == QuestionType.WHY:
            result['findings'].append(f"关于 '{question.content}' 的因果探索")
            result['insights'].append("需要识别因果关系")
        
        elif question.type == QuestionType.HOW:
            result['findings'].append(f"关于 '{question.content}' 的方法探索")
            result['insights'].append("需要找到有效的步骤")
        
        elif question.type == QuestionType.WHAT_IF:
            result['findings'].append(f"关于 '{question.content}' 的假设探索")
            result['insights'].append("需要进行情景推演")
        
        elif question.type == QuestionType.CONNECTION:
            result['findings'].append(f"关于 '{question.content}' 的关联探索")
            result['insights'].append("需要发现隐藏的连接")
        
        return result
    
    # ==================== 假设验证 ====================
    
    def _form_hypothesis(self, exploration: Dict) -> Dict:
        """形成假设"""
        question_id = exploration.get('question_id')
        if not question_id or question_id not in self.questions:
            return {'status': 'no_question'}
        
        question = self.questions[question_id]
        
        # 基于探索发现形成假设
        hypothesis = Hypothesis(
            id=f"h_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            statement=self._generate_hypothesis_statement(question, exploration),
            prediction=self._generate_prediction(question),
            test_method=self._determine_test_method(question.type),
            status=ExplorationStatus.HYPOTHESIS,
            evidence_for=[],
            evidence_against=[],
            confidence=0.3,
            test_count=0,
            created_time=datetime.now().isoformat()
        )
        
        self.hypotheses[hypothesis.id] = hypothesis
        question.hypothesis = hypothesis.statement
        
        return {
            'hypothesis_id': hypothesis.id,
            'statement': hypothesis.statement,
            'prediction': hypothesis.prediction
        }
    
    def _generate_hypothesis_statement(
        self, 
        question: LearningQuestion, 
        exploration: Dict
    ) -> str:
        """生成假设陈述"""
        insights = exploration.get('insights', [])
        if insights:
            return f"假设: 基于 {insights[0]}，{question.content}的答案可能是..."
        return f"假设: 对于 '{question.content}'，可能存在某种模式"
    
    def _generate_prediction(self, question: LearningQuestion) -> str:
        """生成预测"""
        return f"如果假设正确，那么应该观察到..."
    
    def _determine_test_method(self, question_type: QuestionType) -> str:
        """确定测试方法"""
        methods = {
            QuestionType.WHAT: "定义验证",
            QuestionType.WHY: "因果分析",
            QuestionType.HOW: "实践测试",
            QuestionType.WHAT_IF: "情景模拟",
            QuestionType.HOW_BETTER: "对比实验",
            QuestionType.CONNECTION: "关联验证"
        }
        return methods.get(question_type, "综合验证")
    
    def _validate_hypothesis(self, hypothesis_id: str) -> Dict:
        """验证假设"""
        if hypothesis_id not in self.hypotheses:
            return {'status': 'no_hypothesis'}
        
        hypothesis = self.hypotheses[hypothesis_id]
        hypothesis.status = ExplorationStatus.VERIFYING
        hypothesis.test_count += 1
        hypothesis.tested_time = datetime.now().isoformat()
        
        self.stats['total_hypotheses_tested'] += 1
        
        # 模拟验证过程
        validation_success = random.random() > 0.4  # 60%成功率
        
        if validation_success:
            hypothesis.status = ExplorationStatus.CONFIRMED
            hypothesis.confidence = min(1, hypothesis.confidence + 0.3)
            hypothesis.evidence_for.append("验证通过")
        else:
            # 可能是部分确认或反驳
            if random.random() > 0.5:
                hypothesis.status = ExplorationStatus.CONFIRMED
                hypothesis.confidence = min(1, hypothesis.confidence + 0.1)
                hypothesis.evidence_for.append("部分验证")
                hypothesis.evidence_against.append("存在例外情况")
            else:
                hypothesis.status = ExplorationStatus.DISPROVED
                hypothesis.evidence_against.append("验证失败")
        
        # 更新相关问题
        for qid, q in self.questions.items():
            if q.hypothesis == hypothesis.statement:
                if hypothesis.status == ExplorationStatus.CONFIRMED:
                    q.status = ExplorationStatus.CONFIRMED
                    q.confidence = hypothesis.confidence
                elif hypothesis.status == ExplorationStatus.DISPROVED:
                    q.status = ExplorationStatus.OPEN
                    q.hypothesis = None
        
        return {
            'hypothesis_id': hypothesis_id,
            'result': hypothesis.status.value,
            'confidence': hypothesis.confidence,
            'evidence_for': hypothesis.evidence_for,
            'evidence_against': hypothesis.evidence_against
        }
    
    # ==================== 知识构建 ====================
    
    def _build_knowledge(
        self, 
        exploration: Dict, 
        hypothesis_formation: Dict, 
        validation: Dict
    ) -> Dict:
        """构建知识"""
        result = {
            'concepts_created': [],
            'concepts_updated': [],
            'connections_established': []
        }
        
        if validation.get('result') == ExplorationStatus.CONFIRMED.value:
            hypothesis_id = validation.get('hypothesis_id')
            if hypothesis_id and hypothesis_id in self.hypotheses:
                hypothesis = self.hypotheses[hypothesis_id]
                
                # 创建新概念
                concept = KnowledgeConcept(
                    id=f"c_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
                    name=self._extract_concept_name(hypothesis.statement),
                    definition=hypothesis.statement,
                    properties={'confidence': hypothesis.confidence},
                    relationships={},
                    examples=exploration.get('findings', [])[:3],
                    counterexamples=[],
                    source=KnowledgeSourceType.SELF_DERIVED,
                    confidence=hypothesis.confidence,
                    validation_count=1,
                    created_time=datetime.now().isoformat(),
                    last_updated=datetime.now().isoformat()
                )
                
                self.concepts[concept.id] = concept
                result['concepts_created'].append(concept.id)
                self.stats['total_concepts_built'] += 1
                
                # 更新相关问题
                question_id = exploration.get('question_id')
                if question_id and question_id in self.questions:
                    question = self.questions[question_id]
                    question.answer = hypothesis.statement
                    question.status = ExplorationStatus.CONFIRMED
                    question.resolved_time = datetime.now().isoformat()
                    question.knowledge_gained.append(concept.id)
                    self.stats['total_questions_resolved'] += 1
                
                # 建立概念连接
                self._establish_concept_connections(concept.id)
        
        self.stats['total_knowledge_gained'] += len(result['concepts_created'])
        
        return result
    
    def _extract_concept_name(self, statement: str) -> str:
        """从假设陈述中提取概念名"""
        # 简化实现
        return f"概念_{datetime.now().strftime('%H%M%S')}"
    
    def _establish_concept_connections(self, concept_id: str) -> None:
        """建立概念连接"""
        if concept_id not in self.concepts:
            return
        
        new_concept = self.concepts[concept_id]
        
        # 与现有概念建立连接
        for existing_id, existing_concept in self.concepts.items():
            if existing_id != concept_id:
                # 基于某种相似性或关联性建立连接
                if random.random() > 0.7:  # 30%概率建立连接
                    new_concept.relationships[existing_id] = "related"
                    existing_concept.relationships[concept_id] = "related"
                    self.concept_graph[concept_id].add(existing_id)
                    self.concept_graph[existing_id].add(concept_id)
    
    def _update_learning_efficiency(self, cycle_result: Dict) -> None:
        """更新学习效率"""
        # 计算本次循环的效率
        efficiency_score = 0
        
        if cycle_result['stages'].get('question_generation', {}).get('new_questions'):
            efficiency_score += 0.2
        
        if cycle_result['stages'].get('exploration', {}).get('findings'):
            efficiency_score += 0.2
        
        if cycle_result['stages'].get('validation', {}).get('result') == 'confirmed':
            efficiency_score += 0.3
        
        if cycle_result['stages'].get('knowledge_building', {}).get('concepts_created'):
            efficiency_score += 0.3
        
        # 平滑更新
        self.stats['learning_efficiency'] = (
            self.stats['learning_efficiency'] * 0.7 + efficiency_score * 0.3
        )
    
    # ==================== 外部接口 ====================
    
    def register_exploration_callback(self, question_type: str, callback: Callable) -> None:
        """注册探索回调"""
        self.exploration_callbacks[question_type] = callback
    
    def add_external_knowledge(
        self, 
        name: str, 
        definition: str, 
        properties: Dict = None
    ) -> str:
        """添加外部知识"""
        concept = KnowledgeConcept(
            id=f"c_ext_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
            name=name,
            definition=definition,
            properties=properties or {},
            relationships={},
            examples=[],
            counterexamples=[],
            source=KnowledgeSourceType.EXTERNAL,
            confidence=0.8,
            validation_count=1,
            created_time=datetime.now().isoformat(),
            last_updated=datetime.now().isoformat()
        )
        
        self.concepts[concept.id] = concept
        self._establish_concept_connections(concept.id)
        self.stats['total_concepts_built'] += 1
        
        return concept.id
    
    def get_learning_report(self) -> Dict:
        """获取学习报告"""
        return {
            'questions': {
                'total_generated': self.stats['total_questions_generated'],
                'total_resolved': self.stats['total_questions_resolved'],
                'pending': len(self.question_queue),
                'by_status': self._count_questions_by_status()
            },
            'knowledge': {
                'total_concepts': len(self.concepts),
                'total_hypotheses': len(self.hypotheses),
                'avg_confidence': self._calculate_avg_concept_confidence(),
                'concept_connections': sum(len(v) for v in self.concept_graph.values()) // 2
            },
            'efficiency': self.stats['learning_efficiency']
        }
    
    def _count_questions_by_status(self) -> Dict[str, int]:
        """按状态统计问题"""
        counts = defaultdict(int)
        for q in self.questions.values():
            counts[q.status.value] += 1
        return dict(counts)
    
    def _calculate_avg_concept_confidence(self) -> float:
        """计算平均概念置信度"""
        if not self.concepts:
            return 0
        return sum(c.confidence for c in self.concepts.values()) / len(self.concepts)
    
    def get_pending_questions(self, limit: int = 10) -> List[Dict]:
        """获取待处理问题"""
        pending = [self.questions[qid] for qid in self.question_queue 
                  if qid in self.questions]
        return [{
            'id': q.id,
            'type': q.type.value,
            'content': q.content,
            'priority': q.priority,
            'status': q.status.value
        } for q in sorted(pending, key=lambda x: x.priority, reverse=True)[:limit]]
    
    def get_concept_network(self) -> Dict:
        """获取概念网络"""
        return {
            'nodes': [{'id': c.id, 'name': c.name, 'confidence': c.confidence}
                     for c in self.concepts.values()],
            'edges': [{'source': k, 'target': v, 'type': 'related'}
                     for k, vs in self.concept_graph.items() for v in vs]
        }
    
    def _load_state(self) -> None:
        """加载状态"""
        state_file = os.path.join(self.storage_path, 'learning_state.json')
        if os.path.exists(state_file):
            try:
                with open(state_file, 'r') as f:
                    data = json.load(f)
                
                self.stats = data.get('stats', self.stats)
                
                # 加载概念
                for cid, c_data in data.get('concepts', {}).items():
                    self.concepts[cid] = KnowledgeConcept(
                        id=c_data['id'],
                        name=c_data['name'],
                        definition=c_data['definition'],
                        properties=c_data.get('properties', {}),
                        relationships=c_data.get('relationships', {}),
                        examples=c_data.get('examples', []),
                        counterexamples=c_data.get('counterexamples', []),
                        source=KnowledgeSourceType(c_data.get('source', 'self_derived')),
                        confidence=c_data.get('confidence', 0.5),
                        validation_count=c_data.get('validation_count', 0),
                        created_time=c_data['created_time'],
                        last_updated=c_data['last_updated']
                    )
                    # 恢复概念图
                    for rel_id in c_data.get('relationships', {}).keys():
                        self.concept_graph[cid].add(rel_id)
                
            except Exception as e:
                print(f"加载状态失败: {e}")
    
    def _save_state(self) -> None:
        """保存状态"""
        state_file = os.path.join(self.storage_path, 'learning_state.json')
        
        data = {
            'stats': self.stats,
            'concepts': {cid: {
                'id': c.id,
                'name': c.name,
                'definition': c.definition,
                'properties': c.properties,
                'relationships': c.relationships,
                'examples': c.examples,
                'counterexamples': c.counterexamples,
                'source': c.source.value,
                'confidence': c.confidence,
                'validation_count': c.validation_count,
                'created_time': c.created_time,
                'last_updated': c.last_updated
            } for cid, c in self.concepts.items()}
        }
        
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)


def demo_learning():
    """演示自学习引擎"""
    print("=" * 60)
    print("自学习引擎演示")
    print("=" * 60)
    
    engine = SelfLearningEngine()
    
    # 添加一些初始知识
    engine.add_external_knowledge(
        "机器学习",
        "通过数据训练模型，使其能够进行预测或决策的技术"
    )
    engine.add_external_knowledge(
        "深度学习",
        "使用多层神经网络进行学习的机器学习方法"
    )
    
    print(f"\n初始知识: {len(engine.concepts)} 个概念")
    
    # 执行几个学习循环
    print("\n执行学习循环...")
    for i in range(3):
        print(f"\n--- 循环 {i+1} ---")
        result = engine.learning_cycle()
        
        gen = result['stages'].get('question_generation', {})
        print(f"问题生成: 新问题数={len(gen.get('new_questions', []))}")
        
        exp = result['stages'].get('exploration', {})
        print(f"探索: 类型={exp.get('question_type')}, 发现数={len(exp.get('findings', []))}")
        
        val = result['stages'].get('validation', {})
        if val:
            print(f"验证: 结果={val.get('result')}, 置信度={val.get('confidence', 0):.2f}")
        
        kb = result['stages'].get('knowledge_building', {})
        if kb:
            print(f"知识构建: 新概念数={len(kb.get('concepts_created', []))}")
    
    # 查看学习报告
    print("\n学习报告:")
    report = engine.get_learning_report()
    print(f"  问题: 总计={report['questions']['total_generated']}, 已解决={report['questions']['total_resolved']}")
    print(f"  知识: 概念数={report['knowledge']['total_concepts']}, 平均置信度={report['knowledge']['avg_confidence']:.2f}")
    print(f"  效率: {report['efficiency']:.2f}")


if __name__ == "__main__":
    demo_learning()
