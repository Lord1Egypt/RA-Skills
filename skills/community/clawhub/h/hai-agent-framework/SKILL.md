# HAI Agent Framework

**版本：** 1.0.0  
**作者：** 小 D  
**描述：** 企业级 AI Agent 框架 - Hook 事件系统、自动记忆抽取、核心 Agent 定义

---

## 🚀 功能特性

### 1. Hook 事件系统

在关键事件发生时自动触发脚本，实现：
- 会话开始/结束自动处理
- 工具调用前后验证
- 文件操作审计
- 自定义事件响应

**支持的 Hook 事件：**
- `SessionStart` - 会话开始
- `SessionEnd` - 会话结束
- `PreToolUse` - 工具调用前
- `PostToolUse` - 工具调用后
- `UserMessage` - 用户消息
- `AgentResponse` - Agent 回复前

### 2. 自动记忆抽取

从对话中自动学习：
- 用户偏好提取
- 挫折信号检测
- 成功模式识别
- 纠正记录保存
- 决策追踪

### 3. 核心 Agent 定义

预置 4 个专业 Agent：
- **code-reviewer** - 代码审查专家
- **test-generator** - 测试用例生成
- **security-scanner** - 安全扫描专家
- **documentation-writer** - 文档撰写专家

### 4. 四层记忆架构

- **L1 会话记忆** - 当前对话记录
- **L2 项目记忆** - 项目特定上下文
- **L3 全局记忆** - 用户偏好和习惯
- **L4 市场记忆** - 共享知识和规则

---

## 📦 安装

```bash
clawhub install hai-agent-framework
```

---

## 🔧 配置

### 1. 启用 Hook

在 `.hai/hooks/` 目录下创建 Hook 配置文件：

```json
{
  "name": "load-memory",
  "description": "加载用户记忆",
  "event": "SessionStart",
  "priority": 100,
  "enabled": true,
  "action": {
    "type": "script",
    "script": ".hai/scripts/load-memory.py"
  }
}
```

### 2. 使用 Agent

在任务中指定 Agent：

```markdown
---
agent: code-reviewer
---

请审查这段代码...
```

### 3. 记忆抽取

自动运行，无需配置。对话记录会自动分析并保存到 `memory/` 目录。

---

## 📖 使用示例

### 示例 1：会话开始加载记忆

```bash
python3 .hai/scripts/hook-executor.py SessionStart
```

### 示例 2：工具调用验证

```bash
python3 .hai/scripts/hook-executor.py PreToolUse \
  --context '{"tool":"write","args":{"path":"test.txt"}}'
```

### 示例 3：对话分析

```bash
python3 .hai/scripts/conversation-analyzer.py \
  --text "我喜欢用深色模式，不要用浅色"
```

---

## 📁 目录结构

```
.hai/
├── agents/           # Agent 定义
│   ├── code-reviewer.md
│   ├── test-generator.md
│   ├── security-scanner.md
│   └── documentation-writer.md
├── hooks/            # Hook 配置
│   ├── SessionStart/
│   ├── SessionEnd/
│   ├── PreToolUse/
│   └── PostToolUse/
├── scripts/          # 执行脚本
│   ├── hook-executor.py
│   ├── load-memory.py
│   ├── save-summary.py
│   ├── validate-params.py
│   └── conversation-analyzer.py
├── rules/            # 用户规则
│   └── *.local.md
└── memory/           # 记忆文件
    ├── transcript/
    ├── project/
    └── global/
```

---

## 🧪 测试

```bash
# 测试 Hook 系统
python3 .hai/scripts/hook-executor.py --list

# 测试 SessionStart Hook
python3 .hai/scripts/hook-executor.py SessionStart

# 测试对话分析
python3 .hai/scripts/conversation-analyzer.py --text "测试文本"
```

---

## 📊 效果

### Hook 系统
- ✅ 自动加载用户记忆
- ✅ 自动保存会话总结
- ✅ 工具调用安全验证

### 记忆抽取
- ✅ 用户偏好自动学习
- ✅ 纠正记录自动保存
- ✅ 决策追踪

### Agent 定义
- ✅ 标准化 System Prompt
- ✅ 专业化分工
- ✅ 可并行执行

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub:** https://github.com/your-repo/hai-agent-framework

---

## 📄 License

MIT

---

*HAI Agent Framework v1.0 · 2026-04-03*
