# Intent Understanding Layer
# 意图理解层 - 核心思考判断逻辑模块
# 判断用户查询与哪些记忆相关，实现按需加载

import re
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from .semantic_engine import SemanticSimilarityEngine
from .related_neuron import RelatedNeuron

# 尝试导入 LLM 客户端
try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class QueryAnalysis:
    """查询分析结果"""
    original_query: str
    extracted_concepts: List[str]  # 提取的关键概念
    intent_type: str  # question|statement|request|unknown
    related_neurons: List[RelatedNeuron]  # 相关神经元
    suggested_depth: int  # 建议的联想深度


class IntentUnderstandingLayer:
    """
    意图理解层 - 思考判断逻辑模块
    
    核心功能：
    1. 分析用户查询，提取关键概念
    2. 判断查询与哪些神经元记忆相关
    3. 返回相关性排序的神经元列表（用于按需加载）
    """
    
    # 意图关键词模式
    INTENT_PATTERNS = {
        'question': [r'(.*)\?', r'怎么', r'如何', r'为什么', r'什么是', r'有哪些', r'能不能', r'可以', r'吗', r'how', r'what', r'why', r'when', r'where', r'who'],
        'request': [r'帮我', r'请', r'帮我', r'给我', r'查一下', r'找一下', r'please', r'help', r'show', r'find'],
        'statement': [r'我想', r'我认为', r'我觉得', r'感觉', r'i think', r'i feel', r'believe'],
    }
    
    # 领域关键词映射
    DOMAIN_KEYWORDS = {
        '为人处世': ['沟通', '社交', '人际', '说话', '表达', '关系', '边界', '冲突', '职场', '礼仪'],
        '中医药理': ['中医', '中药', '经络', '穴位', '阴阳', '五行', '气血', '脏腑', '脉诊', '舌诊'],
        '民航科研': ['民航', '航空', '飞行', '机场', 'ATM', '安全', '事故', 'CRM', 'SMS', '仿真'],
        '时政金融': ['政治', '经济', '金融', '改革', '政策', '监管', '毛泽东', '历史', '国际'],
        '系统思维': ['系统', '模型', '仿真', 'AnyLogic', 'ABM', 'DES', '动力学'],
        'OpenClaw': ['OpenClaw', '记忆', '神经', '突触', '技能', '配置'],
    }
    
    def __init__(self, storage_manager, semantic_engine: SemanticSimilarityEngine = None, config: Dict = None):
        self.storage = storage_manager
        self.semantic_engine = semantic_engine
        self.config = config or {}
        
        # LLM 配置
        self.use_llm = self.config.get('use_llm', True)
        self.llm_api_key = self.config.get('llm_api_key') or self._get_openrouter_key()
        self.llm_base_url = self.config.get('llm_base_url', 'https://openrouter.ai/api/v1')
        self.llm_model = self.config.get('llm_model', 'openai/gpt-3.5-turbo')
        
        # 相关性阈值
        self.relevance_threshold = self.config.get('relevance_threshold', 0.4)
        self.max_related_neurons = self.config.get('max_related_neurons', 10)
        
        print(f"[IntentLayer] 初始化完成")
        print(f"  - 语义引擎: {'已启用' if semantic_engine else '未启用'}")
        print(f"  - LLM 分析: {'已启用' if self.use_llm and self.llm_api_key else '未启用'}")
    
    def _get_openrouter_key(self) -> Optional[str]:
        """获取 OpenRouter API Key"""
        import os
        return os.environ.get('OPENROUTER_API_KEY')
    
    def analyze_query(self, user_query: str, use_llm: bool = None) -> QueryAnalysis:
        """
        分析用户查询 - 核心方法
        
        Args:
            user_query: 用户查询文本
            use_llm: 是否使用 LLM 分析（可选覆盖默认设置）
        
        Returns:
            QueryAnalysis: 包含提取的概念、相关神经元等
        """
        if use_llm is None:
            use_llm = self.use_llm and bool(self.llm_api_key)
        
        # Step 1: 基础分析（提取概念、判断意图）
        extracted_concepts = self._extract_concepts_basic(user_query)
        intent_type = self._detect_intent_type(user_query)
        
        # Step 2: 找到相关神经元
        related_neurons = self._find_related_neurons(user_query, extracted_concepts)
        
        # Step 3: 如果启用了 LLM，进行深度分析
        if use_llm and len(related_neurons) < 3:
            llm_concepts = self._extract_concepts_with_llm(user_query)
            if llm_concepts:
                extracted_concepts = list(set(extracted_concepts + llm_concepts))
                # 重新查找相关神经元
                additional_neurons = self._find_related_neurons(user_query, llm_concepts)
                related_neurons = self._merge_related_neurons(related_neurons, additional_neurons)
        
        # Step 4: 确定建议的联想深度
        suggested_depth = self._suggest_depth(intent_type, len(related_neurons))
        
        return QueryAnalysis(
            original_query=user_query,
            extracted_concepts=extracted_concepts,
            intent_type=intent_type,
            related_neurons=related_neurons[:self.max_related_neurons],
            suggested_depth=suggested_depth
        )
    
    def _extract_concepts_basic(self, query: str) -> List[str]:
        """基础概念提取 - 基于关键词匹配"""
        concepts = []
        query_lower = query.lower()
        
        # 检查领域关键词
        for domain, keywords in self.DOMAIN_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in query_lower:
                    concepts.append(domain)
                    concepts.append(kw)
        
        # 提取引号中的内容
        quoted = re.findall(r'[""「」『』]([^""「」『』]+)[""「」『』]', query)
        concepts.extend(quoted)
        
        # 提取中文关键词（2-4字的词）
        chinese_words = re.findall(r'[\u4e00-\u9fa5]{2,4}', query)
        concepts.extend(chinese_words)
        
        # 去重并保留顺序
        seen = set()
        unique_concepts = []
        for c in concepts:
            if c not in seen and len(c) > 1:
                seen.add(c)
                unique_concepts.append(c)
        
        return unique_concepts
    
    def _detect_intent_type(self, query: str) -> str:
        """检测意图类型"""
        query_lower = query.lower()
        
        for intent_type, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent_type
        
        return 'unknown'
    
    def _find_related_neurons(self, query: str, concepts: List[str]) -> List[RelatedNeuron]:
        """找到与查询相关的神经元"""
        related = []
        all_neurons = self.storage.get_all_neurons()
        
        # 创建神经元名称和标签的索引
        neuron_scores: Dict[str, float] = {}
        
        for neuron in all_neurons:
            score = 0.0
            
            # 1. 名称匹配
            name_lower = neuron.name.lower()
            query_lower = query.lower()
            
            if name_lower == query_lower:
                score += 1.0
            elif name_lower in query_lower or query_lower in name_lower:
                score += 0.8
            else:
                # 检查名称中的词是否出现在查询中
                name_words = set(name_lower.split())
                query_words = set(query_lower.split())
                overlap = len(name_words & query_words)
                if overlap > 0:
                    score += 0.3 * overlap / max(len(name_words), 1)
            
            # 2. 概念匹配
            for concept in concepts:
                concept_lower = concept.lower()
                if concept_lower in name_lower:
                    score += 0.5
                # 检查标签
                for tag in neuron.tags:
                    if concept_lower in tag.lower():
                        score += 0.3
            
            # 3. 标签匹配
            query_words = set(query_lower.split())
            for tag in neuron.tags:
                tag_lower = tag.lower()
                if tag_lower in query_lower:
                    score += 0.4
                # 分词后匹配
                tag_words = set(tag_lower.replace('_', ' ').split())
                overlap = len(query_words & tag_words)
                if overlap > 0:
                    score += 0.2 * overlap
            
            # 4. 使用语义引擎（如果可用）
            if self.semantic_engine and score < 0.5:
                try:
                    text_sim = self.semantic_engine.compute_text_similarity(query, neuron.name)
                    if text_sim > 0.5:
                        score = max(score, text_sim * 0.7)
                except:
                    pass
            
            # 5. 激活次数加成（热门神经元稍微优先）
            if neuron.activationCount > 0:
                score += min(0.1, neuron.activationCount * 0.01)
            
            if score > 0:
                neuron_scores[neuron.id] = score
        
        # 排序并创建 RelatedNeuron
        sorted_scores = sorted(neuron_scores.items(), key=lambda x: x[1], reverse=True)
        
        for neuron_id, score in sorted_scores[:self.max_related_neurons]:
            if score >= self.relevance_threshold:
                neuron = self.storage.get_neuron(neuron_id)
                if neuron:
                    related.append(RelatedNeuron(
                        neuron_id=neuron_id,
                        relevance_score=min(score, 1.0),
                        matched_concept=neuron.name,
                        match_type='hybrid',
                        confidence=0.7 if score > 0.5 else 0.5
                    ))
        
        return related
    
    def _extract_concepts_with_llm(self, query: str) -> List[str]:
        """使用 LLM 提取概念"""
        if not HAS_OPENAI or not self.llm_api_key:
            return []
        
        try:
            client = openai.OpenAI(
                api_key=self.llm_api_key,
                base_url=self.llm_base_url
            )
            
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "user", "content": f"""提取以下查询的关键概念，直接返回JSON数组。
查询: {query}
返回示例: ["概念1", "概念2"]"""}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            message = response.choices[0].message
            content = message.content
            
            # 某些模型（如 stepfun）把内容放在 reasoning 字段
            if not content and hasattr(message, 'reasoning') and message.reasoning:
                content = message.reasoning
            
            # 检查内容是否为空
            if not content or not content.strip():
                print("[IntentLayer] LLM 返回空内容")
                return []
            
            # 清理可能的 markdown 代码块标记
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # 尝试解析 JSON
            try:
                concepts = json.loads(content)
            except json.JSONDecodeError:
                # 尝试提取 JSON 数组
                import re
                match = re.search(r'\[.*?\]', content, re.DOTALL)
                if match:
                    concepts = json.loads(match.group())
                else:
                    print(f"[IntentLayer] 无法解析 JSON: {content[:100]}")
                    return []
            
            if isinstance(concepts, list):
                return [str(c) for c in concepts]
        
        except Exception as e:
            print(f"[IntentLayer] LLM 概念提取失败: {e}")
        
        return []
    
    def _merge_related_neurons(self, existing: List[RelatedNeuron], 
                               new: List[RelatedNeuron]) -> List[RelatedNeuron]:
        """合并相关神经元列表"""
        existing_ids = {r.neuron_id for r in existing}
        
        for r in new:
            if r.neuron_id not in existing_ids:
                existing.append(r)
                existing_ids.add(r.neuron_id)
        
        # 重新排序
        existing.sort(key=lambda x: x.relevance_score, reverse=True)
        return existing
    
    def _suggest_depth(self, intent_type: str, related_count: int) -> int:
        """建议联想深度"""
        if intent_type == 'question':
            return 3  # 问题需要更深的联想
        elif intent_type == 'request':
            return 2
        elif intent_type == 'statement':
            return 1
        else:
            return 2
    
    def get_relevant_neuron_ids(self, query: str, top_k: int = 5) -> List[str]:
        """
        快速获取相关神经元 ID 列表 - 用于按需加载
        """
        analysis = self.analyze_query(query, use_llm=False)  # 快速模式不使用 LLM
        return [r.neuron_id for r in analysis.related_neurons[:top_k]]
    
    def should_load_neuron(self, query: str, neuron_id: str) -> bool:
        """
        判断是否应该加载某个神经元 - 用于精细的按需加载决策
        """
        neuron = self.storage.get_neuron(neuron_id)
        if not neuron:
            return False
        
        analysis = self.analyze_query(query, use_llm=False)
        
        # 直接匹配
        for r in analysis.related_neurons:
            if r.neuron_id == neuron_id:
                return True
        
        # 检查是否与已选神经元有强连接
        for r in analysis.related_neurons:
            synapses = self.storage.get_synapses_from(r.neuron_id)
            for s in synapses:
                if s.toNeuron == neuron_id and s.weight > 0.7:
                    return True
        
        return False



