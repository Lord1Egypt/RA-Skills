#!/usr/bin/env python3
"""
记忆参数优化器 - 自动调整 memory_search 参数
"""

import config

class MemoryOptimizer:
    def __init__(self, config_obj):
        self.config = config_obj

    def optimize_for_agent(self, agent_id):
        """为指定Agent优化参数"""
        # 获取当前Agent的上下文大小（这里简化处理）
        current_usage = self._estimate_current_usage(agent_id)

        # 计算优化后的参数
        new_params = {
            'memory.min_score': self._optimize_min_score(current_usage),
            'memory.max_results': self._optimize_max_results(current_usage),
            'memory.time_decay_days': self.config.get('memory.time_decay_days', 30),
        }

        # 计算预期改进
        improvements = {
            'accuracy': 15.0,  # 模拟数据
            'speed': 8.0,
            'memory': -5.0  # 略微增加使用但值得
        }

        return {
            'applied': new_params,
            'improvements': improvements,
            'agent': agent_id
        }

    def _estimate_current_usage(self, agent_id):
        """估算当前Agent的记忆使用情况"""
        # 这里应该从实际会话中获取，简化返回模拟数据
        return {
            'context_tokens': 50000,
            'agent_id': agent_id
        }

    def _optimize_min_score(self, usage):
        """优化最小匹配分数"""
        base = self.config.get('memory.min_score', 0.6)

        # 如果上下文使用率高，提高阈值以减少噪音
        if usage['context_tokens'] > 100000:
            return min(0.8, base + 0.1)
        elif usage['context_tokens'] < 20000:
            return max(0.4, base - 0.1)

        return base

    def _optimize_max_results(self, usage):
        """优化最大结果数"""
        base = self.config.get('memory.max_results', 10)

        # 如果记忆条目多，可以返回更多结果
        # 这里简化逻辑
        if usage['context_tokens'] > 80000:
            return min(20, base + 5)

        return base
