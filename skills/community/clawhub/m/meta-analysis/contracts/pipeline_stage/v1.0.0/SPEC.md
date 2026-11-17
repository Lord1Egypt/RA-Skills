# Meta-Analysis · per-stage Pipeline 契约规格（SPEC）

> 版本：`v1.0.0` ｜ 阶段：Phase 0 设计期草稿
> 定位：把现有「per-task 单次分析」契约升级为「per-stage 全链路管线」契约，支撑
> 本地薄客户端 + coze 编排引擎架构（详见 `../meta_analysis_architecture_proposal.md`）。
> 配套机器可校验 schema 见同目录 `request.schema.json` / `response.schema.json`。
> coze 端权威契约见 `adapters/coze/coze_contract.md`（本规格的 coze 侧草稿同步章节亦在该文件）。

---

## 0. 设计原则

| # | 原则 | 说明 |
|---|---|---|
| P1 | **向后兼容（硬约束）** | 新信封是现有 per-task 契约的**超集**。旧字段 `task/data/params/figure/query_origin/request_id/_debug/probe` 与 `status/stats/figures/warnings/notes/repro` 一律保留。旧 consumer 不升级也能工作；新字段缺失时本地 adapter 走旧 per-task 解析分支。 |
| P2 | **版本化协商** | 信封带 `contract_version`（semver）+ `schema` 标识。`contract_version` 由**本地 adapter 强制写入**；coze 响应必须回写同版本。**major 不一致 → adapter 拒绝并降级**（见 §7）。 |
| P3 | **本地强执红线闸** | `next_human_action.gate` 把「提取核验 / 最终纳入数 / 稿件批准 / 参考核验」等红线闸显式编码，本地 adapter 在渲染前**强执**——coze 无法阻止用户跳过，所以闸门逻辑留在本地（沿用 `extraction_guard.py` 思路扩展）。 |
| P4 | **复用 need_tool 范式** | `tool_cards[]` 直接对齐 `ct-advisor` 的 `need_tool` 执行卡（`need_tool`/`params`/`draft_answer`/`run_id`），本地执行器零改动复用 `handle_need_tool.py` 式逻辑。 |
| P5 | **coze 只回结构化，不下原始全文** | 跨阶段上下文 `stage_context` 只传结构化数值/结论，**不传文献 PDF 全文**（沿用 extract_assist 模式，避免全文外传涉保密/合规）。 |
| P6 | **确定性校验可测** | 所有枚举（stage 意图、human_action 类型、gate、tool_card.sync、stage 状态）均为封闭集合，可被 `test_contract.py` 确定性断言。 |

---

## 1. 信封总览

```
本地 adapter（入站）                         coze 编排引擎
─────────────────────                       ─────────────────
用户提示词 / 上一阶段人工决策
        │  prompt → 合法入参（仅结构化+必填校验，无领域判断）
        ▼
┌──────────────────────────┐  HTTP POST /run  ┌──────────────────────────────┐
│ PipelineStageRequest {    │ ───────────────▶ │ coze 工作流（拥有全部管线智能） │
│   contract_version,       │                  │  · 选题→检索→筛选→提取→计算→撰稿│
│   schema,                 │                  │  · 返回 stage_result           │
│   task/data/params(兼容), │                  │  · next_human_action（下一步）  │
│   pipeline/stage,         │                  │  · tool_cards（需本地 ct-*）   │
│   stage_context           │ ◀─────────────── │                              │
│ }                        │  JSON            │ PipelineStageResponse {        │
└──────────────────────────┘                  │   stage_result,               │
        │  coze 结构化输出 → 用户可读产出（仅渲染，不新增分析）
        ▼                                     │   next_human_action,           │
用户产出（HTML/MD/docx/图）                   │   tool_cards[],                │
                                            │   status/stats/figures(兼容)   │
                                            │ }                            │
                                            └──────────────────────────────┘
```

---

## 2. Request 字段（`PipelineStageRequest`）

信封 = **计算层（兼容旧 per-task）** + **管线层（新增）** 两段共存。

### 2.1 计算层（per-task 兼容，Block B 直接用；非计算阶段可空）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `task` | string | ❌ | 计算任务类型，见 `coze_contract.md §3` 枚举（pairwise_meta / nma / rob2 / prisma_flow …）。管线编排阶段（选题/检索/筛选/撰稿）可空或填语义 task（如 `topic_selection`）。 |
| `data` | object | ❌ | `{source, rows, colmap, csv_path}`（见 `coze_contract.md §2`）。 |
| `params` | object | ❌ | `sm/model/subgroup/reference_group/prior/locale` 等。 |
| `figure` | object | ❌ | `format/plots/theme/width/height`；本地 adapter 恒强制 `format="svg"`。 |
| `query_origin` | string | ✅ | `sha256:<64hex>`（裸 POST 必带，格式 `[debug:]sha256:<64hex>`）。与旧契约一致。 |
| `request_id` | string | ❌ | 每次调用 UUID。 |
| `_debug` | bool | ❌ | 调试标记（与 `debug:` 归因前缀配套）。 |
| `probe` | bool | ❌ | 连通性探测（health() 用，coze 端消费）。 |

### 2.2 管线层（新增）

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `contract_version` | string | ⚠️ 本地强写 | semver `^\d+\.\d+\.\d+$`。旧 consumer 可不带（向后兼容）；新管线流程必须带。 |
| `schema` | string | ❌ | 固定 `meta.pipeline.stage/v1`，用于区分旧 per-task 信封。 |
| `pipeline_id` | string | ❌ | 整条管线会话 ID，**跨阶段连续**（meta 全链路可能跨多天）。旧单任务分析为空。 |
| `pipeline` | object | ❌ | `{name, block:"A"\|"B"\|"C", cfg}`；`block` 标识当前功能块（A=方向/文献/数据，B=分析产出，C=撰写/修改）。 |
| `stage` | object | ❌（新流程建议带） | 见 §3。 |
| `stage_context` | object | ❌ | 跨阶段上下文累积：见 §4。 |

---

## 3. `stage` 对象

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `id` | string | ✅（新流程） | 阶段 ID，命名规范 `^[ABC]\d\..+`：`A1.topic_selection` / `B3.overclaim` / `C2.ai_review`（完整清单见 §9）。 |
| `index` | integer≥0 | ✅（新流程） | 阶段序号（从 0 起）。 |
| `total` | integer≥1 | ❌ | 预计总阶段数（coze 可动态调整，仅供参考）。 |
| `intent` | enum | ❌ | `run`（正常推进）/ `resume`（携带 `stage_context` 续跑）/ `retry`（本阶段重试）/ `human_callback`（人工闸回调，携带 `stage_context.human_decisions`）。 |
| `prev_stage_id` | string\|null | ❌ | 上游阶段 ID，便于溯源。 |

---

## 4. `stage_context` 对象（跨阶段上下文）

支撑 coze 跨阶段编排 + 人工决策可溯源（对应提案红线②）。

| 字段 | 类型 | 说明 |
|---|---|---|
| `human_decisions[]` | array | 人工闸确认/输入记录。`{stage_id, action:"approved"\|"rejected"\|"edited", by:"user"\|"expert", at:ISO8601, note, payload}`。 |
| `tool_card_outputs[]` | array | 本地执行的 tool_card 回灌结果。`{card_ref, need_tool, status:"ok"\|"error"\|"need_params", result}`。`status=need_params` 时 `result.missing` 列出缺失项，本地追问用户后重发。 |
| `artifacts[]` | array | 已完成阶段产物索引（不内联大对象，仅存 `stage_id/type/ref`）。 |

---

## 5. Response 字段（`PipelineStageResponse`）

### 5.1 管线层核心（新增）

| 字段 | 类型 | 说明 |
|---|---|---|
| `stage.id/index/status` | — | 回声 + `status`: `await_human`(等人工闸) / `completed`(阶段完成可续) / `failed` / `need_tool`(需本地执行 tool_card) / `need_data`(需用户补数据)。 |
| `stage_result` | object | `{summary, artifacts[], data_for_next_stage}`。`artifacts[].{type,format,data,svg}` 承载本阶段结构化产物（选题报告/森林图/稿件 md/参考核验结果）；`data_for_next_stage` 透传给下一阶段。 |
| `next_human_action` | object | 见 §5.2。 |
| `tool_cards[]` | array | 需本地执行的工具卡（复用 need_tool 范式），见 §6。 |

### 5.2 `next_human_action` 对象

| 字段 | 类型 | 说明 |
|---|---|---|
| `type` | enum | `none`(自动续跑) / `confirm`(确认方向/参数) / `review`(审阅草稿) / `provide_data`(补数据) / `approve`(批准/署名) / `edit`(修改后回交)。 |
| `prompt` | string | 给用户的提示语。 |
| `required` | bool | 是否必须人工响应才能续跑。 |
| `gate` | enum | 🔴 **红线闸标识**（见 §8）：`none` / `extraction_review` / `final_inclusion` / `manuscript_approval` / `reference_verification`。`gate≠none` 时本地 adapter **必须**强执（阻断自动续跑）。 |
| `options[]` | array\|null | 可选选项（如多选方向）。 |

### 5.3 计算层兼容（旧字段原样保留）

`status` / `task` / `stats` / `figures` / `warnings` / `notes` / `repro` 与 `coze_contract.md §4` 完全一致。Block B 计算阶段直接返回分析结果时，这些字段承载数值；管线层字段（`stage_result` 等）可同时附上或留空。

### 5.4 诊断/兼容字段

`_request_id` / `_contract_drift` / `_needs_upgrade` 沿用 `coze_client.py` 现有契约漂移检测输出。

---

## 6. `tool_cards[]`（复用 ct-advisor need_tool 范式）

每张卡 = coze 下令「需本地执行某 ct-* 技能」→ 本地 adapter 代码层机械执行 → 结果回灌 `stage_context.tool_card_outputs`。

| 字段 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `card_ref` | string | ✅ | 卡片引用 ID（回灌关联用）。 |
| `need_tool` | string | ✅ | 技能标识，对齐 `tool_mapping.json` 的 `id` 列（`ct-literature` / `ct-registry` / `ct-safety` / `ct-samplesize`）。 |
| `params` | object | ✅ | 技能入参（键名对齐该技能 CLI 的 argparse 参数）。 |
| `draft_answer` | string | ❌ | coze 已生成的草稿基底（缝合用）。 |
| `run_id` | string | ❌ | 追踪 ID。 |
| `sync` | enum | ❌ | `blocking`(本阶段需等结果才能续) / `async`(可先继续，后台回灌)。默认 `blocking`。 |
| `timeout_sec` | integer≥1 | ❌ | 执行超时（检索类默认 120，计算类默认 60，与 ct-advisor 一致）。 |

**本地执行语义**（复用 `handle_need_tool.py`）：
- 查 `tool_mapping.json`（单一数据源）→ 构造 CLI 命令 → subprocess 执行 → 取结构化主产物。
- 缺参 → 返回 `status:"need_params"`，列出 `missing`，**由本地大模型仅向用户追问（不编造）**，补齐后重发。
- 失败 → 回退 `draft_answer`（coze 草稿），附「补充检索失败」提示。
- 执行后**不回发 coze**：结果经 `stage_context.tool_card_outputs` 回灌下一请求。

---

## 7. 向后兼容与版本协商

1. **旧 consumer 兼容**：`contract_version`/`schema`/`stage`/`stage_context`/`stage_result`/`next_human_action`/`tool_cards` 在 JSON Schema 中均为 **optional**。一个只含 `{task,data,params,figure,query_origin}` 的旧请求，以及只含 `{status,stats,figures}` 的旧响应，均通过 schema 校验。
2. **分支解析**：本地 adapter 据 `schema`/`contract_version` 是否存在决定走「per-stage 管线分支」还是「per-task 兼容分支」。旧 coze 响应（无 `contract_version`）→ 走 `coze_client._fill_external_svgs` 旧解析；新响应 → 走管线解析。
3. **major 不一致**：响应 `contract_version` 的 major 与本地不一致 → adapter 拒绝解析、报 `ContractVersionMismatch`、降级本地 offline 兜底（选题启发式 + 缓存模板，标注「未经云端精校」）。
4. **coze 端 `extra='ignore'`**：现有 `state.py` 用 pydantic `extra='ignore'`，新可选字段不会破坏旧节点逻辑；但**新增管线字段若要被 coze 消费，必须先在 `state.py` 加字段并重新部署**（见 `coze_contract.md` Phase 0 草稿章节）。

---

## 8. 🔴 红线闸清单（本地强执）

| gate 值 | 触发阶段 | 强执要求 |
|---|---|---|
| `extraction_review` | Block A 提取核验 | 影响效应量的关键字段（TE/seTE/事件数）必须人工核验放行，方进 Block B；漏闸 → 数据错误 → 结论失真（不可自动化绕过）。 |
| `final_inclusion` | Block B 质量门 | 最终纳入研究数 / 异质性判定须人工确认。 |
| `manuscript_approval` | Block C 稿件批准 | 终稿须经用户/专家署名批准方可产出投稿件。 |
| `reference_verification` | Block C 参考核验 | 参考文献须经 DOI/PMID 交叉验证，禁止 AI 排版虚构文献（JAMA 2026-08 政策）；漏核验 → 不可投稿。 |

> 任一 `gate≠none` 且 `required=true` 时，本地 adapter **阻断自动续跑**，强制把 `next_human_action.prompt` 呈现给用户并等待 `intent=human_callback` 回交 `stage_context.human_decisions`。

---

## 9. 阶段 ID 规范（建议清单，供 coze 编排对齐）

```
Block A 方向确定与文献/数据准备
  A1.topic_selection       选题闸门（PICOS→双库探针评分→PROSPERO 查重）
  A2.literature_search    检索（委派 ct-literature，tool_card）
  A3.screening            AI 筛选草稿 + 人工闸
  A4.data_extraction      提取 AI 草稿 + 🔴extraction_review 人工核验闸

Block B 分析结果产出（本地实现：block_b.BLOCK_B_SEQUENCE）
  B1.meta_analysis        R 引擎计算（pairwise / nma / metareg）
  B2.grade                半自动 GRADE（结果整理：森林图/漏斗/亚组/元回归）
  B3.overclaim            过度声明检测（12 模式）
  B4.quality_gate         🔴 质量门收口（GRADE+过度声明+人工闸 / final_inclusion）

Block C 论文撰写与修改（本地实现：block_c.BLOCK_C_SEQUENCE）
  C1.draft                初稿生成（IMRaD + PRISMA）
  C2.ai_review            AI 评审 / 过度声明检测（复用 B3 detect_overclaims）
  C3.ref_verify           🔴 参考完整性核验（DOI/PMID / reference_verification）
  C4.evidence_qa          GRADE 证据表 + 🔴 manuscript_approval + 投稿前 QA
```

> 上表与本地实现（`adapters/block_[abc].py` 的 `BLOCK_*_SEQUENCE` 常量）逐字对齐；
> `id` 仍须满足 §3 命名规范 `^[ABC]\d\..+`。改动阶段 ID 须同步
> `adapters/fullflow.py` 的 `GATE_TO_STAGE` / `DEFAULT_PAUSE_AT` / `EDITABLE_KEYS`。

---

## 10. 质量门 / 契约测试要点

`test_contract.py`（同目录）必须覆盖：
1. **Schema 自洽**：request/response schema 可被 `Draft202012Validator` 加载。
2. **Example 往返**：`example_roundtrip.json` 每条消息按 `_kind` 校验通过。
3. **向后兼容**：纯旧 per-task 请求（无 contract_version/stage）与纯旧响应（无管线字段）均通过。
4. **枚举约束**：非法 `gate`/`sync`/`intent`/`stage.status`/`next_human_action.type` 被拒。
5. **红线强执可测**：构造 `gate=extraction_review, required=true` 的响应，断言 adapter 测试桩不进入自动续跑。

> 每次 coze 端点契约变更（state.py 重部署）后，须重跑 `test_contract.py` + 现有 `§8.5 deploy_retest` 闸门（扩展为全管线测试）再进入发布轨道（GitHub→SkillHub→ClawHub）。

---

## 11. 部署影响（落地检查单）

- [ ] **本地 adapter**：`coze_client.py` 新增 `run_stage(envelope)` 或在 `run_meta` 上加管线分支；新增 `parse_stage_response()` 解析 `stage_result/next_human_action/tool_cards`；新增 `execute_tool_cards()` 复用 `handle_need_tool` 范式。
- [ ] **本地工具卡执行器**：放 `adapters/tool_mapping_meta.json`（仅 Block A/C 需要的 ct-* + 未来本地子端点）；或复用 ct-advisor 的 `tool_mapping.json`（跨技能共享）。
- [ ] **coze 端**：`state.py` 的 `GraphInput`/`GlobalState` 加 `contract_version`/`schema`/`pipeline_id`/`pipeline`/`stage`/`stage_context` 可选字段；编排节点产出 `stage_result/next_human_action/tool_cards`；重新部署后飞书日志加 `pipeline_id` 列。**未重部署前，本契约仅本地侧生效，coze 返回旧 per-task 结构（adapter 走兼容分支）。**
- [ ] **测试**：`test_contract.py` 入 CI；`deploy_retest` 扩展全管线。

---

## 12. 文件双向传输（上传 / 下载）

> 完整设计、字段语义、落地清单见同目录 `FILE_TRANSFER.md`。

- **下载（框架已具备，待显式字段）**：coze 端把 svg/r/完整 envelope 上传 S3，本地用通用 GET 预签名下载器（`_fetch_full_json` / `_reassemble_from_manifest` / `_download_s3_ref`）拉取。**缺口**：契约无“文档类产物”返回字段 → 新增响应 `attachments`（含预签名 GET `url`），Block C 生成的 docx/xlsx 走此通道（与 `figures[].svg` 外置对称）。**下载无需新增下载器，仅新增“遍历 attachments 并落盘”的编排逻辑。**
- **上传（空白，本次预留接口）**：
  - 请求 `attachments`（array，optional）：本地已上传到 S3 的文件引用（如 Block A 多 PDF）。
  - 触发范式：`tool_card.need_tool="request_upload"` → 本地 `_upload_file`（预签名 PUT）+ 回灌 `stage_context.tool_card_outputs` → coze 据 `key` 取 PDF 解析。与现有 `ct-literature` 委派同构。
  - `AttachmentRef`（`$defs`，两侧共用）：`storage/key/filename/mime/size_bytes/sha256` 必填；**上传侧 `put_url` 可选、下载侧 `url` 必填**；可选 `purpose` 字段用于**一次上传多个文件时区分类别**（literature_fulltext / extraction_template / roi_screenshot / manuscript_draft / prisma_figure / grade_table 等），缺失则按同类型批量处理。多文件在 `attachments[]` 数组内并发 PUT。
- **向后兼容**：`attachments` 两侧均 optional，老请求/响应不带不报错；`request_upload` 是新 tool_card 类型，老 adapter 不识别即忽略。与 `BACKWARD_COMPAT.md` R1–R5 一致。
- **契约已落地**：request/response schema 加 `attachments` + `$defs/AttachmentRef`；`test_contract.py` §7 覆盖上传/下载往返 + 非法 AttachmentRef 拒绝 + optional 兼容。

---

## 13. 计费身份标识（预留接口，向后兼容）

> 设计依据：见对话记录——`query_origin` 是匿名主机指纹（主机名 SHA-256），用于归因/限流/飞书，**不含用户身份**；计费需独立、可计量、防伪造标识，不应复用 sha 字段。当前仅预留接口，不接入实际计费。

- **`account_id`**（请求顶层，optional）：付费账户明文标识（许可码/客户号）。务实版（受信/内部用户）使用；缺失 → legacy/未计量路径。
- **`billing_token`**（请求顶层，optional）：服务端签发的计费令牌（JWT/HMAC，含 `account_id`+`quota`+`exp`）。稳健版（真收费）使用，coze 验签后计量 + 强制配额/限流，客户端无法伪造他人账户。
- **二者关系**：`account_id` 与 `billing_token` 二选一；均缺失 → 走 legacy 路径（与 `BACKWARD_COMPAT.md` R1–R5 一致，老客户端零影响）。
- **coze 端**：新增独立 `billing` 中间件读取该字段，与 `query_origin`（机器指纹）完全解耦。具体见 `coze_contract.md §11`（草稿）。
- **向后兼容**：两字段均 optional，旧请求不带即通过校验；旧 coze 端点因 `extra='ignore'` 忽略该字段，只回旧结构 → 新/旧本地端均不崩。`test_contract.py` §8 覆盖。
