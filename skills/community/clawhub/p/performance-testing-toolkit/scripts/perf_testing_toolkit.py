#!/usr/bin/env python3
"""
Performance Testing Toolkit - Core Module
性能测试工具包 - 核心模块

Author: ClawHub
Version: 1.0.0
"""

import asyncio
import time
import json
import statistics
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Callable, Any
from concurrent.futures import ThreadPoolExecutor
import requests
import aiohttp
import psutil


@dataclass
class TestResult:
    """性能测试结果数据类 | Performance test result data class"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_time: float = 0.0
    response_times: List[float] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    
    @property
    def success_rate(self) -> float:
        """成功率 | Success rate percentage"""
        if self.total_requests == 0:
            return 0.0
        return (self.successful_requests / self.total_requests) * 100
    
    @property
    def avg_response_time(self) -> float:
        """平均响应时间(ms) | Average response time in ms"""
        if not self.response_times:
            return 0.0
        return statistics.mean(self.response_times)
    
    @property
    def min_response_time(self) -> float:
        """最小响应时间(ms) | Minimum response time"""
        if not self.response_times:
            return 0.0
        return min(self.response_times)
    
    @property
    def max_response_time(self) -> float:
        """最大响应时间(ms) | Maximum response time"""
        if not self.response_times:
            return 0.0
        return max(self.response_times)
    
    @property
    def p50_response_time(self) -> float:
        """50分位响应时间 | P50 response time"""
        if not self.response_times:
            return 0.0
        return statistics.median(self.response_times)
    
    @property
    def p95_response_time(self) -> float:
        """95分位响应时间 | P95 response time"""
        if not self.response_times:
            return 0.0
        return statistics.quantiles(self.response_times, n=20)[18] if len(self.response_times) >= 20 else max(self.response_times)
    
    @property
    def p99_response_time(self) -> float:
        """99分位响应时间 | P99 response time"""
        if not self.response_times:
            return 0.0
        return statistics.quantiles(self.response_times, n=100)[98] if len(self.response_times) >= 100 else max(self.response_times)
    
    @property
    def requests_per_second(self) -> float:
        """每秒请求数(RPS) | Requests per second"""
        if self.total_time <= 0:
            return 0.0
        return self.total_requests / self.total_time
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典 | Convert to dictionary"""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "success_rate": round(self.success_rate, 2),
            "avg_response_time": round(self.avg_response_time, 2),
            "min_response_time": round(self.min_response_time, 2),
            "max_response_time": round(self.max_response_time, 2),
            "p50_response_time": round(self.p50_response_time, 2),
            "p95_response_time": round(self.p95_response_time, 2),
            "p99_response_time": round(self.p99_response_time, 2),
            "requests_per_second": round(self.requests_per_second, 2),
            "total_time": round(self.total_time, 2),
            "errors": self.errors[:10]  # 只保留前10个错误
        }


class LoadTester:
    """
    负载测试器 | Load Tester
    
    模拟多并发用户对接口进行负载测试
    Simulate multiple concurrent users to test API performance
    """
    
    def __init__(
        self,
        url: str,
        concurrent: int = 10,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        timeout: int = 30
    ):
        self.url = url
        self.concurrent = concurrent
        self.method = method.upper()
        self.headers = headers or {}
        self.body = body
        self.timeout = timeout
        self.result = TestResult()
        self._stop_event = False
        
    def _make_request(self, session: requests.Session) -> tuple:
        """执行单个请求 | Execute a single request"""
        start = time.time()
        try:
            if self.method == "GET":
                response = session.get(
                    self.url, 
                    headers=self.headers, 
                    timeout=self.timeout
                )
            elif self.method == "POST":
                response = session.post(
                    self.url, 
                    headers=self.headers, 
                    data=self.body,
                    timeout=self.timeout
                )
            elif self.method == "PUT":
                response = session.put(
                    self.url, 
                    headers=self.headers, 
                    data=self.body,
                    timeout=self.timeout
                )
            elif self.method == "DELETE":
                response = session.delete(
                    self.url, 
                    headers=self.headers, 
                    timeout=self.timeout
                )
            else:
                response = session.request(
                    self.method,
                    self.url,
                    headers=self.headers,
                    data=self.body,
                    timeout=self.timeout
                )
            
            elapsed = (time.time() - start) * 1000  # 转换为毫秒
            success = 200 <= response.status_code < 300
            return success, elapsed, response.status_code, None
            
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return False, elapsed, 0, str(e)
    
    def _worker(self, duration: int, session: requests.Session):
        """工作线程 | Worker thread"""
        end_time = time.time() + duration
        
        while time.time() < end_time and not self._stop_event:
            success, elapsed, status, error = self._make_request(session)
            
            self.result.total_requests += 1
            if success:
                self.result.successful_requests += 1
                self.result.response_times.append(elapsed)
            else:
                self.result.failed_requests += 1
                if error:
                    self.result.errors.append(f"Status {status}: {error}")
    
    def run(self, duration: int = 60) -> TestResult:
        """
        运行负载测试 | Run load test
        
        Args:
            duration: 测试持续时间(秒) | Test duration in seconds
            
        Returns:
            TestResult: 测试结果 | Test results
        """
        print(f"🚀 Starting load test: {self.concurrent} concurrent users for {duration}s")
        print(f"   URL: {self.url}")
        print(f"   Method: {self.method}")
        
        self.result.start_time = time.time()
        
        # 创建会话池 | Create session pool
        sessions = [requests.Session() for _ in range(self.concurrent)]
        
        # 使用线程池并发执行 | Use thread pool for concurrent execution
        with ThreadPoolExecutor(max_workers=self.concurrent) as executor:
            futures = [
                executor.submit(self._worker, duration, session)
                for session in sessions
            ]
            # 等待所有任务完成 | Wait for all tasks to complete
            for future in futures:
                future.result()
        
        self.result.end_time = time.time()
        self.result.total_time = self.result.end_time - self.result.start_time
        
        # 关闭会话 | Close sessions
        for session in sessions:
            session.close()
        
        print(f"✅ Load test completed!")
        return self.result
    
    def stop(self):
        """停止测试 | Stop the test"""
        self._stop_event = True


class StressTester:
    """
    压力测试器 | Stress Tester
    
    逐步增加负载直到找到系统瓶颈
    Gradually increase load until system bottleneck is found
    """
    
    def __init__(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        timeout: int = 30
    ):
        self.url = url
        self.method = method.upper()
        self.headers = headers or {}
        self.body = body
        self.timeout = timeout
        self.results: List[Dict[str, Any]] = []
        
    def run(
        self,
        start_concurrent: int = 10,
        max_concurrent: int = 1000,
        step: int = 50,
        step_duration: int = 30
    ) -> List[Dict[str, Any]]:
        """
        运行压力测试 | Run stress test
        
        Args:
            start_concurrent: 起始并发数 | Starting concurrent users
            max_concurrent: 最大并发数 | Maximum concurrent users
            step: 每步增加的并发数 | Concurrent users increment per step
            step_duration: 每步持续时间(秒) | Duration per step in seconds
            
        Returns:
            List[Dict]: 每步的测试结果 | Results for each step
        """
        print(f"📊 Starting stress test: {start_concurrent} -> {max_concurrent} (step: {step})")
        print(f"   URL: {self.url}")
        
        current = start_concurrent
        
        while current <= max_concurrent:
            print(f"\n🔥 Testing with {current} concurrent users...")
            
            tester = LoadTester(
                url=self.url,
                concurrent=current,
                method=self.method,
                headers=self.headers,
                body=self.body,
                timeout=self.timeout
            )
            
            result = tester.run(duration=step_duration)
            result_dict = result.to_dict()
            result_dict["concurrent"] = current
            self.results.append(result_dict)
            
            print(f"   Success Rate: {result_dict['success_rate']:.1f}%")
            print(f"   Avg Response: {result_dict['avg_response_time']:.1f}ms")
            print(f"   RPS: {result_dict['requests_per_second']:.1f}")
            
            # 如果成功率低于90%, 停止测试
            # Stop if success rate drops below 90%
            if result_dict['success_rate'] < 90:
                print(f"\n⚠️  Success rate dropped below 90% at {current} concurrent users")
                print(f"   System bottleneck detected!")
                break
            
            current += step
        
        print(f"\n✅ Stress test completed! Total steps: {len(self.results)}")
        return self.results


class ReportGenerator:
    """
    报告生成器 | Report Generator
    
    生成HTML/JSON格式的性能测试报告
    Generate HTML/JSON performance test reports
    """
    
    @staticmethod
    def generate_html(results: Dict[str, Any], output_path: str):
        """生成HTML报告 | Generate HTML report"""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Performance Test Report | 性能测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        h2 { color: #555; margin-top: 30px; }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }
        .metric-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
        .metric-value { font-size: 32px; font-weight: bold; color: #007bff; }
        .metric-label { color: #666; margin-top: 5px; }
        .success { color: #28a745; }
        .warning { color: #ffc107; }
        .danger { color: #dc3545; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: bold; }
        .footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Performance Test Report | 性能测试报告</h1>
        
        <h2>📊 Summary Metrics | 汇总指标</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{{ total_requests }}</div>
                <div class="metric-label">Total Requests | 总请求数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value {{ 'success' if success_rate >= 95 else 'warning' if success_rate >= 90 else 'danger' }}">{{ success_rate }}%</div>
                <div class="metric-label">Success Rate | 成功率</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ avg_response_time }}ms</div>
                <div class="metric-label">Avg Response | 平均响应时间</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ rps }}</div>
                <div class="metric-label">RPS | 每秒请求数</div>
            </div>
        </div>
        
        <h2>📈 Response Time Distribution | 响应时间分布</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{{ min_response_time }}ms</div>
                <div class="metric-label">Min | 最小值</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ p50_response_time }}ms</div>
                <div class="metric-label">P50 | 中位数</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ p95_response_time }}ms</div>
                <div class="metric-label">P95 | 95分位</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{{ p99_response_time }}ms</div>
                <div class="metric-label">P99 | 99分位</div>
            </div>
        </div>
        
        <h2>📋 Detailed Results | 详细结果</h2>
        <table>
            <tr>
                <th>Metric | 指标</th>
                <th>Value | 数值</th>
            </tr>
            <tr><td>Total Requests | 总请求数</td><td>{{ total_requests }}</td></tr>
            <tr><td>Successful Requests | 成功请求</td><td>{{ successful_requests }}</td></tr>
            <tr><td>Failed Requests | 失败请求</td><td>{{ failed_requests }}</td></tr>
            <tr><td>Success Rate | 成功率</td><td>{{ success_rate }}%</td></tr>
            <tr><td>Avg Response Time | 平均响应时间</td><td>{{ avg_response_time }}ms</td></tr>
            <tr><td>Min Response Time | 最小响应时间</td><td>{{ min_response_time }}ms</td></tr>
            <tr><td>Max Response Time | 最大响应时间</td><td>{{ max_response_time }}ms</td></tr>
            <tr><td>P50 Response Time | P50响应时间</td><td>{{ p50_response_time }}ms</td></tr>
            <tr><td>P95 Response Time | P95响应时间</td><td>{{ p95_response_time }}ms</td></tr>
            <tr><td>P99 Response Time | P99响应时间</td><td>{{ p99_response_time }}ms</td></tr>
            <tr><td>Requests Per Second | 每秒请求数</td><td>{{ rps }}</td></tr>
            <tr><td>Total Time | 总耗时</td><td>{{ total_time }}s</td></tr>
        </table>
        
        <div class="footer">
            Generated by Performance Testing Toolkit | 性能测试工具包生成<br>
            {{ timestamp }}
        </div>
    </div>
</body>
</html>
        """
        
        from jinja2 import Template
        template = Template(html_template)
        
        html_content = template.render(
            total_requests=results.get('total_requests', 0),
            successful_requests=results.get('successful_requests', 0),
            failed_requests=results.get('failed_requests', 0),
            success_rate=results.get('success_rate', 0),
            avg_response_time=results.get('avg_response_time', 0),
            min_response_time=results.get('min_response_time', 0),
            max_response_time=results.get('max_response_time', 0),
            p50_response_time=results.get('p50_response_time', 0),
            p95_response_time=results.get('p95_response_time', 0),
            p99_response_time=results.get('p99_response_time', 0),
            rps=results.get('requests_per_second', 0),
            total_time=results.get('total_time', 0),
            timestamp=time.strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 HTML report generated: {output_path}")
    
    @staticmethod
    def generate_json(results: Dict[str, Any], output_path: str):
        """生成JSON报告 | Generate JSON report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"📄 JSON report generated: {output_path}")


if __name__ == "__main__":
    # 简单测试 | Simple test
    print("Performance Testing Toolkit - Core Module")
    print("Use 'python scripts/perf_tester.py' for CLI interface")
