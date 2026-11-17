# 可选深度认证

仅在用户明确要求深度核验时读取。默认喜报估算使用 `brief`，不受下面来源数量和矩阵闭合条件限制。

## 研究循环

用 `next` 返回的 typed `QueryTask` 按[检索流程](retrieval-playbook.md)逐项搜索、打开并保存公开材料。宿主写入 `references/host-workflow.md` 定义的 submission 后，运行 `python -m scripts.host_workflow ingest --workspace … --session … --task … --submission …`，即调用 `ingest`；无法完成则运行同一门面的 `unavailable` 并给出真实 reason。每次之后反复调用 `next` 循环，直到没有 pending task。门面拥有 journal、evidence bundle、completed outcomes 和恢复上下文；Agent 只准备公开材料及其提取配置，不手工拼接 receipt、digest 或 journal JSON。

每个任务保持 `ProvinceConfig.mode`、规范化 `subject_group`、`required_extraction_fields`、`availability`、`freshness` 和有界 `max_candidates`，不得另设固定 Top-N。搜索仅发现候选；必须打开原网页或附件，不能把搜索摘要当事实。按实际格式选择 HTML、XLS/XLSX、PDF、OCR 或 QR adapter 提取，下载只走 secure downloader，并保存 year、method、locator、source provenance、coverage 与 warnings。

所有年度数据按 `Y → Y-1 → Y-2 → Y-3` 查询。最新年度没有、缺失或未公布时依次逐年回查，最多向前查三年；每种数据类型独立选择最近可比年份，不能因一项缺失停止整份规划。至少覆盖一分一段表、投档位次、招生计划、招生章程、学费、选科要求、多元路径政策、服务期与违约条款。当前年度只有第三方资料而上一年度有官方资料时同时保留：前者标当年参考，后者标历史基线；制度或口径变化导致不可比时停止数值聚合并说明原因。

普通批投档只经 `scripts.adapters.admission_bridge` 组合 exact adapter row、对应 `QueryTask`、`ValidatedAdmissionRow` 和 extraction coverage，整行绑定委托 `admission_row_hash`，`coverage_status` 与 evidence status 分开。位次与路径分别使用 typed rank/pathway bridge；public prose 使用 quote/span 绑定的 `public_text` adapter，省略字段保持 missing。不得手工拼事实或虚构 `province.json`。

门面的 `ingest` 在同一宿主进程内执行 bridge→receipt→ingest：它用 exact adapter 产生的 typed bridge 调用 `scripts.planning_session.build_task_evidence_outcome(profile, query_plan, task, bridges)`，再以 `session.ingest_task(..., evidence_outcome=task_evidence_outcome)` 和内部 checkpoint 完成该任务。这里的 `evidence_outcome=`、factory-only receipt、完整 origin replay 和裸 digest 无授权能力是实现不变量；Agent 不调用这些底层步骤。

offline 仅消费用户提供或本会话先前保存且已认证的本地材料，不声称当前或实时验证；没有静默联网回退。每个 task 最终必须 `ingest` 为 completed，或用受控 unavailable reason 结束。

查询矩阵不是“所有年份全部抓取成功”的承诺。先核验各族最新年份；读取 `research_summary` 与 `older_year_resolution`，对已获合格较新证据的同族历史任务，按门面提示显式记录 `newer_comparable_year_accepted`。浏览器分支失败不影响其他读取方式，某格式失败不影响其他任务；同一确定故障在本轮只做初次尝试和至多一次重试，不能为每个任务重复启动失效工具。

完成标准：`next` 不再返回查询任务，每个 task 恰有一个可重放 outcome。

## 证据最终化

本节仅用于深度 `finish`。默认 `brief` 使用实际读取的公共原文与精确引用检查，输出 `planning_reference`，不冒称完成本节认证；公开原文足够支持参考学校或路径时不等待全部字段齐全。

按[信源规范](source-policy.md)执行发布者分级、独立性、去重、采纳和冲突处理；冲突不得取平均或挑选方便值。A 级原始来源可形成 `official`；没有 A 时，两个独立 B 一致可形成 `corroborated`，三个独立 C 一致可形成 `reference`。官方来源缺失、不可得或未找到时仍继续检索 B/C；未达到门槛的单源第三方只能作为发现线索或“观察”理由。

所有任务 completed 或 unavailable 后运行 `python -m scripts.host_workflow finish --workspace … --session … --format markdown`。门面先完成 `python scripts/validate_data.py` / `python scripts/validate_evidence.py` 对应的验证语义，再在内部调用 `scripts.planning_session.build_evidence_manifest_outcome(...)` 和 `session.finalize_evidence(evidence_outcome, ...)` 跨越 `finalize` gate并保存 checkpoint。形成 authenticated snapshot 之前不得给出数字或开始计算；未达到采纳门槛时保留 `partial`、`conflict` 或 `missing`，不降低门槛。manifest 裸 digest 不具有效力。

已确认画像或 canonical QueryPlan 中处于 `include` / `discover` 的路径不得因政策 `missing`、`masked`、`partial` 或 `conflict` 从报告消失。通过 typed pathway observation 保留“观察 + 待核验”：只携带真实存在的来源编号与原证据状态，明确缺口及政策/资格核验动作；没有来源时来源编号保持为空。不得为观察项编造政策内容、院校、资格结论、目标位次、政策年份、报名时间线或来源编号。相同计划目标已有可重放的 accepted policy 时，由原正式推荐逻辑替代观察项。

完成标准：fresh evidence bundle 与研究快照已认证；依赖缺失事实的输出具有明确 unavailable reason。

所有任务均真实标为 unavailable、没有公开事实时，也正常执行 `finish`；空证据包的认证仅证明记录和缺口一致，不意味着学生已有认证的位次或资格结论。不得绕过门面凭经验补数。

## 计算发布

用户要求深度报告时，`finish` 继续内部 `compute` gate：调用 `scripts.planning_session.build_calculation_outcome(...)` 和 `scripts.planning_session.build_report_publication_outcome(...)`，保存校验结果并原子发布；调用方提供的 calculation/report 裸 digest 不具有效力。Markdown/DOCX及完整证据审计作为附件，主对话仍按上面七部分先呈现已有结论。深度报告保留原披露：“本结果由 AI 基于公开数据整理，仅供升学规划参考，不构成录取承诺或正式升学建议。政策、招生计划和录取结果请以当年主管部门及招生高校最终公布内容为准。”
