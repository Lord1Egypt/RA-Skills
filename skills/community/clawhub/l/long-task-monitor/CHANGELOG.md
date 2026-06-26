# Changelog - Long Task Monitor

## English

### v1.0.2 (2026-02-22)

#### 🔧 Fix
- Fix sanitizeInput to allow `:` character (needed for session keys like `agent:main:subagent:xxx`)

---

### v1.0.1 (2026-02-22)

#### 🔒 Security Fix
- Use `execFile` with argument arrays to prevent command injection
- Add input sanitization for all user-provided values (task IDs, session keys, descriptions)
- Add security comment at top of script
- Add metadata fields: runtime, permissions, capabilities, requiredBinaries

---

### v1.0.0 (2026-02-22)

#### 🎉 Initial Release
- **Worker-Monitor Architecture**: Long-running task monitoring solution V2
- **Monitor**: Tracks Worker status via hook-logger logs, 10 minutes per round, reports via Announce
- **Main Session Polling**: Uses polling mechanism due to subagent sessions_send limitation

---

## 中文

### v1.0.2 (2026-02-22)

#### 🔧 修复
- 修复 sanitizeInput 函数，允许 `:` 字符（session keys 需要）

---

### v1.0.1 (2026-02-22)

#### 🔒 安全修复
- 使用 `execFile` + 参数数组防止命令注入
- 对所有用户输入进行过滤（任务ID、session key、描述等）
- 脚本顶部添加安全注释
- 添加 metadata 字段：runtime, permissions, capabilities, requiredBinaries

---

### v1.0.0 (2026-02-22)

#### 🎉 初始版本
- **Worker-Monitor 架构**：长任务监控方案 V2
- **Monitor**：通过 hook-logger 日志监控 Worker，每轮 10 分钟 Announce 汇报
- **主会话轮询**：因子代理 sessions_send 限制采用轮询机制
