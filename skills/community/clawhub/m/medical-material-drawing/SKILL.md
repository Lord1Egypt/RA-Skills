---
name: medical-material-drawing
description: 为医学材料、组织工程、骨修复、血管生成、支架机制图等论文配图生成稳定的分镜结构、风格约束与高质量提示词。Use when the user asks for biomaterials figures, scaffold schematics, bone regeneration, defect repair, angiogenesis, osteogenesis, mechanism diagrams, graphical abstracts, or wants a clean publication-style medical illustration in the style of a successful prior figure.
---

# 医学材料绘图 Skill

## 目标

产出适合论文、综述和图形摘要的医学材料示意图，默认追求以下效果：

- 干净、专业、投稿级
- 矢量感强，不走照片写实路线
- 科学逻辑清楚，一眼能看懂“缺损/疾病 -> 材料设计 -> 修复结果”
- 适合后续继续排版到 `Figure`、`TOC graphic`、`graphical abstract`

## 何时使用

当用户提到以下任务时，优先使用这个 skill：

- 医学材料论文配图
- 骨缺损、牙槽嵴、软组织、皮肤、软骨、骨软骨修复示意图
- 支架、微球、水凝胶、膜、涂层、复合材料、药物递送系统机制图
- 血管生成、成骨、免疫调控、屏障作用、细胞迁移、组织再生流程图
- “按之前那张图的风格继续做”
- “做成论文图/图形摘要/机制示意图”

## 先判断用户要的交付物

1. 如果用户只要提示词或构图方案，只输出提示词、分镜和版式建议，不主动生成图片。
2. 如果用户明确要成图，再先整理结构化提示词，然后调用图像生成工具。
3. 如果用户强调论文可编辑、后续还要改字改箭头，优先建议走 `SVG` 或可分层重绘路线，再视需要导出 `PNG`。

## 默认工作流

按下面顺序做，不要一上来就直接堆提示词。

1. 抽取科学主线
   - 缺损或病灶是什么
   - 材料由哪几层/哪几个模块组成
   - 每个模块承担什么功能
   - 生物学结果是什么
   - 时间顺序是否重要
2. 选叙事框架
   - 最常用：`问题/缺损 -> 材料设计 -> 修复结果`
   - 如果强调机制：`材料结构 -> 关键信号/细胞行为 -> 终点组织结果`
   - 如果强调时序：`implantation -> early response -> late regeneration`
3. 生成分镜草案
   - 默认横向 `2` 到 `4` 个 panel
   - 每个 panel 只承载一个核心信息
   - 每个 panel 给一个极短标题
4. 再写提示词
   - 先写主体提示词
   - 再写风格约束
   - 最后补负面约束
5. 生成后复盘
   - 是否像论文图，而不是商业插画
   - 是否标签拥挤
   - 是否科学关系被画反
   - 是否材料和宿主组织区分不清

## 默认版式

- 优先白底
- 优先横向排版
- 默认 `A/B/C` 或 `A/B/C/D` panel 字母放左上角
- 每个 panel 顶部只保留一句短标题
- 标签尽量放到结构外侧，用细引线连接
- 箭头优先表示过程或方向，颜色不要滥用
- 同一个对象在不同 panel 中保持造型一致

## 风格锚点

默认风格接近高质量医学示意图，而不是写实渲染图：

- 解剖结构做适度简化，轮廓清晰
- 边线细且稳，优先深灰或黑色，不要粗黑描边
- 颜色柔和、低饱和、浅梯度
- 允许轻微体积感，但不要金属质感或游戏建模质感
- 材料结构要“可读”，例如通道、孔隙、分层、载药区要明确
- 宿主组织、血管、新生骨、材料本体要一眼区分
- 文本排版像期刊 figure，不像海报宣传图

## 推荐配色

可在不破坏风格统一的前提下替换，但默认先从这一套开始：

- 软组织 / 牙龈：浅粉、肉粉、珊瑚粉
- 骨组织 / 矿化基质：米黄、浅棕、骨色
- 支架 / 水凝胶 / 功能材料：浅蓝、青蓝、灰蓝
- 新生骨 / 成骨区域：青绿、蓝绿
- 血管：暗红、砖红
- 轮廓与引线：深灰，不用纯黑大面积压画面

## 强约束

下面这些约束要尽量固定，除非用户明确要求改：

- 不要照片感皮肤、肉感、血腥渗出或真实手术场景
- 不要高光塑料感、3D 游戏建模感、过强阴影
- 不要背景纹理、花哨光效、漂浮装饰元素
- 不要把标签压在关键结构上
- 不要一张图里塞过多说明文字
- 不要把不同层材料画得混成一团
- 不要把箭头颜色用成彩虹

## 提示词写法

优先输出下面这三段，而不是一整坨长提示词。

### 1. Core prompt

先写清楚科学对象、场景和 panel 结构。

```text
Create a clean publication-quality biomedical schematic illustration for a journal figure.
Theme: [disease/defect/material system].
Layout: [2-4]-panel horizontal figure labeled A, B, C[, D].
Panel A shows [problem / defect / baseline anatomy].
Panel B shows [material design / scaffold architecture / layered construct].
Panel C shows [early biological response / implantation / angiogenesis / immunomodulation].
Panel D shows [late regeneration / tissue repair / functional restoration].
Include clear external labels, thin leader lines, subtle arrows, white background, and consistent anatomy across panels.
```

### 2. Style prompt

把风格往“论文医学图”拉稳。

```text
Style: high-end medical illustration, vector-like clarity, soft pastel palette, subtle gradients, precise outlines, simplified but anatomically credible tissues, clear material microstructure, elegant scientific figure design, not photorealistic, not poster-like, not cartoonish.
```

### 3. Negative prompt

```text
Avoid photorealism, surgical gore, dramatic lighting, glossy 3D render style, cluttered labels, busy background, excessive text, inconsistent anatomy, oversaturated colors, fantasy design, comic style.
```

## 默认输出格式

如果用户没有指定，你可以先给出下面四项：

1. 一句话图意概括
2. 分镜草案
3. 可直接复制的英文提示词
4. 如需二次精修，再补中文改图指令

## 常见图型套路

### 缺损修复类

优先采用：

- `缺损部位`
- `材料植入/结构设计`
- `早期反应`
- `晚期再生`

### 多层材料类

优先强调：

- 上层做什么
- 中间层做什么
- 下层做什么
- 每层对应哪种生物功能

### 机制解释类

优先画清：

- 材料释放什么
- 作用于哪些细胞或组织
- 导致哪些中间事件
- 最终组织结局是什么

## 修图迭代规则

如果第一次生成不理想，优先按下列方向修，不要盲目重写全部提示词。

- 结构不清：减少每个 panel 的信息量
- 材料不像材料：强化 `layered scaffold`, `radial channels`, `porous architecture`, `core-shell`, `mineralized matrix` 之类的结构词
- 解剖不稳：改成 `simplified cross-sectional anatomy`
- 画面太花：强调 `white background`, `minimal clutter`, `publication figure`
- 不像论文图：增加 `journal figure`, `graphical abstract`, `scientific schematic`, `vector-like`
- 颜色脏或太艳：强调 `soft pastel`, `low saturation`, `clean palette`

## 回答模板

用户要你出方案时，优先按这个顺序回答：

1. `图意`
2. `分镜建议`
3. `英文 prompt`
4. `负面约束`
5. `如需我直接生成/继续细化 SVG，请继续说`

## Additional resources

- 示例见 `[examples.md](examples.md)`
