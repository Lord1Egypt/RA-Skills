# 任务监控指南

> Project Analyzer Generate Doc - 任务监控与健康检查

---

## 概述

本文档描述如何在文档生成过程中监控任务状态、检查子代理健康状况，以及生成进度报告。

---

## 任务状态跟踪

### 状态文件位置

```
<项目根目录>/.ai-doc/.generate-state.json
```

### 状态文件结构

```json
{
  "version": "2.1.0",
  "projectPath": "E:\\projects\\mgmt-api-cp",
  "startTime": "2026-03-05T15:30:00+08:00",
  "lastUpdateTime": "2026-03-05T15:45:00+08:00",
  "currentPhase": "L3",
  "overallProgress": 45.5,
  "phases": {
    "L3": {
      "status": "in_progress",
      "totalFiles": 312,
      "processedFiles": 142,
      "skippedFiles": 65,
      "failedFiles": 3,
      "chunks": {
        "total": 28,
        "completed": 12,
        "inProgress": 4,
        "pending": 12,
        "failed": 0
      }
    },
    "L2": {
      "status": "pending",
      "totalModules": 7,
      "completedModules": 0
    },
    "L1": {
      "status": "pending",
      "completed": false
    }
  },
  "subagents": [
    {
      "label": "L3-ces-domain-chunk1",
      "status": "completed",
      "startTime": "2026-03-05T15:32:00+08:00",
      "endTime": "2026-03-05T15:38:00+08:00",
      "processedFiles": 12,
      "retries": 0,
      "error": null
    },
    {
      "label": "L3-admin-api-chunk2",
      "status": "running",
      "startTime": "2026-03-05T15:35:00+08:00",
      "lastUpdateTime": "2026-03-05T15:44:00+08:00",
      "processedFiles": 7,
      "totalFiles": 12,
      "retries": 1,
      "error": null
    }
  ],
  "lastCheckpoint": "2026-03-05T15:45:00+08:00",
  "canResume": true
}
```

### 状态枚举

```typescript
type PhaseStatus = 'pending' | 'in_progress' | 'completed' | 'failed';
type SubagentStatus = 'starting' | 'running' | 'completed' | 'failed' | 'timeout' | 'crashed';
```

---

## 健康检查

### 检查频率

- **常规检查**: 每 60 秒
- **密集检查**: 当子代理状态异常时，每 15 秒

### 检查项目

#### 1. 存活检查 (is_alive)

**目的**: 确认子代理是否仍在运行

**方法**:
```powershell
# 使用 sessions_list 检查会话状态
sessions_list --kinds subagent

# 检查特定子代理
sessions_list | Where-Object { $_.label -eq "L3-ces-domain-chunk1" }
```

**判断标准**:
- ✅ healthy: 会话存在且状态为 running
- ❌ unhealthy: 会话不存在或状态为 failed/crashed

#### 2. 进度检查 (progress_making)

**目的**: 确认子代理是否有进度更新

**方法**:
```json
// 检查 .lastUpdateTime 时间戳
{
  "subagent": "L3-admin-api-chunk2",
  "lastUpdateTime": "2026-03-05T15:44:00+08:00",
  "currentTime": "2026-03-05T15:50:00+08:00",
  "noUpdateDuration": "6 分钟"
}
```

**判断标准**:
- ✅ healthy: 最后更新时间 < 5 分钟前
- ⚠️ warning: 最后更新时间 5-10 分钟前
- ❌ unhealthy: 最后更新时间 > 10 分钟前

#### 3. 上下文使用率检查 (context_usage)

**目的**: 监控子代理上下文使用情况

**方法**:
```powershell
# 获取子代理状态
session_status --sessionKey <sessionKey>

# 检查上下文使用率
{
  "contextUsage": 0.45,  // 45%
  "status": "normal"
}
```

**判断标准**:
- ✅ healthy: < 40%
- ⚠️ warning: 40-50%
- ❌ unhealthy: > 50%（需要强制压缩）

#### 4. 内存使用检查 (memory_usage)

**目的**: 监控子代理内存使用（如果框架支持）

**判断标准**:
- ✅ healthy: < 500MB
- ⚠️ warning: 500MB-1GB
- ❌ unhealthy: > 1GB

---

## 进度报告

### 报告频率

- **定期报告**: 每 5 分钟
- **里程碑报告**: 每完成 10% 进度
- **阶段完成报告**: L3/L2/L1 阶段完成时

### 报告格式

```markdown
## 📊 文档生成进度报告

**项目**: mgmt-api-cp
**开始时间**: 2026-03-05 15:30:00
**当前时间**: 2026-03-05 15:45:00
**已用时间**: 15 分钟

### 总体进度：45.5%

```
[████████████░░░░░░░░░░░] 45.5%
```

### 当前阶段：L3 文件级文档生成

| 模块 | 文件数 | 已完成 | 进度 |
|------|--------|--------|------|
| ces-domain | 109 | 65 | 59.6% |
| admin-api | 53 | 28 | 52.8% |
| business-api | 82 | 35 | 42.7% |
| ... | ... | ... | ... |

### 子代理状态

| 子代理 | 状态 | 文件数 | 重试 |
|--------|------|--------|------|
| L3-ces-domain-chunk1 | ✅ 完成 | 12 | 0 |
| L3-ces-domain-chunk2 | ✅ 完成 | 12 | 0 |
| L3-admin-api-chunk1 | 🔄 运行中 | 7/12 | 1 |
| L3-business-api-chunk1 | 🔄 运行中 | 5/10 | 0 |

### 统计

- 已处理文件：142
- 已跳过文件：65（纯定义类）
- 失败文件：3（将在最后重试）
- 活跃子代理：5/8

### 预计完成时间

- L3 阶段：约 25 分钟（剩余 60%）
- L2 阶段：约 10 分钟
- L1 阶段：约 3 分钟
- **总计**: 约 38 分钟
```

### 报告生成逻辑

```javascript
function generateProgressReport(state) {
  const report = {
    project: path.basename(state.projectPath),
    startTime: state.startTime,
    currentTime: new Date(),
    elapsed: formatDuration(Date.now() - state.startTime),
    overallProgress: calculateOverallProgress(state),
    currentPhase: state.currentPhase,
    phaseDetails: state.phases[state.currentPhase],
    subagentStatus: state.subagents.filter(s => s.status === 'running'),
    statistics: {
      processed: state.phases.L3.processedFiles,
      skipped: state.phases.L3.skippedFiles,
      failed: state.phases.L3.failedFiles,
      activeSubagents: state.subagents.filter(s => s.status === 'running').length
    },
    estimatedCompletion: estimateCompletionTime(state)
  };
  
  return formatReport(report);
}
```

---

## 日志记录

### 日志文件位置

```
<项目根目录>/.ai-doc/.task-log.md
```

### 日志格式

```markdown
# 任务执行日志

## 任务信息
- **项目路径**: E:\projects\mgmt-api-cp
- **开始时间**: 2026-03-05 15:30:00
- **模式**: 完整生成 (L3→L2→L1)

## 执行记录

### [15:30:00] 任务启动
- 扫描项目结构...
- 发现 7 个模块，共 312 个关键文件

### [15:31:00] 分片计划完成
- 制定 28 个分片计划
- 最大并行子代理数：8

### [15:32:00] L3 阶段开始
- Spawn 子代理：L3-ces-domain-chunk1
- Spawn 子代理：L3-ces-domain-chunk2
- ...

### [15:38:00] 子代理完成
- ✅ L3-ces-domain-chunk1 完成（12 文件）
- ✅ L3-ces-domain-chunk2 完成（12 文件）

### [15:40:00] 子代理重试
- ⚠️ L3-admin-api-chunk2 超时，准备重试（1/3）
- 等待 30 秒后重试...

### [15:41:00] 子代理重试成功
- ✅ L3-admin-api-chunk2 重试成功（12 文件）

### [15:45:00] 进度报告
- 总体进度：45.5%
- 已完成：142 文件
- 活跃子代理：5/8
```

### 日志级别

| 级别 | 符号 | 说明 |
|------|------|------|
| INFO | ℹ️ | 一般信息 |
| SUCCESS | ✅ | 操作成功 |
| WARNING | ⚠️ | 警告信息 |
| ERROR | ❌ | 错误信息 |
| RETRY | 🔄 | 重试操作 |

---

## 告警机制

### 告警级别

| 级别 | 触发条件 | 处理方式 |
|------|----------|----------|
| INFO | 正常进度更新 | 记录日志 |
| WARNING | 单个子代理进度缓慢 | 继续观察，准备干预 |
| ERROR | 子代理失败/超时 | 自动重试 |
| CRITICAL | 多个子代理连续失败 | 暂停任务，请求用户干预 |

### 告警示例

```markdown
### ⚠️ 警告：子代理进度缓慢

**子代理**: L3-admin-api-chunk2
**最后更新**: 10 分钟前
**已处理**: 3/12 文件
**建议**: 如果 5 分钟后仍无进展，将自动重启子代理

### ❌ 错误：子代理超时

**子代理**: L3-business-api-chunk3
**超时时间**: 5 分钟
**已处理**: 8/10 文件
**操作**: 准备重试（1/3），等待 30 秒...

### 🚨 严重：多个子代理失败

**失败子代理**: 3 个
**失败原因**: 上下文溢出
**操作**: 暂停任务，调整分片策略
```

---

## 最佳实践

### 1. 定期检查状态文件

```powershell
# 每 5 分钟检查一次状态文件
Get-Content .ai-doc\.generate-state.json | ConvertFrom-Json | 
  Select-Object overallProgress, currentPhase
```

### 2. 监控活跃子代理数量

```powershell
# 确保不超过最大并行数
$activeCount = (Get-Content .ai-doc\.generate-state.json | ConvertFrom-Json).subagents |
  Where-Object { $_.status -eq 'running' } | Measure-Object | Select-Object -ExpandProperty Count

if ($activeCount -gt 8) {
  Write-Warning "活跃子代理数量超过限制：$activeCount"
}
```

### 3. 及时处理警告

- 当子代理进度缓慢时，考虑减小分片大小
- 当上下文使用率高时，增加压缩频率
- 当多个子代理失败时，暂停并分析原因

### 4. 保存历史状态

```powershell
# 每小时保存一次状态快照
$timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
Copy-Item .ai-doc\.generate-state.json ".ai-doc\.state-snapshots\state-$timestamp.json"
```

---

## 故障排查

### 问题：状态文件损坏

**症状**: 无法解析 JSON

**解决**:
```powershell
# 检查文件内容
Get-Content .ai-doc\.generate-state.json

# 如果有备份，恢复备份
Copy-Item .ai-doc\.state-snapshots\state-latest.json .ai-doc\.generate-state.json

# 如果没有备份，重新扫描项目
```

### 问题：子代理状态不一致

**症状**: 状态文件显示 running，但实际已停止

**解决**:
```powershell
# 强制刷新子代理状态
sessions_list --kinds subagent

# 手动更新状态文件
# 将不一致的子代理标记为 failed
```

### 问题：进度报告不准确

**症状**: 报告显示的进度与实际不符

**解决**:
```powershell
# 重新统计已生成的文档数量
$docCount = Get-ChildItem .ai-doc -Include *.md -Recurse | Measure-Object | Select-Object -ExpandProperty Count

# 更新状态文件
Update-StateFile -ProcessedFiles $docCount
```

---

## 相关文档

- [retry-mechanism.md](retry-mechanism.md) - 重试机制指南
- [checkpoint-resume.md](checkpoint-resume.md) - 断点续传指南
- [context-compression.md](context-compression.md) - 上下文压缩指南
