---
name: openclaw-ddl-creator
description: OpenClaw 数据建表规范与流程指导。当用户需要创建数据仓库表（DDL）时使用，支持 DWS/DWD/DIM/ADS 等层级，引导完成工作空间选择、表命名、字段定义、分区策略、生命周期等完整建表流程。
---

# OpenClaw 建表规范

## 使用流程

当用户需要建表时，按以下顺序确认关键信息：

### 1. 工作空间确认
询问用户要在哪个工作空间（Schema/数据库）建表：
- 生产环境：`prod_workspace`
- 测试环境：`test_workspace`
- 开发环境：`dev_workspace`

### 2. 数据层级与数据域确认

**数据层级**（必选其一）：
| 层级 | 代码 | 说明 |
|------|------|------|
| 数据仓库明细层 | dwd | 清洗后的明细数据 |
| 数据仓库汇总层 | dws | 按主题汇总的轻度汇总表 |
| 维度表 | dim | 维度数据（用户、商品等） |
| 应用数据层 | ads | 面向应用的数据集市 |
| 原始数据层 | ods | 原始接入数据 |

**数据域**（根据业务选择）：
- `usr` - 用户域
- `ord` - 订单域
- `prd` - 商品域
- `trd` - 交易域
- `mkt` - 营销域
- `log` - 日志域
- `fin` - 财务域
- 其他自定义域

### 3. 表调度策略确认

| 维度 | 选项 | 代码 |
|------|------|------|
| **调度周期** | 天级 | d |
| | 小时级 | h |
| | 分钟级 | min |
| **更新方式** | 全量 | f |
| | 增量 | i |

**表名拼接规则**：
```
【工作空间】.【数据层】_【数据域】_【业务描述】_【调度周期】【更新方式】
```

**示例**：
- `prod_workspace.dws_ord_daily_order_stats_df` （天级全量）
- `prod_workspace.dwd_ord_order_detail_di` （天级增量）
- `prod_workspace.dws_usr_user_active_hf
<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
` （小时级）

### 4. 字段定义收集

必须提供以下信息：
- **字段英文名**：蛇形命名（如 `user_id`, `order_amount`）
- **字段中文名**：清晰业务含义
- **数据类型**：STRING/BIGINT/DOUBLE/DATETIME/DECIMAL(p,s) 等

**常用字段模板**：
```sql
-- 基础审计字段（强烈建议）
`gmt_create`    DATETIME COMMENT '数据创建时间',
`gmt_modified`  DATETIME COMMENT '数据修改时间',
`ds`            STRING   COMMENT '数据日期，格式yyyyMMdd',
```

### 5. 表注释
必须提供表级 COMMENT，格式：
```sql
COMMENT '【数据域】_【业务描述】_【调度说明】，【主要字段说明】'
```

### 6. 分区字段

**推荐分区策略**：
| 调度类型 | 分区字段 | 说明 |
|---------|---------|------|
| 天级表 | `ds STRING` | 日期分区，格式 yyyyMMdd |
| 小时级 | `ds STRING, hr STRING` | 日期+小时分区 |
| 全量表 | 可选无分区 | 按业务需要 |

**分区示例**：
```sql
PARTITIONED BY (`ds` STRING COMMENT '数据日期，格式yyyyMMdd')
```

### 7. 存储格式

**默认使用 ALIORC**：
```sql
STORED AS ALIORC
```

特殊情况可选项：
- `STORED AS ALIORC` - 推荐，高压缩率
- `STORED AS TEXTFILE` - 纯文本，调试用

### 8. 生命周期（TTL）

按数据层级设置默认 TTL：
| 层级 | 建议 TTL | 说明 |
|------|---------|------|
| ODS | 30-90 天 | 原始数据短期保留 |
| DWD | 180-365 天 | 明细数据中期保留 |
| DWS | 365-730 天 | 汇总数据长期保留 |
| ADS | 90-365 天 | 应用数据按需保留 |
| DIM | 365 天或无 | 维度表通常长期保留 |

**TTL 语法**：
```sql
TBLPROPERTIES ('lifecycle'='30')
```

---

## 完整建表示例

```sql
CREATE TABLE IF NOT EXISTS prod_workspace.dws_ord_daily_order_stats_df (
    -- 维度字段
    `stat_date`         STRING      COMMENT '统计日期，格式yyyy-MM-dd',
    `merchant_id`       BIGINT      COMMENT '商家ID',
    `merchant_name`     STRING      COMMENT '商家名称',
    `category_id`       BIGINT      COMMENT '类目ID',
    
    -- 指标字段
    `order_cnt`         BIGINT      COMMENT '订单笔数',
    `order_amount`      DECIMAL(18,2) COMMENT '订单金额',
    `paid_cnt`          BIGINT      COMMENT '支付笔数',
    `paid_amount`       DECIMAL(18,2) COMMENT '支付金额',
    `refund_cnt`        BIGINT      COMMENT '退款笔数',
    `refund_amount`     DECIMAL(18,2) COMMENT '退款金额',
    
    -- 衍生指标
    `gmv`               DECIMAL(18,2) COMMENT 'GMV',
    `actual_amt`        DECIMAL(18,2) COMMENT '实际成交金额',
    
    -- 审计字段
    `gmt_create`        DATETIME    COMMENT '数据创建时间',
    `gmt_modified`      DATETIME    COMMENT '数据修改时间'
)
COMMENT '订单域_商家每日订单统计_天级全量，包含订单数、金额、退款等核心指标'
PARTITIONED BY (`ds` STRING COMMENT '数据日期，格式yyyyMMdd')
STORED AS ALIORC
TBLPROPERTIES ('lifecycle'='365');
```

---

## 字段命名规范

### 数据类型后缀（可选但推荐）
| 类型 | 后缀 | 示例 |
|------|------|------|
| 数量/次数 | `_cnt` | `order_cnt`, `pv_cnt` |
| 金额 | `_amt` / `_amount` | `order_amt`, `pay_amount` |
| 比率/比例 | `_rate` / `_ratio` | `conversion_rate` |
| 标识/ID | `_id` | `user_id`, `order_id` |
| 时间 | `_time` | `create_time`, `pay_time` |
| 日期 | `_date` / `_dt` | `stat_date`, `birth_dt` |
| 标记/Flag | `_flag` / `_is_xxx` | `is_vip`, `del_flag` |

### 常见缩写
| 全称 | 缩写 | 示例 |
|------|------|------|
| count | cnt | `order_cnt` |
| amount | amt | `pay_amt` |
| number | num | `serial_num` |
| identifier | id | `user_id` |
| timestamp | ts | `create_ts` |
| datetime | dt | `log_dt` |

---

## 快速核对清单

建表完成后，确认以下事项：
- [ ] 工作空间正确
- [ ] 表名格式符合规范：`{层}_{域}_{业务}_{调度}`
- [ ] 所有字段都有 COMMENT
- [ ] 表有 COMMENT
- [ ] 分区字段已定义（非全量表）
- [ ] 存储格式为 ALIORC
- [ ] TTL 已设置且合理
