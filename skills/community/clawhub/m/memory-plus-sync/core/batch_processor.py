"""
批量处理模块

支持批量存储、批量验证记忆
"""

import asyncio
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.triple_agent_processor import TripleAgentProcessor
from core.vote_aggregator import VoteAggregator
from core.mem0_integration import Mem0Integration
from core.memory_dedup import MemoryDeduplicator, DedupResult


@dataclass
class BatchResult:
    """批量处理结果"""
    total: int
    successful: int
    failed: int
    skipped: int
    results: List[Dict]
    total_latency: float
    avg_latency: float


class BatchProcessor:
    """批量处理器"""

    def __init__(self, use_local: bool = True, enable_dedup: bool = True):
        """
        初始化批量处理器

        Args:
            use_local: 是否使用本地模型
            enable_dedup: 是否启用去重
        """
        self.use_local = use_local
        self.enable_dedup = enable_dedup

        self.processor = TripleAgentProcessor(use_local=use_local)
        self.aggregator = VoteAggregator()
        self.mem0 = Mem0Integration()
        self.deduplicator = MemoryDeduplicator() if enable_dedup else None

        self.max_workers = 4  # 最大并发数

    def process_batch(
        self,
        memories: List[Dict],
        user_id: str = "default",
        skip_duplicates: bool = True
    ) -> BatchResult:
        """
        批量处理记忆

        Args:
            memories: 记忆列表，每个元素包含 {'content': str, 'metadata': dict}
            user_id: 用户 ID
            skip_duplicates: 是否跳过重复记忆

        Returns:
            BatchResult: 批量处理结果
        """
        start_time = time.time()
        results = []

        successful = 0
        failed = 0
        skipped = 0

        # 去重检查
        if self.enable_dedup and skip_duplicates:
            print(f"🔍 执行去重检查 ({len(memories)} 条记忆)...")
            dedup_results = self.deduplicator.batch_check_duplicates(
                [m['content'] for m in memories],
                user_id
            )

            # 过滤重复记忆
            filtered_memories = []
            for i, (memory, dedup_result) in enumerate(zip(memories, dedup_results)):
                if dedup_result.recommendation == "SKIP":
                    skipped += 1
                    results.append({
                        'index': i,
                        'content': memory['content'][:100],
                        'status': 'SKIPPED',
                        'reason': f'重复记忆 (相似度：{dedup_result.similarity_score:.2f})'
                    })
                else:
                    filtered_memories.append((i, memory, dedup_result))
        else:
            filtered_memories = [(i, m, None) for i, m in enumerate(memories)]

        print(f"📝 处理 {len(filtered_memories)} 条记忆...")

        # 批量处理
        for idx, (original_index, memory, dedup_result) in enumerate(filtered_memories, 1):
            content = memory['content']
            metadata = memory.get('metadata', {})

            print(f"\n[{idx}/{len(filtered_memories)}] {content[:50]}...")

            try:
                # 三代理验证
                responses = self.processor.process_memory_sync(content)
                agg_result = self.aggregator.aggregate(responses)

                # 存储记忆
                if agg_result.final_decision == "STORE":
                    store_result = self.mem0.store_memory(
                        content=content,
                        user_id=user_id,
                        metadata={
                            **metadata,
                            'validation': {
                                'validator': responses.get('validator', {}).response_data if responses.get('validator', {}).success else {},
                                'scorer': responses.get('scorer', {}).response_data if responses.get('scorer', {}).success else {},
                                'reviewer': responses.get('reviewer', {}).response_data if responses.get('reviewer', {}).success else {},
                            },
                            'aggregated': {
                                'vote_result': agg_result.vote_result.value,
                                'final_decision': agg_result.final_decision,
                                'confidence': agg_result.confidence
                            }
                        }
                    )

                    if store_result.get('success'):
                        successful += 1
                        results.append({
                            'index': original_index,
                            'content': content[:100],
                            'status': 'STORED',
                            'memory_id': store_result.get('id'),
                            'validation': agg_result.final_decision
                        })
                    else:
                        failed += 1
                        results.append({
                            'index': original_index,
                            'content': content[:100],
                            'status': 'FAILED',
                            'reason': store_result.get('error', 'Unknown error')
                        })
                else:
                    skipped += 1
                    results.append({
                        'index': original_index,
                        'content': content[:100],
                        'status': 'SKIPPED',
                        'reason': f'验证未通过 ({agg_result.final_decision})'
                    })

            except Exception as e:
                failed += 1
                results.append({
                    'index': original_index,
                    'content': content[:100],
                    'status': 'FAILED',
                    'reason': str(e)
                })

        total_latency = time.time() - start_time

        return BatchResult(
            total=len(memories),
            successful=successful,
            failed=failed,
            skipped=skipped,
            results=results,
            total_latency=total_latency,
            avg_latency=total_latency / len(memories) if len(memories) > 0 else 0
        )

    async def process_batch_async(
        self,
        memories: List[Dict],
        user_id: str = "default",
        skip_duplicates: bool = True
    ) -> BatchResult:
        """
        异步批量处理记忆

        Args:
            memories: 记忆列表
            user_id: 用户 ID
            skip_duplicates: 是否跳过重复记忆

        Returns:
            BatchResult: 批量处理结果
        """
        # 使用线程池执行同步操作
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            result = await loop.run_in_executor(
                executor,
                lambda: self.process_batch(memories, user_id, skip_duplicates)
            )
        return result


if __name__ == "__main__":
    # 测试批量处理功能
    print("=== 批量处理测试 ===\n")

    # 测试样本
    test_memories = [
        {'content': '2026-04-03 完成 Memory-Plus 开发。', 'metadata': {'type': 'WORK'}},
        {'content': '2026-04-03 参加 AI 架构评审会议。', 'metadata': {'type': 'MEETING'}},
        {'content': '2026-04-03 完成 Memory-Plus 开发。', 'metadata': {'type': 'WORK'}},  # 重复
        {'content': '2026-04-03 学习 Rust 编程语言。', 'metadata': {'type': 'LEARNING'}},
        {'content': '2026-04-03 家庭聚餐，讨论周末郊游计划。', 'metadata': {'type': 'FAMILY'}},
    ]

    processor = BatchProcessor(use_local=True, enable_dedup=True)

    result = processor.process_batch(test_memories, user_id="test")

    print("\n" + "="*60)
    print("批量处理结果")
    print("="*60)
    print(f"总数：{result.total}")
    print(f"成功：{result.successful}")
    print(f"失败：{result.failed}")
    print(f"跳过：{result.skipped}")
    print(f"总耗时：{result.total_latency:.1f}s")
    print(f"平均耗时：{result.avg_latency:.1f}s/条")

    print("\n详细结果：")
    for r in result.results:
        print(f"  [{r['index']}] {r['status']}: {r['content'][:50]}...")
        if 'reason' in r:
            print(f"       原因：{r['reason']}")

    print("\n=== 测试完成 ===")
