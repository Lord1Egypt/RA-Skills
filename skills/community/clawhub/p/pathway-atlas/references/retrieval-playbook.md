# 可复现检索流程

## 统一规范入口

本页只用于用户明确要求的深度核验。默认喜报参考按快速规划使用 `brief`，无需执行本页完整矩阵或精确采纳门槛。以下所有 publisher tier、independence、deduplication、admission、conflict 和 evidence-state 决策只使用[信源规范](source-policy.md)。本流程只规定执行顺序、有限边界和完成标准；能力损失改变 coverage，不改变 truth rules。深度核验时宿主按 [host workflow guide](host-workflow.md) 运行 `scripts.host_workflow` 的 `start`、`next`、`ingest`、`unavailable`、`finish`；该门面以 `scripts/planning_session.py` 管理一次可恢复会话，并在内部完成 `init`、`confirm`、factory-only receipt、journal replay、evidence、calculation 与 publication。状态是这些命令返回的 JSON，不存在单独的 `status` 子命令；用户不接触 JSON、命令或内部路径。

实现不变量仍是 completed bridge→receipt→ingest 留在同一宿主进程，`build_task_evidence_outcome` 的 `evidence_outcome=` 不能由调用方状态或裸 digest 代替。Agent 只准备已打开的公开材料、候选元数据与 adapter 配置；门面拥有 receipt、evidence bundle 和 journal。

低层命令只作 seam 探针；正常规划使用 host workflow guide 的门面命令。

```text
$ python -m scripts.preflight --help
$ python -m scripts.query_plan --help
$ python -m scripts.validate_evidence --help
$ python -m scripts.planning_session --help
```

## 1. 能力预检

画像 `confirm` 后，宿主把完整 normalized20 answers 保存在私有文件，并调用 `python -m scripts.host_workflow start --workspace … --answers … --intake … --confirmed`。只把运行时真实可用的 search、browse、vision 作为重复的 `--host-capability` 参数传入；门面探测 optional modules，创建 replay journal，保存画像、capability report 和 canonical QueryPlan。不得另造能力名或档位别名，也不要求用户运行命令或提供路径。

| 类型 | 有限值 |
|---|---|
| host_capabilities | search,browse,vision |
| optional_modules | docx,openpyxl,pdfplumber |
| capability_tier | full,standard,offline |

统一 capability 入口只在这里定义；方括号表示仅在当前会话确实可调用该能力时加入对应参数，不是字面参数：

```text
python -m scripts.host_workflow start --workspace … --answers … --intake … --confirmed [--host-capability search] [--host-capability browse] [--host-capability vision]
python scripts/preflight.py [--host-capability search] [--host-capability browse] [--host-capability vision]
```

`local_exec` 与 `file_output` 是 workflow gates，不是 `--host-capability` 值。宿主指南只映射实际工具，不复制本会话循环。

完成标准：机器 capability report 已存在，档位与每项 degradation 都有显式值。

## 2. 构建并读取确定性查询计划

宿主从 `start` 返回的 `session_id` 调用 `python -m scripts.host_workflow next --workspace … --session … --limit 3`，读取门面已绑定的 canonical deterministic QueryPlan task。`pending` 是全部未完成任务数；`next` 只是显示切片，默认 3 条，可用 `--limit 1..100` 调整，不会丢弃其余 pending。显示顺序先按最新年份，再按 kind 和 task ID。门面内部加载经过验证的 `ProvinceConfig.mode`，不得虚构 `province.json`。逐个独立处理 `task_id`，保持任务声明的 `province`、`subject_group`、`year`、`kind`、`required_extraction_fields`、`availability`、`freshness` 与 `max_candidates`；不合并不同事实、年份、省份或 subject context。当前查询年由会话日期动态确定，每个数据族都按 `Y → Y-1 → Y-2 → Y-3` 独立回查，并选择最近可比的可用年份。目录、session ID 与 revision 只留在宿主内部。

完成标准：每个 task_id 已排入独立队列，或以明确 unavailable reason 结束。

## 3. 开始检索并枚举候选

只在步骤 1–2 完成后开始检索和 discovery。搜索只用于发现候选；必须打开原页面或附件并核对正文，搜索摘要不得充当事实。依照统一规范入口给出的检索优先级枚举实际可访问候选直到任务上限；首个看似可信页面只进入候选集，不结束枚举。每次失败的 network action 执行一次初始尝试，最多再 retry 一次，然后该 branch 降级或停止。

| 控制项 | 值 | 完成记录 |
|---|---:|---|
| candidate-cap | 10 | 保存实际考察数量与达到上限与否 |
| retry-per-network-action | 1 | 保存 initial attempt 与 retry 的结果 |
| first-plausible-stop | 禁止 | 保存候选枚举继续或停止的理由 |

完成标准：该 task 的候选不超过 10 个，所有 network action 已在 retry 边界内结束，并记录枚举结果。

## 4. 分类并去重

调用 `scripts.source_policy.py` 的 canonicalization 与 `deduplicate_candidates`；本流程不重述或重算规范中的独立性判定。

| 输入状态 | 动作 | 输出状态 |
|---|---|---|
| candidates-enumerated | deduplicate_candidates | independence-components |

完成标准：每个候选恰好处于 kept-once 或 rejected-with-stable-reason 状态。

## 5. 通过匹配适配器提取

网页阅读器只显示标题、空白或 `[Input]` 时，先检查原页面 HTML 中的 `img src`、`input type="image" src` 和公开附件链接。统计表可能以图片呈现，文本抓取为空不能当作数据未公布。按原页 URL 解析相对链接，经 secure downloader 保存原始图片或附件；有可靠视觉能力时逐行核对并使用 `ocr_rows`，否则记录图片提取能力缺失并继续寻找可读的公开来源或最近可比年份。

按 host workflow guide 的 submission schema 选择 exact adapter：HTML table、XLS/XLSX worksheet、PDF text、PDF明确数字表选区、host-normalized `ocr_rows` 或 quote/span 绑定的 public text；保存 URL/source provenance、year、`page/sheet/table/row` 或 `page/image/bbox` 字段 locator、coverage 和 ordered warnings。OCR 的 source path 指向原始公开图片或 PDF，`options.ocr_path` 指向宿主生成的 normalized JSON；门面固定使用 0.95 confidence floor，并验证 bbox anchors。Public text 先按 UTF-8-sig 读取并把 CRLF/CR 归一为 LF，再验证 quote/span；span 必须按该归一化文本计算。缺失 prose 字段从 field map 省略并保持 missing。`pdf_text` 用于路径政策，按页码及唯一精确原文绑定字段；`pdf_table` 只读明确页、表头、行范围与横排列组，保留局部覆盖，不将局部最大累计位次当全省人数。PDF缺pdfplumber时可用已安装pypdf，原始XLS由xlrd读取，真实parser缺失只降级对应分支。尚未由门面支持的 QR 输入记录受控 unavailable reason；QR 输入只能是 host-decoded text，并只通过 secure downloader 获取目标。

普通批投档行的唯一 handoff 是 `scripts.adapters.admission_bridge.bridge_admission_evidence`：组合 exact adapter row、对应 `QueryTask`、验证器返回的 `ValidatedAdmissionRow` 与 extraction coverage，委托公共 `admission_row_hash` 生成整行绑定，并将 `coverage_status` 与 evidence status 分开交给 `EvidenceStore`；本流程不重写这些语义。

Agent 把 submission 交给 `python -m scripts.host_workflow ingest --workspace … --session … --task … --submission …`。门面让位次、路径和普通批先由匹配 bridge 形成 typed record，再调用 `scripts.planning_session.build_task_evidence_outcome(profile, query_plan, task, bridges)`；该工厂重放画像、计划、任务和 bridge，随后由门面调用 `session.ingest_task(..., evidence_outcome=task_evidence_outcome)` 并保存新 revision。不得直接实例化 outcome，也不得把 adapter 输出改写成调用方声明的 completed 状态。

完成标准：每个 kept candidate 都产生显式 extraction coverage/warnings，或一个受控 missing result。

## 6. 证据采纳

调用 `scripts.source_policy.py` 得到规范结果，并把该结果连同 candidates 与 rejections 通过 `EvidenceStore` 持久化；本流程不解释或改写采纳判定。

| 输入状态 | 动作 | 输出状态 |
|---|---|---|
| extraction-results | persist-source-policy-result | EvidenceStore-persisted |

完成标准：每个 required field 恰好具有 accepted、partial/masked、conflict 或 missing 状态。

## 7. 最终化并验证证据

当 `next` 返回 pending 为零时调用 `python -m scripts.host_workflow finish --workspace … --session … --format markdown`。门面最终化 `EvidenceStore` 并运行 `scripts.validate_evidence` 的验证语义；validator 成功后才接受 authenticated immutable evidence snapshot。验证通过后，门面调用 `scripts.planning_session.build_evidence_manifest_outcome(...)`，传入当前 session、已确认画像、canonical QueryPlan、validated bundle 和全部 typed task outcomes，再执行 `session.finalize_evidence(evidence_outcome, ...)` 并保存 revision。任何 validation failure 都停止依赖该事实的 calculation；manifest 裸 digest 不能代替任务全集和事实重放，`compute` gate 晚于 validate 与 finalize。

| 输入状态 | 动作 | 输出状态 |
|---|---|---|
| EvidenceStore-persisted | finalize-then-validate | authenticated-snapshot |

完成标准：authenticated immutable evidence snapshot 已存在，或 dependent output 已显式 unavailable；不存在未验证的计算输入。

## 8. 为每个查询任务停止

每个 task 只允许以下四种 stop condition。completed 任务使用门面 `ingest`；失败则用 `python -m scripts.host_workflow unavailable --workspace … --session … --task … --reason …` 记录唯一 `unavailable reason`，再调用 `next` 取下一任务。仅当同族较新任务已经 completed 时，历史任务才可使用 `--reason newer_comparable_year_accepted --newer-task <completed-task-id>`；门面从 journal 取原始 typed receipt 并交给状态机复核。其他 reason 不得带 `--newer-task`，也不存在自动跳过全部历史任务。门面内部仍以 `build_task_evidence_outcome` 的返回值调用 `ingest_task(..., evidence_outcome=...)` 并先保存 journal revision。不无限循环，也不静默扩大问题。

短暂失败或进程重启后，以原 `--workspace` 和 `--session` 重跑 `next`；门面内部的 `PlanningWorkflow.resume` 调用 `context = journal.load(session_id)`，只使用 context 返回的 `session`、`profile`、`query_plan`、`capability_report`、`bundle_path` 和 `task_outcomes`。随后继续 `ingest` / `unavailable`，或在 pending 为零时 `finish`。`status`、session snapshot、裸 digest 或调用方 JSON 都不包含可授予 completed 权限的 bridge origin，不能代替 `journal.load`。

| 停止 ID | 触发条件 | 记录 |
|---|---|---|
| accepted | qualifying fact 已按统一规范入口采纳 | fact ID 与状态 |
| candidate-cap | 已考察候选达到 10 | 实际候选数与未覆盖项 |
| variants-exhausted | 所有 query variants 及各自 single retry 已耗尽 | variants 与失败原因 |
| unavailable | capability 或 authority availability 使任务不可执行 | unavailable reason 与 degradation |

完成标准：每个 task_id 恰好记录一个停止 ID；没有仍在运行或被静默扩大的分支。

## 9. 交接确定性引擎与报告

`finish` 只把 validated snapshots、已确认画像、canonical QueryPlan 与已声明 datasets/config 交给 deterministic engine/report。门面内部先调用 `scripts.planning_session.build_calculation_outcome(...)` 和 `session.with_calculation(...)` 保存 revision，再调用 `scripts.planning_session.build_report_publication_outcome(calculation_outcome, format="markdown"|"docx")` 并以 `session.publish_report(publication_outcome, ...)` 原子发布。calculation/report 裸 digest 不能替代工厂重建、内部渲染和 receipt 绑定。Markdown 与可选 DOCX 显示 `reference`、`inferred`、`partial`、`masked`、`conflict`、`missing` 及 coverage；推断显示 interval 和 method，不新增 snapshot 外的事实。

路径交接同时调用 typed pathway observation 投影。canonical QueryPlan 中处于 `include` 或 `discover`、但没有 accepted policy 的每个计划目标仍输出 `pending_verification`：投入结论固定为“观察”，资格固定为“待核验”，保留真实 `missing` / `masked` / `partial` / `conflict` 状态与已有 source IDs，并生成政策证据复核和资格核验动作。零来源 `missing` / `masked` 观察明确显示“无来源”；不得用 task ID 代替 source ID，也不得补写政策年份、目标位次或报名时间线。已有 accepted policy 的相同目标继续走原正式政策评估且不重复观察。

完成标准：deterministic engine/report 只消费已验证输入，且报告显式披露所有非 official/corroborated 状态与 unavailable output。

## 能力降级分支

| 机器档位 | 人类标签 | 可用能力与动作 | 证据规范 | 实时声明 |
|---|---|---|---|---|
| full | 完整档 | 执行当前 capability report 允许的所有步骤 | [同一信源规范](source-policy.md) | 只声明 snapshot 实际验证的年份与 coverage |
| standard | 标准档 | 只执行 capability report 允许的分支，其余记录 degradation | [同一信源规范](source-policy.md) | 只声明实际验证的 coverage |
| offline | 离线档 | 只使用用户提供或本会话先前保存且 authenticated 的 local fixtures/evidence；跳过 live discovery | [同一信源规范](source-policy.md) | 禁止声称当前或实时验证 |

三种分支都只调用同一规范入口；capability loss 只能减少 coverage。

按[研究恢复指南](research-recovery.md)执行有界替代路线。只有 `browse` 也能从已知官方源取证；缺少某个搜索API、浏览器或解析库不能当作全部任务不可执行。`research_summary` 披露完成与缺口，`older_year_resolution` 提供通过门面校验的历史任务收束建议。全无事实仍正常 `finish` 交付准备版，有部分事实则交付部分证据版；不得用经验代替缺失位次、学校档位或资格。
