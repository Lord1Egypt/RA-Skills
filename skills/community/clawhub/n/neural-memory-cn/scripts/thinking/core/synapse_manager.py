# Synapse Manager - 突触管理器
# 负责突触的创建、强化、修剪等生命周期管理
from typing import List, Dict, Optional
from ..storage.manager import StorageManager
from .models import Neuron, Synapse

class SynapseManager:
    """突触管理器 - 管理和优化突触连接"""

    def __init__(self, storage: StorageManager):
        self.storage = storage

        # 配置参数
        self.similarity_threshold = 0.65  # 语义相似度阈值
        self.cooccurrence_threshold = 2  # 共现次数阈值
        self.decay_factor = 0.98  # 衰减因子（定期衰减）
        self.decay_days_threshold = 30  # 超过这么多天未激活则衰减
        self.protected_neuron_types = storage.protected_neuron_types

        # 预定义的连接类型映射
        self.connection_rules = {
            ('中医', '系统动力学'): ('analogy', 0.8, 0.9),
            ('中医', '民航安全'): ('analogy', 0.75, 0.85),
            ('社交语言', '中医'): ('similarity', 0.7, 0.8),
            ('民航', '历史政治'): ('causality', 0.7, 0.75),
            ('金融', '历史政治'): ('causality', 0.8, 0.85),
            # 可以从 KnowledgeConnections 导入
        }

    def create_synapse(self, from_neuron_id: str, to_neuron_id: str,
                       synapse_type: str = 'similarity', weight: float = 0.5,
                       confidence: float = 0.7, created_by: str = 'auto',
                       metadata: Dict = None) -> Optional[Synapse]:
        """创建突触（自动检查是否已存在）"""
        # 检查是否已存在
        existing = self.get_synapse_between(from_neuron_id, to_neuron_id)
        if existing:
            return existing

        from_neuron = self.storage.get_neuron(from_neuron_id)
        to_neuron = self.storage.get_neuron(to_neuron_id)

        if not from_neuron or not to_neuron:
            return None

        # 检查保护
        if from_neuron.type in self.protected_neuron_types or \
           to_neuron.type in self.protected_neuron_types:
            print(f"警告: 尝试创建涉及受保护神经元的突触，需要谨慎评估")
            # 这里可以添加更严格的检查逻辑

        synapse = Synapse.create(
            from_neuron=from_neuron_id,
            to_neuron=to_neuron_id,
            synapse_type=synapse_type,
            weight=weight,
            confidence=confidence,
            created_by=created_by,
            metadata=metadata or {}
        )

        self.storage.add_synapse(synapse)
        return synapse

    def get_synapse_between(self, from_id: str, to_id: str) -> Optional[Synapse]:
        """获取两个神经元之间的突触"""
        synapses = self.storage.get_synapses_from(from_id)
        for s in synapses:
            if s.toNeuron == to_id:
                return s
        return None

    def create_from_connection_rule(self, from_name: str, to_name: str,
                                    from_type: str = 'concept', to_type: str = 'concept'):
        """从预定义规则创建连接"""
        key = (from_name, to_name)
        if key in self.connection_rules:
            synapse_type, weight, confidence = self.connection_rules[key]

            from_neuron = self.storage.get_neuron_by_name_and_type(from_name, from_type)
            to_neuron = self.storage.get_neuron_by_name_and_type(to_name, to_type)

            if from_neuron and to_neuron:
                return self.create_synapse(
                    from_neuron.id, to_neuron.id,
                    synapse_type=synapse_type,
                    weight=weight,
                    confidence=confidence,
                    created_by='rule'
                )
        return None

    def create_cooccurrence_synapses(self, cooccurrence_data: Dict[str, List[str]]):
        """
        基于共现数据创建突触
        cooccurrence_data: {session_id: [neuron_name1, neuron_name2, ...]}
        """
        # 统计共现频率
        cooccurrence_count: Dict[Tuple[str, str], int] = {}

        for session_concepts in cooccurrence_data.values():
            concepts = list(set(session_concepts))  # 去重
            for i in range(len(concepts)):
                for j in range(i+1, len(concepts)):
                    key = (concepts[i], concepts[j])
                    cooccurrence_count[key] = cooccurrence_count.get(key, 0) + 1
                    # 也记录反向（双向连接）
                    key_rev = (concepts[j], concepts[i])
                    cooccurrence_count[key_rev] = cooccurrence_count.get(key_rev, 0) + 1

        # 创建突触
        for (from_name, to_name), count in cooccurrence_count.items():
            if count >= self.cooccurrence_threshold:
                from_neuron = self.storage.get_neuron_by_name(from_name)
                to_neuron = self.storage.get_neuron_by_name(to_name)

                if from_neuron and to_neuron:
                    weight = min(0.5 + count * 0.1, 0.9)  # 基于共现次数计算权重
                    self.create_synapse(
                        from_neuron.id, to_neuron.id,
                        synapse_type='similarity',
                        weight=weight,
                        confidence=min(0.5 + count * 0.1, 0.9),
                        created_by='cooccurrence',
                        metadata={'cooccurrence_count': count}
                    )

    def decay_old_synapses(self):
        """衰减长时间未激活的突触（但保护受保护神经元的突触）"""
        import time
        from datetime import datetime, timedelta

        threshold_date = datetime.now() - timedelta(days=self.decay_days_threshold)
        threshold_timestamp = threshold_date.isoformat()

        synapses_to_decay = []

        # 收集需要衰减的突触（排除受保护神经元的突触）
        for synapses in self.storage._synapses_cache.values():
            for synapse in synapses:
                from_neuron = self.storage.get_neuron(synapse.fromNeuron)
                to_neuron = self.storage.get_neuron(synapse.toNeuron)

                # 检查是否为受保护神经元的突触
                is_protected = False
                if from_neuron and from_neuron.type in self.protected_neuron_types:
                    is_protected = True
                if to_neuron and to_neuron.type in self.protected_neuron_types:
                    is_protected = True

                if is_protected:
                    continue  # 跳过受保护的突触

                # 检查最后强化时间
                last_reinforced = synapse.lastReinforced
                if not last_reinforced or last_reinforced < threshold_timestamp:
                    synapses_to_decay.append(synapse)

        # 执行衰减
        for synapse in synapses_to_decay:
            synapse.decay(self.decay_factor)
            # 如果权重太低，考虑删除
            if synapse.weight < 0.1:
                self.storage.delete_synapse(synapse.id)
            else:
                self.storage.add_synapse(synapse)

        print(f"衰减了 {len(synapses_to_decay)} 个旧突触")

    def strengthen_synapses_from_activation(self, neuron_id: str, activated_neurons: List[str]):
        """根据激活结果强化相关突触"""
        synapses = self.storage.get_synapses_from(neuron_id)
        for synapse in synapses:
            if synapse.toNeuron in activated_neurons:
                synapse.reinforce(delta=0.05)
                self.storage.add_synapse(synapse)

    def prune_low_confidence_synapses(self, confidence_threshold: float = 0.3):
        """修剪低置信度的突触（保护受保护神经元）"""
        pruned_count = 0
        for from_id, synapses in list(self.storage._synapses_cache.items()):
            from_neuron = self.storage.get_neuron(from_id)
            if from_neuron and from_neuron.type in self.protected_neuron_types:
                continue

            for synapse in synapses[:]:
                to_neuron = self.storage.get_neuron(synapse.toNeuron)
                if to_neuron and to_neuron.type in self.protected_neuron_types:
                    continue

                if synapse.confidence < confidence_threshold:
                    self.storage.delete_synapse(synapse.id)
                    pruned_count += 1

        print(f"修剪了 {pruned_count} 个低置信度突触")

    def initialize_from_knowledge_connections(self, connections_file: str):
        """
        从 KnowledgeConnections.md 初始化突触连接
        这是一个一次性操作，用于建立初始的跨领域连接
        """
        import re

        with open(connections_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 解析连接条目
        # 格式: **A + B**: description (weight 可选)
        pattern = r'\*\*([^*\n]+) \+ ([^*\n]+)\*\*:.*?(?:\(weight[:\s]*([\d.]+)\))?'

        matches = re.findall(pattern, content, re.DOTALL)

        created_count = 0
        for match in matches:
            from_name, to_name, weight_str = match
            from_name = from_name.strip()
            to_name = to_name.strip()
            weight = float(weight_str) if weight_str else 0.7

            # 检查是否有预定义规则
            synapse_type = 'analogy'  # 默认类型
            confidence = 0.7

            key = (from_name, to_name)
            if key in self.connection_rules:
                synapse_type, weight, confidence = self.connection_rules[key]

            # 尝试创建正向连接
            from_neurons = self.storage.get_neuron_by_name(from_name)
            to_neurons = self.storage.get_neuron_by_name(to_name)

            # 取第一个匹配的神经元
            from_neuron = from_neurons[0] if from_neurons else None
            to_neuron = to_neurons[0] if to_neurons else None

            if from_neuron and to_neuron:
                # 检查是否已存在
                existing = self.get_synapse_between(from_neuron.id, to_neuron.id)
                if existing:
                    continue

                synapse = self.create_synapse(
                    from_neuron.id, to_neuron.id,
                    synapse_type=synapse_type,
                    weight=weight,
                    confidence=confidence,
                    created_by='knowledge_connections',
                    metadata={'source': 'KnowledgeConnections.md'}
                )
                if synapse:
                    created_count += 1

            # 也尝试反向连接（双向）
            if from_name != to_name:
                from_neurons_rev = self.storage.get_neuron_by_name(to_name)
                to_neurons_rev = self.storage.get_neuron_by_name(from_name)
                from_neuron_rev = from_neurons_rev[0] if from_neurons_rev else None
                to_neuron_rev = to_neurons_rev[0] if to_neurons_rev else None

                if from_neuron_rev and to_neuron_rev:
                    # 检查是否已经存在反向连接
                    existing_rev = self.get_synapse_between(from_neuron_rev.id, to_neuron_rev.id)
                    if not existing_rev:
                        synapse_rev = self.create_synapse(
                            from_neuron_rev.id, to_neuron_rev.id,
                            synapse_type=synapse_type,
                            weight=weight,
                            confidence=confidence * 0.9,  # 反向连接置信度稍低
                            created_by='knowledge_connections',
                            metadata={'source': 'KnowledgeConnections.md', 'direction': 'reverse'}
                        )
                        if synapse_rev:
                            created_count += 1

        print(f"从 KnowledgeConnections 初始化了 {created_count} 个连接")
        return created_count

    def _infer_synapse_type(self, from_type: str, to_type: str, from_name: str, to_name: str) -> str:
        """根据类型和名称推断突触类型"""
        if from_type == to_type:
            return 'similarity'
        # 可以根据更多规则推断
        return 'analogy'
