# Cron Task Manager - Cron 任务管理

## 技能描述

管理 OpenClaw Cron 定时任务，支持创建、更新、删除、查看、立即执行，以及任务状态监控。

## 触发条件

- **手动触发**：用户说"创建定时任务"、"查看 Cron"、"删除任务"
- **自动触发**：任务执行失败时通知用户

## 核心能力

1. **任务创建** - 创建 Cron 定时任务（cron/every/at）
2. **任务更新** - 修改任务配置（时间/内容）
3. **任务删除** - 删除指定任务
4. **任务查看** - 列出所有任务及状态
5. **立即执行** - 触发任务立即运行
6. **运行历史** - 查看任务执行记录
7. **失败通知** - 任务失败时飞书通知

## 成功案例（2026-03-06）

### 已有任务清单

| 任务名称 | 类型 | 时间 | 状态 |
|---------|------|------|------|
| **每小时优先级提醒** | every | 每小时 | ✅ 运行中 |
| **周三周报生成** | cron | 周三 15:00 | ✅ 运行中 |

### 每小时优先级提醒

**配置：**
```json
{
  "name": "每小时优先级提醒",
  "schedule": {
    "kind": "every",
    "everyMs": 3600000
  },
  "payload": {
    "kind": "systemEvent",
    "text": "优先级提醒"
  },
  "sessionTarget": "main"
}
```

**执行内容：**
1. 读取 worklog.txt
2. 提取待办事项
3. 优先级排序（四象限）
4. TTS 语音生成
5. 飞书发送（文字 + 语音）
6. 本地自动播放

### 周三周报生成

**配置：**
```json
{
  "name": "周三周报生成",
  "schedule": {
    "kind": "cron",
    "expr": "0 15 * * 3",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "生成周报"
  },
  "sessionTarget": "main"
}
```

**执行内容：**
1. 读取 worklog.txt（本周内容）
2. 读取豆包会话（如有）
3. 生成周报草稿
4. 飞书发送通知
5. 用户手动编辑

---

## Cron 表达式语法

### 格式

```
分 时 日 月 周
```

### 示例

| 表达式 | 说明 |
|--------|------|
| `0 15 * * 3` | 每周三 15:00 |
| `0 9 * * 1-5` | 工作日 9:00 |
| `0 18 * * *` | 每天 18:00 |
| `0 0 1 * *` | 每月 1 日 0:00 |
| `*/30 * * * *` | 每 30 分钟 |

### 特殊字符

- `*` - 每个值（每天、每月等）
- `,` - 分隔多个值（如 1,3,5）
- `-` - 范围（如 1-5 表示周一到周五）
- `/` - 步长（如 */30 表示每 30 分钟）

---

## 任务类型

### 1. Cron 表达式类型

**适用场景：** 固定时间点执行

**示例：**
```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 15 * * 3",
    "tz": "Asia/Shanghai"
  }
}
```

### 2. 间隔执行类型

**适用场景：** 每隔固定时间执行

**示例：**
```json
{
  "schedule": {
    "kind": "every",
    "everyMs": 3600000  // 1 小时
  }
}
```

### 3. 一次性类型

**适用场景：** 指定时间执行一次

**示例：**
```json
{
  "schedule": {
    "kind": "at",
    "at": "2026-03-07T10:00:00+08:00"
  }
}
```

---

## Payload 类型

### systemEvent（主会话）

**适用：** 主会话中的系统事件

**示例：**
```json
{
  "payload": {
    "kind": "systemEvent",
    "text": "优先级提醒"
  },
  "sessionTarget": "main"
}
```

### agentTurn（隔离会话）

**适用：** 独立子代理执行

**示例：**
```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "检查邮箱并总结",
    "model": "qwen",
    "timeoutSeconds": 300
  },
  "sessionTarget": "isolated"
}
```

---

## 工作流程

### 创建任务流程

```
1. 识别用户需求 - 时间、频率、执行内容
2. 生成 Cron 表达式 - 或间隔时间
3. 选择 Payload 类型 - systemEvent/agentTurn
4. 配置 Delivery - none/announce/webhook
5. 调用 Cron API - 创建任务
6. 返回任务 ID - 保存供后续操作
7. 发送确认 - 飞书通知创建成功
```

### 任务管理流程

```
查看任务：
1. 调用 cron list
2. 格式化输出
3. 显示状态（enabled/disabled）

更新任务：
1. 识别任务 ID
2. 生成配置补丁
3. 调用 cron update
4. 确认更新成功

删除任务：
1. 识别任务 ID
2. 用户确认
3. 调用 cron remove
4. 确认删除成功

立即执行：
1. 识别任务 ID
2. 调用 cron run
3. 等待执行完成
4. 返回执行结果
```

---

## 技术实现

### 创建任务（PowerShell）

```powershell
# 创建每小时提醒任务
$job = @{
    name = "每小时优先级提醒"
    schedule = @{
        kind = "every"
        everyMs = 3600000
    }
    payload = @{
        kind = "systemEvent"
        text = "优先级提醒"
    }
    sessionTarget = "main"
    enabled = $true
}

# 调用 Cron API
$response = Invoke-CronAdd -Job $job
$jobId = $response.jobId

Write-Host "✅ 任务已创建：$jobId"
```

### 查看任务列表

```powershell
# 列出所有任务
$jobs = Invoke-CronList -IncludeDisabled $true

foreach ($job in $jobs) {
    Write-Host "任务：$($job.name)"
    Write-Host "ID: $($job.id)"
    Write-Host "状态：$(if ($job.enabled) { '✅' } else { '❌' })"
    Write-Host "类型：$($job.schedule.kind)"
    Write-Host ""
}
```

### 立即执行任务

```powershell
# 触发任务立即运行
$jobId = "964d7956-2991-4288-9c55-c246977bca0c"
$response = Invoke-CronRun -JobId $jobId -RunMode "force"

Write-Host "✅ 任务已触发：$jobId"
Write-Host "执行 ID: $($response.runId)"
```

---

## 输出格式

### 任务列表（飞书消息）

```markdown
## 📅 Cron 任务列表

**时间：** 2026-03-07 01:10
**总计：** 2 个任务

### ✅ 运行中

| 任务名称 | 类型 | 时间 | ID |
|---------|------|------|-----|
| **每小时优先级提醒** | every | 每小时 | 964d7956 |
| **周三周报生成** | cron | 周三 15:00 | a3f8b2c1 |

### ❌ 已禁用

无

[管理任务](command:cron-manage)
```

### 创建确认（飞书消息）

```markdown
## ✅ Cron 任务已创建

**任务名称：** 每日同步提醒
**任务 ID：** b7e9d4f2
**执行时间：** 每天 18:00
**类型：** cron

**执行内容：**
检查邮箱、日历、通知，生成摘要

**状态：** ✅ 已启用

[立即执行](command:cron-run-b7e9d4f2) | [编辑](command:cron-edit-b7e9d4f2) | [删除](command:cron-del-b7e9d4f2)
```

---

## 用户偏好

- ✅ **简单配置** - 用自然语言描述，自动生成 Cron
- ✅ **状态清晰** - 明确显示 enabled/disabled
- ✅ **立即执行** - 支持手动触发测试
- ✅ **运行历史** - 查看执行记录
- ✅ **失败通知** - 任务失败时飞书提醒

---

## 示例用法

**场景 1：创建每小时提醒**
```
用户："每小时提醒我优先级任务"
AI: 
1. 生成配置（every, 3600000ms）
2. 创建任务
3. 返回任务 ID
4. 飞书确认
```

**场景 2：创建周报任务**
```
用户："每周三下午 3 点自动生成周报"
AI:
1. 生成 Cron 表达式（0 15 * * 3）
2. 创建任务
3. 配置 payload（生成周报）
4. 飞书确认
```

**场景 3：查看任务**
```
用户："有哪些定时任务？"
AI:
1. 调用 cron list
2. 格式化输出
3. 显示状态
```

**场景 4：立即执行**
```
用户："现在执行优先级提醒"
AI:
1. 识别任务 ID
2. 调用 cron run
3. 等待执行
4. 返回结果
```

**场景 5：删除任务**
```
用户："删除每小时提醒"
AI:
1. 识别任务 ID
2. 用户确认
3. 调用 cron remove
4. 确认删除
```

---

## 注意事项

1. **时区设置** - 使用 Asia/Shanghai（GMT+8）
2. **任务 ID** - 保存 ID 供后续操作
3. **权限验证** - 删除操作需用户确认
4. **执行日志** - 记录每次执行结果
5. **失败重试** - 失败时发送通知

---

## 参考文档

- Cron API 文档：`openclaw docs/cron`
- 已有任务：`cron list`
- 配置示例：本 Skill 中的成功案例

---

_最后更新：2026-03-07 01:10 - 创建 Skill（参考 2026-03-06 已有任务配置）_
