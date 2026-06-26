#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
负载测试脚本 | Load Testing Script
"""

import asyncio
import aiohttp
import time
import json
import argparse
from datetime import datetime
from collections import defaultdict
import statistics


class LoadTester:
    """负载测试器 | Load Tester"""
    
    def __init__(self, url, concurrent_users=10, duration_seconds=60, 
                 method='GET', headers=None, body=None):
        self.url = url
        self.concurrent_users = concurrent_users
        self.duration_seconds = duration_seconds
        self.method = method
        self.headers = headers or {}
        self.body = body
        self.results = []
        self.errors = []
        
    async def make_request(self, session):
        """发送单个请求 | Send single request"""
        start_time = time.time()
        try:
            if self.method == 'GET':
                async with session.get(self.url, headers=self.headers) as resp:
                    await resp.text()
                    status = resp.status
            elif self.method == 'POST':
                async with session.post(self.url, headers=self.headers, data=self.body) as resp:
                    await resp.text()
                    status = resp.status
            else:
                async with session.request(self.method, self.url, headers=self.headers, data=self.body) as resp:
                    await resp.text()
                    status = resp.status
                    
            elapsed = (time.time() - start_time) * 1000  # ms
            return {'status': status, 'response_time': elapsed, 'success': 200 <= status < 400}
        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return {'status': 0, 'response_time': elapsed, 'success': False, 'error': str(e)}
    
    async def worker(self, session, worker_id):
        """工作线程 | Worker"""
        end_time = time.time() + self.duration_seconds
        while time.time() < end_time:
            result = await self.make_request(session)
            result['worker_id'] = worker_id
            result['timestamp'] = datetime.now().isoformat()
            if result['success']:
                self.results.append(result)
            else:
                self.errors.append(result)
            await asyncio.sleep(0.001)  # 防止CPU过载
    
    async def run_async(self):
        """运行异步测试 | Run async test"""
        connector = aiohttp.TCPConnector(limit=self.concurrent_users * 2)
        timeout = aiohttp.ClientTimeout(total=30)
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [self.worker(session, i) for i in range(self.concurrent_users)]
            await asyncio.gather(*tasks)
        
        return self._analyze_results()
    
    def _analyze_results(self):
        """分析结果 | Analyze results"""
        if not self.results:
            return {'error': 'No successful requests'}
        
        response_times = [r['response_time'] for r in self.results]
        total_requests = len(self.results) + len(self.errors)
        
        analysis = {
            'test_id': f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'url': self.url,
            'concurrent_users': self.concurrent_users,
            'duration_seconds': self.duration_seconds,
            'total_requests': total_requests,
            'successful_requests': len(self.results),
            'failed_requests': len(self.errors),
            'success_rate': len(self.results) / total_requests * 100 if total_requests > 0 else 0,
            'requests_per_second': len(self.results) / self.duration_seconds,
            'response_time_ms': {
                'min': min(response_times),
                'max': max(response_times),
                'avg': statistics.mean(response_times),
                'median': statistics.median(response_times),
                'p95': sorted(response_times)[int(len(response_times) * 0.95)],
                'p99': sorted(response_times)[int(len(response_times) * 0.99)]
            }
        }
        return analysis
    
    def run(self):
        """运行测试 | Run test"""
        return asyncio.run(self.run_async())
    
    def generate_report(self, format='html', output_file=None):
        """生成报告 | Generate report"""
        if not output_file:
            output_file = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format}"
        
        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self._analyze_results(), f, indent=2, ensure_ascii=False)
        elif format == 'csv':
            import csv
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['timestamp', 'worker_id', 'status', 'response_time', 'success'])
                for r in self.results:
                    writer.writerow([r['timestamp'], r['worker_id'], r['status'], 
                                   r['response_time'], r['success']])
        print(f"Report saved to: {output_file}")


def main():
    """CLI入口 | CLI entry"""
    parser = argparse.ArgumentParser(description='负载测试工具 | Load Testing Tool')
    parser.add_argument('--url', '-u', required=True, help='目标URL')
    parser.add_argument('--concurrent-users', '-c', type=int, default=10, help='并发用户数')
    parser.add_argument('--duration-seconds', '-d', type=int, default=60, help='持续时间')
    parser.add_argument('--method', '-m', default='GET', choices=['GET', 'POST', 'PUT', 'DELETE'])
    parser.add_argument('--output', '-o', help='输出文件')
    
    args = parser.parse_args()
    
    print(f"Starting load test: {args.url}")
    print(f"Concurrent users: {args.concurrent_users}")
    print(f"Duration: {args.duration_seconds}s")
    print("-" * 50)
    
    tester = LoadTester(
        url=args.url,
        concurrent_users=args.concurrent_users,
        duration_seconds=args.duration_seconds,
        method=args.method
    )
    
    results = tester.run()
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    if args.output:
        tester.generate_report('json', args.output)


if __name__ == '__main__':
    main()
