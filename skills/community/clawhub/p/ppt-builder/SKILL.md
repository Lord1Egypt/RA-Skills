---
name: ppt-builder
description: "Build high-quality presentation decks from scratch. Covers the full lifecycle from brainstorming through content writing, visual design, AI image generation, iterative QA, and final delivery. Uses OpenRouter + Nano Banana Pro for slide image generation. No external SaaS dependency."
---

# PPT Builder

从一句话需求到高品质演示 PPT 的完整方法论。覆盖内容策划、文案撰写、视觉设计、AI 生图、QA 迭代、交付全流程。

## When to Use

- 用户想从零开始做一份演示 PPT（产品演示 / pitch deck / 培训材料 / 报告）
- 用户有一个主题但还没有具体内容
- 用户已有内容文档但需要高品质视觉呈现
- 用户想用可复现、可迭代、低成本的方式生成 PPT

## 核心理念

**内容和形式分离**。分三步走，每步独立交付、独立审批：

| Step | 产出 | 关注什么 | 不关注什么 |
|------|------|---------|----------|
| 1. 内容文档 | `content.md` | 说什么、论证逻辑、数据 | 颜色、字体、版式 |
| 2. 设计文档 | `design.md` | 视觉风格、模板、每页版式 | 文案本身 |
| 3. PPT 生成 | `deck.pptx` | 按 Step 1 + 2 落地成品 | 回头改文案或改结构 |

**下游不反向改上游**。如果 Step 3 生成时发现某页内容装不下，回 Step 1 改内容，不在 Step 3 里"压一压"。

---

## 工作流总览（7 个阶段）


阶段 1  Brainstorming → 收敛决策，形成定位
阶段 2  Spec 文档     → 大纲 + 多轮自审 → 批准
阶段 3  内容文档      → 每页文案
阶段 4  设计文档      → 视觉系统 + 模板 + 每页指令
阶段 5  PPT 生成      → Nano Banana 逐页生图 + 组装
阶段 6  QA 迭代       → 只修有问题的页
阶段 7  交付          → pptx + pdf


---

## 阶段 1：Brainstorming

**目标**：把模糊的需求收敛为一份明确的决策清单。

> **推荐 Skill**：如果已安装 `idea-to-design`（头脑风暴 · 从想法到设计），可以先调用它完成通用的 brainstorming 流程（探索上下文 → 逐一提问 → 提出方案 → 呈现设计 → Spec 自审）。本阶段的 PPT 专属决策项作为 brainstorming 的具体问题输入。

### 方法

每次**只问一个问题**，给 3-5 个选项，标注你的推荐。等用户回答后再问下一个。不要一次性抛多个问题。

### 必须收敛的决策

| 决策项 | 为什么重要 | 典型选项 |
|-------|---------|---------|
| **类型** | 通用可复用 / 针对特定客户 / 内部用 | 决定复用性和信息密度 |
| **受众** | 老板 / 中层管理 / 技术人 / 投资人 / 终端用户 | 决定语言、深度、卖点 |
| **使用场景** | 现场讲 / 发给客户自己看 / 双用 | 双用 = 每页必须自解释 |
| **时长和页数** | 15 页精简 / 25 页标准 / 35+ 页深度 | 页数服务于内容，不硬限 |
| **叙事骨架** | 问题驱动 / 场景驱动 / 模块驱动 / 混合 | 决定全 deck 的节奏 |
| **主线故事**（可选）| 用一个具体场景串联整份 deck | 有故事的 deck 代入感强 |
| **视觉风格** | 有参考 PDF / 跟产品视觉统一 / 用形容词描述 | 有参考最好，减少猜测 |
| **数据和案例** | 有真实数据 / 用占位符 / 都没有 | 决定可信度策略 |
| **商业信息** | 明码标价 / 给定位信号 / 不提价格 | 老板关心"我付不付得起" |

### 关键原则

- **接纳用户的重新定义**。用户可能打断你的问法，提出更好的流程框架，接受它
- **不要在 brainstorming 阶段写任何内容**。只做决策，不写文案
- **brainstorming 结束的标志**：所有决策项都有明确答案

---

## 阶段 2：Spec 文档

**目标**：写一份全局定位 + 每页大纲 + 视觉方向的 spec 文档。

### 文档结构


# [Deck名称] - 设计文档

## 1. 全局定位（阶段 1 所有决策的汇总表）
## 2. N 页完整大纲
   ### Part X — [章节名]（M 页）
   | # | 页面 | 核心论点 | 必备内容 |
## 3. 生产流程（三步走 + 每步的验收标准）
## 4. 视觉方向（色彩/字体/背景/关键视觉元素）
## 5. 风险和待补项
## 6. 不在范围（Out of Scope）


### 必做：多轮自审

Spec 写完后必须至少做**两轮自审**，不审不进下一步。

**第一轮：受众视角审**

站在目标受众的角度读一遍大纲，问自己：
- 开场有没有让我继续读的理由？（钩子）
- 这份 deck 70% 在讲我的世界还是在讲产品？（应该是前者）
- 读完我能做什么？（CTA 必须具体可行）
- 有没有让我感觉"又是一个卖概念的"？
- 每一页的标题是我会问的问题还是产品经理的术语？

详细检查清单见 `references/spec-review-checklist.md`

**第二轮：文案质量审**

grep 扫描禁用词（见 `references/writing-principles.md`），确保零正文命中。

### 如果自审发现问题

直接改。改完不需要重新审——修了就过。但严重问题（如结构性缺失）需要标注版本号（v1 → v2）并记录变更原因。

---

## 阶段 3：内容文档

**目标**：写 `content.md`，覆盖每一页的完整文案。

### 粒度策略

| 页面类型 | 粒度 | 原因 |
|---------|------|------|
| **核心页**（主线故事 / 核心宣言 / 关键转折） | **终稿级文案** | 这些页决定 deck 成败 |
| **其他页**（模块展开 / 落地 / 附录） | **结构化要点** | Step 3 生成时根据版式微调 |

### 每页标准格式


### Slide N - [标题]

**核心论点**：[一句话，这页要让读者记住什么]
**详细文案**：[终稿文字 或 3-5 个 bullet 要点]
**图片意图**：[需要什么视觉素材——只讲意图不讲样式]
**关键数据**（可选）：[数字和引用来源，占位用 [待补]]


### 写作铁律

1. **用事实和数据制造张力，不用形容词**
2. **具体 > 抽象**——每句话要么是事实、要么是具体动作
3. **先演示后下定义**——核心 claim 放在故事讲完之后
4. **数据克制**——没有真实数据就用 `[待补]`，别编
5. **每个 CTA 必须此刻能兑现**——不承诺不存在的产物
6. **占位符统一格式**——全部用 `[待补]`，不用 TBD / TODO

详细写作原则见 `references/writing-principles.md`

### 验收

- 禁用词 grep 零正文命中
- 核心 claim 只在指定页出现（如有）
- 人物 / 数字 / 名称全 deck 一致
- 每页都有"核心论点"（没有空壳页）

---

## 阶段 4：设计文档

**目标**：写 `design.md`，定义视觉系统和每页的具体版式。

### 文档结构


## §1 视觉系统
   色彩（hex 值 + 用途）/ 字体（字号层级）/ 背景 / 标志性元素 / 间距

## §2 页面模板库（6-10 种）
   每种模板：用途 / Wireframe / 元素清单 / 尺寸 / 变体 / 禁止事项

## §3 每页设计指令
   每页：模板 / 文案来源 / 图像清单 / 版式要点

## §4 AI 插图 Prompt 清单
   概念插画（需要 AI 生成的）/ 示意图（脚本生成的）/ 图标

## §5 降级版规范（可选）
   投影仪 / 打印 / 移动端 的适配规则


### 模板设计原则

- 模板数量 6-10 种（太少挤进不合适的模板，太多视觉碎片化）
- **最复杂的模板优先设计**——它的质量决定全 deck 品质上限
- 每个模板的"禁止事项"和"允许的变体"必须明确

### 每页设计指令格式


#### Slide N - [标题]
**模板**：[模板名或变体]
**文案来源**：`content.md` Slide N
**图像清单**：
- [ILL-N / SCR-N / DGM-N / ICO-N：描述]
**版式要点**：
- [2-3 条具体指令]


---

## 阶段 5：PPT 生成

**目标**：用 Nano Banana Pro 逐页生成幻灯片图片，组装成 pptx。

### 技术栈

- **模型**：Nano Banana Pro（Gemini 图像生成模型）
- **API 网关**：Ofox（无需 VPN）或 OpenRouter
- **组装工具**：python-pptx（将每页 JPG 塞进空白 slide）
- **成本**：约 ¥0.1-0.3 / 页

### 生成脚本



安装后运行：

    # 1. 复制 slides.example.json 为 slides.json，填入你的 prompt
    cp scripts/slides.example.json scripts/slides.json

    # 2. 生成全部页
    python3 scripts/generate_deck.py

    # 3. 只生成第 1-5 页
    python3 scripts/generate_deck.py --start 1 --end 5

    # 4. 重跑某页（删旧图再跑）
    rm scripts/output/slide_03.jpg && python3 scripts/generate_deck.py --start 3 --end 3

    # 5. 生成完自动组装 PPTX
    python3 scripts/generate_deck.py --assemble

slides.json 格式：style（全局风格前缀）+ slides 数组（每页一个 num + prompt）。
见 `scripts/slides.example.json` 示例。

依赖：`pip install python-pptx`（仅组装 PPTX 时需要）

### 全局风格 Prompt

每页 prompt = 全局风格前缀 + 页面具体内容。

全局前缀应包含：角色设定（"你是一名顶级 PPT 设计师"）、输出格式（"16:9 比例的幻灯片图片"）、设计风格要求（从 design.md 提取的背景、色彩、字体）、中文渲染强制要求、"只生成一张图片"。

### 每页 Prompt 写作规则

详见 `references/prompt-writing-guide.md`，核心要点：

1. **文案从 content.md 原文复制**——不让 AI "发挥"
2. **颜色用 hex 不用名字**——精确色值，不是"深绿色"
3. **UI mockup 要详细描述**——不说"一个聊天截图"，要描述每个气泡的内容
4. **中文名加 CRITICAL 指令**——AI 生图经常乱码
5. **表格逐行列出**——不说"一个7行表格"
6. **避免 prompt 泄漏**——第一句不要写样式指令，写"这是一张什么页"

### 断点续跑

已生成的页自动跳过（检查文件是否存在且大于 10KB）。要重跑某页时手动删掉该 JPG 再跑。

### 组装

使用 python-pptx 创建 16:9 空白演示文稿，逐页将 JPG 以全屏尺寸添加到空白 slide 上，最后保存为 pptx。

---

## 阶段 6：QA 迭代

**目标**：审查所有页面，只修有问题的页，不动通过的页。

### QA 协议

1. **逐页审**——打开 pptx 或查看每页 JPG
2. **分级**——Critical（内容错误）> Important（版式/渲染）> Minor（微调）
3. **只重跑受影响的页**——`rm slide_NN.jpg` → 修 prompt → 重跑 → 重组装
4. **永远不碰已通过的页**

### 常见问题修复

详见 `references/qa-fix-patterns.md`，涵盖：

- 标题被加了前缀（"Slide N:"）
- Prompt 指令被渲染为可见文字
- 中文名乱码
- 字号标注泄漏到标题
- 时间轴节点数量错误
- 表格或数据缺失
- 风格不一致（页间跳跃）
- 数字被 AI 篡改

### 参考链模式（提升风格一致性）

生成每页时把上一页的 JPG 作为 visual reference 传入 API。减少页间风格跳跃。

首次全量生成可不用（独立出图速度更快），QA 修复特定页时建议启用。

---

## 阶段 7：交付

### 产出物


output/
├── slide_01.jpg ~ slide_NN.jpg
├── deck-v1.pptx
└── deck-v1.pdf (可选)


### 交付前 Checklist

- [ ] 全部页面生成成功（0 失败）
- [ ] QA 修复后的页面已替换并重组装
- [ ] pptx 在 PowerPoint / Keynote 能正常打开
- [ ] 核心论点在每一页都站得住
- [ ] 禁用词零命中
- [ ] 数字全 deck 一致（同一个数字不出现两个版本）
- [ ] 人物/品牌名称全程一致
- [ ] CTA 页的每个行动都能此刻兑现

### 迭代和定制

改 `content.md` 里的内容 → 只重跑受影响的页 → 重组装。

**不需要全量重跑**。改一页成本 ¥0.1-0.3 + 30 秒。

---

## 成本参考

| 项目 | 成本 | 时间 |
|------|------|------|
| 阶段 1-4（Brainstorming → 设计文档）| ¥0（纯思考和写作）| 4-10 小时 |
| 阶段 5（Nano Banana 生图 30 页） | ~¥5 | ~15 分钟 |
| 阶段 6（QA 重跑 5 页）| ~¥1 | ~5 分钟 |
| **总计** | **~¥6** | **5-12 小时** |

大部分时间花在内容和设计上（阶段 1-4）。PPT 生成本身只需 15 分钟 + ¥5。

**内容质量 > 视觉效果**——PPT 的说服力 80% 来自内容，20% 来自视觉。

---

## Key Pitfalls

- **Never paraphrase user content** — use exact text from content.md
- **Never add "Slide N:" prefixes** to titles
- **Never add English subtitles** unless the spec says so
- **Never include meta-notes** (like "Final CTA" or "重点页") in visible content
- **Never use font size notation** like "(36pt)" in visible title text
- **Never fabricate data** — only use numbers from the spec, or mark as `[待补]`
- **Never skip self-review** — at least two rounds before proceeding
- **Never regenerate approved slides** during QA rounds
- **Never let AI "improve" the copy** — it always makes it worse
- **Never promise deliverables that don't exist yet** in CTA pages
