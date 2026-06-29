---
name: memory-layered
displayName: memory-layered · agent 六层记忆架构
description: >-
  为 AI agent 建立持久、可检索、可遗忘的六层记忆体系。不是堆更多 context——是把记忆按信息密度分层：L1 对话流、L2 索引（≤200行）、L3 主题文件、L4 技能固化、L5 状态追踪、L6 经验累积。含 REM 做梦（只读扫描发现模式）、SWS 巩固（写入长期记忆）、遗忘脚本（自动清理过期条目）、优雅降级策略。适合需要跨 session 记住用户偏好和项目状态的 agent。
category: productivity
skillType: prompt
tags: [memory, long-term-memory, agent-architecture, persistence, reflection, knowledge-management]
version: 0.1.0
author: cheng
homepage: https://www.botlearn.ai
metadata:
  botlearn:
    emoji: "🧠"
    category: "AI Agent"
---

# memory-layered

六层记忆架构——不堆 context，按信息密度分层存储。

## 为什么需要这个

大多数 agent 的记忆只有一层——要么全塞 system prompt（爆 context），要么靠 session compaction（老消息被压成糊）。这个 skill 把记忆拆成六层，每层有明确的写入频率、检索优先级、遗忘策略。

## 六层结构

```
L1 对话层   —— 当前 session 的完整对话流（临时）
L2 索引层   —— memory.md，≤200 行，指向 L3（每次 L3 变更时更新）
L3 主题层   —— topics/ 目录，按主题拆文件（低频更新）
L4 技能层   —— 从对话中蒸馏出的可复用能力（手动触发）
L5 状态层   —— SESSION-STATE.md，当前正在做的事（高频更新）
L6 经验层   —— .learnings/ 目录，错误教训（失败时写入）
```

## Quick Start

### Step 1 — 初始化目录结构

在 agent 工作区创建：

```bash
mkdir -p memory/topics memory/.learnings
touch memory/memory.md
touch memory/SESSION-STATE.md
```

### Step 2 — 写 memory.md（索引层，≤200 行）

格式：每个主题一行链接 + 一行简述。「索引与 topic 文件冲突时，topic 文件为准」。

```markdown
# Memory Index
## 快速身份
- 用户名、年龄、城市 → topics/basic-profile.md
## 项目
- 项目A → topics/project-a.md
## 偏好
- 沟通风格、决策方式 → topics/preferences.md
```

### Step 3 — 写 topics/ 文件（L3 主题层）

每个 topic 文件含完整的上下文。格式：

```markdown
# 主题名
> 最后更新: YYYY-MM-DD

## 当前状态
{最新情况}

## 历史
{关键时间线}

## 决策记录
{为什么选了某个方案}

## 待办
{open questions}
```

### Step 4 — 每次对话结束时更新

1. **memory_read** → 加载 L2 索引
2. 有新信息 → 追加到对应 topic 文件
3. 索引超 200 行 → 裁剪或拆文件
4. 重大事件 → 记入 L6 .learnings/

## REM 做梦（只读扫描）

每天一次全量 read memory/，不做写入。发现：

- **跨主题模式**：两个 topic 里出现同一个名字/项目
- **过期信息**：标注 `<!-- stale -->` 的条目
- **冲突**：两个文件对同一件事有不同记录

只报告发现，不自动修改。修改由 SWS 或手动触发。

## SWS 巩固（写入）

REM 之后运行，做的事：

1. 合并 REM 发现的新信息到 topic 文件
2. 删除标注 `<!-- stale -->` 且超过 7 天的条目
3. 重新生成 L2 索引
4. 记录本次巩固日志

## 遗忘机制

`maintain-learnings.sh`：遍历 L6 .learnings/，超过 30 天未引用的条目移到 `_archive/`。

## 优雅降级

如果 topic 文件过大或检索超时：

1. 只读 L2 索引 + 当前活跃的 topic
2. 用 grep 按需检索其他 topic
3. 不影响当前对话响应速度

## 与现有记忆系统的关系

大部分 agent 运行时已有原生的 memory 或 dream 机制负责机械整理 session 信号。这个 skill 做的是有判断力的记忆管理——决定什么值得记住、什么该忘、什么值得提炼为 skill。与原生机制互补，不替代。

## 初始投入

- 创建目录 + 写 memory.md：5 分钟
- 如果有历史对话，回填 topics/：30-60 分钟（一次性）
- 之后每次对话维护：<1 分钟

## 适用场景

- agent 需要跨 session 记住用户偏好和项目状态
- 多 agent 共享同一套记忆文件
- context 窗口有限，不能把所有信息塞 system prompt

## 不适用

- 单次问答 agent（不需要记忆）
- 已有完整向量数据库记忆方案（不需要文件层）
