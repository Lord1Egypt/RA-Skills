# Performance Testing Toolkit | 性能测试工具包

<p align="center">
  🚀 Enterprise-grade performance testing toolkit for APIs and web services
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>
## English

### Overview

Performance Testing Toolkit is a comprehensive solution for testing the performance of APIs, web services, and applications. It provides load testing, stress testing, benchmark testing, and detailed performance reporting.

### Installation

```bash
pip install -r requirements.txt
```

### Features

| Feature | Description |
|---------|-------------|
| Load Testing | Simulate high-concurrency requests to test API performance |
| Stress Testing | Gradually increase load until system bottleneck is found |
| Benchmark Testing | Compare performance across different configurations |
| Real-time Monitoring | Track CPU, memory, response time in real-time |
| Visual Reports | Generate HTML/JSON performance reports automatically |
| Flexible Config | Support custom headers, parameters, assertions |

### Quick Start

```python
from performance_testing_toolkit import LoadTester

# Create a load tester
tester = LoadTester(
    url="https://api.example.com/users",
    concurrent=100,
    method="GET"
)

# Run the test for 60 seconds
results = tester.run(duration=60)

# Print results
print(f"Total requests: {results.total_requests}")
print(f"Success rate: {results.success_rate}%")
print(f"Avg response time: {results.avg_response_time}ms")
print(f"RPS: {results.requests_per_second}")
```

### CLI Usage

```bash
# Basic load test
python scripts/perf_tester.py load \
  --url https://api.example.com/users \
  --concurrent 100 \
  --duration 60

# Stress test with step increments
python scripts/perf_tester.py stress \
  --url https://api.example.com/search \
  --start 10 \
  --max 1000 \
  --step 50

# Generate HTML report
python scripts/perf_tester.py load \
  --url https://api.example.com/api \
  --concurrent 50 \
  --duration 120 \
  --output html \
  --report-dir ./reports
```

### Configuration File

Create a `benchmark.yaml`:

```yaml
targets:
  - name: "API Endpoint 1"
    url: "https://api.example.com/users"
    method: "GET"
    concurrent: [10, 50, 100, 200]
    duration: 60
  
  - name: "API Endpoint 2"
    url: "https://api.example.com/search"
    method: "POST"
    headers:
      Content-Type: "application/json"
    body: '{"query": "test"}'
    concurrent: [50, 100]
    duration: 120

report:
  format: html
  output_dir: ./reports
```

---

<a name="中文"></a>
## 中文

### 概述

性能测试工具包是一个全面的性能测试解决方案，用于测试API、Web服务和应用程序的性能。它提供负载测试、压力测试、基准测试和详细的性能报告功能。

### 安装

```bash
pip install -r requirements.txt
```

### 功能特性

| 特性 | 说明 |
|------|------|
| 负载测试 | 模拟高并发请求测试接口性能 |
| 压力测试 | 逐步增加负载直到发现系统瓶颈 |
| 基准测试 | 对比不同配置的性能表现 |
| 实时监控 | 实时追踪CPU、内存、响应时间 |
| 可视化报告 | 自动生成HTML/JSON性能报告 |
| 灵活配置 | 支持自定义请求头、参数、断言 |

### 快速开始

```python
from performance_testing_toolkit import LoadTester

# 创建负载测试器
tester = LoadTester(
    url="https://api.example.com/users",
    concurrent=100,
    method="GET"
)

# 运行60秒测试
results = tester.run(duration=60)

# 打印结果
print(f"总请求数: {results.total_requests}")
print(f"成功率: {results.success_rate}%")
print(f"平均响应时间: {results.avg_response_time}ms")
print(f"每秒请求数: {results.requests_per_second}")
```

### 命令行使用

```bash
# 基础负载测试
python scripts/perf_tester.py load \
  --url https://api.example.com/users \
  --concurrent 100 \
  --duration 60

# 阶梯式压力测试
python scripts/perf_tester.py stress \
  --url https://api.example.com/search \
  --start 10 \
  --max 1000 \
  --step 50

# 生成HTML报告
python scripts/perf_tester.py load \
  --url https://api.example.com/api \
  --concurrent 50 \
  --duration 120 \
  --output html \
  --report-dir ./reports
```

### 配置文件

创建 `benchmark.yaml`:

```yaml
targets:
  - name: "API接口1"
    url: "https://api.example.com/users"
    method: "GET"
    concurrent: [10, 50, 100, 200]
    duration: 60
  
  - name: "API接口2"
    url: "https://api.example.com/search"
    method: "POST"
    headers:
      Content-Type: "application/json"
    body: '{"query": "test"}'
    concurrent: [50, 100]
    duration: 120

report:
  format: html
  output_dir: ./reports
```

## 测试 | Testing

```bash
python -m pytest tests/test_perf_testing.py -v
```

## 许可证 | License

MIT License
