# Thinking Adapter - 思考模块适配器
# 将思考模块集成到 OpenClaw 的现有接口

import os
import json
from typing import List, Dict, Any, Optional
from . import ThinkingModule

class ThinkingAdapter:
    """思考模块适配器 - 提供与 OpenClaw 现有接口的兼容性"""

    def __init__(self, thinking_module: ThinkingModule):
        self.thinking = thinking_module
        self.config = self._load_config()

    def _load_config(self):
        """加载配置 / Load configuration"""
        from pathlib import Path
        
        # Auto-detect config path
        if "NEURAL_MEMORY_PATH" in os.environ:
            config_dir = os.environ["NEURAL_MEMORY_PATH"]
        elif "OPENCLAW_STATE_DIR" in os.environ:
            config_dir = os.path.join(os.environ["OPENCLAW_STATE_DIR"], "neural-memory")
        else:
            config_dir = os.path.join(Path.home(), ".openclaw", "neural-memory")
        
        config_path = os.path.join(config_dir, "config.yaml")
        if os.path.exists(config_path):
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {
            'integration': {
                'memory_search_enhancement': True,
                'create_thinking_endpoint': True
            }
        }

    def enhanced_memory_search(self, query: str, max_results: int = 5, **kwargs) -> List[Dict]:
        """
        增强版 memory_search - 结合语义搜索和激活扩散

        Args:
            query: 搜索查询
            max_results: 最大结果数
            **kwargs: 其他参数（传递给记忆搜索）

        Returns:
            增强的搜索结果列表
        """
        results = []

        # 1. 首先调用现有的记忆搜索
        try:
            from openclaw.memory import memory_search as original_search
            original_results = original_search(query=query, maxResults=max_results, **kwargs)

            for r in original_results:
                results.append({
                    'path': r.get('path'),
                    'lines': r.get('lines'),
                    'score': r.get('score'),
                    'source': 'semantic_search'
                })
        except Exception as e:
            print(f"警告: 原记忆搜索不可用: {e}")

        # 2. 使用思考模块进行联想
        thinking_result = self.thinking.think(query, mode='associative', max_depth=2)

        # 将激活的神经元转换为记忆引用格式
        if 'results' in thinking_result:
            for r in thinking_result['results']:
                neuron = r['neuron']
                # 构建虚假的记忆引用路径（指向对应的长期记忆文件）
                source_file = self._get_source_file_for_neuron(neuron)

                results.append({
                    'path': source_file,
                    'lines': neuron.content[:200] + "...",
                    'score': r['activation'],  # 使用激活值作为分数
                    'source': 'thinking_module',
                    'neuron_id': neuron.id,
                    'activation_value': r['activation']
                })

        # 3. 去重并排序
        seen = set()
        unique_results = []
        for r in results:
            key = r.get('neuron_id') or r.get('path')
            if key and key not in seen:
                seen.add(key)
                unique_results.append(r)

        # 按分数排序
        unique_results.sort(key=lambda x: x['score'], reverse=True)

        return unique_results[:max_results]

    def _get_source_file_for_neuron(self, neuron) -> str:
        """根据神经元元数据确定对应的源文件"""
        metadata = neuron.metadata or {}
        source = metadata.get('source')

        if source == 'USER.md':
            return 'memory_long_term/UserProfile.md'
        elif source == 'Preferences.md':
            return 'memory_long_term/Preferences.md'
        elif source == 'LearningProjects.md':
            return 'memory_long_term/LearningProjects.md'
        elif source == 'KeyInsights.md':
            return 'memory_long_term/KeyInsights.md'
        elif source == 'KnowledgeConnections.md':
            return 'memory_long_term/KnowledgeConnections.md'
        else:
            return 'memory_long_term/neurons.json'

    def thinking_query(self, concept: str, mode: str = 'associative',
                       max_depth: int = 3, limit: int = 10, **kwargs) -> Dict:
        """
        独立的思考查询接口

        Args:
            concept: 查询概念
            mode: 思考模式 ('associative', 'focused', 'exploratory')
            max_depth: 最大传播深度
            limit: 返回结果数量

        Returns:
            完整的思考结果（包含神经元、激活值、路径等）
        """
        return self.thinking.think(
            concept=concept,
            mode=mode,
            max_depth=max_depth
        )

    def learn_and_think(self, content: str, concept_name: str, concept_type: str = 'concept',
                        tags: List[str] = None) -> Dict:
        """学习新内容并自动思考"""
        return self.thinking.learn_and_think(
            content=content,
            concept_name=concept_name,
            concept_type=concept_type,
            tags=tags
        )

    def get_stats(self) -> Dict:
        """获取思考模块统计"""
        return self.thinking.get_thinking_stats()

    def save(self):
        """保存思考模块状态"""
        self.thinking.save()

    def run_maintenance(self):
        """运行维护任务"""
        self.thinking.run_maintenance()

# 全局适配器实例
_adapter_instance = None

def get_thinking_adapter() -> ThinkingAdapter:
    """获取思考模块适配器实例（单例）"""
    global _adapter_instance
    if _adapter_instance is None:
        thinking_module = ThinkingModule()
        thinking_module.initialize_from_existing_memory()
        _adapter_instance = ThinkingAdapter(thinking_module)
    return _adapter_instance
