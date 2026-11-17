# 2.0 导出报表版：真实宿主调度与完成检查

适用于 2.0 主理人和成员任务。本文替代 1.x 的封存、等待恢复和任务身份绑定操作；不改变数据、审批、公域隔离、分析深度或默认 PDF 要求。正式范围为用户授权的导出报表，不依赖平台连接；API、后台动作与模型路线扩展未启用。本文是操作规范，不是本次真实运行的验收证据。

## 1. 真实工具先于本地记录

本地程序不创建专家、不发送成员消息，也不能鉴定人为编辑的宿主导出是否真实。宿主工具返回的原始任务 ID、启动结果、等待结果和成员消息才是运行证据。禁止先编写 JSON 状态再声称真实专家已运行。

开始综合任务时先确认当前真实宿主，只能在 `workbuddy` 与 `codex` 中选一个。把当前实际可见的调度能力交给 `scripts/host_orchestration_guard.py`，生成 `omni-ecom.host-orchestration-plan@2.0`。该计划固定本次允许的宿主词汇并拒绝混用；它始终标记 `planned_not_executed`，不能代替任何真实子任务或完成证据。

- WorkBuddy：仍先按主理人规则通过真实 `TeamCreate` 建团，保存真实团队返回，并用 `team_bootstrap_guard.py record` 生成 `omni-ecom.team-bootstrap@2.0`；命令必须同时传入本次 client_scope、run_id、团队版本和真实 team_name。成员通过本次实际可用的 Agent 工具启动，真实子任务轨迹保留；阶段 `TaskCreate` ID 不得作为专家 ID。需要延迟工具时按宿主提供的工具搜索方式加载，不猜测接口存在。
- Codex：使用当前可用的真实 `spawn_agent / wait_agent / send_message` 能力，不寻找或模拟 WorkBuddy 的 `TeamCreate / TaskCreate / TaskList / TaskUpdate / Agent / TaskOutput / SendMessage`。保留工具返回的原始 ID，不加 `agent-` 前缀。没有真实子代理工具就阻断综合任务，不采用内联角色扮演。
- 按宿主实际可用的子代理名额分批。可并发三个时先启动三位、等待并收取其正式回传，再启动第四位。分批不减少四位岗位，不允许前三位回传后提前并稿。等待窗口按宿主工具支持范围调用，观察超时不等于任务失败。
- 模型和推理设置沿用用户或宿主配置；不得凭岗位名虚构实际使用的模型。未公开的成本、版本、时延保持未知。

每次成员及定向质疑的启动、回传、失败和拒收都使用 `omni-ecom.collaboration-event@2.0` 记录事件类型和本次运行版本；旧 1.0 事件只可作为历史阅读，不能计入当前岗位参与、结束等待或完成条件。每次终态会自动记录可取得的模型元数据和回传结果。需要导出本次质量记录、记录真实人工纠正或比较同类历史任务时，读取 [运行质量观察](behavior-monitor-v2.md)，不得把测试夹具当成真实两周基线。

## 2. 运行目录与身份

如果本次包含平台动作建议，先阅读 [受控动作资格检查](action-policy-v2.md)。当前模块不执行平台操作，不将本地 approved 字段当成真实授权；生产网关和平台接入仍需独立验收。

本次报告目录同时作为 `RUN_DIR`，其中保存 `run-journal.sqlite`、报表清单、基线、`quality-inputs.json`、交接件以及报告四件套。`run-journal.sqlite` 是唯一当前运行账本；旧 `run.json/events.jsonl` 不得作为 2.0 当前状态或完成依据，`omni-ecom.run-record@2.0` 只是从 SQLite 生成的只读快照。输入来源放在本次授权目录内的只读副本中，保留原文件指纹。不得为了满足路径要求读取或搬入其他客户资料。成员输出路径在每次 attempt 内唯一，不能覆盖上一尝试。

首次读取业务文件前，运行 `skills/ecom-diagnosis-core/scripts/context_guard.py` 生成 `run-scope.json`。它必须是 `omni-ecom.run-scope@2.0`，与 SQLite 中的 client_scope、run_id、team_version 一致，并列出本次允许目录、实际选择的输入和逐文件 SHA256/大小。将其相对路径写入 `quality-inputs.json` 的 `run_scope`。质量门禁会重新读取全部来源；凭证被阻断、属于旧版、来源移位或哈希变化时都必须停止，且这些来源随后进入复核清单与完成冻结链。

若清单确认 report_count=0，且范围凭证唯一错误为 `run_scope_no_files`，不要建立专家任务或生成报告。仅在仍处于 intake 且运行账本没有其他事件时执行 `scripts/intake_blocked.py --run-dir <RUN_DIR> --run-id <RUN_ID> --client-scope <CLIENT> --team-version <VERSION>`。它生成独立的无报告终态回执和审计事件，明确 `formal_delivery_completed=false`；这不是报告完成回执，也不能在已有文件或已经启动专家后补写。用户上传数据后新建 run_id。

这里的运行账本仅用于本次专家协作与报告。平台动作必须另按 [跨任务固定执行记录](execution-store-v2.md) 使用宿主固定存储，不能每次报告新建一份空的执行记录。两者以真实 run_id 和经校验的执行引用关联；生产自动接线仍待宿主验收。

先初始化（占位符必须换成当前任务的真实值；禁止照抄示例生成运行证据）：

```text
python scripts/host_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT init --team-version VERSION --task-type TYPE
```

`VERSION` 与本次测试/发布实际版本一致；`TYPE` 从 `config/task-profiles.json` 选择。综合报告四位分析岗位必须齐全；仅用户明确的单项问题允许选用真实单点岗位。共享口径基线使用 `omni-ecom.analysis-baseline@2.0`，其客户、run_id、team_version 必须与本次运行及报告一致；旧 1.0 基线仅可读取历史，不能参与当前分析。成员 handoff 内的深度声明使用 `omni-ecom.analysis-depth@2.0`；整轮深度检查与冲突扫描分别输出 `omni-ecom.analysis-depth-guard@2.0` 和 `omni-ecom.conflict-scan@2.0`。三者必须绑定同一基线，不能用旧文件、跨版本文件或错类型文件替代。

每个真实子任务启动后，主理人将已观察到的结果规范化留档；观测文件不含平台凭证或原始业务数据：

```json
{
  "run_id": "本次运行ID",
  "client_scope": "本次客户范围",
  "host": "workbuddy 或 codex",
  "task_id": "工具实际返回的原始ID",
  "state": "created 或 running",
  "evidence_kind": "native_host_observation",
  "source_reference": "本次真实工具结果的可定位引用"
}
```

测试必须改为 `synthetic_fixture`，不得混入真实运行验收。启动与终态观测用不同文件，原文件不改写。使用真实启动返回登记：

```text
python scripts/host_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT start --role ROLE --host HOST --task-id TASK_ID --attempt ATTEMPT --observation observations/ATTEMPT.started.json
```

## 3. 成员一次性正式回传

主理人首次任务包必须给出客户范围、run_id、team_version、scope、attempt、角色卡、章节清单、基线路径及 SHA256、最低深度/岗位最小分析集、当前允许读取的文件和两个输出绝对路径。

分析成员自己生成 raw handoff 并通过 `validate_handoff.py` 与 `analysis_depth_guard.py`。沿用业务字段，额外明确顶层 `client_scope` 和 `agent_version`，不得仅在自由文字里写客户。然后自己计算 raw handoff SHA256，生成本次最小回执：

```json
{
  "run_id": "本次运行ID",
  "agent_id": "本岗位ID",
  "attempt_id": "本次尝试ID",
  "return_status": "completed",
  "returned_at": "真实带时区的时间",
  "contribution_summary": "本次实际贡献",
  "handoff_sha256": "原始交接件的SHA256",
  "response": {"handoff_file": "本次交接件相对路径"}
}
```

成员已知实际 `agent_task_id` 时可附带，但不需要暂停等待主理人提供；主理人封存时绑定真实宿主 ID。已填写却不匹配时阻断，不覆盖错误值。主理人不得代写或修补成员 raw handoff、回执和业务贡献。

完成后仅向主理人回传一次并结束，不与同级聊天。数据不足也需自己交付 WARN/BLOCKED 与补数清单。主理人同时读取真实宿主终态、成员回传和文件，观测终态确为 completed 才登记 completed 观测。仅看到文件存在不算专家任务已完成。

```text
python scripts/host_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT accept --role ROLE --host HOST --task-id TASK_ID --attempt ATTEMPT --handoff raw/ATTEMPT.json --return-file returns/ATTEMPT.return.json --observation observations/ATTEMPT.completed.json --output sealed/ATTEMPT.json
```

2.0 使用此命令代替直接 `seal_handoff.py`：同时封存文件并记录实际接收事件。报告只能引用该次已选中的 sealed 文件。不能用旧版封存程序生成一份文件后绕过运行登记。

## 4. 等待、中断与重试

```text
python scripts/host_runtime.py --run-dir RUN_DIR --run-id RUN_ID --client-scope CLIENT status
```

status 中 `waiting` 是需要回到真实宿主继续查询的原始任务 ID，不是“仍然活着”的独立证明。恢复时用原 ID 核对宿主。宿主观察超时或短暂查询失败，继续观察同一任务，不因超时重新启动。

WorkBuddy 还可运行 `python -B scripts/workbuddy_recovery_status.py --run-dir RUN_DIR`，从原生会话轨迹读取实际成功派工的任务 ID，并与岗位回传文件交叉显示。它只读，不启动任务、不改账本，也不把文件存在当成宿主已完成。中断恢复时先查这些原 ID；宿主支持原任务 resume 时继续原 ID，宿主无法确认恢复时如实保留未完成状态，不重新派发同一任务卡。

`reuse_verified_delivery` 表示完成凭证、对应审计事件、报告文件指纹和实际已选成员仍一致，可读取既有交付，不重新派工。仅有一个写着 completed 的文件而没有对应审计事件，不算已完成。报告或完成凭证变化时显示 `completion_invalidated`，不可沿用旧交付；先检查变化原因，按修订流程重新冻结与复核。

宿主确认 failed/cancelled 时，用对应实际失败观测运行 `fail` 后新开 attempt；失败观测、原回执和原任务 ID 保留。宿主已经 completed 但返回身份或业务契约不合格，`accept` 会记录 `member_rejected`，不是伪标宿主 failed，也不继续无限等待。此类返回不得原位补改，必须由新的真实 attempt 自己重做。原始文件根本无法读取等 I/O 问题先恢复读取，不直接断言专家失败。累计两次实际失败/无效回传后，该岗位重试额度用尽，保持阻断；不能手改数据库绕过。

新的 attempt 尚未回传时，旧 attempt 不能顶替完成；同一宿主任务不能冒充两个岗位。每个岗位最多一次失败重试；hard 冲突质疑是独立的一轮定向追问，不是重跑全团。按 [定向质疑及裁决回传](challenge-round-v2.md) 联系原专家、登记该次实际宿主观察并核对回传；不能拿初次分析完成状态顶替。口径和趋势按其关联的裁决规范重算，因果解释仍需独立证据审查；未通过时保持阻断，不伪造质疑完成。

WorkBuddy 等待时使用宿主阻塞等待/任务输出，不用一条结束回合的“稍后回传”替代等待；Codex 可简短通报实际进度，但不得在成员未齐时宣布完成。不要使用本地 status 代替真实等待工具。

## 5. 质量输入和冻结

生成前按 [数字索引原文件复算](claim-sources-v2.md) 定位原表单元格与推导输入。数字索引及被实际读取的原表自动进入质量检查、复核冻结和完成前复算；来源标注或通过凭证本身不等于原始数字真实。业务口径与来源认证边界见该说明。

在报告目录写 `quality-inputs.json`，以下路径都相对报告目录，必须在目录内；角色映射必须指向本次实际接收的 sealed 文件：

```json
{
  "run_id": "本次运行ID",
  "client_scope": "本次客户范围",
  "report_revision": "R1",
  "inventory": "report-inventory.json",
  "chapter_plan": "chapter-plan.json",
  "baseline": "baseline-pack.json",
  "handoffs": {
    "data-analyst": "sealed/data-a1.json",
    "platform-ops": "sealed/platform-a1.json",
    "content-live-growth": "sealed/content-a1.json",
    "ad-profit-optimizer": "sealed/profit-a1.json"
  },
  "min_level": "L2"
}
```

需要裁决时附 `adjudication` 文件。分析前仍须全量识别/归类报表、生成同一基线；分析后仍须来源数字校验、深度、覆盖和冲突复算。默认归因不低于 L3、决策不低于 L4；不能为了放行降低深度。

存在裁决时，先按 [裁决默认进入报告](decision-delivery-v2.md) 将本次完整裁决与结论放进 quality-inputs.json 指定的 adjudication 文件。生成器默认导入，不再依赖额外参数；有 hard 分歧却没有在实际报告中展示完整处理结果时，不能通过质量检查。

生成并逐页检查报告四件套后调用 `review_guard.py prepare`。它重新执行质量检查，核对本次四位接收记录，冻结 `quality_gate` 和 `runtime_gate`，自动纳入启动观测、原始交接件、attempt 回执和终态观测的指纹。这里冻结的是完成后不可改写的 attempt 证据，不是共享可变 return 文件。运行数据库继续追加，不冻结整个数据库，否则复核任务一启动就会误报来源变更。

候选版真实验收与正式客户交付必须分开：历史 `2.0.3-candidate.*` 使用 `completion_gate.py --candidate-acceptance` 写 `candidate-acceptance-receipt.json`，状态只能是 `candidate_pipeline_complete`，且不向运行账本写正式完成事件。已发布 2.0.3 不使用该选项，生成 `completion-receipt.json` 和 `formal_delivery_complete`。发布验收依据两条真实宿主核心证据，可选扩展未启用不得冒充已验收。

## 6. 复核及最终完成

旧版资料导入与恢复另见 [旧版迁移说明](legacy-migration-v2.md)。迁移出的历史对象不能传入当前成员接收流程，也不能继承旧执行审批。

仅在冻结后实际创建 delivery-review。其 start 命令额外可指定 `--manifest review-manifest-R1.json`，不传时默认 `review-manifest.json`。运行记录绑定复核启动时那份文件的字节和语义哈希，不能换稿后保留原复核身份。

复核员读取清单列明的确切报告、质量和运行证据，检查实际 PDF/逐页图，不编辑任何冻结文件。原始复核结果遵守角色卡，使用 `omni-ecom.review-result@2.0`，包含 `client_scope`、`agent_version`、生成版本、`review_attempt_id`、修订号和全部 reviewed_artifacts；另写上述最小宿主回执，其 `attempt_id` 就是 review_attempt_id。收到真实终态后同样先运行 `host_runtime.py accept`，再用原始复核结果运行 `review_guard.py attest-result`、`verify`。主理人不能改结果，更不能把 conditional_pass 改成 passed。复核清单、系统证明和放行回执分别使用 `review-manifest@2.0`、`review-attestation@2.0`、`review-release@2.0`，不能混用或沿用 1.0 文件。

数字检查回执使用 `omni-ecom.claim-guard@2.0`。公域检查生成回执时必须传 `--team-version`，回执使用 `omni-ecom.public-output-guard@2.0`。完成关会再次核对这两份回执与报告版本；只有状态文字而没有正确文件身份不能放行。

最终 `completion_gate.py` 除原来的数字、PDF和公域检查，还要求：

- 数据库存在且客户、运行、版本、报告类型一致；四位实际回传与报告选件完全一致；没有等待任务。
- 报告岗位表的 ID 与本次已选任务相同，不把未调用角色写成已贡献。
- 每份原始/封存交接件、回执和宿主观测未变化；复核看到的分析成员集合与当前相同。
- 复核结果、实际复核任务、attempt、冻结版本及放行凭证一一对应。

完成回执写入账本时另生成 `omni-ecom.delivery-completed-event@2.0`，绑定回执路径、指纹、报告修订和运行版本。旧完成事件、手写事件或只有完成文件而没有正确账本事件，都不能结束本次任务。

任何一项不符都阻断。程序通过只能证明这些本地记录彼此一致，不证明宿主导出的真实性；正式双宿主验收还需直接查看实际任务轨迹与返回消息。公域只展示实际 ID、贡献和状态，不公开本机目录、内部观测全文或其他客户信息。
