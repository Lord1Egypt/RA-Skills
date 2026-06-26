"""
性能测试工具包 - 基础使用示例
Performance Testing Toolkit - Basic Usage Examples

本示例展示如何使用性能测试工具包进行负载测试和压力测试
"""

import asyncio
import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from load_tester import LoadTester
from stress_tester import StressTester


def example_basic_load_test():
    """
    示例1: 基础负载测试
    Example 1: Basic Load Test
    """
    print("=" * 60)
    print("示例1: 基础负载测试 | Example 1: Basic Load Test")
    print("=" * 60)
    
    # 创建负载测试器 | Create load tester
    tester = LoadTester(
        url="https://httpbin.org/get",
        concurrent=10,
        method="GET",
        timeout=30
    )
    
    # 运行10秒测试 | Run 10-second test
    print("\n开始测试 (10秒)... | Starting test (10s)...")
    results = tester.run(duration=10)
    
    # 打印结果 | Print results
    print("\n测试结果 | Test Results:")
    print(f"  总请求数 | Total Requests: {results['total_requests']}")
    print(f"  成功请求 | Successful: {results['successful_requests']}")
    print(f"  失败请求 | Failed: {results['failed_requests']}")
    print(f"  平均响应时间 | Avg Response Time: {results['avg_response_time']:.2f}ms")
    print(f"  最小响应时间 | Min Response Time: {results['min_response_time']:.2f}ms")
    print(f"  最大响应时间 | Max Response Time: {results['max_response_time']:.2f}ms")
    print(f"  每秒请求数 | Requests Per Second: {results['rps']:.2f}")
    print(f"  成功率 | Success Rate: {results['success_rate']:.2f}%")
    
    return results


def example_post_load_test():
    """
    示例2: POST请求负载测试
    Example 2: POST Request Load Test
    """
    print("\n" + "=" * 60)
    print("示例2: POST请求测试 | Example 2: POST Request Test")
    print("=" * 60)
    
    # 创建带请求体的测试器 | Create tester with request body
    tester = LoadTester(
        url="https://httpbin.org/post",
        concurrent=5,
        method="POST",
        headers={"Content-Type": "application/json"},
        body='{"test": "data", "timestamp": 1234567890}',
        timeout=30
    )
    
    print("\n开始POST测试 (5秒)... | Starting POST test (5s)...")
    results = tester.run(duration=5)
    
    print("\n测试结果 | Test Results:")
    print(f"  总请求数 | Total Requests: {results['total_requests']}")
    print(f"  成功率 | Success Rate: {results['success_rate']:.2f}%")
    print(f"  平均响应时间 | Avg Response Time: {results['avg_response_time']:.2f}ms")
    
    return results


def example_stress_test():
    """
    示例3: 压力测试
    Example 3: Stress Test
    """
    print("\n" + "=" * 60)
    print("示例3: 压力测试 | Example 3: Stress Test")
    print("=" * 60)
    
    # 创建压力测试器 | Create stress tester
    tester = StressTester(
        url="https://httpbin.org/get",
        method="GET",
        timeout=30
    )
    
    print("\n开始压力测试... | Starting stress test...")
    print("并发数: 5 -> 20 (步长5) | Concurrent: 5 -> 20 (step 5)")
    print("每阶段5秒 | 5 seconds per stage")
    
    # 运行阶梯压力测试 | Run stepped stress test
    results = tester.run(
        start_concurrent=5,
        max_concurrent=20,
        step=5,
        stage_duration=5
    )
    
    print("\n压力测试完成 | Stress test completed")
    print(f"总共测试了 {len(results)} 个并发级别 | Tested {len(results)} concurrency levels")
    
    for level, data in results.items():
        print(f"\n  并发 {level} | Concurrent {level}:")
        print(f"    成功率: {data['success_rate']:.2f}%")
        print(f"    平均响应: {data['avg_response_time']:.2f}ms")
        print(f"    RPS: {data['rps']:.2f}")
    
    return results


def example_custom_headers():
    """
    示例4: 自定义请求头测试
    Example 4: Custom Headers Test
    """
    print("\n" + "=" * 60)
    print("示例4: 自定义请求头 | Example 4: Custom Headers")
    print("=" * 60)
    
    # 创建带认证头的测试器 | Create tester with auth headers
    tester = LoadTester(
        url="https://httpbin.org/headers",
        concurrent=3,
        method="GET",
        headers={
            "Authorization": "Bearer test-token-12345",
            "X-Custom-Header": "PerformanceTest",
            "Accept": "application/json"
        },
        timeout=30
    )
    
    print("\n开始带认证头的测试 (5秒)... | Starting auth header test (5s)...")
    results = tester.run(duration=5)
    
    print("\n测试结果 | Test Results:")
    print(f"  成功率 | Success Rate: {results['success_rate']:.2f}%")
    print(f"  平均响应时间 | Avg Response Time: {results['avg_response_time']:.2f}ms")
    
    return results


def example_report_generation():
    """
    示例5: 生成测试报告
    Example 5: Generate Test Report
    """
    print("\n" + "=" * 60)
    print("示例5: 生成测试报告 | Example 5: Generate Test Report")
    print("=" * 60)
    
    # 创建测试器 | Create tester
    tester = LoadTester(
        url="https://httpbin.org/get",
        concurrent=10,
        method="GET",
        timeout=30
    )
    
    print("\n运行测试... | Running test...")
    results = tester.run(duration=10)
    
    # 生成报告目录 | Create reports directory
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # 保存JSON报告 | Save JSON report
    import json
    json_path = os.path.join(reports_dir, 'performance_report.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nJSON报告已保存 | JSON report saved: {json_path}")
    
    # 生成简单HTML报告 | Generate simple HTML report
    html_path = os.path.join(reports_dir, 'performance_report.html')
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Performance Test Report | 性能测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .metric {{ font-weight: bold; color: #2196F3; }}
    </style>
</head>
<body>
    <h1>性能测试报告 | Performance Test Report</h1>
    <p>生成时间 | Generated: {results.get('timestamp', 'N/A')}</p>
    
    <table>
        <tr><th>指标 | Metric</th><th>数值 | Value</th></tr>
        <tr><td>总请求数 | Total Requests</td><td class="metric">{results['total_requests']}</td></tr>
        <tr><td>成功请求 | Successful</td><td class="metric">{results['successful_requests']}</td></tr>
        <tr><td>失败请求 | Failed</td><td class="metric">{results['failed_requests']}</td></tr>
        <tr><td>成功率 | Success Rate</td><td class="metric">{results['success_rate']:.2f}%</td></tr>
        <tr><td>平均响应时间 | Avg Response Time</td><td class="metric">{results['avg_response_time']:.2f}ms</td></tr>
        <tr><td>最小响应时间 | Min Response Time</td><td class="metric">{results['min_response_time']:.2f}ms</td></tr>
        <tr><td>最大响应时间 | Max Response Time</td><td class="metric">{results['max_response_time']:.2f}ms</td></tr>
        <tr><td>每秒请求数 | RPS</td><td class="metric">{results['rps']:.2f}</td></tr>
    </table>
</body>
</html>"""
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"HTML报告已保存 | HTML report saved: {html_path}")
    
    return results


def main():
    """
    运行所有示例
    Run all examples
    """
    print("\n" + "=" * 60)
    print("性能测试工具包 - 完整示例")
    print("Performance Testing Toolkit - Complete Examples")
    print("=" * 60)
    
    try:
        # 运行所有示例
        example_basic_load_test()
        example_post_load_test()
        example_stress_test()
        example_custom_headers()
        example_report_generation()
        
        print("\n" + "=" * 60)
        print("所有示例运行完成！| All examples completed!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\n用户中断 | User interrupted")
    except Exception as e:
        print(f"\n错误 | Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
