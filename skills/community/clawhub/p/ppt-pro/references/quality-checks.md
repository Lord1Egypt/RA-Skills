# PPT Pro — 质量检查、恢复、产物目录与可移植性

本文件为 [SKILL.md](../SKILL.md) 的渐进披露参考：需求消费审查、style 校验、策划/HTML 自检、`progress.json` 恢复、`ppt-output/` 结构、跨环境使用说明。

---

## Step 1 — 五层递进结构（详表）

每个问题标注下游消费节点，确保零废话：

| 层级 | 问题 | 消费节点 |
|------|------|---------|
| 场景层 | 1. 演示场景（现场/自阅/培训） | Step 3 信息密度 + Step 5a 视觉密度 |
| 场景层 | 2. 核心受众（动态生成画像） | Step 3 每页论点设计 + Step 4 card_type |
| 场景层 | 3. 期望行动（决策/理解/执行/改变认知） | Step 3 叙事弧线终点 + Step 4 结尾策略 |
| 内容层 | 4. 叙事结构（问题->方案/科普/对比/时间线） | Step 3 Part 逻辑 + Step 4 card_type 倾向 |
| 内容层 | 5. 内容侧重（搜索结果动态生成，可多选） | Step 3 页数权重 + Step 2 搜索维度 |
| 内容层 | 6. 说服力要素（数据/案例/权威/方法，可多选） | Step 4 card_type 分布 + Step 2 搜索重心 |
| 视觉层 | 7. **视觉风格**（展示完整 8 种预置风格列表 + AI 自动匹配 + 自定义） | Step 5a style.json + Step 4 decoration_hints |
| 执行层 | 8. 信息密度与页数 | 复杂度分级 + Step 4 visual_weight |
| 执行层 | 9. 品牌与身份信息 | Step 4 封面/结尾页内容 + Step 5a 品牌色覆盖 |
| 执行层 | 10. 内容边界（必含/必避） | Step 2 搜索过滤 + Step 4 内容硬约束 |
| 执行层 | 11. 语言偏好 | Step 5a font_family + Step 5c 排版 |
| 执行层 | 12. AI 配图偏好 | Step 4 image 字段 + Step 5b 执行 |
| 动态层 | 13-15. 主题专属追问（0-3 题，基于搜索结果动态生成） | Step 2-4 内容方向聚焦 |

> **Q7 风格选择的特殊要求**：必须以表格形式展示全部 8 种预置风格（蓝白商务/极简灰白/清新自然/暖色大地/朱红宫墙/暗黑科技/紫金奢华/活力彩虹），每种附一句话灵魂描述和适合场景。用户选编号即可，不需要自己描述「什么风格」。
>
> **轻量模式**（用户明确说了页数 <= 8 或暗示简短）：Q1 + Q2 + Q7 + Q8 + Q12（5 题精简版，跳过内容层和部分执行层，由 AI 根据搜索结果自行决策）。
>
> **动态追问**：仅在搜索结果揭示了主题特有的关键分歧（如技术路线分歧、阶段差异、视角选择）时才添加，不凑数。每个动态问题必须标注消费节点。

---

## Step 1 — 消费审查矩阵

Step 1 完成后 LLM 必须对照此表自检，确认每个字段都有下游消费方：

| 需求字段 | 下游 prompt 占位符 | 消费步骤 | 如果未消费会怎样 |
|---------|-------------------|---------|----------------|
| `scene` | `{{SCENE}}` (prompt-2) | Step 3 信息密度策略 | 自阅型 PPT 被做成演讲型，信息不完整 |
| `audience` | `{{AUDIENCE}}` (prompt-2, prompt-3) | Step 3 论点设计 + Step 4 card_type | 专业深度失控 |
| `purpose` | `{{PURPOSE}}` (prompt-2) | Step 3 叙事弧线终点 | 结尾没有 CTA |
| `narrative_structure` | `{{NARRATIVE_STRUCTURE}}` (prompt-2) | Step 3 Part 逻辑 | 大纲缺乏骨架 |
| `emphasis` | `{{EMPHASIS}}` (prompt-2) | Step 3 页数权重 | 重点被平均化 |
| `persuasion_style` | `{{PERSUASION_STYLE}}` (prompt-2) | Step 4 card_type 分布 | data/quote 比例失调 |
| `style_choice` | 资源加载决策树 | Step 5a 风格决策 | 用户选了暗黑科技结果生成蓝白商务 |
| `page_count` + `info_density` | `{{PAGE_REQUIREMENTS}}` (prompt-2) | Step 3 页数 + Step 4 密度 | 页数偏离 |
| `brand_info` | `{{BRAND_INFO}}` (prompt-2, prompt-3) | Step 4 封面/结尾内容 | 封面缺演讲人/公司名 |
| `content_must_include` | `{{CONTENT_CONSTRAINTS}}` (prompt-2) | Step 2 搜索 + Step 4 内容 | 必含内容遗漏 |
| `content_must_avoid` | `{{CONTENT_CONSTRAINTS}}` (prompt-2) | Step 2 搜索过滤 | 触及敏感内容 |
| `language` | 资源加载决策树 | Step 5a 字体栈 | 英文 PPT 用中文字体 |
| `image_preference` | 资源加载决策树 | Step 4-5b 配图 | 不需要配图但生成了 |

> **审查规则**：Step 1 结束整理需求 JSON 后，逐行对照此矩阵。任何字段为空（且用户确实回答了对应问题），必须补全后才能进入 Step 2。

---

## Step 5a — style.json 产物校验（缺一不可）

> **风格不是「选个调色板」，而是为这个特定项目调配独一无二的视觉灵魂。** `style.json` 影响全局每一页的视觉基调，生成质量绝不能马虎。

- `mood_keywords`：3-5 个情绪关键词（不是色彩词）
- `design_soul`：一句话灵魂宣言（有画面感、有通感）
- `variation_strategy`：跨页变奏策略（描述节奏型，不是「每页用不同装饰」这种废话）
- `decoration_dna`：标志手法 / 禁止手法 / 推荐组合
- `css_variables`：完整的 CSS 变量集（必须覆盖全部 12 个变量）
- `font_family`：字体栈

完整结构见 `references/styles/README.md` 的数据模型定义。

---

## Step 5c — 每页 HTML 生成后 5 项自检（写入文件前对照）

每页 HTML 生成后、写入文件前，快速过一遍以下 5 项。如有不通过项，立即修正后再写入：

| # | 检查项 | 判定标准 | 不通过时的修正动作 |
|---|--------|---------|------------------|
| 1 | **内容完整** | 每张卡片有标题 + 正文/数据/列表（无空卡）；data 卡片有可视化元素 | 补充缺失内容，空卡填满 |
| 2 | **布局无重叠** | 所有卡片通过 CSS Grid 自动排列或明确 grid-row/grid-column 定位；跨行/跨列卡片的 span 属性与布局文件一致 | 对照所选布局的 HTML 骨架修正 grid 定位 |
| 3 | **不溢出画布** | 内容区 `overflow:hidden`；每张卡片 `overflow:hidden`；图表容器有明确 `height`；正文有 `-webkit-line-clamp` 截断 | 缩减内容（缩短正文 > 减少列表项 > 移除装饰） |
| 4 | **色彩规范** | 所有颜色通过 `var(--xxx)` 引用（除 transparent 和 rgba(255,255,255,0.x)）；accent 色不超过同页 2 种 | 替换硬编码颜色为 CSS 变量 |
| 5 | **资源已消费** | `prompt-ready-{n}.txt` 中 [RESOURCES] 块的资源已在 HTML 中体现：布局来自 LAYOUT 分区的骨架；每个卡片的复合组件/图表符合 CARD_RESOURCES 分区中该卡片 [block]/[chart] 的设计要点和模板；PAGE_PRINCIPLES 和卡片级 [principle] 在设计决策中被考虑 | 回读 `prompt-ready-{n}.txt` 的 [RESOURCES] 部分对照修正 |

> 自检不是事后审查，而是生成流程的一部分。把 5 项检查融入「生成 -> 检查 -> 修正 -> 写入」的循环中。

### HTML 自检中断点 [STOP -- 等待用户确认]

> **所有页面 HTML 生成完毕后，暂停等用户自检。** 出错概率低，因此统一自检而非逐页中断。

所有 `slide-XX.html` 写入完成后：

1. 运行 `html_packager.py` 生成 `preview.html`（合并预览，方便用户一次性审阅）
2. **通知用户**：告知用户打开 `preview.html` 翻页审阅所有页面
3. **等待用户反馈**（阻断点），用户可以：
   - **A) 直接确认**：回复「OK」或「没问题」，进入 Step 6
   - **B) 自行编辑 HTML**：直接修改 `slides/slide-XX.html` 文件，改完后回复确认
   - **C) 指示 agent 修改**：告诉 agent 哪些页面需要改什么（如「第 3 页标题颜色太淡」、「第 7 页布局太空」），agent 修改后重新生成 `preview.html` 供再次审阅
4. 确认通过后，进入 Step 6

> 如果用户选择 C，agent 修改 HTML 后必须重新运行 `html_packager.py` 更新预览，然后再次等用户确认。循环直到用户满意。

---

## 质量自检（全局级 — 与 Step 5c 逐页自检互补）

| 维度 | 检查项 |
|------|-------|
| 全局一致 | CSS 变量跨页一致 / 配色统一 / 配图风格统一 |
| 叙事节奏 | 相邻页 visual_weight 差 <= 5 / 不连续 3 页高密度 / 规则冲突时内容完整性 > 节奏美感 |

---

## 中断恢复机制

> 长流程（15+ 页 PPT）中途中断时，通过 `progress.json` 记录进度，下次从中断点继续。

### progress.json 结构

```json
{
  "version": "1.0",
  "topic": "PPT 主题",
  "complexity": "light | standard | large",
  "total_pages": 15,
  "started_at": "ISO 时间戳",
  "last_updated": "ISO 时间戳",
  "steps": {
    "step_1": {"status": "done | in_progress | pending"},
    "step_2": {"status": "done"},
    "step_3": {"status": "done"},
    "step_4": {"status": "in_progress", "completed_pages": [1,2,3,4,5], "current_page": 6},
    "step_5a": {"status": "pending"},
    "step_5b": {"status": "pending", "completed_pages": []},
    "step_5c": {"status": "pending", "completed_pages": []},
    "step_6": {"status": "pending", "pipeline": null}
  }
}
```

### 写入时机

| 事件 | 更新内容 |
|------|--------|
| Step 1 完成 | 创建 `progress.json`，写入 topic + complexity + step_1=done |
| Step 2 完成 | step_2=done |
| Step 3 完成 | step_3=done, total_pages |
| Step 4 每页写入 | step_4.completed_pages 追加页码 |
| Step 5a 完成 | step_5a=done |
| Step 5b/5c 每页完成 | 对应 completed_pages 追加页码 |
| Step 6a 用户选择管线 | step_6.pipeline = "png" 或 "editable" |
| Step 6 完成 | step_6=done |

### 恢复流程

流程开始时检查 `OUTPUT_DIR/progress.json` 是否存在：

1. 不存在 -> 全新开始
2. 存在 -> 读取并展示当前进度，询问用户「继续」或「重新开始」
3. 用户选择继续 -> 跳到第一个非 done 的步骤，补全缺失产物
4. 用户选择重新开始 -> 删除 progress.json，全新开始

**恢复时的产物校验**：跳到中断步骤前，检查前序步骤的产物文件是否存在（如 outline.json、planning/*.json、style.json）。缺失则回退到该步骤重新生成。

---

## 输出目录结构

```
ppt-output/
  progress.json        # 进度日志（中断恢复用）
  outline.json         # 大纲（Step 3 产物）
  style.json           # 风格定义（Step 5a 产物）
  planning/            # 策划稿目录（Step 4 产物）
    planning1.json     # 第 1 页策划稿
    planning2.json     # 第 2 页策划稿
    planning{n}.json   # 第 n 页策划稿（每页独立文件）
  images/              # AI 配图（Step 5b 产物）
  prompts-ready/       # ★ 完整 prompt（Step 5c GATE CHECK 产物 -- 必须在写 HTML 之前生成）
    prompt-ready-1.txt # prompt_assembler.py 组装：模板+风格+策划+资源+配图，开箱即用
    prompt-ready-{n}.txt
  slides/              # 每页 HTML（Step 5c 产物 -- 必须基于 prompts-ready 生成）
  preview.html         # 可翻页预览（html_packager.py 合并打包）
  png/                 # PNG 截图（Step 6 PNG 管线产物）
  presentation.pptx    # 最终 PPTX（Step 6 产物 -- PNG 管线嵌入图片 / 可编辑管线原生形状）
```

> **依赖关系**：`planning/` → `prompts-ready/` → `slides/`。每个目录都依赖前一个目录的产物，**禁止跳过中间产物**。

---

## 可移植性 & 首次使用

### 跨环境复制

本 Skill 是自包含的目录，可直接复制到任何支持 Cursor Agent / OpenClaw / 其他 LLM Agent 的环境中使用：

```
ppt-pro/
├── SKILL.md            # Skill 入口（Agent 读取此文件触发）
├── scripts/            # 自动化脚本（Python + Bash）
│   ├── setup.sh        # 环境自检 + 依赖安装
│   ├── prompt_assembler.py
│   ├── resource_assembler.py
│   ├── planning_validator.py
│   ├── html_packager.py
│   ├── html2png.py     # 双后端：Playwright / Puppeteer
│   ├── png2pptx.py
│   ├── html2pptx.js       # 可编辑管线入口（调度下面两个脚本）
│   ├── extract_slides.js  # Phase 1: Puppeteer 截图 + 文本提取
│   ├── assemble_pptx.py   # Phase 2: python-pptx PPTX 组装
│   └── package.json       # Node.js 依赖声明
└── references/         # 设计资源 markdown
    ├── prompts/        # 各阶段 LLM prompt 模板
    ├── styles/         # 8 套预置风格 + 灵动创作方法论
    ├── layouts/        # 10 种布局骨架 + 决策矩阵
    ├── blocks/         # 8 种复合组件 + card_style 体系
    ├── charts/         # 13 种图表模板
    ├── principles/     # 6 大设计原则 + cheatsheet
    ├── page-templates/ # 4 种特殊页面结构
    ├── technique-cards.md
    ├── narrative-rhythm.md
    ├── resource-menu.md
    ├── resource-registry.md
    ├── execution-rules.md
    └── quality-checks.md
```

### 首次使用

1. 运行环境自检：`bash SKILL_DIR/scripts/setup.sh`
2. 如需 PNG 管线（HTML -> 图片 PPTX），确保至少一种截图后端可用：
   - **推荐**：`pip install playwright && playwright install chromium`
   - **备选**：安装 Node.js + `npm install puppeteer`
3. 如需可编辑管线（HTML -> 原生形状 PPTX），安装 Node.js 18+ 并初始化依赖：
   - `cd SKILL_DIR/scripts && npm install`
4. 安装 PPTX 库：`pip install python-pptx Pillow lxml`

### 环境要求

| 组件 | 必需？ | 用途 |
|------|--------|------|
| Python 3.8+ | 是 | 脚本执行 |
| python-pptx | 是（PNG 管线 + 可编辑管线合并） | PPTX 生成与合并 |
| Playwright + Chromium | 推荐（PNG 管线） | HTML 截图，无需 Node.js |
| Node.js 18+ + Puppeteer | 推荐（可编辑管线） / 备选（PNG 管线） | 可编辑管线 headless 浏览器 + HTML 截图备选 |

---

## Step 6c — 通知用户（产物说明要点）

告知产物位置和使用方式（可与 SKILL 主流程 Step 6c 配合使用）：

- `preview.html` -- 浏览器打开即可翻页预览（Step 5c 自检阶段已生成）
- `presentation.pptx` -- 最终 PPTX 文件
- **PNG 管线产物**：
  - `png/` -- 每页截图，可直接插入任何演示软件
  - 文字为像素，不可在 PPT 中直接编辑
- **可编辑管线产物**：
  - `presentation.pptx` -- 截图背景 + 原生文本框叠加，纯文本在 PowerPoint 中可直接编辑
  - 渐变文字、文字阴影（text-shadow）、文字描边（-webkit-text-stroke）等高级 CSS 效果自动映射为原生 OOXML 效果（a:gradFill、a:outerShdw、a:ln），在 PowerPoint 中完全可编辑
  - python-pptx 生成标准 OOXML，PowerPoint 打开时无修复提示
- **如果转换被降级跳过**，说明原因并告知用户手动安装 Node.js 后可重新运行
