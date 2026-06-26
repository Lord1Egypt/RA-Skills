---
name: performance
description: Performance analysis and optimization. Profiles code execution, identifies bottlenecks, and suggests optimizations.
---

# Performance - Performance Analysis

性能分析工具，分析代码执行、识别瓶颈、提供优化建议。

**Version**: 1.0  
**Features**: 性能分析、瓶颈识别、优化建议、基准测试

---

## Quick Start

### 1. 分析 Python 代码

```bash
# 分析函数执行时间
python3 scripts/main.py profile --file src/main.py --function process_data

# 分析整个模块
python3 scripts/main.py profile --file src/main.py
```

### 2. 识别瓶颈

```bash
# 扫描代码中的性能问题
python3 scripts/main.py analyze --file src/main.py

# 分析目录
python3 scripts/main.py analyze --dir src/
```

### 3. 基准测试

```bash
# 运行基准测试
python3 scripts/main.py benchmark --file src/main.py --function heavy_computation
```

---

## Commands

| 命令 | 说明 | 示例 |
|------|------|------|
| `profile` | 性能分析 | `profile --file src.py` |
| `analyze` | 瓶颈分析 | `analyze --file src.py` |
| `benchmark` | 基准测试 | `benchmark --function foo` |

---

## Profile 输出

```bash
$ python3 scripts/main.py profile --file src/processor.py --function process_data

🔍 Performance Profile
======================

Function: process_data
File: src/processor.py:45
Calls: 100
Total time: 2.34s
Avg time: 23.4ms

Top hotspots:
  45% - database.query() (line 67)
  30% - json.dumps() (line 89)
  15% - data transformation (line 78)
  10% - other

Recommendations:
  ⚠️  Consider caching database results
  ⚠️  Use orjson instead of json for better performance
```

---

## 瓶颈分析

```bash
$ python3 scripts/main.py analyze --file src/api.py

🔍 Performance Analysis
=======================

File: src/api.py
Issues found: 3

🔴 High Impact:
  Line 34: Nested loop O(n²)
    for user in users:
      for order in orders:  # ← N+1 query pattern
  
  Suggestion: Use JOIN query instead

🟡 Medium Impact:
  Line 67: String concatenation in loop
    result += item  # ← Use list + join instead

🟢 Low Impact:
  Line 89: Unused import
    import heavy_module  # ← Remove if not used
```

---

## 基准测试

```bash
$ python3 scripts/main.py benchmark --file src/sort.py --function quicksort

⏱️  Benchmark Results
====================

Function: quicksort
Iterations: 1000

Time (ms):
  Mean:   12.34
  Median: 11.89
  Min:     8.45
  Max:    45.67
  P95:    18.90
  P99:    32.10

Memory (MB):
  Mean:   2.45
  Peak:   4.12

Comparison:
  vs bubble sort: 45x faster
  vs merge sort:  1.2x faster
```

---

## 检测的优化模式

### 代码层面

| 问题 | 检测 | 建议 |
|------|------|------|
| N+1 查询 | ✅ | 使用 JOIN / select_related |
| 循环内字符串拼接 | ✅ | 使用 list + join |
| 未使用的导入 | ✅ | 移除导入 |
| 嵌套循环 | ✅ | 优化算法或使用哈希 |
| 重复计算 | ✅ | 缓存结果 |

### Python 特定

| 问题 | 检测 | 建议 |
|------|------|------|
| list vs generator | ✅ | 大数据用 generator |
| dict.get() vs [] | ✅ | 使用 .get() 避免 KeyError |
| 列表推导式 | ✅ | 替代 map/filter |

---

## Configuration

`.performance.json`:

```json
{
  "benchmark_iterations": 1000,
  "warmup_iterations": 10,
  "profile_lines": true,
  "check_patterns": [
    "n_plus_one",
    "string_concat_in_loop",
    "unused_imports"
  ]
}
```

---

## CI/CD 集成

```yaml
# .github/workflows/performance.yml
name: Performance Check
on: [pull_request]

jobs:
  perf:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Analyze Performance
        run: python3 skills/performance/scripts/main.py analyze --dir src/
      
      - name: Run Benchmarks
        run: python3 skills/performance/scripts/main.py benchmark --all
```

---

## Files

```
skills/performance/
├── SKILL.md                    # 本文件
└── scripts/
    ├── main.py                 # ⭐ 统一入口
    ├── profiler.py             # 性能分析器
    └── analyzer.py             # 瓶颈分析器
```

---

## Roadmap

- [x] Basic profiling
- [x] Bottleneck detection
- [x] Benchmark runner
- [ ] Memory profiling
- [ ] Flame graph generation
