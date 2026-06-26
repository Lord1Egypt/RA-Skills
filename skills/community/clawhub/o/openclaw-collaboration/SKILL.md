---
name: openclaw-collaboration
description: Hermes 与本地 OpenClaw 协同工作方案 — 共享记忆、API互调、任务分工
version: 1.1
created: 2026-04-19
---

# Hermes + OpenClaw 协同工作

## ⚠️ 安全警告

**重要：此 skill 涉及系统级操作，请仔细阅读以下安全说明后再使用。**

### 潜在风险

此 skill 允许 AI 执行以下操作：
- 读写 OpenClaw workspace 目录下的文件
- 调用 OpenClaw API 执行任务
- 修改系统配置文件
- 重启 OpenClaw gateway 服务
- 通过飞书等渠道发送消息

### 使用前提条件

**使用此 skill 前，请确保：**

1. **明确授权范围**
   - 只在受信任的环境中使用
   - 明确允许 AI 执行的操作类型
   - 设置审批规则，重要操作需要人工确认

2. **了解操作影响**
   - 理解每个命令的作用和潜在影响
   - 确认不会破坏现有系统配置
   - 评估对生产环境的影响

3. **备份重要数据**
   - 使用前备份 OpenClaw workspace
   - 备份配置文件
   - 记录当前系统状态

4. **监控和审计**
   - 启用操作日志记录
   - 定期检查系统状态
   - 监控异常行为

### 安全建议

**推荐的安全实践：**

1. **限制操作范围**
   - 只允许只读操作（查看日志、状态检查）
   - 禁止修改配置文件
   - 禁止重启服务

2. **使用沙箱环境**
   - 在测试环境中先验证
   - 确认无误后再应用到生产环境

3. **设置审批流程**
   - 重要操作需要人工确认
   - 定期审查 AI 执行的操作
   - 建立回滚机制

4. **定期审计**
   - 检查操作日志
   - 验证系统完整性
   - 审查权限设置

## 环境信息

- OpenClaw: /usr/local/bin/openclaw (v2026.4.15)
- 配置: ~/.openclaw/openclaw.json
- Workspace: ~/.openclaw/workspace/
- Gateway: 端口 18789 (loopback), token 认证
- 可用模型: minimax-m2.5(主), z-ai/glm5, gemma-3-27b-it
- NVIDIA API: integrate.api.nvidia.com/v1

## 三种协同方式

### 1. 共享记忆（只读模式）

Hermes 可以读取 OpenClaw workspace 目录下的记忆文件。
- Hermes 写入时在条目末尾加 [Hermes] 标记
- 避免同时写同一文件: Hermes 写 projects/ 和 decisions/, OpenClaw 写每日日志

**安全提示：**
- 建议只使用只读模式
- 写入操作需要人工确认
- 定期检查文件完整性

### 2. API 互调（需谨慎）

```bash
# 给 OpenClaw 派任务（只读操作）
openclaw agent --agent main --message "任务描述" --json --timeout 60

# 指定 agent
openclaw agent --agent glm5 --message "任务" --json --timeout 60

# 本地模式（推荐）
openclaw agent --local --agent main --message "任务" --json --timeout 30
```

**安全提示：**
- 优先使用本地模式（--local）
- 避免使用 --deliver 参数（可能发送未授权消息）
- 设置合理的 timeout 避免卡住
- 重要任务需要人工确认

**不推荐的操作（需要额外授权）：**
```bash
# ⚠️ 投递回复到频道（可能发送未授权消息）
openclaw agent --agent main --message "任务" --deliver --reply-channel feishu
```

### 3. 任务分工

- 达梦数据库/SQL → Hermes (有专项 skill)
- 飞书消息处理 → OpenClaw (原生集成)
- 快速问答 → Hermes (响应更快)
- 深度推理 → OpenClaw (可调 thinking level)
- 代码编写/文件整理 → 两者均可

## 配置修复踩坑（仅供参考）

**注意：以下操作涉及配置文件修改，请谨慎操作。**

1. 拼写错误: includeDefaultMemor → includeDefaultMemory
2. 非法 key: memory.flush 不是合法配置项(旧版遗留), 需删除
3. 修复: 直接编辑 json 文件, 或 openclaw doctor --fix(可能卡住)

**安全提示：**
- 修改配置前先备份
- 使用 openclaw doctor --fix 前确认不会卡住
- 修改后验证配置正确性

### NVIDIA API 模型 ID 格式

- OpenClaw 配置用: nvidia/z-ai/glm5 (带 provider 前缀)
- NVIDIA API 实际: z-ai/glm5 (无 provider 前缀)
- 调 API 时用无前缀版本

### GLM5 超时问题

- GLM5 在 NVIDIA API 上频繁超时(idle watchdog 触发)
- 表现: agent 命令无响应, err.log 报 timeout from=nvidia/z-ai/glm5
- 这是之前卡顿的根因
- 解决: 优先用 minimax-m2.5 作为主模型

## Gateway 运维（仅供参考）

**注意：以下操作涉及服务管理，请谨慎操作。**

- 检查在线: 访问 localhost:18789/health
- 查进程: ps aux | grep openclaw-gateway
- 查错误日志: tail ~/.openclaw/logs/gateway.err.log
- 重启: kill 旧进程后 openclaw gateway --port 18789

**安全提示：**
- 重启前确认不会影响正在运行的任务
- 查看错误日志前确认日志文件权限
- 重要操作需要人工确认

## 审计和监控

### 操作日志

建议记录以下操作：
- 文件读写操作
- API 调用记录
- 配置修改记录
- 服务重启记录

### 监控建议

1. **定期检查**
   - 检查 workspace 目录完整性
   - 检查配置文件是否被修改
   - 检查 gateway 服务状态

2. **异常检测**
   - 监控异常文件操作
   - 监控异常 API 调用
   - 监控异常消息发送

3. **权限管理**
   - 定期审查文件权限
   - 定期审查 API 访问权限
   - 定期审查消息发送权限

## 待完善

- [ ] WebSocket 长连接实时通信
- [ ] Python 封装脚本简化 agent 调用
- [ ] 文件锁或写入协调避免冲突
- [ ] 操作审计日志
- [ ] 权限管理系统
- [ ] 操作审批流程

## 版本历史

### v1.1 (2026-05-01)
- 添加安全警告和使用前提条件
- 添加安全建议和最佳实践
- 标记危险操作，需要额外授权
- 添加审计和监控建议
- 弱化配置修改和服务重启操作

### v1.0 (2026-04-19)
- 初始版本
- 定义三种协同方式
- 记录配置修复踩坑
- 记录 Gateway 运维方法
