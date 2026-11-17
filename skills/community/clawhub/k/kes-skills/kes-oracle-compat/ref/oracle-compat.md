# KingbaseES Oracle 兼容模式参考

Oracle兼容模式启用后，KingbaseES接受Oracle语法子集，同时保持标准SQL能力。PL函数始终使用KingbaseES原生语法。

## 1. 模式切换

### 查看当前状态

```sql
-- 查看兼容模式开关
SHOW oracle_compatible;

-- 查看Oracle相关参数
SELECT name, setting FROM sys_config
WHERE name LIKE '%oracle%' OR name LIKE '%kdb%'
ORDER BY name;
```

### 启用兼容模式

```sql
-- 会话级（仅当前连接）
SET oracle_compatible = on;

-- 全局持久化
ALTER SYSTEM SET oracle_compatible = on;
SELECT sys_reload_conf();

-- 需重启的参数检查
SELECT name, context FROM sys_config WHERE name = 'oracle_compatible';
```

### 配置文件

```ini
# kingbase.conf
oracle_compatible = on
```

---

## 2. 语法对照

### 空值处理

| Oracle | KingbaseES标准 | 说明 |
|--------|--------------|------|
| `NVL(col, def)` | `COALESCE(col, def)` | 返回第一个非空值 |
| `NVL2(col, if_not_null, if_null)` | `CASE WHEN col IS NOT NULL THEN if_not_null ELSE if_null END` | 空值分支 |
| `NULLIF(a, b)` | `NULLIF(a, b)` | 相等返回NULL |

```sql
-- Oracle
SELECT NVL(comm, sal * 0.1) FROM emp;

-- KingbaseES标准
SELECT COALESCE(comm, sal * 0.1) FROM emp;

-- 兼容模式两者均可
```

### 条件表达式

```sql
-- Oracle DECODE
SELECT DECODE(dept, 10, '会计', 20, '研发', 30, '销售', '其他') FROM emp;

-- KingbaseES标准
SELECT CASE dept
    WHEN 10 THEN '会计'
    WHEN 20 THEN '研发'
    WHEN 30 THEN '销售'
    ELSE '其他'
END FROM emp;
```

### 层级查询

```sql
-- Oracle CONNECT BY
SELECT empno, ename, mgr, LEVEL
FROM emp
START WITH mgr IS NULL
CONNECT BY PRIOR empno = mgr;

-- KingbaseES标准（WITH RECURSIVE）
WITH RECURSIVE emp_tree AS (
    SELECT empno, ename, mgr, 1 AS lvl
    FROM emp WHERE mgr IS NULL
    UNION ALL
    SELECT e.empno, e.ename, e.mgr, et.lvl + 1
    FROM emp e JOIN emp_tree et ON et.empno = e.mgr
)
SELECT * FROM emp_tree;
```

### 字符串函数

| Oracle | KingbaseES标准 | 说明 |
|--------|--------------|------|
| `SUBSTR(str, start, len)` | `SUBSTRING(str FROM start FOR len)` | 子字符串 |
| `INSTR(str, sub, pos, occ)` | `STRPOS(str, sub)` | 查找位置 |
| `TRIM(str)` / `LTRIM` / `RTRIM` | `TRIM` / `LTRIM` / `RTRIM` | 去空格 |
| `REPLACE(str, old, new)` | `REPLACE(str, old, new)` | 替换 |
| `TRANSLATE(str, from, to)` | 无直接等价，用嵌套REPLACE | 字符映射 |
| `REPLICATE(str, n)` | `REPEAT(str, n)` | 重复字符串 |
| `LTRIM(str, chars)` | `LTRIM(str, chars)` | 去前导字符 |

### 日期函数

| Oracle | KingbaseES标准 | 说明 |
|--------|--------------|------|
| `SYSDATE` | `CURRENT_DATE` 或 `NOW()` | 当前时间 |
| `ADD_MONTHS(d, n)` | `d + (n \|\| ' months')::INTERVAL` | 月份加减 |
| `MONTHS_BETWEEN(d1, d2)` | `EXTRACT(EPOCH FROM age(d1, d2)) / (30*86400)` | 月份差 |
| `LAST_DAY(d)` | `date_trunc('month', d)::DATE + '1 month'::INTERVAL - '1 day'::INTERVAL` | 月末 |
| `NEXT_DAY(d, day)` | `d + ((7 - EXTRACT(DOW FROM d) + day_num) % 7 \|\| ' days')::INTERVAL` | 下个星期X |
| `TRUNC(d, fmt)` | `date_trunc(field, d)` | 日期截断 |
| `TO_CHAR(d, fmt)` | `TO_CHAR(d, fmt)` | 日期格式化（格式符相同） |

### 序列操作

```sql
-- 创建序列
CREATE SEQUENCE emp_seq START WITH 1 INCREMENT BY 1;

-- Oracle: seq.NEXTVAL / seq.CURRVAL
SELECT emp_seq.NEXTVAL;
SELECT emp_seq.CURRVAL;

-- KingbaseES标准: nextval() / currval()
SELECT nextval('emp_seq');
SELECT currval('emp_seq');

-- 设置序列值
SELECT setval('emp_seq', 100);        -- 当前值=100，下次NEXTVAL返回101
SELECT setval('emp_seq', 100, true);  -- 同上行

-- 序列关联列
ALTER TABLE emp ALTER COLUMN empno SET DEFAULT nextval('emp_seq');
ALTER SEQUENCE emp_seq OWNED BY emp.empno;
```

### 分页

```sql
-- Oracle ROWNUM
SELECT * FROM (
    SELECT ROWNUM r, t.* FROM emp t WHERE ROWNUM <= 20
) WHERE r > 10;

-- KingbaseES标准
SELECT * FROM emp LIMIT 20 OFFSET 10;

-- 键集分页（推荐）
SELECT * FROM emp
WHERE id > :last_id
ORDER BY id
LIMIT 20;
```

### 双引号标识符

```sql
-- 标准模式：无引号→小写
CREATE TABLE my_table (id INT);      -- 实际名: my_table
CREATE TABLE "MyTable" ("Id" INT);   -- 实际名: MyTable, Id

-- Oracle兼容模式：无引号→大写
SET oracle_compatible = on;
CREATE TABLE my_table (id INT);      -- 实际名: MY_TABLE, ID
CREATE TABLE "MyTable" ("Id" INT);   -- 实际名: MyTable, Id
```

### DUAL表

```sql
-- Oracle
SELECT SYSDATE FROM DUAL;
SELECT 1 + 1 FROM DUAL;

-- KingbaseES：DUAL可用，但也支持省略
SELECT NOW();
SELECT 1 + 1;
```

### PLUS连接（外连接）

```sql
-- Oracle (+) 语法
SELECT e.ename, d.dname
FROM emp e, dept d
WHERE e.dept_id(+) = d.id;

-- KingbaseES标准
SELECT e.ename, d.dname
FROM dept d LEFT JOIN emp e ON e.dept_id = d.id;
```

---

## 3. 数据类型映射

### Oracle → KingbaseES 类型对照

| Oracle类型 | KingbaseES等价 | 说明 |
|-----------|--------------|------|
| `VARCHAR2(n)` | `VARCHAR(n)` | 兼容模式可直接用VARCHAR2 |
| `NVARCHAR2(n)` | `VARCHAR(n)` |  Unicode字符串 |
| `NUMBER` | `NUMERIC` | 精确数值 |
| `NUMBER(p, s)` | `NUMERIC(p, s)` | 精度p, 标度s |
| `NUMBER(p)` | `NUMERIC(p)` | 整数 |
| `NUMBER(*, s)` | `NUMERIC(38, s)` | 可变精度 |
| `FLOAT(n)` | `DOUBLE PRECISION` | n≤126时 |
| `RAW(n)` | `BYTEA` | 二进制数据 |
| `LONG RAW` | `BYTEA` | 长二进制 |
| `DATE` | `DATE` 或 `TIMESTAMP` | Oracle DATE含时间部分 |
| `TIMESTAMP` | `TIMESTAMP` | 时间戳 |
| `TIMESTAMP WITH TIME ZONE` | 同名 | 带时区 |
| `CLOB` | `TEXT` 或 `CLOB` | 大文本 |
| `BLOB` | `BYTEA` 或 `BLOB` | 大二进制 |
| `BFILE` | 不支持 | 外部二进制文件 |
| `ROWID` | `CTID` | 行标识符 |
| `UROWID` | 不支持 | 通用行标识 |
| `XMLTYPE` | `XML` | XML数据 |
| `JSON` | `JSON` / `JSONB` | JSON数据 |

### 自增列

```sql
-- Oracle IDENTIFIED BY
CREATE TABLE emp (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY,
    name VARCHAR2(100)
);

-- KingbaseES等价方式1: SERIAL
CREATE TABLE emp (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);

-- KingbaseES等价方式2: GENERATED ALWAYS
CREATE TABLE emp (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100)
);

-- Oracle风格（兼容模式支持）
CREATE TABLE emp (
    id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR2(100)
);
```

### BOOLEAN

```sql
-- Oracle无原生BOOLEAN，用NUMBER(1)替代
-- KingbaseES支持原生BOOLEAN
CREATE TABLE flags (
    is_active BOOLEAN DEFAULT true,
    flag_flag SMALLINT  -- Oracle风格: 0/1
);
```

---

## 4. 特殊操作符

### 空值合并操作符

```sql
-- Oracle ||| (KingbaseES兼容模式)
SELECT col ||| 'default' FROM t;

-- KingbaseES标准
SELECT COALESCE(col, 'default') FROM t;
```

### 连接操作符

```sql
-- 两者都支持 ||
SELECT first_name || ' ' || last_name FROM emp;
```

### 正则表达式

| Oracle | KingbaseES | 说明 |
|--------|-----------|------|
| `REGEXP_LIKE(str, pat)` | `str ~ pat` 或 `REGEXP_LIKE(str, pat)` | 匹配 |
| `REGEXP_INSTR(str, pat)` | `REGEXP_INSTR(str, pat)` | 查找位置 |
| `REGEXP_REPLACE(str, pat, rep)` | `REGEXP_REPLACE(str, pat, rep)` | 替换 |
| `REGEXP_SUBSTR(str, pat)` | `REGEXP_SUBSTR(str, pat)` | 提取子串 |

### 层次操作符

```sql
-- Oracle PRIOR
CONNECT BY PRIOR empno = mgr

-- KingbaseES：使用WITH RECURSIVE，见上文层级查询
```

---

## 5. 系统视图兼容

### Oracle视图映射

| Oracle视图 | KingbaseES等价 | 说明 |
|-----------|--------------|------|
| `all_tables` | `sys_all_tables` | 可访问的表 |
| `all_tab_columns` | `sys_all_tab_columns` | 可访问的列 |
| `all_indexes` | `sys_all_indexes` | 可访问的索引 |
| `all_ind_columns` | `sys_all_ind_columns` | 索引列 |
| `all_constraints` | `sys_all_constraints` | 约束信息 |
| `all_users` | `sys_user` | 用户列表 |
| `dba_tables` | `sys_stat_user_tables` | 表统计 |
| `v$session` | `sys_stat_activity` | 会话信息 |
| `v$parameter` | `sys_config` | 配置参数 |
| `v$instance` | `sys_database_system_tablespace` | 实例信息 |
| `user_tables` | `sys_stat_user_tables` | 当前用户表 |
| `user_tab_columns` | `sys_stat_user_columns` | 当前用户列 |
| `user_indexes` | `sys_indexes` | 当前用户索引 |
| `tab` | `sys_tables (schemaname=current_schema)` | 当前模式表 |
| `col` | `sys_tab_columns` | 列信息 |

### 查询示例

```sql
-- 查看当前用户表
SELECT table_name, num_rows, blocks FROM user_tables;

-- 查看表结构
SELECT column_name, data_type, data_length, nullable
FROM user_tab_columns
WHERE table_name = 'EMP';

-- 查看索引
SELECT index_name, table_name, uniqueness
FROM user_indexes
WHERE table_name = 'EMP';
```

---

## 6. 包与程序单元

### 标准包映射

| Oracle包 | KingbaseES等价 | 说明 |
|---------|--------------|------|
| `DBMS_OUTPUT` | `RAISE NOTICE` | 输出调试信息 |
| `DBMS_RANDOM` | `random()`、`gen_random_uuid()` | 随机数 |
| `DBMS_LOCK` | `sys_advisory_lock()` | 咨询锁 |
| `UTL_FILE` | 大对象函数 / `COPY` | 文件操作 |
| `DBMS_UTILITY` | 系统函数 | 工具函数 |
| `DBMS_SCHEDULER` | `sys_cron` 扩展 | 定时任务 |
| `DBMS_SQL` | `EXECUTE IMMEDIATE` | 动态SQL |
| `DBMS_CRYPTO` | `sys_tde_*` 函数 | 加密函数 |

### 游标

```sql
-- Oracle强类型游标
TYPE emp_cur IS REF CURSOR RETURN emp%ROWTYPE;

-- KingbaseES等价
TYPE emp_cur IS REFCURSOR;
-- 或声明游标
DECLARE
    cur CURSOR FOR SELECT * FROM emp;
```

### 异常处理

```sql
-- Oracle
EXCEPTION
    WHEN NO_DATA_FOUND THEN ...
    WHEN TOO_MANY_ROWS THEN ...
    WHEN OTHERS THEN ...

-- KingbaseES
EXCEPTION
    WHEN NO_DATA_FOUND THEN ...
    WHEN TOO_MANY_ROWS THEN ...
    WHEN OTHERS THEN ...
-- 语法完全兼容
```

---

## 7. 迁移注意事项

### 语法差异检查清单

1. **字符串字面量**：Oracle单引号转义用 `''` 或 `q'[]`，KingbaseES用 `''` 或 `E'\'`
2. **空字符串**：Oracle `''` = NULL；KingbaseES标准模式 `''` ≠ NULL（兼容模式下行为一致）
3. **子查询LIMIT**：Oracle不支持TOP/LIMIT子查询；KingbaseES支持 `LIMIT n`
4. **GROUP BY**：Oracle要求SELECT列在GROUP BY中；KingbaseES同
5. **HAVING**：两者语法一致
6. **MERGE**：两者都支持MERGE INTO语法
7. **Flashback**：Oracle有Flashback Query；KingbaseES无直接等价

### 迁移步骤

```sql
-- 1. 启用兼容模式
ALTER SYSTEM SET oracle_compatible = on;
SELECT sys_reload_conf();

-- 2. 创建等价类型
-- VARCHAR2 → VARCHAR, NUMBER → NUMERIC 自动映射

-- 3. 序列迁移
-- seq.NEXTVAL → nextval('seq')
-- 或在兼容模式下直接使用seq.NEXTVAL

-- 4. 层级查询迁移
-- START WITH ... CONNECT BY → WITH RECURSIVE

-- 5. 包迁移
-- DBMS_OUTPUT.PUT_LINE → RAISE NOTICE

-- 6. 验证
-- 检查数据类型、约束、索引是否一致
```

### 性能差异

- **执行计划**：Oracle CBO vs KingbaseES规划器，可能需调整统计信息
- **绑定变量**：KingbaseES使用 `$1, $2`；Oracle使用 `:1, :2`（兼容模式支持`:1`）
- **Hint**：Oracle `/*+ INDEX(t idx) */`；KingbaseES使用 `KDB_HINT_PLAN`（已废弃），推荐调整索引/统计信息
- **并行查询**：KingbaseES支持 `max_parallel_workers_per_gather`

---

## 8. 常见迁移问题

### 问题1：日期类型差异

**现象**：Oracle DATE包含时间，KingbaseES DATE仅日期。

**解决**：
```sql
-- Oracle: DATE = '2024-01-01 12:00:00'
-- KingbaseES: 使用TIMESTAMP
ALTER TABLE t ALTER COLUMN col_date TYPE TIMESTAMP;

-- 或保持DATE，只存日期部分
UPDATE t SET col_date = col_date::DATE;
```

### 问题2：序列引用

**现象**：`seq.NEXTVAL`语法报错。

**解决**：
```sql
-- 确保兼容模式已启用
SHOW oracle_compatible;

-- 如未启用，使用标准语法
SELECT nextval('seq_name');
```

### 问题3：标识符大小写

**现象**：兼容模式下表名找不到。

**解决**：
```sql
-- 兼容模式无引号→大写
-- 标准模式无引号→小写
-- 迁移时统一使用小写无引号，或启用兼容模式
```

### 问题4：ROWNUM限制

**现象**：ROWNUM子查询报错。

**解决**：
```sql
-- 改用LIMIT/OFFSET
SELECT * FROM emp LIMIT 10;

-- 分页
SELECT * FROM emp LIMIT 20 OFFSET 10;
```

### 问题5：DECODE性能

**现象**：DECODE改写为CASE后性能下降。

**解决**：
```sql
-- 确保CASE分支有序，最常见值放前面
-- 考虑创建函数索引
CREATE INDEX idx ON t((CASE WHEN col = 'A' THEN 1 WHEN col = 'B' THEN 2 ELSE 3 END));
```

---

## 9. 快速参考卡

### 最常用的Oracle→KingbaseES替换

```sql
-- 空值
NVL(x, y)          → COALESCE(x, y)
NVL2(x, a, b)      → CASE WHEN x IS NOT NULL THEN a ELSE b END

-- 条件
DECODE(x, a, b, c) → CASE WHEN x=a THEN b ELSE c END

-- 层级
START WITH ... CONNECT BY  → WITH RECURSIVE ...

-- 序列
seq.NEXTVAL         → nextval('seq')
seq.CURRVAL         → currval('seq')

-- 分页
ROWNUM <= N         → LIMIT N

-- 日期
SYSDATE             → NOW() 或 CURRENT_DATE
ADD_MONTHS(d, n)    → d + (n || ' months')::INTERVAL
TRUNC(d, 'MM')      → date_trunc('month', d)

-- 连接
e.col(+) = d.col    → LEFT JOIN ... ON

-- 类型
VARCHAR2(n)         → VARCHAR(n)
NUMBER(p,s)         → NUMERIC(p,s)
RAW(n)              → BYTEA
```
