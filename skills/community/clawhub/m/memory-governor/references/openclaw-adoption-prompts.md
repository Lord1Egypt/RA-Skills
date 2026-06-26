# OpenClaw Adoption Prompts

## Goal

定义 OpenClaw 在 **尚未安装** 或 **尚未完整接入** `memory-governor` 时，应该怎样提示使用者。

目标不是强推安装，而是：

- 在复杂度真的开始上升时提醒
- 把 `Installed / Integrated / Validated` 说清楚
- 明确不会因为安装而静默修改宿主
- 按使用者当前语言给出低摩擦提示

## Product Rule

OpenClaw 可以提示，但不应打扰式强推。

推荐原则：

- 条件触发
- 低频
- 可拒绝
- 可静默
- 按当前会话语言本地化

## Trigger Conditions

只有当下面信号足够强时，才推荐提示：

- 检测到多层记忆已经存在
- 检测到多个 skill 会写记忆
- 宿主尚未安装 `memory-governor`

或：

- 已安装 `memory-governor`
- 但未完成 `Integrated`

或：

- 已 `Integrated`
- 但尚未 `Validated`

不适合提示的情况：

- 宿主很简单，只有单一记忆入口
- 用户刚明确拒绝过
- 当前任务与记忆治理完全无关

## Frequency Rule

不要每次加载都提示。

推荐频率：

- 首次满足条件时提示一次
- 用户拒绝后进入静默
- 只有当宿主状态明显变化时才重新提示

可接受的重新提示条件：

- 新增多个会写记忆的 skill
- 宿主开始出现多层记忆
- 用户主动询问记忆系统、安装、治理、集成

## State-Specific Prompting

### State: Not Installed

提示目标：

- 告诉用户当前记忆系统已经开始复杂化
- 建议安装治理内核
- 明确安装不会静默改宿主

中文建议文案：

> 检测到当前宿主已经有多层记忆或多个会写记忆的 skill。  
> 如果你想统一“什么该记、记到哪、何时升格”的规则，可以考虑安装 `memory-governor`。  
> 它默认不会自动修改宿主，只提供治理规则、snippet、manifest 和 checker。  
> 需要的话我可以帮你安装，并在之后引导你做显式集成。

英文建议文案：

> Your host now appears to have multiple memory layers or multiple skills that write memory.  
> If you want a single rule set for what should be remembered, where it should go, and when it should be promoted, consider installing `memory-governor`.  
> It does not silently modify the host on install. It provides governance rules, snippets, a manifest model, and a checker.  
> If you want, I can help install it and then guide the explicit integration steps.

### State: Installed But Not Integrated

提示目标：

- 告诉用户已拿到规则层
- 但宿主还没完整接线

中文建议文案：

> `memory-governor` 已安装，但当前宿主还没有完成完整接入。  
> 现在你已经有治理规则，但主入口、相关 skill 和宿主 manifest 还没有全部接上。  
> 如果你愿意，我可以继续引导你完成 `Integrated` 状态。

英文建议文案：

> `memory-governor` is installed, but this host is not fully integrated yet.  
> You already have the governance layer, but the host entrypoint, relevant skills, and host manifest are not all wired in yet.  
> If you want, I can guide the remaining steps to reach the `Integrated` state.

### State: Integrated But Not Validated

提示目标：

- 提醒用户再跑 checker 完成 readiness 确认

中文建议文案：

> 当前宿主已经基本接入 `memory-governor`，但还没有完成校验。  
> 建议再跑一次 host checker，确认当前接线是否处于 `Validated` 状态。

英文建议文案：

> This host appears to be integrated with `memory-governor`, but it has not been validated yet.  
> Run the host checker once to confirm the current wiring is in the `Validated` state.

## Language Policy

提示文案应优先跟随使用者当前语言。

推荐优先级：

1. 当前会话语言
2. 宿主显式 locale
3. 默认英文

注意：

- 这里只要求提示层本地化
- 不要求整个 skill 包自动翻译
- 文档本体可以保持单主语言

## Decline / Snooze Behavior

如果用户明确拒绝：

- 记录一次拒绝状态
- 后续默认静默

可选的轻量确认文案：

中文：

> 好的，我先不再提示。之后如果你的记忆层继续变复杂，或者你主动提到记忆治理，我再重新提醒。

英文：

> Understood. I’ll stay quiet about it for now. If the host grows more memory complexity later, or if you bring up memory governance again, I can remind you then.

## Important Boundary

无论提示如何设计，都不应把“安装”说成“完整生效”。

推荐固定用语：

- `Installed`
- `Integrated`
- `Validated`

避免说法：

- “安装后自动接管”
- “安装后立即完整工作”
- “你只要装上就不用再管了”
