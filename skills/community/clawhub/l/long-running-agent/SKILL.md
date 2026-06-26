---
name: long-running-agent
description: |
  长时间运行智能体编排框架。让AI智能体能够跨会话持续工作并完成复杂任务。
  
  使用场景：
  - 用户说 "创建一个新项目"、"开始一个项目"、"新建任务"、"启动项目"
  - 用户说 "继续项目"、"继续工作"、"接着做"、"继续开发"
  - 用户说 "更新进度"、"记录进度"、"保存进度"
  - 用户说 "项目状态"、"查看进度"、"做到哪了"
  - 用户说 "列出项目"、"所有项目"、"我有哪些项目"
  - 用户说 "暂停项目"、"存档项目"
  - 用户需要执行多步骤、长时间、跨会话的任务
  - 用户需要AI持续追踪工作进度和上下文
  - 用户需要AI记住之前尝试过但失败的方法
  
  核心功能：
  - 创建新项目（自动生成 PROJECT.md, CHANGELOG.md）
  - 继续项目（自动读取进度，从断点继续）
  - 更新进度（自动更新 CHANGELOG.md）
  - Ralph Loop 自动推进（解决智能体惰性）
  - 多项目管理
  - 项目状态概览
  - 失败方法记录（防止重复尝试）
metadata:
  openclaw:
    emoji: "🔄"
    requires:
      bins:
        - git
---

# Long-Running Agent - 长时间运行智能体编排框架

基于 Anthropic 论文《Long-Running Claude for Scientific Research》实现，让 AI 智能体能够跨会话持续工作并完成复杂任务。

## 核心理念

**问题**：AI智能体每次会话都是"新生的"，没有记忆延续。

**解决方案**：通过文件系统作为"外部大脑"，实现跨会话的持续工作能力。

---

## 快速开始

### 创建新项目

当用户说 "创建一个[项目名]项目" 时：

```
Step 1: 确认项目名称和目标
Step 2: 在 workspace/tasks/{项目名}/ 创建目录
Step 3: 生成 PROJECT.md（项目简报）
Step 4: 生成 CHANGELOG.md（进度追踪）
Step 5: 开始第一项任务
```

**示例对话**：

```
用户: 创建一个博客系统项目，用 Node.js 实现

QClaw: ✅ 项目已创建: 博客系统

📁 位置: tasks/博客系统/
📄 PROJECT.md - 项目简报
📄 CHANGELOG.md - 进度追踪

🎯 目标: 用 Node.js 实现博客系统

下一步: 定义详细需求

请告诉我：
1. 博客系统需要哪些功能？
2. 使用什么数据库？
```

### 继续项目

当用户说 "继续[项目名]项目" 时：

```
Step 1: 读取 tasks/{项目名}/PROJECT.md（了解上下文）
Step 2: 读取 tasks/{项目名}/CHANGELOG.md（了解进度）
Step 3: 执行定向协议（PROJECT.md 中定义）
Step 4: 从"下一步"继续工作
```

**示例对话**：

```
用户: 继续博客系统项目

QClaw: 📋 继续项目: 博客系统

📊 当前状态: Phase 2 进行中
📈 进度: 5/12 任务，42%

🔄 Ralph Loop: 迭代 4/20

📍 下一步: 实现文章 API

[开始工作...]
```

### 查看项目状态

```
用户: 我有哪些项目？

QClaw: 📋 项目列表 (共 3 个)

名称                    | 状态           | 进度    
------------------------|----------------|---------
博客系统                | Phase 2        | 42%     
用户管理API             | 已完成         | 100%    
数据分析工具            | Phase 1        | 15%     
```

---

## 文件结构

每个项目都有标准结构：

```
workspace/
├── tasks/
│   └── {项目名}/
│       ├── PROJECT.md      # 项目简报（目标、成功标准、定向协议）
│       ├── CHANGELOG.md    # 进度追踪（跨会话记忆）
│       ├── tests/          # 测试预言机
│       └── src/            # 项目源代码
└── memory/
    └── YYYY-MM-DD.md       # 每日记录
```

---

## 核心组件

### 1. PROJECT.md - 项目简报

每个项目的"说明书"：

```markdown
# PROJECT.md - {项目名称}

## 项目概述
一句话描述项目做什么

## 交付物
- [ ] 交付物1
- [ ] 交付物2

## 成功标准
可量化的完成定义：
- 所有测试通过
- 测试覆盖率 > 80%
- 功能完整可用

## 定向协议
每个会话开始时执行：
1. 读取 CHANGELOG.md 的"当前状态"和"下一步"
2. 运行快速测试确认无回归
3. 从优先列表选择任务
4. 开始工作

## 不要做的事
- ❌ 跳过定向协议
- ❌ 重新尝试已记录为"失败"的方法
- ❌ 在测试失败时提交代码
```

### 2. CHANGELOG.md - 进度追踪

**最重要的文件！** 智能体的"长期记忆"：

```markdown
# CHANGELOG.md

## 当前状态: Phase 2 进行中
**进度**: 5/12 任务完成，42%
**下一步行动**: 
1. 实现文章 API
2. 编写测试

**Ralph Loop 状态**:
迭代: 4/20
成功标准: 所有测试通过，覆盖率>80%

## 失败的方法
> ⚠️ 最重要！防止重复尝试

### 方法：使用 Python 实现 - 2026-03-19
**尝试**: 使用 Python 创建项目
**结果**: 系统未安装 Python
**教训**: 当前环境优先使用 JavaScript/TypeScript

## 完成的任务
### 2026-03-19: 用户模型实现
- 实现 User 数据类
- 10 个测试用例通过
- 提交: abc123

## 会话日志
### Session 4 - 2026-03-19
**完成**: 用户 API 实现
**下次继续**: 文章 API
```

### 3. 测试预言机

让智能体能自主判断是否在进步：

| 类型 | 说明 | 示例 |
|------|------|------|
| 参考实现 | 已知的正确输出 | 预期输出文件 |
| 量化目标 | 明确的数值指标 | 覆盖率 > 80% |
| 测试套件 | 可执行的测试 | npm test |

### 4. Ralph Loop

解决"智能体惰性"问题——智能体有时会在完成部分任务后找借口停下来。

**实现**：循环检查，确保真正完成

```
for i in 1..MAX_ITERATIONS:
    result = agent.work(task)
    if result.includes("DONE") and verify_completion():
        break
    else:
        agent.continue("你确定完成了吗？请验证：{success_criteria}")
```

**在 CHANGELOG.md 中声明**：

```markdown
**Ralph Loop 状态**:
迭代: 1/20
成功标准: 所有测试通过，覆盖率>80%
```

每次会话检查是否达到标准，未达到则继续推进。

### 5. Git 协调

每个"有意义的工作单元"后提交代码：

```
一个功能实现 → 一次提交
一个 bug 修复 → 一次提交
一个重构 → 一次提交
```

---

## 命令参考

| 用户指令 | 触发条件 | QClaw 行为 |
|----------|----------|------------|
| 创建项目 | "创建/开始/新建/启动" + 项目名 | 生成 PROJECT.md, CHANGELOG.md，开始第一项任务 |
| 继续项目 | "继续/接着做/继续开发" + 项目名 | 读取进度，从断点继续 |
| 更新进度 | "更新进度/记录进度/保存进度" | 更新 CHANGELOG.md |
| 项目状态 | "项目状态/查看进度/做到哪了" | 显示当前进度和下一步 |
| 列出项目 | "列出项目/所有项目/我有哪些项目" | 显示所有项目及其状态 |
| 暂停项目 | "暂停项目/存档项目" | 标记项目为暂停状态 |

---

## 工作规则

### 必须做

- ✅ 每个子任务完成后更新 CHANGELOG.md
- ✅ 先写测试再写代码（TDD）
- ✅ 记录所有失败的方法（最重要！）
- ✅ 使用定向协议确保从正确位置开始
- ✅ 简洁输出（成功5-10行，失败20行）

### 禁止做

- ❌ 跳过定向协议
- ❌ 重新尝试已记录为"失败"的方法
- ❌ 在测试失败时提交代码
- ❌ 打印完整数组或日志
- ❌ 冗长的描述

---

## 输出规范

### 创建项目时

```
✅ 项目已创建: {项目名}

📁 位置: tasks/{项目名}/
📄 PROJECT.md - 项目简报
📄 CHANGELOG.md - 进度追踪

🎯 目标: {项目目标}
📊 成功标准: {成功标准}

下一步: {第一个任务}
```

### 继续项目时

```
📋 继续项目: {项目名}

📊 当前状态: {状态}
📈 进度: {X/Y 任务，Z%}

🔄 Ralph Loop: 迭代 {N}/20

📍 下一步: {下一个任务}

[开始工作...]
```

### 更新进度时

```
📝 进度已更新

状态: {新状态}
进度: {X/Y → X+1/Y}
完成: {刚完成的任务}
下一步: {新任务}
```

---

## 与 HEARTBEAT 集成

可以将项目检查加入 HEARTBEAT.md，实现后台持续推进：

```markdown
## 当前 Ralph Loop 任务

```
项目: 博客系统
迭代: 4/20
成功标准: 所有测试通过
```

检查：是否需要继续推进？
```

---

## 模板文件

详见 `references/` 目录：

- [project-template.md](references/project-template.md) - PROJECT.md 完整模板
- [changelog-template.md](references/changelog-template.md) - CHANGELOG.md 完整模板
- [ralph-loop.md](references/ralph-loop.md) - Ralph Loop 详细说明
- [best-practices.md](references/best-practices.md) - 最佳实践指南

---

## 脚本工具

### init-project.js

初始化新项目：

```bash
node scripts/init-project.js <项目名> --desc "项目描述"
```

### list-projects.js

列出所有项目：

```bash
node scripts/list-projects.js
```

---

## 错误处理

| 错误 | 处理方式 |
|------|----------|
| 项目不存在 | 提示用户创建或列出可用项目 |
| CHANGELOG.md 损坏 | 尝试恢复，无法恢复则提示重新创建 |
| 测试失败 | 记录失败原因到 CHANGELOG，继续调试 |
| Git 冲突 | 提示用户手动解决 |

---

## 示例项目

查看 `examples/task-planner-demo/` 目录，这是一个完整的示例项目，展示了：

- ✅ 完整的 PROJECT.md 和 CHANGELOG.md
- ✅ 失败方法记录（Python → TypeScript 迁移）
- ✅ Ralph Loop 迭代过程（3次迭代完成任务）
- ✅ 测试驱动开发流程

---

## 参考资料

- [Anthropic 论文](https://www.anthropic.com/research/long-running-tasks)
- [参考实现 smsharma/clax](https://github.com/smsharma/clax)
