---
name: performance-testing-toolkit
version: 1.0.0
description: |
  企业级性能测试工具包，支持HTTP接口压测、负载测试、性能基准测试和报告生成。
  Enterprise-grade performance testing toolkit supporting HTTP load testing, stress testing, benchmark testing and report generation.
---

# Performance Testing Toolkit | 性能测试工具包

一套完整的性能测试解决方案，用于测试API、Web服务和应用程序的性能表现。

A comprehensive performance testing solution for testing APIs, web services, and application performance.

## 核心功能 | Core Features

- 🚀 **HTTP负载测试** | HTTP Load Testing - 模拟高并发请求测试接口性能
- 📊 **实时性能监控** | Real-time Performance Monitoring - CPU、内存、响应时间追踪
- 📈 **压力测试** | Stress Testing - 逐步增加负载直到系统瓶颈
- 🎯 **基准测试** | Benchmark Testing - 对比不同配置的性能表现
- 📋 **可视化报告** | Visual Reports - 自动生成HTML/JSON性能报告
- 🔧 **灵活配置** | Flexible Configuration - 支持自定义请求头、参数、断言

## 快速开始 | Quick Start

### 命令行使用 | CLI Usage

```bash
# 基础负载测试 | Basic load test
python scripts/perf_tester.py load --url https://api.example.com/users --concurrent 100 --duration 60

# 压力测试 | Stress test
python scripts/perf_tester.py stress --url https://api.example.com/search --start 10 --max 1000 --step 50

# 基准对比测试 | Benchmark test
python scripts/perf_tester.py benchmark --config benchmark.yaml
```

### Python API | Python API

```python
from performance_testing_toolkit import LoadTester, StressTester

# 负载测试 | Load test
tester = LoadTester(url="https://api.example.com/api", concurrent=100)
results = tester.run(duration=60)
print(f"平均响应时间: {results.avg_response_time}ms")

# 压力测试 | Stress test
stress = StressTester(url="https://api.example.com/api")
stress.run(start_concurrent=10, max_concurrent=1000, step=50)
```

## 参数说明 | Parameters

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 目标URL | 必填 |
| `--concurrent` | 并发用户数 | 10 |
| `--duration` | 测试持续时间(秒) | 60 |
| `--method` | HTTP方法 | GET |
| `--headers` | 请求头(JSON格式) | {} |
| `--output` | 报告输出格式 | html |

## 示例 | Examples

详见 [examples/](examples/) 目录。

## 测试 | Tests

```bash
python -m pytest tests/ -v
```
