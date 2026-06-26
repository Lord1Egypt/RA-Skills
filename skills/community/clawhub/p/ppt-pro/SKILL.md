---
name: ppt-pro
description: >-
  专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流
  （需求调研 -> 资料搜集 -> 大纲策划 -> 策划稿 -> 设计稿），输出高质量 HTML
  格式演示文稿并可转换为可编辑 PPTX。当用户提到制作 PPT、做演示文稿、做 slides、
  做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发。也适用于
  "帮我把这篇文档做成 PPT"等需要将内容转化为演示格式的场景。
metadata:
  author: ppt-pro-team
  version: "9.7.0"
  tags: pptx, presentation, slides, html
compatibility: Requires python3 and node. Linux/macOS/Windows.
---

# PPT Pro -- 专业演示文稿全流程生成

## PPTX 可编辑管线技术规则

完整技术约束详见 [pptx-pipeline.md](references/pptx-pipeline.md)。核心原则：

1. **背景仅承担装饰**：用户可能调整的元素必须作为独立 PPTX shape/picture
2. **data-pptx-role 驱动分层**：`content` / `content-icon` / `decoration` / `watermark` 四角色
3. **z-order**：shapes → icons → text boxes
4. **原生控件优先**：表格/图表优先用 python-pptx 原生 API，禁止手动 XML 注入

---

## 核心理念

模仿专业 PPT 设计公司（报价万元/页级别）的完整工作流，而非「给个大纲套模板」：

1. **先调研后生成** -- 用真实数据填充内容，不凭空杜撰
2. **策划与设计分离** -- 先验证信息结构，再做视觉包装
3. **内容驱动版式** -- Bento Grid 卡片式布局，每页由内容决定版式
4. **全局风格一致** -- 先定风格再逐页生成，保证跨页统一
5. **智能配图** -- 利用图片生成能力为每页配插图（绝大多数环境都有此能力）

---

## 环境感知

开始工作前自省 agent 拥有的工具能力：

| 能力 | 降级策略 |
|------|---------|
| **信息获取**（搜索/URL/文档/知识库） | 全部缺失 -> 依赖用户提供材料 |
| **图片生成**（绝大多数环境都有） | 缺失 -> 纯 CSS 装饰替代 |
| **文件输出** | 必须有 |
| **脚本执行**（Python/Node.js） | 缺失 -> 跳过自动打包和可编辑管线转换 |
| **Sub-agent / 并行代理**（Agent tool / subagent） | 可用 -> Step 4 策划和 Step 5c HTML 生成启用并行模式；缺失 -> 退回逐页串行 |

**原则**：检查实际可调用的工具列表，有什么用什么。检测 sub-agent 能力时，确认是否有 `Agent` 工具（或等价的 subagent 调用能力）。若有，在 `progress.json` 中标记 `"has_subagent": true`，后续 Step 4 和 Step 5c 自动启用并行模式。

---

## 路径约定

| 变量 | 含义 | 获取方式 |
|------|------|---------|
| `SKILL_DIR` | 本 SKILL.md 所在目录的绝对路径 | 即触发 Skill 时读取 SKILL.md 的目录 |
| `OUTPUT_DIR` | 产物输出根目录 | 用户当前工作目录下的 `ppt-output/`（首次使用时 `mkdir -p` 创建） |

后续所有路径均基于这两个变量，不再重复说明。

---

## 输入模式与复杂度判断

### 入口判断

| 入口 | 示例 | 从哪步开始 |
|------|------|-----------|
| 纯主题 | "做一个 Dify 企业介绍 PPT" | Step 1 完整流程 |
| 主题 + 需求 | "15 页 AI 安全 PPT，暗黑风" | Step 1（跳部分已知问题）|
| 源材料 | "把这篇报告做成 PPT" | Step 1（材料为主）|
| 已有大纲 | "我有大纲了，生成设计稿" | Step 4 或 5 |

### 跳步规则

| 起始步骤 | 缺失依赖 | 补全方式 |
|---------|---------|---------|
| Step 4 | 每页内容文本 | 先用 Prompt #3 为每页生成内容分配 |
| Step 5 | 策划稿 JSON | 用户提供或先执行 Step 4 |

### 复杂度自适应

| 规模 | 页数 | 调研 | 搜索 | 策划 | 生成 |
|------|------|------|------|------|------|
| **轻量** | <= 8 页 | 5 题精简版（Q1+Q2+Q7+Q8+Q12） | 3-5 个查询 | 整体生成（Step 3 可与 Step 4 合并） | 逐页生成 |
| **标准** | 9-18 页 | 完整 12 题 + 动态追问 | 8-12 个查询 | 逐页生成 | 逐页生成 |
| **大型** | > 18 页 | 完整 12 题 + 动态追问 | 10-15 个查询 | 逐页生成 | 逐页生成 |

**复杂度判断时机**：(1) **预判**（Step 1 前）：据用户描述估算；明确页数或暗示简短则预判轻量并精简提问。(2) **确认**（Step 1 后）：据 Q8 写入 `progress.json` 的 `complexity_level`（light / standard / large）。(3) **传递**：后续步骤从 `progress.json` 读取并调整搜索数、策划深度等。

---

## 6 步 Pipeline

### Step 1: 需求调研 [STOP -- 必须等用户回复]

> **禁止跳过。** 无论主题多简单，都必须提问并等用户回复后才能继续。不替用户做决定。

**执行**：`references/prompts/prompt-1-research.md`。有搜索则搜主题背景（3-5 条）并据此生成 Q2/Q5/动态追问选项；无搜索则用通用选项并跳过第五层动态追问。一次性发出 12 基础题 + 0-3 动态题，**等待用户回复**，再整理为需求 JSON。整理后须对照 [quality-checks.md](references/quality-checks.md) 中的**消费审查矩阵**自检；**五层问题详表、Q7/轻量/动态追问全文**亦在同文件。

**问题层级（简表）**：场景层 Q1-3 → 内容层 Q4-6 → 视觉层 Q7（**须表格展示 8 种预置风格**：蓝白商务/极简灰白/清新自然/暖色大地/朱红宫墙/暗黑科技/紫金奢华/活力彩虹，各附一句灵魂描述；用户选编号）→ 执行层 Q8-12 → 动态层 0-3 题（仅当搜索揭示主题关键分歧时追加，须标注消费节点）。

**轻量模式**（页数 <= 8 或暗示简短）：仅 Q1+Q2+Q7+Q8+Q12。**动态追问**：不凑数。

**产物**：需求 JSON（字段须完整）：

```json
{
  "topic": "PPT 主题",
  "scene": "Q1 演示场景（现场演讲/自阅文档/培训教学/其他）",
  "audience": "Q2 核心受众画像",
  "purpose": "Q3 期望观众做什么",
  "narrative_structure": "Q4 叙事结构",
  "emphasis": ["Q5 内容侧重（可多选）"],
  "persuasion_style": ["Q6 说服力要素（可多选）"],
  "style_choice": "Q7 风格选择（A-J）",
  "style_detail": "Q7 附加信息（如选 J 时的自定义描述）",
  "page_count": "Q8 页数（数字或 null=AI 决定）",
  "info_density": "Q8 信息密度偏好（少而精/适中/信息量大）",
  "brand_info": {
    "presenter": "Q9 演讲人",
    "date": "Q9 日期",
    "company": "Q9 公司名",
    "brand_color": "Q9 品牌色（如有，覆盖 style_choice）",
    "logo_path": "Q9 Logo 路径"
  },
  "content_must_include": ["Q10 必须包含"],
  "content_must_avoid": ["Q10 必须回避"],
  "language": "Q11 语言偏好（中文/英文/中英混排/其他）",
  "image_preference": "Q12 配图偏好（A-D）",
  "dynamic_answers": {"问题文本": "用户回答"},
  "complexity_level": "light | standard | large（根据 page_count 判定）"
}
```

---

### Step 2: 资料搜集

> 盘点所有信息获取能力，全部用上。

**2a. 查询规划** — 按复杂度表控制查询数；维度与 JSON 整理模板见 [execution-rules.md](references/execution-rules.md)（Step 2 两节）。

**2b. 并行搜索** — 搜索引擎、URL、文档、知识库等凡可用尽用。

**2c. 结果整理** — 每组输出结构化 JSON（`query` + `findings[]`：`fact` / `data` / `source` / `reliability` high|medium|low / `relevance`）。仅 high/medium 可进策划 `data_highlights`；low 仅作参考。

**产物**：搜索结果集合 JSON。

---

### Step 3: 大纲策划

**执行**：`references/prompts/prompt-2-outline.md`。方法论与 5 步思考过程全文见 [execution-rules.md](references/execution-rules.md)「Step 3」；prompt 内亦内置自动执行。

**自检**：页数合规；每 Part >= 2 页；Part 间逻辑递进；要点有搜索支撑（缺则 `found_in_search: false`）；`design_rationale` 与 `transition_from_previous` 完整。

**产物**：`[PPT_OUTLINE]` JSON（含 `design_rationale`）。

---

### Step 4: 内容分配 + 策划稿 [STOP -- 完成后必须等用户确认]

> 内容分配与策划稿合并为一步；策划稿须为 AI 逐页思考的创作产物。**核心：一页一 `planning{n}.json`，对应一页 HTML。**
> **⛔ 未经用户确认，禁止跳进 Step 5。**

#### 4a. 资源菜单预读（首页策划前一次）

策划第一页前按序读取（每项以 README 或指定章节为主，勿通读全书）：

| 优先级 | 路径 | 用途 |
|--------|------|------|
| **0** | `principles/design-principles-cheatsheet.md` | JSON 字段操作 + 逐页 8 项体检（**必读第一项**） |
| 1 | `layouts/README.md` | `layout_hint` |
| 1b | `layout-patterns.md` | 12 种布局模式、4 层结构、通用组件 |
| 2 | `blocks/README.md` | `card_type` |
| 3 | `blocks/card-styles.md` | `card_style` |
| 4 | `charts/README.md` | `chart_type` |
| 5 | `principles/README.md` | 原则索引 |
| 6 | `styles/README.md` 的**装饰技法工具箱**章节 | `decoration_hints` |
| 7 | `image-generation.md`（Q12 ≠ A 时） | `image.prompt` / `image.usage` |

预读后从工具箱选型，避免只会 text+data+list。第 7 项仅在需要配图时读。

#### 4b. 逐页策划

**执行**：`references/prompts/prompt-3-planning.md`。

**占位符**：`{{DESIGN_PRINCIPLES_CHEATSHEET}}`、`{{RESOURCE_MENU}}` 分别注入 cheatsheet 与 `resource-menu.md` 全文；其余从需求 JSON 填入（`{{SCENE}}` 等）。

**设计感约束（须遵守）**：拒绝千篇一律网页风；页与页版式须有反差与非对称；`director_command` 须给出具体、可执行的视觉与排版指令。

**要点**：逐页按 cheatsheet 尾部 8 项体检；映射搜索素材；主内容 40-100 字 + 数据亮点 + 辅助要点；`layout_hint` / `card_type` / `chart_type` 来自预读菜单；叙事节奏见 `references/narrative-rhythm.md`；每页 `visual_weight`、`required_resources`、`image`（总页数 >= 8 时全稿至少各用 1 次 `split-content` 与 `card-inset`）。

#### 串并行、验证与操作边界

据 `has_subagent` 与复杂度选择串行或按 Part 并行；**验证是写入流程的一部分**（每页 `planning_validator.py` 单页验证，ERROR 必改）。4a 补充说明、4b 持久上下文与设计感约束、全量验证、Sub-agent 模板、操作边界 6 条、上下文传递 — 详见 [execution-rules.md](references/execution-rules.md)。

**⛔ [GATE] 所有页完成后，必须执行且必须 PASS 才能继续**：

```bash
# Step 1: 运行门禁脚本（内部调用 planning_validator.py）
bash SKILL_DIR/scripts/pipeline_gate.sh check-planning OUTPUT_DIR SKILL_DIR

# Step 2: 若有 ERROR，修正 planning JSON 后重跑，直到 PASS
# Step 3: PASS 后向用户展示策划概览，等待确认
```

`planning_validator.py` 返回 exit 1（FAILED）时 → **禁止继续，必须修正全部 ERROR**。ERROR 修复参考各条错误提示中的「期望格式」说明。

修正跨页问题 → 向用户展示概览 → **[STOP -- 等待用户确认]**（可编辑 `planning/planning{n}.json` 后回复再继续）。

**产物**：`OUTPUT_DIR/planning/planning{n}.json`。

---

### Step 5: 风格决策 + 设计稿生成

顺序：**5a → 5b（可选）→ 5c**。

#### 5a. 风格决策

**执行**：`references/styles/README.md` 的**灵动创作方法论（四步法）**：情绪关键词 → 从情绪推导色彩 → 灵魂宣言 → 变奏策略；并读对应 `styles/{id}.md`。`style.json` 须含灵魂层、装饰基因、`css_variables`（12 项）、`font_family` — **校验清单**见 [quality-checks.md](references/quality-checks.md)。调色板路径见 `resource-registry.md` 第 1 节。

**产物**：`OUTPUT_DIR/style.json`。

#### 5b. 配图生成（可选）

读取每页 `planning{n}.json` 的 `image`；`usage` = `none` 则跳过；否则 `generate_image` 用 `image.prompt`，保存 `OUTPUT_DIR/images/`。**须在生成该页 HTML 之前**完成该页配图。

#### 5c. 逐页 HTML

一对一：`planning{n}.json` → `slides/slide-{NN}.html`。

**⛔ GATE CHECK（任何一步 BLOCKED 则禁止写 HTML）**：

```bash
# [1] 确认 planning 通过门禁
bash SKILL_DIR/scripts/pipeline_gate.sh check-planning OUTPUT_DIR SKILL_DIR

# [2] 组装 prompt-ready 文件（全量批次）
python3 SKILL_DIR/scripts/prompt_assembler.py \
  OUTPUT_DIR/planning/ --refs SKILL_DIR/references \
  --style OUTPUT_DIR/style.json -o OUTPUT_DIR/prompts-ready/

# [3] 确认 prompts-ready 与 planning 数量一致
bash SKILL_DIR/scripts/pipeline_gate.sh check-prompts OUTPUT_DIR

# [4] 读全局资源（仅一次）
# view_file SKILL_DIR/references/styles/README.md
# view_file SKILL_DIR/references/principles/README.md
# view_file SKILL_DIR/references/blocks/README.md
# view_file SKILL_DIR/references/layout-patterns.md
```

每页：**先** `view_file OUTPUT_DIR/prompts-ready/prompt-ready-{n}.txt`，**再**据完整 prompt 生成 HTML；禁止跳过 prompt-ready。三层资源决策、`prompt_assembler` 占位符说明、批量/单页命令、并行 HTML Sub-agent、核心设计约束与逐页 ASSERT 流程 — 详见 [execution-rules.md](references/execution-rules.md)。

**逐页自检**：写入前执行 [quality-checks.md](references/quality-checks.md) 中的 **5 项自检**。

**跨页叙事**：遵循 `references/narrative-rhythm.md`。

**HTML 完成后**：`html_packager.py` 生成 `preview.html` → 请用户审阅 → **[STOP]**（确认或改稿后再 Step 6）。

```bash
python3 SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/preview.html
```

**产物**：`OUTPUT_DIR/slides/*.html`、`preview.html`。

---

### Step 6: 管线选择 + 后处理 [必做]

> 用户确认 HTML 后必须跑转换管线，勿停在 preview。

#### 6a. 管线选择 [STOP]

| 管线 | 路径 | 优势 | 劣势 |
|------|------|------|------|
| **A) PNG** | HTML → PNG → PPTX | 兼容极好；CSS 全保留 | 字不可编辑 |
| **B) 可编辑** | HTML → Puppeteer + python-pptx | 字可编辑；CSS 高级效果映射 OOXML | 需 Node 18+ 与 python-pptx |

等用户选 A 或 B。

#### 6b. 执行转换

```bash
bash SKILL_DIR/scripts/setup.sh
pip install python-pptx lxml Pillow 2>/dev/null
```

**管线 A**：`html2png.py` → `png2pptx.py`（脚本自动选 Playwright / Puppeteer）。

```bash
python3 SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/png/ --scale 2
python3 SKILL_DIR/scripts/png2pptx.py OUTPUT_DIR/png/ -o OUTPUT_DIR/presentation.pptx
```

**管线 B**：`cd SKILL_DIR/scripts && npm install`（首次）；`node html2pptx.js ...`

```bash
cd SKILL_DIR/scripts && npm install
pip install python-pptx lxml
node SKILL_DIR/scripts/html2pptx.js OUTPUT_DIR/slides/ -o OUTPUT_DIR/presentation.pptx
```

#### 6c. 通知用户

说明 `preview.html`、`presentation.pptx`、`png/`（若用 A）及可编辑管线编辑能力；降级时说明原因与补装依赖。

---

## 执行规则（扩展）

策划与 HTML 阶段的串并行流程、Sub-agent 提示词模板、操作边界、Step 5c 资源决策树、`prompt_assembler` 与禁止行为等 — 详见 [execution-rules.md](references/execution-rules.md)。

---

## 质量检查、恢复与产物目录

需求消费审查矩阵、style.json 校验、HTML 5 项自检、全局质量表、`progress.json` 恢复流程、`ppt-output/` 目录树、可移植性与首次使用 — 详见 [quality-checks.md](references/quality-checks.md)。

---

## Reference 文件索引

> 完整映射见 `resource-registry.md`。

| 文件 | 何时读 | 内容 |
|------|-------|------|
| **`execution-rules.md`** | Step 4-5c 按需 | 串并行、Sub-agent 模板、资源决策树、prompt 组装、HTML 并行与约束 |
| **`quality-checks.md`** | Step 1/5a/5c/恢复/部署 | 消费审查、style 校验、自检表、progress.json、目录结构、可移植性 |
| `prompts/prompt-1-research.md` | Step 1 | 需求调研 |
| `prompts/prompt-2-outline.md` | Step 3 | 大纲架构 v3.0 |
| `prompts/prompt-3-planning.md` | Step 4 | 策划稿 |
| `prompts/prompt-4-design.md` | prompt_assembler 内部 | 设计模板（勿手动读） |
| `blocks/README.md` | Step 4 首页前 | 复合组件 |
| `blocks/{type}.md` | Step 4 + 5c 按需 | 8 种复合组件 |
| `principles/README.md` | Step 4 首页前 | 6 大原则索引 |
| `principles/{name}.md` | 按需 | 各原则正文 |
| `principles/design-principles-cheatsheet.md` | Step 4 首页前（第 0 项） | JSON 字段手册 + 体检单 |
| `resource-menu.md` | 经 `{{RESOURCE_MENU}}` 注入 prompt-3 | 资源速查 |
| `styles/README.md` | Step 5a + 5c 首页前 | 色彩 + 装饰工具箱 |
| `styles/{id}.md` | Step 5a | 8 套调色板 |
| `layouts/README.md` | 策划 / 5c | 布局总则 |
| **`layout-patterns.md`** | **5c GATE #2** | 布局模式 + 4 层结构 + 组件 |
| `layouts/{layout}.md` | resource 组装 | 骨架 |
| `charts/{type}.md` | resource 组装 | 图表模板 |
| `page-templates/{type}.md` | resource 组装 | 页面结构建议 |
| `narrative-rhythm.md` | Step 3 后 | 节奏与色彩递进 |
| `technique-cards.md` | prompt_assembler | T1-T10 技法牌 |
| `resource-registry.md` | 维护 | 全局映射 |
| `pptx-pipeline.md` | 可编辑管线 | PPTX 技术规则 |
| `scripts/prompt_assembler.py` | Step 5c GATE | 组装 prompt-ready |
| `scripts/resource_assembler.py` | 内部 | [RESOURCES] 块 |
| `scripts/planning_validator.py` | Step 4 | 策划校验 |
| `scripts/setup.sh` | 首次 / 自检 | 环境 |
| `scripts/html2png.py` | Step 6 A | 截图 |
| `scripts/png2pptx.py` | Step 6 A | PNG → PPTX |
| `scripts/html2pptx.js` | Step 6 B | 可编辑管线入口 |
| `scripts/extract_slides.js` | Step 6 B | Phase 1 |
| `scripts/assemble_pptx.py` | Step 6 B | Phase 2 |
| `scripts/package.json` | Step 6 B | Node 依赖 |
| `scripts/html_packager.py` | Step 5c | preview.html |
