---
name: natural-light-direction
description: |
  用户想了解光线方向对照片效果的影响、问"什么光线适合拍人像"、或面对自然光
  场景不知如何选择拍摄角度时调用。不适用于人造光布光（应调用 three-point-lighting）
  或曝光参数设置（应调用 exposure-dual-control）。
  Invoke when the user wants to understand how light direction affects photos,
  asks "what light is best for portraits," or doesn't know which angle to shoot
  from in natural light. Not for artificial light setup (use three-point-lighting)
  or exposure parameter settings (use exposure-dual-control).
  关键 trigger / Key triggers: "光线方向"、"顺光逆光"、"侧光"、"natural light direction"、
  "best light for portrait"、"golden hour"、"backlight"、"side light"、
  "front light vs back light"、"what direction should light come from"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第九章 p197-p201
tags: [lighting, natural-light, direction, portrait]
related_skills: []
---

# 自然光方向选择法

## R — 原文 (Reading)

> "正面光...45°侧光...90°侧光...逆光"——四种基本光线方向各有特性。45°侧光被称为"自然光"，是人像摄影最佳光线，立体感强。90°侧光被称为"结构光"，强调质感和戏剧性对比。正面光制造平面二维感，缺乏层次。
>
> — 美国纽约摄影学院，第九章

---

## I — 方法论骨架 (Interpretation)

光线方向是照片情感基调的决定因素。四种基本方向各有明确的效果和适用场景：正面光（顺光，光源在摄影师后方）均匀照亮被摄体，不产生阴影，缺乏立体感和层次，适合记录但不适合艺术表达。45°侧光（前侧光）在面部产生自然的明暗过渡，立体感强，是人像摄影的"自然光"——最接近人眼日常观察的效果。90°侧光（正侧光）将面部一分为二，明暗对比强烈，强调质感和纹理，被称为"结构光"，适合表现沧桑感、戏剧性。逆光（光源在被摄体后方）创造剪影、轮廓光和透明感，最有戏剧性但需要补光或接受主体变暗。选择光线方向就是选择照片的情感基调。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 45°侧光人像
- **问题**: 如何让人像有立体感
- **方法论的使用**: 使用45°侧光，在面部产生自然的明暗过渡，既不过于平淡也不过于戏剧化。
- **结论**: 45°侧光是人像摄影的"自然光"
- **结果**: 立体感强，最接近人眼日常观察效果

### 案例 2: 90°侧光质感表现
- **问题**: 如何强调被摄体的质感和纹理
- **方法论的使用**: 使用90°侧光，光线从侧面垂直照射，横穿主体表层，产生强烈的明暗对比。
- **结论**: 90°侧光是"结构光"，强调质感
- **结果**: 适合表现老人面部皱纹、建筑纹理、织物质感

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 户外人像拍摄，不确定什么时间/角度拍最好
2. 问"为什么我的人像看起来像证件照"
3. 想创造特定情感氛围（温暖/戏剧/神秘）
4. 问"顺光好还是逆光好"

### 语言信号
- "什么光线适合拍人像？"
- "顺光还是逆光？"
- "为什么照片看起来很平"
- "natural light portrait"
- "best time for outdoor photography"
- "backlight silhouette"

### 与相邻 skill 的区分
- 与 `three-point-lighting` 的区别：本 skill 关注自然光（太阳）方向选择，three-point-lighting 关注人造光布光。
- 与 `golden-hour` 的区别：本 skill 关注光线方向（角度），golden-hour 关注一天中不同时段的光线特性（时间）。
- 与 `composition-eight-questions` 的区别：八问法中"用光突出"只是八分之一，本 skill 专门深入光线方向。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **确定拍摄主题和情感目标**
   - 完成标准: 明确用户要拍什么（人像/风光/建筑）和想要什么情感（自然/戏剧/神秘/温暖）

2. **选择光线方向**
   - 完成标准: 根据情感目标推荐光线方向
   - 自然温暖→45°侧光（人像最佳）
   - 戏剧质感→90°侧光
   - 神秘剪影→逆光
   - 记录文档→正面光（但提醒缺乏艺术感）

3. **调整拍摄角度**
   - 完成标准: 建议用户相对于光源的站位
   - 45°侧光: 站在光源斜前方45°位置
   - 90°侧光: 站在光源侧面
   - 逆光: 站在光源和被摄体之间（面对光源）

4. **注意事项**
   - 完成标准: 提醒关键注意事项
   - 逆光人像需补光（反光板/闪光灯）或接受剪影效果
   - 正午顶光避免人像（产生难看的眼窝/鼻下阴影）
   - 直射阳光下人像导致眯眼

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 室内人造光布光 → 应调用 three-point-lighting
- 曝光参数设置 → 应调用 exposure-dual-control
- 一天中什么时间拍摄 → 应调用 golden-hour（本 skill 关注角度而非时间）

### 作者在书中警告的失败模式
- 正面光制造平面二维感，缺乏层次（像证件照）
- 直射阳光下拍人像导致眯眼和难看阴影
- 逆光不补光导致主体全黑

### 作者的盲点 / 时代局限
- 未涉及数码时代HDR/后期提亮阴影的技术
- 对"不完美光线"的创意运用（如正午硬光的时尚摄影）关注不足

---

## 相关 skills (阶段 3 填充)

- composes-with: golden-hour（方向+时间=完整自然光策略）
- composes-with: composition-eight-questions（用光是构图八问之一）
- contrasts-with: three-point-lighting（自然光 vs 人造光）
- composes-with: available-light-photography（自然光是现场光的一种）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
