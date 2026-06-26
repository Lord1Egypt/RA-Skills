# Multi-User Long-Term Memory Skill

为 OpenClaw Agent 提供多用户长期记忆管理能力。

## 📖 概述

这个 Skill 允许 Agent 为不同用户维护独立的长期记忆文件，适用于群聊、多用户对话等场景。

## 👤 用户标识规则

**核心规则**：用于区分记忆的用户名取自 `sender_id` 中 `|` 符号**以前**的部分。

### 示例

| sender_id | 提取的用户名 | 记忆文件名 |
|-----------|-------------|-----------|
| `hzg-demo-appWillNing\|s-24485376` | `hzg-demo-appWillNing` | `hzg-demo-appWillNing.md` |
| `alice\|session-123` | `alice` | `alice.md` |
| `bob_channel\|xyz` | `bob_channel` | `bob_channel.md` |
| `no_pipe_user` | `no_pipe_user` | `no_pipe_user.md` |

### 设计理由

- `|` 前通常代表用户标识
- `|` 后通常代表会话或实例标识
- 同一用户的不同会话应共享记忆

## 📁 文件结构

```
~/.openclaw/workspace/skills/multi-user-long-term-memory/
├── SKILL.md              # Agent 使用的 Skill 文档
├── README.md             # 本文件
├── references/
│   └── user-memory.js    # 核心实现脚本
└── users/
    ├── {username}.md     # 各用户的记忆文件
    └── .gitkeep
```

## 🚀 使用方法

### 作为 Node.js 模块

```javascript
const { get, save, append, init } = require('./references/user-memory.js');

// 初始化用户记忆
init('hzg-demo-appWillNing|s-24485376', 'WillNing');

// 追加记忆
append('hzg-demo-appWillNing|s-24485376', '偏好：使用简体中文交流');

// 读取记忆
const memory = get('hzg-demo-appWillNing|s-24485376');
console.log(memory);
```

### 命令行使用

```bash
# 初始化用户记忆
node references/user-memory.js init "hzg-demo-appWillNing|s-24485376" "WillNing"

# 追加记忆
node references/user-memory.js append "hzg-demo-appWillNing|s-24485376" "偏好：使用简体中文交流"

# 读取记忆
node references/user-memory.js get "hzg-demo-appWillNing|s-24485376"

# 保存记忆（覆盖）
node references/user-memory.js save "hzg-demo-appWillNing|s-24485376" "新的记忆内容"
```

## 📝 记忆文件格式

每个用户的记忆文件是 Markdown 格式：

```markdown
# Memory for User: WillNing

Username: hzg-demo-appWillNing
Created: 2026-03-17T10:00:00.000Z

---

## 2026-03-17T10:05:00.000Z

偏好：使用简体中文交流

## 2026-03-17T10:10:00.000Z

项目：正在开发多用户记忆系统
```

## 🔒 安全性

- 仅读写 workspace 内的文件
- 用户ID经过安全清理（移除特殊字符）
- 不执行任何需要提升权限的操作

## 📦 依赖

- Node.js 内置模块（fs, path）
- 无外部依赖

## 📄 许可

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
