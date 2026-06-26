-- 金蝶ERP常用SQL查询模板
-- 数据库: PostgreSQL
-- 注意: 所有查询默认加上LIMIT和时间范围

-- ============================================
-- 1. 表结构查询
-- ============================================

-- 查询表的所有列信息
SELECT 
    column_name, 
    data_type, 
    is_nullable,
    character_maximum_length
FROM information_schema.columns 
WHERE table_name = 't_po_purorder' 
  AND table_schema = 'public'
ORDER BY ordinal_position;

-- 搜索包含指定关键词的表
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public'
  AND table_name LIKE '%keyword%'
ORDER BY table_name;

-- 统计表的记录数
SELECT COUNT(*) FROM t_po_purorder;

-- ============================================
-- 2. 采购订单查询
-- ============================================

-- 查询采购订单表头
SELECT 
    fid,
    fnumber,
    fdate,
    fsupplierid,
    fdeptid,
    femployeeid,
    famount_lc,
    fdocumentstatus,
    fcreate_time,
    fcreatorid
FROM t_po_purorder
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;

-- 查询采购订单表头+分录
SELECT 
    h.fnumber,
    h.fdate,
    h.fsupplierid,
    h.famount_lc as total_amount,
    l.fentryid,
    l.fmaterialid,
    l.fqty,
    l.fprice,
    l.famount as entry_amount,
    h.fdocumentstatus
FROM t_po_purorder h
LEFT JOIN t_po_purorder_l l ON h.fid = l.fid
WHERE h.fdate >= '2025-01-01'
ORDER BY h.fdate DESC, l.fentryid
LIMIT 200;

-- 按状态统计采购订单
SELECT 
    CASE fdocumentstatus
        WHEN 0 THEN '草稿'
        WHEN 1 THEN '已提交'
        WHEN 2 THEN '已审核'
        WHEN 3 THEN '已驳回'
        WHEN 4 THEN '已关闭'
        WHEN 5 THEN '作废'
        ELSE '未知:' || fdocumentstatus
    END as status_name,
    COUNT(*) as bill_count,
    SUM(famount_lc) as total_amount
FROM t_po_purorder
WHERE fdate >= '2025-01-01'
GROUP BY fdocumentstatus
ORDER BY fdocumentstatus;

-- ============================================
-- 3. 销售订单查询
-- ============================================

SELECT 
    fid,
    fnumber,
    fdate,
    fcustid,
    fsalerid,
    famount_lc,
    fdocumentstatus
FROM t_sal_saleorder
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;

-- ============================================
-- 4. 应付付款单查询
-- ============================================

SELECT 
    fid,
    fnumber,
    fdate,
    fpaytype,
    fpayeeid,
    famount_lc,
    fdocumentstatus,
    fsettleorgid
FROM t_ap_paybill
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;

-- ============================================
-- 5. 应收收款单查询
-- ============================================

SELECT 
    fid,
    fnumber,
    fdate,
    fpayerid,
    famount_lc,
    fdocumentstatus
FROM t_ar_receivebill
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;

-- ============================================
-- 6. 入库单查询
-- ============================================

SELECT 
    fid,
    fnumber,
    fdate,
    fstockorgid,
    fwarehouseid,
    fdocumentstatus
FROM t_im_purinbill
WHERE fdate >= '2025-01-01'
ORDER BY fdate DESC
LIMIT 100;

-- ============================================
-- 7. 编码规则查询
-- ============================================

SELECT 
    fnumber,
    fprefix,
    fformat,
    fcurrentvalue,
    fstep,
    fdescription
FROM t_bos_atomicincr_generator
ORDER BY fnumber;

-- ============================================
-- 8. 按日期统计
-- ============================================

SELECT 
    DATE(fdate) as bill_date,
    COUNT(*) as bill_count,
    SUM(famount_lc) as total_amount
FROM t_po_purorder
WHERE fdate >= '2025-01-01'
GROUP BY DATE(fdate)
ORDER BY bill_date DESC;

-- ============================================
-- 9. 查询指定单据编号
-- ============================================

SELECT *
FROM t_po_purorder
WHERE fnumber = 'PO202501001';

-- ============================================
-- 10. 查询分录数量大于N的单据
-- ============================================

SELECT 
    h.fid,
    h.fnumber,
    COUNT(l.fentryid) as entry_count
FROM t_po_purorder h
LEFT JOIN t_po_purorder_l l ON h.fid = l.fid
WHERE h.fdate >= '2025-01-01'
GROUP BY h.fid, h.fnumber
HAVING COUNT(l.fentryid) > 5
ORDER BY entry_count DESC
LIMIT 50;
