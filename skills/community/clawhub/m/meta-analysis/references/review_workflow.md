# Systematic Review Workflow / 系统评价流程辅助

> **Scope / 定位**：本技能只承接系统综述中**可确定性计算或绘图**的环节。
> 全面文献检索 → 交 `ct-literature`；综述正文撰写 → 交 `ct-csr`；本技能不重复造轮子。
>
> **实证基线（2026-08-30）**：本文所有 metagear 结论均经本地 R 4.6.1 + metagear 0.7
> 逐函数实测，非文档推断。历史版本中的 7 段示例代码（`prisma_flow` / `export` /
> `screen_titles` / `retrieve_pdf` / `retrieve_pmid` / `extract_digit` / `impute_ml`）
> **函数名系虚构，metagear 中不存在**，已全部删除。

---

## 0. Capability Boundary / 能力边界（先看这一节）

### 0.1 Supported / 本文件提供

| 环节 | 支持 | 载体 |
|---|---|---|
| PRISMA 2020 流程图 | ✅ 投稿级 | task `prisma_flow`（`metagear::plot_PRISMA`，矢量 SVG） |
| PRISMA 2020 检查表（27 项） | ✅ | task `prisma_checklist` |
| 偏倚风险图（traffic-light / summary bar） | ✅ | task `rob2` / `rob_summary` |
| GRADE 证据分级 | ✅ | task `grade` |
| 文献筛选（纳入/排除判定） | ✅ | **agent 行为层**（对话中逐条判定，见 §2） |
| 数据提取表 | ⚠️ 模板 | §3 提供字段模板；引擎不存表，由 agent 在对话中维护 |
| 全面文献检索 | ❌ | 转 `ct-literature`（含 `screen_prisma.py`） |
| 综述正文撰写 | ❌ | 转 `ct-csr` |

### 0.2 metagear 中**不接入**的能力（勿向用户承诺）

| metagear 函数 | 实测结果 | 为何不接 |
|---|---|---|
| `abstract_screener` | 本地可用（Tcl/Tk GUI），coze Linux 无 X11 | 无头容器跑不了；已由 §2 agent 行为层替代 |
| `figure_*`（图表数字化，15 个） | 需 EBImage（仅 Bioconductor，不在 CRAN），且安装时**交互式询问** | 批处理会卡死；缺依赖即不可用 |
| `PDF_download` | 实测 404（期刊有墙） | 外部服务不可靠 |
| `scrape_bibliography` | WoS 接口 HTTP 500，已失效 | 外部服务已死 |
| `impute_missingness` | **只返回 4×3 缺失率汇总表，不做实际插补** | 名不副实；用户要插补时勿推荐此函数 |
| `random_d` / `random_OR` / `covariance_commonControl` | 签名可用，但与本技能需求错位 | 非综述流程必需 |

> ⚠️ 上表任一函数若出现在 agent 回答中，即为幻觉——本技能不提供这些入口。

---

## 1. PRISMA 2020 Flow Diagram / PRISMA 流程图

### 1.1 走技能 task（推荐）

直接说人话即可，`classify.py` 会路由到 `prisma_flow`（无需用户懂 R）：

> 检索到 1200 篇，去重 140 篇，筛查 1140 篇，排除 250 篇，
> 全文评估 890 篇，排除 114 篇，最终纳入 42 项研究 —— 生成 PRISMA 流程图

### 1.2 Parameters / 参数

| 参数 | 含义 | 默认 |
|---|---|---|
| `records` | 数据库检索到的记录数 | 0 |
| `other_sources` | 其他来源（手工检索等）记录数 | 0（`>0` 时才出该分支） |
| `duplicates` | 去重移除数 | 0 |
| `screened` | 初筛（标题/摘要）记录数 | 0 |
| `excluded_title` | 初筛排除数 | 0 |
| `assessed` | 全文评估数 | 0 |
| `excluded_elig` | 全文排除数（需附理由） | 0 |
| `included` | 最终纳入研究数 | 0 |
| `reports` | 纳入报告的报告数 | 0（与 `included` 不等时才单列） |
| `design` | 配色方案，见 §1.3 | `cinnamonMint` |
| `colWidth` | 阶段文字换行宽度 | 30 |
| `excludeDistance` | 排除分支的水平间距 | 0.8 |
| `fig_width` / `fig_height` | 画布英寸 | 7 / 9（竖版） |

### 1.3 Design 配色方案（仅 7 个合法值）

`classic`（metagear 原生默认）· `cinnamonMint` · `sunSplash` · `pomegranate` ·
`vintage` · `grey` · `greyMono`

- 技能默认 `cinnamonMint`：橙 → 黄 → 绿渐变，接近 PRISMA 2020 statement 官方推荐配色。
- 传非法值（如 `mintChocolate`）由 `plot_prisma_flow` 主动校验并回落到 `cinnamonMint`，
  不依赖 metagear 的 warning（它会静默回落到 `classic`，与预期不符）。

### 1.4 Reproducible R Script / 可复现脚本

```r
library(metagear)

pv <- c(
  "START_PHASE: Identification",
  "Records identified from databases (n = 1200)",
  "Records identified from other sources (n = 80)",
  "EXCLUDE_PHASE: Duplicates removed (n = 140)",
  "START_PHASE: Screening",
  "Records screened (n = 1140)",
  "EXCLUDE_PHASE: Records excluded (n = 250)",
  "Full-text articles assessed for eligibility (n = 890)",
  "EXCLUDE_PHASE: Full-text excluded, with reasons (n = 114)",
  "Studies included in the meta-analysis (n = 42)"
)

svg("prisma_flow.svg", width = 7, height = 9)
metagear::plot_PRISMA(pv, design = "cinnamonMint")
dev.off()
```

**向量语法约定**（metagear 原生接口，技能层已封装，此处仅供排错）：

- `START_PHASE: xxx` = 阶段标题行（如 Identification / Screening），**不是**一个真实数据节点；
- `EXCLUDE_PHASE: xxx` = 右侧排除分支；
- 其余行 = 主流程节点，按书写顺序自上而下排列；
- 输出为纯 grid 绘图 → **矢量、零 GUI 依赖**，coze 无头 Linux 容器可直接跑；
- 同一设备内不要重复调用（metagear 不自动 `grid.newpage()`，会叠加绘制）。

### 1.5 计数来源与人工补齐（与 ct-literature 衔接）

> 本技能 `prisma_flow` 需要 **9 个计数字段**（见 §1.2）。它们**不能**全部由
> `ct-literature` 自动产出——检索归 ct-literature、绘图归本技能，分工正确，
> 但**接缝是裸的**：两套字段名不同、且部分语义错位。桥接脚本
> `scripts/prisma_bridge.py` 是两者间**唯一** sanctioned 胶水，已处理好下述映射。

**9 字段来源分级**（决定哪些能自动填、哪些必须人工）：

| `prisma_flow` 字段 | 来源 | 说明 |
|---|---|---|
| `records` | 自动（派生） | ct-literature `identified_records` + `duplicates_removed`（= 去重前原始检索总数） |
| `duplicates` | 自动 / 人工 | ct-literature `duplicates_removed`（2026-08-30 起由 `normalize.merge_with_stats` 输出）；若旧版未报告则标 `[MANUAL]` |
| `screened` | 自动 | ct-literature `identified_records`（去重后总数，全部经标题/摘要初筛） |
| `excluded_title` | 自动 | ct-literature `excluded_records`（标题/摘要规则排除数） |
| `other_sources` | **人工** | 手工检索、追溯参考文献等其他来源，引擎无法获知 |
| `assessed` | **人工** | 全文评估数；ct-literature `included_records`（机器初筛通过数）**仅作参考初值**，须人工确认 |
| `excluded_elig` | **人工** | 全文排除数（需附理由）；需获取 PDF 全文，自动化结构性不可达（见 §0.2） |
| `included` | **人工** | 最终纳入 Meta 分析的研究数 |
| `reports` | **人工** | 纳入研究的报告数（与 `included` 不等时才单列） |

⚠️ **最危险的一类：语义错位，不是缺失**。
ct-literature 的 `included_records`（机器初筛通过数）与 PRISMA 的 `included`（最终纳入数）
**含义不同**。若直接映射，会静默产出一张数字齐全、方法学错误的流程图。
**`included` 绝不接受机器初筛数**；`assessed` 可用其作参考初值但必须人工确认。
这正是 §0.2 所述「不报错、给错答案」的典型陷阱。

**推荐工作流**：

```
ct-literature --topic "..." --prisma
   ↓  .merged.json（含 4 键 + duplicates_removed + 每篇 prisma_stage/reason）
meta-analysis/scripts/prisma_bridge.py --merged .merged.json \
   --set assessed=890 --set excluded_elig=114 --set included=42 --set other_sources=80
   ↓  prisma_flow_request.json（task=prisma_flow 请求信封，params 已填 9 字段）
meta-analysis 「按这份参数生成 PRISMA 流程图」
```

桥接脚本会打印**逐字段来源表**与**强制声明**：
「机器初筛，非人工终审 / MACHINE SCREEN — NOT A SUBSTITUTE FOR HUMAN FINAL REVIEW」，
并对仍为 0 的 `[MANUAL]` 字段提示需人工补全后才能出图。

---

## 2. AI 辅助文献筛选（agent 行为层，2026-08-20 起）

> 替代 metagear 本地 GUI：由 agent 在对话中按纳入/排除标准逐条判定标题/摘要。
> **纯 agent 行为，无引擎/脚本依赖**，因此不受 coze 无 X11 的限制。

**流程**：

1. 用户提供标题/摘要列表（文本、CSV，或经 `adapters/pdf_fetch.py` 收集的文献清单）。
2. agent 与用户确认纳入/排除标准（PICO 维度）。
3. 逐条判定，输出统一筛选表：

| 序号 | 标题 | 作者/年 | 判定 | 理由（对照标准） | 置信度 |
|---|---|---|---|---|---|
| 1 | ... | ... | Include / Exclude / Maybe | ... | 高/中/低 |

4. Maybe 项进入第二轮人工复核；Exclude 项须给可追溯理由。
5. 纳入清单可导出 CSV，供后续数据提取与 Meta 分析。

**规则**：

- 判定必须对照用户确认的纳入/排除标准，**不臆造标准**；标准未覆盖的维度标注"待确认"。
- 置信度低或证据边界模糊 → 一律标 Maybe，不硬判。
- 批量处理时每批 ≤50 条，防止上下文超限；分批间保持判定一致性。

**双筛选与一致性**：两名评价者独立判定时，对 Include/Exclude 的一致率计算 Cohen's kappa；
kappa < 0.60 视为一致性不足，需讨论分歧后再进入全文阶段。

---

## 3. Data Extraction Table / 数据提取表

> ⚠️ 引擎不存储提取表，由 agent 在对话中维护并导出 CSV。
> 以下为最小字段集，按研究设计取用；不要为"看起来完整"而增设无来源字段。

| 字段组 | 字段 |
|---|---|
| 标识 | Study ID、第一作者、发表年、国家、资助来源 |
| 设计 | 研究设计（RCT / 队列 / 病例对照）、样本量（试验组/对照组）、随访时长 |
| 人群 | 纳入标准摘要、年龄（均数±SD 或中位数）、性别比例 |
| 干预/暴露 | 名称、剂量、疗程、对照类型 |
| 结局 | 结局名称、测量时点、效应量类型（二分类/连续/生存） |
| 二分类 | 事件数/总数（试验组、对照组） |
| 连续 | 均数±SD、样本量（试验组、对照组） |
| 生存 | HR 及其 95% CI（或 logHR ± SE） |
| 偏倚风险 | RoB 2 / ROBINS-I 各域判定（供 `rob2` task 直接出图） |

**提取纪律**：

- 每个数值须能追溯到原文页码/表号；无法定位的标 `NR`（not reported），**不臆造**。
- 同一结局多个时点 → 明确主时点，其余作为次要分析。
- 单位不统一（如 mg vs μg）→ 先换算并在表中记录原单位。

---

## 4. Missing Data / 缺失数据

**如实说明**：metagear 的 `impute_missingness()` **不做插补**——它只返回一张
按列统计缺失率的汇总表（`n_missing` / `percent_missing`），这是 2026-08-30 实测结论。
不要把它当作插补工具推荐给用户。

| 缺失情形 | 处理方式 |
|---|---|
| 缺 SD，有 95% CI | 由 CI 宽度反推：`SD ≈ (上限−下限) / (2×1.96) × √n` |
| 缺 SD，有 SE | `SD = SE × √n` |
| 缺 SD，有 t 值或 p 值 | 反推 SE 后同上 |
| 缺均数，仅有中位数 | 通常不做转换；作为敏感性分析说明，主分析剔除 |
| 结局数据完全缺失 | 联系作者；未果则在偏倚风险"缺失数据"域降级，不做插补 |

**纪律**：任何换算须在报告中写明公式与假设；由换算得来的数据应在敏感性分析中剔除后复跑，
确认合并效应量方向不变。

---

## 5. References / 引用

- R metagear package (v0.7, Lajeunesse 2016): https://github.com/cran/metagear
  — Lajeunesse MJ. (2016) *Methods in Ecology and Evolution*, 7:323-330.
- PRISMA 2020 statement: Page MJ, et al. (2021). *BMJ*, 372, n71.
- RoB 2 tool: Sterne JAC, et al. (2019). *BMJ*, 366, l4898.
- GRADE handbook: https://gdt.gradepro.org/app/handbook/handbook.html
