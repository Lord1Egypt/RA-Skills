# heartbeat-memory 故障排查

本文档提供 heartbeat-memory Skill 的完整故障排查指南。

> 💡 **路径说明：​** 本文档中的命令分两类：
> - **相对路径（`./`）​**：在工作区目录下执行，适用于所有工作区，无需替换。
> - **绝对路径示例**：使用默认工作区 `~/.openclaw/workspace/` 举例。如使用多个 Agent，请将 `workspace` 替换为对应工作区名称（如 `workspace-dev`、`workspace-test`）。

---

## 🔍 问题诊断流程

```
1. 确认 Heartbeat 已启用
   ↓
2. 检查配置文件是否存在
   ↓
3. 查看状态文件
   ↓
4. 查看执行日志
   ↓
5. 手动触发测试
```

---

## ❓ 常见问题

### 问题 1：Skill 不执行

**症状：​** Heartbeat 触发但没有执行记忆保存

**检查步骤：​**

```bash
# 1. 确认 Heartbeat 已启用
openclaw config get agents.defaults.heartbeat

# 2. 检查配置文件是否存在（相对路径，在工作区目录下执行）
ls -lh ./memory/heartbeat-memory-config.json

# 3. 查看状态文件
cat ./memory/heartbeat-state.json
```

**可能原因：​**

- Heartbeat 未启用
- 配置文件损坏
- Skill 未正确安装

**解决方案：​**

```bash
# 方案 1：检查 Heartbeat 配置
openclaw config get agents.defaults.heartbeat
# 输出 {"every": "30m"} 表示已启用
# 如未启用，编辑 openclaw.json 添加：
# "agents": { "defaults": { "heartbeat": { "every": "30m" } } }
openclaw gateway restart

# 方案 2：重建配置文件（相对路径，在工作区目录下执行）
rm ./memory/heartbeat-memory-config.json
# 下次执行时会自动重建

# 方案 3：重新安装 Skill
clawhub reinstall heartbeat-memory
openclaw gateway restart
```

---

### 问题 2：HEARTBEAT.md 未更新

**症状：​** 配置已变更但 HEARTBEAT.md 未同步

**检查步骤：​**

```bash
# 1. 查看配置是否真的变更（相对路径，在工作区目录下执行）
cat ./memory/heartbeat-memory-config.json

# 2. 查看状态文件中的 configHash
cat ./memory/heartbeat-state.json | grep configHash

# 3. 手动触发一次执行
# 在聊天中发送："执行 heartbeat-memory"
```

**可能原因：​**

- configHash 未更新
- 文件权限问题
- 同步逻辑错误

**解决方案：​**

```bash
# 方案 1：删除 configHash（强制重新同步）
# 编辑 ./memory/heartbeat-state.json，删除 "configHash" 字段

# 方案 2：检查文件权限（相对路径，在工作区目录下执行）
ls -lh ./HEARTBEAT.md
# 确保当前用户有写权限

# 方案 3：手动删除 HEARTBEAT.md，下次执行时会自动创建（相对路径）
rm ./HEARTBEAT.md
```

---

### 问题 3：日期检测错误

**症状：​** `processSessionsAfter` 日期不正确

**可能原因：​**

- 自动检测使用了错误的参考点
- 配置文件被手动修改
- sessions 日期格式不一致

**解决方案：​**

```bash
# 方案 1：手动设置正确日期
# 编辑 ./memory/heartbeat-memory-config.json
```

```json
{
  "memorySave": {
    "processSessionsAfter": "2026-03-01T00:00:00Z"
  }
}
```

```bash
# 方案 2：删除配置，让 Skill 重新检测（相对路径）
rm ./memory/heartbeat-memory-config.json
# 下次执行时会自动检测

# 方案 3：删除 configHash（触发重新同步）
# 编辑 ./memory/heartbeat-state.json，删除 "configHash" 字段
```

---

### 问题 4：通知未发送

**症状：​** 执行完成但没有收到通知

**检查步骤：​**

```bash
# 1. 查看日志中是否有 "通知已发送"（查看 Gateway 日志或终端输出）

# 2. 检查 notifyTarget 配置（相对路径）
cat ./memory/heartbeat-memory-config.json | grep notifyTarget
```

**可能原因：​**

- 通知目标配置错误
- 渠道不支持
- 权限不足

**解决方案：​**

```bash
# 方案 1：不配置 notifyTarget（自动检测）
# 删除 notifyTarget 字段，Skill 会自动获取当前用户

# 方案 2：手动指定正确的目标
```

```json
{
  "notifyTarget": "feishu:ou_xxxxx"
}
```

```bash
# 方案 3：检查渠道配置
# 确保飞书机器人已正确配置和授权
```

---

### 问题 5：处理速度慢

**症状：​** 执行时间超过预期（>5 分钟）

**可能原因：​**

- sessions 数量过多
- LLM 超时设置过短
- 网络问题

**解决方案：​**

```json
// 方案 1：限制单次处理数量
{
  "memorySave": {
    "maxSessionsPerRun": 20
  }
}
```

```json
// 方案 2：增加超时时间
{
  "memorySave": {
    "timeoutSeconds": 1500
  }
}
```

```json
// 方案 3：限制日期范围
{
  "memorySave": {
    "processSessionsAfter": "2026-03-01T00:00:00Z"
  }
}
```

---

### 问题 6：LLM 提炼失败

**症状：​** 提示 "LLM 调用失败" 或 "LLM 解析失败"

**可能原因：​**

- 模型不可用
- token 超限
- 网络超时

**解决方案：​**

```json
// 方案 1：增加超时时间
{
  "memorySave": {
    "timeoutSeconds": 1500
  }
}
```

```json
// 方案 2：减少 batchSize
{
  "memorySave": {
    "batchSize": 3
  }
}
```

```bash
# 方案 3：检查模型配置
# 确认 openclaw.json 中配置的模型可用
openclaw models status
```

---

### 问题 7：MEMORY.md 未提炼

**症状：​** 执行完成但 MEMORY.md 未更新

**可能原因：​**

- 未达到提炼时间
- refineSchedule 配置错误
- 提炼逻辑失败

**解决方案：​**

```json
// 方案 1：检查提炼配置
{
  "memorySave": {
    "refineSchedule": {
      "type": "weekly",
      "dayOfWeek": "sunday",
      "time": "20:00"
    }
  }
}
```

```bash
# 方案 2：手动触发提炼
# 编辑 ./memory/heartbeat-state.json，删除 "lastRefine" 字段
# 下次执行时会检查是否需要提炼

# 方案 3：查看提炼日志
# 检查是否有 "MEMORY.md 提炼失败" 的错误
```

---

## 🛠️ 调试工具

### 查看执行日志

```bash
# 查看当前 Agent 的执行记录（将 <agent-id> 替换为你的 Agent ID）
tail -100 ~/.openclaw/agents/<agent-id>/sessions/*.jsonl | grep "heartbeat-memory"
# 示例：
# tail -100 ~/.openclaw/agents/main/sessions/*.jsonl | grep "heartbeat-memory"
# tail -100 ~/.openclaw/agents/dev-agent/sessions/*.jsonl | grep "heartbeat-memory"

# 查看 Gateway 日志（系统级日志，路径固定）
tail -f ~/.openclaw/logs/gateway.log | grep "heartbeat-memory"
```

### 手动触发调试

```
在聊天中发送：执行 heartbeat-memory
```

### 查看状态文件

```bash
# 完整状态（相对路径，在工作区目录下执行）
cat ./memory/heartbeat-state.json

# 只看关键字段
cat ./memory/heartbeat-state.json | jq '{processedSessions, lastCheck, lastRefine, configHash}'
```

### 验证配置

```bash
# 检查配置语法（相对路径）
node -e "console.log(JSON.parse(require('fs').readFileSync('./memory/heartbeat-memory-config.json')))"

# 检查文件权限
ls -lh ./memory/
```

---

## 📊 性能优化建议

### 大量 sessions（>100 个）

```json
{
  "memorySave": {
    "maxSessionsPerRun": 20,
    "processSessionsAfter": "2026-03-01T00:00:00Z",
    "timeoutSeconds": 1500,
    "batchSize": 5
  }
}
```

**说明：​** 分批处理，限制日期范围，增加超时时间，防止 OOM 和失败。

---

### 频繁触发（减少通知打扰）

```json
{
  "channels": {
    "defaults": {
      "heartbeat": {
        "showOk": false
      }
    }
  }
}
```

**说明：​** 在 `openclaw.json` 中配置，禁用 OK 通知，减少打扰。

---

### 内存优化

```json
{
  "memorySave": {
    "batchSize": 3,
    "maxSessionsPerRun": 10,
    "continuousBatching": true
  }
}
```

**说明：​** 小批量处理，减少内存占用，连续分批避免堆积。

---

## 📞 获取帮助

### 收集诊断信息

```bash
# 1. 系统信息
node --version
openclaw --version

# 2. 配置文件（相对路径，在工作区目录下执行）
cat ./memory/heartbeat-memory-config.json

# 3. 状态文件
cat ./memory/heartbeat-state.json

# 4. 最近的日志
tail -50 ~/.openclaw/logs/gateway.log
```

### 报告问题

提供以上信息，有助于快速定位问题。

---

## 📖 相关文档

- [配置详解](config.md) - 完整配置说明
- [API 参考](api.md) - 字段详解和数据结构
- [SKILL.md](../SKILL.md) - Skill 使用指南
```
