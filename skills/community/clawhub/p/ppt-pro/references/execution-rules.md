# PPT Pro — 执行规则与扩展上下文

本文件为 [SKILL.md](../SKILL.md) 的渐进披露参考：策划串并行、Sub-agent 模板、操作边界、Step 5c 资源加载与 prompt 组装、HTML 并行生成等。

---

## Step 2 — 查询维度示例表

根据主题和用户需求规划多维度搜索（数量参考 SKILL 复杂度表）。**不要所有查询都是同一维度的换词**；每个维度至少 1 个查询，核心维度可多个。

| 查询维度 | 示例 | 目的 |
|---------|------|------|
| 核心定义 | "{主题} 是什么 / 定义 / 核心概念" | 确保基础事实准确 |
| 市场数据 | "{主题} 市场规模 / 增长率 / 行业报告 2024-2026" | 数据卡片填充 |
| 竞品/对比 | "{主题} vs {竞品} / 对比分析 / 优劣势" | 对比论证素材 |
| 案例/应用 | "{主题} 客户案例 / 应用场景 / 成功案例" | 故事化说服 |
| 趋势/展望 | "{主题} 发展趋势 / 未来展望 / 技术路线图" | 结尾展望素材 |
| 权威观点 | "{主题} 专家评价 / 行业报告 / 白皮书" | 权威背书 |

---

## Step 2 — 搜索结果 JSON 模板

每组搜索结果须结构化整理为以下格式，不要只贴原文：

```json
{
  "query": "搜索查询",
  "findings": [
    {
      "fact": "一句话核心发现",
      "data": "具体数据/数字（如有）",
      "source": "来源（网站/报告名/作者）",
      "reliability": "high | medium | low",
      "relevance": "与大纲哪个 Part 最相关"
    }
  ]
}
```

**可信度判定**：

- **high**：权威机构报告（Gartner/IDC/政府统计）、学术论文、官方文档
- **medium**：行业媒体报道、企业博客、分析师个人观点
- **low**：论坛讨论、自媒体、无来源数据

> 只有 high/medium 的数据才能进入策划稿的 data_highlights。low 可信度数据仅作参考，不用于关键数据展示。

---

## Step 3 — 大纲方法论补充

**方法论**（配合 `prompt-2-outline.md`）：

- **金字塔原理** — 结论先行、以上统下、归类分组、逻辑递进
- **叙事弧线** — 根据 Step 1 第 4 题选择的叙事结构，确定 Part 排列的情感轨迹
- **论证策略** — 每 Part 选择论证策略（data_driven / case_study / comparison / framework / step_by_step / authority）

**大纲架构师的 5 步思考过程**（prompt 内置，自动执行）：

1. 提炼全局核心论点（1 句话 core_thesis）
2. 确定 Part 数量和主题（含 Part 间逻辑关系标注）
3. 为每 Part 选择论证策略
4. 分配页面并确定每页论点
5. 标注每页数据需求和搜索覆盖情况

---

## Step 5a 与 prompt 的衔接（风格注入）

风格的装饰工具箱已在 `styles/README.md` 中定义，首页生成前读取一次即可。`style.json` 承载三层信息：**灵魂层**（mood_keywords / design_soul / variation_strategy）+ **装饰基因层**（decoration_dna）+ **色值层**（css_variables）。灵魂层和装饰基因层由 `prompt_assembler.py` 自动注入到每页 prompt 中，为设计师提供情绪锚点和变奏引导。

---

## Step 5b — 配图执行要点

> **prompt 已由 Step 4 策划阶段生成**，写入 `planning{n}.json` 的 `image.prompt` 字段。Step 5b 只需读取并调用 `generate_image`。

- 配图时机：在生成每页 HTML **之前**先生成该页配图
- `image-generation.md` 的融入技法和 HTML 模板已在 4a 预读阶段读取（供 Step 5c 使用）
- 融入技法不限，LLM 自由选择最佳视觉效果

---

## Step 4 — 4a 资源预读补充说明

> 第 0 项（`design-principles-cheatsheet.md`）是整个策划阶段的**地基**。它将 6 大设计原则（CRAP/Miller's Law/60-30-10/格式塔/Tufte/金字塔原理）翻译为 planning JSON 的字段级操作指令 — 每条原则直接告诉 LLM 操作哪个字段、填什么值、怎么判断对不对、不对怎么改。通过 `{{DESIGN_PRINCIPLES_CHEATSHEET}}` 占位符注入到 prompt-3 的上下文中。

> 第 7 项仅在 Q12 配图偏好 != A（不需要）时读取。策划师要写 `image.prompt`，就必须先掌握 prompt 构造方法、场景翻译技巧和各风格的关键词——没有这些上下文就是「没见过食材长什么样就要写菜谱」。

> 第 6 项的 `styles/README.md` 只读「装饰技法工具箱」章节（约 L100-141），**不读**风格决策流程和调色板信息（那些留给 Step 5a）。策划师需要知道「有哪些装饰手法可选」，但不需要此刻决定具体配色。

> 预读后，策划师就知道自己的「工具箱」里有什么。后续逐页策划时，根据内容特征从工具箱中选择最合适的组件，而非只用最熟悉的几种。

### 4b — 持久上下文注入（核心机制）

- `{{DESIGN_PRINCIPLES_CHEATSHEET}}` — 替换为 4a 阶段读取的 `principles/design-principles-cheatsheet.md` 的完整内容。确保 6 大黄金标准的核心决策点在每页策划时始终在上下文中。
- `{{RESOURCE_MENU}}` — 替换为 `resource-menu.md` 的完整内容。这是一张精简的资源菜单速查卡（布局/卡片/图表/card_style/装饰技法的完整选项列表），防止 LLM 在策划后半程因上下文衰减而退化为只用 text+data+list 三板斧。每次策划每页时 LLM 都能「翻看菜单」而不是靠记忆。
- 其他占位符（`{{SCENE}}` / `{{AUDIENCE}}` / `{{PERSUASION_STYLE}}` / `{{BRAND_INFO}}` / `{{CONTENT_CONSTRAINTS}}` / `{{IMAGE_PREFERENCE}}`）从 Step 1 需求 JSON 的对应字段填入。

### 4b — 设计感强制约束（灵魂级）

1. **彻底拒绝千篇一律的普通前端排版**，策划的必须是**完完全全的 PPTX 演讲展示组合**。
2. **单页组合极其要求随机但是灵动**：绝不能上下两页长得一模一样，通过极端反差、非对称策略打破死板。
3. **高质量的设计上下文传递**：必须通过 `director_command` 填写极具张力和具体排版暗示（如出血、压盖、全屏文本）的指令，指引下游的 HTML 生成渲染出完美符合 PPTX 共识的画面效果。单页设计极其重要，必须给足高质量上游意图上下文。

---

## Step 4 — 策划稿：串行 vs 并行（Sub-agent）

根据环境感知阶段检测的 `has_subagent` 标记自动选择模式。

### 模式 A：串行模式（无 sub-agent）

```
── 第 1 页 ──────────────────────────────
生成：用 Prompt #3 为第 1 页生成策划 JSON
写入：write_to_file -> OUTPUT_DIR/planning/planning1.json
验证：python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning/planning1.json --refs SKILL_DIR/references

── 第 2 页 ──────────────────────────────
生成：用 Prompt #3 为第 2 页生成策划 JSON
      注入上下文：上一页 JSON（保证衔接）
写入：write_to_file -> OUTPUT_DIR/planning/planning2.json
验证：python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning/planning2.json --refs SKILL_DIR/references

── 第 3, 4, 5... 页 重复 ──────────────
每页都是：生成 -> write_to_file -> 验证 -> 下一页
```

### 模式 B：并行模式（有 sub-agent，标准/大型复杂度时推荐）

> **按 Part 分组并行，组内串行。** 同一 Part 的页面由同一个 sub-agent 串行生成（保证章节内衔接），不同 Part 的 sub-agent 并行执行（加速整体流程）。

**分发前准备**（主 agent 执行）：

1. 完成 4a 资源菜单预读
2. 确定 Part 分组：`Part 1: [page 1-4], Part 2: [page 5-8], ...`
3. 为每组准备共享上下文：需求 JSON + 大纲 JSON + 搜索素材 + 资源菜单内容 + 设计原则 cheatsheet

**并行分发**（使用 Agent tool / 等价并行工具）：

```
┌─ Sub-agent A (Part 1: 封面+引入) ──────────────────────
│  输入：共享上下文 + Part 1 页面列表 + 上下文衔接指令
│  任务：逐页生成 planning JSON -> 写入 -> 验证
│  产物：planning1.json ~ planning4.json
│
├─ Sub-agent B (Part 2: 核心论证) ───────────── 并行 ────
│  输入：共享上下文 + Part 2 页面列表 + Part 1 最后一页摘要（衔接用）
│  任务：逐页生成 planning JSON -> 写入 -> 验证
│  产物：planning5.json ~ planning8.json
│
├─ Sub-agent C (Part 3: 总结+结尾) ───────────── 并行 ────
│  输入：共享上下文 + Part 3 页面列表 + Part 2 最后一页摘要（衔接用）
│  任务：逐页生成 planning JSON -> 写入 -> 验证
│  产物：planning9.json ~ planning12.json
└────────────────────────────────────────────────────────
```

### Sub-agent Prompt 模板（策划师）

```
你是 PPT 策划师，负责生成第 {start_page} ~ {end_page} 页的策划稿 JSON。

## 共享上下文
- 需求 JSON: {requirement_json}
- 大纲 JSON: {outline_json}（仅你负责的 Part 部分）
- 搜索素材: {search_findings_for_this_part}
- 设计原则 Cheatsheet: {cheatsheet_content}
- 资源菜单: {resource_menu_content}

## 衔接上下文
- 上一个 Part 最后一页摘要: {previous_part_last_page_summary}
  （第一个 Part 无此项）

## 执行规则
1. 严格遵循 Prompt #3 的策划规范
2. 每页生成后立即写入 OUTPUT_DIR/planning/planning{n}.json
3. 写入后运行验证: python3 SKILL_DIR/scripts/planning_validator.py OUTPUT_DIR/planning/planning{n}.json --refs SKILL_DIR/references
4. ERROR 必须修正后再继续下一页
5. 组内串行：上一页的完整 JSON 作为下一页的衔接上下文
```

**回收与校验**（主 agent 执行）：

1. 等待所有 sub-agent 完成
2. 运行全量验证（含跨页规则）
3. 重点检查 Part 交界处（如 page 4→5, page 8→9）的衔接是否自然，必要时微调

**轻量模式（<= 8 页）**：即使有 sub-agent 也建议串行，页数少时并行开销不划算。

> **验证是写入流程的一部分，不是事后审查。** 每页 JSON 写入后立即运行 `planning_validator.py` 单页验证。validator 检查：字段完整性、枚举值合法性、资源文件路径存在性、card_style 多样性。有 ERROR 时必须修正后再继续下一页。

### 操作边界（串行 / 并行通用）

1. 每次只在 Prompt #3 中请求**一页**的策划（封面/目录/章节封面等极简页可 2-3 页一起，但仍然每页独立文件）
2. 每页生成后**必须**立即写入 `planning/planning{n}.json`
3. 写入后立即运行 `planning_validator.py` 验证（ERROR = 必须修正，WARNING = 建议修正）
4. 验证通过后才开始下一页
5. 不要用 Python 脚本操作 JSON 文件
6. 不要尝试一次输出全部页面

**上下文传递**：每页生成时注入上一页的完整 JSON，保证内容衔接和节奏递进。并行模式下，Part 交界处通过「上一 Part 最后一页摘要」传递衔接上下文。

---

## Step 5c — 资源按需加载决策树

> **核心理念：用户采访后获得的信息已经足以确定后续需要读取哪些资源。** 不要一口气读完所有参考文件，按以下三层决策树精确加载。

### 第一层：采访后全局决策（Step 1 完成后立即执行，全流程只做一次）

根据 Step 1 的采访答案，确定整个 PPT 生命周期内的资源加载策略：

| 采访答案 | 触发的加载决策 |
|---------|--------------|
| Q12 配图偏好 = A（不需要） | 整个流程**跳过** `image-generation.md`，Step 5b 全部跳过 |
| Q12 配图偏好 = B/C/D | 标记**需要配图**，4a 预读阶段读取 `image-generation.md`（prompt 构造公式 + 风格关键词表 + 构图自适应表），Step 4 每页策划时填写 `image` 字段，Step 5b 执行 |
| Q7 风格选择 = A-H（明确选择预置风格） | Step 5a 直接读取对应 style_id 的文件（style_id -> 文件路径映射见 `resource-registry.md` 第 1 节），跳过其他风格 |
| Q7 风格选择 = I（AI 自动匹配） | 先读 `styles/README.md` 的决策规则，确定风格后只读命中风格的独立文件 |
| Q7 风格选择 = J（自定义） | 读 `styles/README.md` 的灵动创作方法论，基于用户描述自创配色方案 |
| Q11 语言偏好 = B/C/D（非纯中文） | 标记**多语言模式**，Step 5a 额外读取 `styles/README.md` 的「多语言排版优化」章节 |
| Q6 说服力要素 = 数据为主 | 标记**数据密集型**，Step 4 每页 data 卡片比例提高 |
| Q4 叙事结构 = 时间线 | 标记**时间线叙事**，Step 4 中更倾向使用 timeline chart_type |

### 第二层：大纲后节奏决策（Step 3 完成后执行，全流程只做一次）

| 大纲信息 | 触发的加载决策 |
|---------|------|
| 总页数 <= 12 | 读取 `narrative-rhythm.md` 的 **10 页标准模板** |
| 总页数 13-17 | 读取 `narrative-rhythm.md` 的 **15 页标准模板** |
| 总页数 >= 18 | 读取 `narrative-rhythm.md` 的 **20 页标准模板** |
| Part 数量确定后 | 读取 `narrative-rhythm.md` 的**章节色彩递进规则** |

### 第三层：prompt_assembler 自动组装完整 prompt（GATE CHECK #1 强制执行）

> **⛔ [STOP] GATE CHECK #1 — 在生成任何 HTML 前，必须先执行以下两步，任何一步失败都禁止继续：**
>
> ```bash
> # 步骤 A: planning 门禁（validator 必须 PASS）
> bash SKILL_DIR/scripts/pipeline_gate.sh check-planning OUTPUT_DIR SKILL_DIR
>
> # 步骤 B: 组装 prompt-ready 文件
> python3 SKILL_DIR/scripts/prompt_assembler.py \
>   OUTPUT_DIR/planning/ \
>   --refs SKILL_DIR/references \
>   --style OUTPUT_DIR/style.json \
>   -o OUTPUT_DIR/prompts-ready/
>
> # 步骤 C: 验证 prompts-ready 文件已生成
> bash SKILL_DIR/scripts/pipeline_gate.sh check-prompts OUTPUT_DIR
> ```
>
> **核心变化：LLM 不再需要自己拼装 prompt。** `prompt_assembler.py` 一次性完成所有占位符替换，输出一个开箱即用的完整 prompt 文件。LLM 只需 `view_file` 一个文件就获得全部上下文（设计模板 + CSS 变量 + 策划 JSON + 配图信息 + [RESOURCES] 资源块），从根本上消除「忘记读资源」的可能性。
>
> **如果你发现 `prompts-ready/` 目录不存在或为空，说明 GATE CHECK 未通过，立即回退执行。**

**原理**：`prompt_assembler.py` 读取 `prompt-4-design.md` 模板，替换其中 6 个占位符：

- `{{STYLE_DEFINITION}}` <- `style.json` 的 CSS 变量定义（灵魂层 + 装饰基因层 + 色值层）
- `{{PLANNING_JSON}}` <- `planning{n}.json` 的完整 JSON
- `{{PAGE_CONTENT}}` <- 从 planning JSON 中提取的内容摘要
- `{{IMAGE_INFO}}` <- 配图信息（usage + path + placement），无配图时自动省略
- `{{TECHNIQUE_CARDS}}` <- 从 `director_command` 中提取技法牌编号（T1-T10），展开为该页所需的 2-3 张牌的完整 CSS 原子代码 + ADAPT 参数范围（来源：`references/technique-cards.md`）
- `{{RESOURCES}}` <- 内部调用 `resource_assembler.py` 组装的完整资源块（布局骨架 + 组件模板 + 图表模板 + 设计原则）

**首页 HTML 生成前的强制执行流程（批量模式，推荐）**：

```bash
# 一次性为所有页面组装完整 prompt（执行一次，后续逐页 view_file）
python3 SKILL_DIR/scripts/prompt_assembler.py \
  OUTPUT_DIR/planning/ \
  --refs SKILL_DIR/references \
  --style OUTPUT_DIR/style.json \
  --image-dir OUTPUT_DIR/images/ \
  -o OUTPUT_DIR/prompts-ready/
```

也支持单页模式：

```bash
python3 SKILL_DIR/scripts/prompt_assembler.py \
  OUTPUT_DIR/planning/planning{n}.json \
  --refs SKILL_DIR/references \
  --style OUTPUT_DIR/style.json \
  --image-dir OUTPUT_DIR/images/ \
  -o OUTPUT_DIR/prompts-ready/prompt-ready-{n}.txt
```

**每页 HTML 生成时只需一步**：

```
view_file OUTPUT_DIR/prompts-ready/prompt-ready-{n}.txt
```

然后直接根据完整 prompt 生成 HTML，**不需要再手动读取任何资源文件**。

> 脚本输出会显示资源统计和 WARNING（文件未找到时），方便快速发现 planning JSON 中的路径错误。

### 首页生成前必须完整读取的全局资源（仅一次，全局生效）

- `references/styles/README.md` -- 装饰技法工具箱 + 色彩原则
- `references/principles/README.md` -- 设计原则索引
- `references/blocks/README.md` -- 复合组件索引

> **注意**：`prompt-4-design.md` 不再需要手动读取，其内容已由 `prompt_assembler.py` 自动注入到每页的 `prompt-ready-{n}.txt` 中。

> 页面类型专属规范：封面/目录/章节封面/结束页的结构规范已通过 `required_resources.page_template` 指定路径（如 `page-templates/cover.md`），无需另行查映射。**规范只定义「必须有哪些区域」，不提供具体 HTML 代码**。每次生成时，构图方式、排版比例、装饰元素必须根据所选风格的装饰 DNA 自由变化。

> 叙事节奏：整体 PPT 的视觉密度起伏须遵循 `references/narrative-rhythm.md` 的节奏规则和标准模板。

> CSS 动画（可选）：HTML 预览可嵌入渐入/计数/填充/描边动画，见 `references/prompts/animations.md`。不影响 PPTX 输出。

> **禁止跳过策划稿直接生成。** 每页必须先有 Step 4 的结构 JSON。

> **装饰手法不在每页 Prompt 中重复注入。** 装饰工具箱（`styles/README.md`）在首页生成前读取一次，模型每页自由组合不同装饰技法，而不是被同一份装饰说明反复引导。

### 核心设计约束（完整清单见 prompt-ready 文件内部）

- 画布 1280x720px，overflow:hidden
- 所有颜色通过 CSS 变量引用，禁止硬编码
- CSS 技法不受限，可自由使用伪元素、渐变、滤镜等一切浏览器原生能力，追求极致视觉效果
- 配图融入设计：按 `planning{n}.json` 的 `image.usage` 决定融入技法（7 种用法详见 `image-generation.md`）

**布局骨架引用（防错位核心机制）**：每个布局文件（如 `layouts/hero-top.md`）包含完整的 HTML 骨架代码。prompt-ready 文件的 [RESOURCES] 块中 LAYOUT 分区已包含完整骨架代码，以此为起点填充内容。跨行/跨列卡片的 `grid-row` / `grid-column` 属性必须与骨架保持一致。

### 逐页生成（严格流程 — 禁止跳步）

> **⛔ 强制门禁 — 开始生成 HTML 前必须执行**：
> ```bash
> bash SKILL_DIR/scripts/pipeline_gate.sh check-prompts OUTPUT_DIR
> ```
> 若输出 `[GATE ✗ BLOCKED]`，禁止继续，必须先修复错误。

```
每页 HTML 的生成流程（N = 页码）：

  GATE:   bash SKILL_DIR/scripts/pipeline_gate.sh check-prompts OUTPUT_DIR
          ↳ 失败？→ 先修复 planning/validator 错误，再运行 prompt_assembler.py

  STEP 1: view_file OUTPUT_DIR/prompts-ready/prompt-ready-{N}.txt
          ↳ 获得完整上下文（设计模板 + CSS 变量 + 策划 JSON + 配图路径 + [RESOURCES] 资源块）
          ↳ 必须完整读取此文件，禁止凭记忆或跳过直接写 HTML

  STEP 2: 基于 prompt-ready 内容生成 HTML
          ↳ 布局骨架必须来自 [RESOURCES] 的 LAYOUT 分区
          ↳ 复合组件必须参考 [RESOURCES] 的 CARD_RESOURCES 分区
          ↳ 图表模板必须参考 [RESOURCES] 的 chart 分区

  STEP 3: 5 项自检 → 写入 OUTPUT_DIR/slides/slide-{NN}.html
          ↳ ① 内容与 planning.goal 对应  ② 无卡片溢出/重叠
          ↳ ③ 画布 1280x720 overflow:hidden  ④ 颜色全用 var(--)
          ↳ ⑤ data-pptx-role 属性完整（content/decoration/watermark）
```

**禁止行为**：不读 prompt-ready 文件就直接写 HTML。这是 Step 5c 的第一条红线。

---

## Step 5c — 并行生成 HTML（Sub-agent 可用时启用）

> 每页 HTML 的生成输入**完全自包含**，页面之间无运行时依赖，天然适合并行。有 sub-agent 能力时**必须启用并行模式**（标准/大型复杂度）。

每页 HTML 的生成输入：

```
并行单元输入:
  page_number:       页码
  prompt_ready_txt:  prompt_assembler.py 为该页生成的 prompt-ready-{n}.txt 完整内容
                     （已包含设计模板 + CSS 变量 + 策划 JSON + 配图信息 + [RESOURCES] 资源块）
  global_resources:  首页前已读取的全局资源（styles/README / principles/README / blocks/README / card-styles.md）
```

**并行策略**：按 Part 分组（同一 Part 的页面分给同一 sub-agent，保证章节内视觉一致性）。不同 Part 的 sub-agent 并行执行。

**分发前准备**（主 agent 执行）：

1. 完成 GATE CHECK（prompt_assembler.py 已为所有页面生成 prompt-ready 文件）
2. 读取全局资源（styles/README.md + principles/README.md + blocks/README.md）
3. 确定 Part 分组

**并行分发**（使用 Agent tool / 等价并行工具）：

```
┌─ Sub-agent A (Part 1: page 1-4) ──────────────────────
│  输入：global_resources + prompt-ready-1~4.txt 内容
│  任务：逐页读取 prompt-ready -> 生成 HTML -> 5 项自检 -> 写入 slides/
│  产物：slide-01.html ~ slide-04.html
│
├─ Sub-agent B (Part 2: page 5-8) ────────── 并行 ──────
│  输入：global_resources + prompt-ready-5~8.txt 内容
│  任务：同上
│  产物：slide-05.html ~ slide-08.html
│
├─ Sub-agent C (Part 3: page 9-12) ───────── 并行 ──────
│  输入：global_resources + prompt-ready-9~12.txt 内容
│  任务：同上
│  产物：slide-09.html ~ slide-12.html
└────────────────────────────────────────────────────────
```

### Sub-agent Prompt 模板（设计师）

```
你是 PPT 设计师，负责生成第 {start_page} ~ {end_page} 页的 HTML 设计稿。

## 全局资源（已读取，直接使用）
{global_resources_content}

## 执行规则
对于你负责的每一页（N = {start_page} ~ {end_page}）：

1. 读取 OUTPUT_DIR/prompts-ready/prompt-ready-{N}.txt
2. 基于 prompt-ready 内容生成 HTML：
   - 布局骨架来自 [RESOURCES] 的 LAYOUT 分区
   - 复合组件参考 [RESOURCES] 的 CARD_RESOURCES 分区
   - 图表模板参考 [RESOURCES] 的 chart 分区
3. 5 项自检（内容完整/布局无重叠/不溢出画布/色彩规范/资源已消费）
4. 写入 OUTPUT_DIR/slides/slide-{NN}.html（NN = 两位数页码）

## 核心约束
- 画布 1280x720px，overflow:hidden
- 所有颜色通过 CSS 变量引用
- 禁止不读 prompt-ready 文件就直接写 HTML
- 组内逐页串行生成，保证章节内视觉一致性
```

**回收与校验**（主 agent 执行）：

1. 等待所有 sub-agent 完成
2. 检查所有 `slide-XX.html` 文件是否存在
3. 跨页视觉一致性抽检（Part 交界处的配色/装饰风格衔接）
4. 运行 `html_packager.py` 生成 `preview.html`

**串行退化**：轻量模式（<= 8 页）或无 sub-agent 时，主 agent 按原有逐页串行流程执行。

---

## 跨页视觉叙事（执行侧提醒）

按 `references/narrative-rhythm.md` 的节奏规则和章节色彩递进规则执行，确保密度交替、章节色彩递进、封面-结尾呼应。
