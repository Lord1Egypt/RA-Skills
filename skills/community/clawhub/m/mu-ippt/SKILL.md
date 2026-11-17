---
name: mu-ippt
version: 1.1.0
description: "PPT生成与编辑，覆盖四大场景（从零生成/技术图表/咨询模板/编辑已有）。触发词：做PPT、画架构图、改PPT、咨询PPT、汇报PPT。不适用：纯图片生成"
visibility: public
---

**IRON LAW：⛔ BLOCKING 步骤不可跳过不可合并；所有生成的 PPTX 必须经 visual_verify.py 验证通过后才能交付用户；一个演示文稿只用一个图标库、一套配色方案，禁止混用；多页完整PPT需求必须先经工作流 0 路由诊断再执行；混合方案（A+C）合并后必须运行 color_unify 后处理，将工作流C的默认色替换为用户选定的设计哲学色板，禁止以原始默认配色交付。无例外。**

> **路径初始化**：本文件中所有 `${SKILL_DIR}` 均指 Skill 根目录。使用前须先执行：
> ```bash
> SKILL_DIR=<AGENT_HOME>/skills/mu-ippt
> ```

---

# mu-ippt · PPT Skill（外网版）

> 一个 Skill 搞定所有 PPT 场景：**从零生成** · **技术图表** · **咨询汇报模板** · **编辑已有PPT**
>
> 🎨 **26 套配色**（12 设计风格 + 14 行业配色）· 📊 **119 种图表** · 📐 **20 套布局模板** · 🖼️ **6,732 图标** · 📏 **8 种画布**（演示 / 社交 / 印刷等场景全覆盖）
## 🚀 首次使用

本 Skill 的 AI 配图功能需要配置图片生成 API Key（二选一）：

| 后端 | 环境变量 | 说明 |
|------|---------|------|
| **OpenAI（默认）** |  | DALL-E 3 图片生成 |
| **Gemini（备选）** |  | Google Imagen 图片生成 |

配置方式：


> 💡 如果不需要 AI 配图功能（仅使用 SVG 图表和图标），无需配置 API Key。


## 五大工作流

| 场景 | 触发词 | 走哪个流程 |
|------|--------|-----------|
| **多页完整PPT（自动路由）** | 做PPT、做汇报、生成演示文稿、把这个文档变成PPT | → [工作流 0](#工作流-0多页需求路由诊断) |
| **从零生成多页 PPT** | （工作流0路由后）SVG自由排版、高度定制化风格 | → [工作流 A](#工作流-a从零生成多页-ppt) |
| **生成单张技术图表** | 画架构图、画流程图、画UML、画时序图、技术图表PPT | → [工作流 B](#工作流-b生成单张技术图表) |
| **咨询汇报模板** | 咨询汇报模板、咨询PPT、专业模板、KPI仪表盘、甘特图模板、议题树、漏斗图 | → [工作流 C](#工作流-c咨询汇报模板) |
| **编辑已有 PPT** | 改PPT、修改第三页标题、用这个模板做PPT、替换内容 | → [工作流 D](#工作流-d编辑已有-ppt) |

> 💡 **判断规则**：单张技术图表/架构图/UML → 直接B；改现有PPT或套模板 → 直接D；专业咨询风格原生幻灯片（KPI/甘特/组织架构/趋势）→ 直接C；**其他多页完整PPT → 必须先走工作流0路由诊断**。

---

## 工作流 0：多页需求路由诊断

> **触发条件**：用户提出多页完整 PPT 需求（含 2 页以上、且非单张技术图表、非直接编辑已有文件）
> **目标**：在动手之前，帮用户规划每页走哪个工作流，输出「页面规划表」供确认

### Step 1：理解需求

收集以下信息（可一次问完）：
- 主题/用途（汇报/培训/融资/管理复盘等）
- 大概页数
- 受众类型（高管/内部团队/客户/大会等）
- 风格偏好（如有，见下方设计哲学速查）
- 是否有已有 PPT 文件需要复用

### Step 1.5：设计哲学推荐 ⛔ BLOCKING

**必须**根据主题和受众，从 `references/design-philosophies.md` 的 14 种哲学流派中推荐 3 种，以「设计哲学名 + Visual DNA 一句话 + 最佳用途」格式展示，供用户选择。**禁止用「A/B/C/D商务风/简约风」等普通词汇代替设计哲学推荐。**

**推荐逻辑**（优先级依次）：
1. 用户明确说了风格 → 映射到最匹配的哲学，同时给1个备选
2. 有受众信息 → 参照 `design-philosophies.md §按受众选择` 速查表
3. 有内容类型 → 参照 `design-philosophies.md §按内容类型选择` 速查表
4. 都没有 → 默认推荐 Fathom(02) + Pentagram(01) + Fukasawa(14)

**推荐格式**：每个哲学 = 名称 + Visual DNA一句话 + 色彩token + 最佳用途；末尾加「🧠 木老师倾向：」说明推荐理由。等待用户确认后进入 Step 2。

> 💡 用户风格模糊时，用 [references/directions.md](references/directions.md) 的6个快捷方向包快速推荐；哲学与图表类型适配见 [references/style-diagram-matrix.md](references/style-diagram-matrix.md)。

### Step 2：生成页面规划表 ⛔ BLOCKING

根据用户需求和已选设计哲学，为每一页/每一类页面推荐最合适的工作流：

| 页面 | 内容描述 | 推荐工作流 | 理由 |
|------|---------|-----------|------|
| 封面 | 标题+副标题 | **A**（SVG自由排版）| 高度定制，视觉冲击 |
| KPI仪表盘 | 4个核心指标 | **C**（咨询模板）| 原生形状，专业排版 |
| 甘特图 | 项目排期 | **C**（咨询模板）| gantt_timeline 模板最稳 |
| 组织架构 | 团队关系 | **C**（咨询模板）| org_chart 模板专业 |
| 自定义图表 | 数据趋势 | **A**（SVG自由排版）| 需定制配色和样式 |
| 结语 | 联系方式+致谢 | **A**（SVG自由排版）| 与封面风格一致 |

**推荐方案**（含 A/B/C/D 选项说明）：

- **方案A（全SVG）**：所有页用工作流A生成，风格高度统一，适合定制化强的场景；耗时较长
- **方案B（全咨询模板）**：所有页用工作流C生成，专业咨询级质感，适合管理汇报；模板限制较多
- **方案C（混合，推荐）**：创意页/封面/自定义页 → 工作流A；数据页/图表页/时间线 → 工作流C，两者最终合并为一个PPTX
- **方案D（编辑现有）**：基于用户提供的模板文件，走工作流D改内容；保留原有视觉风格

**等待用户确认选择方案 + 页面规划表**，确认后再分别执行对应工作流。

### Step 3：执行

- 单一工作流（A/B/C/D）→ 直接进入对应工作流
- 混合方案 → 先执行工作流A的页面，再执行工作流C的页面，用 `rearrange.py` 合并，**最后必须运行 color_unify 后处理统一色系**

```bash
# Step 1：合并（工作流A输出 + 工作流C输出）
python3 ${SKILL_DIR}/scripts/pptx_editing/rearrange.py part_a.pptx combined.pptx 0,1,2

# Step 2：⛔ BLOCKING — 色系统一（将工作流C默认麦肯锡色替换为设计哲学色板）
# --bg/--primary/--accent 从工作流0 Step 1.5 确认的色板中取值
python3 ${SKILL_DIR}/scripts/pptx_editing/color_unify.py \
  combined.pptx final.pptx \
  --bg 0D0D2B --primary 00FF88 --accent FF6B35
```

### Anti-Pattern（工作流 0）

- ❌ 禁止在用户确认页面规划表之前就开始生成任何 PPTX 内容
- ❌ 禁止只给一个方案让用户「要/不要」，必须给 A/B/C/D 四个选项
- ❌ 禁止在规划表中混淆工作流B（单张技术图表）和工作流A
- ❌ 禁止用「简约风/商务风/科技风/大气风」等普通词汇代替设计哲学推荐——必须用 design-philosophies.md 中的具名哲学（如 Fathom、Field.io、Pentagram）
- ❌ 禁止跳过 Step 1.5 直接进入 Step 2——设计哲学未确认不得出规划表
- ❌ **混合方案禁止以原始默认配色交付**——工作流C模板内置麦肯锡配色（#2E9BD6/#0A1F3D等），合并后必须用 color_unify 后处理替换为用户选定色板，未统一色系 = 未完成任务

---

## 风格体系（26 套配色）

> 🎨 **12 种设计风格 + 14 种行业配色**。用户未指定时走设计哲学推荐流程。
> 📖 完整配色表：`${SKILL_DIR}/references/style-color-layout-tables.md`

**设计风格快速路由**：

```
用户没指定 → 走设计哲学推荐流程（Fathom/Pentagram/Fukasawa）
正式/高管/投资人 → corporate / consulting
数据/分析/报告 → consulting
酷/技术/暗色 → dark / blueprint / tech
简洁/极简 → notion / flat
产品/发布 → glass
培训/课件 → general
学术/论文 → academic
政府/党政 → government
```

**行业配色**（`--industry` 参数）：金融→finance | 医疗→healthcare | 科技→technology | 教育→education | 零售→retail | 物流→logistics | 制造→manufacturing | 能源→energy | 地产→realestate | 媒体→media | 法律→legal | 农业→agriculture | 旅游→tourism | 汽车→automotive

---

## 图表体系（~79 种）

- **技术图表 27 种**（工作流B）：架构/流程/UML/AI-Agent 等，引擎来自 svg-to-ppt
- **商务图表 52 种**（工作流A）：比较/趋势/组成/指标/分析/项目/战略/信息图

> 📖 完整分类表：`${SKILL_DIR}/references/style-color-layout-tables.md`
> 📖 图表索引（含函数名）：`cat ${SKILL_DIR}/templates/charts/charts_index.json | python3 -m json.tool`

---

## 布局模板体系（20 套）

共 5 类：品牌（9）/ 通用（3）/ 场景（4）/ 政务（3）/ 特殊（1）

**场景快速路由**：战略/高管→exhibit/mckinsey | 通用商务→科技蓝商务/smart_red | 技术→anthropic/google_style | 政务→government_red/government_blue | 学术答辩→academic_defense | 金融→招商银行 | 工程→中国电建系列 | 极客→pixel_retro

> 📖 完整模板详情表：`${SKILL_DIR}/references/style-color-layout-tables.md`

### 关键说明

- 模板索引文件：`${SKILL_DIR}/templates/layouts/layouts_index.json`
- 每个模板目录包含：`design_spec.md`（设计规范）+ 标准页面 SVG（cover/toc/chapter/content/ending）

### 品牌素材

> 📖 各布局模板自带的 PNG 素材清单（22 个品牌 PNG + 2 个脚本素材）：`${SKILL_DIR}/references/brand-assets.md`

---

## 工作流 A：从零生成多页 PPT

> **核心引擎**：PPT Master 的 Strategist→Executor 流水线
> **输出**：每个元素原生可编辑的 PPTX（SVG→DrawingML 转换）

### 前置准备

```bash
# 确保依赖就绪
pip install python-pptx lxml Pillow numpy requests beautifulsoup4 svglib reportlab 2>/dev/null
```

### 文件完整性验证

> ⚠️ **所有引用文件均随 ZIP 包分发**。安装后执行以下命令验证完整性：

```bash
# 验证核心文件（子SKILL.md + 策略师 + 执行器参考文档）
for f in \
  "${SKILL_DIR}/SKILL.md" \
  "${SKILL_DIR}/references/strategist.md" \
  "${SKILL_DIR}/references/executor-base.md" \
  "${SKILL_DIR}/references/executor-general.md" \
  "${SKILL_DIR}/references/executor-consultant.md" \
  "${SKILL_DIR}/references/executor-consultant-top.md" \
  "${SKILL_DIR}/references/canvas-formats.md" \
  "${SKILL_DIR}/references/shared-standards.md"; do
  [ -f "$f" ] && echo "✅ $(basename $f)" || echo "❌ MISSING: $f"
done

# 验证核心脚本
for f in \
  "${SKILL_DIR}/scripts_ppt/project_manager.py" \
  "${SKILL_DIR}/scripts_ppt/finalize_svg.py" \
  "${SKILL_DIR}/scripts_ppt/svg_to_pptx.py" \
  "${SKILL_DIR}/scripts_ppt/svg_quality_checker.py" \
  "${SKILL_DIR}/scripts_ppt/image_gen.py" \
  "${SKILL_DIR}/scripts/pptx_editing/ooxml/unpack.py" \
  "${SKILL_DIR}/scripts/pptx_editing/ooxml/validate.py" \
  "${SKILL_DIR}/scripts/pptx_editing/ooxml/pack.py" \
  "${SKILL_DIR}/scripts/pptx_editing/rearrange.py" \
  "${SKILL_DIR}/scripts/pptx_editing/inventory.py" \
  "${SKILL_DIR}/scripts/pptx_editing/replace.py" \
  "${SKILL_DIR}/scripts/pptx_editing/thumbnail.py" \
  "${SKILL_DIR}/scripts/visual_verify.py"; do
  [ -f "$f" ] && echo "✅ $(basename $f)" || echo "❌ MISSING: $f"
done
```

### 完整 7 步流程

| 步骤 | 说明 | 关键脚本 |
|------|------|---------|
| **Step 1** | 源内容处理（PDF/DOCX/URL→MD） | `${SKILL_DIR}/scripts_ppt/source_to_md/*.py` |
| **Step 2** | 项目初始化 | `${SKILL_DIR}/scripts_ppt/project_manager.py` |
| **Step 3** | 模板选择 ⛔ BLOCKING（见下） | `${SKILL_DIR}/templates/layouts/` |
| **Step 4** | 策略师八大确认 ⛔ BLOCKING（见下） | `${SKILL_DIR}/references/strategist.md` |
| **Step 5** | AI 配图（条件触发） | `${SKILL_DIR}/scripts_ppt/image_gen.py` |
| **Step 6** | 执行器逐页生成 SVG | `${SKILL_DIR}/references/executor-*.md` |
| **Step 7** | 后处理 + 导出 PPTX | `${SKILL_DIR}/scripts_ppt/finalize_svg.py` + `svg_to_pptx.py` |

#### Step 3 详细：模板选择 ⛔ BLOCKING

> **入口条件**：Step 2 项目初始化完成
> **出口条件**：布局模板 + 配色方案已确认，用户明确同意后才能继续

1. 根据用户描述的场景/受众/风格，从布局模板体系（20套）+ 风格体系（26套）中推荐候选
2. **推荐优先级**：场景精确匹配 > 品牌匹配 > 设计风格匹配 > 通用模板（exhibit/科技蓝商务）
3. 无匹配时默认：consulting 配色 + exhibit 布局

> 📖 品牌资产接入协议（八项确认前必须执行）：[references/brand-asset-protocol.md](references/brand-asset-protocol.md)
> 📖 自定义模板设计：[references/template-designer.md](references/template-designer.md)
> 📖 设计 Token 引用语法：[references/token-reference.md](references/token-reference.md)
4. 向用户列出推荐组合（布局模板 + 配色），**等待用户明确确认**，不可跳过继续

#### Step 4 详细：策略师八大确认 ⛔ BLOCKING

> **入口条件**：Step 3 模板/配色已确认
> **出口条件**：八项参数全部用户确认，可进入 SVG 生成阶段
> 📖 详细策略师指南：`Read ${SKILL_DIR}/references/strategist.md`

需要与用户逐一确认的八项：
1. **页数**：总页数（含封面/目录/结语）
2. **画布格式**：ppt169（默认）/ ppt43 / a4 / 社交格式等
3. **内容大纲**：每页标题 + 核心内容要点
4. **配色方案**：（Step 3 已确认，此处复确认）
5. **图标库**：chunk（默认）/ tabler-filled / tabler-outline
6. **AI 配图**：是否需要 AI 生成图片，哪几页
7. **图表类型**：哪几页需要图表，具体类型
8. **交付要求**：纯 PPTX / 附视觉验证截图

以上全部确认后生成正式「设计规格书」，**执行器严格按规格书执行，不得自行发挥**。

### 关键规则

1. **串行流水线** — 步骤必须按顺序执行，前一步的输出是后一步的输入
2. **⛔ BLOCKING = 硬停** — 必须等用户明确回复才能继续
3. **主 Agent 端到端** — SVG 生成不能委托给子 Agent
4. **逐页顺序生成** — 禁止分批/并行生成页面
5. **设计哲学推荐** — 八大确认中配色走设计哲学推荐流程

### AI 配图

使用 OpenAI DALL-E 作为默认图片后端（需配置 OPENAI_API_KEY）：

```bash
python3 ${SKILL_DIR}/scripts_ppt/image_gen.py "prompt" --aspect_ratio 16:9 --image_size 1K -o <project_path>/images
```

> 📖 图片生成完整规范（11种后端+参数+水印移除）：[references/image-generator.md](references/image-generator.md)
> 📖 图片布局规范（强制执行）：[references/image-layout-spec.md](references/image-layout-spec.md)

### 视觉验证（生成后自动执行）

```bash
python3 ${SKILL_DIR}/scripts/visual_verify.py <output.pptx> --output-dir <review_dir>
```

生成逐页 JPEG 截图，审查：文字溢出、元素重叠、对齐问题、颜色对比度。

### Pre-Delivery Checklist（工作流 A）

- [ ] 页数与策略师规划一致
- [ ] 配色与用户确认的风格一致，全篇无混用
- [ ] 图标库全篇统一，未混用不同图标库
- [ ] visual_verify.py 已执行，无文字溢出/元素重叠/对齐问题
- [ ] AI 配图已嵌入且尺寸正确（若有）
- [ ] 画布格式与用户要求一致（默认 ppt169）
- [ ] PPTX 文件已发送给用户

### 画布格式（8 种场景画布）

> 📖 完整格式表 + 选择决策树：`${SKILL_DIR}/references/canvas-formats.md`
> 默认：`ppt169`（1280×720）；社交竖版 → xiaohongshu/story；印刷 → a4

---

## 工作流 B：生成单张技术图表

> **来源**：mu-svg-to-ppt 的 27 种技术图表模板 + 7 种风格
> **特色**：一张图一页 PPT，右键转换为形状后每个元素可编辑

### 适用场景

- "帮我画个微服务架构图"
- "画一张 RAG 流程图到 PPT"
- "做个类图，包含 User、Order、Product"
- "画个时序图，用 consulting 风格"

### 生成流程

#### Step 1：确定图表类型和风格

> **入口条件**：用户描述了需要生成的技术图表内容
> **出口条件**：图表类型（27 种之一）和风格（默认 consulting）已确定

从 27 种技术图表中选择（见上方图表体系），默认 `consulting` 风格。

#### Step 2：生成 SVG

> **入口条件**：Step 1 已确定图表类型和风格
> **出口条件**：SVG 代码已生成，viewBox 和占位符使用正确

根据用户描述 + 风格占位符系统生成 SVG 代码：

> 📖 Vega 数据图表引擎（柱状图/折线图/散点图等）：[references/engine-vega.md](references/engine-vega.md)
> 📖 信息图嵌入引擎（漏斗图/时间线/SWOT/KPI卡片）：[references/engine-infographic-embed.md](references/engine-infographic-embed.md)

- `viewBox="0 0 900 500"`（16:9 宽屏比例）
- 使用占位符：`{{BG_COLOR}}`、`{{TEXT_COLOR}}`、`{{ACCENT_COLOR}}` 等
- 参考模板目录：`${SKILL_DIR}/templates/charts/`

**风格占位符系统（12 个）**：

| 占位符 | 默认值 | 说明 |
|--------|---------|------|
| `{{BG_COLOR}}` | `#FFFFFF` | 背景色 |
| `{{TEXT_COLOR}}` | `#333333` | 正文色 |
| `{{ACCENT_COLOR}}` | `#FFD100` | 强调色 |
| `{{ACCENT_LIGHT}}` | `#FFF9E0` | 浅强调 |
| `{{SECONDARY_COLOR}}` | `#FFC300` | 辅助色 |
| `{{BORDER_COLOR}}` | `#E0E0E0` | 边框色 |
| `{{TITLE_COLOR}}` | `#222222` | 标题色 |
| `{{SUBTITLE_COLOR}}` | `#666666` | 副标题色 |
| `{{SUCCESS_COLOR}}` | `#52C41A` | 成功/正面 |
| `{{WARNING_COLOR}}` | `#FAAD14` | 警告 |
| `{{ERROR_COLOR}}` | `#FF4D4F` | 错误/负面 |
| `{{INFO_COLOR}}` | `#1890FF` | 信息 |

#### Step 3：替换占位符 + 嵌入 PPT

> **入口条件**：Step 2 已生成 SVG 代码
> **出口条件**：占位符已替换为目标风格色值，SVG 已嵌入 PPTX 文件

将占位符替换为目标风格色值，然后将 SVG 嵌入 PPTX：

```bash
# 方法一：用 PPT Master 引擎（DrawingML，元素级可编辑）
# 将 SVG 保存到项目目录后用 svg_to_pptx.py 导出

# 方法二：SVG 直接嵌入（Office 2019+ 右键转形状）
# 用 python-pptx 将 SVG 作为图片嵌入
```

#### Step 4：视觉验证 ⛔ BLOCKING

> **入口条件**：Step 3 已生成 PPTX 文件
> **出口条件**：visual_verify.py 已执行，截图已生成，无文字溢出/元素重叠

```bash
python3 ${SKILL_DIR}/scripts/visual_verify.py <output.pptx> -o <review_dir>
```

审查截图确认无明显问题后才可交付。**此步骤为强制门控，不可跳过。**

### Pre-Delivery Checklist（工作流 B）

- [ ] 图表类型与用户需求匹配
- [ ] 风格配色统一，占位符全部替换完毕
- [ ] SVG viewBox 尺寸正确（默认 900×500）
- [ ] visual_verify.py 已执行，无文字溢出/元素重叠
- [ ] PPTX 文件已发送给用户

### 语义形状规范（技术图表专用）

> 📖 **完整形状词汇表**（14 种参数化 SVG 模板，含用户/LLM/DB/API/决策/数据流等）：`${SKILL_DIR}/references/shape-vocabulary.md`
> 📖 **箭头语义规范**（7 种箭头类型 + 图例规则）：`${SKILL_DIR}/references/arrow-semantics.md`
> 📖 **技术产品图标**（40+ AI/技术品牌 SVG 图标）：`${SKILL_DIR}/references/tech-product-icons.md`
> 📖 SVG 图片嵌入指南：[references/svg-image-embedding.md](references/svg-image-embedding.md)
> 📖 SVG 布局最佳实践：[references/svg-layout-best-practices.md](references/svg-layout-best-practices.md)
> 📖 行业专业图标索引（45 namespace/8092 图标）：[references/icons-industry.md](references/icons-industry.md)
> 📖 PlantUML/mxGraph 图标索引：[references/icons-plantuml-index.md](references/icons-plantuml-index.md)

---

## 工作流 C：咨询汇报模板

> **引擎**：`scripts/workflow_d.py` + `scripts/consulting_pptx/`（python-pptx 原生形状，无需右键转换）
> **特点**：40 个专业咨询模板，输出原生可编辑 PPTX，零 SVG 依赖。

### 触发词

咨询汇报模板、咨询PPT、咨询风格PPT、专业业务模板、KPI仪表盘、甘特图模板、议题树、问题树、漏斗图、BCG矩阵、组织架构图、项目团队图

### 完整流程

#### Step 1：理解需求 + 推荐模板组合 ⛔ BLOCKING

> **入口条件**：用户描述了咨询模板需求
> **出口条件**：用户确认了模板列表 + 输出路径，才可执行生成

1. 根据用户需求从 40 个模板中推荐组合（先用 `--list` 查询可用模板）
2. 向用户展示：推荐的模板 ID 列表 + 每个模板的用途说明 + 预计页数
3. **等待用户明确确认**，不可自行跳过直接生成

#### Step 2：生成 PPTX

用户确认后执行：

```bash
cd ${SKILL_DIR}/scripts
# 查看所有40个模板
python3 workflow_d.py --list

# 按需组合模板生成 PPTX
python3 workflow_d.py --templates cover,agenda,kpi_dashboard,gantt_timeline --output /tmp/deck.pptx

# 生成含10张示例页的演示文稿
python3 workflow_d.py --demo --output /tmp/demo.pptx
```

### 40个模板速查表

> 📖 完整模板ID、中文名、场景、分类：`${SKILL_DIR}/references/consulting-templates.md`
> 高频模板：`cover` / `agenda` / `kpi_dashboard` / `gantt_timeline` / `org_chart` / `issue_tree` / `phases_chevron_3`

### Pre-Delivery Checklist（工作流 C）

- [ ] 模板 ID 均通过 `--list` 确认存在
- [ ] 输出 PPTX 文件已生成且非空（`ls -la`）
- [ ] PPTX 文件已发送给用户

---

## 工作流 D：编辑已有 PPT

> **来源**：pptx 内置 Skill 的 OOXML 工具链
> **适用**：修改已有 PPT 内容、基于模板生成新 PPT
>
> ⚠️ **以下脚本文件均随 ZIP 包分发**，位于 `scripts/pptx_editing/` 目录下。安装后可通过上方「文件完整性验证」命令确认。

### 场景一：修改已有 PPT

#### Step 1：解包

> **入口条件**：用户已提供待修改的 PPTX 文件
> **出口条件**：PPTX 已解包为 XML 目录结构

```bash
python3 ${SKILL_DIR}/scripts/pptx_editing/ooxml/unpack.py <input.pptx> <output_dir>
```

#### Step 2：编辑 XML

> **入口条件**：Step 1 解包完成，XML 目录已生成
> **出口条件**：目标 XML 文件已修改，修改内容与用户需求一致

直接编辑 `ppt/slides/slide{N}.xml` 等 XML 文件。

关键文件结构：
- `ppt/presentation.xml` — 主元数据
- `ppt/slides/slide{N}.xml` — 各页内容
- `ppt/notesSlides/notesSlide{N}.xml` — 演讲备注
- `ppt/theme/` — 主题配色
- `ppt/media/` — 图片媒体

#### Step 3：验证

> **入口条件**：Step 2 编辑完成
> **出口条件**：XML 验证通过，无合规性错误

```bash
cd ${SKILL_DIR}/scripts/pptx_editing/ooxml
python3 validate.py <output_dir> --original <input.pptx>
```

#### Step 4：用户确认 ⛔ BLOCKING（Confirmation Gate）

> **入口条件**：Step 3 验证通过
> **出口条件**：用户确认修改内容无误，同意打包

向用户展示修改摘要（修改了哪些页面、哪些元素、具体改动内容），等待用户明确确认后再打包。**此步骤为强制门控，不可跳过。**

#### Step 5：打包

> **入口条件**：Step 4 用户已确认
> **出口条件**：PPTX 文件已生成

```bash
python3 ${SKILL_DIR}/scripts/pptx_editing/ooxml/pack.py <output_dir> <output.pptx>
```

#### Step 6：视觉验证 ⛔ BLOCKING

> **入口条件**：Step 5 打包完成
> **出口条件**：visual_verify.py 已执行，截图已生成，无明显问题

```bash
python3 ${SKILL_DIR}/scripts/visual_verify.py <output.pptx> -o <review_dir>
```

审查截图确认无文字溢出、元素重叠、对齐问题。**此步骤为强制门控，不可跳过。**

### 场景二：基于模板生成新 PPT

#### Step 1：分析模板

> **入口条件**：用户已提供模板 PPTX 文件
> **出口条件**：模板文本已提取，缩略图已生成，页面结构已分析

```bash
# 提取文本
python3 -m markitdown template.pptx > template-content.md

# 生成缩略图
python3 ${SKILL_DIR}/scripts/pptx_editing/thumbnail.py template.pptx
```

#### Step 2：排列页面

> **入口条件**：Step 1 模板分析完成
> **出口条件**：页面已按需求重新排列，working.pptx 已生成

根据分析结果选择要用的页面，重新排列：

```bash
python3 ${SKILL_DIR}/scripts/pptx_editing/rearrange.py template.pptx working.pptx 0,3,3,7,12
```

> 页面索引从 0 开始，同一索引可重复使用（复制该页）。

#### Step 3：提取文本清单

> **入口条件**：Step 2 页面排列完成
> **出口条件**：text-inventory.json 已生成，包含所有 shape 文本结构

```bash
python3 ${SKILL_DIR}/scripts/pptx_editing/inventory.py working.pptx text-inventory.json
```

#### Step 4：准备替换内容

> **入口条件**：Step 3 文本清单已生成
> **出口条件**：replacement-text.json 已准备，覆盖所有需替换的 shape

根据 `text-inventory.json` 中的 shape 结构准备 `replacement-text.json`：

```json
{
  "slide-0": {
    "shape-0": {
      "paragraphs": [
        {"text": "新标题", "bold": true, "alignment": "CENTER"}
      ]
    }
  }
}
```

> ⚠️ 未在 JSON 中提供 `paragraphs` 的 shape 会被自动清空文本。

#### Step 5：用户确认 ⛔ BLOCKING（Confirmation Gate）

> **入口条件**：Step 4 替换内容已准备
> **出口条件**：用户确认替换内容无误，同意执行

向用户展示替换计划摘要（哪些页面的哪些 shape 将被替换为什么内容），等待用户明确确认后再执行替换。**此步骤为强制门控，不可跳过。**

#### Step 6：应用替换

> **入口条件**：Step 5 用户已确认
> **出口条件**：output.pptx 已生成

```bash
python3 ${SKILL_DIR}/scripts/pptx_editing/replace.py working.pptx replacement-text.json output.pptx
```

#### Step 7：视觉验证 ⛔ BLOCKING

> **入口条件**：Step 6 替换完成，PPTX 已生成
> **出口条件**：visual_verify.py 已执行，截图已生成，无明显问题

```bash
python3 ${SKILL_DIR}/scripts/visual_verify.py <output.pptx> -o <review_dir>
```

审查截图确认无文字溢出、元素重叠、对齐问题。**此步骤为强制门控，不可跳过。**

### Pre-Delivery Checklist（工作流 D）

- [ ] 修改/替换内容与用户需求一致
- [ ] XML 验证通过（场景一）或替换 JSON 正确（场景二）
- [ ] 用户已确认修改摘要（Confirmation Gate 已通过）
- [ ] visual_verify.py 已执行，无文字溢出/元素重叠/对齐问题
- [ ] 原始 PPTX 未被覆盖（输出为新文件）
- [ ] PPTX 文件已发送给用户

---

## 图标库（6,732 个 SVG 图标）

三个图标库，MIT 许可：

| 库 | 风格 | 数量 | 推荐场景 |
|----|------|------|---------|
| `chunk` | 填充 · 方正 | 640 | **默认**，大多数场景 |
| `tabler-filled` | 填充 · 圆润 | 1,053 | 柔和/温暖设计 |
| `tabler-outline` | 描边 · 线条 | 5,039 | 轻量/极简风格 |

**搜索图标**：
```bash
ls ${SKILL_DIR}/templates/icons/chunk/ | grep chart
```

> ⚠️ 一个演示文稿只用一个图标库，禁止混用。

---

## 脚本索引

### 核心生成引擎（`${SKILL_DIR}/scripts_ppt/`）

| 脚本 | 用途 |
|------|------|
| `source_to_md/*.py` | 源文档转 Markdown（PDF/DOCX/URL/PPTX） |
| `project_manager.py` | 项目初始化 / 验证 / 管理 |
| `image_gen.py` | AI 图片生成（openai/gemini 后端） |
| `svg_quality_checker.py` | SVG 质量检查 |
| `finalize_svg.py` | SVG 后处理（图标嵌入/图片修复/文本扁平化） |
| `svg_to_pptx.py` | SVG→DrawingML 导出 PPTX |
| `total_md_split.py` | 演讲备注拆分 |
| `config.py` | 统一配置（配色/画布/行业色） |
| `analyze_images.py` | 图片分析 |
| `svg_to_pptx/` | SVG→DrawingML 转换引擎（7 模块） |
| `svg_finalize/` | SVG 后处理模块 |
| `image_backends/` | openai/gemini 图片生成后端 |

### 编辑工具链（`scripts/pptx_editing/`）

| 脚本 | 用途 |
|------|------|
| `ooxml/unpack.py` | 解包 PPTX 为 XML |
| `ooxml/validate.py` | 验证 XML 合规性 |
| `ooxml/pack.py` | 打包 XML 为 PPTX |
| `rearrange.py` | 页面重排/复制/删除 |
| `inventory.py` | 提取文本结构清单 |
| `replace.py` | 批量替换文本内容 |
| `thumbnail.py` | 生成缩略图网格 |

### 增强工具（`scripts/`）

| 脚本 | 用途 |
|------|------|
| `visual_verify.py` | PPTX→PDF→JPEG 视觉验证 |

---

## Anti-Pattern 清单

> 以下为三个工作流的禁止行为，违反任何一条视为执行失败。

### 工作流 A（从零生成）

- ❌ 禁止并行或分批生成 SVG 页面，必须逐页顺序生成
- ❌ 禁止跳过 ⛔ BLOCKING 步骤（模板选择、策略师八大确认）
- ❌ 禁止将 SVG 生成委托给子 Agent，主 Agent 必须端到端执行
- ❌ 禁止在一份演示文稿中混用多个图标库
- ❌ 禁止在一份演示文稿中混用多套配色方案
- ❌ ✅ IRON LAW: visual_verify 必须通过
- ❌ 禁止忽略策略师确认的设计规格书，执行器必须严格遵循

### 工作流 B（技术图表）

- ❌ 禁止不确定图表类型就直接生成 SVG
- ❌ 禁止手动硬编码色值替代占位符系统
- ❌ 禁止混用不同风格的占位符色值
- ❌ 禁止修改 viewBox 比例而不告知用户
- ❌ ✅ IRON LAW: visual_verify 必须通过

### 工作流 C（咨询汇报模板）

- ❌ 禁止修改 scripts/consulting_pptx/ 源码，只调用不改动
- ❌ 禁止硬编码 token/key/凭据到任何文件
- ❌ 禁止在不确认模板 ID 有效的情况下直接生成（先 `--list` 查询）
- ❌ 禁止跳过 Step 1 确认门控直接生成（必须等用户确认模板组合）

### 工作流 D（编辑已有 PPT）

- ❌ 禁止不经用户确认就执行打包（Confirmation Gate 不可跳过）
- ❌ 禁止覆盖用户的原始 PPTX 文件，必须输出为新文件
- ❌ ✅ IRON LAW: visual_verify 必须通过
- ❌ 禁止跳过 XML 验证步骤（场景一）
- ❌ 禁止遗漏 replacement-text.json 中的 shape 导致内容被意外清空

---

## 已知局限

- visual_verify 依赖 LibreOffice，容器环境需预装（降级：browser automation tool 截图验证）
- AI 图片生成需配置对应后端 API Key（gemini/openai/qwen 等11种后端可选）
- 超大 PPTX（>50页）可能超时，建议分批生成
- SVG 技术图表复杂度受 python-pptx 限制

---

## 降级链速查

| 失败点 | 降级方案 |
|--------|---------|
| visual_verify.py（LibreOffice不可用） | browser automation tool 截图验证 |
| AI 图片生成失败 | 纯色占位图+提示用户替换 |
| source_to_md 转换失败 | 手动粘贴关键内容 |
| SVG 质量检查失败 | 肉眼检查+用户确认 |

---

## 参考文档

> 完整 references/ 索引见 `${SKILL_DIR}/references/` 目录，按需读取。
> 📖 15 个示例项目：[references/example-projects.md](references/example-projects.md)
