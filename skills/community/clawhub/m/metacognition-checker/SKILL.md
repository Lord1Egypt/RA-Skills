---
name: metacognition-checker
description: Check whether a user truly understands a concept, decision, plan, or belief, or is only feeling familiar and overconfident. Use for learning validation, decision review, blind-spot detection, error review, confidence calibration, and minimum verification planning.
version: v1.0.0
tags: metacognition, self-assessment, blind-spot-detection
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":[],"env":[]}}}
---

# Metacognition Checker

## Usage Scenarios

### Scenario 1: Check True Understanding of a Concept
**User input:** "I think I understand recursion, but I'm not sure if I really get it"
**Expected output:** The skill runs the four checks (Explain, Transfer, Boundary, Evidence). Identifies whether the user has familiarity vs true understanding. Outputs the minimal verification action: "Close all references and write 3 sentences explaining recursion in your own words, then give one novel example."

### Scenario 2: Review a Decision for Blind Spots
**User input:** "I'm confident this business plan will work. My evidence is market research and competitor analysis. Check my reasoning."
**Expected output:** The skill reveals the current claim, separates facts from interpretation, identifies the most likely blind spot (e.g., survivorship bias in competitor data), and provides one minimum verification action before proceeding.

### Scenario 3: Post-Mortem Analysis of a Wrong Call
**User input:** "I made a wrong judgment call in that meeting. I thought the client would prefer option A but they chose option B. Help me analyze what went wrong."
**Expected output:** The skill separates facts from interpretation, identifies likely bias (e.g., confirmation bias from past experience), and provides a structured breakdown of what was known vs assumed.

帮助用户检查自己的判断、学习或决策过程，识别"感觉懂了"与"真的懂了"的差异。
### Scenario 4: 总觉得自己学习效率很低
**User input:** "我在准备考研，每天学8个小时但感觉什么都没记住，是不是学习方法有问题？"
**Expected output:** 用元认知检查法分析学习效率：1）识别'虚假学习'——被动看视频/划书不等于主动学习；2）推荐的主动学习方法：费曼技巧（用自己的话讲出来）、间隔重复（艾宾浩斯遗忘曲线）、自我测试（合上书回忆）；3）提供学习策略诊断清单：是否做笔记？是否会做思维导图？是否会定期复习？建议换用番茄工作法（25分钟学习+5分钟休息），其实真正的有效学习时间可能只有4小时。

## Best Use Cases

- 学完一个概念后，检查自己是"看懂了"还是"会用了"
- 做重要决定前，校准信心和证据质量
- 复盘错误判断，找出盲点、反例和遗漏信息
- 准备考试、面试、写作或汇报前做理解自测
- 判断一个计划是否只是听起来合理，还是已经可执行
- 把模糊的"我感觉没问题"转成可验证的小测试

## 适用场景

- 做决策前
- 学习过程中卡住时
- 复盘失败/误判时
- 想知道自己到底是不会，还是没看清

## 使用方式

根据用户给出的判断、计划或理解，输出：
1. 元认知检查清单
2. 盲点与反例
3. 缺失信息
4. 最小验证动作

## Prompt 指引

- 不直接替用户思考完
- 用问题暴露盲点
- 把"感觉"与"证据"分开
- 优先做小验证，而不是继续空想

## 输入

- 一个判断、选择、计划或理解
- 当前依据
- 当前信心程度
- 最大不确定点

## Four Checks

Use these checks before giving advice:

1. **Explain** - Can the user restate the idea without copying source wording?
2. **Transfer** - Can the user apply it to a new example?
3. **Boundary** - Can the user name where it fails or does not apply?
4. **Evidence** - Can the user separate observed facts from interpretation?

If one check fails, recommend a minimum verification action instead of continuing with abstract reassurance.

## 输出

- 检查清单
- 可能存在的偏差/盲区
- 需要补充的信息
- 下一步验证动作

## Output Contract

Keep the response short unless the user asks for a full audit:

1. Current claim or belief
2. Confidence level and evidence quality
3. Likely blind spot or missing counterexample
4. One question the user must answer
5. One smallest verification action

## 输出模板

- 你现在的判断是：`<判断>`
- 你依据的事实是：`<事实>`
- 你加入的解释是：`<解释>`
- 你最可能忽略的是：`<盲点/反例>`
- 在继续之前，你可以先验证一件事：`<最小验证动作>`

## 示例交互

**用户**：我觉得我已经学懂了这个概念，但做题还是错。

**Skill**：
你现在的判断是：你"懂了"。
但目前更像是你对这个概念有熟悉感，而不是已经具备可调用的理解。
请分开检查：
1. 你能不能不用原文，用自己的话解释它？
2. 你能不能举一个新例子？
3. 你能不能说出它不适用的情况？
如果这三步里有一步做不到，那就说明你还处在"看懂了"，没有到"会用了"。
你接下来的最小验证动作是：关掉资料，写 3 句话解释这个概念，并举 1 个自己的例子。

## Quick Prompts

```text
我觉得我懂了这个概念，请帮我做元认知检查。
```

```text
我准备做这个决定：<决定>。我的证据是：<证据>。请找盲点和最小验证动作。
```

```text
我这次判断错了，帮我区分事实、解释、偏见和遗漏信息。
```

## 注意事项

- 不代替专业外部判断
- 不适合纯情绪安抚场景
- 不要直接给结论，优先帮助用户自查
