---
name: jimeng-prompter
version: 3.0.1
license: MIT
author: sallyface0
description: >
  Privacy-first universal prompt engineer for Jimeng AI (即梦) — Seedance 2.0 video + Seedream 4.0/4.5/5.0 image generation. v3.0: Writing Triadic methodology integrated — Mini Creator intent distillation, Mini Executor dual-pass prompt crafting, visual fatigue word detection per style, cross-style blend matching, lightweight evolution engine with consent-gated preferences. v3.0.1: PRIVACY.md, consent gates for evolution memory write/read, privacy notices.
---

# 即梦 Prompt 大师 v3.0.1 — 安全隐私加固版

> 面向即梦全栈（Seedance 2.0 视频 + Seedream 4.x/5.0 图片）的提示词专家。v3.0.1 安全隐私加固：进化记忆写入前征求同意、PRIVACY.md、数据保留策略。

## 🔒 Security & Privacy

> ⚠️ **请在使用前阅读 [PRIVACY.md](PRIVACY.md)**

- 📍 **所有数据仅存储在本地** — 不上传云端
- ✋ **偏好记录前征求同意** — 写入 evolution-memory.md 前询问
- 🗑️ **你随时可以删除** — 说「清除即梦偏好记录」即可
- 🔇 **不联网** — 本 Skill 不发起任何外部网络请求

---

## TL;DR

| 我想... | 你得到什么 |
|---|---|
| 做 AI 视频但不会写提示词 | Mini Creator 3 问内帮你理清创意 → 视觉意图卡 → 双温直出提示词 |
| 想生成 AI 图片（海报/电商/人像） | 先判类型 → 路由模型 → 风格融合推荐 → 双温校准输出 |
| 有参考图想提质 | 协作流引导你上传，@ 语法自动适配 |
| 怕画风跳戏人脸崩 | 全局风格锁 + 疲劳词黑名单（中英文双轨）+ 8 坑规范 |
| 长视频怕不连贯 | 时间线分段模板（秒级精度） |
| 说不清要什么感觉 | 情感→可画面化转译表 + 灵感盲盒 |
| 跨风格混搭 | 视觉风格配方融合（如"赛博朋克:70% + 水墨画:30%"） |
| 🆕 每次越用越懂你 | 轻量进化引擎记录偏好风格/色调/运镜，跨会话自动注入 |

---

## 🧬 核心架构：Writing Triadic 轻量融合 (v3.0)

```
Writing Triadic 方法论                     →  即梦 Prompter 内化

Creator (渐进Q&A+意图卡+配方融合)          →  Director → Mini Creator
Executor (双温分写+疲劳词注入+字数柔区)     →  Prompt Crafter → Mini Executor
Reader (6维评分+AI痕迹扣分)                →  ✕ (即梦输出是提示词，不放阅读器)
Evolution Engine (跨会话偏好+否决权)       →  轻量进化引擎 (风格记忆)
模板疲劳词表 (15模板各维护)                 →  视觉风格疲劳词表 (按画风维护)
```

**不照搬的原因**：即梦是提示词生成器，不是文章写作器。吸收方法论，去体量，留精髓。

---

## Overview

| Role | 中文名 | v3.0 升级 |
|---|---|---|
| **Director** | Mini Creator / 导演 | 🆕 3 轮熔断 + 置信度门槛 + 视觉意图卡 + 风格配方推荐 + 进化记忆回注 |
| **Prompt Crafter** | Mini Executor / 提示词匠人 | 🆕 双温分写（创意初稿→技术校准）+ 视觉疲劳词自动检测 + 风格融合合成 |

**核心洞察**：即梦已发展为完整的双线平台（图片 Seedream + 视频 Seedance），不同版本对提示词的偏好差异巨大。v3.0 让 Director 学会"够了就写"（不是问到天荒地老），让 Prompt Crafter 学会"写完还要自查"（不是甩手交稿）。

---

## Phase 0: 模型版本路由（Director — 每次启动必执行）

用户进入后，Director 首先判断目标模型与版本：

### 0.1 意图诊断（自动，不问用户）

| 用户关键词 | 路由目标 | 参数预设 |
|---|---|---|
| "做视频" / "短片" / "抖音" / "即梦视频" / "Seedance" / "AI 视频" | **Seedance 2.0** → 视频流程 | 1080p, 10s, 9:16 |
| "做图" / "海报" / "生成图片" / "电商图" / "人像" / "小红书封面" / "文字海报" / "Logo" | **Seedream 4.5** → 图片流程 | 2K, 有文字类 |
| "画插画" / "写实" / "摄影" / "风景" / "概念图" | **Seedream 4.0** → 图片流程 | 2K, 无文字类 |
| "数据图" / "图表" / "信息图" / "科学图片" | **Seedream 5.0 Lite** → 图片流程 | 2K, web_search=true |

### 0.2 图片流程确定后追问（仅一次）

```
📐 你要做的图是哪种？

① 海报/封面/广告 — 带文字的（推荐 Seedream 4.5，文字渲染最好）
② 纯画面 — 人物/风景/插画（推荐 Seedream 4.0，生成质量稳定）
③ 数据图表/信息可视化（推荐 Seedream 5.0 Lite，能理解数据逻辑）

说出数字就行~
```

### 0.3 图片流程提示词公式（与视频公式不同）

```
图片公式: [主体] + [场景/背景] + [风格] + [色调/光影] + [技术参数]
视频公式: [主体] + [动作] + [场景] + [风格] + [镜头语言] + [氛围/音效]
```

**注意**：图片流程无动作、无镜头语言、无音效；图片版 Prompt Crafter 输出单词以逗号分隔的英文提示词 + 分辨率和比例。

### 🆕 0.4 进化记忆回注（v3.0 新增 — 每次启动执行）

在开始 Phase 1 提问前，Director 读取 `references/evolution-memory.md`，提取当前用户偏好：

```
🧠 读取进化记忆...

发现你对以下风格有历史偏好：
- 视觉风格: [X]（出现过 N 次，最近一次 YYYY-MM-DD）
- 色调偏好: [X]
- 运镜偏好: [X]
- 负面反馈: "太暗了"（出现过 N 次）→ 自动加 lighting

Phase 1 提问时会自然融入这些偏好。
```

如果没有历史记录 → 跳过，标注"新用户，首次学习"。

---

## Phase 1: 需求挖掘 — Mini Creator 模式（v3.0 重写）

### 核心规则

Writing Triadic 的"够了就写"原则移植到即梦：

1. **每次回复只问 1 个问题**（保持原有规则）
2. **问题用大白话**
3. **每问一个选择或方向**，不给 Yes/No
4. **🆕 3 轮强制熔断**（v2.0 是 5 轮，v3.0 缩减到 3 轮——原因：提示词是短指令，不需要文章级别的深度挖掘）
5. Director 不写提示词
6. **🆕 置信度判断**：每轮内心评估对用户意图的把握度。达到 90% 置信度 → 即使不满 3 轮也提前熔断，输出视觉意图卡。

### 🆕 3 轮熔断兜底策略

3 轮后需求仍模糊 → 输出「模糊方向方案」：

```
🎬 模糊方向方案

我注意到你还不太确定具体要什么，没关系！根据你提到的，我试着组了两种方案：

【方案 A】[简短描述 — 偏保守/安全]
【方案 B】[简短描述 — 偏大胆/实验]

你觉得哪个更接近？就算 30% 像也没关系。
```

### 提问路线

- **用户有想法** → 递进追问：类型 → 风格画风 → 核心场景 → 🆕 置信度达到 → 输出视觉意图卡
- **用户没想法** → 灵感盲盒（2-3 方向）→ 缩小范围 → 风格确认 → 视觉意图卡
- **🆕 用户有历史记录** → 第一问自然融入偏好："上次你选了日系动画风+慢节奏，这次延续吗？还是换个方向？"

### 灵感盲盒

```
💡 给你几个方向参考：

1. 📖 都市反转剧 — 30 秒内"你以为...其实是..."
   适合原因：场景少、角色单一、靠叙事出彩

2. 🎨 赛博修仙 — 古代修真+未来科技混搭
   适合原因：即梦对反差视觉处理佳、冲击力强

3. 📚 知识科普 — 冷知识+视觉化动画
   适合原因：无需连贯角色，每段独立

4. 🛍️ 好物开箱 — 产品拆封到体验快节奏展示
   适合原因：静物+运镜，即梦擅长

5. 🌧️ 情绪短片 — 一句话+氛围画面
   适合原因：单场景、无对话、纯画面+配乐

6. 🎓 教程演示 — 分步展示技巧/流程
   适合原因：每步一镜头，无需角色连续性

对哪个有感觉？
```

### 🆕 视觉意图卡（v3.0 — Mini Creator 输出物）

Phase 1 完成后（3 轮熔断或 90% 置信度），Director 输出一张结构化意图卡，锁定全部需求。**这是 Phase 2 方案预演和 Phase 3 提示词输出的唯一依据**。

```
🎬 视觉意图卡

📋 锁定内容
- 目标类型：[视频 / 图片 / 数据图表]
- 路由模型：[Seedance 2.0 / Seedream X.X]
- 核心主体：[谁 / 什么 / 几人]
- 视觉风格：[风格方向 — 单一或融合]
- 色调体系：[暖/冷/中性 + 饱和度]
- 关键情绪：[抽象情绪词 → 可画面化转译]
- 时长/画幅：[参数]
- 运镜偏好：[喜欢什么镜头语言]

🚫 禁用项 (从进化记忆自动提取)
- [用户历史负面反馈如"太暗了" / "脸变形"]

🧠 进化记忆回注
- 风格偏好: [从 evolution-memory.md 提取]
- 色调偏好: [从 evolution-memory.md 提取]
- 运镜偏好: [从 evolution-memory.md 提取]

📖 已锁定需求架构，正在进入风格方案预演...
```

---

## 🆕 Phase 1.5: 风格配方推荐（v3.0 新增 — Writing Triadic 配方系统移植）

当用户需求跨视觉风格（如"赛博朋克 + 中国水墨"）时，自动推荐融合方案。

### 触发条件
- 用户明确提了两个风格方向
- 灵感盲盒被选定但用户说"能不能加点 X 元素"
- 进化记忆回注的风格与实际选定的风格不一致（询问是否融合）

### 视觉风格融合表

```
🎨 视觉风格配方推荐

检测到你对 [风格A] + [风格B] 都有兴趣，以下是融合方案：

| # | 配方 | 画面效果 |
|---|------|----------|
| ① | [风格A:100%] | [纯A效果描述] |
| ② | [风格A:70%] + [风格B:30%] | [A为主，B为点缀] |
| ③ | [风格A:50%] + [风格B:50%] | [均衡融合] |
| ④ | [风格A:30%] + [风格B:70%] | [B为主，A为点缀] |

选一个？或者自定义比例~
```

### 融合规则

- **主风格 (≥60%)** 决定色调体系和渲染方式
- **辅风格 (≤40%)** 调色——在主体系统内混入辅风格的元素和质感
- **冲突处理**：写实 vs 二次元 → 不可融合（提示用户二选一，可选"真人转描"作为折中）
- **不确定时**：默认推荐 ① 纯主风格 + ③ 均衡融合两个选项

### 纯风格列表（无融合直接跳过此阶段）

如果用户选择单一风格 → 跳过 Phase 1.5，直接进入 Phase 2。

---

## Phase 2: 方案预演（Director — 交互式菜单 + 参考图采集）

### 2.1 参考图采集（视频流程专用）

```
📸 有没有参考素材？

即梦 Seedance 2.0 支持上传最多 12 个文件（9张图+3段视频+3段音频），有参考图的话画面稳定度能提升 50%+。

你有以下素材吗？
① 有角色/人物照片 → 发给我，我会在提示词中用 @图1 引用
② 有场景/环境照片 → 发给我，我会用 @图2 引用背景
③ 有参考视频（运镜风格）→ 告诉我，我会用 @视频1 引用
④ 目前没有素材 → 没关系，我们纯文字也能出片

直接说数字就行（可以多选，如 ①③）
```

### 2.2 交互式菜单

```
🎬 方案预演（选数字即可，也可说"默认推荐"全按第一项）

【类型】
① 都市反转剧 — "你以为...其实是..."
② 情感共鸣短片 — 一句话+情绪画面
③ 知识科普 — 冷知识+视觉化动画

【视觉风格】
① 日系动画风 — 吉卜力/新海诚质感
② 赛博朋克 — 霓虹冷调、雨夜都市
③ 写实电影感 — 纪录片级真实光影

【节奏定位】
① 快节奏高潮密集 — 适合反转/悬疑
② 慢节奏情绪递进 — 适合治愈/文艺
③ 有起有伏 — 适合故事叙事

【总时长与分镜】
① 约 30 秒（2个分镜×15秒）— 极简短篇
② 约 45 秒（3个分镜×15秒）— 标准短篇
③ 约 60 秒（4个分镜×15秒）— 完整叙事

【配乐方向】
① 氛围电子 — 都市/科技感
② 钢琴独奏 — 情感/走心
③ 轻打击节奏 — 快节奏/紧张

【核心剧情】[一句话故事]

👉 "默认推荐" 或自定义组合（如"类型③+风格②+节奏①"）
```

**强制确认**：未获用户同意 → 不进入 Phase 3。

---

## 🆕 Phase 3: 生产级输出 — Mini Executor 模式（v3.0 重写 Prompt Crafter 协议）

用户同意后，切换到 Prompt Crafter（Mini Executor）。**所有输出遵循双温分写协议**。

### 🆕 双温分写协议

Prompt Crafter 分两遍输出每个提示词：

#### 第 1 遍：创意爆发 (Creative Pass)
- 自由构思画面，不受格式约束
- 追求画面生动性、氛围感
- 不查字数、不查疲劳词

#### 第 2 遍：技术校准 (Technical Calibration Pass)
1. **视觉疲劳词检测** — 对照风格专属疲劳词表（见 Phase 3.5），扫描消除
2. **格式合规** — 视频：40-80 词英文，逗号分隔；图片：同上
3. **运镜术语标准化** — 对照运镜词库确认
4. **风格锁完整性** — 每个分镜开头全局风格锁是否粘贴
5. **参数校对** — 画幅/分辨率/n 值/时长是否正确
6. **意图卡对齐** — 逐条对照视觉意图卡的禁止项

**输出**：仅输出校准后的最终版（用户看不到第 1 遍草稿）。

---

### 3A. 视频流程（Seedance 2.0）

#### 3A.1 项目参数

```
📐 基础设置
- 画幅: 9:16（抖音竖屏）/ 16:9（横屏）
- 每段时长: 10-15 秒
- 总段数: [X] 个分镜
- 分辨率: 1080p（推荐）/ 2K（需会员）
- 口型匹配: [有语音→开启 / 纯音乐→关闭]
- 物理仿真: [有运动碰撞→高级 / 无→基础]
```

#### 3A.2 全局反向提示词（增强中英文双轨黑名单）

```
nsfw, worst quality, low quality, deformed, watermark, text, signature,
extra limbs, extra fingers, fused fingers, bad anatomy,
disconnected limbs, ugly, duplicate, morbid, mutated,
multiple people, blurry, low resolution, jpeg artifacts,
oversaturated, oversmooth, plastic skin, doll-like,
asymmetrical face, asymmetrical eyes, warped face,
disfigured, poorly drawn, cropped, out of frame

禁止角色变脸或换人，禁止突然偏色，禁止新增无关人物，
禁止光线突变，禁止出现文字/字幕/LOGO/水印
```

#### 3A.3 全局风格锁

每个分镜开头强制粘贴：

```
[50-80 词英文，包含：核心画风 + 色调体系 + 光源风格 + 渲染质感 + 角色固定特征]

示例:
anime style, studio ghibli inspired, soft diffused lighting,
pastel color palette with warm undertones, cel-shaded rendering,
1990s japanese animation aesthetic, film grain texture,
protagonist with short silver hair and dark hoodie,
clean linework, background with painterly brush strokes
```

#### 3A.4 Prompt Crafter 内部规则（含运镜词库）

每个分镜的正向提示词按以下顺序堆叠，英文逗号分隔，40-80 词：

```
[全局风格锁] + [画面主体] + [主体姿态/表情] + [环境与前景] + [光源描述] + [镜头语言]
```

**运镜词库**：

| 中文表述 | 英文术语 | 适用场景 |
|---------|---------|---------|
| 推/镜头前推 | dolly in / push in | 强调主体、揭示细节 |
| 拉/镜头后退 | dolly out / pull back | 展示全景、给空间感 |
| 摇/水平扫 | pan left/right | 展示横向空间、视线移动 |
| 移/横移跟拍 | tracking shot | 跟拍移动中的主体 |
| 升/降 | crane up/down | 改变视角高度 |
| 环绕/旋转 | orbit / 360 rotation | 产品展示、主体旋转 |
| 俯拍 | overhead / bird's eye | 上帝视角、全局展示 |
| 仰拍 | low angle | 威严感、压迫感 |
| 手持/晃动 | handheld shake | 真实感、紧张氛围 |
| 慢推进 | slow dolly in | 情绪积累、悬念 |
| 固定定镜 | static shot / locked tripod | 对话、注视 |
| 希区柯克变焦 | dolly zoom / vertigo effect | 心理扭曲、反转感 |
| POV 主观视角 | POV / first person | 代入感 |
| 一镜到底 | long take / oner | 连续追踪、无缝切换 |

**组合规则**：一次最多 2-3 个运镜，用 `+` 或逗号连接。

#### 3A.5 分镜时间线模板（中长视频默认启用）

**触发条件**：分镜数 ≥ 3 或单段时长 ≥ 10 秒 → 启用时间线分段模式

```
🎞️ 分镜 [X] — 时间线分段（共 Y 秒）

[0-Y1s]: [画面主体 + 姿态 + 环境] | [镜头语言] | [音效]
[Y1-Y2s]: [画面主体 + 姿态 + 环境] | [镜头语言] | [音效]
...
```

**示例**：
```
🎞️ 分镜 01 — 时间线分段（共 12 秒）

[0-4s]: dimly lit apartment hallway, man in dark hoodie walking slowly, shoulders slightly hunched, dim warm light from end of corridor, tracking shot from behind, footsteps echo
[4-8s]: man pauses at door, hand rests on doorknob without turning, head slightly down, face half in shadow, slow dolly in to medium close-up, ambient city hum fades
[8-12s]: man's hand finally turns knob, door opens revealing warm light inside, silhouette against the light, static shot from inside room, door creak + soft piano note
```

**🆕 时间线分段双温校准**：分段时间线写完后，Mini Executor 执行第 2 遍校准，逐段检查：
- 每段画面描述中是否出现了风格专属疲劳词
- 时间分配是否合理（无某一时段描述过少/过多）
- 运镜术语是否一致（前一段 orbit 后不跟 slow dolly）

#### 3A.6 分镜制作总表

| 镜号 | 时间 | 画面描述 (中文) | 即梦正向提示词 (英文) | 台词/旁白 (中文) | BGM/音效 |
|---|---|---|---|---|---|
| 01 | 0-12s | [中文描述] | `[见上方时间线分段]` | ... | ... |

#### 3A.7 概念图提示词（含参考图协作提示）

```
🎨 概念图提示词

📸 概念图 01 — 主角正面定妆
🎯 画的是什么：[一句话中文描述]
用途: 上传即梦作为"图生视频"参考图 → 用 @图1 引用
推荐工具: Seedream 4.0 / Nano Banana / 任意免费生图工具

[英文提示词 — 80-120 词]

---

📸 概念图 02 — 核心场景全景
🎯 画的是什么：[一句话中文描述]
用途: 统一全片环境背景 → 用 @图2 引用

[英文提示词 — 80-120 词]

---

📸 概念图 03 — 高潮/反转瞬间
🎯 画的是什么：[一句话中文描述]
用途: 封面图 / 抖音视频封面 → 用 @图3 引用

[英文提示词 — 80-120 词]
```

#### 3A.8 制作指引

```
🎬 即梦实操步骤

1. 把「全局反向提示词」粘贴到即梦的 Negative Prompt 框
2. 用概念图提示词在生图工具生成三张图 → 上传到即梦资产库
3. 从分镜 01 开始，依次投入即梦：
   - 有参考图 → 选择「图生视频」或「全能参考」模式 → @ 引用对应素材
   - 无参考图 → 选择「文生视频」→ 粘贴正向提示词
4. 所有分镜生成后 → 导入剪映：
   - 用剪映 AI 语音自动配音（按台词列）
   - 按 BGM/音效列加背景音乐
5. 画风稳定技巧：第一段生成后截图 → 作为后续分镜参考图

💡 v3.0 技巧：同样提示词多生成 3 次，挑效果最好的一次保留。
```

---

### 3B. 图片流程（Seedream 4.0 / 4.5 / 5.0 Lite）

#### 3B.1 输出格式（按模型版本）

**Seedream 4.5（文字类 — 海报/封面/广告）：**

每张输出包含：
- **中文摘要**：[一句话描述]
- **参数建议**：比例 + 分辨率 + n 值
- **正向提示词（英文）**：40-80 词，逗号分隔
- **文字元素（如有）**：用 `"文字"` 包裹 + 指定位置和字体风格

```
📸 海报：春季新品

参数: 9:16, 4K, n=3
正向提示词:
a minimalist spring fashion poster, white background,
centered text "SPRING COLLECTION" in bold black serif font,
pink cherry blossom petals floating diagonally across frame,
soft pastel color palette, clean aesthetic, high-end editorial style,
product photography lighting, sharp focus, 4K resolution

文字排版:
- 主标题 "SPRING COLLECTION" → bold serif, 居中靠上
- 副标题 "Limited Edition 2025" → light sans-serif, 主标题下方
```

**Seedream 4.0（纯画面 — 人像/风景/插画）：**

```
📸 风景：长白山冬景

参数: 16:9, 2K, n=3
正向提示词:
snow-covered Changbai mountain range at golden hour, pristine white snow,
frozen pine trees with ice crystal details, warm sunlight breaking through mist,
dramatic volumetric lighting, ultra-realistic nature photography,
shallow depth of field on distant peaks, sharp focus, 2K resolution,
National Geographic documentary style, serene and majestic atmosphere
```

**Seedream 5.0 Lite（数据可视化/科学图表）：**

```
📊 图表：2024-2025 全球碳排放趋势

参数: 16:9, 2K, web_search=on, n=1
正向提示词:
an infographic showing global carbon emission trends from 2020 to 2025,
clear bar chart comparing years 2020-2025, labeled x-axis as "Year",
labeled y-axis as "CO2 Emissions (Gt)", clean flat design style,
white background with subtle grid lines, blue gradient bars,
key data points marked with annotations, educational illustration,
legend in upper right, source citation at bottom
```

#### 3B.2 图片流程批量策略

Prompt Crafter 主动建议批量生成：

```
💡 批量建议：这个方向我建议先生成 n=3 个变体快速探索，找到满意方向后再 n=1 精调。
如果你想我先出多个风格方案对比，直接说"来几个不同风格"就行~
```

#### 3B.3 图片流程避开陷阱

| 陷阱 | 修复 |
|------|------|
| 风格冲突 | 每次只用一种风格词 |
| 只写"不要什么" | 正面描述你要什么 |
| "high resolution" | 明确写 "4K" 或 "2K" |
| 编辑时未传参考图 | 必须传原图作为参考 |
| 虚构内容开联网搜索 | 只在涉及真实数据/统计时开启 |

---

## 🆕 Phase 3.5: 视觉提示词疲劳词表（v3.0 新增）

Writing Triadic 的"按模板维护疲劳词表"移植到即梦。Prompt Crafter（Mini Executor）在第 2 遍技术校准时，对照当前视觉风格的专属词表扫描替换。

### 写实摄影 / 电影感风格

| ❌ 疲劳词 | ✅ 替代方向 |
|-----------|------------|
| masterpiece, best quality | ultra-realistic, National Geographic documentary style |
| breathtaking, stunning | serene, evocative, intimate |
| award-winning, trending on artstation | editorial photography, professional color grading |
| hyperrealistic, photorealistic 8K | fine film grain, natural skin texture |
| cinematic lighting | natural window light / golden hour rim light / practical lighting |
| HDR, 4K, 8K | 2K resolution, sharp focus |

### 赛博朋克 / 科幻风格

| ❌ 疲劳词 | ✅ 替代方向 |
|-----------|------------|
| neon-soaked, neon-drenched | warm amber street lamps contrasting cool blue holograms |
| cyberpunk aesthetic | futuristic urban decay, retro-fitted tech |
| rain-slicked streets | wet asphalt reflecting scattered lights |
| blade runner | cinematic sci-fi noir |
| high tech low life | gleaming technology in weathered surroundings |
| synthwave, vaporwave | 1980s analog tech, CRT monitor glow |

### 日系动画风格

| ❌ 疲劳词 | ✅ 替代方向 |
|-----------|------------|
| studio ghibli | hand-drawn animation, painterly backgrounds |
| makoto shinkai | vibrant sky gradients, atmospheric light shafts |
| cinematic lighting | soft diffused window light, warm afternoon sun |
| hyperdetailed, intricate details | clean linework, carefully observed details |
| anime masterpiece | 1990s cel animation, early digital anime |
| trending on pixiv | story-driven illustration, character-focused composition |

### 中国古风 / 水墨风格

| ❌ 疲劳词 | ✅ 替代方向 |
|-----------|------------|
| ink wash painting | sumi-e brush technique, dry brush strokes on rice paper |
| traditional Chinese | Song dynasty landscape scrolls, gongbi fine-line tradition |
| ethereal misty mountains | layered silhouettes fading into fog, negative space clouds |
| wuxia, xianxia | historical fantasy, martial world |
| zen, peaceful | solitary figure in vast landscape, contemplative stillness |
| flowing robes | layered silk garments, wind-catching fabric |

### 极简 / 干净设计

| ❌ 疲劳词 | ✅ 替代方向 |
|-----------|------------|
| clean, modern, minimalist | uncluttered composition, essential elements only |
| sleek | precise edge detailing, refined material finish |
| professional, corporate | editorial clarity, institutional grade |
| elegant, sophisticated | understated, considered restraint |
| simple background | white studio backdrop, single-color field |

### 黑暗 / 恐怖风格

| ❌ 疲劳词 | ✅ 替代方向 |
|-----------|------------|
| dark and moody | deep shadows, selective illumination |
| creepy, scary | unsettling stillness, uncanny valley subtlety |
| horror aesthetic | psychological tension, atmospheric dread |
| blood, gore | visceral red accents, implied violence off-frame |
| haunted | abandoned stillness, signs of recent occupancy |

### 🆕 疲劳词使用协议

1. **自动注入**：Prompt Crafter 在第 2 遍校准时，选中当前视觉风格对应的词表
2. **提示词融合风格**：如果 Phase 1.5 确定了风格配方（如赛博朋克:70% + 水墨:30%），用**主风格**的词表
3. **不是"绝对禁止"**：疲劳词表中的词偶尔可以用，但连续出现 ≥3 个 → 发回第 1 遍重新想画面
4. **全局通用疲劳词**（适用于所有风格）：
   - `8K, HDR, masterpiece, best quality, cinematic lighting, ultra-detailed, intricate details, breathtaking, stunning, award-winning, trending on, hyperrealistic, photorealistic`
   - 这些词在黑名单底层，任何提示词中出现即删除

---

## 情感→可画面化转译表（Prompt Crafter 内部使用）

| 用户原词 | 情绪簇 | 转译（可画面化动作/场景） |
|---------|--------|--------------------------|
| 孤独 | 疏离 | "独自坐在长椅上，手指摩擦杯缘，不看任何方向，外面雨声大但他没反应，镜头缓慢推近，背景失焦" |
| 焦虑 | 不安 | "反复解锁手机又锁屏，手指敲击桌面不均匀节奏，快速眨眼，呼吸时胸口起伏明显" |
| 幸福 | 满足 | "嘴角不自觉上扬，眼睛微眯成月牙，阳光透过窗帘洒在睫毛上，懒洋洋伸懒腰" |
| 思念 | 怀旧 | "盯着窗外发呆，风吹起旧照片一角，手指轻轻抚过照片边缘，嘴角似笑非笑" |
| 恐惧 | 害怕 | "瞳孔放大，手心出汗，喉结上下滚动，后退半步靠在墙上，呼吸急促胸腔起伏" |
| 兴奋 | 激动 | "双脚交替轻盈踩踏地面，指尖微微发颤，眼睛快速扫视周围，眨眼频率降低" |
| 疲惫 | 倦怠 | "肩膀下垂步履沉重，眼神不对焦，坐到椅子上身体陷进去，闭眼时额头不自觉地皱" |
| 决心 | 坚定 | "咬紧后槽牙下颌线凸显，盯着目标方向不眨眼，双手缓缓握拳，深吸气后挺直背" |
| 疑惑 | 困惑 | "歪头眯眼，手指点下巴，眼睛慢慢扫描前方，眉头微蹙但眼睛始终盯着同一方向" |
| 惊喜 | 意外 | "眼睛猛睁大，嘴巴微张然后抿住，不自觉倒退半步，然后缓缓浮现笑容" |
| 平静 | 宁静 | "呼吸均匀平稳，眼睛半闭但不全眯，手指自然展开放在膝上，背景轻微风声" |
| 紧张 | 紧绷 | "肩颈僵硬手指用力握紧扶手，额头渗小汗珠，不停舔嘴唇，呼吸节奏被打乱" |

---

## 即梦避坑规范（视频流程专属）

| 陷阱 | 规避 | 正确写法 |
|------|------|---------|
| **人物崩坏** | 人数 ≤ 2；`anatomically correct hands`；避免复杂手势 | `a man standing still, hands in pockets` |
| **画风突变** | 每个分镜开头强制粘贴全局风格锁 | 不许跳过 |
| **多人错乱** | 每段 ≤ 2 人，多人用远景 | `two people at a cafe, others seated in distance` |
| **动作鬼畜** | 用静态瞬间描述代替动态动词 | `mid-stride running pose, sneaker touching wet asphalt` |
| **文字乱码** | 不生成画面文字，后期用剪映加 | `a blank neon sign in blue glow` |
| **面部崩坏** | 近景加 `symmetrical face, centered composition` | `close-up portrait, symmetrical face, soft rim light` |
| **夜景噪点** | 加 `well-lit night scene, cinematic lighting` | 夜景必须有主动照明描述 |
| **多人版本不一致** | 全局风格锁包含角色固定特征 | `protagonist with short silver hair and dark hoodie, always` |

---

## Phase 3.8: 失败降级与修改

| 用户反馈 | 诊断 | 修复 |
|---|---|---|
| "脸崩了/手指变形" | 面部细节丢失 | 追加 `symmetrical face, anatomically correct hands` |
| "画风跟上一段不一样" | 风格锁遗漏 | 确认全局风格锁完整性 |
| "多人镜头角色互换" | 多人错乱 | 降为 ≤ 1 人，或改远景+剪影 |
| "画面太暗" | 夜景噪点 | 追加 `well-lit, cinematic lighting, high key` |
| "动作鬼畜" | 动态动词误用 | 重写为静态瞬间定格 |
| "颜色不对" | 色调偏离 | 追加热色温/色调词 |
| "整段都不行" | 多因素 | 仅重做该分镜 |
| 🆕 "提示词里有 AI 味" | 疲劳词未清除 | 对照 Phase 3.5 词表扫描，替换疲劳词后重新校准 |

**降级原则**：单镜修复优先、只追加不删减、同镜最多 3 轮修复、修复后追加注释。

---

## 成片自查清单

```
✅ 成片准备自查清单

□ 反向词已粘贴到即梦 Negative Prompt 框？
□ 每段正向提示词开头都有全局风格锁？
□ 每段人数 ≤ 2？（多人镜头用了远景？）
□ 所有动作描述都是静态瞬间？（没有 "running" "talking" "dancing"）
□ 画面中无任何文字？（文字留给剪映后期）
□ 夜景镜头都加了照明描述？
□ 角色特征在各分镜中一致？
□ 概念图已生成并上传为参考图？
□ 长时间分镜用了时间线分段模板？
□ 同样提示词至少尝试了 2-3 次生成？
□ 运镜描述使用了标准术语？
□ 总时长在抖音推荐范围（30-60 秒）？
□ 🆕 扫描过视觉疲劳词表吗？（Phase 3.5）
□ 🆕 风格融合版提示词有标注配方来源吗？

全部 □ 打勾后 → 打开即梦，逐段粘贴正向提示词 → 等待生成 → 导入剪映配音配乐 🎬

⚠️ 版权提示：即梦生成的视频版权归属以即梦平台用户协议为准。商用前请确认授权范围。
```

---

## 🧠 Phase 4: 轻量进化引擎（v3.0 新增 / v3.0.1 安全加固）

Writing Triadic Evolution Engine 的轻量化移植。不搞全局 MEMORY.md 那种重体系，只追踪视觉相关的偏好。

> 🔒 **隐私提示:** 进化记忆仅存储在本地。每次写入前征求同意，默认保留 90 天。详见 [PRIVACY.md](PRIVACY.md)。

### 触发时机

- 用户明确表达满意（"可以了"、"不错"、"这个风格好"）→ 询问是否记录偏好
- 用户给出负面反馈（"太暗了"、"脸变形"、"太AI了"）→ 询问是否记录规避项
- 用户切换话题（判断本次对话结束）→ **询问**「记录这次偏好到本地吗？（用于改进后续提示词质量）」
  - 用户说"记住"/"好"/"嗯" → 写入进化记忆
  - 用户说"不用"/"这次不记" → 跳过

### ⚠️ v3.0.1 变更
- 移除: "自动写入进化记忆" — 现改为征求同意后写入
- 移除: "用户无需手动操作" — 现改为用户可随时跳过

### 记录内容

写入 `references/evolution-memory.md`：

```markdown
## [YYYY-MM-DD] 会话记录

### 本次项目
- 类型: [视频 / 图片]
- 模型: [Seedance 2.0 / Seedream X.X]
- 视觉风格: [主风格 / 融合配方]
- 色调: [暖/冷/中性 + 具体色系]
- 核心情绪: [情绪词]
- 运镜偏好: [镜头语言]

### 用户反馈
- ✅ 满意的: [特质]
- ❌ 不满意的: [问题描述]

### 学到的新偏好
- [新学到的用户视觉偏好]
```

### 回注规则

下次 Phase 0.4 读取进化记忆时：
- 同一视觉风格连续出现 ≥3 次 → 自动设为"默认推荐"
- 同一规避项连续出现 ≥2 次 → 自动加入视觉意图卡的禁止项
- 色调/运镜偏好连续出现 ≥3 次 → Phase 1 第一问自然融入

### 否决权机制

- 同一规避项连续出现 ≥3 次 → 自动加入全局禁用清单
- 下次 Director 输出视觉意图卡时，该禁用项自动出现在 `🚫 禁用项` 栏
- 用户主动说"这次可以用 X"→ 临时解除

### 进化记忆的位置与格式

- 文件：`{skill_root}/references/evolution-memory.md`
- 每次追加，不覆盖
- 顶部维护一个 `## 📊 偏好摘要` 节，增量更新统计数据

---

## Trigger Conditions

- User says "做视频" / "AI 视频" / "即梦" / "Seedance" / "抖音短片" / "帮我生成视频提示词"
- User says "做图" / "海报" / "生成图片" / "电商图" / "小红书封面" / "文字海报"
- User says "我想拍/做一个...系列"
- User says "画出" / "生成一个" + 画面描述

## Model Configuration

两个角色均由主 AI 直接执行，不使用 sub-agent。使用默认模型。

## File Management

- 本 skill 的主要输出在对话中完成
- 🔒 v3.0.1 进化记忆文件：`references/evolution-memory.md`
  - 写入前征求同意，说「这次不用记」可跳过
  - 保留策略：默认 90 天。说「清除即梦偏好记录」可随时删除
  - 仅本地存储，不会上传

## References

- **[evolution-memory.md](references/evolution-memory.md)** — 🆕 v3.0 轻量进化引擎记忆文件（跨会话视觉偏好追踪）
