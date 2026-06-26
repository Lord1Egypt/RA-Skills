# ORM 映射

> 来源: Java开发手册（嵩山版）— 五(四) ORM 映射

## 【强制】规则

### 1. 禁止 SELECT *

需要哪些字段必须明确写明。

> **说明**: 增加解析成本、增减字段与 resultMap 不一致、无用字段增加网络消耗。

### 2. POJO 布尔属性不加 is

数据库字段加 `is_`，在 `resultMap` 中进行映射。

### 3. 用 resultMap 不用 resultClass

即使类属性名与数据库字段一一对应，也需要定义 `<resultMap>`。每个表必然有一个 `<resultMap>`。

### 4. 用 #{} 不用 ${}

sql.xml 配置参数使用 `#{}`。`${}` 容易出现 SQL 注入。

### 5. 不用 queryForList(start, size)

其实现是在数据库取到所有记录后再 subList，性能差。

> **正例**: 使用 Map 传入 start/size，在 SQL 中用 LIMIT 分页。

### 6. 不用 HashMap/HashTable 作为结果集输出

数据库版本不同可能导致类型解析不一致（如 bigint 解析为 Long 或 BigInteger）。

### 7. 更新时同步 update_time

更新数据表记录时，必须同时更新 `update_time` 为当前时间。

## 【推荐】规则

### 8. 不要大而全的更新接口

不要不管目标字段都 `update table set c1=v1, c2=v2, c3=v3`。不更新无改动的字段。

## 【参考】

### 9. 事务不滥用

`@Transactional` 影响 QPS，需考虑缓存回滚、消息补偿等回滚方案。

### 10. MyBatis 动态标签

- `<isEqual>`: compareValue 相等时带上条件
- `<isNotEmpty>`: 不为空且不为 null 时执行
- `<isNotNull>`: 不为 null 时执行
