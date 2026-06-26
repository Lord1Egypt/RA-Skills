# Correction Pipeline

## Goal

把“这次被纠正了”与“以后都该这么做”拆开。

如果没有中间层，单次纠错太容易被直接写成长期真理。
这就是 `learning_candidates` 存在的原因。

## Default Pipeline

默认三段式：

1. correction is observed
2. correction is captured in `learning_candidates`
3. candidate is reviewed for promotion into `reusable_lessons`

一句话：

**先收集证据，再硬化规则。**

## What Belongs In `learning_candidates`

适合进入候选层的内容：

- 用户明确纠正了一次输出或判断
- 某个问题第一次出现，但看起来可能会重复
- 一条经验已经值得记下，但还没有足够证据证明它应长期复用

不适合进入候选层的内容：

- 明显只对当前项目成立的局部事实
- 纯临时 breadcrumb
- 已经是稳定长期偏好或长期事实的内容

## Promotion Standard

从 `learning_candidates` 升到 `reusable_lessons`，默认至少满足任意两个条件：

- 这类问题在多个任务、日期或上下文里重复出现
- 已经能重写成脱离当前案例的通用规则
- 用户明确说以后都应遵守这条规则
- 它稳定改变未来的判断、执行或协作质量

如果只满足一个条件，先留在候选层。

## Review Rhythm

推荐在这些时机 review 候选层：

- 任务结束后的短复盘
- 同类错误再次出现时
- 准备把经验升到 `AGENTS.md` / `TOOLS.md` / `SOUL.md` 之前

不要把候选层当默认启动上下文。

## Anti-Patterns

- 单次纠错直接写进 `reusable_lessons`
- 把候选层写成原始长日志
- 未 review 就把候选层升到系统级规则
- 让自动采样在没有边界的情况下批量制造候选垃圾
