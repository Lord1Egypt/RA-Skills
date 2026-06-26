# Enhanced Thinking Module
import os
from typing import List, Dict, Optional
from pathlib import Path
from .storage.lazy_manager import LazyStorageManager
from .core.engine import ActivationSpreadingEngine
from .core.synapse_manager import SynapseManager
from .core.neuron_builder import NeuronBuilder
from .core.intent import IntentUnderstandingLayer, SemanticSimilarityEngine


def get_default_base_path():
    """Get default base path for neural memory storage.
    获取神经记忆存储的默认路径。
    """
    # Check environment variable first
    if "NEURAL_MEMORY_PATH" in os.environ:
        return os.environ["NEURAL_MEMORY_PATH"]
    
    # Check OpenClaw state directory
    if "OPENCLAW_STATE_DIR" in os.environ:
        return os.path.join(os.environ["OPENCLAW_STATE_DIR"], "neural-memory")
    
    # Default to user home
    return os.path.join(Path.home(), ".openclaw", "neural-memory")


class EnhancedThinkingModule:
    def __init__(self, base_path: str = None, config: Dict = None):
        """Initialize enhanced thinking module.
        初始化增强版思考模块。
        
        Args:
            base_path: Storage path, auto-detected if None
                      存储路径，为空时自动检测
            config: Optional configuration dictionary
                   可选的配置字典
        """
        print("[ThinkingModule] Initializing enhanced mode / 初始化增强模式...")
        
        # Auto-detect base path if not provided
        if base_path is None:
            base_path = get_default_base_path()
        
        print(f"[ThinkingModule] Storage path / 存储路径: {base_path}")
        
        # Load config
        if config is None:
            try:
                from . import get_config
                full_config = get_config()
                config = full_config.get('thinking', {})
            except:
                config = {}
        
        self.config = config
        self.base_path = base_path
        
        # Initialize components
        self.storage = LazyStorageManager(base_path, self.config.get('storage', {}))
        self.semantic_engine = SemanticSimilarityEngine(self.config.get('semantic', {}))
        
        # Pass full intent config (including API key)
        intent_config = self.config.get('intent', {})
        self.intent_layer = IntentUnderstandingLayer(
            storage_manager=self.storage,
            semantic_engine=self.semantic_engine,
            config=intent_config
        )
        
        self.engine = ActivationSpreadingEngine(self.storage)
        self.synapse_manager = SynapseManager(self.storage)
        self.neuron_builder = NeuronBuilder(self.storage)
        
        self.is_initialized = False
        self.thinking_stats = {
            'total_thinking_sessions': 0,
            'total_connections_created': 0,
            'total_activations': 0,
            'queries_with_intent_analysis': 0
        }
        
        print(f"[OK] Enhanced mode initialized / 增强模式初始化完成")
    
    def initialize_from_existing_memory(self):
        """Initialize from existing memory files.
        从现有记忆文件初始化。
        """
        count = self.neuron_builder.build_from_memory_files()
        print(f"[OK] Created {count} neurons / 已创建 {count} 个神经元")
        self.synapse_manager.initialize_from_knowledge_connections(
            os.path.join(self.storage.base_path, "memory_long_term", "KnowledgeConnections.md")
        )
        self.is_initialized = True
    
    def think(self, query: str, mode: str = 'smart', max_depth: int = None) -> Dict:
        """Query the memory system.
        查询记忆系统。
        
        Args:
            query: User query string / 用户查询字符串
            mode: 'smart', 'exact', or 'associative' / 模式
            max_depth: Maximum spreading depth / 最大扩散深度
        """
        if not query or not query.strip():
            return {'query': query, 'error': 'empty_query', 'message': 'Query cannot be empty / 查询不能为空'}
        
        self.thinking_stats['total_thinking_sessions'] += 1
        
        if mode == 'smart':
            return self._smart_think(query)
        elif mode == 'exact':
            return self._exact_think(query, max_depth)
        else:
            return self._associative_think(query, max_depth)
    
    def _smart_think(self, query: str) -> Dict:
        """Smart thinking with intent analysis.
        智能思考，带意图分析。
        """
        analysis = self.intent_layer.analyze_query(query)
        self.thinking_stats['queries_with_intent_analysis'] += 1
        
        print(f"  Intent analysis / 意图分析结果:")
        print(f"    - Intent type / 意图类型: {analysis.intent_type}")
        print(f"    - Concepts / 提取概念: {analysis.extracted_concepts[:5]}")
        print(f"    - Related neurons / 相关神经元: {len(analysis.related_neurons)}")
        
        if not analysis.related_neurons:
            return {
                'query': query,
                'analysis': {'intent_type': analysis.intent_type, 'concepts': analysis.extracted_concepts},
                'error': 'no_related_neurons',
                'message': f"No related memories found / 未找到与查询相关的记忆"
            }
        
        all_results = []
        for related in analysis.related_neurons[:3]:
            neuron = self.storage.get_neuron(related.neuron_id)
            if neuron:
                neuron.activate()
                self.storage.update_neuron(neuron.id, lastActivated=neuron.lastActivated, activationCount=neuron.activationCount)
                spread_result = self.engine.spread(related.neuron_id, max_depth=analysis.suggested_depth)
                for r in spread_result.get('results', []):
                    all_results.append(r)
        
        # Merge and sort results
        merged = {}
        for r in all_results:
            nid = r['neuron'].id
            if nid not in merged or r['activation'] > merged[nid]['activation']:
                merged[nid] = r
        
        sorted_results = sorted(merged.values(), key=lambda x: x['activation'], reverse=True)
        self.thinking_stats['total_activations'] += len(sorted_results)
        
        print(f"  Thinking complete / 思考完成:")
        print(f"    - Activated neurons / 激活神经元数: {len(sorted_results)}")
        if sorted_results:
            print(f"    - Top associations / 最强关联:")
            for i, r in enumerate(sorted_results[:3], 1):
                print(f"      {i}. {r['neuron'].name[:20]} (activation: {r['activation']:.3f})")
        
        return {
            'query': query,
            'analysis': {
                'intent_type': analysis.intent_type,
                'concepts': analysis.extracted_concepts,
                'related_count': len(analysis.related_neurons)
            },
            'results': sorted_results[:20],
            'stats': {'total_activated': len(sorted_results), 'seeds_used': min(len(analysis.related_neurons), 3)}
        }
    
    def _exact_think(self, concept: str, max_depth: int = None) -> Dict:
        """Exact neuron lookup.
        精确神经元查找。
        """
        neurons = self.storage.get_neuron_by_name(concept)
        if not neurons:
            return {'query': concept, 'error': 'concept_not_found', 'message': f"Concept '{concept}' not found / 未找到概念 '{concept}'"}
        
        main_neuron = max(neurons, key=lambda n: n.activationCount)
        main_neuron.activate()
        self.storage.update_neuron(main_neuron.id, lastActivated=main_neuron.lastActivated, activationCount=main_neuron.activationCount)
        
        result = self.engine.spread(main_neuron.id, max_depth=max_depth or 3)
        self.thinking_stats['total_activations'] += result['stats'].get('returned', 0)
        
        return {'query': concept, 'query_name': main_neuron.name, 'results': result['results'], 'stats': result['stats']}
    
    def _associative_think(self, concept: str, max_depth: int = None) -> Dict:
        """Associative thinking mode.
        联想思考模式。
        """
        neurons = self.storage.get_neuron_by_name(concept)
        if neurons:
            main_neuron = max(neurons, key=lambda n: n.activationCount)
            main_neuron.activate()
            self.storage.update_neuron(main_neuron.id, lastActivated=main_neuron.lastActivated, activationCount=main_neuron.activationCount)
            result = self.engine.spread(main_neuron.id, max_depth=max_depth or 3)
            self.thinking_stats['total_activations'] += result['stats'].get('returned', 0)
            return {'query': concept, 'results': result['results'], 'stats': result['stats']}
        return self._smart_think(concept)
    
    def learn_and_think(self, content: str, concept_name: str, concept_type: str = 'concept', tags: List[str] = None, use_llm: bool = True):
        """Learn new knowledge and trigger thinking.
        学习新知识并触发思考。
        """
        print(f"Learning new concept / 学习新概念: '{concept_name}'")
        
        existing = self.storage.get_neuron_by_name(concept_name)
        if existing:
            print(f"  Concept exists, updating / 概念已存在，更新内容...")
            neuron = existing[0]
            self.storage.update_neuron(neuron.id, content=content)
            connections = 0
        else:
            neuron = self.neuron_builder.create_neuron_from_text(name=concept_name, content=content, neuron_type=concept_type, tags=tags or [])
            if not neuron:
                neurons = self.storage.get_neuron_by_name(concept_name)
                neuron = neurons[0] if neurons else None
            
            connections = 0
            if neuron:
                connections = self._create_smart_connections(neuron, content)
                print(f"  Created {connections} connections / 建立了 {connections} 个新连接")
        
        if neuron:
            result = self.think(concept_name, mode='associative', max_depth=2)
            return {'neuron': neuron, 'connections_created': connections, 'thinking_result': result}
        return {'error': 'failed_to_create_neuron'}
    
    def _create_smart_connections(self, new_neuron, content: str) -> int:
        """Create smart connections based on tags.
        基于标签创建智能连接。
        """
        connections = 0
        for tag in new_neuron.tags:
            related_ids = self.storage._neuron_index.search_by_tag(tag)
            for nid in related_ids[:5]:
                if nid != new_neuron.id:
                    existing = [s for s in self.storage.get_synapses_from(new_neuron.id) if s.toNeuron == nid]
                    if not existing:
                        self.synapse_manager.create_synapse(from_neuron_id=new_neuron.id, to_neuron_id=nid, synapse_type='shared_tag', weight=0.5, confidence=0.5, created_by='tag_match')
                        connections += 1
        return connections
    
    def get_relevant_memories(self, query: str, top_k: int = 5) -> List[Dict]:
        """Get relevant memories without full activation.
        获取相关记忆，无需完整激活。
        """
        analysis = self.intent_layer.analyze_query(query, use_llm=False)
        memories = []
        for related in analysis.related_neurons[:top_k]:
            neuron = self.storage.get_neuron(related.neuron_id)
            if neuron:
                memories.append({
                    'name': neuron.name, 
                    'type': neuron.type, 
                    'content': neuron.content[:500] if neuron.content else '', 
                    'relevance': related.relevance_score, 
                    'tags': neuron.tags
                })
        return memories
    
    def should_remember(self, query: str, neuron_id: str) -> bool:
        """Check if neuron should be loaded for query.
        检查是否应该为查询加载神经元。
        """
        return self.intent_layer.should_load_neuron(query, neuron_id)
    
    def get_thinking_stats(self) -> Dict:
        """Get statistics about the memory system.
        获取记忆系统统计信息。
        """
        return {
            'neurons_count': self.storage._neuron_index.size(),
            'synapses_count': sum(len(s) for s in self.storage._synapses_cache.values()),
            'protected_neurons_count': len(self.storage.get_protected_neurons()),
            'thinking_sessions': self.thinking_stats['total_thinking_sessions'],
            'total_activations': self.thinking_stats['total_activations'],
            'queries_with_intent_analysis': self.thinking_stats['queries_with_intent_analysis'],
            'hot_cache_size': self.storage._hot_cache.size(),
            'semantic_indexed': len(self.semantic_engine._neuron_embeddings)
        }
    
    def save(self):
        """Save all memory data.
        保存所有记忆数据。
        """
        self.storage.save_all()
        print("[OK] Memory data saved / 思考模块数据已保存")
    
    def run_maintenance(self):
        """Run maintenance tasks.
        运行维护任务。
        """
        print("Running maintenance / 正在执行维护任务...")
        self.synapse_manager.decay_old_synapses()
        self.synapse_manager.prune_low_confidence_synapses()
        self.save()
        print("[OK] Maintenance complete / 维护任务完成")


ThinkingModule = EnhancedThinkingModule