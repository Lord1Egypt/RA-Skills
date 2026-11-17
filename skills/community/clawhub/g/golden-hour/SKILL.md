---
name: golden-hour
description: |
  用户想了解一天中什么时间最适合拍照、问"什么时候拍照光线最好"、或规划户外
  拍摄时间时调用。不适用于光线方向选择（应调用 natural-light-direction）或
  室内布光（应调用 three-point-lighting）。
  Invoke when the user wants to know the best time of day for photography,
  asks "when is the best light," or is planning outdoor shoot timing.
  Not for light direction choices (use natural-light-direction) or
  indoor lighting setup (use three-point-lighting).
  关键 trigger / Key triggers: "黄金时段"、"什么时间拍照"、"golden hour"、"best time
  to photograph"、"blue hour"、"photography time of day"、
  "when to shoot outdoors"、"best light time"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第九章 p208-p213
tags: [natural-light, golden-hour, time-of-day, planning]
related_skills: []
---

# 黄金时段与时辰光线法

## R — 原文 (Reading)

> "从拂晓到黄昏拍摄旅行照片"——一天中不同时段的光线特性截然不同。专业摄影师将早晨和午后视为一天中摄影的黄金时段。正午阳光是硬顶光，在人像上产生难看的阴影。
>
> — 美国纽约摄影学院，第九章

---

## I — 方法论骨架 (Interpretation)

一天中光线随太阳位置变化呈现系统性差异，理解这些差异可大幅提升户外拍摄质量。拂晓（日出前）：柔和冷调光线，天空呈蓝紫色，适合安静、神秘的氛围。清晨（日出后1-2小时）：温暖侧光，立体感强，是黄金时段的开始。正午（太阳在头顶）：硬顶光，产生难看的鼻下阴影和眼窝黑影，避免人像拍摄，但适合建筑几何感拍摄。午后（日落前1-2小时）：温暖侧光，与清晨类似，是第二个黄金时段。黄昏（日落后）：暖调逆光，天空呈橙红色。蓝调时刻（日落后20-40分钟）：天空呈深蓝色，与人造灯光形成冷暖对比，是城市摄影的最佳时间。核心策略：将重要拍摄安排在清晨和午后两个黄金时段，正午休息或拍摄不需要柔和光线的题材。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 旅行摄影的时间规划
- **问题**: 如何在旅行中最大化拍摄机会
- **方法论的使用**: 从拂晓到黄昏规划不同题材：拂晓拍安静街景→清晨拍人像和风光→正午拍建筑内部或休息→午后拍人像和风光→黄昏拍逆光剪影→蓝调时刻拍城市夜景。
- **结论**: 时间规划是旅行摄影成功的关键
- **结果**: 充分利用每个时段的光线特性

### 案例 2: 黄金时段人像
- **问题**: 什么时候拍人像光线最好
- **方法论的使用**: 在清晨或午后的黄金时段拍摄，此时阳光角度低，产生温暖的45°侧光，立体感强且肤色好看。
- **结论**: 黄金时段是人像摄影的最佳时间
- **结果**: 自然温暖的人像效果，无需人工补光

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 规划户外拍摄的时间安排
2. 问"什么时候拍照光线最好"
3. 旅行摄影想最大化拍摄机会
4. 问"为什么正午拍的人像不好看"

### 语言信号
- "什么时间拍照最好？"
- "黄金时段是什么时候"
- "正午能拍照吗"
- "golden hour"
- "best time for outdoor photography"
- "blue hour city photography"

### 与相邻 skill 的区分
- 与 `natural-light-direction` 的区别：本 skill 关注时间（什么时候拍），natural-light-direction 关注角度（从哪个方向拍）。两者配合使用。
- 与 `available-light-photography` 的区别：本 skill 关注户外自然光的时间特性，available-light 关注室内/混合光源。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **确定拍摄题材**
   - 完成标准: 明确用户要拍什么（人像/风光/建筑/城市/旅行）

2. **推荐最佳时段**
   - 完成标准: 根据题材推荐最佳拍摄时段
   - 人像→清晨或午后黄金时段
   - 风光→清晨（有晨雾/露水）或黄昏（暖调）
   - 建筑几何→正午（硬光强调线条）
   - 城市夜景→蓝调时刻（日落后20-40分钟）
   - 旅行→全天规划不同题材

3. **提供时段光线特性**
   - 完成标准: 描述推荐时段的光线方向、色温、质感
   - 配合 natural-light-direction skill 选择拍摄角度

4. **注意事项**
   - 完成标准: 提醒关键注意事项
   - 黄金时段短暂（约1-2小时），提前到达准备
   - 正午避免人像（或找阴影/用反光板补光）
   - 蓝调时刻短暂，需提前架好三脚架

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 室内拍摄 → 光线不受时段影响
- 光线方向选择 → 应调用 natural-light-direction
- 阴天/雨天 → 光线特性不同，时段差异减小

### 作者在书中警告的失败模式
- 正午直射阳光下拍人像导致眯眼和难看阴影
- 错过黄金时段（短暂，需提前准备）

### 作者的盲点 / 时代局限
- 未涉及不同纬度和季节对黄金时段长度的影响
- 数码时代可通过后期调整色温，部分弥补非黄金时段的色温问题

---

## 相关 skills (阶段 3 填充)

- composes-with: natural-light-direction（时间+方向=完整自然光策略）
- composes-with: photo-three-principles（光线服务于主题表达）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
