---
name: mysql-to-oracle-sql
description: 将 MySQL SQL（尤其是建表 DDL）转换为 Oracle SQL。用户提到“转为oracle”或“转换oracle”，或明确要求把 MySQL 语句改成 Oracle 语句时必须使用此技能。转换时强制执行类型、默认值和主键约束命名规则。
---

# MySQL To Oracle SQL

## Overview

将输入的 MySQL SQL 转换为 Oracle SQL，并严格执行本技能定义的定制规则。

## Conversion Workflow

1. 解析原始 SQL，识别表定义、字段类型、默认值、空值约束和主键定义。
2. 按本技能规则逐项替换类型和默认值表达。
3. 从 `CREATE TABLE` 中移除内联主键定义，改为单独 `ALTER TABLE` 主键语句。
4. 输出最终 Oracle SQL，并附简短变更说明。

## Required Rules

1. 所有字符串类型统一转换为 `NVARCHAR2`。
2. 严禁输出 `DEFAULT ''`（空字符串默认值）。
3. 字段不是 `NOT NULL` 时，显式输出 `DEFAULT NULL`。
4. `BIGINT` 必须转换为 `NUMBER(20)`。
5. 主键必须使用以下格式单独创建：

```sql
ALTER TABLE <TABLE_NAME> ADD CONSTRAINT BWCT_SYS_C######## PRIMARY KEY (<PK_COLUMNS>);
```

约束名规则：前缀固定 `BWCT_SYS_C`，后接 8 位随机数字（`0-9`）。每个主键约束都要使用新的 8 位随机数字。

## Mapping Rules

- `VARCHAR`, `CHAR`, `MEDIUMTEXT`, `TINYTEXT` -> `NVARCHAR2`（按长度能力选择合适长度）
- `BIGINT` -> `NUMBER(20)`
- `INT` -> `NUMBER(10)`
- `SMALLINT` -> `NUMBER(5)`
- `TINYINT` -> `NUMBER(3)`
- `DECIMAL(p,s)` -> `NUMBER(p,s)`
- `DATE`,`DATETIME` -> `DATE`
- `TEXT`, `LONGTEXT` -> `CLOB`

## Default Value Rules

1. 若原字段可空（未声明 `NOT NULL`），输出字段定义时包含 `DEFAULT NULL`。
2. 若原字段为 `NOT NULL` 且有默认值，则保留合法默认值。
3. 若原字段默认值为 `''`，则改为`DEFAULT NULL`；若字段可空，则改为 `DEFAULT NULL`。
4. 若原字段为时间且默认为`DEFAULT CURRENT_TIMESTAMP`时保持默认值不变。

## Output Requirements

1. 输出可直接在 Oracle 执行的 SQL。
2. 每张表先给 `CREATE TABLE`，再给主键 `ALTER TABLE`。
3. 不输出 MySQL 方言（如反引号、`ENGINE=`、`CHARSET=`）。
4. 输出表和所有字段的注释SQL。

## Example

输入（MySQL）：

```sql
CREATE TABLE `user_info` (
  `id` BIGINT NOT NULL COMMENT '主键',
  `name` VARCHAR(100) DEFAULT '' COMMENT '名称',
  `note` TEXT COMMENT '笔记',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB COMMENT='用户信息表';
```

输出（Oracle）：

```sql
CREATE TABLE USER_INFO (
  ID NUMBER(20) NOT NULL,
  NAME NVARCHAR2(100) DEFAULT NULL,
  NOTE CLOB DEFAULT NULL
);

ALTER TABLE USER_INFO ADD CONSTRAINT BWCT_SYS_C02512526 PRIMARY KEY (ID);

COMMENT ON TABLE USER_INFO IS '用户信息表';
COMMENT ON COLUMN USER_INFO.ID IS '主键';
COMMENT ON COLUMN USER_INFO.NAME IS '名称';
COMMENT ON COLUMN USER_INFO.NOTE IS '笔记';
```
