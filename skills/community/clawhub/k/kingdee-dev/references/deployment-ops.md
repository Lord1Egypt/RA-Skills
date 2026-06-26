# 金蝶云星空部署运维

## 目录
- [打包部署流程](#打包部署流程)
- [补丁安装与回滚](#补丁安装与回滚)
- [版本升级（账套升级）](#版本升级账套升级)
- [账套管理与迁移](#账套管理与迁移)
- [IIS配置](#iis配置)
- [数据库维护与备份](#数据库维护与备份)
- [日志查看与排查](#日志查看与排查)
- [常见生产故障处理](#常见生产故障处理)
- [性能优化建议](#性能优化建议)
- [环境监控指标](#环境监控指标)

---

## 打包部署流程

### 1. 创建部署包

1. BOS IDE →「文件」→「打包」→「创建部署包」
2. 选择要打包的对象（单据/插件/报表等）
3. 选择包含的扩展和插件
4. 设置部署包版本号
5. 生成 `.kdbdp` 或 `.zip` 部署包

### 2. 部署到目标环境

1. 目标环境登录管理中心（`http://IP/K3Cloud/ManageCenter.aspx`）
2.「部署」→「安装部署包」
3. 上传部署包
4. 执行安装
5. 重启 IIS

### 3. 自定义插件 dll 部署

```
# 插件 dll 放置位置
K3Cloud\WebSite\bin\

# 替换后必须回收应用池或重启IIS，否则旧dll仍在内存
```

**步骤：**
1. 停止或回收 IIS 应用池（防止文件被占用）
2. 替换 `bin` 目录下的 `.dll` 文件
3. 重启应用池
4. 在 BOS IDE 中确认插件注册有效，重新发布单据

### 4. 打包注意事项

- 打包前确保所有修改已**保存并签入**（未签入的对象不会被打包）
- 目标环境版本需与源环境**主版本兼容**
- 先备份目标环境数据库再安装
- 先在**测试环境**验证，再部署生产

---

## 补丁安装与回滚

### 安装补丁

1. 从官方渠道下载对应版本补丁（官网 / 金蝶社区 / 技术支持）
2. 管理中心 →「补丁管理」→「安装补丁」
3. 上传补丁包（`.zip`）
4. 执行安装前先备份数据库
5. 执行安装
6. 重启 IIS

### 查看当前版本和补丁列表

```sql
-- 查询当前星空版本
SELECT FVALUE FROM T_BAS_SYSTEMPROFILE WHERE FKEY = 'SysVersion'

-- 查询已安装补丁
SELECT * FROM T_BAS_HOTFIXINFO ORDER BY FINSTALLDATE DESC
```

### 常见安装问题

| 问题 | 解决方案 |
|------|----------|
| 安装失败 | https://vip.kingdee.com/article/465831002527655168 |
| 升级失败 | https://vip.kingdee.com/article/474018491821827072 |
| 补丁冲突 | 卸载冲突补丁后重新安装 |
| 版本不兼容 | 确认补丁版本与星空版本匹配 |
| 安装中断 | 恢复数据库备份，重新尝试安装 |

### 补丁回滚

1. 管理中心 →「补丁管理」→「已安装补丁」
2. 选择要回滚的补丁 → 点击「卸载」
3. 重启 IIS
4. 如果数据结构变更，须同时恢复数据库备份

---

## 版本升级（账套升级）

> 版本升级指从低版本星空升级到高版本，如从 7.5 升至 8.x。

### 升级前准备

1. **确认升级路径**：有些版本需逐级升级，不能跨版本跳跃
2. **全量备份**：备份数据库 + `K3Cloud` 整个目录
3. **导出自定义配置**：BOS IDE 导出所有自定义单据/插件
4. **记录第三方集成信息**：WebAPI 账号、自定义服务
5. **通知业务部门**：升级期间停止使用

### 升级步骤

1. 停止 IIS 应用池
2. 备份数据库（完整备份）
3. 下载新版本安装包
4. 运行安装程序（选择升级安装，不要全新安装）
5. 安装完毕后启动 IIS
6. 登录管理中心 →「账套」→「升级账套」
7. 逐一升级每个账套的数据结构
8. 验证功能是否正常

### 升级后检查清单

- [ ] 登录正常，各账套均可访问
- [ ] 核心业务单据（采购/销售/库存/财务）可正常使用
- [ ] 自定义插件是否还能执行（需重新注册或重新编译）
- [ ] 报表数据是否正确
- [ ] 审批流程是否正常触发
- [ ] 第三方接口是否仍可连通
- [ ] 检查日志，无新增 Error 级别异常

### 自定义插件兼容性处理

版本升级后，自定义插件的 BOS API 可能有变动：
1. 重新引用新版本的 BOS `.dll`（从新的 `K3Cloud\WebSite\bin` 拷贝）
2. 对照官方升级说明，修改废弃/变更的 API 调用
3. 重新编译，将新 `.dll` 部署到 `bin` 目录
4. 在 BOS IDE 中重新注册并发布

---

## 账套管理与迁移

### 账套备份与还原（迁移到新服务器）

#### 方法1：数据库备份方式（推荐）

**源服务器操作：**
```sql
-- 1. 备份账套数据库
BACKUP DATABASE [AIS20240101_001]
TO DISK = 'D:\Backup\AIS20240101_001_full.bak'
WITH INIT, COMPRESSION, STATS = 10

-- 2. 备份管理账套（存有账套注册信息）
BACKUP DATABASE [AIS20230101] -- 管理账套名称，通常以 AIS2023 开头
TO DISK = 'D:\Backup\ManageDB_full.bak'
WITH INIT, COMPRESSION, STATS = 10
```

**目标服务器操作：**
```sql
-- 1. 还原账套数据库
RESTORE DATABASE [AIS20240101_001]
FROM DISK = 'D:\Backup\AIS20240101_001_full.bak'
WITH MOVE 'AIS20240101_001' TO 'D:\MSSQL\Data\AIS20240101_001.mdf',
     MOVE 'AIS20240101_001_log' TO 'D:\MSSQL\Log\AIS20240101_001_log.ldf',
     REPLACE, STATS = 10

-- 2. 还原管理账套
RESTORE DATABASE [AIS20230101]
FROM DISK = 'D:\Backup\ManageDB_full.bak'
WITH MOVE ... -- 同上
REPLACE, STATS = 10
```

**管理中心操作：**
1. 管理中心 →「账套」→「注册已有账套」
2. 选择刚还原的数据库
3. 验证账套信息
4. 连接测试

#### 方法2：导出/导入方式

1. 管理中心 →「账套」→「导出账套」→ 生成 `.kdbak` 文件
2. 目标环境：管理中心 →「账套」→「导入账套」

> **注意：** 导出/导入方式数据量大时速度慢，生产环境建议用数据库备份方式

### 修改账套数据库连接

当数据库服务器迁移后，需更新连接信息：
1. 管理中心 →「账套」→「编辑账套」
2. 修改数据库服务器地址
3. 测试连接
4. 保存

### 多账套同服务器部署

星空支持一台服务器部署多个账套，关键是：
- 每个账套对应一个独立数据库
- 所有账套共用一套 IIS 应用（`K3Cloud` 目录）
- 管理中心统一管理所有账套

---

## IIS配置

### 基本配置

| 配置项 | 推荐值 | 说明 |
|--------|--------|------|
| 应用池 .NET 版本 | .NET Framework 4.0（CLR v4.0） | 不要选 No Managed Code |
| 应用池管道模式 | 集成 | Integrated |
| 应用池空闲超时 | 0（不超时） | 避免长时间无操作后重启 |
| 应用池定期回收时间 | 0 或 1740分钟 | 生产环境可选深夜固定时间 |
| 最大工作进程数 | 1（默认） | Web Farm 多节点除外 |
| 启用32位应用程序 | False | 64位系统下必须为 False |
| 最大并发请求 | 按实际调整 | 默认5000 |

### 常用 IIS 管理命令

```batch
:: 完整重启 IIS
iisreset /restart

:: 仅停止/启动
iisreset /stop
iisreset /start

:: 回收指定应用池（不影响其他站点）
%systemroot%\system32\inetsrv\appcmd recycle apppool /apppool.name:"K3CloudAppPool"

:: 查看应用池状态
%systemroot%\system32\inetsrv\appcmd list apppool

:: 查看站点状态
%systemroot%\system32\inetsrv\appcmd list site
```

### 常见IIS问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 503 Service Unavailable | 应用池停止/崩溃 | 检查应用池状态，查看事件查看器 |
| 500 Internal Server Error | .NET 运行时错误 | 查看 `%K3Cloud%\App_Data\Logs` |
| 页面加载慢（首次） | 应用池回收后 JIT 编译 | 设置预热，减少不必要的回收 |
| 上传文件大小限制 | IIS 默认限制 4MB | 修改 web.config |
| 部分用户访问慢 | 并发数不足 / 内存泄漏 | 查监控，必要时增加内存或服务器 |
| 登录后立即掉线 | Session 超时 / 负载均衡 Session 不共享 | 检查 Session 配置 |

### web.config 关键配置

```xml
<configuration>
  <system.web>
    <!-- 最大请求大小（KB），102400 = 100MB -->
    <httpRuntime maxRequestLength="102400" executionTimeout="3600" />
    <!-- Session 超时（分钟） -->
    <sessionState timeout="60" />
  </system.web>
  <system.webServer>
    <security>
      <requestFiltering>
        <!-- 最大请求内容长度（字节），104857600 = 100MB -->
        <requestLimits maxAllowedContentLength="104857600" />
      </requestFiltering>
    </security>
    <!-- 启用 Gzip 压缩 -->
    <urlCompression doStaticCompression="true" doDynamicCompression="true" />
  </system.webServer>
</configuration>
```

---

## 数据库维护与备份

### 备份策略（推荐）

| 备份类型 | 频率 | 保留时间 | 说明 |
|----------|------|----------|------|
| 完整备份 | 每日凌晨 | 7天 | 业务低峰期执行 |
| 差异备份 | 每2小时 | 2天 | 减少恢复时间窗口 |
| 日志备份 | 每15分钟 | 1天 | 满足精确时间点恢复需求 |

### SQL Server 自动备份作业（SQL Agent）

```sql
-- 完整备份脚本（可加入 SQL Agent 作业）
DECLARE @backupPath NVARCHAR(500)
SET @backupPath = 'D:\Backup\AIS20240101_' + CONVERT(NVARCHAR(8), GETDATE(), 112) + '.bak'

BACKUP DATABASE [AIS20240101_001]
TO DISK = @backupPath
WITH INIT,
     NAME = 'Full Backup',
     COMPRESSION,
     CHECKSUM,
     STATS = 10

-- 验证备份完整性
RESTORE VERIFYONLY FROM DISK = @backupPath
```

### 日志清理（简单恢复模式）

> 如果数据库处于完整恢复模式但未做日志备份，日志会无限增长

```sql
-- 查看数据库恢复模式
SELECT name, recovery_model_desc FROM sys.databases WHERE name = 'AIS20240101_001'

-- 查看日志文件大小
SELECT name, log_size_mb = size * 8.0 / 1024,
       log_used_mb = FILEPROPERTY(name, 'SpaceUsed') * 8.0 / 1024
FROM sys.master_files
WHERE type_desc = 'LOG' AND database_id = DB_ID('AIS20240101_001')

-- 收缩日志（简单恢复模式下或备份日志后）
USE [AIS20240101_001]
DBCC SHRINKFILE (AIS20240101_001_log, 100)  -- 收缩至100MB

-- 切换到简单恢复模式（仅开发/测试环境）
ALTER DATABASE [AIS20240101_001] SET RECOVERY SIMPLE
DBCC SHRINKFILE (AIS20240101_001_log, 100)
ALTER DATABASE [AIS20240101_001] SET RECOVERY FULL  -- 生产环境改回完整
```

### 常用维护 SQL

```sql
-- 检查数据库总大小
EXEC sp_spaceused

-- 检查各表大小（找最大的表）
SELECT
    t.NAME AS TableName,
    p.rows AS RowCounts,
    SUM(a.total_pages) * 8 / 1024 AS TotalSpaceMB,
    SUM(a.used_pages) * 8 / 1024 AS UsedSpaceMB
FROM sys.tables t
INNER JOIN sys.indexes i ON t.OBJECT_ID = i.object_id
INNER JOIN sys.partitions p ON i.object_id = p.OBJECT_ID AND i.index_id = p.index_id
INNER JOIN sys.allocation_units a ON p.partition_id = a.container_id
LEFT JOIN sys.schemas s ON t.schema_id = s.schema_id
WHERE t.NAME LIKE 'T_%'
GROUP BY t.Name, p.Rows
ORDER BY TotalSpaceMB DESC

-- 查找碎片率高的索引
SELECT
    OBJECT_NAME(ind.OBJECT_ID) AS TableName,
    ind.name AS IndexName,
    indexstats.avg_fragmentation_in_percent AS Fragmentation
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, NULL) indexstats
INNER JOIN sys.indexes ind ON ind.object_id = indexstats.object_id
    AND ind.index_id = indexstats.index_id
WHERE indexstats.avg_fragmentation_in_percent > 10
ORDER BY Fragmentation DESC

-- 重建碎片率 > 30% 的索引（可生成批量脚本）
ALTER INDEX ALL ON T_SAL_ORDER REBUILD WITH (ONLINE = ON)

-- 更新统计信息
UPDATE STATISTICS T_SAL_ORDER WITH FULLSCAN

-- 查看当前活动连接数
SELECT COUNT(*) AS ConnectionCount
FROM sys.dm_exec_sessions
WHERE database_id = DB_ID('AIS20240101_001')

-- 查找长时间运行的查询
SELECT
    r.session_id,
    r.status,
    r.start_time,
    r.total_elapsed_time / 1000 AS elapsed_seconds,
    SUBSTRING(st.text, (r.statement_start_offset/2)+1,
        ((CASE r.statement_end_offset WHEN -1 THEN DATALENGTH(st.text)
          ELSE r.statement_end_offset END - r.statement_start_offset)/2)+1) AS statement_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS st
WHERE r.total_elapsed_time > 30000
ORDER BY r.total_elapsed_time DESC
```

---

## 日志查看与排查

### 星空日志位置

```
# 应用日志
K3Cloud\WebSite\App_Data\Logs\YYYYMMDD.log

# 旧版日志位置（视版本而定）
K3Cloud\WebSite\Log\

# IIS 错误日志
C:\inetpub\logs\LogFiles\W3SVC1\
```

### 日志级别

| 级别 | 含义 | 处理优先级 |
|------|------|------------|
| Debug | 调试信息 | 仅开发时关注 |
| Info | 正常操作记录 | 了解即可 |
| Warning | 潜在问题 | 定期检查 |
| Error | 操作失败 | 尽快处理 |
| Fatal | 系统级错误 | 立即处理 |

### 排查流程

1. **确认现象**：报错时间 / 操作步骤 / 受影响用户范围
2. **查看对应时间段日志**：筛选 Error/Fatal 级别
3. **搜索关键字**：用户报错信息、单据编号、操作名称
4. **定位插件/方法**：从堆栈跟踪中找到自定义代码位置
5. **复现问题**：在测试环境尝试复现

### 常用日志关键字搜索

```powershell
# 搜索今日日志中的 Error
Select-String -Path "K3Cloud\WebSite\App_Data\Logs\$(Get-Date -Format 'yyyyMMdd').log" -Pattern "Error|Exception" -Context 2,5

# 搜索特定单据相关日志
Select-String -Path "*.log" -Pattern "SAL_SaleOrder" | Select-Object -Last 50
```

### 数据库操作日志

```sql
-- 查看最近的操作日志（谁做了什么操作）
SELECT TOP 100
    OL.FCREATEDATE,
    OL.FUSERID,
    U.FNAME AS UserName,
    OL.FOPERATETYPE,
    OL.FBILLNO,
    OL.FFORMID
FROM T_BAS_OPERATIONLOG OL
LEFT JOIN T_SEC_USER U ON U.FID = OL.FUSERID
ORDER BY OL.FCREATEDATE DESC

-- 查看系统异常日志
SELECT TOP 100 * FROM T_BAS_EXCEPTIONLOG ORDER BY FCREATEDATE DESC

-- 查看登录记录
SELECT TOP 100
    FLoginTime,
    FUserName,
    FLoginIP,
    FLoginResult
FROM T_SEC_LOGINLOG
ORDER BY FLoginTime DESC
```

---

## 常见生产故障处理

### 故障1：系统无法登录

**排查步骤：**
1. 检查 IIS 应用池是否正常运行（不是停止状态）
2. 检查数据库服务是否正常（SQL Server 服务）
3. 检查数据库连接配置（管理中心 → 账套 → 编辑）
4. 查看应用日志是否有数据库连接超时/失败
5. 检查服务器磁盘空间（日志和数据库空间是否满了）

```sql
-- 检查数据库是否可连接
SELECT @@VERSION, GETDATE()

-- 检查数据库状态
SELECT name, state_desc FROM sys.databases WHERE name LIKE 'AIS%'
```

### 故障2：某操作报错"未将对象引用设置到对象的实例"

这是最常见的 NullReferenceException，通常是自定义插件中空值未处理。

**排查：**
1. 查看日志，找到完整堆栈
2. 定位到具体代码行
3. 检查相关字段是否可能为 null
4. 修复：在代码中添加 null 判断

```csharp
// 错误写法（可能 NullReferenceException）
string name = (this.Model.GetValue("FMaterialId") as DynamicObject)["Name"].ToString();

// 正确写法
var material = this.Model.GetValue("FMaterialId") as DynamicObject;
string name = material?["Name"]?.ToString() ?? string.Empty;
```

### 故障3：提交/审核卡住（长时间转圈）

**排查步骤：**
1. 查看数据库是否有死锁或长时间运行的事务

```sql
-- 检查死锁和阻塞
SELECT
    blocking_session_id AS BlockingSession,
    session_id AS BlockedSession,
    wait_type,
    wait_time / 1000 AS WaitSeconds,
    SUBSTRING(st.text, (r.statement_start_offset/2)+1, 100) AS BlockedSQL
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) st
WHERE blocking_session_id > 0

-- 终止阻塞进程（谨慎使用）
KILL 55  -- 55 是 session_id
```

2. 检查是否有操作插件中有耗时操作（如在循环中查数据库）
3. 查看 IIS 线程是否耗尽

### 故障4：数据库日志满导致无法写入

```sql
-- 立即处理：切简单恢复模式，收缩日志（临时措施）
USE [AIS20240101_001]
ALTER DATABASE [AIS20240101_001] SET RECOVERY SIMPLE
DBCC SHRINKFILE (N'AIS20240101_001_log', 100)
ALTER DATABASE [AIS20240101_001] SET RECOVERY FULL

-- 长期方案：配置定期日志备份 + 监控日志空间
```

### 故障5：部署包安装失败

| 错误信息 | 原因 | 处理 |
|----------|------|------|
| 版本不兼容 | 包的版本高于目标环境 | 升级目标环境版本 |
| 对象已签出 | 目标环境有人正在编辑同名对象 | 让对方签入，或强制签入 |
| 字段已存在 | 字段名冲突 | 检查是否重复部署，或重命名 |
| 数据库错误 | 目标环境数据库异常 | 查数据库日志 |

---

## 性能优化建议

### 数据库层

1. **索引优化**：对 WHERE 子句中的高频条件字段建立索引
2. **避免全表扫描**：查询条件走索引，注意函数包装会导致索引失效
3. **分页查询**：大结果集务必使用分页，避免一次性加载全部数据
4. **读写分离**：大型企业可考虑将报表查询指向只读副本
5. **定期维护**：每周重建碎片率>30%的索引，每日更新统计信息

**常见 SQL 性能问题：**
```sql
-- 坏：LIKE 前缀通配符无法使用索引
WHERE t.FNAME LIKE '%测试%'

-- 好：后缀通配符可以走索引
WHERE t.FNAME LIKE '测试%'

-- 坏：函数导致索引失效
WHERE YEAR(t.FDATE) = 2024

-- 好：改写为范围查询
WHERE t.FDATE >= '2024-01-01' AND t.FDATE < '2025-01-01'
```

### 插件层

1. **OnPreparePropertys**：只加载当前操作需要的字段，避免加载全部
2. **批量查询**：避免在循环中反复查数据库，先批量查，再内存匹配
3. **缓存基础资料**：频繁使用的基础资料可用 `MemoryCache` 缓存
4. **异步处理**：发邮件、调外部接口等耗时操作用后台线程或定时任务

### WebAPI 层

1. **批量操作**：使用 `BatchSave` 减少请求次数
2. **合理分页**：大数据量用 `startRow` + `limit` 分页获取
3. **字段精简**：`fieldKeys` 只传需要的字段
4. **连接复用**：使用 Session 复用登录凭证，不要每次请求都重新登录

### IIS 层

1. **禁用不必要回收**：生产环境应用池设置固定回收时间（如凌晨2点），避免业务高峰期回收
2. **启用 Gzip 压缩**：静态资源和 JSON 响应开启压缩，减少传输量
3. **输出缓存**：不常变化的列表页面开启缓存
4. **服务器资源监控**：CPU > 80% 或内存 > 85% 时发出告警

---

## 环境监控指标

### 关键监控项

| 监控项 | 正常范围 | 告警阈值 | 说明 |
|--------|----------|----------|------|
| IIS 应用池状态 | Running | 非 Running | 立即告警 |
| CPU 使用率 | < 70% | > 85% | 持续5分钟以上 |
| 内存使用率 | < 80% | > 90% | 注意内存泄漏 |
| 数据库日志空间 | < 70% | > 85% | 提前清理或扩容 |
| 磁盘空间（日志盘） | < 75% | > 85% | 定期清理日志 |
| 活动数据库连接数 | < 200 | > 500 | 可能连接泄漏 |
| 页面响应时间 | < 3s | > 10s | 前端或后端性能问题 |

### 监控脚本（定期执行）

```sql
-- 汇总监控快照
SELECT
    '当前时间' AS Item, CONVERT(NVARCHAR, GETDATE(), 120) AS Value
UNION ALL
SELECT '活动连接数', CAST(COUNT(*) AS NVARCHAR)
FROM sys.dm_exec_sessions WHERE status = 'running'
UNION ALL
SELECT '阻塞数量', CAST(COUNT(*) AS NVARCHAR)
FROM sys.dm_exec_requests WHERE blocking_session_id > 0
UNION ALL
SELECT '数据库日志使用率(%)',
    CAST(CAST(log_reuse_wait_desc AS NVARCHAR) AS NVARCHAR) + ' / ' +
    CAST(CAST((SELECT SUM(used_pages) * 8.0 / 1024 / SUM(size) * 100
               FROM sys.master_files WHERE database_id = DB_ID() AND type = 1) AS INT) AS NVARCHAR) + '%'
FROM sys.databases WHERE name = DB_NAME()
```

### 快速健康检查脚本（PowerShell）

```powershell
# 检查 IIS 应用池状态
Import-Module WebAdministration
Get-WebConfiguration system.applicationHost/applicationPools/add |
    Select-Object name, @{n='state';e={(Get-WebAppPoolState $_).Value}} |
    Where-Object { $_.state -ne 'Started' }

# 检查磁盘空间
Get-PSDrive C, D | Select-Object Name,
    @{n='Used(GB)';e={[math]::Round(($_.Used/1GB),1)}},
    @{n='Free(GB)';e={[math]::Round(($_.Free/1GB),1)}},
    @{n='Free%';e={[math]::Round(($_.Free/($_.Used+$_.Free)*100),1)}}
```
