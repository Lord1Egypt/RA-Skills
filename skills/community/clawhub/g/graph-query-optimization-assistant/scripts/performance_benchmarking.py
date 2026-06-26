"""
Performance Benchmarking Tools: Compare and analyze query performance.

Provides utilities for benchmarking graph queries, comparing optimization
strategies, and generating performance reports.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
import time
import statistics


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class BenchmarkRun:
    """Result of a single benchmark run."""
    query_name: str
    query: str
    execution_time_ms: float
    memory_mb: float = 0.0
    nodes_visited: int = 0
    success: bool = True
    error: Optional[str] = None


@dataclass
class BenchmarkStatistics:
    """Statistics for multiple benchmark runs."""
    query_name: str
    run_count: int = 0
    mean_time_ms: float = 0.0
    median_time_ms: float = 0.0
    min_time_ms: float = 0.0
    max_time_ms: float = 0.0
    stdev_time_ms: float = 0.0
    mean_memory_mb: float = 0.0
    success_rate: float = 100.0


@dataclass
class PerformanceComparison:
    """Comparison between two query variants."""
    query_name: str
    original_stats: BenchmarkStatistics
    optimized_stats: BenchmarkStatistics
    speedup_factor: float = 1.0
    memory_reduction_percent: float = 0.0
    improvement_summary: str = ""


# ============================================================================
# Benchmark Runner
# ============================================================================

class BenchmarkRunner:
    """Executes benchmark runs for queries."""

    def __init__(self, run_count: int = 5):
        """
        Initialize benchmark runner.

        Args:
            run_count: Number of runs for each benchmark
        """
        self.run_count = run_count
        self.runs: List[BenchmarkRun] = []

    def run_benchmark(self, query_name: str, query: str,
                     executor: Callable[[str], float],
                     memory_executor: Optional[Callable[[str], float]] = None) -> BenchmarkStatistics:
        """
        Run benchmark for a query.

        Args:
            query_name: Name of the query
            query: Query string
            executor: Function that executes query and returns time in ms
            memory_executor: Optional function that returns memory usage in MB

        Returns:
            BenchmarkStatistics with results
        """
        execution_times = []
        memory_usages = []
        success_count = 0

        for i in range(self.run_count):
            try:
                # Measure execution time
                start_time = time.time()
                exec_time = executor(query)
                elapsed = (time.time() - start_time) * 1000  # Convert to ms

                execution_times.append(exec_time if exec_time > 0 else elapsed)

                # Measure memory if available
                if memory_executor:
                    memory_mb = memory_executor(query)
                    memory_usages.append(memory_mb)

                run = BenchmarkRun(
                    query_name=query_name,
                    query=query,
                    execution_time_ms=exec_time if exec_time > 0 else elapsed,
                    memory_mb=memory_mb if memory_executor else 0.0,
                    success=True
                )
                self.runs.append(run)
                success_count += 1

            except Exception as e:
                run = BenchmarkRun(
                    query_name=query_name,
                    query=query,
                    execution_time_ms=0.0,
                    success=False,
                    error=str(e)
                )
                self.runs.append(run)

        # Calculate statistics
        if execution_times:
            stats = BenchmarkStatistics(
                query_name=query_name,
                run_count=len(execution_times),
                mean_time_ms=statistics.mean(execution_times),
                median_time_ms=statistics.median(execution_times),
                min_time_ms=min(execution_times),
                max_time_ms=max(execution_times),
                stdev_time_ms=statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0,
                mean_memory_mb=statistics.mean(memory_usages) if memory_usages else 0.0,
                success_rate=(success_count / self.run_count) * 100
            )
        else:
            stats = BenchmarkStatistics(query_name=query_name)

        return stats

    def compare_queries(self, query_name: str, original_query: str,
                       optimized_query: str, executor: Callable[[str], float],
                       memory_executor: Optional[Callable[[str], float]] = None) -> PerformanceComparison:
        """
        Compare performance of original vs optimized query.

        Args:
            query_name: Name of the query
            original_query: Original query string
            optimized_query: Optimized query string
            executor: Function to execute queries
            memory_executor: Optional memory measurement function

        Returns:
            PerformanceComparison with results
        """
        original_stats = self.run_benchmark(
            f"{query_name} (Original)", original_query, executor, memory_executor
        )

        optimized_stats = self.run_benchmark(
            f"{query_name} (Optimized)", optimized_query, executor, memory_executor
        )

        # Calculate comparison metrics
        speedup = (original_stats.mean_time_ms /
                  max(optimized_stats.mean_time_ms, 0.001))
        memory_reduction = 0.0
        if original_stats.mean_memory_mb > 0:
            memory_reduction = ((original_stats.mean_memory_mb - optimized_stats.mean_memory_mb) /
                               original_stats.mean_memory_mb) * 100

        summary = f"{speedup:.1f}x faster, {memory_reduction:.1f}% less memory"

        comparison = PerformanceComparison(
            query_name=query_name,
            original_stats=original_stats,
            optimized_stats=optimized_stats,
            speedup_factor=speedup,
            memory_reduction_percent=memory_reduction,
            improvement_summary=summary
        )

        return comparison

    def get_run_history(self, query_name: Optional[str] = None) -> List[BenchmarkRun]:
        """
        Get benchmark run history.

        Args:
            query_name: Optional filter by query name

        Returns:
            List of benchmark runs
        """
        if query_name:
            return [r for r in self.runs if query_name in r.query_name]
        return self.runs


# ============================================================================
# Metrics Collector
# ============================================================================

class MetricsCollector:
    """Collects and aggregates query execution metrics."""

    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: Dict[str, List[Dict]] = {}

    def record_execution(self, query_name: str, execution_time_ms: float,
                        nodes_visited: int = 0, memory_mb: float = 0.0):
        """
        Record query execution metrics.

        Args:
            query_name: Name of the query
            execution_time_ms: Execution time in milliseconds
            nodes_visited: Number of nodes visited (optional)
            memory_mb: Memory used in MB (optional)
        """
        if query_name not in self.metrics:
            self.metrics[query_name] = []

        self.metrics[query_name].append({
            "time_ms": execution_time_ms,
            "nodes": nodes_visited,
            "memory_mb": memory_mb
        })

    def get_summary(self, query_name: str) -> Dict:
        """
        Get summary statistics for a query.

        Args:
            query_name: Name of the query

        Returns:
            Dictionary with summary statistics
        """
        if query_name not in self.metrics or not self.metrics[query_name]:
            return {}

        records = self.metrics[query_name]
        times = [r["time_ms"] for r in records]
        nodes = [r["nodes"] for r in records if r["nodes"] > 0]
        memory = [r["memory_mb"] for r in records if r["memory_mb"] > 0]

        summary = {
            "query": query_name,
            "run_count": len(records),
            "avg_time_ms": statistics.mean(times),
            "min_time_ms": min(times),
            "max_time_ms": max(times),
        }

        if nodes:
            summary["avg_nodes_visited"] = statistics.mean(nodes)

        if memory:
            summary["avg_memory_mb"] = statistics.mean(memory)

        return summary

    def compare_metrics(self, query1: str, query2: str) -> Dict:
        """
        Compare metrics between two queries.

        Args:
            query1: First query name
            query2: Second query name

        Returns:
            Comparison dictionary
        """
        summary1 = self.get_summary(query1)
        summary2 = self.get_summary(query2)

        if not summary1 or not summary2:
            return {}

        speedup = summary1["avg_time_ms"] / max(summary2["avg_time_ms"], 0.001)

        return {
            "query1": query1,
            "query2": query2,
            "speedup_factor": speedup,
            "time_savings_ms": summary1["avg_time_ms"] - summary2["avg_time_ms"],
            "faster_query": query1 if speedup > 1 else query2
        }


# ============================================================================
# Report Generator
# ============================================================================

class BenchmarkReportGenerator:
    """Generates formatted benchmark reports."""

    @staticmethod
    def generate_comparison_report(comparison: PerformanceComparison) -> str:
        """
        Generate formatted comparison report.

        Args:
            comparison: PerformanceComparison object

        Returns:
            Formatted report string
        """
        lines = [
            f"\n{'='*70}",
            f"Performance Comparison Report: {comparison.query_name}",
            f"{'='*70}\n",

            "ORIGINAL QUERY:",
            f"  Mean Time: {comparison.original_stats.mean_time_ms:.2f} ms",
            f"  Median Time: {comparison.original_stats.median_time_ms:.2f} ms",
            f"  Min/Max: {comparison.original_stats.min_time_ms:.2f} / {comparison.original_stats.max_time_ms:.2f} ms",
            f"  StdDev: {comparison.original_stats.stdev_time_ms:.2f} ms",
            f"  Runs: {comparison.original_stats.run_count}",
            f"  Memory (avg): {comparison.original_stats.mean_memory_mb:.2f} MB",
            f"  Success Rate: {comparison.original_stats.success_rate:.1f}%\n",

            "OPTIMIZED QUERY:",
            f"  Mean Time: {comparison.optimized_stats.mean_time_ms:.2f} ms",
            f"  Median Time: {comparison.optimized_stats.median_time_ms:.2f} ms",
            f"  Min/Max: {comparison.optimized_stats.min_time_ms:.2f} / {comparison.optimized_stats.max_time_ms:.2f} ms",
            f"  StdDev: {comparison.optimized_stats.stdev_time_ms:.2f} ms",
            f"  Runs: {comparison.optimized_stats.run_count}",
            f"  Memory (avg): {comparison.optimized_stats.mean_memory_mb:.2f} MB",
            f"  Success Rate: {comparison.optimized_stats.success_rate:.1f}%\n",

            "IMPROVEMENT METRICS:",
            f"  ⚡ Speedup: {comparison.speedup_factor:.1f}x faster",
            f"  💾 Memory Reduction: {comparison.memory_reduction_percent:.1f}%",
            f"  Time Saved: {comparison.original_stats.mean_time_ms - comparison.optimized_stats.mean_time_ms:.2f} ms per query",
            f"\n  Summary: {comparison.improvement_summary}",
            f"\n{'='*70}\n"
        ]

        return "\n".join(lines)

    @staticmethod
    def generate_batch_report(comparisons: List[PerformanceComparison]) -> str:
        """
        Generate report for multiple comparisons.

        Args:
            comparisons: List of PerformanceComparison objects

        Returns:
            Formatted batch report
        """
        lines = [
            f"\n{'='*70}",
            "Benchmark Report - Multiple Queries",
            f"{'='*70}\n",
            f"{'Query':<30} {'Speedup':<12} {'Memory':<15} {'Status':<10}",
            f"{'-'*67}"
        ]

        total_speedup = 0
        for comp in comparisons:
            speedup_str = f"{comp.speedup_factor:.1f}x"
            memory_str = f"{comp.memory_reduction_percent:.1f}%"
            status = "✓" if comp.speedup_factor > 1 else "✗"

            lines.append(
                f"{comp.query_name:<30} {speedup_str:<12} {memory_str:<15} {status:<10}"
            )
            total_speedup += comp.speedup_factor

        avg_speedup = total_speedup / len(comparisons) if comparisons else 0
        lines.extend([
            f"{'-'*67}",
            f"Average Speedup: {avg_speedup:.1f}x",
            f"\n{'='*70}\n"
        ])

        return "\n".join(lines)


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    print("🚀 Performance Benchmarking Tools - Example\n")

    # Create benchmark runner
    runner = BenchmarkRunner(run_count=5)

    # Simulate query executor (in real usage, this would run actual queries)
    def mock_executor(query: str) -> float:
        """Mock executor that returns simulated execution time."""
        if "optimized" in query.lower():
            return 320.0  # Optimized query is faster
        return 8342.0  # Original query is slower

    # Compare queries
    original = "MATCH (p:Person)-[:WORKS_AT]->(c:Company) WHERE c.name = 'Acme' RETURN p"
    optimized = "MATCH (c:Company {name: 'Acme'}) MATCH (c)<-[:WORKS_AT]-(p:Person) RETURN p"

    comparison = runner.compare_queries(
        "Product Search",
        original,
        optimized,
        mock_executor
    )

    # Generate report
    report = BenchmarkReportGenerator.generate_comparison_report(comparison)
    print(report)

    print("✅ Benchmark Tools Ready!")

