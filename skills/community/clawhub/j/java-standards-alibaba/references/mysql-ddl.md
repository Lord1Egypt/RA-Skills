# MySQL 建表规约

> 来源: Java开发手册（嵩山版）— 五(一) 建表规约

## 【强制】规则

### 1. is_xxx 命名 + tinyint unsigned

表达是与否的字段，必须用 `is_xxx` 命名，数据类型为 `unsigned tinyint`（1 表示是，0 表示否）。

> **说明**: POJO 类布尔变量不加 is 前缀，需在 `<resultMap>` 设置映射关系。

### 2. 小写字母或数字

表名、字段名必须使用小写字母或数字，禁止数字开头，禁止两个下划线中间只出现数字。

> **正例**: `aliyun_admin` / `rdc_config` / `level3_name`

### 3. 表名不用复数

表名仅表示实体内容，不表示数量。

### 4. 禁用保留字

如 `desc`、`range`、`match`、`delayed` 等。

### 5. 索引命名

- 主键索引: `pk_字段名`
- 唯一索引: `uk_字段名`
- 普通索引: `idx_字段名`

### 6. 小数用 decimal

禁止使用 `float` 和 `double`。

### 7. 定长字符串用 char

如果存储的字符串长度几乎相等。

### 8. varchar 长度 ≤ 5000

超过 5000 用 `text` 类型，独立成表。

### 9. 表必备三字段

`id`, `create_time`, `update_time`。

- `id`: 主键，`bigint unsigned`，自增，步长 1
- `create_time`: `datetime`，主动式创建
- `update_time`: `datetime`，被动式更新

## 【推荐】规则

### 10. 表名规范

"业务名称_表的作用"，如 `alipay_task` / `trade_config`

### 11. 库名与应用一致

### 12. 及时更新字段注释

修改字段含义或追加状态时。

### 13. 冗余字段原则

- 不是频繁修改的字段
- 不是唯一索引的字段
- 不是 varchar 超长字段或 text 字段

### 14. 分库分表条件

单表行数 > 500 万 或 单表容量 > 2GB 才推荐。

## 【参考】

### 15. 合适的字符存储长度

| 对象 | 类型 | 范围 |
|------|------|------|
| 人 150 岁内 | `tinyint unsigned` | 0~255 |
| 龟 数百岁 | `smallint unsigned` | 0~65535 |
| 化石 数千万年 | `int unsigned` | 0~43亿 |
| 太阳 约50亿年 | `bigint unsigned` | 0~10^19 |
