# ODPS SQL 参考指南

> 供 Claude 参考，用于生成正确的 ODPS (MaxCompute) SQL 语句。

---

## 与标准 SQL 的主要差异

| 特性 | 标准 SQL / MySQL | ODPS SQL |
|------|-----------------|----------|
| 字符串连接 | `a || b` 或 `CONCAT(a, b)` | `CONCAT(a, b)` |
| 当前时间 | `NOW()` / `CURRENT_TIMESTAMP` | `GETDATE()` |
| 日期字面量 | `'2024-01-01'` | `TO_DATE('2024-01-01', 'yyyy-mm-dd')` |
| 字符串转数字 | `CAST(x AS INT)` | `CAST(x AS BIGINT)` 或 `TO_NUMBER(x)` |
| 随机数 | `RAND()` | `RAND()` ✓ |
| 正则匹配 | `REGEXP` | `RLIKE` |
| 行号 | `ROW_NUMBER()` | `ROW_NUMBER()` ✓ |
| `IF NULL` | `IFNULL(x, y)` | `NVL(x, y)` |
| 条件表达式 | `IF(cond, t, f)` | `IF(cond, t, f)` ✓ 或 `CASE WHEN ... END` |

---

## 分区表

ODPS 中分区是物理存储隔离单元，**必须**在 `WHERE` 子句中指定分区列以避免全表扫描。

```sql
-- 按日期分区查询（dt 为分区列）
SELECT * FROM dws_order_summary
WHERE dt = '2024-01-01'
LIMIT 100;

-- 多分区列
SELECT * FROM fact_sales
WHERE year = '2024' AND month = '03'
LIMIT 100;

-- 查询分区范围
SELECT * FROM dws_order_summary
WHERE dt >= '2024-01-01' AND dt <= '2024-01-31';
```

### 查看表的分区列表

```sql
SHOW PARTITIONS table_name;
```

---

## 常用日期函数

```sql
-- 当前日期时间
SELECT GETDATE();

-- 日期格式化
SELECT TO_CHAR(GETDATE(), 'yyyy-mm-dd');

-- 字符串转日期
SELECT TO_DATE('2024-01-15', 'yyyy-mm-dd');

-- 日期加减
SELECT DATEADD(GETDATE(), -7, 'dd');   -- 7天前
SELECT DATEADD(GETDATE(), 1, 'mm');    -- 下个月

-- 两日期差值（天数）
SELECT DATEDIFF('2024-01-31', '2024-01-01', 'dd');  -- 返回 30

-- 提取日期部分
SELECT DATEPART(GETDATE(), 'yyyy');  -- 年
SELECT DATEPART(GETDATE(), 'mm');    -- 月
SELECT DATEPART(GETDATE(), 'dd');    -- 日
```

---

## 字符串函数

```sql
-- 长度
SELECT LENGTH('hello');          -- 5
SELECT LENGTHB('中文');          -- 字节长度

-- 截取
SELECT SUBSTR('hello world', 1, 5);   -- 'hello'

-- 去空格
SELECT TRIM('  hello  ');
SELECT LTRIM('  hello');
SELECT RTRIM('hello  ');

-- 大小写
SELECT UPPER('hello');    -- 'HELLO'
SELECT LOWER('HELLO');    -- 'hello'

-- 替换
SELECT REPLACE('hello world', 'world', 'ODPS');

-- 拼接
SELECT CONCAT('hello', ' ', 'world');

-- 分割（返回数组）
SELECT SPLIT('a,b,c', ',');
-- 取分割后第 n 个元素（1-indexed）
SELECT SPLIT_PART('a,b,c', ',', 2);  -- 'b'

-- 正则匹配
SELECT * FROM t WHERE col RLIKE '^[0-9]+$';

-- 正则提取
SELECT REGEXP_EXTRACT('order_12345', 'order_([0-9]+)', 1);  -- '12345'
```

---

## 聚合与窗口函数

```sql
-- 标准聚合
SELECT
    category,
    COUNT(*) AS cnt,
    SUM(amount) AS total,
    AVG(amount) AS avg_amount,
    MAX(amount) AS max_amount,
    MIN(amount) AS min_amount
FROM orders
WHERE dt = '2024-01-01'
GROUP BY category
ORDER BY total DESC;

-- 窗口函数 - 排名
SELECT
    user_id,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rn,
    RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS rank,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS dense_rank
FROM orders
WHERE dt = '2024-01-01';

-- 窗口函数 - 累计/移动
SELECT
    dt,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY dt ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS cumulative_sales,
    AVG(daily_sales) OVER (ORDER BY dt ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS moving_avg_7d
FROM daily_summary;

-- 偏移函数
SELECT
    dt,
    amount,
    LAG(amount, 1) OVER (ORDER BY dt) AS prev_day_amount,
    LEAD(amount, 1) OVER (ORDER BY dt) AS next_day_amount
FROM daily_summary;
```

---

## 常见查询模式

### Top-N 查询

```sql
-- 每个分类下金额最高的前 3 个订单
SELECT * FROM (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rn
    FROM orders
    WHERE dt = '2024-01-01'
) t
WHERE rn <= 3;
```

### 同比/环比

```sql
SELECT
    a.dt,
    a.sales AS current_sales,
    b.sales AS last_year_sales,
    (a.sales - b.sales) / b.sales * 100 AS yoy_growth_pct
FROM daily_sales a
LEFT JOIN daily_sales b
    ON b.dt = DATEADD(TO_DATE(a.dt, 'yyyy-mm-dd'), -1, 'yyyy')
WHERE a.dt >= '2024-01-01' AND a.dt <= '2024-01-31';
```

### 去重计数

```sql
SELECT COUNT(DISTINCT user_id) AS uv FROM orders WHERE dt = '2024-01-01';
```

### NULL 处理

```sql
SELECT NVL(amount, 0) AS amount FROM orders;
SELECT COALESCE(col1, col2, 'default') FROM t;
```

---

## 性能优化建议

1. **始终指定分区列**：避免全表扫描，分区列通常为 `dt`、`year`、`month` 等。
2. **使用 LIMIT**：探索数据时限制返回行数，避免传输大量数据。
3. **先聚合再 JOIN**：尽量减少 JOIN 前的数据量。
4. **避免 `SELECT *`**：只选取需要的列，减少数据传输。
5. **小表放右侧**：在 JOIN 中，将小表放在右侧以便 MapJoin 优化。

```sql
-- 强制 MapJoin（小表广播）
SELECT /*+ MAPJOIN(small_table) */
    a.*,
    b.name
FROM large_table a
JOIN small_table b ON a.id = b.id
WHERE a.dt = '2024-01-01';
```
