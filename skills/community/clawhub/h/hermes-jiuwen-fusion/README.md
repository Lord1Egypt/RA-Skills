# hermes-jiuwen-fusion

> 融合 Hermes Agent 与 JiuwenClaw 精华的自进化多Agent协作系统

## 简介

本 Skill 从两个优秀的 AI Agent 框架中提取精华设计思想，融合为 OpenClaw 可用的外挂 Skill：

| 来源 | 融合的能力 |
|------|-----------|
| **[Hermes Agent](https://github.com/NousResearch/hermes-agent)** | 闭环学习体系、自动技能沉淀（复杂任务后生成 SKILL.md）、并行子代理编排 |
| **[JiuwenClaw](https://gitcode.com/openJiuwen/jiuwenclaw)** | Skills 自纠错、上下文瘦身、分层记忆、事件驱动状态机 |

## 核心特性

- **三角色协作**：项目经理(PM) + 执行者(executor) + 监督者(supervisor) + 品质管理(qa)
- **闭环学习**：执行 -> 复盘 -> 沉淀 -> 复用，越用越聪明
- **自动技能沉淀**：复杂任务完成后自动生成 SKILL.md 保存经验
- **技能自纠错**：识别执行中的异常，自动修正技能定义
- **上下文瘦身**：长任务中主动压缩历史上下文，控制 token 消耗
- **三级记忆**：工作记忆(当前会话) + 项目记忆(跨会话) + 技能库(长期知识)
- **事件驱动状态机**：任务进展实时同步，状态流转清晰可控

## 安装方式

### 方式一：通过 ClawHub 安装（推荐）

```bash
npx clawhub install hermes-jiuwen-fusion --workdir ~ --dir .workbuddy/skills
```

### 方式二：手动安装

1. 克隆本仓库
2. 将 `SKILL.md` 复制到 `~/.workbuddy/skills/hermes-jiuwen-fusion/`

## 使用方式

安装后，当用户提出复杂任务时，Skill 会被自动触发，主代理切换为项目经理模式，按任务复杂度启动三角色流程：

- **S/A级（高难度）**：执行者 -> 监督者审查 -> 品质管理验收 -> PM汇报
- **B级（中等）**：执行者 -> 品质管理验收 -> PM汇报
- **C/D级（简单）**：执行者完成 -> PM直接汇报

## 致谢

- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) - 闭环学习与技能沉淀设计
- [openJiuwen/jiuwenclaw](https://gitcode.com/openJiuwen/jiuwenclaw) - 多智能体协同与自演进设计

## License

MIT-0
