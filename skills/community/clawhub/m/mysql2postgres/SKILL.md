---
name: mysql2postgres
description: >
  Use this skill when migrating a project's database layer from MySQL to PostgreSQL.
  Covers SQL dialect conversion (MyBatis XML / raw SQL), ORM configuration (MyBatis-Plus),
  JDBC connection setup, data type pitfalls, and common runtime errors with their fixes.
  Trigger when the user mentions: migrating from MySQL to PG, converting SQL dialects,
  MyBatis XML migration, or any of the specific error patterns listed below.
compatibility: Java / Spring Boot / MyBatis / MyBatis-Plus projects
---

# MySQL → PostgreSQL 迁移 Skill

## 概览

本 Skill 总结了将 Java（Spring Boot + MyBatis/MyBatis-Plus）项目从 MySQL 迁移到 PostgreSQL 的完整经验，涵盖五类核心改动，以及各类运行时报错的根因与修复方法。

---

## 一、JDBC 连接配置

### application.yaml 改动

```yaml
# MySQL（原）
spring.datasource.url: jdbc:mysql://host/dbname
validation-query: SELECT 1 FROM DUAL

# PostgreSQL（改后）
spring.datasource.url: jdbc:postgresql://host/dbname?currentSchema=your_schema
validation-query: SELECT 1
```

**关键点：**
- `currentSchema=your_schema` 指定默认 schema，避免每条 SQL 都加 schema 前缀
- `SELECT 1 FROM DUAL` 是 MySQL/Oracle 方言，PG 直接用 `SELECT 1`

---

## 二、SQL 方言转换速查表（MyBatis XML）

| 类别 | MySQL 写法 | PostgreSQL 写法 | 备注 |
|------|-----------|----------------|------|
| **空值处理** | `IFNULL(a, b)` | `COALESCE(a, b)` | 标准 SQL，推荐 |
| **日期格式化** | `DATE_FORMAT(d, fmt)` | `TO_CHAR(d, fmt)` | 格式符略有差异 |
| **日期加减** | `DATE_ADD(d, INTERVAL 1 DAY)` | `d + INTERVAL '1 day'` | PG 用运算符 |
| **当前日期** | `CURDATE()` | `CURRENT_DATE` | |
| **当前时间** | `NOW()` | `CURRENT_TIMESTAMP` | PG 也支持 `NOW()`，可保留 |
| **类型转换-时间** | `CAST(x AS DATETIME)` | `CAST(x AS TIMESTAMP)` | PG 无 DATETIME 类型 |
| **类型转换-日期** | `DATE(x)` | `CAST(x AS DATE)` | |
| **Upsert-忽略** | `INSERT IGNORE INTO` | `INSERT INTO ... ON CONFLICT DO NOTHING` | |
| **Upsert-更新** | `INSERT ... ON DUPLICATE KEY UPDATE` | `INSERT INTO ... ON CONFLICT (col) DO UPDATE SET ...` | |
| **多表更新** | `UPDATE t1 INNER JOIN t2 ON ... SET t1.col=...` | `UPDATE t1 SET col=... FROM t2 WHERE ...` | 见下方详解 |

### UPDATE JOIN → UPDATE FROM 详解

```sql
-- MySQL
UPDATE orders o
INNER JOIN users u ON o.user_id = u.id
SET o.name = u.name
WHERE o.status = 1;

-- PostgreSQL
UPDATE orders o
SET name = u.name
FROM users u
WHERE o.user_id = u.id
  AND o.status = 1;
```

> **规律：** PG 把 JOIN 的表放到 `FROM` 子句，`WHERE` 里写关联条件。

---

## 三、数据类型陷阱

### BIT(1) 类型与逻辑删除

MySQL 的 `bit(1)` 迁移到 PG 后仍是 `BIT` / `BIT(1)` 类型，但 PG **严格禁止** BIT 与整数直接比较。

**报错：**
```
operator does not exist: bit = integer
```

**两处修复：**

**① MyBatis-Plus 逻辑删除配置（application.yaml）：**
```yaml
# 原（MySQL 兼容）
mybatis-plus.global-config.db-config.logic-delete-value: 1
mybatis-plus.global-config.db-config.logic-not-delete-value: 0

# 改后（PG BIT literal）
mybatis-plus.global-config.db-config.logic-delete-value: "B'1'"
mybatis-plus.global-config.db-config.logic-not-delete-value: "B'0'"
```

**② XML 手写 SQL 中的 deleted 字段：**
```sql
-- MySQL / 错误写法
WHERE deleted = 0
WHERE deleted = 1

-- PostgreSQL 正确写法
WHERE deleted = B'0'
WHERE deleted = B'1'
```

> **⚠️ 注意：** MyBatis-Plus 自动生成的 `deleted=0` 和 XML 里手写的都要改，两处独立，不要遗漏。建议用全局搜索：`deleted = 0` / `deleted = 1`，统计 XML 文件中所有出现位置后批量替换。

---

## 四、自增主键 / Sequence

MySQL 的 `AUTO_INCREMENT` 在 PG 中对应 `SEQUENCE`。

### MyBatis-Plus @KeySequence

```java
// Java DO 类上标注
@KeySequence("demo_entity_seq")
public class DemoEntityDO { ... }
```

运行时 MyBatis-Plus 会执行：
```sql
SELECT nextval('demo_entity_seq')
```

**常见报错：**
```
ERROR: relation "demo_entity_seq" does not exist
```

**修复：在对应 schema 下创建 Sequence：**
```sql
-- 对齐现有数据的最大 ID，避免主键冲突
CREATE SEQUENCE your_schema.demo_entity_seq
  START WITH 10001      -- 从当前最大 id + 1 开始
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;
```

> **最佳实践：** 迁移数据后，用 `SELECT MAX(id) FROM table` 确认最大 ID，再设置 Sequence 的起始值。

---

## 五、GROUP BY 严格模式

PG 严格遵循 SQL 标准：`SELECT` 中所有**非聚合列**必须出现在 `GROUP BY` 中。MySQL 可通过 `sql_mode` 去掉 `ONLY_FULL_GROUP_BY` 来绕过，但 **PG 没有对应的宽容模式**。

**报错：**
```
ERROR: column "d.flag_col" must appear in the GROUP BY clause
or be used in an aggregate function
```

**修复策略：**

| 情况 | 解决方案 |
|------|---------|
| 列的值在组内唯一（由业务保证） | 加入 `GROUP BY` |
| 列是枚举/状态值，取任意值均可 | `MAX(col)` 或 `MIN(col)` |
| 列是标志位，有任意一行满足即为真 | `BOOL_OR(col)` 或 `MAX(col)` |

```sql
-- 原 MySQL 写法（SELECT 了非聚合列）
SELECT o.id, d.flag_col, d.status_col,
       MIN(d.amount_col) as amount_col
FROM demo_order o
LEFT JOIN demo_order_detail d ON o.id = d.order_id
GROUP BY o.id;

-- PG 修复写法
SELECT o.id,
       MAX(d.flag_col) as flag_col,      -- 取最大值
       MAX(d.status_col) as status_col,  -- 有任意在售即为在售
       MIN(d.amount_col) as amount_col
FROM demo_order o
LEFT JOIN demo_order_detail d ON o.id = d.order_id
GROUP BY o.id;
```

---

## 六、包名 / Namespace 重构（MyBatis）

迁移时建议将 MyBatis 的包路径和 namespace 从 `dal.mysql` 改为 `dal.pg`，保持语义清晰。

**涉及的修改点：**
1. `src/main/java` 下的目录：`dal/mysql/` → `dal/pg/`
2. XML 文件中的 `namespace`：`dal.mysql.XxxMapper` → `dal.pg.XxxMapper`
3. Java 文件中的 `import` 语句
4. `application.yaml` 中的日志监控包名配置

---

## 七、迁移检查清单

```
[ ] JDBC URL 改为 PG 格式，指定 currentSchema
[ ] validation-query 去掉 FROM DUAL
[ ] IFNULL → COALESCE（全局搜索替换）
[ ] DATE_FORMAT → TO_CHAR
[ ] DATE_ADD(...INTERVAL) → date + INTERVAL '...'
[ ] CURDATE() → CURRENT_DATE
[ ] CAST(x AS DATETIME) → CAST(x AS TIMESTAMP)
[ ] DATE(x) → CAST(x AS DATE)
[ ] INSERT IGNORE → INSERT ... ON CONFLICT DO NOTHING
[ ] UPDATE ... JOIN → UPDATE ... FROM ... WHERE
[ ] deleted = 0/1 → deleted = B'0'/B'1'（XML 手写 SQL）
[ ] MyBatis-Plus logic-delete-value 改为 B'1' / B'0'
[ ] 为每个 @KeySequence 在 PG 中创建对应 SEQUENCE
[ ] 确认所有 SEQUENCE 起始值 > 表中当前最大 ID
[ ] 检查 GROUP BY：SELECT 中非聚合列必须在 GROUP BY 或用聚合函数包裹
[ ] 包名 / namespace 从 dal.mysql 改为 dal.pg（可选）
```

---

## 八、常见运行时报错速查

| 报错关键词 | 根因 | 修复 |
|-----------|------|------|
| `operator does not exist: bit = integer` | BIT 列与整数比较 | 改为 `B'0'` / `B'1'` |
| `relation "xxx_seq" does not exist` | Sequence 未创建 | 在对应 schema 建 Sequence |
| `must appear in the GROUP BY clause` | SELECT 非聚合列未在 GROUP BY | 加入 GROUP BY 或用聚合函数 |
| `SELECT 1 FROM DUAL` 报错 | DUAL 是 Oracle/MySQL 方言 | 改为 `SELECT 1` |
| `function ifnull does not exist` | IFNULL 是 MySQL 方言 | 改为 `COALESCE` |
| `function date_format does not exist` | DATE_FORMAT 是 MySQL 方言 | 改为 `TO_CHAR` |
