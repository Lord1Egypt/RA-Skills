---
name: light-meter-compensation
description: |
  用户遇到曝光不准（雪景拍成灰色、逆光人像面部全黑）、问"测光表怎么用"、
  或面对高反差场景不知如何曝光时调用。不适用于光圈快门创意选择
  （应调用 exposure-dual-control）或胶片宽容度理论查询。
  Invoke when the user faces incorrect exposure (gray snow, black faces in
  backlight), asks "how to use a light meter," or doesn't know how to expose
  high-contrast scenes. Not for aperture/shutter creative choices
  (use exposure-dual-control) or film latitude theory queries.
  关键 trigger / Key triggers: "雪景发灰"、"逆光曝光"、"测光表不准"、"18%灰"、
  "light meter"、"exposure compensation"、"backlit portrait"、
  "high contrast scene exposure"、"why is my snow gray"、"18% gray card"。
source_book: 《纽约摄影学院摄影教程》 美国纽约摄影学院
source_chapter: 第五章 p111-p125
tags: [exposure, light-meter, 18-percent-gray, compensation, high-contrast]
related_skills: []
---

# 测光补偿与高反差曝光法

## R — 原文 (Reading)

> "测光表是'愚蠢的'，它不会思考，不能做出明智的决断。测光表将所有场景都校准为18%的灰色影调。不管对准白雪还是黑炭，测光表都会给出使它们呈现18%灰色的曝光量。"
>
> — 美国纽约摄影学院，第五章

---

## I — 方法论骨架 (Interpretation)

测光表的核心局限在于它把所有场景都当作18%灰色处理——对准白雪会建议让雪变灰，对准黑炭会建议让炭变浅。因此正确使用测光表的核心原则是"接近并读取最重要的影调区域"：靠近被摄主体的关键部位（如人像的面部）测光，而非从远处测光（会纳入天空和背景导致平均读数不准）。替代方案包括读取自己皮肤色调（需光线条件相同）或使用18%灰板。在高反差场景（亮度范围超过胶片宽容度）中，使用累积测光法：分别对阴影区和强光区测光，根据负片"宁过勿欠"特性（曝光过度宽容度远大于曝光不足），以阴影区读数为基础收缩曝光不足宽容度的挡数来设置曝光。

---

## A1 — 书中的应用 (Past Application)

### 案例 1: 高反差场景累积测光法
- **问题**: 模特在明亮阳光下、面部处于阴影，如何正确曝光
- **方法论的使用**: 分别测光：面部f/2，天空f/22，范围7挡。中点曝光（f/7）导致面部细节损失；阴影区曝光（f/2）导致天空细节损失。最终方案：以阴影区f/2为基础收缩2挡（Plus-X曝光不足宽容度）→ f/4。
- **结论**: 累积测光法+负片宽容度不对称法则可完美处理高反差场景
- **结果**: 阴影区和强光区细节都得到保留

### 案例 2: 18%灰板使用
- **问题**: 如何获得准确的曝光读数
- **方法论的使用**: 将18%灰板放在与被摄体相同的光线下，测光表指向灰板读数。灰板反射18%光线，测光表给出使灰板呈现18%灰色的曝光量，所有其他色调也会真实重现。
- **结论**: 灰板读数是最可靠的曝光基准
- **结果**: 适用于自动和手动曝光相机

---

## A2 — 触发场景 (Future Trigger)

### 用户会在什么情境下需要这个 skill?
1. 拍雪景/沙滩发现雪/沙变成灰色
2. 逆光人像面部全黑
3. 问"测光表怎么用才准确"
4. 高反差场景（明亮背景+暗主体）不知如何曝光
5. 问"曝光补偿怎么设"

### 语言信号
- "雪景拍出来是灰色的"
- "逆光人像脸太黑"
- "测光表不准怎么办"
- "exposure compensation"
- "backlit portrait exposure"
- "18% gray card"
- "high contrast scene"

### 与相邻 skill 的区分
- 与 `exposure-dual-control` 的区别：本 skill 解决"测光表读数不准怎么办"，exposure-dual-control 解决"选什么光圈快门组合"。
- 与 `film-exposure-asymmetry` 的区别：本 skill 是测光操作方法，film-exposure-asymmetry 是胶片宽容度特性决定的曝光策略。

---

## E — 可执行步骤 (Execution)

当 skill 被激活后，agent 应按以下步骤执行：

1. **判断场景类型**
   - 完成标准: 识别是正常场景、大面积白/黑场景、还是高反差场景
   - 大面积白/黑→需要曝光补偿；高反差→需要累积测光法

2. **正常场景：接近测光**
   - 完成标准: 建议用户靠近被摄主体关键部位测光
   - 替代方案: 读取自己皮肤色调（光线条件需相同）或使用18%灰板

3. **大面积白色场景（雪/沙滩/白墙）**
   - 完成标准: 在测光表读数基础上开大1-2挡光圈（或降低快门速度1-2挡）
   - 原理: 测光表会让白色变灰，需要额外曝光让白色保持白色

4. **高反差场景：累积测光法**
   - 完成标准: 分别测阴影区和强光区，计算挡数差
   - 负片策略: 以阴影区读数为基础，收缩曝光不足宽容度挡数（黑白约2挡，彩色负片约1挡）
   - 反转片策略: 以强光区读数为基础（宁欠勿过）
   - 备选: 分界曝光法（同一场景拍2-3张不同曝光）

---

## B — 边界 (Boundary)

### 不要在以下情况使用此 skill
- 光圈快门创意选择 → 应调用 exposure-dual-control
- 胶片/ISO选择 → 不涉及感光度
- 数码后期调整曝光 → 本 skill 关注拍摄时的测光决策

### 作者在书中警告的失败模式
- 从过远处测光，纳入天空和背景导致平均读数不准
- 摄影师身体影子投射在被摄体上，读取的是影子而非主体色调
- 黑暗背景下远距离测光，黑暗背景要求更多曝光导致前景过曝

### 作者的盲点 / 时代局限
- 数码时代有HDR、曝光包围自动合成等技术可部分解决高反差问题
- 数码传感器的宽容度（尤其现代微单）远优于胶片，高反差场景的处理空间更大
- 未涉及数码相机的点测光、矩阵测光等现代测光模式

---

## 相关 skills (阶段 3 填充)

- depends-on: film-exposure-asymmetry（高反差曝光策略依赖胶片宽容度特性）
- composes-with: exposure-dual-control（测光后选择具体参数）
- composes-with: available-light-photography（现场光测光技术）

---

## 审计信息

- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 待测试
- **蒸馏时间**: 2026-08-03
