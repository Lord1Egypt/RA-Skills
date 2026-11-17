---
slug: "learn-cog-free"
name: "learn-cog-free"
version: 1.0.1
displayName: "个性化学习助手免费版"
summary: "免费版AI学习助手，支持概念解释、语言学习与学习指南生成。。个性化学习助手免费版，提供基础AI辅导功能. 支持概念解释、语言学习基础与学习指南生成. 适用于学生的日常学习与知识获取."
summary_zh: "免费版AI学习助手，支持概念解释、语言学习与学习指南生成。。个性化学习助手免费版，提供基础AI辅导功能. 支持概念解释、语言学习基础与学习指南生成. 适用于学生的日常学习与知识获取."
license: "MIT"
description: "|-. 适用于需要learn cog相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  个性化学习助手免费版，提供基础AI辅导功能.
  支持概念解释、语言学习基础与学习指南生成.
  适用于学生的日常学习与知识获取.
tools:
  - read
  - exec
  - write
homepage: ""
tags:
  - 通用办公
  - learn
  - cog
  - automation
  - productivity
  - 工具
  - 效率
  - 知识
  - 文档
  - 概念拆解
category: "Automation"
pricing_tier: free
---
# 个性化学习助手（免费版）

AI驱动的学习助手，支持概念解释、语言学习与学习指南生成.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 个性化学习助手免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

### 概念解释（Concept Explanations）
多角度解释概念，适配不同理解水平：

- **概念拆解**：如"Explain quantum entanglement like I'm 10 years old"
- **多角度解释**：如"Explain recursion using 3 different analogies"
- **作业辅导**：逐步解答数学、物理等问题并解释每步
- **代码调试**：解释代码问题并帮助修复

### 语言学习（Language Learning）

基础语言学习辅导：

- **语法讲解**：如"Explain Japanese particles with examples"
- **词汇构建**：如"Teach me 20 essential business Chinese phrases"
- **写作反馈**：检查语言学习写作并提供修改建议

### 学习指南（Study Guides）
生成基础学习材料：

- **学习指南**：如"Create a study guide for AP Chemistry exam"
- **摘要笔记**：如"Summarize Chapter 5 of my biology textbook"
- **速查表**：如"Create a one-page reference for Python syntax"

### 概念拆解

针对概念拆解,自动解析输入参数、调度任务队列、格式化输出,返回结构化响应.
**输入**: 用户提供概念拆解相关的配置参数、输入数据和处理选项.
**输出**: 返回概念拆解的处理结果。- 验证返回数据的完整性和格式正确性
- 参考`概念拆解`的配置文档进行参数调优
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. 确认运行环境满足依赖说明中的要求
2. 明确学习目标与当前水平
3. 使用自然语言描述学习需求
4. Agent生成个性化学习内容
5. 通过练习巩固学习成果

**结果验证**: 任务完成后,查看输出确认状态。成功时返回摘要和数据;失败时根据错误信息排查,参考恢复章节获取修复步骤.
## 示例

### 示例1：学习递归概念

```
用户: Explain recursion using 3 different analogies, I'm a beginner
# ...
Agent: 递归的三种类比解释：
1. 镜中镜 - 一面镜子映照另一面镜子，层层深入
2. 俄罗斯套娃 - 打开一个娃娃里面还有更小的娃娃
3. 楼梯攀登 - 每步只上一级，重复直到顶层
[附Python代码示例]
```

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| 学习内容过浅/过深 | 未说明当前水平 | 明确说明：Complete beginner / Intermediate / Advanced |
| 概念解释不清楚 | 学习风格不匹配 | 尝试不同学习风格：Analogies / Step-by-Step |
| 代码示例无法运行 | 环境依赖缺失 | 检查Python/Node版本；安装所需依赖 |

## 常见问题

### Q1: 免费版与付费版有什么区别？
A: 免费版提供概念解释、基础语言学习与学习指南功能。付费版额外提供项目教程、视觉学习、对话练习、闪卡生成、模拟测试等高级功能.
### Q2: 支持哪些学科？
A: 支持STEM、人文、技术技能等基础学科的辅导，覆盖数学、物理、编程、语言等常见领域.
### Q3: 如何获得更好的学习效果？
A: 说明当前水平、多问为什么、请求练习题、承认困惑点，并基于已理解内容构建新知识.
## 已知限制

- 不支持项目教程与实战项目驱动学习
- 不支持视觉学习的图表生成
- 不支持闪卡与模拟测试生成
- 语言学习口语练习需配合TTS工具

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "个性化学习助手免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "learn-cog"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
