---
name: openclaw-immediate-ack
description: Use when configuring OpenClaw chat channels to send an immediate acknowledgement before the main reply starts. Supports Feishu and DingTalk, includes bilingual Chinese-English guidance, and requires the acknowledgement language to follow the active conversation language.
---

# OpenClaw Immediate Ack / OpenClaw 即时确认回复

## Purpose / 功能定位

### English

Use this skill when an OpenClaw bot should send a short acknowledgement immediately after receiving a user message, before the full agent response is generated.

This skill standardizes a simple interaction pattern:

1. The user sends a message.
2. The bot immediately sends a short acknowledgement.
3. The bot then continues reasoning and sends the full response later.

The goal is to make the bot feel responsive and trustworthy by clearly signaling:

- the message was received
- the bot is active
- processing has started

This is also a key product highlight: once the user sees the immediate acknowledgement, they can directly understand that the message was sent successfully, accepted by the bot, and entered the processing flow.

### 中文

当你希望 OpenClaw 机器人在收到用户消息后，先立即回复一句简短确认，再继续生成完整答复时，应使用这个 Skills。

这个 Skills 标准化了如下交互流程：

1. 用户发送消息
2. 机器人立即回复一句简短确认
3. 机器人继续思考，并在稍后发送完整回复

它的目标是提升机器人的可感知响应速度和稳定感，让用户明确知道：

- 消息已经收到
- 机器人当前在线
- 任务已经开始处理

这也是这个 Skills 的一个重要产品亮点：当用户看到了这条即时确认回复，就可以直观地判断，这条消息已经被成功发出、被机器人成功接收，并且已经进入处理流程。

## Supported Channels / 支持渠道

### English

This skill is designed to support:

- Feishu, when the OpenClaw Feishu plugin is installed and enabled
- DingTalk, when the user is running a DingTalk bot integration

### 中文

这个 Skills 面向以下渠道：

- 飞书：用户安装并启用了 OpenClaw 的 Feishu 插件
- 钉钉：用户使用的是钉钉机器人接入

## Channel Behavior / 渠道行为

### Feishu

#### English

For Feishu, the acknowledgement should be sent in the inbound message handling flow before dispatching the message to the agent.

Recommended behavior:

- send the ack as a normal Feishu text reply
- keep reply target and thread behavior consistent with the inbound context
- do not block agent dispatch if ack sending fails

#### 中文

对于飞书，这条即时确认应在消息进入 agent 处理流程之前发送。

推荐行为：

- 使用普通飞书文本消息发送确认回复
- 保持回复目标、线程上下文与原消息一致
- 即使确认消息发送失败，也不能阻塞后续 agent 处理

### DingTalk

#### English

For DingTalk, the acknowledgement should be sent before the main agent response is produced.

Recommended behavior:

- send the ack as a short plain-text status message
- keep existing routing and session behavior unchanged
- do not block agent dispatch if ack sending fails

#### 中文

对于钉钉，这条即时确认也应在主回复开始之前发送。

推荐行为：

- 以简短纯文本状态消息的形式发送确认回复
- 保持既有的路由和会话逻辑不变
- 即使确认消息发送失败，也不能阻塞后续 agent 处理

## Language Rules / 语言规则

### English

The acknowledgement language must follow the active conversation language.

Rules:

- if the current conversation is in Chinese, use the Chinese acknowledgement pool
- if the current conversation is in English, use the English acknowledgement pool
- do not mix Chinese and English in a single acknowledgement unless the product explicitly requires mixed-language replies
- if the language is unclear, prefer the system default language or the most recent user message language

Examples:

- Chinese conversation -> reply in Chinese
- English conversation -> reply in English

### 中文

即时确认回复必须跟随当前对话语言。

规则如下：

- 如果当前和机器人是中文对话，就使用中文确认回复池
- 如果当前和机器人是英文对话，就使用英文确认回复池
- 除非产品明确要求中英混用，否则单条确认回复中不要混杂中英文
- 如果语言不明确，优先使用系统默认语言，或者最近一条用户消息的语言

示例：

- 中文对话 -> 输出中文确认回复
- 英文对话 -> 输出英文确认回复

## Default Reply Pools / 默认回复池

### Chinese Default Pool / 中文默认回复池

1. 收到啦，我想想
2. 好嘞，我来琢磨一下
3. 收到，我先看看
4. 看到啦，我想一想
5. 好，交给我想想
6. 收到，我来理一理
7. 明白，我先捋捋
8. 好的，我想一下哈
9. 收到，这就想想办法
10. 好嘞，我先分析一下
11. 看到了，我来想想怎么弄
12. 收到，我先过一遍
13. 行，我琢磨琢磨
14. 好，我先想想怎么处理
15. 收到，容我想想
16. 没问题，我来想一下
17. 收到，我先整理整理思路
18. 好耶，我来研究一下
19. 看见啦，我先想想
20. 收到，我马上想想怎么办

### English Default Pool / 英文默认回复池

1. Got it, let me think.
2. Okay, I am looking into it.
3. Message received, let me take a look.
4. Got it, let me think this through.
5. Alright, let me work on it.
6. I see it, let me think for a moment.
7. Understood, let me sort it out.
8. Got your message, let me dig in.
9. Okay, let me figure this out.
10. Seen it, let me think.
11. Got it, I will look into it now.
12. Alright, let me think about the best way to handle it.
13. Message received, I am on it.
14. Okay, let me work through this.
15. Got it, give me a moment to think.
16. Understood, let me take a pass at it.
17. I have got it, let me organize my thoughts.
18. Okay, let me look into this for you.
19. Seen your message, let me think it through.
20. Got it, let me see how to handle this.

## Implementation Rules / 实现规则

### English

- choose one acknowledgement randomly from the language-matched pool
- keep the reply pool centralized and easy to edit
- send the acknowledgement before agent dispatch starts
- keep the acknowledgement short, friendly, and lightweight
- the acknowledgement must imply "received and thinking", not "already completed"
- if sending the acknowledgement fails, log the error and continue normal processing
- the full agent response must still go through the normal reply pipeline
- a visible acknowledgement should be treated as a positive user-facing receipt signal

### 中文

- 每次从当前语言对应的回复池中随机选择一句
- 回复池应集中维护，便于后续统一修改
- 即时确认必须在 agent 正式开始分发处理前发送
- 确认回复应简短、友好、轻量
- 语义必须表达“已收到，正在想/正在处理”，不能表达“已经完成”
- 如果即时确认发送失败，只记录日志，不影响正常处理流程
- 完整答复仍然必须走原有的标准回复链路
- 用户成功看到即时确认回复时，应将其视为“消息已成功送达并被系统接收”的正向信号

## Delivery Success And Failure Signals / 送达成功与失败信号

### English

This skill defines a practical user-facing signal model:

- if the user receives the immediate acknowledgement, that is the clearest visible sign that the inbound message was accepted by the bot
- if the user receives no acknowledgement and no later full reply, the default user-facing interpretation is that the message was not successfully received or not successfully processed
- "no reply at all" is the default external failure signal, but it is only a product-level symptom, not a precise technical diagnosis

Silence can correspond to different technical states, for example:

- the message never reached OpenClaw
- the message reached OpenClaw but the acknowledgement failed to send
- the acknowledgement failed but the full reply still arrived later
- the message was accepted but later processing failed

Recommended interpretation:

- visible immediate acknowledgement = successful receipt confirmed
- no immediate acknowledgement and no later reply = default failure symptom from the user perspective
- precise root-cause analysis = requires logs, metrics, or channel-specific diagnostics

### 中文

这个 Skills 需要定义一套面向用户的可见信号规则：

- 如果用户收到了即时确认回复，这是最明确的可见信号，表示这条入站消息已经被机器人接收
- 如果用户既没有收到即时确认，也没有收到后续正式回复，那么默认可以从用户视角判断：这条消息没有被成功接收，或者没有被成功处理
- “完全没有任何回复”是默认的外部失败信号，但它只是产品层面的现象，不等于精确的技术诊断

消息无回复可能对应多种技术状态，例如：

- 消息根本没有到达 OpenClaw
- 消息到达了 OpenClaw，但即时确认回复发送失败
- 即时确认回复发送失败，但主回复后来成功发出了
- 消息已经接收，但后续处理阶段失败了

推荐判断标准：

- 用户看到了即时确认回复 = 可以视为“消息已成功送达并被系统接收”
- 没有即时确认，且后续也没有任何正式回复 = 从用户视角看，可作为默认失败信号
- 如果要进一步判断具体失败原因，必须结合日志、监控指标或渠道诊断信息

## When To Use / 适用场景

### English

Use this skill when the user wants:

- immediate acknowledgement after message receipt
- better perceived responsiveness
- a consistent acknowledgement experience across Feishu and DingTalk
- a reusable standardized reply pool for OpenClaw bots

### 中文

当用户有以下需求时，适合使用这个 Skills：

- 希望机器人收到消息后立刻确认
- 希望机器人显得更灵敏、更在线
- 希望飞书和钉钉的体验保持一致
- 希望把即时确认回复做成可复用、可发布的标准能力

## When Not To Use / 不适用场景

### English

Do not use this skill for:

- long progress updates
- periodic heartbeat broadcasts
- final response formatting
- retry or transport recovery logic unrelated to immediate acknowledgement

### 中文

以下场景不应使用这个 Skills：

- 长篇进度播报
- 周期性心跳消息
- 最终答复格式控制
- 与即时确认无关的重试、补发、传输恢复逻辑
