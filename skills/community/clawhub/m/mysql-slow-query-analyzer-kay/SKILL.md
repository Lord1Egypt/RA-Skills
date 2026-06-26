# MySQL Slow Query Analyzer / MySQL慢查询分析与优化

## 身份与目标

你是 **MySQL Performance Expert**，专门帮助开发者定位和优化 MySQL 慢查询。

## 触发词

- "慢查询"
- "mysql explain"
- "分析慢查询"
- "slow query"
- "查询优化"
- "mysql 优化建议"
- "索引建议"
- "explain analyze"
- "慢查询日志"

---

## 痛点

- **慢查询难定位**：生产环境慢查询日志动辄数万行，人工分析耗时耗力
- **EXPLAIN 难读懂**：EXPLAIN 输出字段多（15+字段），新手难以判断性能问题
- **索引滥用**：不知道该在哪些列上建索引，或者建了索引却不走
- **重写困难**：知道问题但不知道怎么重写 SQL，ORDER BY + GROUP BY 组合让人头疼

---

## 场景

### 场景1：开发自测
```
开发阶段发现某个接口响应慢，直接把 SQL 发给技能分析
→ 立即知道走没走索引、成本多少、需要什么优化
```

### 场景2：上线前评审
```
DBA 或同事 review SQL，粘贴 EXPLAIN 输出
→ 自动生成优化建议（索引/重写/配置调整）
```

### 场景3：慢查询日志分析
```
从生产环境拉取 slow_query_log，粘贴给技能
→ 自动识别最慢的 TOP N 查询，逐一给出优化方案
```

### 场景4：数据库性能排查
```
数据库 CPU/IO 突然飙升，怀疑有烂 SQL
→ 通过 slow query log 快速定位元凶
```

---

## 核心功能

### 1. MySQL EXPLAIN 解析（支持 JSON / TAB / Traditional 格式）

```
输入: EXPLAIN FORMAT=JSON SELECT ...
输出: 结构化分析报告
  - 查询成本（query_cost）
  - 扫描行数（rows_examined）
  - 索引使用情况（index_used）
  - 连接类型（join_type）
  - 性能评分（0-100）
  - 问题识别 + 优化建议
```

### 2. 慢查询日志分析

```
输入: # Time: 2024-01-01T10:00:00.123456Z
      # Query_time: 5.234193  Lock_time: 0.000089 Rows_sent: 100  Rows_examined: 500000
      SELECT * FROM orders WHERE status = 1;
输出:
  - 查询耗时分级（WARNING / CRITICAL）
  - 扫描行数 vs 返回行数 比值
  - 每行扫描成本
  - 优化建议
```

### 3. 索引建议生成

```
分析维度:
  - WHERE 子句中的列 → 建议建立索引
  - JOIN 连接的列 → 建议建立索引
  - ORDER BY 列 → 建议建立索引
  - GROUP BY 列 → 建议建立索引
  - 联合索引字段顺序建议

输出格式:
  - 建议创建的索引（DROP / ADD）
  - 覆盖索引建议（Using index）
  - 前缀索引建议（长字符串列）
```

### 4. SQL 重写建议

```
支持的场景:
  - SELECT * → 指定列名
  - OR → UNION 重写
  - NOT IN → NOT EXISTS
  - 子查询 → JOIN 重写
  - DISTINCT 优化
  - LIMIT offset 大 → 游标分页
  - 隐式类型转换修复
```

### 5. 性能指标计算

```
输出指标:
  - 查询成本评分（0-100，>70 需优化）
  - 扫描效率（rows_examined / rows_sent）
  - 每秒扫描行数估算
  - 索引命中率
  - 全表扫描检测
```

---

## 输出格式示例

### EXPLAIN 分析结果

```
📊 MySQL EXPLAIN 分析报告

🎯 查询成本: 12450.35
📦 扫描行数: 50,000
📨 返回行数: 100
⚡ 扫描效率: 500:1 (较差，每500行才返回1行)

🔍 执行计划:
  - 类型: ALL (全表扫描) ⚠️
  - 索引: NULL
  - 键: NULL
  - 行长度: 256
  - Extra: Using filesort ⚠️

⚠️ 性能问题:
  - 🔴 全表扫描，50,000行数据全部扫描
  - 🔴 Using filesort，ORDER BY 未走索引
  - 🟡 隐式类型转换：status = '1' (字符串 vs 数字)

💡 优化建议:
  1. 🔧 在 orders.status 列建立索引
  2. 🔧 在 orders(created_at, status) 建立联合索引消除 filesort
  3. 🔧 将 status = '1' 改为 status = 1 避免类型转换
  4. 🔧 用 EXPLAIN FORMAT=JSON 查看真实成本
```

### 慢查询日志分析

```
🐌 慢查询分析

⏱️ 查询时间: 5.23s (🔴 CRITICAL > 5s)
🔒 锁等待: 0.09ms
📊 扫描行数: 500,000
📨 返回行数: 100
📈 效率比: 5000:1 (极差)

💡 优化建议:
  1. 🔧 orders.status 列缺少索引 → 添加 INDEX idx_status (status)
  2. 🔧 查询返回100行却扫描50万行 → 检查是否有合适索引
  3. 🔧 考虑在 status + created_at 上建立联合索引
```

---

## 定价

- **Free**: 10次/天（EXPLAIN 解析）
- **Pro** (¥19/月): 100次/天 + 慢查询日志分析 + 历史记录
- **Team** (¥49/月): 无限制 + 批量分析 + 导出报告 + 团队共享

---

## 技术实现

- **Python 3.10+** 标准库为主，无外部依赖（纯正则 + 内置解析）
- **支持格式**: MySQL EXPLAIN (JSON / TAB / Traditional) + slow query log
- **架构**: 单文件 < 500行，CLI 独立入口
- **纯本地运行**: 不需要网络，不上传任何数据

## 限制

- 不支持存储过程、触发器的 EXPLAIN
- 不支持复杂多语句事务分析
- 索引建议基于启发式规则，不保证最优

---

## 使用示例

### Python API

```python
from mysql_slow_query_analyzer import (
    parse_explain_json,
    parse_explain_text,
    parse_slow_query_log,
    generate_index_suggestions,
    generate_rewrite_suggestions,
    analyze_slow_query,
)

# 解析 EXPLAIN JSON
explain_json = '{"query_block": {"select_id": 1, "cost_info": {"query_cost": "12450.35"}, ...}}'
report = parse_explain_json(explain_json)
print(report)

# 解析慢查询日志
log_entry = """
# Time: 2024-01-01T10:00:00.123456Z
# Query_time: 5.234193  Lock_time: 0.000089 Rows_sent: 100  Rows_examined: 500000
SELECT * FROM orders WHERE status = 1;
"""
report = parse_slow_query_log(log_entry)
print(report)

# 生成索引建议
sql = "SELECT * FROM orders WHERE status = 1 AND created_at > '2024-01-01'"
suggestions = generate_index_suggestions(sql)
print(suggestions)

# 完整分析
report = analyze_slow_query(sql)
print(report)
```

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

# 完整分析（输入 SQL，自动 EXPLAIN 解析 + 建议）
python mysql_slow_query_analyzer.py analyze '<SQL>'
```
