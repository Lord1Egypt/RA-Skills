---
name: long-running-harness
description: >
  长时程 Agent 项目工作流框架（基于 Anthropic "Effective Harnesses for Long-Running Agents"）。
  用于创建、管理和调度跨多个上下文窗口的长期项目任务。
  Use when: 启动新项目、初始化项目工作流、管理项目任务列表、调度子Agent增量开发、
  恢复项目状态、生成项目进度报告。触发短语包括：
  "启动项目"、"初始化项目"、"创建工作流"、"项目进度"、"继续开发"、
  "管理任务列表"、"分配任务"、"next feature"、"project status"。
---

# 长时程 Agent 工作流框架

> 基于 Anthropic 工程团队的 [Effective Harnesses for Long-Running Agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) 方法论，适配 OpenClaw 环境。

---

## 核心原则

1. **持久化优于记忆** — 用文件系统记录状态，不依赖 Agent 上下文记忆
2. **结构化优于自由文本** — 关键状态用 JSON，进度日志用 Markdown
3. **验证优于声明** — 每个功能完成后必须验证，不接受未测试的 "完成"
4. **增量优于大步** — 每次 Agent 会话只做一个功能点，保持可回滚
5. **标准化优于临时** — 固定的启动例程和结束例程，减少混乱

---

## 项目结构

每个受管理项目遵循以下标准结构：

```
projects/<project-name>/
├── PROJECT.md              # 项目概述、目标、技术栈
├── progress.md             # Agent 工作日志（每次会话追加）
├── features.json           # 功能列表（状态追踪，仅修改 passes 字段）
├── init.sh                 # 环境初始化脚本（可选）
├── src/                    # 项目源码
└── tests/                  # 测试代码（如有）
```

---

## 生命周期

### 阶段一：初始化（Init）

当用户要求启动新项目或初始化工作流时执行：

1. **创建项目目录** `projects/<project-name>/`
2. **编写 `PROJECT.md`** — 包含：
   - 项目名称和目标
   - 技术栈和依赖
   - 验收标准
   - 关键约束
3. **编写 `features.json`** — 功能列表，格式如下：
   ```json
   {
     "project": "项目名称",
     "created": "2026-03-18",
     "features": [
       {
         "id": "feat-001",
         "name": "功能名称",
         "description": "功能详细描述",
         "category": "functional|infra|docs|perf|fix",
         "priority": "high|medium|low",
         "passes": false,
         "tests": [
           "测试步骤 1",
           "测试步骤 2"
         ],
         "notes": ""
       }
     ]
   }
   ```
4. **创建 `progress.md`** — 模板：
   ```markdown
   # 项目工作日志

   ## 初始化
   - 日期：2026-03-18
   - 初始化人：主 Agent
   - 功能总数：N
   ```
5. **初始化 git** — `git init` + 首次提交
6. 如果适用，**编写 `init.sh`**

**重要：** 功能列表要尽量详尽，把大功能拆成小功能。200 个小功能 > 10 个大功能。

### 阶段二：增量开发（Each Session）

当用户说"继续开发"、"next feature"、"继续项目"或调度子Agent开发时：

**启动例程（每个会话必须执行）：**
1. `pwd` 确认工作目录
2. `cat projects/<name>/progress.md` — 读取工作日志
3. `git log --oneline -10` — 查看最近提交
4. `cat projects/<name>/features.json` — 读取功能列表
5. 选择优先级最高且 `passes: false` 的功能
6. 运行 `init.sh`（如有）+ 基础验证测试
7. 确认环境正常后，开始实现

**工作约束：**
- 每次**只做一个功能**
- 实现完成后**必须验证**（运行测试、手动检查等）
- 验证通过后才能将 `features.json` 中对应功能的 `passes` 改为 `true`
- **禁止**删除或修改功能条目（只改 `passes` 和 `notes` 字段）

**结束例程（每个会话必须执行）：**
1. 更新 `features.json` 中完成状态
2. 追加会话记录到 `progress.md`：
   ```markdown
   ## 会话 N — 日期
   - **目标功能：** feat-XXX - 功能名称
   - **状态：** ✅ 完成 / ⏳ 部分完成 / ❌ 失败
   - **完成内容：** 具体做了什么
   - **遇到的问题：** 问题描述和解决方案
   - **下次继续：** 待办事项
   - **Git commits：** hash - message
   ```
3. `git add . && git commit -m "feat: 完成功能描述"`

### 阶段三：进度报告

当用户问"项目进度"、"project status"时：

1. 读取 `features.json`
2. 统计完成率（passes: true / 总数）
3. 按优先级列出未完成功能
4. 读取 `progress.md` 最近条目
5. 生成进度摘要

输出格式：
```
📋 项目进度：项目名称
━━━━━━━━━━━━━━━━━━
✅ 完成：X / Y（Z%）
🔴 待做（高优先级）：...
🟡 待做（中优先级）：...
🟢 待做（低优先级）：...
━━━━━━━━━━━━━━━━━━
最近会话：[简要摘要]
```

---

## 调度子Agent（sessions_spawn）

将单个功能委派给子Agent开发时，task 描述必须**自包含**：

```json
{
  "task": "## 任务：实现 feat-XXX 功能\n\n### 项目信息\n- 路径：projects/project-name/\n- 技术栈：...\n\n### 你的目标\n实现以下功能并验证：\n[功能描述]\n\n### 启动例程\n1. 读取 projects/project-name/features.json 找到 feat-XXX\n2. 读取 projects/project-name/progress.md 了解历史\n3. 运行 git log --oneline -5\n4. 运行 projects/project-name/init.sh（如有）\n5. 运行基础测试确认环境正常\n\n### 工作要求\n- 只做这一个功能\n- 完成后必须验证\n- 结束时更新 features.json 的 passes 字段\n- 结束时追加 progress.md 日志\n- 结束时 git commit",
  "sessionKey": "alpha",
  "runTimeoutSeconds": 600
}
```

**关键：** task 必须包含所有上下文。子Agent看不到主对话历史。

---

## 定时巡检（Cron Job）

对于重要项目，可设置定时 cron job 巡检进度：

```
schedule: kind=cron, expr="0 */4 * * *"
payload: kind=agentTurn, message="读取 projects/<name>/progress.md 和 features.json，检查是否有功能卡住超过3个会话未完成。如有，输出简要报告。"
```

---

## 故障模式预防

| 故障模式 | 预防措施 |
|---------|---------|
| Agent 试图一次性做完所有功能 | 强制每次只选一个 `passes: false` 的功能 |
| Agent 过早宣布项目完成 | `features.json` 有明确的状态追踪 |
| Agent 留下的代码有 bug | 启动时运行基础测试；结束时 git commit 便于回滚 |
| Agent 花时间理解环境 | 使用 `init.sh` 标准化启动 |
| 上下文丢失导致重复工作 | `progress.md` + git log 提供完整历史 |
| 功能未真正完成就标记 passes | 要求验证后才能修改 passes 字段 |

---

## 通用领域扩展

此框架不限于软件开发。对于非代码类长期任务：

- **研究项目：** features.json 中的 tests 改为 research objectives，passes 表示研究是否完成
- **写作项目：** features 拆分为章节/段落，passes 表示是否已写完并审校
- **数据分析：** features 拆分为分析步骤，passes 表示结果是否已验证

使用不同 category 区分：`research|writing|analysis|infra|docs`
