---
name: joycode
version: 1.0.0
description: 通过 shell 控制 JoyCode CLI 工具进行代码生成和 AI 辅助编程。使用场景：(1) 用户要求代码生成、代码补全或编程帮助 (2) 需要使用 AI 助手进行代码审查 (3) 需要在终端中进行交互式编程对话 (4) 需要执行自动化代码任务
---

# JoyCode CLI 代码生成助手

## 安装

```bash
# 使用 npm 全局安装
npm install -g joycode-cli

# 验证安装
joycode-cli --version
```

## 核心命令

### 交互模式

```bash
# 启动交互式 TUI 界面
joycode-cli

# 带问题启动
joycode-cli "如何使用 Rust 编写一个 Hello World 程序？"
```

### 自动化模式

```bash
# 执行简单任务
joycode-cli exec "统计当前项目代码行数"

# 全自动模式（允许文件编辑）
joycode-cli exec --full-auto "为 utils.ts 编写单元测试"
```

### 会话管理

```bash
# 恢复上次会话
joycode-cli resume --last

# 通过会话 ID 恢复
joycode-cli resume <SESSION_ID>

# 打开会话列表选择
joycode-cli resume
```

### 登录认证

```bash
# 交互式登录 JoyCode 账号
joycode-cli login
```

## 斜杠命令（交互模式中使用）

| 命令 | 功能 |
|------|------|
| `/quit` | 退出程序 |
| `/logout` | 退出登录 |
| `/new` | 开始新对话 |
| `/undo` | 撤销上一步操作 |
| `/diff` | 查看 Git 差异 |
| `/compact` | 压缩对话历史 |
| `/init` | 初始化 AGENTS.md |
| `/review` | AI 代码审查 |
| `/approvals` | 动态修改审批策略 |

## 常用工作流

1. **代码生成**: `joycode-cli exec --full-auto "为 src/main.ts 编写单元测试"`
2. **代码审查**: 在交互模式输入 `/review`
3. **项目初始化**: `joycode-cli init`
4. **恢复会话**: `joycode-cli resume --last`
