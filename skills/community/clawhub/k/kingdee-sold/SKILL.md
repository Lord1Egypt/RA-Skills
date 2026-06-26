---
name: kingdee-sold
name_cn: 金蝶ERP SOLD数据库查询
description: 金蝶EAS Cloud ERP系统数据库SQL查询技能，支持采购、销售、库存、财务等模块的单据查询和数据分析。
category: domain
tags: ["kingdee", "金蝶", "ERP", "SQL", "PostgreSQL", "数据库", "EAS"]
version: "1.0.0"
author: "Hermes Agent"
created: "2026-04-27"
---

# 金蝶ERP SOLD数据库查询技能

## 技能概述

本技能用于金蝶EAS Cloud ERP系统的PostgreSQL数据库查询，支持各类业务单据的SQL查询、数据分析、表结构探查等操作。

## 数据库连接信息

```
主机: 111.198.79.26
端口: 5432
用户: cosmic
密码: Kd1234567890!
数据库: yyzl202501
```

## 表命名规范

| 前缀/后缀 | 说明 | 示例 |
|----------|------|------|
| `t_` | 业务数据表前缀 | `t_ap_finapbill` |
| `_l` | 分录表后缀 | `t_ap_finapbill_l` |
| `_r3` | R3视图后缀 | `t_im_purinbill_r3` |
| `_lk` | Link关联表 | `t_po_purorder_lk` |
| `_tc` | 临时表 | |
| `_wb` | 工作流相关表 | |
| `t_bos_` | BOS平台表 | `t_bos_atomicincr_generator` |
| `t_gl_` | 财务总账模块 | `t_gl_voucher` |
| `t_ap_` | 应付模块 | `t_ap_paybill` |
| `t_ar_` | 应收模块 | `t_ar_receivebill` |
| `t_im_` | 库存模块 | `t_im_purinbill` |
| `t_po_` | 采购模块 | `t_po_purorder` |
| `t_sal_` | 销售模块 | `t_sal_saleorder` |
| `t_bd_` | 基础资料 | `t_bd_material` |

## 常用标准字段

| 字段名 | 说明 |
|--------|------|
| `fid` | 单据主键ID |
| `fnumber` | 单据编号 |
| `fcreate_time` | 创建时间 |
| `fcreatorid` | 创建人ID |
| `fmodify_time` | 修改时间 |
| `fmodifierid` | 修改人ID |
| `fdocumentstatus` | 单据状态 |
| `fbilltype` | 单据类型 |
| `fdate` | 单据日期 |
| `famount` | 金额 |
| `famt_lc` | 本币金额 |

## 单据状态码说明

| 状态码 | 说明 |
|--------|------|
| 0 | 草稿 |
| 1 | 已提交/审核中 |
| 2 | 已审核 |
| 3 | 已驳回 |
| 4 | 已关闭 |
| 5 | 作废/红冲 |

## 使用示例

### 1. 查询表结构

```sql
-- 查询表的列信息
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 't_po_purorder' 
ORDER BY ordinal_position;
```

### 2. 查询采购订单

```sql
-- 查询采购订单表头
SELECT fid, fnumber, fdate, famount_lc, fdocumentstatus
FROM t_po_purorder
WHERE fdate >= '2025-01-01'
LIMIT 100;

-- 查询采购订单分录
SELECT fid, fentryid, fmaterialid, fqty, fprice, famount
FROM t_po_purorder_l
WHERE fid = '订单fid';
```

### 3. 查询销售订单

```sql
SELECT fid, fnumber, fdate, fcustid, famount_lc, fdocumentstatus
FROM t_sal_saleorder
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;
```

### 4. 查询应付付款单

```sql
SELECT fid, fnumber, fdate, famount_lc, fpaytype, fdocumentstatus
FROM t_ap_paybill
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;
```

### 5. 查询应收收款单

```sql
SELECT fid, fnumber, fdate, famount_lc, fdocumentstatus
FROM t_ar_receivebill
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;
```

### 6. 查询入库单

```sql
SELECT fid, fnumber, fdate, fstockorgid, fdocumentstatus
FROM t_im_purinbill
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;
```

### 7. 查询编码规则

```sql
-- 查询所有单据编码规则
SELECT fnumber, fprefix, fformat, fcurrentvalue
FROM t_bos_atomicincr_generator
ORDER BY fnumber;
```

### 8. 模糊搜索表名

```sql
-- 搜索包含指定关键词的表
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
AND table_name LIKE '%keyword%'
ORDER BY table_name;
```

## 常用SQL模板

### 关联查询表头和分录

```sql
SELECT 
    h.fnumber,
    h.fdate,
    h.famount_lc,
    l.fentryid,
    l.fmaterialid,
    l.fqty,
    l.fprice,
    l.famount
FROM t_po_purorder h
LEFT JOIN t_po_purorder_l l ON h.fid = l.fid
WHERE h.fdate >= '2025-01-01'
LIMIT 100;
```

### 按日期统计单据数量和金额

```sql
SELECT 
    DATE(fdate) as bill_date,
    COUNT(*) as bill_count,
    SUM(famount_lc) as total_amount
FROM t_po_purorder
WHERE fdate >= '2025-01-01'
GROUP BY DATE(fdate)
ORDER BY bill_date DESC;
```

### 按状态统计单据

```sql
SELECT 
    CASE fdocumentstatus
        WHEN 0 THEN '草稿'
        WHEN 1 THEN '已提交'
        WHEN 2 THEN '已审核'
        WHEN 3 THEN '已驳回'
        WHEN 4 THEN '已关闭'
        WHEN 5 THEN '作废'
        ELSE '未知'
    END as status_name,
    COUNT(*) as count,
    SUM(famount_lc) as total_amount
FROM t_po_purorder
WHERE fdate >= '2025-01-01'
GROUP BY fdocumentstatus
ORDER BY fdocumentstatus;
```

## 注意事项

1. **大表查询限制**: 生产环境数据量较大，查询时务必加上LIMIT和时间范围条件
2. **避免全表扫描**: 尽量使用fid、fnumber、fdate等有索引的字段作为查询条件
3. **分录表关联**: 分录表使用`_l`后缀，通过fid字段与主表关联
4. **时间格式**: PostgreSQL中日期比较使用标准ISO格式 `'YYYY-MM-DD'`
5. **权限**: 只有只读权限，请勿执行UPDATE/DELETE/DROP等写操作

## 故障排除

### 表不存在
- 检查表名是否正确，是否遗漏了`t_`前缀
- 确认是表头还是分录表（分录表需加`_l`后缀）
- 使用模糊搜索查找正确的表名

### 字段不存在
- 使用`information_schema.columns`查询表的实际列名
- 注意字段大小写（PostgreSQL默认小写）

### 查询太慢
- 增加LIMIT限制返回行数
- 加上时间范围条件
- 使用有索引的字段过滤
- 避免在大表上使用ORDER BY无索引字段
