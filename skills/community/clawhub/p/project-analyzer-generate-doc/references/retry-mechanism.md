# 重试机制指南

> Project Analyzer Generate Doc - 自动重试策略

---

## 概述

本文档描述文档生成过程中的自动重试机制，包括重试策略、可重试错误类型、以及重试流程。

---

## 重试策略

### 配置参数

```yaml
retry_policy:
  max_retries: 3                    # 最大重试次数
  initial_delay: 30                 # 初始延迟（秒）
  backoff_multiplier: 2             # 延迟倍增因子
  max_delay: 300                    # 最大延迟（秒）
  retryable_errors:                 # 可重试的错误类型
    - "timeout"
    - "context_overflow"
    - "file_access_error"
    - "subagent_crash"
  non_retryable_errors:             # 不可重试的错误类型
    - "invalid_project_path"
    - "permission_denied"
    - "disk_full"
```

### 延迟计算

```javascript
function calculateDelay(retryCount) {
  const delay = Math.min(
    initial_delay * Math.pow(backoff_multiplier, retryCount - 1),
    max_delay
  );
  return delay; // 秒
}

// 示例：
// 第 1 次重试：30 秒
// 第 2 次重试：60 秒
// 第 3 次重试：120 秒（不超过 300 秒上限）
```

---

## 错误分类

### 可重试错误

#### 1. timeout - 子代理超时

**原因**: 子代理处理文件时超过预设时间限制

**处理**:
```
1. 记录已完成的文件
2. 等待延迟时间
3. 重新 spawn 子代理，处理剩余文件
4. 如果连续 3 次超时，减小分片大小
```

#### 2. context_overflow - 上下文溢出

**原因**: 子代理上下文使用率超过 60%

**处理**:
```
1. 触发强制压缩
2. 如果压缩后仍超过 60%，停止子代理
3. 将剩余文件拆分为更小的分片
4. 为新分片 spawn 新的子代理
```

#### 3. file_access_error - 文件访问错误

**原因**: 文件被安全软件限制、文件被占用等

**处理**:
```
1. 记录失败文件到日志
2. 等待 30 秒后重试（文件可能被临时占用）
3. 如果重试后仍失败，跳过该文件
4. 在最终报告中标注无法访问的文件
5. 请求用户确认文件访问权限（不尝试提权）
```

#### 4. subagent_crash - 子代理崩溃

**原因**: 子代理意外退出

**处理**:
```
1. 检查子代理日志，确定崩溃原因
2. 如果是因为上下文溢出，减小分片大小
3. 如果是因为超时，增加超时时间
4. 重新 spawn 子代理，传递已完成进度
```

### 不可重试错误

#### 1. invalid_project_path - 项目路径无效

**原因**: 项目路径不存在或格式错误

**处理**: 
```
1. 验证路径是否存在
2. 检查路径格式
3. 请求用户提供正确的路径
4. 暂停任务，等待用户干预
```

#### 2. permission_denied - 权限不足

**原因**: 没有权限访问项目目录或文件

**处理**:
```
1. 检查目录权限
2. 请求用户授权
3. 如果无法解决，暂停任务
4. ⚠️ 禁止尝试提权
```

#### 3. disk_full - 磁盘已满

**原因**: 目标磁盘空间不足

**处理**:
```
1. 检查磁盘空间
2. 清理临时文件
3. 请求用户释放空间
4. 暂停任务，等待空间释放
```

---

## 重试流程

### 完整流程图

```
子代理失败
    ↓
检测错误类型
    ↓
┌─────────────────┐
│  是否可重试？   │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   是        否
    │         │
    ↓         ↓
检查重试次数  记录错误
    │         │
    │         ↓
    │    请求用户干预
    │
    ↓
┌─────────────────┐
│  达到最大重试   │
│     次数？      │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
   否        是
    │         │
    ↓         ↓
计算延迟时间  标记为失败
    │         │
    │         ↓
    │    继续处理其他任务
    ↓
等待延迟时间
    ↓
重新 spawn 子代理
    ↓
传递已完成进度
    ↓
继续处理剩余文件
    ↓
成功？───→ 完成
    │
   否
    │
    └──→ 回到"检测错误类型"
```

### PowerShell 实现示例

```powershell
function Invoke-WithRetry {
    param(
        [ScriptBlock]$Action,
        [string]$TaskName,
        [int]$MaxRetries = 3,
        [int]$InitialDelay = 30,
        [double]$BackoffMultiplier = 2,
        [int]$MaxDelay = 300
    )
    
    $retryCount = 0
    $lastError = $null
    
    while ($retryCount -lt $MaxRetries) {
        try {
            Write-Host "[$TaskName] 执行任务 (尝试 $($retryCount + 1)/$MaxRetries)..."
            & $Action
            Write-Host "[$TaskName] ✅ 成功"
            return $true
        }
        catch {
            $lastError = $_
            $retryCount++
            
            if ($retryCount -lt $MaxRetries) {
                $delay = [Math]::Min($InitialDelay * [Math]::Pow($BackoffMultiplier, $retryCount - 1), $MaxDelay)
                Write-Warning "[$TaskName] ⚠️ 失败：$lastError"
                Write-Host "[$TaskName] 🔄 $delay 秒后重试..."
                Start-Sleep -Seconds $delay
            }
        }
    }
    
    Write-Error "[$TaskName] ❌ 失败：达到最大重试次数"
    Write-Error "最后错误：$lastError"
    return $false
}

# 使用示例
$success = Invoke-WithRetry -Action {
    # 子代理任务
    sessions_spawn -task "生成 L3 文档" -label "L3-chunk1"
} -TaskName "L3-ces-domain-chunk1" -MaxRetries 3
```

---

## 重试状态跟踪

### 状态文件中的重试信息

```json
{
  "subagents": [
    {
      "label": "L3-admin-api-chunk2",
      "status": "running",
      "startTime": "2026-03-05T15:35:00+08:00",
      "retries": 1,
      "retryHistory": [
        {
          "attempt": 1,
          "startTime": "2026-03-05T15:35:00+08:00",
          "endTime": "2026-03-05T15:40:00+08:00",
          "error": "timeout",
          "errorMessage": "子代理处理超时（5 分钟）",
          "delayBeforeRetry": 30
        }
      ]
    }
  ]
}
```

### 重试日志

```markdown
### [15:40:00] 子代理重试
- ⚠️ L3-admin-api-chunk2 超时，准备重试（1/3）
- 错误类型：timeout
- 错误信息：子代理处理超时（5 分钟）
- 等待 30 秒后重试...

### [15:40:30] 子代理重试启动
- 🔄 重新 spawn 子代理：L3-admin-api-chunk2
- 传递已完成进度：7/12 文件
- 剩余文件：5

### [15:45:00] 子代理重试成功
- ✅ L3-admin-api-chunk2 重试成功（12 文件）
- 总重试次数：1
```

---

## 最佳实践

### 1. 记录详细的错误信息

```javascript
function handleError(error) {
  return {
    type: classifyError(error),
    message: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString(),
    context: {
      subagent: this.label,
      processedFiles: this.processedFiles,
      remainingFiles: this.remainingFiles
    }
  };
}
```

### 2. 智能调整分片大小

```javascript
function adjustChunkSize(failures) {
  if (failures >= 3) {
    // 连续失败 3 次，减小分片大小
    return Math.max(5, currentChunkSize - 3);
  }
  return currentChunkSize;
}
```

### 3. 避免无限重试

```javascript
if (retryCount >= maxRetries) {
  // 标记为永久失败
  markAsPermanentFailure(task);
  // 通知用户
  notifyUser(task, 'failed');
  // 继续处理其他任务
  continueWithNextTask();
}
```

### 4. 区分临时错误和永久错误

```javascript
function isRetryableError(error) {
  const retryableErrors = [
    'timeout',
    'context_overflow',
    'file_access_error',
    'subagent_crash',
    'network_error',
    'rate_limit'
  ];
  
  const permanentErrors = [
    'invalid_path',
    'permission_denied',
    'disk_full',
    'unsupported_file_type'
  ];
  
  if (permanentErrors.includes(error.type)) {
    return false;
  }
  
  return retryableErrors.includes(error.type) || 
         error.type.startsWith('temp_');
}
```

---

## 故障排查

### 问题：重试后仍然失败

**症状**: 子代理重试多次后仍然失败

**排查步骤**:
```
1. 检查错误日志，确定失败原因
2. 如果是超时，考虑增加超时时间或减小分片
3. 如果是上下文溢出，增加压缩频率
4. 如果是文件访问错误，检查文件权限
5. 如果所有重试都失败，标记为"需要手动干预"
```

### 问题：重试延迟过长

**症状**: 重试等待时间过长，影响整体进度

**解决**:
```powershell
# 调整重试策略
$retryPolicy = @{
  MaxRetries = 2           # 减少重试次数
  InitialDelay = 15        # 减少初始延迟
  MaxDelay = 60            # 减少最大延迟
}

# 或者对于紧急任务，禁用重试
$retryPolicy = @{
  MaxRetries = 0
}
```

### 问题：重试导致重复处理

**症状**: 重试后文件被重复处理

**解决**:
```javascript
// 在重试前记录已完成进度
function beforeRetry() {
  saveCheckpoint({
    processedFiles: this.processedFiles,
    currentFileIndex: this.currentFileIndex
  });
}

// 重试后从断点继续
function afterRetry() {
  const checkpoint = loadCheckpoint();
  this.currentFileIndex = checkpoint.currentFileIndex;
  this.processedFiles = checkpoint.processedFiles;
}
```

---

## 相关文档

- [task-monitoring.md](task-monitoring.md) - 任务监控指南
- [checkpoint-resume.md](checkpoint-resume.md) - 断点续传指南
- [error-handling.md](error-handling.md) - 错误处理指南
