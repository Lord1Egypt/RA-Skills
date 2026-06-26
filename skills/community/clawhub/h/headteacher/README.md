<div align="center">

# 班主任.Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

一个面向教师和班主任的工作台 Skill。  
它的重点不是“模仿老师说话”，而是帮助教师持续管理学生数据，并按需生成日常需要的文件。

[English](README_EN.md)

[安装](#安装) · [使用](#使用) · [工作台模型](#工作台模型)

</div>

---

## 这是什么

`班主任.Skill` 的核心是两种能力：

1. 数据的记录、读写以及动态读写。  
   包括一次性导入、日常动态添加、纵向读取某个学生、横向读取部分学生或全班。
2. 按需生成特定的 Office 文件。  
   包括排座表、值日表、家长会 PPT，以及其他通知或记录文档。

第一版默认首选接入 **飞书多维表格**。  
`Notion` 和 `Obsidian` 暂时作为后续开发方向保留。

飞书接入方式会按运行环境自动分流：

- 如果 Skill 运行在 OpenClaw 中，优先检测并使用 OpenClaw 官方飞书插件 `openclaw-lark`
- 如果 Skill 运行在 Codex、Claude Code 或其他本地 Agent 中，沿用原有 `lark-cli` 方案

## 第一版范围

### 现在可用

- 飞书多维表格工作台初始化
- 标准班主任数据模型
- 已有飞书多维表格的迁移检查
- 本地产物登记

### 后续开发

- Notion：等待后续开发，计划通过 MCP 的方式连接
- Obsidian：等待后续开发，计划使用 Obsidian 的 CLI

## 工作台模型

第一版围绕这些核心对象展开：

- 学生主档
- 考试批次
- 成绩明细
- 成长事件
- 家校沟通
- 座位安排
- 值日安排
- 班委任命
- 产物索引

飞书多维表格是第一后端，但 Skill 本身真正关心的是班级数据和文件生成能力。

## 安装

不需要手动记复杂命令。  
如果你在使用 Agent、OpenClaw 或其他类似工具，直接发送下面这句提示词即可：

```bash
请帮我安装这个技能：https://github.com/YZDame/headteacher-skill
```

安装完成后，再告诉你的 Agent：

```bash
请帮我启用班主任.Skill，并先带我完成飞书多维表格的初始化。
```

如果你是在 OpenClaw 中使用本 Skill，飞书多维表格初始化应优先通过 OpenClaw 官方飞书插件完成，而不是默认要求你安装 `lark-cli`。

如果你后续要使用“按需生成文件”这项能力，还需要本地具备 Office 相关的 Skill 套装，用来处理：

- `.docx`
- `.xlsx`
- `.pptx`

具体参考: Anthropic Skills 仓库中的 Office 相关 Skill  
  [https://github.com/anthropics/skills/tree/main/skills](https://github.com/anthropics/skills/tree/main/skills)

## 使用

触发 Skill 后，默认按以下顺序进入：

1. 环境检查
2. 后端选型
3. 工作台初始化
4. 正式运行时任务

默认首选接入：

- 飞书多维表格

其中飞书多维表格的接入会按环境自动切换：

- OpenClaw -> 官方飞书插件 `openclaw-lark` + 飞书 API
- Codex / Claude Code / 本地 Agent -> `lark-cli`

后续计划支持：

- Notion
- Obsidian

典型请求：

- “帮我初始化一个高一 3 班的班主任工作台”
- “把这份学生名单和历史成绩一次性导入进去”
- “记一条学生表现：张三今天课后主动来问题”
- “按时间轴整理一下张三这学期的成绩和表现”
- “看一下这次月考后全班哪些学生需要重点跟进”
- “按成绩、性别和身高重新排一个座位表”
- “根据最近一次考试和这段时间的日常表现生成家长会 PPT”

## 仓库结构

```text
headteacher-skill/
├── SKILL.md
├── prompts/
├── references/
├── tools/
├── docs/
└── paper/
```

其中：

- `SKILL.md` 负责触发条件、主流程和运行时路由
- `prompts/` 负责 setup、迁移、runtime 和文件生成的操作指引
- `references/` 负责标准模型与规则说明
- `tools/` 负责初始化、迁移检查和产物登记

## 注意

- 这个 Skill 不再以“角色扮演班主任”为目标
- 不会默认覆盖已有的飞书多维表格
- 如果用户提供已有工作台，会先做检查与迁移建议
- 敏感字段默认按“少展示、先确认”处理
