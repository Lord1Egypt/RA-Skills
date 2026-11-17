"""
Agent Memory System - 性能基准测试套件

提供核心操作的性能基准测试，包括：
- 记忆写入延迟
- 检索吞吐量
- 链提取速度
- 压缩比
"""

import sys
import time
import statistics
from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
from pathlib import Path

from .logging_config import get_logger

logger = get_logger(__name__)


@dataclass
class BenchmarkResult:
    """基准测试结果"""
    name: str
    iterations: int
    total_time: float
    avg_time: float
    min_time: float
    max_time: float
    p50_time: float
    p95_time: float
    p99_time: float
    throughput: float  # ops/sec
    errors: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "iterations": self.iterations,
            "total_time": round(self.total_time, 4),
            "avg_time": round(self.avg_time, 6),
            "min_time": round(self.min_time, 6),
            "max_time": round(self.max_time, 6),
            "p50_time": round(self.p50_time, 6),
            "p95_time": round(self.p95_time, 6),
            "p99_time": round(self.p99_time, 6),
            "throughput": round(self.throughput, 2),
            "errors": self.errors,
        }


class BenchmarkRunner:
    """基准测试运行器"""
    
    def __init__(self, warmup_iterations: int = 10):
        self.warmup_iterations = warmup_iterations
        self.results: List[BenchmarkResult] = []
    
    def run(
        self,
        name: str,
        func: Callable,
        iterations: int = 100,
        *args,
        **kwargs
    ) -> BenchmarkResult:
        """
        运行基准测试
        
        Args:
            name: 测试名称
            func: 测试函数
            iterations: 迭代次数
            *args, **kwargs: 传递给测试函数的参数
        """
        logger.info(f"开始基准测试: {name} (迭代 {iterations} 次)")
        
        # 预热
        for _ in range(self.warmup_iterations):
            try:
                func(*args, **kwargs)
            except Exception:
                pass
        
        # 正式测试
        times = []
        errors = 0
        
        for _ in range(iterations):
            start = time.perf_counter()
            try:
                func(*args, **kwargs)
                elapsed = time.perf_counter() - start
                times.append(elapsed)
            except Exception as e:
                errors += 1
                logger.debug(f"测试执行出错: {e}")
        
        if not times:
            result = BenchmarkResult(
                name=name,
                iterations=iterations,
                total_time=0,
                avg_time=0,
                min_time=0,
                max_time=0,
                p50_time=0,
                p95_time=0,
                p99_time=0,
                throughput=0,
                errors=errors,
            )
        else:
            total_time = sum(times)
            avg_time = total_time / len(times)
            sorted_times = sorted(times)
            
            result = BenchmarkResult(
                name=name,
                iterations=len(times),
                total_time=total_time,
                avg_time=avg_time,
                min_time=sorted_times[0],
                max_time=sorted_times[-1],
                p50_time=sorted_times[len(sorted_times) // 2],
                p95_time=sorted_times[int(len(sorted_times) * 0.95)],
                p99_time=sorted_times[int(len(sorted_times) * 0.99)],
                throughput=len(times) / total_time if total_time > 0 else 0,
                errors=errors,
            )
        
        self.results.append(result)
        logger.info(
            f"基准测试完成: {name} - "
            f"平均: {result.avg_time*1000:.3f}ms, "
            f"吞吐: {result.throughput:.1f} ops/s"
        )
        
        return result
    
    def get_results(self) -> List[Dict[str, Any]]:
        """获取所有测试结果"""
        return [r.to_dict() for r in self.results]
    
    def print_summary(self) -> None:
        """打印测试摘要"""
        print("\n" + "=" * 70)
        print("性能基准测试摘要")
        print("=" * 70)
        print(f"{'测试名称':<30} {'平均(ms)':<12} {'P95(ms)':<12} {'吞吐(ops/s)':<12}")
        print("-" * 70)
        
        for result in self.results:
            print(
                f"{result.name:<30} "
                f"{result.avg_time*1000:<12.3f} "
                f"{result.p95_time*1000:<12.3f} "
                f"{result.throughput:<12.1f}"
            )
        
        print("=" * 70)


# ============================================================================
# 预定义基准测试
# ============================================================================

def benchmark_memory_write(store, data: Dict[str, Any]) -> None:
    """记忆写入基准测试"""
    store.store_conversation(
        user_message=data.get("user_message", "测试消息"),
        system_response=data.get("system_response", "测试回复"),
        user_id=data.get("user_id", "benchmark_user"),
        session_id=data.get("session_id", "benchmark_session"),
    )


def benchmark_memory_read(store, session_id: str) -> None:
    """记忆读取基准测试"""
    store.get_items_by_session(session_id)


def benchmark_chain_extraction(extractor, text: str) -> None:
    """链提取基准测试"""
    extractor.extract(text)


def benchmark_context_orchestration(orchestrator, context: Dict[str, Any]) -> None:
    """上下文编排基准测试"""
    orchestrator.prepare_context(context)


def run_all_benchmarks(output_path: str = None) -> List[Dict[str, Any]]:
    """
    运行所有基准测试
    
    Args:
        output_path: 结果输出路径（可选）
    """
    runner = BenchmarkRunner()
    
    # 注意：这里需要根据实际模块初始化
    # 以下仅为示例框架
    
    logger.info("性能基准测试套件已加载")
    logger.info("请使用 run_all_benchmarks() 运行完整测试")
    
    results = runner.get_results()
    
    if output_path:
        import json
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        logger.info(f"基准测试结果已保存到: {output_path}")
    
    return results


if __name__ == "__main__":
    # Windows 管道重定向时强制 UTF-8 输出，避免 GBK 乱码
    for _stream in (sys.stdout, sys.stderr):
        _stream.reconfigure(encoding="utf-8", errors="replace")
    run_all_benchmarks()
