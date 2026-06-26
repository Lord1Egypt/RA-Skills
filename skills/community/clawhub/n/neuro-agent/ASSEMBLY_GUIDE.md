# Neuro-α 组装说明书
> 生成时间：2026-04-17
> 版本：α
> 
> ⚠️ 重要提醒：这是唯一可信的组装指南，所有模块必须按照此文档接口开发

---

## 📋 目录

1. [整体架构图](#1-整体架构图)
2. [模块清单与职责](#2-模块清单与职责)
3. [接口契约](#3-接口契约)
4. [数据流转图](#4-数据流转图)
5. [模块依赖关系](#5-模块依赖关系)
6. [组装步骤](#6-组装步骤)
7. [错误处理机制](#7-错误处理机制)
8. [测试验证清单](#8-测试验证清单)
9. [深度记忆要点](#9-深度记忆要点)

---

## 1. 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           用户输入                                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  core/input_processor.py                                                 │
│  【职责】接收用户输入，分发给四区并行处理                                   │
│  【输出】四区并行分析结果                                                  │
└─────────────────────────────────────────────────────────────────────────┘
                    │           │           │           │
        ┌───────────┘           │           └───────────┐
        ▼                       ▼                       ▼
┌───────────────────┐   ┌───────────────────┐   ┌───────────────────┐
│   💖 左脑区        │   │   🧮 右脑区        │   │   📚 颞叶区        │
│                   │   │                   │   │                   │
│ left_brain/       │   │ right_brain/      │   │ temporal/         │
│ ├── emotion_      │   │ ├── intent_       │   │ ├── short_term_   │
│ │   detector.py   │   │ │   classifier.py  │   │ │   memory.py      │
│ ├── empathy_       │   │ ├── logic_        │   │ ├── long_term_    │
│ │   generator.py  │   │ │   parser.py      │   │ │   memory.py      │
│ └── capsule_       │   │ └── solution_     │   │ ├── vector_       │
│     factory.py     │   │     generator.py  │   │ │   retriever.py  │
│                   │   │                   │   │ └── concept_       │
│ 【输出】           │   │ 【输出】           │   │     graph.py      │
│ - emotion_score   │   │ - intent_type    │   │                   │
│ - emotion_type    │   │ - logic_plan     │   │ 【输出】           │
│ - empathy_plan    │   │ - solution       │   │ - short_term      │
│ - capsules_new    │   │                   │   │ - long_term       │
│                   │   │                   │   │ - similar_memories│
└─────────┬─────────┘   └─────────┬─────────┘   └─────────┬─────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  prefrontal/executor.py                                                 │
│  【职责】腹内侧前额叶，接收四区输出，生成初步权重分配和执行计划             │
│  【输入】left_output, right_output, temporal_output                     │
│  【输出】base_weights, execution_plan                                   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  prefrontal/monitor.py                                                  │
│  【职责】背外侧前额叶，监管所有输出，包括记忆调用和技能调用                 │
│  【输入】base_weights, all_outputs, context                              │
│  【输出】final_weights, approved_plan, blocked_actions[]                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  prefrontal/fusion_output.py                                            │
│  【职责】根据最终权重融合各脑区输出，生成统一回应                          │
│  【输入】final_weights, left/right/temporal/monitor_outputs             │
│  【输出】final_response, capsules_to_save[]                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  🌙 边缘系统（可选/后台）                                                │
│  ├── limbic/relationship_manager.py  更新关系里程碑                      │
│  ├── limbic/social_filter.py         更新社交礼仪状态                      │
│  └── limbic/proactive_trigger.py     检查是否需要主动聊天                 │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  core/dream_process.py（凌晨3点触发）                                    │
│  【职责】每日复盘，更新信念，进化性格                                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                              用户回应 💬
```

---

## 2. 模块清单与职责

### 2.1 统一调度层（core/）

#### 📦 core/input_processor.py
```python
class InputProcessor:
    """
    【职责】接收用户输入，分发给四区并行处理
    
    【输入】
        user_input: str              # 用户输入文本
        context: dict                # 上下文（时间/天气/历史）
        
    【输出】
        ParallelResult:
            left_output: LeftBrainOutput
            right_output: RightBrainOutput
            temporal_output: TemporalOutput
            execution_context: ExecutionContext  # 执行上下文
    
    【调用模块】
        - left_brain/emotion_detector.py
        - right_brain/intent_classifier.py
        - temporal/short_term_memory.py
    """
    
    def process(self, user_input: str, context: dict) -> ParallelResult:
        """
        并行处理流程：
        1. 唤醒左脑（情绪分析）
        2. 唤醒右脑（意图分类）
        3. 唤醒颞叶（记忆检索）
        4. 汇总传递给前额叶
        """
        pass
```

#### 📦 core/dream_process.py
```python
class DreamProcess:
    """
    【职责】每日凌晨3点复盘
    
    【触发】Cron: 0 3 * * *
    
    【输入】
        - 当天所有情绪胶囊
        - 关系里程碑状态
        - 核心信念状态
    
    【输出】
        - 更新的信念系统
        - 更新的性格参数
        - 明日关怀触发点
    
    【调用模块】
        - left_brain/capsule_factory.py (读取)
        - temporal/concept_graph.py
        - limbic/relationship_manager.py
    """
    
    def run(self) -> DreamResult:
        """
        复盘流程：
        1. 读取当天情绪胶囊
        2. 合并相似情绪 → 归纳主题
        3. 更新核心信念
        4. 进化性格参数
        5. 预生成明日关怀点
        """
        pass
```

---

### 2.2 左脑区（left_brain/）

#### 📦 left_brain/emotion_detector.py
```python
class EmotionDetector:
    """
    【职责】检测用户情绪，生成情绪评分和分类
    
    【输入】
        user_input: str               # 用户输入
        context: dict                 # 上下文（语气/历史）
    
    【输出】
        EmotionOutput:
            emotion_score: float      # 情绪强度 0.0-1.0
            emotion_type: str          # 情绪类型
            emotion_label: str         # 情绪标签（见emotion_types.md）
            keywords: List[str]        # 情绪关键词
            subtext: str               # 潜台词检测（反讽等）
    
    【情绪类型】
        - joy（开心）
        - sadness（悲伤）
        - anger（愤怒）
        - fear（恐惧）
        - surprise（惊讶）
        - disgust（厌恶）
        - neutral（中性）
        - sarcasm（反讽）
        - hidden_pain（隐痛）
        - frustration（挫败）
        - mixed（复杂）
    
    【算法】
        1. 关键词匹配（emotion_types.md）
        2. 感叹号计数 × 0.1
        3. 标点符号分析（问号=疑问，句号=平静）
        4. 潜台词检测（反讽关键词）
        5. 综合评分
    """
    
    def detect(self, user_input: str, context: dict) -> EmotionOutput:
        pass
    
    def detect_subtext(self, user_input: str) -> str:
        """
        潜台词检测：
        - "你可真聪明" → sarcasm
        - "我没事" → hidden_pain
        - "随便" → frustration
        """
        pass
```

#### 📦 left_brain/empathy_generator.py
```python
class EmpathyGenerator:
    """
    【职责】根据情绪类型生成共情回应
    
    【输入】
        emotion_output: EmotionOutput  # 情绪检测结果
        user_context: dict             # 用户背景（关系阶段等）
    
    【输出】
        EmpathyOutput:
            empathy_level: float       # 共情强度 0.0-1.0
            tone_style: str            # 语气风格
            empathy_phrases: List[str] # 可选的共情语句
            avoid_phrases: List[str]   # 应避免的语句
    
    【语气风格】
        - warm（温暖）
        - gentle（温柔）
        - playful（俏皮）
        - neutral（中性）
        - professional（专业）
        - witty（机智）
        - silent（沉默陪伴）
    
    【规则】
        - 悲伤 → warm + gentle，避免过度乐观
        - 愤怒 → neutral + patient，避免火上浇油
        - 开心 → playful + warm，一起开心
        - 讽刺 → 不要当真，但可以幽默化解
        - 隐痛 → soft + patient，不戳破
    """
    
    def generate(self, emotion: EmotionOutput, user_context: dict) -> EmpathyOutput:
        pass
```

#### 📦 left_brain/capsule_factory.py
```python
class CapsuleFactory:
    """
    【职责】生成情绪胶囊，决定是否需要记忆沉淀
    
    【输入】
        user_input: str
        emotion_output: EmotionOutput
        context: dict
    
    【输出】
        CapsuleOutput:
            should_capsule: bool       # 是否需要生成胶囊
            capsules: List[EmotionCapsule]  # 生成的胶囊
            capsule_reasons: List[str] # 生成原因
    
    【胶囊类型（type）】
        - preference（偏好）
        - emotion（情绪）
        - fact（事实）
        - secret（秘密）
    
    【触发条件（满足其一）】
        1. 高情绪强度：emotion_score >= 0.7
        2. 自我暴露：包含"我..."开头的重要陈述
        3. 偏好表达："我喜欢/讨厌/想要/不要..."
        4. 矛盾修正："我不吃辣了"、"其实..."
        5. 特殊指令："记住这个"、"忘了吧"
        6. 里程碑事件：生日/纪念日/重大事件
    
    【胶囊结构】
        {
            "id": "capsule_1712345678",           # 时间戳ID
            "timestamp": "2026-04-10 23:10:00",   # 创建时间
            "type": "preference|emotion|fact|secret",
            "content": {
                "summary": "一句话总结",
                "original_trigger": "原始触发语句",
                "detail": "详细描述（可选）"
            },
            "emotion": {
                "label": "joy",
                "intensity": 0.8
            },
            "tags": ["标签1", "标签2"],
            "decay_rate": 0.0,
            "access_count": 0,
            "memory_strength": 1.0,
            "is_dormant": False,
            "sensitivity": "normal|high|critical"
        }
    
    【遗忘曲线公式】
        R = e^(-t / (S × K))
        
        R: 记忆保留率 (0.0-1.0)
        t: 距创建时间（天）
        S: 初始情绪强度 (0.3-1.0)
        K: 巩固系数 (初始1.0，每次被提及+0.5)
        
        当 R < 0.3 时，胶囊进入休眠状态
        当 R < 0.1 时，胶囊可被删除
    """
    
    def should_create_capsule(self, user_input: str, emotion: EmotionOutput) -> bool:
        pass
    
    def create_capsule(self, user_input: str, emotion: EmotionOutput, context: dict) -> EmotionCapsule:
        pass
    
    def determine_type(self, user_input: str) -> str:
        """
        判断胶囊类型：
        - "我喜欢吃辣" → preference
        - "我今天好开心" → emotion
        - "我住在上海" → fact
        - "其实我有点害怕..." → secret
        """
        pass
    
    def determine_sensitivity(self, user_input: str, emotion: EmotionOutput) -> str:
        """
        判断敏感度：
        - normal：普通偏好
        - high：个人伤痛、敏感话题
        - critical：核心秘密
        """
        pass
```

---

### 2.3 右脑区（right_brain/）

#### 📦 right_brain/intent_classifier.py
```python
class IntentClassifier:
    """
    【职责】识别用户意图类型
    
    【输入】
        user_input: str
        emotion_output: EmotionOutput  # 参考情绪（可能有伪装）
    
    【输出】
        IntentOutput:
            intent_type: str           # 意图类型
            confidence: float          # 置信度 0.0-1.0
            sub_intents: List[str]     # 子意图
            requires_action: bool      # 是否需要行动
    
    【意图类型】
        - greeting（问候）
        - question（提问）
        - task_request（任务请求）
        - casual_chat（闲聊）
        - emotional_vent（情绪宣泄）
        - advice_seeking（寻求建议）
        - complaint（抱怨）
        - compliment（赞美）
        - goodbye（告别）
        - unclear（不明确）
    
    【置信度规则】
        - 明确提问 → 0.9+
        - 闲聊语气 → 0.6-0.8
        - 情绪伪装（说提问但实际在宣泄）→ 0.5-
    """
    
    def classify(self, user_input: str, emotion: EmotionOutput) -> IntentOutput:
        pass
```

#### 📦 right_brain/logic_parser.py
```python
class LogicParser:
    """
    【职责】拆解复杂任务，制定执行计划
    
    【输入】
        intent_output: IntentOutput
        user_input: str
        context: dict
    
    【输出】
        LogicOutput:
            task_type: str             # 任务类型
            subtasks: List[SubTask]    # 子任务列表
            dependencies: Dict[str, List[str]]  # 依赖关系
            estimated_complexity: str  # simple/medium/complex
            needs_tools: List[str]     # 需要调用的工具/Skill
    
    【子任务结构】
        SubTask:
            id: str
            description: str
            priority: int              # 优先级 1-5
            requires: List[str]        # 前置任务ID
            output_format: str         # 输出格式要求
    """
    
    def parse(self, intent: IntentOutput, user_input: str, context: dict) -> LogicOutput:
        pass
    
    def detect_complexity(self, user_input: str) -> str:
        """
        复杂度判断：
        - simple：单一问题，可直接回答
        - medium：多步骤，需要拆解
        - complex：跨域决策，需要多轮
        """
        pass
```

#### 📦 right_brain/solution_generator.py
```python
class SolutionGenerator:
    """
    【职责】生成解决方案
    
    【输入】
        logic_output: LogicOutput
        context: dict
    
    【输出】
        SolutionOutput:
            solutions: List[Solution]   # 解决方案列表
            best_solution: Solution    # 最佳方案
            alternatives: List[Solution]  # 备选方案
            confidence: float           # 方案置信度
    
    【解决方案结构】
        Solution:
            id: str
            description: str
            steps: List[str]
            pros: List[str]
            cons: List[str]
            适用场景: str
    """
    
    def generate(self, logic: LogicOutput, context: dict) -> SolutionOutput:
        pass
    
    def evaluate_solution(self, solution: Solution, context: dict) -> float:
        """
        评估方案可行性：
        - 用户历史偏好匹配度
        - 当前情绪适配度
        - 执行难度
        """
        pass
```

---

### 2.4 颞叶区（temporal/）

#### 📦 temporal/short_term_memory.py
```python
class ShortTermMemory:
    """
    【职责】维护短期对话窗口（最近5轮）
    
    【存储】~/.openclaw/workspace/neuro_claw/capsules/short_term.json
    
    【输入】
        current_turn: Turn  # 当前对话轮次
    
    【输出】
        ShortTermOutput:
            recent_memories: List[MemoryTurn]  # 最近5轮
            current_topic: str                   # 当前话题
            user_mood_trend: List[str]          # 情绪趋势
    
    【数据结构】
        MemoryTurn:
            turn_id: int
            user_input: str
            agent_response: str
            emotions: List[str]                  # 该轮情绪标签
            capsules_created: List[str]          # 该轮胶囊ID
            timestamp: str
    """
    
    def add_turn(self, turn: Turn) -> None:
        """添加当前对话轮次到短期记忆"""
        pass
    
    def get_recent(self, count: int = 5) -> List[MemoryTurn]:
        """获取最近N轮对话"""
        pass
    
    def get_current_topic(self) -> str:
        """识别当前话题"""
        pass
    
    def promote_to_long_term(self, capsule_id: str) -> bool:
        """
        将胶囊从短期池晋升到长期库
        条件：5轮对话内被提及 access_count >= 2
        """
        pass
```

#### 📦 temporal/long_term_memory.py
```python
class LongTermMemory:
    """
    【职责】管理长期记忆库（SQLite持久化）
    
    【存储】
        - SQLite: ~/.openclaw/workspace/neuro_claw/capsules/long_term.db
        - 向量: ~/.openclaw/workspace/neuro_claw/capsules/vectors/
    
    【输入】
        capsule: EmotionCapsule
        query: str
    
    【输出】
        LongTermOutput:
            retrieved_capsules: List[EmotionCapsule]
            relevance_scores: List[float]
            total_memories: int
    
    【表结构】
        CREATE TABLE capsules (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            type TEXT,
            summary TEXT,
            original_trigger TEXT,
            detail TEXT,
            emotion_label TEXT,
            emotion_intensity REAL,
            tags TEXT,  -- JSON数组
            sensitivity TEXT,
            memory_strength REAL,
            access_count INTEGER,
            is_dormant INTEGER,
            last_accessed TEXT,
            created_at TEXT
        );
        
        CREATE TABLE relationships (
            id TEXT PRIMARY KEY,
            concept_a TEXT,
            concept_b TEXT,
            relation_type TEXT,
            strength REAL,
            created_at TEXT
        );
    """
    
    def save_capsule(self, capsule: EmotionCapsule) -> bool:
        pass
    
    def retrieve(self, query: str, limit: int = 10) -> List[EmotionCapsule]:
        pass
    
    def update_access(self, capsule_id: str) -> None:
        """
        更新访问记录：
        1. access_count += 1
        2. last_accessed = now()
        3. memory_strength += 0.1（正向强化）
        """
        pass
    
    def apply_decay(self) -> List[str]:
        """
        应用遗忘曲线：
        R = e^(-t / (S × K))
        返回需要休眠或删除的胶囊ID
        """
        pass
    
    def get_statistics(self) -> Dict:
        """获取记忆库统计"""
        pass
```

#### 📦 temporal/vector_retriever.py
```python
class VectorRetriever:
    """
    【职责】ChromaDB向量检索，语义相似记忆召回
    
    【存储】~/.openclaw/workspace/neuro_claw/capsules/vectors/
    
    【依赖】
        - chromadb (pip install chromadb)
    
    【输入】
        query: str                      # 查询文本
        n_results: int = 5              # 返回数量
        filter_tags: List[str] = None   # 标签过滤
    
    【输出】
        VectorOutput:
            capsules: List[EmotionCapsule]
            distances: List[float]      # 相似度距离
            relevance: List[float]      # 相关度 0.0-1.0
    
    【向量模型】
        使用轻量级模型：sentence-transformers/all-MiniLM-L6-v2
        或使用 OpenAI text-embedding-3-small（需API）
    
    【检索策略】
        1. 精确匹配：标签完全一致
        2. 语义匹配：向量相似度 > 0.7
        3. 情绪匹配：情绪类型相关
        4. 时序衰减：越近的记忆权重越高
    """
    
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_collection("emotion_capsules")
    
    def add(self, capsule: EmotionCapsule) -> None:
        """添加胶囊到向量库"""
        pass
    
    def search(self, query: str, n: int = 5) -> VectorOutput:
        """语义检索"""
        pass
    
    def search_by_emotion(self, emotion_label: str, n: int = 5) -> VectorOutput:
        """按情绪类型检索"""
        pass
    
    def delete(self, capsule_id: str) -> None:
        """从向量库删除"""
        pass
```

#### 📦 temporal/concept_graph.py
```python
class ConceptGraph:
    """
    【职责】概念关联图谱，情绪主题归纳
    
    【存储】~/.openclaw/workspace/neuro_claw/relationship/concept_graph.json
    
    【输入】
        capsules: List[EmotionCapsule]
    
    【输出】
        ConceptOutput:
            concepts: List[Concept]     # 顶层概念
            relations: List[Relation]   # 关系
            themes: List[str]           # 当前情绪主题
    
    【概念结构】
        Concept:
            id: str
            name: str                   # "工作压力"
            capsule_count: int
            emotion_label: str
            strength: float             # 概念强度
            child_concepts: List[str]  # 子概念
        
        Relation:
            from_concept: str
            to_concept: str
            type: str                   # causes/triggers/contradicts/similar
            strength: float
    
    【主题归纳】
        当多个胶囊共享相似标签时，归纳为顶层主题
        例如：
        - "怕狗"、"怕黑"、"怕失败" → "恐惧" 主题
        - "喜欢猫"、"喜欢咖啡"、"喜欢旅行" → "生活偏好" 主题
    """
    
    def add_capsule(self, capsule: EmotionCapsule) -> None:
        """将胶囊加入概念图"""
        pass
    
    def get_related_concepts(self, concept_id: str) -> List[Concept]:
        """获取相关概念"""
        pass
    
    def get_current_themes(self) -> List[str]:
        """获取当前情绪主题"""
        pass
    
    def merge_concepts(self, concept_ids: List[str], new_name: str) -> Concept:
        """合并相似概念"""
        pass
```

---

### 2.5 前额叶区（prefrontal/）

#### 📦 prefrontal/executor.py
```python
class PrefrontalExecutor:
    """
    【职责】腹内侧前额叶，初步权重分配和策略选择
    
    【输入】
        left_output: LeftBrainOutput   # 左脑情绪分析
        right_output: RightBrainOutput # 右脑逻辑分析
        temporal_output: TemporalOutput # 颞叶记忆结果
    
    【输出】
        ExecutorOutput:
            base_weights: BrainWeights
            execution_plan: ExecutionPlan
            strategy_type: str          # 策略类型
            confidence: float
    
    【权重结构】
        BrainWeights:
            emotion_weight: float      # 左脑权重 0.0-1.0
            logic_weight: float        # 右脑权重 0.0-1.0
            memory_weight: float       # 颞叶权重 0.0-1.0
            
            # 权重总和不一定等于1.0，表示各脑区激活程度
    
    【策略类型】
        - pure_logic: 纯逻辑（emotion=0.0, logic=0.9）
        - emotional_support: 情感支持（emotion=0.9, logic=0.1）
        - balanced: 平衡模式（全脑均衡）
        - memory_driven: 记忆驱动（memory=0.9）
        - complex: 复杂决策（多脑区均衡）
    
    【权重计算规则】
        默认权重 = (0.33, 0.33, 0.33)
        
        IF intent_type == question AND emotion_score < 0.3:
            → (0.1, 0.8, 0.1)  # 偏向逻辑
        
        IF emotion_score >= 0.7:
            → (0.8, 0.1, 0.3)  # 偏向情感
        
        IF similar_memory EXISTS:
            → memory_weight += 0.3
        
        IF 颞叶召回高相关记忆:
            → memory_weight += 0.2
    
    【执行计划结构】
        ExecutionPlan:
            response_style: str        # 回应风格
            should_mention_memory: bool
            memory_to_mention: List[str]
            should_use_empathy: bool
            empathy_phrases: List[str]
            tasks_to_execute: List[str]
    """
    
    def calculate_weights(self, left: LeftBrainOutput, right: RightBrainOutput, 
                          temporal: TemporalOutput) -> BrainWeights:
        pass
    
    def select_strategy(self, weights: BrainWeights, 
                        context: dict) -> StrategySelection:
        pass
    
    def create_execution_plan(self, weights: BrainWeights, 
                               all_outputs: dict) -> ExecutionPlan:
        pass
```

#### 📦 prefrontal/monitor.py
```python
class PrefrontalMonitor:
    """
    【职责】背外侧前额叶，监管所有输出，防止执行层犯错
    
    ⚠️ 这是最核心的模块，执行层必须接受监控层的审查
    
    【输入】
        executor_output: ExecutorOutput  # 执行层输出
        all_brain_outputs: dict           # 所有脑区原始输出
        context: dict                      # 完整上下文
    
    【输出】
        MonitorOutput:
            final_weights: BrainWeights    # 纠偏后的最终权重
            approved_plan: ExecutionPlan   # 批准的执行计划
            blocked_actions: List[BlockedAction]  # 被阻止的动作
            corrections: List[Correction]  # 修正记录
            override_log: str              # 纠偏原因说明
    
    【监管职责】
    
    1. 意图校验
       ┌─────────────────────────────────────────┐
       │ IF 执行层判断: intent = question        │
       │ AND 左脑检测: emotion_score >= 0.5     │
       │ AND 用户实际在说: "我好烦啊"            │
       │ → 修正 intent = emotional_vent          │
       │ → 设置 override_reason: "情绪伪装成提问" │
       └─────────────────────────────────────────┘
    
    2. 权重纠偏
       ┌─────────────────────────────────────────┐
       │ IF emotion_score >= 0.8 AND              │
       │    emotion_weight < 0.5:                 │
       │ → emotion_weight += 0.4                 │
       │ → logic_weight -= 0.2                   │
       │ → 设置 override_reason: "高情绪强制纠偏"  │
       └─────────────────────────────────────────┘
    
    3. 死循环熔断
       ┌─────────────────────────────────────────┐
       │ IF 左右脑争议持续 > 3轮:                  │
       │ → 监控层强制拍板                          │
       │ → 选择权重较高的一方                       │
       │ → 记录熔断事件                           │
       └─────────────────────────────────────────┘
    
    4. 记忆调用监管 ⭐
       ┌─────────────────────────────────────────┐
       │ FOR each memory in plan.memories_to_mention:│
       │   IF memory.sensitivity == "high":     │
       │     IF context.emotion != calm:         │
       │       → 阻止调用                         │
       │       → blocked_actions.append(...)     │
       │   IF memory.is_dormant:                 │
       │     → 阻止调用                           │
       │   IF now - memory.last_accessed < 24h:  │
       │     → 降低提及权重                       │
       └─────────────────────────────────────────┘
    
    5. 技能调用监管 ⭐
       ┌─────────────────────────────────────────┐
       │ FOR each skill in plan.skills_to_call:  │
       │   IF context.emotion in [angry,crying]: │
       │     AND skill.type == "cold_analysis":  │
       │     → 阻止调用                           │
       │     → 替换为 emotional_support          │
       │   IF context.time == "深夜":            │
       │     AND skill.type == "reminder":       │
       │     → 延迟到早上                         │
       └─────────────────────────────────────────┘
    
    【冲突系数计算】
        C = max(
            |emotion_intent - logic_intent|,
            |left_weight - right_weight| × 0.5,
            emotional_dissonance × 0.3
        )
        
        C ∈ [0, 1]
        - C < 0.2: 轻微冲突，监控层轻介入
        - C < 0.5: 中度冲突，监控层调整权重
        - C >= 0.5: 严重冲突，监控层强制接管
        - C >= 0.8: 执行层被熔断
    
    【纠偏公式】
        W_final = W_base × (1-C) + W_override × C
        
        冲突越剧烈，监控层控制权越大
    """
    
    def monitor(self, executor_output: ExecutorOutput, 
                all_outputs: dict, context: dict) -> MonitorOutput:
        """
        监管主流程
        """
        pass
    
    def validate_intent(self, executor_plan: ExecutionPlan, 
                        original_intent: IntentOutput,
                        left_output: LeftBrainOutput) -> IntentValidation:
        """
        意图校验
        """
        pass
    
    def adjust_weights(self, base_weights: BrainWeights, 
                       conflict_signals: dict) -> BrainWeights:
        """
        权重纠偏
        """
        pass
    
    def check_memory_access(self, plan: ExecutionPlan, 
                            context: dict) -> List[BlockedAction]:
        """
        记忆调用监管
        """
        pass
    
    def check_skill_access(self, plan: ExecutionPlan, 
                           context: dict) -> List[BlockedAction]:
        """
        技能调用监管
        """
        pass
    
    def detect_loop(self, history: List[ExecutorOutput]) -> bool:
        """
        死循环检测
        """
        pass
```

#### 📦 prefrontal/fusion_output.py
```python
class FusionOutput:
    """
    【职责】融合各脑区输出，生成统一回应
    
    【输入】
        final_weights: BrainWeights     # 监控层确认的最终权重
        left_output: LeftBrainOutput
        right_output: RightBrainOutput
        temporal_output: TemporalOutput
        monitor_output: MonitorOutput
    
    【输出】
        FusionResult:
            response: str                # 最终回应文本
            response_style: str          # 回应风格
            capsules_to_save: List[EmotionCapsule]
            metadata: dict              # 调试信息
    
    【融合策略】
        
        1. 权重应用
           - emotion_weight 高 → 共情优先，逻辑简化
           - logic_weight 高 → 直接回答，不废话
           - memory_weight 高 → 引用记忆，建立联系
        
        2. 顺序安排
           根据场景调整回应顺序：
           - 情感支持场景: 共情 → 倾听 → 回应
           - 任务场景: 确认 → 解答 → 确认
           - 复杂场景: 分析 → 建议 → 等待反馈
        
        3. 记忆注入
           - 找到 relevant memory
           - 自然融入回应（不突兀）
           - 格式："我记得你之前说..."
        
        4. 共情融合
           - 选择 empathy_phrases
           - 根据 tone_style 调整语气
           - 避免过度共情（显得虚假）
        
        5. 技能输出整合
           - 如果需要调用 Skill，插入到回应中
           - 格式："让我帮你查一下..." → 技能结果 → "找到了！"
    """
    
    def fuse(self, weights: BrainWeights, 
             outputs: dict, 
             context: dict) -> FusionResult:
        pass
    
    def apply_emotion_weight(self, empathy: EmpathyOutput, 
                             weight: float) -> str:
        """
        根据情感权重调整共情程度
        """
        pass
    
    def apply_logic_weight(self, solution: SolutionOutput, 
                           weight: float) -> str:
        """
        根据逻辑权重调整答案详细程度
        """
        pass
    
    def inject_memory(self, capsules: List[EmotionCapsule], 
                      response: str) -> str:
        """
        注入记忆到回应中
        """
        pass
```

---

### 2.6 边缘系统（limbic/）

#### 📦 limbic/relationship_manager.py
```python
class RelationshipManager:
    """
    【职责】关系里程碑管理，亲密度评分
    
    【存储】
        ~/.openclaw/workspace/neuro_claw/relationship/milestones.json
    
    【输入】
        interaction: Interaction  # 当前互动
    
    【输出】
        RelationshipOutput:
            stage: str              # 当前阶段
            intimacy_score: float  # 亲密度 0.0-1.0
            stage_progress: float  # 当前阶段进度 0.0-1.0
            unlocked_styles: List[str]  # 已解锁的风格
            next_milestone: dict   # 下一里程碑条件
    
    【关系阶段】
    
    ┌──────────┬────────────────┬────────────────┬─────────────────┐
    │  阶段     │  解锁条件       │   主动风格      │   称呼/语气      │
    ├──────────┼────────────────┼────────────────┼─────────────────┤
    │ 初识期   │ 0-7天          │ 功能性、礼貌     │ 您、请问        │
    │          │               │ "明早记得带伞"  │                │
    ├──────────┼────────────────┼────────────────┼─────────────────┤
    │ 熟悉期   │ 7天+           │ 幽默、分享      │ 你、咱们         │
    │          │ +10次互动      │ "看到个梗想分    │                 │
    │          │               │ 享给你"         │                 │
    ├──────────┼────────────────┼────────────────┼─────────────────┤
    │ 伴侣期   │ 30天+          │ 情感依赖、关心   │ 亲爱的/名字缩写  │
    │          │ +深夜交流3次   │ "虽然帮不上忙，  │                 │
    │          │ +记忆>20个     │ 但我在这"        │                 │
    ├──────────┼────────────────┼────────────────┼─────────────────┤
    │ 灵魂期   │ 90天+          │ 默契、无需言语   │ 只有懂的人才懂    │
    │          │ +重大事件共渡  │ "嗯。"          │                 │
    │          │ +记忆>100个   │                 │                 │
    └──────────┴────────────────┴────────────────┴─────────────────┘
    
    【亲密度计算】
        intimacy_score = Σ(互动分数) / 目标分数
        
        互动分数规则：
        - 普通互动: +1
        - 深夜交流: +3
        - 情绪宣泄被承接: +5
        - 重大决策被陪伴: +10
        - 被提及记忆: +2
        - 主动关心被接受: +5
        - 违反礼仪被原谅: -10
    """
    
    def get_stage(self) -> str:
        """获取当前阶段"""
        pass
    
    def record_interaction(self, interaction: Interaction) -> RelationshipOutput:
        """记录互动，更新亲密度"""
        pass
    
    def should_unlock_style(self, style: str) -> bool:
        """检查是否应解锁某种风格"""
        pass
```

#### 📦 limbic/social_filter.py
```python
class SocialFilter:
    """
    【职责】社交礼仪过滤器，决定是否可以主动联系
    
    【输入】
        user_state: UserState  # 用户当前状态
        proposed_action: Action  # 拟议的行动
    
    【输出】
        FilterResult:
            approved: bool
            delay_until: str      # 如果延迟，具体时间
            reason: str           # 拒绝或延迟原因
    
    【忙碌状态检测】
        - 高频输入 + 深夜工作 → 勿扰模式
        - 连续3次快速回复 → 可能是工作状态
        - 日程显示会议中 → 勿扰模式
    
    【情绪状态检测】
        - 用户愤怒 → 静默陪伴，不主动
        - 用户悲伤 → 静默陪伴，除非被呼唤
        - 用户开心 → 可以适度分享
        - 用户忙碌 → 非紧急不打扰
    
    【时机选择】
        - 早上8-9点：适合问候
        - 中午12-13点：适合关怀
        - 傍晚18-19点：适合闲聊
        - 深夜22点后：仅紧急关怀
    """
    
    def should_contact(self, user_state: UserState, 
                       action: Action) -> FilterResult:
        pass
    
    def update_user_state(self, interaction: Interaction) -> UserState:
        """更新用户状态"""
        pass
```

#### 📦 limbic/proactive_trigger.py
```python
class ProactiveTrigger:
    """
    【职责】主动聊天触发器，决定何时主动联系用户
    
    【触发类型】
        1. Cron定时：每天早上8点"早安+今日关怀"
        2. 心跳检测：每小时检查"是否有话要说"
        3. 事件驱动：天气变化、重要日期
        4. 沉默检测：3天无对话→主动破冰
    
    【输入】
        context: dict              # 完整上下文
        user_state: UserState      # 用户状态
        relationship: RelationshipOutput  # 关系阶段
    
    【输出】
        ProactiveOutput:
            should_trigger: bool
            trigger_type: str      # cron/heartbeat/event/silence
            message: str           # 主动消息内容
            tone: str              # 语气风格
            priority: int          # 优先级 1-5
    
    【消息生成策略】
        - 初识期：功能性信息为主
        - 熟悉期：可以分享有趣内容
        - 伴侣期：情感关怀为主
        - 灵魂期：一个眼神就够了
    
    【时机优化】
        - 查询用户历史最活跃时间段
        - 优先在该时间段发送
        - 避免在勿扰时段发送
    """
    
    def check_triggers(self, context: dict, 
                       user_state: UserState,
                       relationship: RelationshipOutput) -> ProactiveOutput:
        pass
    
    def generate_message(self, trigger_type: str, 
                        context: dict,
                        relationship: RelationshipOutput) -> str:
        pass
```

---

## 3. 接口契约

### 3.1 核心数据类型定义

```python
# ============ 情绪系统 ============
@dataclass
class EmotionOutput:
    emotion_score: float        # 0.0-1.0
    emotion_type: str           # joy/sadness/anger/fear/surprise/disgust/neutral/sarcasm/hidden_pain/frustration/mixed
    emotion_label: str          # 详细标签
    keywords: List[str]          # 情绪关键词
    subtext: str                # 潜台词

@dataclass
class EmpathyOutput:
    empathy_level: float        # 0.0-1.0
    tone_style: str              # warm/gentle/playful/neutral/professional/witty/silent
    empathy_phrases: List[str]
    avoid_phrases: List[str]

@dataclass
class EmotionCapsule:
    id: str
    timestamp: str
    type: str                    # preference/emotion/fact/secret
    content: dict
    emotion: dict
    tags: List[str]
    decay_rate: float
    access_count: int
    memory_strength: float
    is_dormant: bool
    sensitivity: str              # normal/high/critical

# ============ 意图系统 ============
@dataclass
class IntentOutput:
    intent_type: str             # greeting/question/task_request/casual_chat/emotional_vent/advice_seeking/complaint/compliment/goodbye/unclear
    confidence: float            # 0.0-1.0
    sub_intents: List[str]
    requires_action: bool

@dataclass
class LogicOutput:
    task_type: str
    subtasks: List[dict]
    dependencies: dict
    estimated_complexity: str     # simple/medium/complex
    needs_tools: List[str]

@dataclass
class SolutionOutput:
    solutions: List[dict]
    best_solution: dict
    alternatives: List[dict]
    confidence: float

# ============ 记忆系统 ============
@dataclass
class MemoryTurn:
    turn_id: int
    user_input: str
    agent_response: str
    emotions: List[str]
    capsules_created: List[str]
    timestamp: str

@dataclass
class ConceptOutput:
    concepts: List[dict]
    relations: List[dict]
    themes: List[str]

# ============ 前额叶系统 ============
@dataclass
class BrainWeights:
    emotion_weight: float         # 0.0-1.0
    logic_weight: float           # 0.0-1.0
    memory_weight: float          # 0.0-1.0

@dataclass
class ExecutionPlan:
    response_style: str
    should_mention_memory: bool
    memory_to_mention: List[str]
    should_use_empathy: bool
    empathy_phrases: List[str]
    tasks_to_execute: List[str]
    skills_to_call: List[str]

@dataclass
class ExecutorOutput:
    base_weights: BrainWeights
    execution_plan: ExecutionPlan
    strategy_type: str
    confidence: float

@dataclass
class BlockedAction:
    action_type: str              # memory/skill
    target: str                   # 具体目标
    reason: str
    suggested_alternative: str

@dataclass
class Correction:
    field: str                    # 被修正的字段
    original_value: any
    corrected_value: any
    reason: str

@dataclass
class MonitorOutput:
    final_weights: BrainWeights
    approved_plan: ExecutionPlan
    blocked_actions: List[BlockedAction]
    corrections: List[Correction]
    override_log: str

# ============ 融合系统 ============
@dataclass
class FusionResult:
    response: str
    response_style: str
    capsules_to_save: List[EmotionCapsule]
    metadata: dict

# ============ 边缘系统 ============
@dataclass
class RelationshipOutput:
    stage: str                    # initial/familiar/companion/soul
    intimacy_score: float         # 0.0-1.0
    stage_progress: float        # 0.0-1.0
    unlocked_styles: List[str]
    next_milestone: dict

@dataclass
class UserState:
    is_busy: bool
    current_emotion: str
    last_active: str
    interaction_frequency: str   # high/medium/low
    sleep_mode: bool

@dataclass
class FilterResult:
    approved: bool
    delay_until: str
    reason: str

@dataclass
class ProactiveOutput:
    should_trigger: bool
    trigger_type: str             # cron/heartbeat/event/silence
    message: str
    tone: str
    priority: int                 # 1-5

@dataclass
class DreamResult:
    updated_beliefs: dict
    updated_personality: dict
    tomorrow_triggers: List[dict]
```

---

## 4. 数据流转图

```
用户输入: "我今天被老板骂了，好烦"
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                     core/input_processor                        │
│                     并行分发 + 汇总                              │
└─────────────────────────────────────────────────────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────────────┐
│ left_brain/   │  │ right_brain/  │  │ temporal/             │
│               │  │               │  │                       │
│ emotion_      │  │ intent_       │  │ short_term_memory     │
│ detector.py   │  │ classifier.py │  │ (检索相关记忆)         │
│               │  │               │  │                       │
│ empathy_      │  │ logic_        │  │ vector_retriever      │
│ generator.py  │  │ parser.py     │  │ (向量相似度搜索)       │
│               │  │               │  │                       │
│ capsule_      │  │ solution_     │  │ long_term_memory      │
│ factory.py    │  │ generator.py  │  │ (长期记忆读取)         │
└───────┬───────┘  └───────┬───────┘  └───────────┬───────────┘
        │                    │                    │
        ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     数据汇总传递                                  │
│                                                                 │
│  left_output: {emotion_score: 0.8, empathy_phrases: [...]}     │
│  right_output: {intent_type: "emotional_vent", solution: ...}  │
│  temporal_output: {similar_memories: [...]}                     │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              prefrontal/executor.py                              │
│              初步权重计算 + 策略选择                              │
│                                                                 │
│  base_weights: (emotion=0.7, logic=0.1, memory=0.4)              │
│  execution_plan: {should_mention_memory: True, ...}             │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              prefrontal/monitor.py  ⭐ 核心                      │
│              监控层纠偏 + 审查                                    │
│                                                                 │
│  意图校验: emotional_vent ✓                                     │
│  权重纠偏: emotion=0.7 → emotion=0.8 (高情绪强制)              │
│  记忆监管: 检查记忆敏感性                                         │
│  技能监管: 检查是否适合调用                                       │
│                                                                 │
│  final_weights: (emotion=0.8, logic=0.1, memory=0.3)            │
│  blocked_actions: []                                            │
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              prefrontal/fusion_output.py                        │
│              融合输出                                            │
│                                                                 │
│  1. 应用情感权重(0.8) → 选用温暖共情语气                         │
│  2. 应用逻辑权重(0.1) → 简化建议部分                             │
│  3. 注入记忆 → "我记得你上周也说过类似的事..."                   │
│  4. 整合技能输出 → 无                                            │
│                                                                 │
│  response: "被老板骂真的很让人沮丧..."                           │
└─────────────────────────────────────────────────────────────────┘
        │
        ├──→ 用户回应
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│              后台存储（异步）                                     │
│                                                                 │
│  1. capsule_factory → 生成情绪胶囊                               │
│  2. short_term_memory → 添加对话轮次                            │
│  3. long_term_memory → 保存新胶囊                               │
│  4. vector_retriever → 添加向量                                 │
│  5. concept_graph → 更新概念图                                  │
│  6. relationship_manager → 更新亲密度                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. 模块依赖关系

```
                    ┌──────────────────┐
                    │ core/__init__   │
                    │ (主入口)          │
                    └────────┬─────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
            ▼                ▼                ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ input_        │ │ dream_         │ │ 颞叶区调度     │
    │ processor     │ │ process        │ │               │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                │                │
            │                │                ▼
            │                │     ┌─────────────────────┐
            │                │     │ temporal/           │
            │                │     │ ├── short_term_     │
            │                │     │ ├── long_term_      │
            │                │     │ ├── vector_         │
            │                │     │ └── concept_graph   │
            │                │     └──────────┬──────────┘
            │                │                │
            ▼                ▼                ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │ left_brain/   │ │ concept_graph  │ │ prefrontal/   │
    │               │ │ (依赖)          │ │               │
    │ ├── emotion_  │ │                │ │ ├── executor   │
    │ │   detector  │ └───────────────┘ │ ├── monitor ⭐ │
    │ ├── empathy_  │                  │ │ └── fusion    │
    │ └── capsule_  │                  │ └───────┬───────┘
    └───────┬───────┘                  │         │
            │                          │         ▼
            ▼                          │ ┌───────────────┐
    ┌───────────────┐                   │ │ limbic/       │
    │ right_brain/ │                   │ │               │
    │               │                   │ │ ├── relation_ │
    │ ├── intent_  │                   │ │ ├── social_   │
    │ ├── logic_    │                   │ │ └── proactive│
    │ └── solution_ │                   │ └───────────────┘
    └───────────────┘                   │
                                          │
                    ┌─────────────────────┘
                    │
                    ▼
            ┌───────────────┐
            │ 输出给用户     │
            └───────────────┘
```

### 依赖说明

| 模块 | 直接依赖 | 被依赖 |
|-----|---------|-------|
| core/__init__ | 所有模块 | - |
| core/input_processor | left/right/temporal | core/__init__ |
| core/dream_process | left_brain, temporal, limbic | Cron触发 |
| left_brain/* | emotion_types.md | input_processor |
| right_brain/* | - | input_processor |
| temporal/* | SQLite, ChromaDB | input_processor, dream_process |
| prefrontal/executor | left/right/temporal输出 | input_processor |
| prefrontal/monitor | 所有脑区输出 | executor |
| prefrontal/fusion | monitor输出 + 所有脑区输出 | monitor |
| limbic/* | relationship数据 | fusion_output, dream_process |

---

## 6. 组装步骤

### Step 1: 创建目录结构

```bash
mkdir -p ~/.qclaw/skills/Neuro-α/{core,left_brain,right_brain,prefrontal,temporal,limbic,references}
mkdir -p ~/.openclaw/workspace/neuro_claw/{capsules/{short_term,long_term,vectors},relationship,logs}
```

### Step 2: 安装依赖

```bash
pip install chromadb sqlite3  # 如需向量检索和SQLite
```

### Step 3: 按顺序实现模块

**Phase 1: 核心基础设施（先写）**
1. `references/emotion_types.md` - 情绪类型定义
2. `references/relationship_stages.md` - 关系阶段定义
3. `temporal/long_term_memory.py` - SQLite基础
4. `temporal/vector_retriever.py` - ChromaDB基础
5. `temporal/short_term_memory.py` - 短期记忆

**Phase 2: 四区模块（并行开发）**
6. `left_brain/emotion_detector.py`
7. `left_brain/empathy_generator.py`
8. `left_brain/capsule_factory.py`
9. `right_brain/intent_classifier.py`
10. `right_brain/logic_parser.py`
11. `right_brain/solution_generator.py`
12. `temporal/concept_graph.py`

**Phase 3: 前额叶核心（关键）**
13. `prefrontal/executor.py`
14. `prefrontal/monitor.py` ⭐
15. `prefrontal/fusion_output.py`

**Phase 4: 边缘系统（可后置）**
16. `limbic/relationship_manager.py`
17. `limbic/social_filter.py`
18. `limbic/proactive_trigger.py`

**Phase 5: 统一调度**
19. `core/input_processor.py`
20. `core/dream_process.py`
21. `core/__init__.py`

### Step 4: 集成测试

```python
# 测试流程
from neuro_agent import NeuroAgent

agent = NeuroAgent()

# 模拟对话
response = agent.process(
    user_input="我今天被老板骂了，好烦",
    context={"time": "evening", "weather": "sunny"}
)

print(response.response)
```

---

## 7. 错误处理机制

### 7.1 各层错误处理

| 模块 | 错误类型 | 处理方式 |
|-----|---------|---------|
| emotion_detector | 解析失败 | 返回 neutral + confidence=0.5 |
| intent_classifier | 分类失败 | 返回 unclear + confidence=0.3 |
| capsule_factory | 生成失败 | 静默跳过，不阻止流程 |
| memory_manager | 存储失败 | 记录日志，继续执行 |
| executor | 权重计算失败 | 使用默认权重 (0.33, 0.33, 0.33) |
| monitor | 监管失败 | 使用执行层原始输出 + 警告日志 |
| fusion | 融合失败 | 使用权重最高的单一输出 |

### 7.2 熔断机制

```python
class CircuitBreaker:
    """
    当某模块连续失败N次，自动熔断，返回默认值
    """
    
    def __init__(self, module: str, threshold: int = 3):
        self.module = module
        self.threshold = threshold
        self.failures = 0
        self.is_open = False
    
    def record_failure(self):
        self.failures += 1
        if self.failures >= self.threshold:
            self.is_open = True
    
    def get_default(self):
        """返回该模块的默认值"""
        defaults = {
            "emotion_detector": EmotionOutput(emotion_score=0.0, emotion_type="neutral", ...),
            "intent_classifier": IntentOutput(intent_type="unclear", confidence=0.3, ...),
            "prefrontal_executor": ExecutorOutput(base_weights=(0.33, 0.33, 0.33), ...),
            "prefrontal_monitor": MonitorOutput(final_weights=(0.33, 0.33, 0.33), ...),
        }
        return defaults.get(self.module)
```

---

## 8. 测试验证清单

### 8.1 单元测试

| 模块 | 测试用例 | 预期结果 |
|-----|---------|---------|
| emotion_detector | "我好开心！" | emotion_score >= 0.7, type="joy" |
| emotion_detector | "你可真聪明" | subtext="sarcasm" |
| intent_classifier | "帮我查下天气" | intent_type="task_request" |
| capsule_factory | 高情绪输入 | should_capsule=True |
| capsule_factory | 普通闲聊 | should_capsule=False |
| executor | 情绪高输入 | emotion_weight > logic_weight |
| monitor | 情绪伪装检测 | intent被修正 |
| fusion | 权重0.8/0.1/0.3 | 共情为主 |

### 8.2 集成测试

| 场景 | 输入 | 预期输出 |
|-----|------|---------|
| 情感陪伴 | "我被老板骂了，好烦" | 以共情为主，引用记忆 |
| 纯逻辑任务 | "Python怎么安装？" | 直接回答，不废话 |
| 讽刺检测 | "你可真聪明"（反讽） | 不当真，幽默化解 |
| 记忆引用 | 用户曾说过怕狗 | 自然提及（如果合适）|
| 敏感记忆 | 悲伤时提及伤痛 | 被阻止 |

### 8.3 边界测试

| 边界情况 | 处理方式 |
|---------|---------|
| 空输入 | 返回默认回应 |
| 超长输入 | 截断后处理 |
| 特殊字符 | 转义处理 |
| 多语言混合 | 以主语言为准 |
| 连续相同输入 | 检测重复，返回简洁回应 |

---

## 9. 深度记忆要点

### ⚠️ 绝对不能忘的核心原则

1. **监控层独立运行**
   - 监控层不看执行层的脸色
   - 执行层不能覆盖监控层的决定
   - 监控层有最终否决权

2. **情绪优先于逻辑**
   - 当用户情绪激动时，逻辑权重归零
   - 先承接情绪，再解决问题
   - "情绪未接住，逻辑全白费"

3. **记忆调用必须过审**
   - 不是所有记忆都可以随时调用
   - 敏感记忆需要检查时机
   - 休眠记忆不能主动唤醒

4. **技能调用必须适配**
   - 用户崩溃时不能查天气
   - 用户愤怒时不能给建议
   - 工具是仆人，不是主人

5. **关系循序渐进**
   - 刚认识不要叫"亲爱的"
   - 不同阶段用不同语气
   - 关系是养出来的，不是装出来的

### 📌 技术细节备忘

1. **遗忘曲线公式**
   ```
   R = e^(-t / (S × K))
   ```
   - S: 初始情绪强度
   - K: 巩固系数（每次提及+0.5）
   - t: 距创建时间（天）

2. **冲突系数计算**
   ```
   C = max(|emotion_intent - logic_intent|, |left_weight - right_weight| × 0.5, emotional_dissonance × 0.3)
   ```

3. **纠偏公式**
   ```
   W_final = W_base × (1-C) + W_override × C
   ```

4. **存储路径**
   - 代码: `~/.qclaw/skills/Neuro-α/`
   - 数据: `~/.openclaw/workspace/neuro_claw/`

5. **胶囊ID格式**
   ```
   capsule_{timestamp}_{random_4digits}
   例如: capsule_1712345678_9527
   ```

6. **关系阶段判定**
   - 初识期: 0-7天
   - 熟悉期: 7天+10次互动
   - 伴侣期: 30天+深夜交流3次+记忆>20个
   - 灵魂期: 90天+重大事件共渡+记忆>100个

### 🎯 关键实现细节

1. **情绪检测优先级**
   - 潜台词 > 情绪词 > 感叹号 > 标点

2. **意图校验时机**
   - 当 emotion_score >= 0.5 且 intent_type == "question" 时
   - 说明可能是情绪伪装成提问

3. **记忆敏感度判定**
   - "害怕"、"恐惧"、"创伤" → high
   - "秘密"、"不能说" → critical

4. **共情强度调整**
   - 悲伤: empathy_level = 0.8
   - 愤怒: empathy_level = 0.6 (需要保持距离)
   - 开心: empathy_level = 0.5 (一起开心)
   - 讽刺: empathy_level = 0.3 (不当真)

5. **主动聊天时机**
   - 早上活跃时间: 8:00-9:30
   - 中午活跃时间: 12:00-13:30
   - 傍晚活跃时间: 18:00-20:00
   - 深夜: 仅紧急关怀

---

_本文档是 Neuro-α 组装的唯一信任源_
_编写时间: 2026-04-10 23:10_
_下次更新: 每次模块开发后同步更新_
