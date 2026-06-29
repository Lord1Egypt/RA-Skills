# 金蝶云星空性能优化与调试排错指南

## 目录
- [概述](#概述)
- [插件层性能优化](#插件层性能优化)
- [SQL 层性能优化](#sql层性能优化)
- [数据库死锁与阻塞排查](#数据库死锁与阻塞排查)
- [日志分析](#日志分析)
- [Dump 与内存分析](#dump与内存分析)
- [插件冲突排查](#插件冲突排查)
- [常见性能问题](#常见性能问题)

---

## 概述

星空二次开发中，性能问题通常来自：

- 插件中加载了过多字段或数据
- 在循环中反复查询数据库
- SQL 缺少索引或写法不当
- 数据库死锁、阻塞
- 多个插件执行顺序冲突

## 插件层性能优化

### 1. 最小化加载字段

操作插件默认只加载部分字段，必须显式声明：

```csharp
public override void OnPreparePropertys(PreparePropertysEventArgs e)
{
    base.OnPreparePropertys(e);
    e.FieldKeys.Add("FBillNo");
    e.FieldKeys.Add("FMaterialId");
    e.FieldKeys.Add("FQty");
    e.FieldKeys.Add("FPrice");
    e.FieldKeys.Add("FAmount");
}
```

不要一次性加载所有字段，尤其是基础资料引用字段会触发额外的多语言查询。

### 2. 避免循环查库

```csharp
// 错误：每条明细都查一次库存
foreach (DynamicObject row in entryRows)
{
    long materialId = (row["FMaterialId"] as DynamicObject)?["Id"] as long? ?? 0;
    decimal stockQty = GetStockQty(materialId); // 每次循环查库
}

// 正确：先批量查询，再内存匹配
var materialIds = entryRows
    .Select(r => (r["FMaterialId"] as DynamicObject)?["Id"] as long? ?? 0)
    .Where(id => id > 0)
    .Distinct()
    .ToList();

Dictionary<long, decimal> stockQtyDict = BatchGetStockQty(materialIds);

foreach (DynamicObject row in entryRows)
{
    long materialId = (row["FMaterialId"] as DynamicObject)?["Id"] as long? ?? 0;
    if (stockQtyDict.ContainsKey(materialId))
    {
        row["FStockQty"] = stockQtyDict[materialId];
    }
}
```

### 3. 缓存频繁使用的基础资料

```csharp
private static Dictionary<string, long> _materialCache = new Dictionary<string, long>();

private long GetMaterialIdByNumber(string number)
{
    if (_materialCache.ContainsKey(number))
    {
        return _materialCache[number];
    }

    var material = BusinessDataServiceHelper.LoadSingle(
        this.Context,
        "BD_Material",
        new OQLFilter(new OQLFilterHeadEntityItem
        {
            FilterItems = new List<FilterItem>
            {
                new FilterItem("FNumber", CompareType.Equals, number)
            }
        })
    );

    long id = material?["Id"] as long? ?? 0;
    _materialCache[number] = id;
    return id;
}
```

> 注意：缓存需考虑内存泄漏和多线程问题，生产环境建议使用 `MemoryCache` 并设置过期时间。

### 4. 批量操作接口

WebAPI 调用时，使用批量接口减少网络往返：

```json
POST .../DynamicFormService.BatchSave.common
{
    "formid": "SAL_SaleOrder",
    "BatchCount": 4,
    "data": {
        "Model": [
            { /* 单据1 */ },
            { /* 单据2 */ }
        ]
    }
}
```

每批次建议 50-100 条，保存/提交/审核分开执行。

## SQL 层性能优化

### 1. 索引优化

对高频查询字段建立索引：

```sql
-- 销售订单常用查询字段
CREATE INDEX IX_T_SAL_ORDER_FDATE_FORGID ON T_SAL_ORDER(FDATE, FORGID);
CREATE INDEX IX_T_SAL_ORDER_FBILLNO ON T_SAL_ORDER(FBILLNO);

-- 明细表关联字段
CREATE INDEX IX_T_SAL_ORDERENTRY_FID ON T_SAL_ORDERENTRY(FID);
```

### 2. 避免索引失效

```sql
-- 错误：函数包装导致索引失效
WHERE YEAR(FDATE) = 2024

-- 正确：范围查询
WHERE FDATE >= '2024-01-01' AND FDATE < '2025-01-01'

-- 错误：前导通配符
WHERE FNAME LIKE '%测试%'

-- 正确：后缀通配符
WHERE FNAME LIKE '测试%'
```

### 3. 大查询加分页

```sql
-- 只取前 100 条
SELECT TOP 100 h.FBILLNO, h.FDATE
FROM T_SAL_ORDER h
WHERE h.FDATE >= @BeginDate
ORDER BY h.FDATE DESC;

-- 或 OFFSET/FETCH 分页（SQL Server 2012+）
SELECT h.FBILLNO, h.FDATE
FROM T_SAL_ORDER h
WHERE h.FDATE >= @BeginDate
ORDER BY h.FDATE DESC
OFFSET 0 ROWS FETCH NEXT 100 ROWS ONLY;
```

### 4. 多语言表关联

```sql
-- 正确：关联条件中同时包含 FLOCALEID=2052
SELECT t1.FNUMBER, t2.FNAME
FROM T_BD_MATERIAL t1
LEFT JOIN T_BD_MATERIAL_L t2 ON t2.FMATERIALID = t1.FMATERIALID AND t2.FLOCALEID = 2052
```

## 数据库死锁与阻塞排查

### 查找当前阻塞

```sql
SELECT
    blocking_session_id AS BlockingSession,
    session_id AS BlockedSession,
    wait_type,
    wait_time / 1000 AS WaitSeconds,
    SUBSTRING(st.text, (r.statement_start_offset/2)+1, 100) AS BlockedSQL
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) st
WHERE blocking_session_id > 0
ORDER BY wait_time DESC;
```

### 终止阻塞进程

```sql
-- 谨慎使用！先确认是否确实是死锁或长时间阻塞
KILL 55;  -- 55 为阻塞进程的 session_id
```

### 死锁日志分析

开启 SQL Server 死锁跟踪：

```sql
-- 开启死锁跟踪（会记录到错误日志）
DBCC TRACEON (1222, -1);
```

## 日志分析

### 星空日志位置

```
K3Cloud\WebSite\App_Data\Logs\YYYYMMDD.log
K3Cloud\WebSite\App_Data\Logs\Error\YYYYMMDD.log
```

### PowerShell 快速搜索

```powershell
# 搜索今日日志中的异常
$date = Get-Date -Format 'yyyyMMdd'
Select-String -Path "C:\K3Cloud\WebSite\App_Data\Logs\$date.log" -Pattern "Error|Exception|Timeout" -Context 2,5

# 搜索特定单据
Select-String -Path "C:\K3Cloud\WebSite\App_Data\Logs\*.log" -Pattern "SO2024001" | Select-Object -Last 50
```

### 数据库操作日志

```sql
-- 最近操作日志
SELECT TOP 100
    OL.FCREATEDATE,
    U.FNAME AS UserName,
    OL.FOPERATETYPE,
    OL.FBILLNO,
    OL.FFORMID
FROM T_BAS_OPERATIONLOG OL
LEFT JOIN T_SEC_USER U ON U.FID = OL.FUSERID
ORDER BY OL.FCREATEDATE DESC;

-- 系统异常日志
SELECT TOP 100 * FROM T_BAS_EXCEPTIONLOG ORDER BY FCREATEDATE DESC;
```

## Dump 与内存分析

### 抓取 w3wp 进程 Dump

```powershell
# 安装 ProcDump 后执行
procdump -ma -s 5 -n 3 w3wp.exe C:\Dumps\w3wp.dmp
```

### 分析内存占用

使用 WinDbg 或 Visual Studio 分析：

```
!dumpheap -stat
!gcroot <object address>
```

重点关注：
- `DynamicObjectCollection` 是否大量堆积
- 自定义缓存是否未释放
- 事件订阅是否未取消导致对象无法回收

## 插件冲突排查

### 检查插件执行顺序

```sql
-- 查询某单据注册的所有插件
SELECT
    FFORMID,
    FPLUGINTYPE,
    FASSEMBLYNAME,
    FCLASSNAME,
    FSEQ
FROM T_BOS_FORMPLUGIN
WHERE FFORMID = 'SAL_SaleOrder'
ORDER BY FPLUGINTYPE, FSEQ;
```

### 常见冲突

| 现象 | 原因 | 排查 |
|------|------|------|
| 插件不触发 | 注册顺序靠后且被前面插件取消 | 检查所有插件的 `CancelOperation` 设置 |
| 断点不命中 | 注册位置错误 | 确认表单插件/操作插件/列表插件注册位置正确 |
| 数据被覆盖 | 多个插件修改同一字段 | 检查插件执行顺序和字段修改逻辑 |
| 操作变慢 | 多个插件叠加耗时 | 逐个禁用插件排查 |

## 常见性能问题

| 现象 | 可能原因 | 解决 |
|------|----------|------|
| 列表加载慢 | 缺少索引、加载字段过多 | 加索引、优化 `PrepareFilterParameter` |
| 保存/审核转圈 | 操作插件循环查库、事务死锁 | 批量查询、检查死锁 |
| 内存占用高 | 缓存无过期、大数据集加载 | 设置缓存过期、分页加载 |
| WebAPI 超时 | 单批次过大、未分页 | 分批处理、增加超时 |
| 首次加载慢 | IIS 应用池回收、JIT 编译 | 设置固定回收时间、预热 |
