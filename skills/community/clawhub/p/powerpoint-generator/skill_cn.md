---
name: ppt-agent
description: 专业 PPT 演示文稿全流程 AI 生成助手。模拟顶级 PPT 设计公司的完整工作流（需求调研 -> 资料搜集 -> 大纲策划 -> 策划稿 -> 设计稿），输出高质量 HTML 格式演示文稿。当用户提到制作 PPT、做演示文稿、做 slides、做幻灯片、做汇报材料、做培训课件、做路演 deck、做产品介绍页面时触发此技能。即使用户只说"帮我做个关于 X 的介绍"或"我要给老板汇报 Y"，只要暗示需要结构化的多页演示内容，都应该触发。也适用于用户说"帮我把这篇文档做成 PPT"、"把这个主题做成演示"等需要将内容转化为演示格式的场景。
---

# PPT Agent -- 专业演示文稿全流程生成

## 核心理念

模仿专业 PPT 设计公司（报价万元/页级别）的完整工作流，而非"给个大纲套模板"：

1. **先调研后生成** -- 用真实数据填充内容，不凭空杜撰
2. **策划与设计分离** -- 先验证信息结构，再做视觉包装
3. **内容驱动版式** -- Bento Grid 卡片式布局，每页由内容决定版式
4. **全局风格一致** -- 先定风格再逐页生成，保证跨页统一
5. **智能配图** -- 利用图片生成能力为每页配插图（绝大多数环境都有此能力）

---

## 环境准备 [首次使用必读]

### Node.js 环境

**中国大陆镜像安装**（必须设置，否则 puppeteer Chrome 二进制下载会失败）：

```bash
export PUPPETEER_DOWNLOAD_HOST=https://storage.googleapis.com.cnpmjs.org
npm install -g puppeteer --unsafe-perm
npm install -g dom-to-svg esbuild
```

**验证**：`node -e "require('puppeteer'); console.log('puppeteer OK')"`

### Python 环境

```bash
pip install python-pptx lxml Pillow
```

---

## 管线强制声明 [红线]

> 以下规则不可违反，任何绕过都会导致输出质量严重下降。

### 六步管线顺序固定，禁止跳过

```
Step 1 → Step 2 → Step 3 → Step 4 → Step 5 → Step 6
```

### 禁止行为

- ❌ 跳过 Step 1 直接生成 PPT
- ❌ 没有策划稿就进入 Step 5c
- ❌ 停在 preview.html 不执行 SVG 和 PPTX
- ❌ 用其他工具/管线替代本流程

### 唯一允许的降级

- Node.js 不可用 → 跳过 SVG 分支，只输出 preview.html，告知用户
- Python 不可用 → 跳过 SVG + PNG + PPTX 分支，只输出 preview.html，告知用户并等待反馈
- Puppeteer 不可用 → 跳过 PNG 分支（Visual QA 也跳过），SVG 分支继续
- 视觉模型不可用 → 跳过视觉审计，DOM 断言仍正常运行

### 各 Step 强制级别

| Step | 强制级别 |
|------|---------|
| Step 1 | STOP -- 禁止跳过，必须等用户回复 |
| Step 2-3 | 禁止跳过 |
| Step 4 | 禁止跳过，必须等用户确认大纲 |
| Step 5 内部 | 顺序固定：5a → 5b → 5c |
| Step 6 | 禁止跳过，必须执行全部后处理管线 |

---

## 环境感知

开始工作前自省 agent 拥有的工具能力：

| 能力 | 降级策略 |
|------|---------|
| **信息获取**（搜索/URL/文档/知识库） | 全部缺失 -> 依赖用户提供材料 |
| **图片生成**（绝大多数环境都有） | 缺失 -> 纯 CSS 装饰替代 |
| **文件输出** | 必须有 |
| **脚本执行**（Python/Node.js） | 缺失 -> 跳过自动打包和 SVG 转换 |

**原则**：检查实际可调用的工具列表，有什么用什么。

---

## 路径约定

整个流程中反复用到以下路径，在 Step 1 完成后立即确定：

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

跳过前置步骤时，必须补全对应依赖产物：

| 起始步骤 | 缺失依赖 | 补全方式 |
|---------|---------|---------|
| Step 4 | 每页内容文本 | 先用 Prompt #3 为每页生成内容分配 |
| Step 5 | 策划稿 JSON | 用户提供或先执行 Step 4 |

### 复杂度自适应

根据目标页数自动调整流程粒度：

| 规模 | 页数 | 调研 | 搜索 | 策划 | 生成 |
|------|------|------|------|------|------|
| **轻量** | <= 8 页 | 3 题精简版（场景+受众+补充信息） | 3-5 个查询 | Step 3 可与 Step 4 合并一步完成 | 逐页生成 |
| **标准** | 9-18 页 | 完整 7 题 | 8-12 个查询 | 完整流程 | 按 Part 分批，每批 3-5 页 |
| **大型** | > 18 页 | 完整 7 题 | 10-15 个查询 | 完整流程 | 按 Part 分批，每批 3-5 页，批间确认 |

---

## 断点恢复
> 工作流是无状态的。中断后，主 Agent 扫描磁盘上已有产物，自动推断恢复点。

### 恢复逻辑

```python
def find_recovery_point(run_dir: Path) -> str:
    """扫描已有产物，确定恢复点。"""
    milestones = [
        ("presentation-svg.pptx", "P5-SVG完成"),
        ("presentation-png.pptx", "P5-PNG完成"),
        ("png/slide-*.png", "P4-VQA完成"),
        ("slides/slide-*.html", "P4-页面完成"),
        ("style.json", "P3.5-风格锁定"),
        ("outline.txt", "P3-大纲完成"),
        ("search.txt", "P2-资料搜集完成"),
        ("requirements-interview.txt", "P1-需求确认完成"),
    ]
    for pattern, step in reversed(milestones):
        matches = list(run_dir.glob(pattern))
        if matches:
            return step
    return "P0-从头开始"
```

### 恢复规则

| 规则 | 说明 |
|------|------|
| **无状态文件** | 工作流不依赖任何进度状态文件 |
| **扫描磁盘产物** | 恢复点由磁盘已有文件推断 |
| **部分完成正常** | 只要存在任意一页 HTML = 该页 P4 已完成 |
| **Agent 决定** | 主 Agent 根据扫描结果决定调度哪些 Subagent |
| **不回滚** | 恢复时绝不删除已写入的产物 |

### 产物存在 = 里程碑达成

| 产物 | 里程碑 |
|------|--------|
| `requirements-interview.txt` | P1 完成 |
| `search.txt` | P2 完成 |
| `outline.txt` | P3 完成 |
| `style.json` | P3.5 风格锁定 |
| `slides/slide-N.html`（任意） | P4 页面生成中 |
| `png/slide-N.png`（全部） | P4 视觉 QA 完成 |
| `presentation-svg.pptx` | P5 SVG 导出完成 |
| `presentation-png.pptx` | P5 PNG 导出完成 |

---

## Subagent 调度表（Subagent Dispatch）
> 各阶段独立 Subagent，避免 Context 互染。每个 Subagent 只携带自己阶段的信息。

### Subagent 架构

```
主 Agent（决策 + 调度）
    │
    ├── ResearchAgent ──→ search.txt
    │       模型：必须传 --model 参数
    │
    ├── OutlineAgent ──→ outline.txt
    │       模型：必须传 --model 参数
    │
    ├── StyleAgent ──→ style.json
    │       模型：必须传 --model 参数
    │
    ├── PlanningAgent ──→ planning-N.json（每页）
    │       模型：必须传 --model 参数
    │
    ├── PageAgent-1 ──→ slide-1.html（并行）
    ├── PageAgent-2 ──→ slide-2.html（并行）
    │         ...（全部页面并行）
    └── PageAgent-N ──→ slide-N.html（并行）
        模型：每个 PageAgent 必须传 --model 参数
主 Agent ← 所有 Subagent 完成 ← Step 6 后处理
```

### Subagent 规则

| 规则 | 说明 |
|------|------|
| **必须指定 --model** | 每个 Subagent 必须传 --model 参数，禁止默认回退 |
| **Context 隔离** | 每个 Subagent 只读写自己阶段的产物 |
| **失败隔离** | 单个 Subagent 失败不影响其他 Subagent |
| **失败重试** | 失败 Subagent 最多重试 2 次，失败超过次数则上报主 Agent |

### 产物命名规范

| 产物 | 文件名 |
|------|--------|
| 需求访谈 | `requirements-interview.txt` |
| 资料搜集 | `search.txt` |
| 大纲 | `outline.txt` |
| 风格定义 | `style.json` |
| 策划稿 | `planning-N.json`（N = 页码）|
| 设计稿 | `slides/slide-N.html` |
| 截图 | `slides/slide-N.png` |
| SVG | `svg/slide-N.svg` |

---


## 6 步 Pipeline

### Step 1: 需求调研 [STOP -- 禁止跳过]

> **禁止跳过。** 无论主题多简单，都必须提问并等用户回复后才能继续。不替用户做决定。

**执行**：使用 `references/prompts.md` Prompt #1
1. 搜索主题背景资料（3-5 条）
2. 根据复杂度选择完整 7 题或精简 3 题，一次性发给用户
3. **等待用户回复**（阻断点）
4. 整理为需求 JSON

**7 题三层递进结构**（轻量模式只问第 1、2、7 题）：

| 层级 | 问题 | 决定什么 |
|------|------|---------|
| 场景层 | 1. 演示场景（现场/自阅/培训） | 信息密度和视觉风格 |
| 场景层 | 2. 核心受众（动态生成画像） | 专业深度和说服策略 |
| 场景层 | 3. 期望行动（决策/理解/执行/改变认知） | 内容编排的最终导向 |
| 内容层 | 4. 叙事结构（问题->方案/科普/对比/时间线） | 大纲骨架逻辑 |
| 内容层 | 5. 内容侧重（搜索结果动态生成，可多选） | 各 Part 主题权重 |
| 内容层 | 6. 说服力要素（数据/案例/权威/方法，可多选） | 卡片内容类型偏好 |
| 执行层 | 7. 补充信息（演讲人/品牌色/必含/必避/页数/配图偏好） | 具体执行细节 |

**产物**：需求 JSON（topic + requirements）

---

### Step 2: 资料搜集

> 盘点所有信息获取能力，全部用上。

**执行**：
1. 根据主题规划查询（数量参考复杂度表）
2. 用所有可用的信息获取工具并行搜索
3. 每组结果摘要总结

**产物**：搜索结果集合 JSON

---

### Step 3: 大纲策划

**执行**：使用 `references/prompts.md` Prompt #2（大纲架构师 v2.0）

**方法论**：金字塔原理 -- 结论先行、以上统下、归类分组、逻辑递进

**自检**：页数符合要求 / 每 part >= 2 页 / 要点有数据支撑

**产物**：`[PPT_OUTLINE]` JSON

---

### Step 4: 内容分配 + 策划稿 [禁止跳过 -- 必须等用户确认大纲后执行]

> 将内容分配和策划稿生成合为一步。在思考每页应该放什么内容的同时，决定布局和卡片类型，更自然高效。

**执行**：使用 `references/prompts.md` Prompt #3（内容分配与策划稿）

**要点**：
- 将搜索素材精准映射到每页
- 为每页设计多层次内容结构（主卡片 40-100 字 + 数据亮点 + 辅助要点）
- 同时确定 page_type / layout_hint / cards[] 结构
- **每个内容页至少 3 张卡片 + 2 种 card_type + 1 张 data 卡片**
- 布局选择参考 `references/bento-grid.md` 的决策矩阵

向用户展示策划稿概览，建议等用户确认后再进入 Step 5。

**产物**：每页策划卡 JSON 数组 -> 保存为 `OUTPUT_DIR/planning.json`

---

### Step 5: 风格决策 + 设计稿生成

分三个子步骤，**顺序不可颠倒**：

#### 5a. 风格决策

**执行**：阅读 `references/style-system.md`，选择或推断风格

根据主题关键词匹配 16 种预置风格之一（暗黑科技 / 小米橙 / 蓝白商务 / 朱红宫墙 / 清新自然 / 紫金奢华 / 极简灰白 / 活力彩虹 / 渐变蓝 / 暖阳夕照 / 北欧极简 / 赛博朋克 / 优雅金 / 深海蓝 / 复古胶片 / 稳重蓝），详细匹配规则和完整 JSON 定义见 `references/style-system.md`。

**产物**：风格定义 JSON -> 保存为 `OUTPUT_DIR/style.json`

#### 5b. 智能配图 [根据 Step 1 第 7 题答案执行]

> 如果 Step 1 用户选择"不需要配图"，跳过本节全部内容。

**Step 1 答案路由**：

| Step 1 答案 | 执行动作 |
|-------------|---------|
| "用户提供图片" | 使用用户提供路径的图片 |
| "AI 生成" | 调用 image_generate 工具 |
| "Unsplash" | 调用 Unsplash API |

##### 配图时机

在生成每页 HTML **之前**，先为该页生成配图。每页至少 1 张（封面页、章节封面必须有），生成后保存到 `OUTPUT_DIR/images/`。

**降级链路**（自动降级，无需再次询问用户）：

```
AI 生成（image_generate）
  └─ 工具可用 → 生成图片
  └─ 工具不可用/失败 → Unsplash API
                        └─ Key 已配置 → 搜索获取
                        └─ Key 未配置/失败 → 纯 CSS 装饰降级

用户提供图片
  └─ 路径有效且语义匹配 → 使用该图片
  └─ 路径无效/语义不匹配 → 降级 Unsplash 或 CSS 装饰

Unsplash
  └─ UNSPLASH_ACCESS_KEY 已配置 → 调用 API
  └─ Key 未配置/失败 → 纯 CSS 装饰降级
```

**按页面类型的图片数量**：

| 页面类型 | 需要配图时 | 不需要时 |
|---------|----------|---------|
| 封面页 | **必须有** | 纯 CSS 装饰 |
| 章节封面 | **必须有** | 纯 CSS 装饰 |
| 内容页 | 每页可选 1 张 | 无图 |
| 结束页 | 可选 | 纯 CSS 装饰 |

**产物**：`OUTPUT_DIR/images/` 下的配图文件（如有）

##### image_generate 提示词构造公式

提示词必须同时满足 **4 个维度**，按以下公式组装：

[内容主题] + [视觉风格] + [画面构图] + [技术约束]

| 维度 | 说明 | 示例 |
|------|------|------|
| 内容主题 | 从该页策划稿 JSON 的核心概念提炼，具体到场景/对象 | "DMSO molecular purification process, crystallization flask with clear liquid" |
| 视觉风格 | 与 style.json 的配色方案和情感基调对齐 | 暗黑科技 -> "deep blue dark tech background, subtle cyan glow, futuristic" |
| 画面构图 | 根据图片在页面中的放置方式决定 | 右侧半透明 -> "clean composition, main subject on left, fade to transparent on right" |
| 技术约束 | 固定后缀，确保输出质量 | "no text, no watermark, high quality, professional illustration" |

##### 风格与配图关键词对应

| PPT 风格 | 配图风格关键词 |
|---------|--------------|
| 暗黑科技 | dark tech background, neon glow, futuristic, digital, cyber |
| 小米橙 | minimal dark background, warm orange accent, clean product shot, modern |
| 蓝白商务 | clean professional, light blue, corporate, minimal, bright |
| 朱红宫墙 | traditional Chinese, elegant red gold, ink painting, cultural |
| 清新自然 | fresh green, organic, nature, soft light, watercolor |
| 紫金奢华 | luxury, purple gold, premium, elegant, metallic |
| 极简灰白 | minimal, grayscale, clean, geometric, academic |
| 活力彩虹 | colorful, vibrant, energetic, playful, gradient, pop art |
| 渐变蓝 | gradient blue, tech, futuristic, clean, digital, professional |
| 暖阳夕照 | warm orange, sunset, lifestyle, travel, food, cozy lighting |
| 北欧极简 | minimal, white, clean, scandinavian, lifestyle, bright |
| 赛博朋克 | neon, cyber, dark, futuristic, gaming, vibrant, holographic |
| 优雅金 | gold, luxury, elegant, premium, metallic, champagne |
| 深海蓝 | ocean blue, deep sea, marine, aquatic, serene, gradient |
| 复古胶片 | vintage, film grain, retro, warm tones, nostalgic, cinematic |
| 稳重蓝 | corporate, professional, blue, business, formal, trustworthy |

##### 按页面类型调整

| 页面类型 | 图片特征 | Prompt 额外关键词 |
|---------|---------|-----------------|
| 封面页 | 主题概览，视觉冲击 | "hero image, wide composition, dramatic lighting" |
| 章节封面 | 该章主题的象征性视觉 | "symbolic, conceptual, centered composition" |
| 内容页 | 辅助说明，不喧宾夺主 | "supporting illustration, subtle, background-suitable" |
| 数据页 | 抽象数据可视化氛围 | "abstract data visualization, flowing lines, tech" |

##### 禁止事项
- 禁止图片中出现文字（AI 生成的文字质量差）
- 禁止与页面配色冲突的颜色（暗色主题配暗色图，亮色主题配亮色图）
- 禁止与内容无关的装饰图（每张图必须与该页内容有语义关联）
- 禁止重复使用相同 prompt（每页图片必须独特）

**产物**：`OUTPUT_DIR/images/` 下的配图文件

#### 5c. PageAgent 并行生成

> **禁止跳过策划稿直接生成。** 每页必须先有 Step 4 的结构 JSON。

**并行调度**：所有页面通过 PageAgent-N 子代理并行生成，每个 PageAgent 只负责一页。

**并行策略**：

| 规模 | 页数 | 策略 |
|------|------|------|
| **小型** | <= 5 页 | 全部页面并行 |
| **标准** | 6-18 页 | 全部页面并行（独立）|
| **大型** | > 18 页 | 按 Part 并行，Part 内全部并行 |

**PageAgent 工作流程**：
```
PageAgent-N
    │
    ├── 1. 读取 planning-N.json
    ├── 2. 读取 style.json
    ├── 3. 读取 images/planning-N.png（如果有）
    ├── 4. 生成 slide-N.html
    ├── 5. DOM 自审（溢出/伪元素/硬编码检查）
    └── 6. 输出：--- PAGE N COMPLETE ---
```

**失败处理**：
- 单页失败不影响其他页面
- 失败页进入 PagePatchAgent 重试队列（最多 2 次重试）
- 主 Agent 等待所有 PageAgent 完成后进入 Step 6

**每页 Prompt 组装公式**：
```
Prompt #4 模板
+ 风格定义 JSON（5a 产物）[必须]
+ 该页策划稿 JSON（Step 4 产物，含 cards[]/card_type/position/layout_hint）[必须]
+ 该页内容文本（Step 4 产物）[必须]
+ 配图路径（5b 产物）[可选 -- 无配图时省略 IMAGE_INFO 块]
```

**核心设计约束**（完整清单见 Prompt #4 内部）：
- 画布 1280x720px，overflow:hidden
- 所有颜色通过 CSS 变量引用，禁止硬编码
- 凡视觉可见元素必须是真实 DOM 节点，图形优先用内联 SVG
- 禁止 `::before`/`::after` 伪元素用于视觉装饰、禁止 `conic-gradient`、禁止 CSS border 三角形
- 配图融入设计：渐隐融合/色调蒙版/氛围底图/裁切视窗/圆形裁切（技法详见 Prompt #4）

**跨页视觉叙事**：

| 策略 | 规则 | 原因 |
|------|------|------|
| **密度交替** | 高密度页后跟低密度页 | 避免视觉疲劳 |
| **章节色彩递进** | 每个 Part 使用不同 accent 主色 | 无意识感知章节切换 |
| **封面-结尾呼应** | 结束页呼应封面页 | 完整闭环感 |
| **渐进揭示** | 复杂度逐页递增 | 引导观众逐步深入 |

**产物**：每页一个 HTML 文件 -> `OUTPUT_DIR/slides/`

---

### Step 6: 后处理 [必做 -- HTML 生成完后立即执行]

> **禁止跳过，必须执行。** HTML 生成完后必须立即执行以下管线步骤。

```
slides/*.html
  ├── html_packager.py --> preview.html
  ├── html2svg.py --> svg/*.svg --> svg2pptx.py --> presentation-svg.pptx
  └── html2png.py --> png/*.png --> png2pptx.py --> presentation-png.pptx
```

**依赖检查**（首次运行自动执行）：
```bash
pip install python-pptx lxml Pillow 2>/dev/null
npm install puppeteer dom-to-svg 2>/dev/null
```

**依次执行**：

1. **合并预览** -- 运行 `html_packager.py`
   ```bash
   python SKILL_DIR/scripts/html_packager.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/preview.html
   ```

2. **SVG 转换** -- 运行 `html2svg.py`（DOM 直接转 SVG，保留 `<text>` 可编辑）
   > **重要**：HTML 设计稿必须遵守 `references/pipeline-compat.md` 中的管线兼容性规则，否则转换后会出现元素丢失、位置错位等问题。
   ```bash
   python SKILL_DIR/scripts/html2svg.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/svg/
   ```

   底层用 dom-to-svg（自动安装），首次运行会 esbuild 打包。
   **降级**：如果 Node.js 不可用或 dom-to-svg 安装失败，跳过 SVG 分支。

3. **SVG PPTX 导出** -- 运行 `svg2pptx.py`（OOXML 原生 SVG 嵌入，PPT 365 可编辑）
   ```bash
   python SKILL_DIR/scripts/svg2pptx.py OUTPUT_DIR/svg/ -o OUTPUT_DIR/presentation-svg.pptx --html-dir OUTPUT_DIR/slides/
   ```

   PPT 365 中右键图片 -> "转换为形状" 即可编辑文字和形状。

4. **PNG 截图** -- 运行 `html2png.py`（Puppeteer 截图，支持并行）
   ```bash
   python SKILL_DIR/scripts/html2png.py OUTPUT_DIR/slides/ -o OUTPUT_DIR/png/ --concurrency 4
   ```

   使用 Puppeteer 进行像素级截图，并发数控制并行线程数。
   **降级**：如果 Node.js/Puppeteer 不可用，跳过 PNG 分支。

5. **PNG PPTX 导出** -- 运行 `png2pptx.py`（PNG 作为背景，跨平台 100% 视觉还原）
   ```bash
   python SKILL_DIR/scripts/png2pptx.py OUTPUT_DIR/png/ -o OUTPUT_DIR/presentation-png.pptx
   ```

   PNG 填满每页幻灯片作为背景，文字不可编辑但视觉效果像素级还原。

6. **通知用户** -- 告知产物位置和使用方式：
   - `preview.html` -- 浏览器打开即可翻页预览
   - `presentation-svg.pptx` -- SVG 矢量 PPTX（文字可编辑，PPT 365 "转换为形状"）
   - `presentation-png.pptx` -- PNG 像素 PPTX（视觉效果完美，文字不可编辑）
   - `svg/` -- 每张 SVG 也可单独拖入 PPT
   - `png/` -- PNG 截图（用于 Visual QA 参考）
   - **如果 SVG 分支被降级跳过**，说明原因并告知用户可手动安装 Node.js 后重新运行
   - **如果 PNG 分支被降级跳过**，说明 PNG 截图仅用于 Visual QA

**产物**：preview.html + svg/*.svg + png/*.png + presentation-svg.pptx + presentation-png.pptx

---

## 输出目录结构

```
ppt-output/
  slides/                    # 每页 HTML
  svg/                       # 矢量 SVG（可导入 PPT 编辑）
  png/                       # PNG 截图（用于 Visual QA + PNG PPTX 导出）
  images/                    # AI 配图
  preview.html               # 可翻页预览
  presentation-svg.pptx      # SVG 矢量 PPTX（文字可编辑）
  presentation-png.pptx      # PNG 像素 PPTX（视觉效果完美）
  outline.json               # 大纲
  planning.json              # 策划稿
  style.json                # 风格定义
```

---

## 质量自检

| 维度 | 检查项 |
|------|-------|
| 内容 | 每页 >= 2 信息卡片 / >= 60% 内容页含数据 / 章节有递进 |
| 视觉 | 全局风格一致 / 配图风格统一 / 卡片不重叠 / 文字不溢出 |
| 技术 | CSS 变量统一 / SVG 友好约束遵守 / HTML 可被 Puppeteer 渲染 / `pipeline-compat.md` 禁止清单检查 |

---

## Reference 文件索引

| 文件 | 何时阅读 | 关键内容 |
|------|---------|---------|
| `references/prompts.md` | 每步生成前 | 5 套 Prompt 模板（调研/大纲/策划/设计/备注）|
| `references/style-system.md` | Step 5a | 16 种预置风格 + CSS 变量 + 风格 JSON 模型 |
| `references/bento-grid.md` | Step 5c | 7 种布局 + 12 种卡片类型 + 决策矩阵 |
| `references/method.md` | 初次了解 | 核心理念与方法论 |
| `references/pipeline-compat.md` | **Step 5c 设计稿生成时** | CSS 禁止清单 + 图片路径 + 字号混排 + SVG text + 环形图 + svg2pptx 注意事项 |
