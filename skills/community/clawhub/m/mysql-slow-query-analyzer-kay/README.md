# MySQL Slow Query Analyzer

MySQL 慢查询分析与优化工具 - 帮助开发者定位和优化 MySQL 慢查询。

## 功能特性

- **EXPLAIN 解析**: 支持 JSON / Traditional / TAB 格式
- **慢查询日志分析**: 自动识别慢查询并给出严重级别
- **索引建议**: 基于 WHERE/JOIN/ORDER BY/GROUP BY 自动生成索引建议
- **SQL 重写建议**: 检测并建议 SELECT *、大 OFFSET、隐式类型转换等问题
- **性能评分**: 0-100 分评分系统，直观展示查询质量

## 安装

```bash
git clone <repo>
cd mysql-slow-query-analyzer
```

无需额外依赖，仅需要 Python 3.10+。

## 使用方法

### CLI

```bash
# 解析 EXPLAIN JSON
python mysql_slow_query_analyzer.py explain-json '<JSON>'

# 解析 EXPLAIN TEXT
python mysql_slow_query_analyzer.py explain-text '<TEXT>'

# 分析慢查询日志
python mysql_slow_query_analyzer.py slowlog '<LOG_ENTRY>'

# 生成索引建议
python mysql_slow_query_analyzer.py index-advice '<SQL>'

# SQL 重写建议
python mysql_slow_query_analyzer.py rewrite '<SQL>'

# 完整分析
python mysql_slow_query_analyzer.py analyze '<SQL>'
```

### Python API

```python
from mysql_slow_query_analyzer import (
    parse_explain_json,
    parse_slow_query_log,
    generate_index_suggestions,
    generate_rewrite_suggestions,
    analyze_slow_query,
)

# 解析 EXPLAIN JSON
result = parse_explain_json('{"query_block": {...}}')
print(result["score"])  # 性能评分

# 分析慢查询日志
log = """# Query_time: 5.234193  Lock_time: 0.000089  Rows_sent: 100  Rows_examined: 500000
SELECT * FROM orders WHERE status = 1;"""
result = parse_slow_query_log(log)
print(result["severity"])  # CRITICAL / WARNING / NORMAL

# 生成索引建议
sql = "SELECT * FROM orders WHERE status = 1 AND created_at > '2024-01-01'"
suggestions = generate_index_suggestions(sql)
for s in suggestions:
    print(s)

# 完整分析
report = analyze_slow_query(sql)
print(report["score"])
print(report["index_suggestions"])
print(report["rewrite_suggestions"])
```

## 测试

```bash
python -m pytest tests/test_mysql_slow_query_analyzer.py -v
```

## 定价

- **Free**: 10次/天
- **Pro** (¥19/月): 100次/天 + 慢查询日志分析 + 历史记录
- **Team** (¥49/月): 无限制 + 批量分析 + 导出报告 + 团队共享

## 许可证

MIT License
