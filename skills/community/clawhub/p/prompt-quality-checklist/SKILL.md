---
name: prompt-quality-checklist
description: AI 短剧/短片分镜 prompt 质量审核清单。触发词：检查清单、质量审核、提示词检查、分镜审核、prompt 检查、镜头质检、生成前检查、自查、自审。用途：在执行 AI 生图/生视频之前，对每一句 prompt 进行 10 项系统性核查，确保日夜景、主体、空间、光源、阴影、质感、纵深、景别、投影方向、资产锚点全部合规。
---

# Prompt Quality Checklist / 提示词质量检查清单

## 这是什么

一套 10 项 prompt 自审清单，在 AI 生图/生视频之前逐条过筛。

适用于：LibLib、即梦、海螺、Runway、Pika 等所有生成工具的 image/video prompt 审查。

---

## 如何使用

### 基本流程

```
生成 prompt → 逐条对照清单 → 标记通过/打回 → 修改后重新提交
```

**通过标准：** 10 项全部通过（每项必须满足）→ 标记 ✅ PASS → 可执行
**打回标准：** 任何一项不满足 → 标记 ❌ FAIL → 必须修改后重审

### 使用场景

| 场景 | 操作 |
|------|------|
| 分镜设计阶段 | 对每个镜头 prompt 做预审，发现问题提前修改 |
| 批量生成前 | 统一跑一遍清单，杜绝低级错误批量出现 |
| 审核他人 prompt | 快速定位问题，给出具体修改建议 |
| 自查复盘 | 每周整理一次 fail 记录，归纳高频错误类型 |

### 审查顺序

建议按以下顺序逐条检查，不要跳项：

```
① 日夜景标注 → ② 主体描述 → ③ 空间坐标 → ④ 光源方向 → ⑤ 接触阴影
→ ⑥ 质感统一 → ⑦ 三层纵深 → ⑧ 景别对应 → ⑨ 投影方向 → ⑩ 资产锚点
```

---

## 10 项质量检查

### ① 日夜景标注 / Day–Night Marking

**检查点：** prompt 第一个从句/分句是否明确标注了时间（day / night / dawn / dusk / midday / golden hour /深夜/黄昏/正午等）。

❌ **错误：**
> A woman in red standing on a rooftop

✅ **正确：**
> Night, a woman in red standing on a rooftop, city lights below

> 白天，一位穿红色连衣裙的女人站在天台上

**说明：** AI 生图对"白天"和"深夜"的光线理解差异极大。不写时间，等于把画面氛围的决定权完全交给 AI 随机性。

---

### ② 主体描述 / Character Consistency

**检查点：** prompt 中的人物外貌、服装、姿态是否与该镜头的定妆照（costume reference）一致。

❌ **错误：**
> A beautiful girl wearing a white dress

✅ **正确：**
> Character ref: heroine_001.png, white silk qipao, hair up in a bun, right hand touching the earring, same appearance as in the reference photo

**说明：** "美女"是模糊描述，不同 AI 模型理解差异巨大。必须用具体的服装描述 + 定妆照资产路径锁定主体一致性。

---

### ③ 空间坐标 / Scene Asset Anchor

**检查点：** 场景是否有具体的资产锚点（asset path / location descriptor），而非笼统的"办公室""街道""房间"。

❌ **错误：**
> Interior of a luxury office

✅ **正确：**
> Interior of office_int_003, dark walnut desk, green banker lamp on the left, window with blinds on the right wall

**说明：** AI 对"豪华办公室"的理解可能是欧式古典，也可能是现代极简。具体到资产路径或至少3个硬质物件锚点，才能控制场景走向。

---

### ④ 光源方向 / Light Direction

**检查点：** 光源方向是否具体（left / right / above / behind / 45-degree），禁止使用"natural lighting / 自然光 / 柔和光线"等模糊描述。

❌ **错误：**
> Soft natural lighting, cinematic

✅ **正确：**
> Single light source from the left at 45°, hard rim light on the character's right shoulder, no fill

**说明：** "自然光"是玄学。同一个场景，侧光、背光、顶光产生完全不同的情绪和空间感。必须量化光源方向。

---

### ⑤ 接触阴影 / Ground Contact Shadow

**检查点：** 人物是否有投影落在地面/接触面上，是否有"shadow on the floor / 脚下阴影 / ground shadow"描述，避免人物"漂浮"。

❌ **错误：**
> Full body shot of a woman standing on the street

✅ **正确：**
> Full body shot, woman standing on the wet asphalt street, dark ground shadow directly beneath her feet, shadow stretching 1.5m to the right

**说明：** 没有地面阴影的人物看起来像被抠图贴上去的。接触阴影是空间真实感的最低底线。

---

### ⑥ 质感统一 / Material Consistency

**检查点：** prompt 中是否出现 retouching 类词汇（smooth skin / porcelain skin / flawless / 磨皮 / 柔焦），以及材质描述是否前后矛盾。

❌ **错误：**
> Porcelain smooth skin, matte eyeshadow, glossy lips

✅ **正确：**
> Realistic skin texture, visible pores, matte eyeshadow, semi-matte lips, consistent material finish across the face

**说明：** "陶瓷肌"和"哑光眼影"在材质上互相矛盾。Retouching 语言会触发 AI 的"美颜模式"，导致画面质感割裂。保持全部材质属性一致。

---

### ⑦ 三层纵深 / Three-Layer Depth

**检查点：** 画面是否具备前景（foreground）、中景（midground）、背景（background）三层物理纵深，且三层之间有合理的空间关系。

❌ **错误：**
> Close-up shot of a character's face

✅ **正确：**
> Medium shot, character in the midground, a blurred ancient bookshelf in the foreground (left 1/3), a window with rain streaks in the background (right wall), depth of field: shallow, focus on character

**说明：** 竖屏叙事空间有限，但纵深依然需要。哪怕是特写镜头，也应该用前景物件（头发丝、衣领边缘、雨滴玻璃）和背景虚化建立 Z 轴。

---

### ⑧ 景别对应 / Shot Type Matches Emotion

**检查点：** 景别（shot type）的选择是否服务于该镜头的情绪/叙事目标。

| 情绪目标 | 合适景别 |
|----------|----------|
| 压抑、孤独、命运感 | Wide / Extreme Wide |
| 角色陷入困境 | Wide + Low angle |
| 情感爆发、亲密 | Close-up / Medium Close-up |
| 叙事交代、环境压迫感 | Establishing shot → Medium |
| 力量展示、气场 | Low angle Medium / Low angle Wide |

❌ **错误：**
> A sad woman in an extreme close-up shot showing the vast ocean behind her

✅ **正确：**
> Full body shot, woman standing on the shore at dusk, tiny against the vast ocean, vastness reinforces her loneliness

**说明：** 景别是叙事工具，不是随机选择。情绪和画面要形成共振。

---

### ⑨ 投影方向 / Shadow Direction Consistency

**检查点：** 投影方向是否与第④项的光源方向一致。

**检查逻辑：**
- 光源在左侧 → 阴影投向右侧
- 光源在右侧 → 阴影投向左侧
- 光源在上方 → 阴影在正下方（短影）
- 光源在 45° 侧上方 → 阴影在对侧 45° 斜下方

❌ **错误：**
> Light from the left at 45°, shadow cast to the left side of the character

✅ **正确：**
> Light from the left at 45°, hard shadow stretching 2m to the right of the character, shadow angle matches light angle

**说明：** 光源方向和投影方向是配套检查项。写光源时不写投影，等于只完成了一半。

---

### ⑩ 资产锚点 / Asset Path Annotation

**检查点：** prompt 末尾是否附带了具体的资产路径或参考文件标注，格式统一，方便追溯。

**标准格式：**
```
[ASSET] character: char_ref_001.png | location: loc_venue_02.jpg | prop: prop_dagger_03.png | costume: cost_001.jpg
```

❌ **错误：**
> A warrior holding a sword in a dark forest

✅ **正确：**
> ... dark forest, warrior holding a longsword, camera slightly low angle
> [ASSET] character: warrior_male_001.png | location: forest_dark_001.png | prop: weapon_sword_002.png

**说明：** 资产锚点让每次生成都可复现、可复审。没有资产路径的 prompt 是"一次性"prompt，不适合 AI 短剧这种需要跨镜头一致性的场景。

---

## 通过/打回标准

### PASS（全部通过）

- 10 项检查全部满足
- prompt 语法清晰，无歧义描述
- 资产路径完整且格式统一

### FAIL（必须修改）

- 任何一项不满足
- 出现模糊词汇：自然光、柔和、美丽、豪华、适当
- 资产路径缺失或格式不统一

### 修改后重审

```
FAIL → 修改 prompt → 重新跑 10 项检查 → PASS → 执行生成
```

---

## 快速参考卡

将以下清单剪贴到工作台旁边：

```
✅ ① 时间：第1分句标注 day / night / dusk
✅ ② 主体：与定妆照一致，含资产路径
✅ ③ 空间：≥3个硬质物件锚点
✅ ④ 光源：具体方向（left/right/45°），禁止"自然光"
✅ ⑤ 阴影：地面接触阴影描述存在
✅ ⑥ 质感：无 retouching 词汇，材质统一
✅ ⑦ 纵深：前景+中景+背景三层
✅ ⑧ 景别：服务于情绪/叙事目标
✅ ⑨ 投影：方向与光源一致
✅ ⑩ 资产：末尾标注 [ASSET] 完整路径
```

---

## 相关参考

详细检查项说明及错误/正确示例对比 → `references/checklist-detailed.md`
