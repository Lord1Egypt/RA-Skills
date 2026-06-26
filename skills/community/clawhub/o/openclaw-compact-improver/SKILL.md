---
name: openclaw-compact-improver
description: 优化 OpenClaw 4.2 的 /compact 压缩命令提示词，生成结构化摘要。当用户提到压缩效果差、摘要不完整、上下文丢失、/compact 格式不好，或要求改进压缩提示词时触发。
---

# OpenClaw Compact Improver

改进 `/compact` 命令的压缩摘要质量，参考 Claude Code 的 9 段结构化摘要格式。

## 当前 OpenClaw 的问题

OpenClaw 4.2 的压缩提示较为简单，缺少：
1. 结构化分段格式
2. 文件路径和代码片段的精确保留
3. 记忆验证行为指导
4. Pending tasks 的明确提取

## 结构化压缩摘要格式（目标格式）

当执行 `/compact` 或触发自动压缩时，使用以下 9 段格式：

```
<analysis>
[分析过程，确保覆盖所有要点：
- 用户的核心请求是什么
- 涉及了哪些文件和代码
- 遇到了什么错误/问题
- 当前工作进展到哪里]
</analysis>

<summary>
1. Primary Request and Intent:
   [用户的核心请求，一句话概括]

2. Key Technical Concepts:
   - [概念1]: [简要说明]
   - [概念2]: [简要说明]

3. Files and Code Sections:
   - [文件名1] ([为什么重要])
     ```[语言]
     [相关代码片段，完整可运行]
     ```
   - [文件名2] ...

4. Errors and Fixes:
   - [错误描述]:
     修复方法: [具体步骤]

5. Problem Solving:
   [问题解决过程，当前状态]

6. All User Messages:
   - [用户消息1（原始表述）]
   - [用户消息2（原始表述）]

7. Pending Tasks:
   - [任务1，含具体文件路径]
   - [任务2，含具体文件路径]

8. Current Work:
   [正在做的内容，含文件名+行号+当前代码片段]

9. Optional Next Step:
   [下一步，直接引用用户最近的原话]
</summary>
```

## 注入方法

将上述格式注入到 `~/.openclaw/openclaw.json` 的 `agents.defaults.systemPrompt` 或通过 HOOK 注入：

```bash
# 查看当前 compact 提示词
openclaw config get agents.defaults.systemPrompt | grep -i compact
```

## Claude Code 压缩行为的关键差异

Claude Code 压缩时有这些 OpenClaw 没有的细节：

1. **文件路径完整性**：压缩摘要中保留精确的文件路径和行号
2. **代码片段可运行**：不是描述性文字，而是可直接使用的代码
3. **Pending tasks 明确**：用户说"下一步要做 X" 会被显式记录
4. **microCompact 机制**：不是等 token 阈值触发，而是工具结果即时压缩

## 手动优化 /compact

如果无法修改配置，可以在触发压缩时给模型明确的格式指令：

```
请用以下格式压缩对话，只输出 <analysis> 和 <summary> 部分，
不要使用任何工具，纯文本响应：

<analysis>
[你的分析，确保覆盖所有要点]
</analysis>

<summary>
1. Primary Request and Intent:
   ...

[其余 8 个部分]
</summary>
```
