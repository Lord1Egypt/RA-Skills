# SQL 查询示例

> 提能任务项目 - 5 个常用 SQL 查询示例

---

## 📋 示例清单

| 序号 | 查询主题 | 复杂度 | 使用场景 |
|------|----------|--------|----------|
| 1 | 查询所有提能任务及关联 SDC 反馈 | ⭐⭐ | 任务列表展示 |
| 2 | 查询验证产能有偏差的任务 | ⭐⭐⭐ | 偏差分析 |
| 3 | 查询提能任务的审批流水 | ⭐⭐⭐ | 审批进度跟踪 |
| 4 | 统计各状态的提能任务数量 | ⭐ | 数据统计 |
| 5 | 查询被驳回的提能任务及驳回原因 | ⭐⭐ | 问题分析 |

---

## 1️⃣ 查询所有提能任务及关联 SDC 反馈

**场景**：展示任务列表，包含供应商承诺产能信息

```sql
SELECT 
    t.task_id,
    t.task_name,
    t.task_status,
    t.supplier_code,
    t.factory_code,
    t.material_code,
    t.sdc_deadline_date,
    s.promised_sdc,
    s.enhance_cost,
    s.reach_date,
    s.deviation_reason,
    t.created_at
FROM m_capacity_enhance_task t
LEFT JOIN m_capacity_enhance_sdc_feedback s 
    ON t.task_id = s.enhance_task_id
ORDER BY t.created_at DESC;
```

### 查询说明

| 要点 | 说明 |
|------|------|
| 连接方式 | LEFT JOIN（保留无 SDC 反馈的任务） |
| 排序 | 按创建时间倒序 |
| 适用场景 | 任务列表、任务详情页 |

### 扩展：带状态名称

```sql
SELECT 
    t.task_id,
    t.task_name,
    CASE t.task_status
        WHEN 0 THEN '待发布'
        WHEN 1 THEN '调研中'
        WHEN 2 THEN '任务取消'
        WHEN 3 THEN '待审批 SDC'
        WHEN 4 THEN 'SDC 驳回'
        WHEN 5 THEN '待反馈验证产能'
        WHEN 6 THEN '待审批验证产能'
        WHEN 7 THEN '验证产能驳回'
        WHEN 8 THEN '验证产能有偏差'
        WHEN 9 THEN '无效提能'
        WHEN 10 THEN '偏差关闭'
        WHEN 11 THEN '提能完成'
        ELSE '未知'
    END AS status_name,
    t.supplier_code,
    s.promised_sdc,
    s.enhance_cost
FROM m_capacity_enhance_task t
LEFT JOIN m_capacity_enhance_sdc_feedback s 
    ON t.task_id = s.enhance_task_id
ORDER BY t.created_at DESC;
```

---

## 2️⃣ 查询验证产能有偏差的任务（含偏差率计算）

**场景**：分析验证产能与承诺产能的偏差情况

```sql
SELECT 
    t.task_id,
    t.task_name,
    t.supplier_code,
    t.factory_code,
    s.promised_sdc AS 承诺产能,
    v.verify_capacity AS 验证产能,
    ROUND(
        (v.verify_capacity - s.promised_sdc) / s.promised_sdc * 100, 
        2
    ) AS 偏差率_百分比,
    CASE 
        WHEN v.verify_capacity >= s.promised_sdc THEN '达标'
        WHEN v.verify_capacity >= s.promised_sdc * 0.9 THEN '轻微偏差'
        ELSE '严重偏差'
    END AS 偏差等级,
    v.reach_date AS 实际达产日期,
    s.reach_date AS 计划达产日期
FROM m_capacity_enhance_task t
INNER JOIN m_capacity_enhance_sdc_feedback s 
    ON t.task_id = s.enhance_task_id
INNER JOIN m_capacity_enhance_verify_feedback v 
    ON s.id = v.sdc_feedback_id
WHERE t.task_status IN (8, 10, 11)  -- 有偏差/偏差关闭/完成
    AND s.promised_sdc > 0  -- 避免除零
ORDER BY 偏差率_百分比 ASC;
```

### 查询说明

| 要点 | 说明 |
|------|------|
| 连接方式 | INNER JOIN（只查有验证反馈的任务） |
| 偏差率公式 | (验证产能 - 承诺产能) / 承诺产能 × 100% |
| 偏差等级 | 达标/轻微偏差/严重偏差 |
| 筛选条件 | 任务状态为偏差相关状态 |

### 扩展：按偏差等级统计

```sql
SELECT 
    CASE 
        WHEN v.verify_capacity >= s.promised_sdc THEN '达标'
        WHEN v.verify_capacity >= s.promised_sdc * 0.9 THEN '轻微偏差'
        ELSE '严重偏差'
    END AS 偏差等级,
    COUNT(*) AS 任务数量,
    AVG((v.verify_capacity - s.promised_sdc) / s.promised_sdc * 100) AS 平均偏差率
FROM m_capacity_enhance_task t
INNER JOIN m_capacity_enhance_sdc_feedback s 
    ON t.task_id = s.enhance_task_id
INNER JOIN m_capacity_enhance_verify_feedback v 
    ON s.id = v.sdc_feedback_id
WHERE s.promised_sdc > 0
GROUP BY 偏差等级;
```

---

## 3️⃣ 查询提能任务的审批流水（含最新审批结果）

**场景**：查看任务的审批进度和最新状态

```sql
SELECT 
    t.task_id,
    t.task_name,
    b.approval_type,
    CASE b.approval_type
        WHEN 1 THEN 'SDC 无偏差采购审批'
        WHEN 2 THEN 'SDC 有偏差三方会签'
        WHEN 3 THEN '验证产能 SQE 审批'
        ELSE '未知'
    END AS 审批类型名称,
    b.approval_round AS 审批轮次,
    b.approval_result,
    CASE b.approval_result
        WHEN 0 THEN '处理中'
        WHEN 1 THEN '通过'
        WHEN 2 THEN '驳回'
        WHEN 3 THEN '终止/撤回'
        ELSE '未知'
    END AS 审批结果名称,
    b.process_instance_status AS 流程状态,
    b.created_at AS 审批时间
FROM m_capacity_enhance_task t
INNER JOIN (
    -- 子查询：获取每个任务的最新审批记录
    SELECT 
        enhance_task_id,
        approval_type,
        approval_round,
        approval_result,
        process_instance_status,
        created_at,
        ROW_NUMBER() OVER (
            PARTITION BY enhance_task_id 
            ORDER BY created_at DESC
        ) AS rn
    FROM m_capacity_enhance_bpm_record
) b ON t.task_id = b.enhance_task_id AND b.rn = 1
ORDER BY b.created_at DESC;
```

### 查询说明

| 要点 | 说明 |
|------|------|
| 最新记录 | 使用 ROW_NUMBER() 窗口函数 |
| 分区字段 | PARTITION BY enhance_task_id |
| 排序字段 | ORDER BY created_at DESC |
| 筛选条件 | rn = 1（只取最新一条） |

### 扩展：查询完整审批历史

```sql
SELECT 
    t.task_id,
    t.task_name,
    b.approval_type,
    b.approval_round,
    b.approval_result,
    b.process_instance_status,
    b.bpm_business_key,
    b.created_at
FROM m_capacity_enhance_task t
INNER JOIN m_capacity_enhance_bpm_record b 
    ON t.task_id = b.enhance_task_id
WHERE t.task_id = 'TASK-2026-001'  -- 指定任务
ORDER BY b.created_at DESC;
```

---

## 4️⃣ 统计各状态的提能任务数量

**场景**：数据统计看板，了解任务分布情况

```sql
SELECT 
    t.task_status,
    CASE t.task_status
        WHEN 0 THEN '待发布'
        WHEN 1 THEN '调研中'
        WHEN 2 THEN '任务取消'
        WHEN 3 THEN '待审批 SDC'
        WHEN 4 THEN 'SDC 驳回'
        WHEN 5 THEN '待反馈验证产能'
        WHEN 6 THEN '待审批验证产能'
        WHEN 7 THEN '验证产能驳回'
        WHEN 8 THEN '验证产能有偏差'
        WHEN 9 THEN '无效提能'
        WHEN 10 THEN '偏差关闭'
        WHEN 11 THEN '提能完成'
        ELSE '未知'
    END AS 状态名称,
    COUNT(*) AS 任务数量,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS 占比_百分比
FROM m_capacity_enhance_task t
GROUP BY t.task_status
ORDER BY t.task_status;
```

### 查询说明

| 要点 | 说明 |
|------|------|
| 分组字段 | task_status |
| 占比计算 | 使用窗口函数 SUM() OVER() |
| 排序 | 按状态值排序 |

### 扩展：按时间维度统计

```sql
SELECT 
    DATE_FORMAT(created_at, '%Y-%m') AS 月份,
    task_status,
    CASE task_status
        WHEN 11 THEN '提能完成'
        WHEN 8 THEN '验证产能有偏差'
        WHEN 4 THEN 'SDC 驳回'
        WHEN 2 THEN '任务取消'
        ELSE '其他'
    END AS 状态分类,
    COUNT(*) AS 任务数量
FROM m_capacity_enhance_task
WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY DATE_FORMAT(created_at, '%Y-%m'), task_status
ORDER BY 月份, task_status;
```

---

## 5️⃣ 查询被驳回的提能任务及驳回原因

**场景**：分析问题任务，找出驳回原因

```sql
SELECT 
    t.task_id,
    t.task_name,
    t.supplier_code,
    t.factory_code,
    t.material_code,
    t.task_status,
    CASE t.task_status
        WHEN 4 THEN 'SDC 驳回'
        WHEN 7 THEN '验证产能驳回'
        ELSE '其他'
    END AS 驳回类型,
    s.deviation_reason AS SDC 偏差原因,
    s.enhance_plan AS 提能方案,
    b.approval_result AS 最新审批结果,
    b.process_instance_status AS 流程状态,
    t.created_at AS 任务创建时间
FROM m_capacity_enhance_task t
LEFT JOIN m_capacity_enhance_sdc_feedback s 
    ON t.task_id = s.enhance_task_id
LEFT JOIN (
    SELECT 
        enhance_task_id,
        approval_result,
        process_instance_status,
        ROW_NUMBER() OVER (
            PARTITION BY enhance_task_id 
            ORDER BY created_at DESC
        ) AS rn
    FROM m_capacity_enhance_bpm_record
) b ON t.task_id = b.enhance_task_id AND b.rn = 1
WHERE t.task_status IN (2, 4, 7, 9)  -- 取消/SDC 驳回/验证驳回/无效
ORDER BY t.created_at DESC;
```

### 查询说明

| 要点 | 说明 |
|------|------|
| 驳回状态 | 2(取消), 4(SDC 驳回), 7(验证驳回), 9(无效) |
| 驳回原因 | 来自 sdc_feedback.deviation_reason |
| 最新审批 | 子查询获取最新 BPM 记录 |

### 扩展：驳回原因分析

```sql
SELECT 
    CASE 
        WHEN s.deviation_reason LIKE '%成本%' THEN '成本问题'
        WHEN s.deviation_reason LIKE '%技术%' THEN '技术问题'
        WHEN s.deviation_reason LIKE '%产能%' THEN '产能不足'
        WHEN s.deviation_reason LIKE '%交期%' THEN '交期问题'
        ELSE '其他原因'
    END AS 原因分类,
    COUNT(*) AS 数量,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS 占比
FROM m_capacity_enhance_task t
LEFT JOIN m_capacity_enhance_sdc_feedback s 
    ON t.task_id = s.enhance_task_id
WHERE t.task_status IN (2, 4, 7, 9)
    AND s.deviation_reason IS NOT NULL
GROUP BY 原因分类
ORDER BY 数量 DESC;
```

---

## 📝 使用建议

### 性能优化

1. **索引使用**：确保外键字段有索引
2. **避免全表扫描**：WHERE 条件使用索引字段
3. **分页查询**：大数据量时使用 LIMIT/OFFSET
4. **缓存结果**：统计类查询可定时缓存

### 代码规范

1. **表别名**：使用有意义的别名（t=task, s=sdc, v=verify, b=bpm）
2. **字段前缀**：多表查询时所有字段加表前缀
3. **注释清晰**：复杂查询添加注释说明
4. **格式统一**：SQL 关键字大写，字段小写

---

_最后更新：2026-03-11_
