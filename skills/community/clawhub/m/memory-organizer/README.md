# Memory Organizer

[English](#english) | [中文](#中文)

---

## English

### Description
Organize OpenClaw memory with a clean two-layer strategy. Keep `MEMORY.md` small and durable, while preserving daily details inside `memory/YYYY-MM-DD.md` files.

### What it does
- Compress dated memory files without losing historical structure
- Remove duplication and noise from permanent memory
- Keep permanent memory focused on must-read facts
- Avoid copying every daily memory into `MEMORY.md`

### Permanent vs daily memory

**Keep in `MEMORY.md`:**
- Stable user preferences
- Durable project configuration
- Workspace rules
- Active cross-session todos

**Keep in `memory/YYYY-MM-DD.md`:**
- Daily summaries
- Work logs
- Debugging details
- Temporary notes
- Historical progress records

### Installation
```bash
npx clawhub install memory-organizer
```

### Usage
```bash
# Scan memory files
node memory-organizer.js scan

# Compress one dated memory file in place
node memory-organizer.js compress 2026-03-08.md

# Selectively promote durable facts only
node memory-organizer.js merge 2026-03-08.md
```

### Rule
Do not merge every dated memory file into permanent memory. Promote only durable facts that should be loaded at the start of future sessions.

---

## 中文

### 描述
用干净的双层结构整理 OpenClaw 记忆。让 `MEMORY.md` 保持精简稳定，把每天的细节继续留在 `memory/YYYY-MM-DD.md` 里。

### 功能
- 压缩每日记忆文件，但保留历史结构
- 清理永久记忆中的重复和噪音
- 让永久记忆只保留必须长期读取的信息
- 避免把每天的记忆都复制进 `MEMORY.md`

### 永久记忆和每日记忆的边界

**适合放进 `MEMORY.md` 的内容：**
- 稳定的用户偏好
- 长期有效的项目配置
- 工作区规则
- 跨会话仍然有效的待办

**适合留在 `memory/YYYY-MM-DD.md` 的内容：**
- 每日总结
- 工作日志
- 调试细节
- 临时笔记
- 历史进展记录

### 安装
```bash
npx clawhub install memory-organizer
```

### 使用
```bash
# 扫描记忆文件
node memory-organizer.js scan

# 原地压缩某天的记忆文件
node memory-organizer.js compress 2026-03-08.md

# 只提炼长期有效信息到永久记忆
node memory-organizer.js merge 2026-03-08.md
```

### 规则
不要把每个日期的记忆都合并进永久记忆。只有那些未来每次开新会话都应该读到的稳定事实，才应该提升到 `MEMORY.md`。
