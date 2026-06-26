---
name: lowcode-sql-generator
description: 低代码模块生成器 - SQL初始化语句生成
metadata:
  type: docs
  version: 3.0.0
---

# SQL初始化语句生成

根据字段明细自动生成数据库表初始化SQL语句，支持 Oracle、MySQL、达梦（DM）三种数据库。

## 数据库类型识别

## 数据库类型对比

| 特性 | MySQL     | Oracle | 达梦(DM) |
|-----|-----------|------|------|
| 主键生成 | 后台程序生成    | 后台程序生成 | 后台程序生成 |
| 日期类型 | datetime  | date / timestamp | date / timestamp |
| 字符串 | varchar   | varchar2 | varchar2 |
| 分页 | LIMIT     | ROWNUM / ROW_NUMBER() | ROWNUM / ROW_NUMBER() |
| 空值判断 | IFNULL    | NVL | NVL |
| 字符串截取 | SUBSTRING | SUBSTR | SUBSTR |
| 注释 | COMMENT   | COMMENT | COMMENT |

## SQL生成模板

### 通用字段（所有数据库）

每个表都需要包含以下通用字段：

| 字段名 | 类型 | 说明 | MySQL | Oracle | 达梦 |
|-------|------|-----|-------|--------|------|
| id | Long | 主键（后台程序生成） | BIGINT NOT NULL | NUMBER NOT NULL | NUMBER NOT NULL |
| LAST_UPD_TIME | Date | 最后更新时间 | datetime | DATE | DATE |
| LAST_UPD_USER | String | 最后更新人 | varchar(100) | VARCHAR2(100) | VARCHAR2(100) |
| CREAT_TIME | Date | 创建时间 | datetime DEFAULT CURRENT_TIMESTAMP | DATE DEFAULT SYSDATE | DATE DEFAULT SYSDATE |
| CREATOR | Long | 创建人 | BIGINT | NUMBER | NUMBER |
| LAST_UPD_IP | String | 最后更新IP | varchar(100) | VARCHAR2(100) | VARCHAR2(100) |
| WSDVER | Long | 版本号 | INT | NUMBER | NUMBER |
| TENANT_ID | Long | 租户ID | BIGINT | NUMBER | NUMBER |
| SORT_NUM | Long | 排序号 | INT | NUMBER | NUMBER |

### Java类型到数据库类型映射

| Java类型 | MySQL | Oracle | 达梦 |
|---------|-------|--------|------|
| String | VARCHAR(255) | VARCHAR2(255) | VARCHAR2(255) |
| Integer | INT | INT | INT |
| Long | BIGINT | BIGINT | BIGINT |
| Date | DATETIME | DATE | DATE |
| BigDecimal | DECIMAL(precision,scale) | NUMBER(precision,scale) | NUMBER(precision,scale) |
| Boolean | TINYINT(1) | SMALLINT | SMALLINT |
| byte[] | BLOB | BLOB | BLOB |
| Text | TEXT | CLOB | CLOB |

## MySQL SQL生成

```sql
-- 创建表（主键由后台程序生成，SQL只定义主键列类型）
CREATE TABLE `{tableName}` (
  `ID` BIGINT NOT NULL COMMENT '主键（后台程序生成）',
  {-- 业务字段 --}
  `LAST_UPD_TIME` datetime DEFAULT NULL COMMENT '最后更新时间',
  `LAST_UPD_USER` varchar(100) DEFAULT '' COMMENT '最后更新人',
  `CREAT_TIME` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `CREATOR` BIGINT DEFAULT NULL COMMENT '创建人',
  `LAST_UPD_IP` varchar(100) DEFAULT '' COMMENT '最后更新IP',
  `WSDVER` INT DEFAULT 0 COMMENT '版本号',
  `TENANT_ID` BIGINT DEFAULT NULL COMMENT '租户ID',
  `SORT_NUM` INT DEFAULT 0 COMMENT '排序号',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='{tableComment}';
```

### MySQL示例

```sql
CREATE TABLE `wsd_equipment` (
  `ID` BIGINT NOT NULL COMMENT '主键（后台程序生成）',
  `EQUIPMENT_NAME` VARCHAR(255) NOT NULL COMMENT '设备名称',
  `EQUIPMENT_CODE` VARCHAR(64) DEFAULT NULL COMMENT '设备编号',
  `ORG_ID` BIGINT DEFAULT NULL COMMENT '责任部门',
  `USER_ID` BIGINT DEFAULT NULL COMMENT '责任人',
  `STATUS` VARCHAR(32) DEFAULT NULL COMMENT '设备状态',
  `BUY_DATE` DATE DEFAULT NULL COMMENT '购买日期',
  `DESCRIPTION` TEXT DEFAULT NULL COMMENT '使用说明',
  `LAST_UPD_TIME` datetime DEFAULT NULL COMMENT '最后更新时间',
  `LAST_UPD_USER` varchar(100) DEFAULT '' COMMENT '最后更新人',
  `CREAT_TIME` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `CREATOR` BIGINT DEFAULT NULL COMMENT '创建人',
  `LAST_UPD_IP` varchar(100) DEFAULT '' COMMENT '最后更新IP',
  `WSDVER` INT DEFAULT 0 COMMENT '版本号',
  `TENANT_ID` BIGINT DEFAULT NULL COMMENT '租户ID',
  `SORT_NUM` INT DEFAULT 0 COMMENT '排序号',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备管理';
```

## Oracle SQL生成

```sql
-- 创建表（主键由后台程序生成，SQL只定义主键列类型）
CREATE TABLE "{tableName}" (
  "ID" NUMBER NOT NULL COMMENT '主键（后台程序生成）',
  {-- 业务字段 --}
  "LAST_UPD_TIME" DATE,
  "LAST_UPD_USER" VARCHAR2(100),
  "CREAT_TIME" DATE DEFAULT SYSDATE,
  "CREATOR" NUMBER,
  "LAST_UPD_IP" VARCHAR2(100),
  "WSDVER" NUMBER,
  "TENANT_ID" NUMBER,
  "SORT_NUM" NUMBER,
  PRIMARY KEY ("ID")
);

COMMENT ON TABLE "{tableName}" IS '{tableComment}';
{-- 字段注释 --}
COMMENT ON COLUMN "{tableName}"."ID" IS '主键（后台程序生成）';
```

### Oracle示例

```sql

-- 创建表（主键由后台程序生成）
CREATE TABLE "WSD_EQUIPMENT" (
  "ID" NUMBER NOT NULL COMMENT '主键（后台程序生成）',
  "EQUIPMENT_NAME" VARCHAR2(255) NOT NULL COMMENT '设备名称',
  "EQUIPMENT_CODE" VARCHAR2(64) COMMENT '设备编号',
  "ORG_ID" NUMBER COMMENT '责任部门',
  "USER_ID" NUMBER COMMENT '责任人',
  "STATUS" VARCHAR2(32) COMMENT '设备状态',
  "BUY_DATE" DATE COMMENT '购买日期',
  "DESCRIPTION" CLOB COMMENT '使用说明',
  "LAST_UPD_TIME" DATE,
  "LAST_UPD_USER" VARCHAR2(100),
  "CREAT_TIME" DATE DEFAULT SYSDATE,
  "CREATOR" NUMBER,
  "LAST_UPD_IP" VARCHAR2(100),
  "WSDVER" NUMBER,
  "TENANT_ID" NUMBER,
  "SORT_NUM" NUMBER,
  PRIMARY KEY ("ID")
);

COMMENT ON TABLE "WSD_EQUIPMENT" IS '设备管理';
COMMENT ON COLUMN "WSD_EQUIPMENT"."ID" IS '主键（后台程序生成）';
COMMENT ON COLUMN "WSD_EQUIPMENT"."EQUIPMENT_NAME" IS '设备名称';
```

## 达梦(DM) SQL生成

达梦数据库语法与 Oracle 类似。

```sql
-- 创建表（主键由后台程序生成，SQL只定义主键列类型）
CREATE TABLE "{tableName}" (
  "ID" NUMBER NOT NULL COMMENT '主键（后台程序生成）',
  {-- 业务字段 --}
  "LAST_UPD_TIME" DATE,
  "LAST_UPD_USER" VARCHAR2(100),
  "CREAT_TIME" DATE DEFAULT SYSDATE,
  "CREATOR" NUMBER,
  "LAST_UPD_IP" VARCHAR2(100),
  "WSDVER" NUMBER,
  "TENANT_ID" NUMBER,
  "SORT_NUM" NUMBER,
  PRIMARY KEY ("ID")
);

COMMENT ON TABLE "{tableName}" IS '{tableComment}';
COMMENT ON COLUMN "{tableName}"."ID" IS '主键（后台程序生成）';
```

## SKILL生成流程

```
步骤1：确定数据库类型
    - 检查微服务配置文件中的 driver-class-name
    - 或根据 jdbc url 前缀判断
    ↓
步骤2：解析字段明细
    - 提取字段名（英文）
    - 提取字段类型（Java类型）
    - 提取字段简体中文名（用于注释）
    ↓
步骤3：生成字段SQL
    - Java类型 → 数据库类型
    - 生成列定义
    - 生成注释
    ↓
步骤4：生成完整SQL
    - 加上通用字段（CREATOR, CREAT_TIME 等）
    - 加上主键约束
    - 加上表注释
    ↓
步骤5：输出SQL
    - 根据数据库类型输出对应SQL
```

## 输出位置

生成的SQL文件存放在{microservice}的 db 目录下，只生成一个SQL文件（根据微服务实际连接的数据库类型）：

```
{microservice}/
├── db/
│   └── init.sql        # 根据数据库类型生成对应的SQL
```

## 注意事项

1. **表名前缀**：使用 `{database.tablePrefix}` 配置，如 `wsd_`
2. **字段名转换**：英文转大写（Oracle/达梦）或小写（MySQL）
3. **字符串长度**：根据业务需求设置合适长度，默认255
4. **日期字段**：MySQL用datetime，Oracle/达梦 用date
5. **CLOB/TEXT**：超过4000字符的文本使用CLOB/TEXT类型
