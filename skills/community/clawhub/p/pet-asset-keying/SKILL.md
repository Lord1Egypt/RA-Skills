---
name: pet-asset-keying
description: "Cut pet (anthropomorphized character) assets to transparent PNG — single image or video frame sequences. Primary method is 'outline-cut': slice along the character's own outline so the boundary already sits on the line; do NOT hunt for edges inside the anti-aliasing blur band. No AI model required (no rembg / no torch / no onnx). Use for 'matting', 'remove background', 'transparent PNG', 'hair-edge cutout', 'video frame keying', 'batch cutout', 'gray halo or black edge on border', '抠图', '去背景', '透明底', '发丝边缘', '批量抠像'. Includes calibrated parameters, enclosed-space (crescent/irregular) handling, safety guardrails, a self-check report, and a 'tested backfires — do not retry' list."
license: MIT
metadata:
  slug: "pet-asset-keying"
  displayName: "Pet Asset Keying (宠物素材抠像)"
  category: "image-processing"
  description_zh: "给「宠物拟人角色」素材抠透明底（单图或视频帧序列）。主方案是「勾线切」—— 顺着角色自身的勾线切割，边界本来就在勾线上，不要再去抗锯齿模糊带里找边界。无需任何 AI 模型（no rembg / no torch / no onnx）。当任务涉及「抠图、去背景、透明底、PNG 透明通道、发丝边缘、视频抽帧抠像、批量抠图、边缘有灰晕/黑边」时使用。含已标定参数、封闭空间（月牙/异形）处理、安全护栏、自检报告，以及一份「实测反效果·别再试」的清单。"
  agent_created: "true"
---

# 宠物 / 动漫角色素材抠图

给拟人角色素材抠透明底。单张图，或整段视频抽出来的帧序列。

**不需要任何 AI 模型**：no rembg / no torch / no onnx。只要 numpy + opencv + scipy。

## 先选路：你有勾线吗？

| 情况 | 走哪条 | 为什么 |
|---|---|---|
| 角色/道具**有描边勾线**（立绘、描边插画、多数精灵素材） | **勾线切** `scripts/line_keying.py` | 边界本来就在勾线上，参数不敏感，0.2s/帧 |
| **发丝级细结构**、没有勾线的地方 | **交集法** `scripts/keying.py` | 语义模型管轮廓、颜色阈值管小洞 |
| 两者都有 | **串起来**：勾线的地方勾线切，细结构交回 matting | 两者短板不重叠 |

## 一、核心判断：不要在模糊带里找边界

这是整个 skill 唯一重要的一句话。

角色边缘有一圈**抗锯齿混出来的像素**——它既不是背景也不是前景。任何阈值方法在这圈里切，只有两个结果：

- 切多了 ⇒ 吃角色
- 切少了 ⇒ 留一圈淡边 / 暗边

**那圈边不是你没抠好，是源图里本来就有。** 五个不同开源模型跑同一张图，色边全都在。

所以正确做法是**换一个位置下刀**：人物是有勾线的，勾线是一条深色、高对比、位置唯一的线 —— **它本来就是画上去的切割线**。

## 二、勾线切怎么工作

两条 pass：

**pass1 · 外轮廓**
从画面四边泛洪，可通行区 = 距背景 < `TOL_OUT`。勾线是深色，泛洪穿不过去 ⇒ 角色 = 非外部区。

**pass2 · 封闭空间**（手叉腰的三角、辫子和肩之间的缝、刘海和脸颊之间）
候选 = 距背景 < `SEED_MAX`（严格：必须是"真背景色"，不是过渡色）。
种子 = 块内**非边缘像素**里距背景最近的那个。
⛔ **不用几何质心** —— 月牙/异形时质心会落到块外或过渡色上，实测 **10% 的块中招**。
泛洪 8 连通 + 绝对阈值 `TOL_HOLE`，结果锁在角色内部。

**alpha**
先内缩 `ALPHA_ERODE` px（把边界从模糊带压回 50% 覆盖线），再高斯软化 `ALPHA_SIGMA`。
⛔ **不能用 `distance_transform` 直接做软边** —— 它给整数距离，会退化成二值，实测半透明像素 = 0%。

## 三、已标定参数（`line_keying.py` 出厂值）

| 参数 | 值 | 说明 |
|---|---|---|
| `TOL_OUT` | 30 | pass1 可通行阈值 |
| `SEED_MAX` | 12 | 种子必须"像背景"的严格阈值 |
| `TOL_HOLE` | 40 | pass2 泛洪阈值 |
| `MAX_HOLE` | 30000 px² | 单块上限 |
| `MAX_REMOVE_FRAC` | 0.20 | 单帧移除总面积上限，超了整帧放弃 pass2 |
| `MIN_BLOB` | 200 | 小块过滤 |
| `ALPHA_ERODE` | 1 px | |
| `ALPHA_SIGMA` | 0.8 | |

⭐ **参数很不敏感**：`TOL_OUT` 从 20 加到 65，切出的角色像素只差 **3.5%**。因为拦住泛洪的是勾线，不是阈值。**调不干净时不要死调阈值，去查勾线有没有断口。**

## 四、自检：加任何后处理之前先跑一遍

工具会打印一份自检报告：角色像素 / 洞数 / 残留背景。

⛔ **洞数异常就停下**，别继续往后处理。理由见下一条。

## 五、⛔ 实测反效果 · 别再试

| 试过的做法 | 结果 |
|---|---|
| "颜色清理"：距背景 < N 就扣 | ⛔ 挖洞。色板距离 ≠ 像素级安全 |
| 精确去污染 `F=(C−(1−α)·BG)/α` | ⛔ 过度放大颜色 |
| 混合方程反解 `α=\|C−BG\|/\|F−BG\|` | ⛔ 边缘满圈麻点 |
| 分块放大建模（头部放大 2x 单跑） | ⛔ 打断 α 连续性 |
| 只用语义模型、不开 alpha_matting | ⛔ 硬 α，等于没做 |
| "两版颜色"（α 取 A 版、RGB 取 B 版） | ⛔ 视频里姿势一变就对不齐 |
| 逐轮死调色阈值 | ⛔ 走两轮只救回 400px，且开始咬角色色 |

⭐ **真正管用的判据全是「几何 + 颜色」组合，不是单看颜色。**

### 一个反直觉的教训

我算过角色主色离背景最近有 **59**，容差给 30 觉得万无一失，结果挖出一堆洞。
原因：那个 59 是**颜色代表值**之间的距离，实际像素会被抗锯齿、阴影、混合一路拉近背景。
⇒ **能担保像素安全的，只有在像素上量一遍，没有别的办法。**

### 验证底色选错 = 没验证

拿**中灰底**"验证"了一版觉得挺好，交出去被打回来。因为残留背景本身就是灰的，合成到灰底上和透明区长一模一样。

⇒ **验证一律用青色底**（`(0,255,255)` 之类）：透明显青、残留显灰，一眼现形。

## 六、两个"静默不挖"的 bug（比 bug 值钱）

症状跟"漏抠"一模一样，根因全在内部记账：

- ⛔⛔ **`cv2.floodFill` 不检查起点的值。** 种子落在被剔除的掩码上时，它把**整片 0 区**当填充区，实测淹掉 95 万像素（≈整图）→ 被单块上限拦下 → 整块 skip。**19/38 个候选块中招，整整一半。**
- ⛔ **泛洪掩码那段代码被整段复制了两遍** → 移除量重复累加 → 误触单帧总量闸 → 整帧回滚到 pass1 → 该挖的全没挖。

> ⭐ **教训：上限类逻辑会掩盖 bug。** 单块上限把 95 万像素拦下来了，程序不崩、不报错、日志只有一句 `skip` —— 看起来像正常的保守跳过，实际是 bug 在隐身。
> ✅ 所以任何"超上限就跳过"的分支**必须带计数器或告警**。

## 七、序列（视频抽帧）上的三个补丁

逐帧独立的做法在序列上会闪烁。见 `scripts/temporal_keying.py`：时域中值平滑 + 洞数突变检测 + 首末帧锚定。

## 八、已知物理下限（写进说明，别承诺做不到的事）

发梢边缘的**混合像素**既非背景也非前景。任何阈值方法只能在

- **削细发丝**  ↔  **留一圈淡边**

之间二选一。**这不是参数问题，是物理下限。**

唯一还在收的失败模式：**勾线断口** —— 线断了泛洪就钻进去。见 `references/LINE_KEYING.md`。

## 九、文件

| 文件 | 用途 |
|---|---|
| `scripts/line_keying.py` | 勾线切主程序（外轮廓 + 封闭空间 + pass3 补漏） |
| `scripts/keying.py` | 交集法（传统 matting ∩ isnet-anime），带自检报告 |
| `scripts/temporal_keying.py` | 帧序列时域平滑 |
| `references/PITFALLS.md` | 踩坑全集 |
| `references/LINE_KEYING.md` | 勾线切的设计与迭代记录 |
