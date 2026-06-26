# Activation Spreading Engine - 激活扩散引擎
# 实现改进的 Spreading Activation 算法
from typing import List, Dict, Tuple, Optional
from ..storage.manager import StorageManager
from .models import Neuron, Synapse, ActivationRecord

class ActivationSpreadingEngine:
    """激活扩散引擎 - 模拟神经元激活传播"""

    def __init__(self, storage: StorageManager):
        self.storage = storage
        self.default_decay_factor = 0.8
        self.default_max_depth = 3
        self.default_min_activation = 0.15
        self.default_result_limit = 20

    def spread(self, query_neuron_id: str, max_depth: int = None,
               decay_factor: float = None, min_activation: float = None,
               limit: int = None, synapse_types: List[str] = None) -> Dict:
        """
        执行激活扩散
        """
        max_depth = max_depth or self.default_max_depth
        decay_factor = decay_factor or self.default_decay_factor
        min_activation = min_activation or self.default_min_activation
        limit = limit or self.default_result_limit

        query_neuron = self.storage.get_neuron(query_neuron_id)
        if not query_neuron:
            return {'query': query_neuron_id, 'results': [], 'stats': {'error': 'neuron_not_found'}}

        query_neuron.activate()
        self.storage.update_neuron(query_neuron_id, lastActivated=query_neuron.lastActivated,
                                   activationCount=query_neuron.activationCount)

        activations = {query_neuron_id: 1.0}
        paths = {query_neuron_id: []}

        frontier = [query_neuron_id]
        for depth in range(max_depth):
            next_frontier = []
            for current_id in frontier:
                current_activation = activations[current_id]
                synapses = self.storage.get_synapses_from(current_id)

                for synapse in synapses:
                    if synapse_types and synapse.type not in synapse_types:
                        continue

                    transmitted = current_activation * synapse.weight * (decay_factor ** depth)
                    target_id = synapse.toNeuron
                    activations[target_id] = activations.get(target_id, 0) + transmitted

                    if target_id not in paths:
                        paths[target_id] = []
                    paths[target_id].append({
                        'from': current_id,
                        'to': target_id,
                        'synapse_id': synapse.id,
                        'synapse_type': synapse.type,
                        'weight': synapse.weight,
                        'transmitted_activation': transmitted,
                        'depth': depth
                    })

                    if target_id not in next_frontier:
                        next_frontier.append(target_id)

                    if transmitted > 0.05:
                        synapse.reinforce(delta=0.02)

            frontier = next_frontier
            if not frontier:
                break

        results = []
        for neuron_id, activation in activations.items():
            if neuron_id != query_neuron_id and activation >= min_activation:
                neuron = self.storage.get_neuron(neuron_id)
                if neuron:
                    results.append({
                        'neuron': neuron,
                        'activation': activation,
                        'path': paths.get(neuron_id, [])
                    })

        results.sort(key=lambda x: x['activation'], reverse=True)
        results = results[:limit]

        # 使用已导入的 ActivationRecord
        try:
            record = ActivationRecord.create(
                query_neuron_id=query_neuron_id,
                activated_neurons={r['neuron'].id: r['activation'] for r in results},
                path=[p for r in results for p in r['path']],
                parameters={
                    'max_depth': max_depth,
                    'decay_factor': decay_factor,
                    'min_activation': min_activation,
                    'synapse_types': synapse_types
                }
            )
            self.storage.log_activation(record)
        except Exception as e:
            pass  # 忽略日志错误

        return {
            'query': query_neuron_id,
            'query_name': query_neuron.name,
            'results': results,
            'stats': {
                'total_activated': len(activations) - 1,
                'returned': len(results),
                'max_depth_reached': max_depth,
                'total_synapses_traversed': sum(len(r.get('path', [])) for r in results)
            }
        }

    def find_related(self, concept_name: str, top_k: int = 10) -> List[Dict]:
        """根据概念名称查找相关知识"""
        neurons = self.storage.get_neuron_by_name(concept_name)
        if not neurons:
            return []

        all_results = {}
        for neuron in neurons:
            result = self.spread(neuron.id, limit=top_k)
            for r in result['results']:
                nid = r['neuron'].id
                if nid not in all_results or r['activation'] > all_results[nid]['activation']:
                    all_results[nid] = r

        sorted_results = sorted(all_results.values(), key=lambda x: x['activation'], reverse=True)[:top_k]
        return sorted_results

    def get_strongest_connections(self, neuron_id: str, top_k: int = 5) -> List[Dict]:
        """获取与指定神经元最强连接的神经元"""
        synapses = self.storage.get_synapses_from(neuron_id)
        synapses.sort(key=lambda s: s.weight, reverse=True)

        results = []
        for synapse in synapses[:top_k]:
            target = self.storage.get_neuron(synapse.toNeuron)
            if target:
                results.append({
                    'neuron': target,
                    'synapse_type': synapse.type,
                    'weight': synapse.weight,
                    'confidence': synapse.confidence,
                    'reinforcement_count': synapse.reinforcementCount
                })

        return results
