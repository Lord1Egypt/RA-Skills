# MySQL SQL 语句

> 来源: Java开发手册（嵩山版）— 五(三) SQL 语句

## 【强制】规则

### 1. count(*) 是标准语法

不要用 `count(列名)` 或 `count(常量)` 替代 `count(*)`。`count(*)` 统计所有行（含 NULL），`count(列名)` 不统计 NULL 行。

### 2. count(distinct col1, col2)

如果其中一列全为 NULL，返回 0。

### 3. sum() 注意 NPE

某一列全是 NULL 时，`sum(col)` 返回 NULL（不是 0）。

> **正例**: `SELECT IFNULL(SUM(column), 0) FROM table;`

### 4. 用 ISNULL() 判断 NULL

> **说明**: `NULL<>NULL` 返回 NULL（不是 false）；`NULL=NULL` 返回 NULL（不是 true）。  
> **正例**: `ISNULL(column)` 是一个整体，简洁易懂。

### 5. count 为 0 直接返回

分页查询中，若 count 为 0 应直接返回，避免执行分页语句。

### 6. 禁止外键与级联

一切外键概念必须在应用层解决。外键不适合分布式、高并发集群。

### 7. 禁止存储过程

难以调试和扩展，没有移植性。

### 8. 数据订正先 select

删除或修改记录时，先 `select` 确认无误再执行。

### 9. 多表操作用表别名限定

> **正例**: `select t1.name from table_first as t1, table_second as t2 where t1.id=t2.id;`

## 【推荐】规则

### 10. 别名命名规范

表别名前加 `as`，以 `t1`、`t2`、`t3` 的顺序命名。

### 11. in 集合 ≤ 1000

in 操作能避免则避免，控制在 1000 个之内。

### 【参考】

### 12. utf8mb4 存表情

所有字符存储采用 utf8 字符集。存储表情用 `utf8mb4`。

> **说明**: `LENGTH("轻松工作")` 返回 12；`CHARACTER_LENGTH("轻松工作")` 返回 4。

### 13. TRUNCATE 谨慎使用

速度快但不触发事务和 trigger，可能造成事故。
