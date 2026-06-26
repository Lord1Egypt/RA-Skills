---
name: performance-profiling
description: 性能分析速查。当需要：(1) Python 性能分析 (2) Node.js 性能分析 (3) 数据库优化 (4) 系统性能监控时使用。
---

# Performance Profiling

性能分析和调优工具速查。

## 快速参考

### Python 分析
```bash
python -m cProfile script.py
python -m cProfile -s cumtime script.py
pip install py-spy && py-spy top --pid 12345
```

### Node.js 分析
```bash
node --prof app.js
node --cpu-prof app.js
npm install -g clinic && clinic doctor -- node app.js
```

### 数据库
```sql
-- MySQL
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'Alice';
SHOW PROCESSLIST;

-- PostgreSQL
EXPLAIN ANALYZE SELECT * FROM users WHERE name = 'Alice';
SELECT * FROM pg_stat_activity;
```

### 系统
```bash
top -o %CPU                 # CPU
iostat -x 1                 # I/O
vmstat 1                    # 综合
```

## 详细参考

- **Python 分析**: [references/python.md](references/python.md) - cProfile, line_profiler, py-spy
- **Node.js 分析**: [references/nodejs.md](references/nodejs.md) - V8 分析, clinic.js
- **数据库优化**: [references/database.md](references/database.md) - MySQL, PostgreSQL, Redis
- **系统性能**: [references/system.md](references/system.md) - CPU, 内存, I/O
- **Web 压测**: [references/load-test.md](references/load-test.md) - ab, wrk, hey

## 常见优化

### Python
```python
# 字符串拼接
result = "".join(strings)   # 而非 for + loop

# 使用生成器
result = (x for x in range(1000000))

# 内置函数更快
total = sum(numbers)
```

### 数据库
- 添加合适索引
- 避免全表扫描
- 使用 EXPLAIN 分析
- 缓存热点数据

## 文档

- Python profiling: https://docs.python.org/3/library/profile.html
- clinic.js: https://clinicjs.org/
- FlameGraph: https://www.brendangregg.com/flamegraphs.html
