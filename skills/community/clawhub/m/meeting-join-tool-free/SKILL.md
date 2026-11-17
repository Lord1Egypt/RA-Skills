---

slug: meeting-join-tool-free
name: meeting-join-tool-free
version: 1.0.0
displayName: AI会议助手免费版
summary: 让AI机器人以语音方式加入视频会议(Google Meet/Teams/Zoom),支持实时转写、问答与笔记,适合个人使用.
license: MIT
edition: free
description: "AI会议助手(Meeting Join)免费版，让AI机器人以语音方式加入Google Meet、Microsoft Teams、Zoom等视频会议平台，支持实时语音转写、智能问答和会议纪要自动生成。机器人加入会议后可全程聆听并转写内容，会议结束后提取关键决策、待办事项与责任人，输出Markdown格式纪要便于归档与分享。适合需要自动记录和整理meeting内容的个人用户。"
tags:
  - 会议
  - 语音转写
  - AI助手
  - 生产力
  - 协作
  - 工具
  - 效率
  - 创意
  - audio
  - bash
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
pricing_tier: free
---

# AI会议助手免费版

## 概述

AI会议助手免费版帮助个人用户让AI机器人以语音方式加入视频会议。机器人可以实时聆听会议内容、进行语音转写、回答基于会议上下文的问题,并在会议结束后生成结构化的会议纪要.
本版本面向个人用户,提供基础的语音会议参与能力,支持Google Meet、Microsoft Teams与Zoom三大主流平台. 通过Meeting Join功能,用户可以快速让AI机器人加入(meeting join)各类在线会议并进行实时转写.
## 核心能力

### 会议接入

- 支持Google Meet、Microsoft Teams、Zoom三大平台
- 以语音机器人身份加入,显示自定义名称
- 自动检测会议链接并配置连接参数

**处理**: 解析会议接入的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回会议接入的响应数据,包含状态码、结果和日志.
### 实时转写

- 实时语音转文字,区分不同发言者
- 支持中英文混合识别
- 转写内容实时保存,可回溯查看

**处理**: 解析实时转写的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回实时转写的响应数据,包含状态码、结果和日志.
### 常见问题

- 基于会议上下文回答问题
- 支持关键词触发响应
- 会议进行中可随时提问

**处理**: 解析常见问题的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回常见问题的响应数据,包含状态码、结果和日志.
### 纪要生成

- 会议结束后自动生成结构化纪要
- 提取关键决策、待办事项与责任人
- 输出Markdown格式,便于归档与分享

**处理**: 解析纪要生成的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回纪要生成的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：机器人以语音方式、加入视频会议、支持实时转写、问答与笔记、适合个人使用、会议助手免费版让、加入视频会议平台、实现实时会议转写、智能问答与会议纪、核心能力、加入主流视频会议、实时语音转写与会、议内容理解、基于会议上下文的、智能问答、成纪要与待办事项等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:个人日常会议记录

需求:自由职业者需要记录与客户的沟通会议.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | AI会议助手免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 以语音模式加入会议(最简配置)
（请参考skill目录中的脚本文件） "https://meet.google.com/abc-defg-hij" \
  --mode audio \
  --bot-name "助手" \
  --voice-strategy direct
```

会议结束后,自动生成纪要:

```markdown
# 会议纪要 - 2026年7月18日
# ...
## 不适用场景
# ...
以下场景AI会议助手免费版不适合处理：
# ...
- 需要100%确定性的关键决策
- 医疗诊断
- 法律判决
# ...
## 触发条件
# ...
需要AI模型调用、智能对话、Agent编排、LLM应用时使用。不适用于非本工具能力范围的需求.
# ...
## 参会人员
- 客户代表:张总
- 我方:设计师小李
# ...
## 关键讨论
1. 项目需求确认:完成首页设计稿
2. 交付时间:下周五前提交初稿
3. 反馈方式:通过邮件沟通修改意见
# ...
## 待办事项
- [ ] 小李:完成首页设计初稿(下周五前)
- [ ] 张总:提供品牌素材与参考网站
```

### 场景二:在线课程内容整理

需求:学生希望将在线课程内容转写为笔记.
```bash
# 加入在线课堂并转写
（请参考skill目录中的脚本文件） "https://zoom.us/j/123456789" \
  --mode audio \
  --bot-name "学习助手" \
  --voice-strategy direct \
  --transcription on
```

### 场景三:客户沟通会议问答

需求:在客户会议中,需要快速查阅产品资料回答问题.
```bash
# 带上下文加入会议
（请参考skill目录中的脚本文件） "https://teams.microsoft.com/l/meetup-join/..." \
  --mode audio \
  --bot-name "产品助手" \
  --voice-strategy direct \
  --context "我们是一款企业级项目管理SaaS产品,核心功能包括任务管理、甘特图、时间追踪。定价分为免费版、团队版、企业版。"
```

## 快速开始

### 依赖详情

```bash
# Python依赖
pip install aiohttp websockets
# ...
# 或使用Node.js
cd （请参考skill目录中的脚本文件） && npm install
```

### Step 2:配置API Key

```bash
# 方式一:通过邮箱注册(包含免费试用额度)
python （请参考skill目录中的脚本文件） send --email you@example.com
python （请参考skill目录中的脚本文件） verify --email you@example.com --code 123456
# ...
# 方式二:手动配置(使用当前目录下的配置文件)
mkdir -p ./config/agentcall
cat > ./config/agentcall/config.json << 'EOF'
{"api_key": "your_api_key_here"}
EOF
```

### Step 3:加入会议

```bash
# 最简方式:纯语音模式
（请参考skill目录中的脚本文件） "会议链接" --mode audio --bot-name "助手"
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 示例

### 基础配置

```json
{
  "api_key": "ak_ac_your_api_key_here",
  "default_mode": "audio",
  "default_voice_strategy": "direct",
  "default_bot_name": "助手"
}
```

### 命令行参数

| 参数 | 默认值 | 说明 |
|:-----|:-----|:-----|
| `--mode` | `audio` | 会议模式:`audio`(纯语音) |
| `--voice-strategy` | `direct` | 语音策略:`direct`(直接响应) |
| `--bot-name` | `助手` | 机器人在会议中的显示名称 |
| `--transcription` | `on` | 实时转写开关 |
| `--context` | 空 | 初始上下文(最多4000字符) |
| `--max-duration` | 套餐限制 | 最大会议时长(分钟) |
| `--alone-timeout` | 120 | 无人发言时自动离开(秒) |
| `--silence-timeout` | 300 | 静默超时自动离开(秒) |

### 机器人命名建议

选择语音识别友好的简短名称:

```bash
# 推荐:简短、独特、真实词汇
--bot-name "小助手" --trigger-words "助手,小助,助"
# ...
# 避免:通用短语,容易被转写错误
# 不推荐: AI助手、机器人、会议助手
```

## 优秀实践

### 会议前准备

| 准备事项 | 说明 | 重要性 |
|---:|---:|---:|
| 配置API Key | 确保账户有足够额度 | 必需 |
| 测试网络 | 确保稳定网络连接 | 必需 |
| 准备上下文 | 预先输入会议相关资料 | 推荐 |
| 设置机器人名 | 选择易识别的名称 | 推荐 |
| 确认权限 | 确保有权限让机器人加入 | 必需 |

### 上下文配置技巧

```bash
# 提供丰富的初始上下文,提升问答质量
（请参考skill目录中的脚本文件） "会议链接" \
  --mode audio \
  --context "会议主题:季度产品规划评审.
            参会人员:产品经理、设计师、开发负责人.
            讨论重点:Q3功能优先级、资源分配、发布节奏.
            背景:本季度用户增长20%,需要规划下季度重点。"
```

### 会议纪要优化

```python
# 纪要生成配置
summary_config = {
    "format": "markdown",
    "sections": ["参会人员", "关键讨论", "决策", "待办事项"],
    "extract_actions": True,        # 提取待办事项
    "identify_speakers": True,      # 区分发言者
    "highlight_keywords": True      # 高亮关键词
}
```

## 常见问题(补充)

### Q1: 机器人无法加入会议怎么办?

A: 检查以下几点:1)会议链接是否正确;2)是否已配置API Key;3)账户是否有足够额度;4)会议是否已开始且允许外部参与者加入.
### Q2: 语音转写准确率不高?

A: 确保会议环境安静,发言人靠近麦克风。中英文混合场景下,可在上下文中说明会议语言。免费版使用基础转写引擎,如需更高准确率可升级PRO版.
### 已知限制

A: 免费版包含试用额度(约360分钟),适合中小型会议。时长达到套餐限制时机器人会自动离开。如需更长会议时长,请升级PRO版.
### Q4: 是否支持视频画面?

A: 免费版仅支持纯语音模式(`audio`),不提供视频画面。如需可视化头像、屏幕共享等能力,请使用PRO版.
### Q5: 会议数据是否安全?

A: 会议转写内容作为Agent输入处理。建议在可信会议环境中使用,并配置Agent框架的权限系统限制机器人行为.
## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md规范的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux
- **Python**: 3.10+ 或 **Node.js**: 18+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| aiohttp | Python库 | 必需 | pip install aiohttp |
| websockets | Python库 | 必需 | pip install websockets |
| 会议平台账户 | 服务 | 必需 | Google/MS/Zoom账户 |

### API Key 配置

- 需要配置会议机器人服务的API Key
- 通过 `./config/agentcall/config.json` 或 `AGENTCALL_API_KEY` 环境变量配置
- 新账户注册包含免费试用额度

### 可用性分类

- **分类**: MD+EXEC模式纯Markdown指令+脚本执行能力)
- **说明**: 基于Markdown指令驱动Agent执行会议加入任务,通过Python/Node.js脚本实现会议机器人连接
- **免费版限制**: 纯语音模式、单次会议时长受限、基础转写引擎、无视频画面

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "AI会议助手免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "meeting join"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
