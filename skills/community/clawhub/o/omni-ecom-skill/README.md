# omni-ecom 全域电商经营专家团

ClawHub 分发条目：`gzbarry1980-bot/omni-ecom-skill`。由经营总监统筹，四位分析专家和一位独立复核专家协作。先核对真实报表和指标口径，再输出经营诊断、增长动作与图表 PDF。

本分发版同步 v2.0.3、维护批次 20261014-r2 的核心脚本、角色卡、规范及数据契约。没有内置客户报表、客户名单、凭证或真实任务日志。安装、能力和使用限制先见 [ClawHub 分发说明](references/clawhub-distribution.md)。下文保留原工程说明；WorkBuddy 插件安装、头像、钩子与双宿主发布验收步骤只适用于原工程，不是本分发包自动拥有的功能。本包不提供这些安装组件。

## 版本

当前版本：`2.0.3`，现有专家团流程修整正式补丁版（上一正式版：`2.0.2`）。以授权 Excel/CSV 等导出分析经营，不依赖平台 API；模型沿用用户选择。无客户固定夹具的 WorkBuddy/Codex 真实多专家、图表 PDF 和独立复核验收已通过；不代表客户经营认证或周报耗时承诺。流程变化见 references/workflow-refinement.md。

沿用的基础能力：分析前先做 **Stage 0 报表识别与归类**，完整遍历用户上传的全部报表、归类并动态生成章节框架，再进入专家协作。

**第一步：完整遍历（`report_triage.py`）**
- 逐份识别报表类型（15 类）、业务域（10 域）、平台、时间范围、统计粒度、标准化指标、维度、完整度和可用性。
- 规则优先、模型补判：规则库先跑，未命中项进入 `model_review_pending`，由模型判定后用 `--model-verdicts` 回填，保证可复现、可回归。
- 自动定位表头行，并从表头前的标题行提取店铺与平台信息（生意参谋等导出文件的表头常在第 2-4 行）。
- 产出 `report-inventory.json`；`partial` 与 `insufficient` 必须写 `verdict_reason`。

**第二步：三轴归类（`cluster_reports.py`）**
- 业务域决定章节归属；时间轴禁止把不可比的报表凑在一起（期间重叠率 < 80% 只能单列趋势）；指标轴指定主源与印证源并生成交叉验证项。
- 归不进任何域的报表进 `unclustered`，`reason` 必填，单独占用独立观察章节，不丢弃。

**第三步：动态章节框架（`chapter-plan.json`）**
- 每个归类一个章节，写明分析口径、关键指标、跨报表交叉验证项和主责专家；章节骨架固定四段：口径与覆盖 → 核心指标 → 跨报表交叉验证 → 判断与行动。
- 主责映射：交易/流量/客服/市场大盘 → 数据专家；商品/会员资产 → 平台运营；内容与直播/达人 → 内容增长；投放/财务 → 投流利润；未归类 → 团长。

**第四步：覆盖闸门（`coverage_guard.py`，分级阻断）**
- `analyzable` 报表没有任何分析章节覆盖 → 硬阻断；`partial` / `insufficient` 只要写全原因、影响、补数要求 → 放行，未写全 → 硬阻断。
- 同时校验章节引用、数据概览是否列全、覆盖计划是否遗漏，以及最终报告正文是否逐份提及每个报表编号或文件名。

**当前报告结构**
- 前部展示经营摘要、任务重点、核心指标与图表；报表清单、归类和章节映射完整保留在同一 PDF 的证据附录中。
- 新增「数据缺口与限制」章节：数据不足的报表逐份写明原因、对结论的影响、补数要求与降级处理方式。
- `baseline-pack` 的指标契约改由清单中真实识别到的指标生成，权威顺序与归类的主源印证源一致。

上一版本：

- v1.5.13 聚焦团队协作质量与个体分析深度：共享口径基线包 `baseline-pack.json`，成员回写 SHA256；L0-L4 分析深度阶梯默认最低 L2。
- 新增 `analysis_depth_guard.py` 与 `conflict_scan.py`，把深度校验和四类跨成员冲突从肉眼比对改为机器扫描。
- 新增定向交叉质疑轮与团长亲跑数裁决铁律，未被采纳观点必须写明去向。

上一版本：

- v1.5.12 将四位分析专家的首次 a1 直接升级为正式可冻结 handoff，避免“健康检查一轮 + 补格式一轮”的重复子任务。
- 四位分析专家在同一分析阶段连续启动，全部取得真实 task ID 后统一等待；宿主逐条调用 Agent 时也不会被误判为未并行，只要中途没有等待或开始并稿。
- 新增 `release_guard.py` 与 `release_guard_smoke.py`：最终 ZIP 必须含根目录 `SKILL.md`，且拒绝 `.gitkeep`、`.pyc`、`__pycache__` 和未允许的文件类型。
- `verify_workbuddy_load.py` 不再只做单总监握手，改为调用 `runtime_acceptance.py` 验证真实 TeamCreate、四分析专家、韦交达、五个 task ID 和 `formal_delivery_complete`。
- 团长负责阶段任务状态闭环；成员不再调用 `TaskList / TaskUpdate`。最终交付前若仍有阶段任务悬空，返回 `phase_task_status_incomplete`。
- 每位分析专家每次 attempt 只向团长回传一次；禁止成员之间互发消息、回传后追加讨论或被同级消息反复唤醒。
- PDF 首屏补齐上一版本和版本差异；行动区改为逐条完整展示，避免负责人、审批状态、停止条件和贡献摘要被裁剪。
- 真实运行验收默认等待 45 分钟；若超时会返回本次 partial run 目录，供原 run 安全续跑，不会把超时当成功。
- 运行验收同时识别指定 `runs` 目录和宿主实际使用的 `.omni-ecom-runs`；可用 `--inspect-run` 对已完成的真实运行重新验真，不会因目录差异误报未创建。
- v1.5.11 在 v1.5.10 基础上增加数字来源、公式和归因硬闸门；没有 `claim_guard_passed` 不得进入正式交付。
- v1.5.10 在 v1.5.9 基础上增加团队启动超时边界和中断后安全续跑能力。
- 新增 `team_bootstrap_guard.py`：只接受真实 TeamCreate 返回的 `team_name`，并把宿主模式写入本次运行凭证。
- 新增 `collaboration_resume_guard.py`：按同一 run_id 判断成员回传、sealed handoff、报告、复核和完成凭证处于哪一阶段。
- 新增 `resume_smoke.py`：验证建团缺失、成员未齐、报告待生成、复核待完成和正式完成五种状态。
- TeamCreate 超过 90 秒没有成功 team_name 时返回 `collaboration_unavailable_timeout`，不会无限等待或重复建团。
- 用户说“继续”时，先检查原运行凭证；无法确认原团队身份就创建新的 run_id，不跨运行搬运文件。
- v1.5.9 修复 v1.5.8 完整协作冒烟测试中复核等待、attempt 绑定和正式完成状态未闭环的问题。
- 新增 `claim_guard.py` 与 `claim-ledger.schema.json`：每个数字必须回到来源文件、字段、期间和 SHA256；转化率、访客价值、ROAS/ROI、净 ROAS 公式和归因范围分开校验。
- `build_report_package.py` 强制接收 `--claim-ledger`，生成 `claim-receipt.json`；`completion_gate.py` 必须核验回执与冻结报告哈希。
- 新增 `completion_gate.py`：成员回传、数字来源、PDF验真、韦交达独立复核、公域隔离必须全部通过，才生成 `completion-receipt.json.status=formal_delivery_complete`。
- 新增八类任务配置：店铺诊断、周报、月报、季报、年报、大促复盘、数据质量审计和单项经营专题；报告包显式记录 `task_type/task_profile`。
- 最终完成凭证合并六岗位真实贡献与 Agent 子任务 ID；韦交达在候选报告中标为 `pending_review`，复核通过后在完成凭证中更新为 `contributed`。
- 公域隔离检查新增带文件哈希的 `public-output-receipt.json`，旧的扫描结果不能替代当前产物。
- v1.5.8 将可变 `*.return.json` 回执与不可变 `handoff-*.json` 业务交接彻底分离；报告构建和冻结复核只能使用 handoff。
- v1.5.8 R2 热修进一步按 `attempt_id` 隔离 raw handoff/return，并用 `seal_handoff.py` 绑定真实 Agent 子任务号；迟到或重试 Agent 不再能够覆盖已选中的交接件。
- 团长被禁止代写成员 raw handoff/return 或先写模板让成员只校验；成员不能亲自落盘时必须 fail closed。
- PDF 会把结构化待补数据转换为可读文本，并逐岗展示贡献摘要；交付复核岗在候选稿中明确指向最终放行凭证，避免产生“未复核”的误解。
- `review_guard prepare` 主动拒绝活动 return 文件并返回 `mutable_return_source_blocked`，避免成员结束阶段补写回执导致复核哈希失效。
- 冻结后任何 handoff、裁决或报告变化都必须升报告修订号并创建新的韦交达任务，禁止手写被 guard 拒绝的签收件。
- 韦交达采用一次性复核结果协议，不暂停等待创建后才出现的 task ID；团长只能用 `attest-result` 将原始复核结论绑定 WorkBuddy 的真实子任务 ID。
- 原始 CSV / JSON / XLSX / 可读 XLS 报表适配与字段映射
- `client_scope` / `run_id` 客户隔离和运行账本
- 结构化交接 Schema 与交接校验
- 12 个脱敏行为属性评测用例
- 数据质量闸门：`PASS / WARN / BLOCKED`
- 统一指标契约与证据账本
- N0 / N1 / N2 异常订单情景复算
- ROAS、扣退款 ROAS、扣匹配变动成本 ROAS 与利润 ROI 分离；共享成本分摊可复算且不冒充真实性审计
- 旧版数字可连同真实原导出和范围标签重新核验为 2.0 候选证据；不继承旧审批，也不把人工范围确认写成平台认证
- 搜索渠道可承受 CPC 测算
- 带验收指标和停止条件的行动清单
- 行动台账：提议 → 审批 → 执行 → 验证 / 回滚 / 阻断，并保留事件记录
- 结构化报告包：JSON + Markdown + 默认图表化 PDF + PDF 渲染凭证，证据、来源指纹、缺失数据和审批状态可追溯
- `BLOCKED` 自动收敛为数据质量报告，不把草稿包装成经营结论
- Connector 基础契约：能力声明、调用记录、对象 ID 映射、凭证引用和 mock dry-run
- 所有新报告自动显示专家团版本、发布日期、上一版本和版本差异
- 综合任务按 v1.0 成功模式强制执行 `TeamCreate → TaskCreate → 四位分析专家并行调度 → 四位真实回传 → 团长裁决 → delivery-review 独立复核`
- `TeamCreate` 缺失或失败时 fail closed，不允许团长以内联分段或岗位署名模拟专家协作。
- 每个成员必须保留 WorkBuddy 返回的 `agent_task_id`；最终报告直接列出各 Agent 子任务 ID，便于逐个打开核查。
- `delivery-review` 在四位分析专家完成并由团长裁决后才携完整材料创建；不再依赖无法保证的待命 Agent 二次唤醒。
- 最终交付前不执行 `TeamDelete`，确保子任务工作轨迹仍可查看。
- 综合模式六岗位必须全部具有独立 handoff；缺数据的岗位也必须参与并回传“数据不足”，不能从过程和报告中消失
- 报告列出六个岗位及其 `contributed / not_invoked` 状态、Agent 子任务 ID、贡献摘要和交接 SHA256
- 综合报告缺少必要成员交接时直接阻断，不能由总监模拟其他岗位
- `scripts/wait_for_agent_returns.py` 支持按 `attempt_id` 指定回传文件，并为韦交达使用独立 `delivery_review` 契约；主任务在四位分析专家与交付专家真实回传前保持同一执行回合。
- 综合报告要求每位成员携带 `agent_return_status / agent_returned_at / agent_return_file / agent_return_sha256`，缺任一回传凭证即 `collaboration_unreturned`。
- 综合任务第一可执行动作必须是 `TeamCreate`；若工具被延迟提供，必须先执行 `ToolSearch({"tool_names":["TeamCreate"]})`，再通过 `DeferExecuteTool` 建团。
- 未取得活动 `team_name`、或 Agent 返回 `No active team found` 时，在读取业务数据前返回 `collaboration_unavailable`，不允许团长单人替代。
- 新增 `scripts/public_output_guard.py`：所有公域报告和最终回复只允许出现当前 `client_scope` 授权的客户名称，跨客户命中即 `client_scope_leak_blocked`。
- 真实客户隔离名单移至本机私有目录 `~/.workbuddy/private/omni-ecom/client-brand-registry.json`；发布包只带匿名示例名单，也可用 `OMNI_ECOM_CLIENT_REGISTRY` 指向指定名单。
- 历史记忆和版式模板只复用匿名结构，不复用历史客户名称、数据和结论。
- 最终报告先冻结为 `R1/R2...` 候选稿，再由韦交达复核清单中列出的确切文件；不再先复核材料后生成报告。
- `scripts/review_guard.py` 使用 `prepare → attest-result → verify`；自由填写复核状态的 `attest` 已禁用，复核必须绑定 `review_attempt_id`、报告修订号和真实 Agent task ID。
- 复核后任一文件发生变化即 `review_stale_blocked`；必须升级报告修订号并新建韦交达子任务。
- `conditional_pass` 不等于通过；`review_release_verified` 后仍需公域隔离和最终完成闸门。
- 正式交付包含 `release-receipt.json`、`public-output-receipt.json` 和 `completion-receipt.json`，记录最新复核任务、六岗位贡献和产物哈希。

## 团队

- 沐风：任务拆解、数据裁决、交叉验证与最终报告
- 沈数清：数据质量、指标复算与经营归因
- 梁运通：天猫、京东、拼多多货架运营
- 洪涨声：抖音、视频号、小红书内容与直播
- 罗效盈：投流、单位经济与利润情景
- 韦交达：周报、月报、PPT、数据表与定版 PDF

## 推荐用法

1. 先指定客户范围和本次决策，不跨客户读取历史底稿。
2. 上传原始导出文件，不只上传截图或旧报告。
3. 说明平台、店铺、统计期间、任务类型和要支持的决策。
4. 先完成来源适配、资料清单、口径映射和数据质量闸门。
5. 闸门通过后，再进入领域分析、冲突裁决和报告交付。
6. 店铺诊断、周报、月报、季报、年报和大促复盘必须选择综合协作模式，并把各成员 sealed handoff 传给报告构建器。

示例：

- 审核这批天猫或京东原始报表的口径和数据质量，列出阻断项、可用指标与待补数据。
- 基于搜索渠道数据和完整成本，测算净 ROAS、可承受 CPC，并给出保守与进取方案。
- 基于通过数据闸门的本周数据，生成经营周报和带验收标准的行动清单。

## 能力模块

- `ecom-diagnosis-core`：资料体检、指标契约、确定性复算、数据质量闸门、证据与决策输出。
- `schemas/`：交接、运行记录和客户范围的机器可校验协议。
- `scripts/action_tracker.py`：仅按客户范围查看 1.x 行动历史；2.0 当前行动使用受控动作、资格检查、可信审批、执行网关与回读审计链，旧工具的创建/审批/流转/结果写入已停用。
- `scripts/platform_read_guard.py`：独立平台只读入口；把 mock 与 API 观察分开标记，固定客户/账号/店铺范围，校验读取时间和来源指纹，并确保凭证引用不进入输出。
- `scripts/model_route_guard.py`：用同客户、同任务、同岗位、同宿主的两个真实模型样本组做路线评估；样本或生产阈值不足时继续收集，达到条件也只提交人工审阅，不会自动换模型。
- `scripts/monitor_policy_store.py`：跨任务固定监测策略库；按客户追加策略版本和人工采用依据，阻止静默改阈值，并把旧 1.x 策略隔离为无当前效力的原字节历史。
- `scripts/build_report_package.py`：从通过校验的 handoff 生成下游统一报告包。
- `config/task-profiles.json`：统一八类经营任务的时间粒度、比较窗口、决策重点和默认协作模式。
- `scripts/task_profile_smoke.py`：校验八类任务是否齐全、综合/单点协作默认值和报告交付要求是否一致。
- `scripts/generate_pdf_report.py`：从 `report.json` 默认生成至少 3 张图表的 A4 PDF，并输出逐页渲染验收凭证。
- `scripts/collaboration_smoke.py`：验证综合任务不能退化为总监单人报告。
- `scripts/wait_for_agent_returns.py`：阻塞等待指定 Agent 的同一 run_id 完成凭证，超时 fail closed。
- `scripts/team_bootstrap_guard.py`：记录并核验真实 TeamCreate 结果，避免续跑时猜测团队身份。
- `scripts/collaboration_resume_guard.py`：只读判断中断运行可否安全续跑以及下一阶段。
- `scripts/resume_smoke.py`：验证五种续跑状态。
- `scripts/public_output_guard.py`：展示前执行客户名称隔离扫描，命中非当前客户名称时阻断且不回显该名称。
- `scripts/review_guard.py`：准备不可变复核清单、生成韦交达复核凭证，并在发布前检查复核是否过期。
- `scripts/analysis_depth_guard.py`：校验四份 sealed handoff 的个体分析深度，含基线包 SHA 绑定、L0-L4 层级达标、逐层证据、拆解维度、岗位最小分析集和结论自检七问。
- `scripts/analysis_depth_smoke.py`：回归测试深度缺失、L1 停在 L2 门槛、基线 SHA 不符、自检过弱、BLOCKED 降级和成员缺失。
- `scripts/conflict_scan.py`：扫描四份 sealed handoff 的数值、口径、方向和归因四类跨成员冲突，输出 `conflict-scan.json`。
- `scripts/conflict_scan_smoke.py`：回归测试无冲突、核心指标数值冲突、方向冲突、口径冲突、handoff 缺失和 run_id 不一致。
- `schemas/baseline-pack.schema.json`：共享口径基线包协议，四位成员分析前必须统一确认。
- `schemas/analysis-depth.schema.json`：个体分析深度声明协议。
- `schemas/conflict-scan.schema.json` / `schemas/conflict-verdict.schema.json`：冲突扫描结果与团长裁决书协议。
- `scripts/claim_guard.py`：校验数字来源、公式、输入 claim 和归因范围，输出 `claim-receipt.json`。
- `scripts/report_triage.py`：Stage 0 第一步，完整遍历上传目录，输出 `report-inventory.json`。支持 `--model-verdicts` 回填模型判定。
- `scripts/cluster_reports.py`：Stage 0 第二、三步，三轴归类并生成 `report-clusters.json` 与 `chapter-plan.json`。
- `scripts/coverage_guard.py`：Stage 0 第四步，分级阻断的覆盖闸门，输出 `coverage-gate.json`。可用报表无章节覆盖或数据不足报表未写全原因时返回 `coverage_blocked`。
- `scripts/claim_guard_smoke.py`：回归测试“GMV/访客误写转化率”“概览花费与流量 GMV 拼接 ROI”“未知数字硬编码”等失败场景。
- `scripts/completion_gate.py`：综合验证报告、PDF、数字来源回执、六岗位、复核回执和公域隔离凭证，只在全部通过后签发正式完成凭证。
- `scripts/release_acceptance_guard.py` / `release_acceptance_smoke.py`：核验 WorkBuddy 与 Codex 两条真实多专家 PDF 和独立复核证据；核心缺项、证据被改动或冒用 mock/合成标记即阻断。API、动作回读和模型路线是独立可选能力，未验收时标为 not_enabled，不阻塞报表版发布。
- `scripts/completion_gate.py --candidate-acceptance`：完整复用数字、PDF、多专家和独立复核检查，但只签发无正式交付权限的候选流水线验收凭证，避免“候选必须先发布才能验收”的循环。
- `scripts/release_guard.py` / `release_guard_smoke.py`：校验目录与最终 ZIP 的根结构、文件类型、缓存污染、版本和六岗位清单；正式 released 包还必须带有效的双宿主核心验收凭证。
- `scripts/runtime_acceptance.py`：在全新 WorkBuddy 会话中验证真实 TeamCreate、四分析专家首轮正式回传、韦交达复核与完成凭证。
- `connectors/`：端口与适配器契约，以及仅用于测试的 `mock-platform`。
- `version-info.json`：专家团版本和发布变更的唯一来源。
- `evals/`：脱敏行为属性用例和内置夹具；使用 `scripts/run_evals.py` 批量评测。
- `ecom-report-pdf-layout`：A4 电商经营报告的排版、图表与生成后验证。

## 安装与更新

将完整 `omni-ecom` 目录放入 WorkBuddy 的个人专家插件目录，再通过 WorkBuddy 专家管理能力执行校验和注册。更新后请新建或重载会话，使新角色定义生效。

## 发布前自检

- `plugin.json` 可解析，团队成员与 Agent 文件一致。
- 两个技能目录均包含合法 `SKILL.md`。
- 诊断脚本 `metric_gate.py --self-test` 通过。
- 原始适配脚本 `normalize_reports.py --self-test` 通过。
- 交接校验 `validate_handoff.py` 和行为评测 `scripts/run_evals.py` 通过。
- `scripts/analysis_depth_smoke.py` 与 `scripts/conflict_scan_smoke.py` 全部通过。
- 多 Agent 协作冒烟测试全部通过：综合报告具备团长、数据、平台、内容直播、投流利润的 sealed handoff，韦交达按独立 attempt 复核，最终完成凭证汇总六岗位。
- Stage 0 冒烟测试全部通过：遍历识别 6 个场景（含表头偏移、陌生结构进模型复核、空表与缺失降级、模型回填），归类与章节框架 7 个场景（含时间不重叠拒绝同比、未归类不丢弃、覆盖率 100%），覆盖闸门 7 个场景（含分级阻断的四条边界）。
- 打包前需先清理 `__pycache__`：发布守卫会拒绝 `.pyc` 文件，字节码混入会让 `release_guard` 直接判 FAIL。
- 每次真实运行都产出 `baseline-pack.json`、`depth-guard.json`、`conflict-scan.json` 与 `conflict-verdict.json`，且四份凭证都进入复核冻结清单。
- 行动审批与报告包验收通过：审批前不能执行，执行后必须有结果回写。
- Connector 冒烟测试通过：权限阻断、dry-run、幂等、对象定位和回读验证。
- 包级检查脚本 `scripts/validate_package.py` 通过。
- 头像为 PNG/JPG、512×512、单张不超过 500KB。
- 包内无客户名称、店铺 ID、密钥或本机私有数据路径。
- `claim_guard.py` 在缺来源、错误公式、跨来源/跨归因 ROI、未知数字和报告哈希变化时正确阻断。
- `completion_gate.py` 在缺数字回执、缺复核、公域隔离过期或任一产物哈希变化时正确阻断。
- 压缩包顶层结构为 `omni-ecom/...`。
- 发布目录和最终 ZIP 都通过 `scripts/release_guard.py`，不得含 `.gitkeep`、`.pyc`、`__pycache__` 或未允许文件类型。

WorkBuddy 重载后，运行 `scripts/verify_workbuddy_load.py`（兼容入口）或 `scripts/runtime_acceptance.py` 做真实多专家验收；只有读取到本轮 `team-bootstrap.json`、五位成员真实 task ID 和 `completion-receipt.json.status=formal_delivery_complete` 才是通过。空输出、超时、单总监回复或缺少运行凭证均不是加载成功。中断后先运行 `scripts/collaboration_resume_guard.py`，不要直接把旧目录当成新任务。
