# 金蝶云星空数据库参考

## 目录
- [表命名规则](#表命名规则)
- [多语言表规则](#多语言表规则)
- [LK关联表规则](#lk关联表规则)
- [核心业务表清单](#核心业务表清单)
- [枚举值查询](#枚举值查询)
- [常用SQL模板](#常用sql模板)
- [数据库操作注意事项](#数据库操作注意事项)

---

## 表命名规则

| 后缀 | 含义 | 示例 |
|------|------|------|
| 无后缀 | 单据头表 | `T_SAL_ORDER` |
| ENTRY | 单据体（明细行）表 | `T_SAL_ORDERENTRY` |
| _L | 多语言表 | `T_BD_MATERIAL_L` |
| _LK | 上下游关联表 | `T_SAL_OUTSTOCKENTRY_LK` |
| FIN | 财务拆分表 | `T_SAL_OUTSTOCKFIN` |
| _A | 辅助属性表 | 部分单据的辅助属性拆分 |

### 单据结构

一张单据通常由以下表组成：
- **主表**（单据头）：FID 为主键
- **明细表**（单据体）：FID 关联主表，FENTRYID 为自身主键
- **拆分表**：FID 关联主表，FENTRYID 关联明细表
- **多语言表**：关联主表/明细表，FLOCALEID 区分语言

---

## 多语言表规则

**核心规则：所有涉及中文名称的字段，必须通过 `_L` 表关联，且 `FLOCALEID=2052`（简体中文）。**

### 关联方式

``sql
-- 取物料编码和名称
SELECT t1.FNUMBER AS 物料编码
      ,t2.FNAME  AS 物料名称
FROM T_BD_MATERIAL t1
LEFT JOIN T_BD_MATERIAL_L t2 ON t2.FMATERIALID = t1.FMATERIALID AND t2.FLOCALEID = 2052
``

### 常用FLOCALEID

| 值 | 语言 |
|----|------|
| 2052 | 简体中文 |
| 1028 | 繁体中文 |
| 1033 | 英语 |

### 常见多语言表

| 主表 | 多语言表 | 关联字段 |
|------|----------|----------|
| T_BD_MATERIAL | T_BD_MATERIAL_L | FMATERIALID |
| T_BD_CUSTOMER | T_BD_CUSTOMER_L | FCUSTID |
| T_BD_SUPPLIER | T_BD_SUPPLIER_L | FSUPPLIERID |
| T_BD_STOCK | T_BD_STOCK_L | FSTOCKID |
| T_BD_DEPARTMENT | T_BD_DEPARTMENT_L | FDEPTID |
| V_BD_SALESMAN | V_BD_SALESMAN_L | FSTAFFID |

---

## LK关联表规则

**LK表用于跟踪上下游单据的关联关系。**

### 字段说明

| 字段 | 含义 |
|------|------|
| FENTRYID | 当前单据明细行的FENTRYID |
| FSID | 上游单据明细行的FENTRYID |
| FSTABLENAME | 上游明细表名 |

### 关联示例

``sql
-- 销售订单 → 发货通知单 → 销售出库单 关联查询
SELECT so.FBILLNO AS 销售订单号
      ,dn.FBILLNO AS 发货通知单号
      ,os.FBILLNO AS 销售出库单号
FROM T_SAL_ORDER so
INNER JOIN T_SAL_ORDERENTRY soe ON soe.FID = so.FID
-- 订单 → 发货通知
LEFT JOIN T_SAL_DELIVERYNOTICEENTRY_LK dn_lk ON dn_lk.FSID = soe.FENTRYID
LEFT JOIN T_SAL_DELIVERYNOTICEENTRY dne ON dne.FENTRYID = dn_lk.FENTRYID
LEFT JOIN T_SAL_DELIVERYNOTICE dn ON dn.FID = dne.FID
-- 发货通知 → 出库
LEFT JOIN T_SAL_OUTSTOCKENTRY_LK os_lk ON os_lk.FSID = dne.FENTRYID
LEFT JOIN T_SAL_OUTSTOCKENTRY ose ON ose.FENTRYID = os_lk.FENTRYID
LEFT JOIN T_SAL_OUTSTOCK os ON os.FID = ose.FID
``

---

## 核心业务表清单

### 销售管理

| 表名 | 说明 |
|------|------|
| T_SAL_ORDER | 销售订单（头） |
| T_SAL_ORDERENTRY | 销售订单（明细） |
| T_SAL_DELIVERYNOTICE | 发货通知单（头） |
| T_SAL_DELIVERYNOTICEENTRY | 发货通知单（明细） |
| T_SAL_OUTSTOCK | 销售出库单（头） |
| T_SAL_OUTSTOCKENTRY | 销售出库单（明细） |
| T_SAL_OUTSTOCKFIN | 销售出库单（财务拆分） |
| T_SAL_RETURNSTOCK | 销售退货单（头） |
| T_SAL_RETURNSTOCKENTRY | 销售退货单（明细） |

### 采购管理

| 表名 | 说明 |
|------|------|
| T_PUR_POORDER | 采购订单（头） |
| T_PUR_POORDERENTRY | 采购订单（明细） |
| T_PUR_RECEIVE | 收料通知单（头） |
| T_PUR_RECEIVEENTRY | 收料通知单（明细） |
| T_PUR_INSTOCK | 采购入库单（头） |
| T_PUR_INSTOCKENTRY | 采购入库单（明细） |

### 应收/应付

| 表名 | 说明 |
|------|------|
| T_AR_RECEIVABLE | 应收单（头） |
| T_AR_RECEIVABLEENTRY | 应收单（明细） |
| T_AP_PAYABLE | 应付单（头） |
| T_AP_PAYABLEENTRY | 应付单（明细） |
| T_AR_RECEIVEBILL | 收款单（头） |
| T_AP_PAYBILL | 付款单（头） |

### 库存管理

| 表名 | 说明 |
|------|------|
| T_STK_INSTOCK | 入库单（头） |
| T_STK_INSTOCKENTRY | 入库单（明细） |
| T_STK_OUTSTOCK | 出库单（头） |
| T_STK_OUTSTOCKENTRY | 出库单（明细） |
| T_STK_MISCELLANEOUS | 其他入库单 |
| T_STK_MISDELIVERY | 其他出库单 |
| T_STK_TRANSFERDIRECT | 直接调拨单 |
| T_STK_INVENTORY | 期末盘点 |

### 基础资料

| 表名 | 说明 |
|------|------|
| T_BD_MATERIAL | 物料 |
| T_BD_MATERIAL_L | 物料多语言 |
| T_BD_CUSTOMER | 客户 |
| T_BD_CUSTOMER_L | 客户多语言 |
| T_BD_SUPPLIER | 供应商 |
| T_BD_SUPPLIER_L | 供应商多语言 |
| T_BD_STOCK | 仓库 |
| T_BD_STOCK_L | 仓库多语言 |
| T_BD_DEPARTMENT | 部门 |
| T_BD_DEPARTMENT_L | 部门多语言 |
| T_BD_STAFF | 员工 |
| T_BD_UNIT | 单位 |
| T_BD_UNIT_L | 单位多语言 |
| V_BD_SALESMAN | 业务员视图 |
| V_BD_SALESMAN_L | 业务员多语言 |

### BOM

| 表名 | 说明 |
|------|------|
| T_BOM_BOM | BOM表 |
| T_BOM_BOMDETAIL | BOM明细 |
| T_BOM_BOMUSAGE | BOM用途 |

---

## 枚举值查询

``sql
-- 查询枚举值
SELECT t0.FID, t0.FENUMID, t0.FVALUE, t1.FNAME
FROM T_BAS_ENUMITEM t0
LEFT JOIN T_BAS_ENUMITEM_L t1 ON t1.FENUMID = t0.FENUMID AND t1.FLOCALEID = 2052
WHERE t0.FENUMID IN (
    SELECT FENUMID FROM T_BAS_FLEXSITEMDETAIL WHERE ...
)

-- 常用枚举
-- 单据状态：A=暂存, B=已提交, C=已审核, D=已关闭
-- 是/否：0=否, 1=是
``

---

## 常用SQL模板

### 查询单据头+明细

``sql
SELECT h.FBILLNO, h.FDATE, h.FNOTE
      ,e.FSEQ, e.FMATERIALID, e.FQTY, e.FPRICE, e.FAMOUNT
FROM T_SAL_ORDER h
INNER JOIN T_SAL_ORDERENTRY e ON e.FID = h.FID
WHERE h.FBILLNO = @BillNo
``

### 查询含多语言的完整单据

``sql
SELECT h.FBILLNO
      ,h.FDATE
      ,cust.FNUMBER AS 客户编码
      ,cust_L.FNAME AS 客户名称
      ,mat.FNUMBER AS 物料编码
      ,mat_L.FNAME AS 物料名称
      ,e.FQTY
      ,e.FPRICE
      ,e.FAMOUNT
FROM T_SAL_ORDER h
INNER JOIN T_SAL_ORDERENTRY e ON e.FID = h.FID
LEFT JOIN T_BD_CUSTOMER cust ON cust.FCUSTID = h.FCUSTOMERID
LEFT JOIN T_BD_CUSTOMER_L cust_L ON cust_L.FCUSTID = cust.FCUSTID AND cust_L.FLOCALEID = 2052
LEFT JOIN T_BD_MATERIAL mat ON mat.FMATERIALID = e.FMATERIALID
LEFT JOIN T_BD_MATERIAL_L mat_L ON mat_L.FMATERIALID = mat.FMATERIALID AND mat_L.FLOCALEID = 2052
WHERE h.FDATE >= @BeginDate AND h.FDATE <= @EndDate
``

### 存货收发存汇总

``sql
SELECT mat.FNUMBER AS 物料编码
      ,mat_L.FNAME AS 物料名称
      ,unit_L.FNAME AS 单位
      ,ISNULL(SUM(CASE WHEN io.FBUSINESSTYPE IN ('1') THEN ie.FQTY ELSE 0 END), 0) AS 收入数量
      ,ISNULL(SUM(CASE WHEN io.FBUSINESSTYPE IN ('2') THEN oe.FQTY ELSE 0 END), 0) AS 发出数量
      ,ISNULL(SUM(CASE WHEN io.FBUSINESSTYPE IN ('1') THEN ie.FQTY ELSE 0 END), 0)
      - ISNULL(SUM(CASE WHEN io.FBUSINESSTYPE IN ('2') THEN oe.FQTY ELSE 0 END), 0) AS 结存数量
FROM T_BD_MATERIAL mat
LEFT JOIN T_BD_MATERIAL_L mat_L ON mat_L.FMATERIALID = mat.FMATERIALID AND mat_L.FLOCALEID = 2052
LEFT JOIN T_BD_UNIT unit ON unit.FUNITID = mat.FBASEUNITID
LEFT JOIN T_BD_UNIT_L unit_L ON unit_L.FUNITID = unit.FUNITID AND unit_L.FLOCALEID = 2052
LEFT JOIN T_STK_INSTOCK io ON ...
LEFT JOIN T_STK_OUTSTOCK oe ON ...
GROUP BY mat.FNUMBER, mat_L.FNAME, unit_L.FNAME
``

### BOM多级展开

``sql
-- 递归查询BOM
WITH BOMTree AS (
    -- 顶层物料
    SELECT b.FID, b.FMATERIALID, d.FMATERIALID AS ChildMaterialId, d.FQTY, 1 AS Level
    FROM T_BOM_BOM b
    INNER JOIN T_BOM_BOMDETAIL d ON d.FID = b.FID
    WHERE b.FMATERIALID = @TopMaterialId

    UNION ALL

    -- 递归展开子件
    SELECT b.FID, b.FMATERIALID, d.FMATERIALID AS ChildMaterialId, d.FQTY, t.Level + 1
    FROM T_BOM_BOM b
    INNER JOIN T_BOM_BOMDETAIL d ON d.FID = b.FID
    INNER JOIN BOMTree t ON t.ChildMaterialId = b.FMATERIALID
)
SELECT t.Level
      ,mat_parent.FNUMBER AS 父件编码
      ,mat_parent_L.FNAME AS 父件名称
      ,mat_child.FNUMBER AS 子件编码
      ,mat_child_L.FNAME AS 子件名称
      ,t.FQTY AS 用量
FROM BOMTree t
LEFT JOIN T_BD_MATERIAL mat_parent ON mat_parent.FMATERIALID = t.FMATERIALID
LEFT JOIN T_BD_MATERIAL_L mat_parent_L ON mat_parent_L.FMATERIALID = mat_parent.FMATERIALID AND mat_parent_L.FLOCALEID = 2052
LEFT JOIN T_BD_MATERIAL mat_child ON mat_child.FMATERIALID = t.ChildMaterialId
LEFT JOIN T_BD_MATERIAL_L mat_child_L ON mat_child_L.FMATERIALID = mat_child.FMATERIALID AND mat_child_L.FLOCALEID = 2052
ORDER BY t.Level, mat_parent.FNUMBER
``

---

## 数据库操作注意事项

1. **禁止直接修改业务数据表** — 通过API或插件操作
2. **查询走只读副本** — 避免影响业务性能
3. **大查询加 TOP** — 防止全表扫描
4. **注意_F后缀字段** — 部分字段存储的是内码，需要关联取名称
5. **DateTime字段** — 比较时注意时间部分，用 `FDATE >= @BeginDate AND FDATE < DATEADD(DAY, 1, @EndDate)`
6. **删除操作** — 业务数据用API删除，不要直接 DELETE
