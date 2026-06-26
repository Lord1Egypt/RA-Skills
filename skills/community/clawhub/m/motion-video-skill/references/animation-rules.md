# Animation Rules

本文件定义“文本内容 -> 动画讲解效果”的默认映射规则。

## 先拆语义，再选版式

在生成 `movie.json` 之前，先把输入内容拆成下面几类：

- 定义 / 金句
- 问题 / 痛点
- 步骤 / 流程
- 对比 / 变化
- 数据 / 结论
- 总结 / 号召

不要先想特效，再硬套内容。

## narration 优先

- 每个 `scene` 都必须有一段对应的 `narration`
- `scene.durationMs` 必须覆盖这段 narration 的朗读长度，再加少量首尾缓冲
- 动画切换点要跟语义停顿走，而不是机械平均分布
- narration 应尽量拆成逐句级 `cues`，后续字幕、bullet reveal 和重点高亮都优先基于 cue
- narration 太长时，应该拆 scene，而不是压缩播放时间

## 推荐映射

### 定义 / 金句

- scene type：`hero`
- 结构：`title` + `subtitle` + `chip`
- 动效：标题 `fade-up`，副标题 `fade`
- 用途：视频开场、观点定义、章节开头

### 问题 / 痛点

- scene type：`problem`
- 结构：大标题 + 短文案 + 1 个强调色块
- 动效：标题 `slide-left`，说明 `fade`
- 用途：先说清“为什么要看这个视频”

### 步骤 / 流程

- scene type：`steps`
- 结构：标题 + `bullet-list`
- 动效：列表用 `itemStaggerMs`
- 转场：优先 `lift-up` 入场
- 用途：教程、操作流程、方法论拆解

### 对比 / 变化

- scene type：`comparison`
- 结构：左右卡片、上下对照或前后变化
- 动效：左侧 `slide-left`，右侧 `slide-right`
- 转场：优先 `wipe-left` 或 `slide-right`
- 用途：剪辑前后、旧方案 vs 新方案、问题 vs 方案

### 数据 / 结论

- scene type：`stat`
- 结构：大数字 / 关键词 + 补充文本
- 动效：`glow-pop`、`zoom-in` 或 `clip-up`
- 用途：记忆点、指标、结论强化

### 总结 / 号召

- scene type：`closing`
- 结构：收束标题 + 口号 / CTA
- 动效：标题 `fade-up`，结尾标签 `pop`
- 转场：优先 `iris-in`
- 用途：视频结束、引导关注、强调下一步动作

## 节奏建议

- 单个 scene 建议 `2400 - 4200 ms`
- 全片 15 到 45 秒时，建议 `4 - 8` 个 scene
- 同一 scene 内最多保留 1 个主标题和 1 组主内容
- 单个 scene 不要超过 4 段入场动画

## 自动 timing 建议

- 标题一般在 scene 开始后 `120 - 240 ms` 内出现
- 副标题、正文和 quote 应跟在标题后的第一或第二个语义停顿后出现
- `bullet-list` 的 `itemStaggerMs` 应跟单项讲解长度相关，通常在 `160 - 420 ms`
- 场景切换前至少留 `240 - 420 ms` 的收尾空间
- 如果已有逐句 cue，标题、bullet 和字幕优先锚定 cue，而不是继续平均估算

## cue 和字幕轨建议

- 逐句 cue 是讲解视频里最值得保留的中间层
- 字幕轨应默认直接消费 scene cue，不要再单独手写一遍时间轴
- `bottom-band` 适合课程、产品讲解
- `short-video-pop` 适合强节奏短视频
- `minimal-center` 适合克制、理性、访谈式视频

## scene 入场/出场建议

- `hero`: `zoom-out` 入场，快速建立舞台感
- `problem`: `blur-in` 入场，更像“问题浮现”
- `steps`: `lift-up` 入场，适合流程展开
- `comparison`: `wipe-left` 入场，更像切到另一组信息
- `closing`: `iris-in` 入场，更有收束感

## 动效使用建议

- `fade`: 最稳妥，适合副标题、注释、收尾说明
- `fade-up`: 最像讲解型动效，适合标题和结论
- `slide-left` / `slide-right`: 适合对比、卡片分栏和结构切入
- `pop`: 适合数字、标签、CTA、小结论
- `clip-up`: 适合做强调条、遮罩式揭示
- `zoom-in`: 适合结论卡、重点卡片
- `blur-in`: 适合副标题、quote、较有氛围感的文案
- `glow-pop`: 适合关键数字、CTA、亮点词
- `swing-up`: 适合带一点态度感的标题
- `reveal-right` / `reveal-down`: 适合做遮罩揭示和字幕式展开

## 不建议的情况

- 不要在一个 scene 内同时使用 4 种不同入场方向
- 不要把长段落做成密集字幕墙
- 不要让装饰性 shape 的视觉权重超过正文
- 不要为了“像 AE”而牺牲可读性
