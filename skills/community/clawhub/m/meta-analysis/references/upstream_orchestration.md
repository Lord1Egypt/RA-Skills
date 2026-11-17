# Upstream Orchestration / 上游编排（检索 → 筛选 → 提取 → 分析）

> **定位 / Scope**：本文件把 meta-analysis 从「只算合并效应量」升级为「覆盖 Meta 分析全链路的编排器」。
> 上游三段（方向判断 / 文献检索整理 / 筛选清理）尽量复用现有模块与 `ct-literature`；
> 新增的唯一能力是**数据提取助手**（LLM 草稿 + 人工核验闸），把提取结果无缝接入现有计算轨。
>
> **实证基线（2026-08-30）**：本文件所有脚本引用均经实际存在文件核对（见下方 `脚本清单`），
> 非文档推断。各模块的「能/不能」边界以 `review_workflow.md`、`prisma_bridge.py`、
> `topic-selection.md` 的实测结论为准。

---

## 0. 能力边界总览 / Capability boundary

| 环节 | 谁来做 | 载体 | 是否新增 |
|---|---|---|---|
| ① 方向判断 | **meta-analysis 本技能** | `topic-selection.md` + `adapters/literature_probe.py`（Europe PMC 去重探针）+ `scripts/generate_topic_report.py` | 已有，补「委托 ct-literature 全面检索」 |
| ② 文献检索整理 | **ct-literature**（委托） | `ct_literature.py` + 6 个 fetch adapter，归一化去重，输出 `.merged.json` / Excel / HTML | 已有，meta 侧只编排 |
| ③ 文献清理（初筛） | **ct-literature 规则筛 + meta agent 层** | ct-literature `screen_prisma.py`；`review_workflow.md §2` agent 逐条判标题/摘要；`prisma_bridge.py` 桥到 PRISMA 9 字段 | 已有，桥接已就绪 |
| ④ 数据提取 | **LLM 草稿 + 人工核验**（meta 新增） | `scripts/extract_assist.py` + `scripts/extraction_guard.py` | **新增** |
| ⑤ Meta 计算 | **meta-analysis 计算轨（现有）** | `scripts/run_meta.py` → coze R 引擎 | 已有，仅加抽取核验闸 |

> ⚠️ **全文级 eligibility 排除、效应量抽取精度，属结构性不可自动化**（PDF 有墙、
> 系统综述要求双人独立抽取+仲裁）。自动化只能到「标题/摘要初筛」与「抽取草稿」，
> 全文与抽取必须人工。这是方法学硬约束，不是工程缺憾。

---

## 1. 编排流程 / Pipeline

```
① 方向判断 (meta-analysis 本技能)
   topic-selection.md → literature_probe.py (Cochrane/PubMed 探针)
   → 如需全面检索，委托 ct-literature（见 §2）
   → generate_topic_report.py 出 5 阶段 11 节报告
        │  verdict: recommend / hold / not_recommended
        ▼
② 文献检索整理 (委托 ct-literature)
   ct_literature.py --topic "..." --online --prisma --run
   → .merged.json（含 prisma 块：identified/excluded/included_records + duplicates_removed）
        │
        ▼
③ 文献清理 (ct-literature 规则筛 + agent 层)
   - 机器初筛：ct-literature screen_prisma.py（标题/摘要规则）
   - 人工判定：review_workflow.md §2 agent 逐条判 Include/Exclude/Maybe
   - PRISMA 图：prisma_bridge.py 桥 → meta-analysis prisma_flow task
        │  ⚠️ 见 §4 接缝陷阱
        ▼
④ 数据提取 (LLM 草稿 + 人工核验)【新增】
   extract_assist.py scaffold → agent/LLM 读全文提草稿 → 填 CSV
   → extract_assist.py validate
   → 人工逐行核验（来源页码/表号）→ extract_assist.py stamp --confirm
        │  verified_by_human=YES
        ▼
⑤ Meta 计算 (现有计算轨)
   run_meta.py --data <提取CSV> --out-dir <工作区>
   （extraction_guard 自动校验 verified_by_human，未核验则拦截）
```

---

## 2. ① 方向判断 → 委托 ct-literature 全面检索

- **本技能侧已有**：`topic-selection.md` 的 4 维评分（临床/可行性/数据/新颖性，任一 ≤2 一票否决）+ R1–R7 交叉检查 + `generate_topic_report.py`，以及**选题门控** `scripts/topic_gate.py`（确定性检测 ct-literature 是否安装并路由）。
- **选题门控（必读）**：进入选题轨第一步先跑 `python scripts/topic_gate.py --topic "<topic>"`：
  - ct-literature **已安装** → 直接调用它做全面检索（见下方命令），其 `.merged.json` 作为 Stage 4 新颖性证据；
  - ct-literature **未安装** → AskUserQuestion 询问「安装后继续 / 简单分析」；选简单分析则直接调 **ct-search 远端服务**（`adapters/ctsearch_client.py search --source europepmc ...`），无需安装 ct-literature；
  - 绝对兜底（ct-search 也不可达）→ 退回 in-skill `adapters/literature_probe.py`（直连 Europe PMC）。
- **补一步委托**：当选题报告需要「全面证据基础」且 ct-literature 已安装时，在 Stage 4 显式调用 ct-literature 做跨库检索，而不是只靠 in-skill 探针：

  ```bash
  python <ct-literature>/scripts/ct_literature.py \
      --topic "osimertinib advanced NSCLC" --review-type meta-analysis \
      --with-europepmc --with-semantic-scholar --year-from 2018 --safety --prisma --run \
      --out-dir ./lit
  ```
  产出的 `lit_report.html` / `lit_report.xlsx` / `.merged.json` 作为选题报告的新颖性证据补充。

- **边界**：PROSPERO 注册库、非英文数据库仍属「引导人工」步骤（ct-literature `--with-prospero` 为保留接口，无 token 时静默跳过，不声称可用）。

---

## 3. ③ 文献清理 → PRISMA 桥接

复用 `scripts/prisma_bridge.py`（ct-literature `.merged.json` → meta-analysis `prisma_flow` 参数的**唯一 sanctioned 胶水**）：

```bash
python scripts/prisma_bridge.py \
    --merged ./lit/.merged.json \
    --set assessed=890 --set excluded_elig=114 --set included=42 --set other_sources=80 \
    --out prisma_flow_request.json
```
随后「按这份参数生成 PRISMA 流程图」即可。桥接脚本会打印逐字段来源表并强制声明
「机器初筛，非人工终审」。

---

## 4. 接缝陷阱 / Seam trap（必读）

> **`included_records`（机器初筛通过数）≠ `included`（人工最终纳入数）。**
> 把 ct-literature 的 `included_records` 直接映射到 PRISMA 的 `included`，会静默产出
> 一张数字齐全、方法学错误的流程图。`prisma_bridge.py` 对 `included` / `assessed` /
> `excluded_elig` 一律标 `[MANUAL]` 强制人工填——**不要绕过**。

同理，④ 数据提取的「纳入研究清单」也**不能**由 `included_records` 自动生成数据行；
必须由人工确认的最终纳入清单驱动。

---

## 5. ④ 数据提取助手【新增】/ Data-extraction assistant

### 5.1 设计原则
- **引擎/coze 不存提取表**（对齐 `review_workflow.md §3`）；本助手只做「结构化 + 校验 + 护栏」。
- **真正的抽取由 agent/LLM 在对话中完成**：读 OA 全文或用户上传 PDF（先转 md/text，见 §7），提出 Type 1/2/3 草稿行。
- **任何无法从原文定位的数值 → 填 `NR`**（not reported），绝不可臆造。
- **未经人工核验，禁止进计算轨**：由 `extraction_guard.py` 在 `run_meta.py` 入口拦截。

### 5.2 工作流

```bash
# 1) 生成空白抽取表（仅含 Type 列，可直接喂 run_meta --data），并写 provenance 同伴文件
#    若已有 Stage3 人工确认的最终纳入清单文件，用 --studies-file 自动预填 study 列（与 --studies 合并去重）
python scripts/extract_assist.py scaffold --type binary --out extracted.binary.csv --studies-file included_studies.json
#    或手动：--studies "Zhang2020,Wang2019"

# 2) agent/LLM 读全文，把效应量填入 extracted.binary.csv（来源页码/表号记在脑子里/备忘录）
#    二分类列：study,n_exp,event_exp,n_ctrl,event_ctrl,year
#    连续型列：study,n_exp,mean_exp,sd_exp,n_ctrl,mean_ctrl,sd_ctrl,year
#    预计算效应量：study,effect_type,effect_size,lower95,upper95,year

# 3) 校验结构 + 数值合理性 + 缺失标记
python scripts/extract_assist.py validate --csv extracted.binary.csv

# 4) 人工逐行核验（对照原文页码/表号）→ 打核验章（必须 --confirm）
python scripts/extract_assist.py stamp --csv extracted.binary.csv --confirm

# 5) 直接计算（extraction_guard 自动放行）
python scripts/run_meta.py --query "pool OR from extracted studies" \
    --data extracted.binary.csv --out-dir <工作区>/meta_analysis
```

### 5.3 守卫语义（extraction_guard.check_verified）
| 情形 | 行为 |
|---|---|
| 非 CSV（内联 `--data-json`） | 跳过（对话内可信构造） |
| CSV 无同伴 `.provenance.json` | 视为人工手搓 CSV，放行（提示） |
| 同伴存在，`verified_by_human=YES` | 放行 |
| 同伴存在，`verified_by_human=NO` | **拦截**，`META_STATUS=unverified_extraction`，退出码 3 |
| `run_meta --trust-data` | 一律放行（用户显式担责兜底，仅用于确认可信的存量/手搓 CSV） |

---

## 6. 支持的 Type / Supported schemas

`extract_assist.py types` 列出全部。与 `data_templates.md` 一一对应：
`binary` / `continuous` / `precomputed`(Type3) / `rate`(Type3b) / `correlation`(Type3c) /
`single_proportion`(Type3d) / `single_mean`(Type3e)。

---

## 7. 全文获取 / Full-text access（责任边界）

- 本技能 **不自动批量抓 PDF**（付费墙；`review_workflow.md §0.2` 实测 `PDF_download` 404）。
- 用户上传 PDF → 按 `data_templates.md §4` 先转 md/text（`scripts/office_to_md.py` 处理 docx/pptx；
  `.pdf` 走环境 pdf 技能；`.doc`/扫描件请用户给文本版），再由 agent/LLM 抽取。
- 仅当用户提供 DOI/PMID 且**显式确认**时，`adapters/pdf_fetch.py` 才去取 OA 全文（opt-in）。

---

## 8. 脚本清单 / Script inventory（均实测存在）

| 脚本 | 角色 |
|---|---|
| `scripts/extract_assist.py` | 数据提取助手：scaffold / validate / stamp / types（**新增**） |
| `scripts/extraction_guard.py` | 抽取人工核验闸（**新增**，被 run_meta 调用） |
| `scripts/run_meta.py` | 计算轨入口（已接入守卫，新增 `--trust-data`） |
| `scripts/prisma_bridge.py` | ct-literature → PRISMA 参数胶水（已有） |
| `scripts/generate_topic_report.py` | 选题报告生成（已有） |
| `adapters/literature_probe.py` | 选题去重探针（已有） |
| `references/topic-selection.md` | 选题评估框架（已有） |
| `references/review_workflow.md` | 系统评价流程（已有，含筛选/提取模板） |
| `references/data_templates.md` | 计算轨输入模板（已有） |
| ct-literature `scripts/ct_literature.py` / `screen_prisma.py` | 检索/去重/初筛（委托） |
