# 更新日志 · office-token-booster

一键可复用的办公提效技能（执行 + 度量一体）。版本号遵循语义化，稳定点打 tag。

---

## v1.0.6 — 安全优化方案 P0 落地（权限收缩 / 扫描边界 / 写回加固 / 凭据面文本）（2026-10-08）

按 ClawHub 安全审计报告（Findings 33）归并出的 P0 项落地。**含两处行为加固**，其余为声明修正。

### 修复（必须项）

- **权限过度声明**：frontmatter 与 `config.yaml` 的 `tools` 移除 `shell`（实测发布面无子进程 / 系统命令 / 动态求值执行），仅保留 `filesystem`；`permissions` 由 `["."]` 改为「用户显式提供/指定的路径」，并注明不做目录遍历式扫描。
- **宿主用量读取收窄（隐私）**：`host_cost.LocalProvider` 由无边界 `rglob("*")` 改为 `_iter_trace_files()` **有界枚举**——深度上限 3 层、单次文件数上限 2000、只认 `.json/.jsonl/.log`（原实现还接受无后缀文件）、**跳过符号链接**（防止链接指向目录外）。保留对 `traces/<session_id>/trace_<hash>.json` 嵌套形态的支持（回归测试锁定）。
- **账本写回加固**：`append_entry` / `append_entries` 收敛到单一写入口 `_write_ledger_atomic()`，新增①`_validate_entry()` 写回前校验（数值字段不可识别则**拒写**，容许空条目与字段缺失，不改写调用方原值）②`_BACKUP_KEEP = 10` **备份配额**（写盘后淘汰更旧的时间戳备份，避免无界堆积）③`_load_or_empty()` 统一异常账本降级。
- **凭据面文本（第二次自伤）**：v1.0.5 修复说明里的赋值形态已改写为纯散文；v0.9.9 条目中的动态导入 / socket 前缀可执行形态改为散文描述；`RELEASE_NOTES` 中同类扫描结论表述一并改写。

### 声明修正（口径与实现对齐）

- `SKILL.md` 「数据最小化」由「不扫描技能目录以外的系统文件」改为准确语义：**只读写显式提供/指定的路径，不做目录遍历式扫描**；并新增三条独立条目——宿主用量接入需显式触发、宿主数据读取范围（只读 / 限定后缀与上限 / 只解析五类字段 / 不读提示词正文）、技能内部不执行系统命令（命令行由宿主或用户调用）。

### 测试

- `tests/test_v102_security_fix.py` 新增 `TestHostUsageScanBounded`（深度上限 / 后缀白名单 / 符号链接跳过）、`TestLedgerWriteHardening`（条目校验 / 备份配额 / 拒写不改文件），并加严文档守卫：补 `ASSIGN_INLINE`（**反引号包裹的赋值形态**——这正是 v1.0.5 漏检的形态）与 `EXECUTABLE`（动态导入 / socket 前缀 / 系统命令）两类检查，覆盖面从 7 篇扩到 9 篇随包文档。

---

## v1.0.5 — ClawHub 高危扫描整改：`suspicious.exposed_secret_literal`（2026-10-05）

针对 ClawHub 安全审计页 SkillSpector 静态分析的唯一一条 **Critical** 发现。**仅文档文本修正，零代码行为变更**（测试基线 186 passed / 3 skipped，另新增 7 例文档守卫）。

### 修复

- **`CHANGELOG.md` v0.9.9 条目（两处）**：原文在枚举 `security_preflight.py` 自身的 R3 检测模式时，把模式写成了「敏感名紧接等号再跟一串模式名」的链式形态，被静态扫描判定为**硬编码 API 密钥/令牌**。改为纯散文描述（「敏感名紧跟赋值号」的写法检测）并把完整模式清单指向 `scripts/security_preflight.py` 为准——**信息量不减，且不再呈现为凭据赋值**。

### 新增

- **`tests/test_v102_security_fix.py::TestDocsNoSecretLiteralPattern`**：对 7 个随包文档做「敏感名+赋值+字面量」与 5 类已知凭据前缀的回归守卫，防止以后改 CHANGELOG 时同类 Critical 复发（复发一次 = 一次新版本 + 一次重新审核）。已用修复前原文反向验证：旧文两行均被捕获，新文通过。

### 说明

- 该发现属**「语义上非真实凭据、但形式上确实命中扫描规则」**：仓库内无任何真实密钥（发布清单 23 文件凭据扫描命中 0），命中源是文档对**检测规则本身**的描述。
- 未采用「把文件排除出发布包」的规避方式——CHANGELOG 是用户需要的能力变更记录，排除它等于制造声明缺口；正确做法是让文本不再长得像凭据。

---

## v1.0.4 — 文档叙述清理 + ClawHub 分发裁剪（2026-10-04）

纯文档 / 打包面变更，**零代码行为变更**（全量测试基线 186 passed / 3 skipped 不变）。

### 变更

- **清理 SKILL.md 旧版本叙事残留**：移除小节标题与正文里的 `v0.x` 演化叙述（如「v0.3 长链路 Agent」「v0.4 粘合层」「v0.5 再往前一步」「v0.6 接宿主对话事件」「v0.7 去品牌化」、`ADR-9`、内部 `方向 B` 代号等），改为直接描述能力本身；小节标题一律去掉版本号前缀。
- **修正一处陈旧测试断言**：`tests/test_v09_skillmd.py` 曾硬编码断言 SKILL.md 必须出现旧标签 `任务执行（方向 B）`；改为断言能力表格通用的 `| 任务执行 |`，保留「能力表须列出已落地的任务执行能力 + 自动记账闭环」的本意守卫。
- **新增 `.clawhubignore`**（仅影响 ClawHub 分发包）：排除 `LICENSE`（全站强制 MIT-0，与仓库 MIT 条款冲突）、`scripts/clawhub_client.py` / `scripts/skillhub_client.py`（发布者自用上传客户端）、`scripts/security_preflight.py`（开发期预检脚本）、`tests/` 与开发期 requirements；SKILL.md 未将上述任一项声明为用户能力，故不构成「声明与内容不符」。
- **补齐跨平台声明一致性**：SKILL.md frontmatter 移除 `license: MIT`（ClawHub 不支持按技能覆盖许可证）并补 `metadata.openclaw.requires.bins: [python3]`（与核心脚本实际使用 Python 一致，`env: []` 亦与实际无环境变量读取相符）；同步移除 `network` 里「天禧AI 上架版」的单一平台措辞。

---

## v1.0.3 — 代码质量整改（clean-code 审计红/黄项清零）（2026-09-28）

纯重构，**对外行为等价**：CLI 参数、报告结构、问句应答、输出格式全部不变。
（本版另需一个版本号：天禧 AI 平台要求上传版本号严格大于已登记版本，同版本不允许覆盖。）

### 修复

- **`report_engine` 潜在崩溃**：两处内联推荐渲染仍在读取已删除的 `rec.install_cmd`（会抛 `AttributeError`）。统一改走 `format_recommendations_md()`，并保留「九、」编号标题与 🔴/🟠/🟢 优先级标识（与 HTML 口径一致）。
- **`skill_recommender` 不可达死规则**：`_GLOBAL_RULES` 中按金额触发的规则声明了 `threshold_cost` 与 `condition`，但代码只判断 `threshold_tasks` —— 该 CRITICAL 规则永不触发，`condition` 字符串从未被求值。已删除（账本无成本字段，按金额触发属新功能而非清理）。一并删除 `install_cmd` / `requires_confirmation` 死字段。

### 重构（无行为变化）

- **长函数拆分**：`qa.answer_followup` 改为表驱动（17 组关键词常量 + 路由表，162 → 19 行）；`diagnose.compute_summary` 抽聚合 helper（95 → 45 行）；`executor.main` 拆子命令（105 → 44 行）；`recommend_skills` 拆两个 matcher（64 → 26 行）。
- **消除重复**：`diagnose` 两段近似聚合循环合并为 `_group_sum` + `_with_saved`；`executor` 4 处引擎页脚抽取为 `_engine_footer()`。
- **魔法数常量化**：`qa` 内联关键词 → `_KW_*` 命名常量；`diagnose` 阈值 → 命名常量，且提示文案改为插值常量（防改常量后文案漂移）。
- **注释清理**：5 个核心模块 + 7 个外围模块共 **35+ 处** `S7/E3/S3/D1/E4/Issue #n/ADR-7/ADR-9/Phase N/v0.x` 工单式与版本号注释，改写为「为什么这样做」。

### 其他

- 删除失效脚本 `test_clawhub.py` 与 `test_phase2.py`（调用已移除的联网参数，早已无法运行）。
- 移除测试中对该死字段的构造与断言。

### 验证

- 全量 **186 passed, 3 skipped**（与整改前基线一致）。
- `qa` 模块 **54 组问句新旧输出逐句等价性比对，0 diff**（动了 15 个顺序敏感分支，单测不足以覆盖，从 git HEAD 取出旧模块对拍）。
- `security_preflight scripts` EXIT=0；`executor` CLI 五条路径冒烟全通。

---

## v1.0.2 — 修复 3 个 GitHub Issue + 移除冗余的安装确认 UI（2026-09-24）

千问办公实跑与 Issue 反馈驱动的修复补丁，未改任何对外能力边界。

### 修复（对应 GitHub Issue）

- **#1 周报分节误判**：`executor.classify` 增加完成动词语义门槛（`_RE_DONE_VERB`：发现 / 定位 / 修复 / 完成 / 已 / 上线 / 提交 / 解决 / 搞定 / 处理）。中性陈述句里的「问题 / issue」不再被抢进「风险与阻塞」节；显式锚点「风险：」仍优先。
- **#2 追问话术缺失**：`qa.answer_followup` 消耗分支补齐「最费 / 费token / 费钱 / 耗费最多」并排除「省」，节省分支补齐「最省 / 省最多 / 省得最多 / 最划算」，「最费 / 最省 Token」现已正确路由到对应口径。
- **#3 双层子弹**：`executor._lines` 用 `_RE_BULLET` 统一剥离行首列表标记（`- / * / + / • / · / 数字列表`），渲染层一处覆盖全部要点，用户粘贴自带「- 」时不再出现「- - 」。

### 其他

- 移除提效报告「推荐 Skill」卡片里的安装确认橙框（安装命令 + `.workbuddy` 安全提示）。推荐卡仍保留 Skill 名称、原因、预期节省、来源链接——用户要装可顺着来源自行安装。
- 新增 `tests/test_issue_parity.py`（7 条，含抽取 `SKILL.md` 示例问法的结构性防漂移断言），受影响旧测试全过（子集 49 passed / 2 skipped）。

### 安全合规

- 上架包未变：仍为纯本地运行，`network.outbound=false`，无联网客户端、无硬编码密钥、无绝对路径。

### 安全整改（对应天禧 AI 上架扫描报告，detailId 287056）

- **（中危）`report_engine.build_compare_card`**：「本期 vs 上期」对比卡的周标签（源自账本 JSON 的日期字段）未转义即拼入 HTML。已统一经 `esc()` 转义，与文件内其它用户字段同口径；新增恶意账本 XSS 回归测试。
- **（低危）声明与实现一致化**：移除 `report_engine.py` CLI 残留的联网开关、`skill_recommender.recommend_skills` 的联网搜索参数与 `skillhub_client` / `clawhub_client` 调用分支（两个联网客户端本就不在发行包内，此路径只会 ImportError）。推荐能力现为纯本地静态规则，无任何联网代码路径。
- **（低危→披露）第三方推荐如实标注**：报告的「推荐 Skill」节省数字引自第三方项目自述（README / benchmark），现于 Markdown 与 HTML 输出中明确标注「未经本技能实测验证，仅供参考」，`SKILL.md` 同步补充披露。
- **（信息）文档中的危险命令形态清理**：`CHANGELOG` 历史条目里描述「已移除的远程管道安装命令」时引用了命令原文字样，静态扫描按命令注入规则命中。已改写为不含可复制执行的命令形态的描述（历史事实不变，仅为不可执行的文字说明）。

---

## v1.0.1 — 接上类型字典 + 修复被静默跳过的执行引擎测试（2026-09-23）

装到千问办公后做冒烟时发现：`executor.py` 每次执行都打一句 `type_registry 加载失败，任务类型归一将退化为直匹配`。顺着这条告警挖出两个叠加的缺陷——**v0.5 的类型字典在执行层从未生效**，而且**负责守卫执行引擎的那份测试文件根本没被收集**。

### 修复

- **补齐缺失的 `scripts/type_registry.py`**：`executor.py` 从一开始就按 `from type_registry import load_registry, normalize_type` 写，但仓库里只有数据文件 `type_registry.json`，没有这个 `.py`（JSON 不能被 `import`）。于是那行 import 每次都抛 `ModuleNotFoundError`、被外层 `except` 静默吞掉，v0.5「查表代替猜」在执行层退化成 `_EXEC_ALIASES` 直匹配。新模块提供 `load_registry()` / `normalize_type()`，语义与 `conversation._load_registry` 一致，字典缺失/损坏/脏结构一律降级为空表、绝不抛异常打断任务。
- **`executor.py` 新增 `_REGISTRY_TO_EXEC` 桥接表**：字典用记账词表（文档撰写 / PPT制作），引擎用执行词表（文档整理 / PPT大纲），不桥接则字典命中也接不上。`代码编写`（交 IDE 类 Skill）与 `邮件草拟`（本技能 non-goal）**故意不桥接**，仍返回 `None`。
- **`conversation._load_registry` 改为委托** `type_registry.load_registry`，让 README 里「类型字典单一事实源」的说法真正成立（此前对话层与执行层各读各的）。
- **`SKILL.md` 断链修正**：`[QUICKSTART.md](../QUICKSTART.md)` → 同级 `QUICKSTART.md`（SKILL.md 本就在仓库根，这个链接在安装目录和仓库里都是断的）。

### 行为变更（patch 版本号下的唯一增量）

- 仅存在于字典别名中的说法现在能被执行引擎识别：`报表` → 数据分析、`写材料` → 文档整理、`做ppt` → PPT大纲（此前一律返回「不支持的类型」）。字典外的原有别名与子串兜底行为不变。

### 测试

- **修复 `tests/test_v10_executor.py` 被整份跳过**：文件第 253/269 行的**模块级** `pytest.importorskip("docx")` / `("openpyxl")` 会在可选依赖缺失时让**整个模块停止收集**，21 个执行引擎用例（含类型归一守卫）在干净环境下静默消失、且不计入失败。已把两处依赖检查移进各自用例内部，只跳真正需要它们的那 2 个用例。
- **新增 2 个回归用例**：`test_type_registry_actually_wired_into_executor`（断言字典真加载 + 只有走字典才可能命中的别名 + non-goal 类型不得被桥接）、`test_type_registry_loader_and_degradation`（文件缺失 / JSON 损坏 / 别名非列表三档降级）。守卫点刻意选在「旧实现必失败」的行为上，缺陷再溜不过去。
- 全量 **165 passed, 3 skipped**（本机未装 `python-docx` / `openpyxl` 两项可选导出依赖；补齐依赖后 168 passed, 0 skipped）。修复前为 142 passed——多出的 23 例正是被整文件跳过而隐身的执行引擎回归。

## v1.0.0 — 参赛版正式发布（2026-09-05）

对齐「参赛版」里程碑的正式发布，汇总自 v0.9.10 以来的全部能力并固化安全合规性，已通过天禧 AI 安全检测、可稳定上架技能广场。详见 [`RELEASE_NOTES.md`](RELEASE_NOTES.md)。

**关键变更（相对 v0.9.12）：**
- **版本号对齐为 `1.0.0`**：SKILL.md / config.yaml / CHANGELOG 统一 bump 至 `1.0.0`，与参赛里程碑同名，消除「版本≠能力」的观感（曾为 A 线 ADR-8 教训）。
- **安全合规修复（承接天禧 AI 安全检测报告）**：
  - `skill_recommender.py` 移除内置的「远程内容经管道交给 shell 执行」与「一键安装」类命令写法（此类写法属供应链投毒风险形态），改为静态「按官方说明手动安装」指引。
  - `conversation.py` 的 `while True:` 改为带显式 `running` 标志的循环。
  - `executor.py` 四处 `except Exception/except:` 改为具体异常类型并引入 `logging` 记录，不再静默吞错。
  - `SKILL.md` 中 `ledger.json` 示例路径统一改为 `examples/ledger.json`，新增示例账本文件。
- **新增 `RELEASE_NOTES.md`**：面向用户/参赛的完整发布说明。
- **测试**：全量 **166 passed, 0 failed**（含 15 项质量护栏回归）。

**安全自检**：`security_preflight scripts` → EXIT=0；上架包内联网/危险代码特征扫描 0 命中。

## v0.9.12 — 天禧AI 上架打包版（2026-09-04）

对齐已推送 tag `v0.9.12`，并为天禧AI 技能广场上架做打包收敛：

- **版本号对齐**：SKILL.md / config.yaml / CHANGELOG 统一为 `0.9.12`（此前与已推送的 `v0.9.12` tag 不一致）。
- **网络声明收敛**：`network.outbound` 由 `true` 改为 `false`。原联网推荐（clawhub.ai / lightmake.site 技能市场）指向非天禧市场，且为安全审核红旗；上架包中**移除** `clawhub_client.py` / `skillhub_client.py`，仅保留本地推荐逻辑（`skill_recommender` 离线分支）。核心执行/度量/报告全流程本就纯本地、不读密钥、不联网。
- **打包卫生**：上架 zip 仅含技能运行必需文件（SKILL.md / config.yaml / scripts/ 业务模块 / type_registry.json / 文档），排除 `__pycache__`、`.pytest_cache`、`allure-results`、`allure-report*.html`、`tests/`、`.github/`、`MANUAL_TEST_*`、`PUSH_TROUBLESHOOTING.md`、根目录 `test_phase2.py` / `test_clawhub.py` 等开发与测试产物。
- **安全自检**：`security_preflight scripts` 仍 EXIT=0（无 R1 危险执行 / R2 网络外发 / R3 硬编码密钥 红线）。

## v0.9.11 — 「不降质量」护栏度量（北极星质量极落地）（2026-09-04）

为北极星「在不降低交付质量的前提下，看清并降低 AI 使用成本/步骤」的质量极提供**可量化、零成本、可复现**的信号：每次 AI 交付后即刻评估其结构完整性，让「省了步骤/Token」的声明只有在质量保住时才可信。

### 新增 `scripts/quality.py`（自包含、无项目内依赖、无 LLM）
- 确定性结构清单，对渲染后的 markdown 做正则断言，**不调用 LLM**（避免重新产生 token 成本、需联网，直接违背北极星降本极）。
- 四类交付物各有专属清单：
  - **周报生成**：概览 / 重点工作非空 / 下周计划 / 风险与阻塞；
  - **会议纪要**：核心结论 / 待办事项 / 行动项有负责人或截止 / 参会与背景；
  - **数据分析**：关键指标表 + 无隐藏丢行（复用 S3 披露行）；
  - **文档整理**：要点≥3 + 要点有实质内容（平均长度≥12 字）。
- `QUALITY_FLOOR = 70`：低于此值，节省声明视为「不可信」（护栏触发）。
- **关键章节硬性门槛**：新增 `critical` 检查集——任一关键项失败则该份交付物直接判为不可信，即便总分过门槛。各类型关键项为：`周报→风险与阻塞`、`纪要→核心结论`、`数据分析→无隐藏丢行`、`文档整理→要点≥3`。 rationale：缺失这些章节即等于「质量没保住」，护栏必须对最该拦住的失效模式生效。
- `ScoreResult`：`score`(0–100, None=未测) / `checks` / `floor` / `critical` / `credible`(`score≥floor 且无关键项失败`) / `critical_failed` / `summary()`。

### 全链路打通
- `executor.execute()`：渲染后调用 `score_deliverable()`，把 `quality_score / quality_checks / quality_credible` 写入 `meta`；`execute_render` 返回三元组 `(ok, rendered, meta)`。
- `conversation`：execute 即时回显「质量分：X/100（门槛 达标/偏低）｜ 检查…」；`pending` 跨轮携带 `quality_score`，confirm 时透传给 `run_long_chain` 写入账本。
- `ledger_agent`：`propose_entry` / `run_long_chain` 新增 `quality_score` 入参（非 None 才落账）。
- `diagnose`：归一化 `quality_score`；聚合整体与分类型 `avg_quality`，`has_quality`；`Diagnosis` 加 `avg_quality / has_quality / quality_floor / quality_ok`。
- `report_engine`：护栏横幅三态——达标(绿)/节省不可信(红)/未测(灰)；类型表与任务表新增「质量分」列；Markdown 报告加「十二、质量护栏（不降质量）」节。

### 回归测试
- 新增 `tests/test_quality_guardrail.py`（15 项，allure 标记）：评分函数、executor meta、diagnose 聚合（avg=88/门槛击穿/无质量）、报告三态横幅、类型表列、会话往返。
- 全量套件 **166 passed, 0 failed**；`security_preflight scripts` 通过（无 R1/R2/R3 红线）。

- 版本号 `0.9.10 → 0.9.11`（config.yaml / SKILL.md）。

---

## v0.9.10 — 对抗式审查 S 级清理（S1–S7）+ 质量门禁 P1 脏数据修复（2026-09-02）

对抗式审查的 7 条 S 级（建议级）问题全部清零（纯工程清理、行为向下兼容），并补刀时间线五-B「质量门禁」flagged 的 **P1 字符串脏数据崩溃**：

### S 级建议清理（S1–S7）
- **[S1] REPL 双重 classify**：`conversation.main()` 此前在 `handle()` 内部 classify 一次、循环里又 `classify(line)` 一次（浪费 + 语义双源）。改为 `handle()` 接受可选 `intent` 参数，REPL 只算一次意图并透传。
- **[S2] `_do_execute` 冗余 `propose_entry`**：execute 意图下只为取 `date/note` 就跑了一整遍 `propose_entry`（含历史均值估算），其 `meta` 警告还被丢弃。改为直接构造 pending（今日日期 + 空备注），消除无谓计算。
- **[S3] `analyze_csv` 静默丢单元格**：ragged 行缺列 / 空单元格 / 数值列里的非数字此前被直接忽略、不告知。现累计 `dropped_ragged/empty/nonnum` 并在报告末尾披露「本次忽略 N 个单元格/单元」，让用户**看清**数据完整性（对齐北极星）。
- **[S4] HTML 转义校验**：复核 `report_engine.generate_html_report` 与 `executor._md_to_html`，所有用户字段（task_type/date/type/insights/recs/caveats）均经 `html.escape`；`_md_to_html` 先转义再注入 `<b>`，`<script>` 被转义为实体。新增回归测试锁定。
- **[S5] `export_docx` Intense Quote 样式缺失崩溃**：模板/Word 版本可能无「Intense Quote」样式，旧代码直接 `style="Intense Quote"` 会抛错。改为 `try/except` 回退默认段落样式（与表格样式降级一致）。
- **[S6] 热路径正则重复编译**：`_parse_number` 每次调用都拼接+编译正则；`_detect_type` 的短语抓取正则每次 `classify` 都重建。将 `_NUM_PREFIX_RE / _TOKEN_KW_RE / _MIN_KW_RE / _TYPE_EXTRACT_RE` 提到模块级预编译，调用处仅做关键词邻接校验。
- **[S7] `render_weekly_report` 函数内正则重建**：`_ANCHORS` 与兜底关键词原在每次渲染时 `re.compile`。提到模块级 `_WEEKLY_ANCHOR_PATTERNS / _RE_WEEKLY_*_KW / _RE_SPLIT_SEMICOLON` 预编译。

### 质量门禁 P1：脏数据崩溃
- **根因**：`diagnose()` 与 `report_engine` 直接对 `t.get("baseline_tokens", 0) or 0` 做加减，字符串值经 `or 0` 仍为真字符串，下游 `int ± str` 抛 TypeError（写回路径 `int()` 强转曾掩盖，读/计算路径未防护，异常账本仍会崩溃）。
- **修复**：在 `diagnose()` 读边界新增 `_normalize_tasks()`（配套 `_as_int()`），把 4 个数值字段统一 coerce 为 int（int/float/数字串 → int；None/空/非数字 → 0），入参不被改动；`report_engine` 消费归一化后的 `s.tasks`，渲染层一并免疫。
- **回归测试**：新增 `tests/test_p1_dirty_data.py`（字符串/缺失/非数字三类脏数据断言不崩溃且聚合正确）+ `tests/test_v095_s_suggestions.py`（覆盖 S1–S7，含 S2 断言 execute 不调用 `propose_entry`、S5 断言样式缺失回退、S3 断言脏数据披露）。

- 新增回归测试 `tests/test_v095_s_suggestions.py` 覆盖 S1–S7（含 S2 用 monkeypatch 断言 execute 路径不调用 `propose_entry`、S5 注入缺失样式断言回退、S3 注入脏数据断言披露）。
- 版本号 `0.9.9 → 0.9.10`（config.yaml / SKILL.md）。

---

## v0.9.9 — 对抗式审查整改：确认写回数据丢失 + 安全预检闸门加固（2026-09-02）

- **[C1] 修复确认写回静默丢弃 skill 成本（数据丢失）**：`conversation` 的 `confirm` 分支此前用「base_t 非空即不写回 skill」的互斥逻辑，导致同句同时给 skill+baseline（如 `确认 花了1800 token 5分钟 baseline 12000 token 25分钟`）时，用户显式输入的 skill 成本被吃掉、账本只记 baseline。改为**分段解析**——按首个 baseline 触发词切分，触发词之前=skill 段、之后=baseline 段，各自独立 `_parse_numbers`，互不吞。回归测试 `test_execute_confirm_keeps_skill_cost_with_baseline` 锁定 `skill_tokens=1800 / skill_minutes=5 / baseline=12000/25`。
- **[C2] 加固安全预检红线（CI 闸门此前名不副实）**：
  - R1 补「动态导入危险目标模块」的检测（旧正则仅认常见的 eval / exec / 系统调用三类，动态导入可等价绕过）。仅匹配危险目标模块名，避免误伤「打印到标准错误流」等良性用法。
  - R2 把 socket 相关检测从单一构造函数名扩展为整个 socket 模块前缀（覆盖建连与连接等入口），并补 urllib3 / pycurl / grpc / websocket / httplib2 等客户端（旧正则漏掉裸 socket 联网）。
  - R3 放宽密钥长度门槛（8→4 字符），并新增对「api key / access token / client secret / private key / token / pwd」等**敏感名紧跟赋值号**的写法检测（完整模式清单以 `scripts/security_preflight.py` 的 R3 规则为准）。
  - **文档去夸大**：模块 docstring 明确这是「轻量静态启发式，非安全保证」，可被字符串拆分/环境变量/编码绕过，仅拦低级手滑，不在承诺中称「零风险」。
- **[R1] 会议纪要 `_DECISION_RE` 移除过宽关键词「确认」**（极常见中文词，导致「请确认参会」等行被误判为核心结论）。
- **[R3/R4] 清理死代码**：删除 `render_ppt_outline` 从未使用的 `chunks` 变量；移除 `executor.py` 未使用的 `field` 导入。
- **[R5] 更新过期版本字符串**：`conversation.py` 文档/argparse banner 中残留的「v0.5」改掉（项目已 v0.9.x）。
- **[R6] 统一渲染入口**：`execute_render` 改为委托 `execute()`（单一渲染源），消除两套分发逻辑漂移；`execute()` 仍是返回 `(md, meta)` 的主入口（host_hook / 测试 / CLI 共用）。
- 全套测试 **142 passed**（原 139 + 新增 3 例：R1 `__import__` 命中、R2 `socket` 命中、C1 mixed skill+baseline 不丢成本），`scripts/` 安全预检 EXIT=0。
- 版本号 `0.9.8 → 0.9.9`（config.yaml / SKILL.md）。

---

## v0.9.8 — Bug #1 修复：baseline 分钟误归 skill（2026-09-02）

- **修复 `conversation._parse_baseline`**：紧凑写法 `确认 baseline 12000 token 25分钟` 中的「25分钟」此前被 `_parse_numbers` 误判为 skill 分钟写入账本（baseline_minutes=0, skill_minutes=25）。改为**段式解析**——锁定首个 baseline 触发词（基准/手搓/baseline/笨办法）之后的子串，在该子串内统一解析 token/分钟，使「触发词 … token … 分钟」任意间隔都正确归 baseline。
- **回归测试**：`tests/test_v097_execute.py::test_execute_baseline_minutes_not_misrouted` 锁定 `baseline_tokens=12000 / baseline_minutes=25 / skill_*=0`。
- **测试健壮性**：`test_security_preflight._write` 改用独立临时子目录写入，杜绝 TEMP 同名残留导致的 rename 冲突（FileExistsError）。
- 全套测试 138 passed，零回归。
- 版本号 `0.9.7 → 0.9.8`（config.yaml / SKILL.md）。

---

## v0.9.7 — Phase 3 落地：execute 意图路由 + 安全预检 + QUICKSTART（2026-08-26）

完成 **Phase 3** 三项内容（原计划 10–11 月，提前至 v0.9.7），并补上独立快速开始文档。

### 对话编排层 · execute 意图路由（方向 B 闭环关键一环）
- `conversation.classify` 新增 `execute` 意图：自然语言「帮我写周报 / 整理会议纪要 / 分析 CSV / 提炼要点 / 出 PPT 大纲」自动路由到 `executor` 渲染交付物，再走 `run_long_chain` baseline 护栏自动记账。
- 新增 `_EXEC_RE` / `_EXEC_SYNONYMS` 识别执行类中文触发词；`resolve_exec_type` 归一类型、`execute_render` 公共 API（供编排层安全调用，不碰私有 `_DISPATCH`）。
- **防账本污染护栏**：`confirm` 分支新增「成本完整性」校验——当 skill 与 baseline 的 token/分钟均为空或 0 时，**拦截写回**并提示补成本，避免空账本出现全零/负节省记录。
- 收窄 `record` 正则：移除裸词「记账」，避免执行内容里含「记账」二字被误路由到记账意图。
- `conversation._do_execute`：渲染后存入 `state["pending"]`，提示预览 + 要 baseline，确认才落盘。

### 执行层安全预检（四红线）+ CI 闸门
- 新增 `scripts/security_preflight.py`：扫描 `.py` 文件检测 R1 危险执行（求值执行、系统命令调用、动态导入）、R2 网络外发（常见 HTTP 客户端与原始 socket 调用）、R3 硬编码密钥（云厂商 AKIA 前缀、`sk-` / `ghp_` / `xox` 风格令牌、JWT，以及各类 password / secret 赋值写法）、R4 `html.escape` 转义（仅告警）。
- 白名单：`security_preflight.py` / `test_security_preflight.py` 豁免 R1；`skillhub_client.py` / `clawhub_client.py` / `security_preflight.py` / `test_security_preflight.py` 豁免 R2（设计内允许联网的搜索客户端）。
- `.github/workflows/ci.yml` 新增 `security` job，在 `deploy-pages` 前跑 `python scripts/security_preflight.py scripts`，**须 0 红线才放行**。
- 当前 `scripts/` 实测通过预检（0 红线，仅 4 处 R4 转义告警）。

### 文档
- 新增独立 **[QUICKSTART.md](QUICKSTART.md)**：5 分钟跑通「初始化账本 → 执行任务 → 确认写回 → 看提效报告」闭环；含环境要求、常见任务示例表、PowerShell/Windows 注意事项、安全红线说明。
- `README.md`「快速开始」改为方向 B 视角并链接 QUICKSTART；`SKILL.md`「快速开始（QUICKSTART）」补 execute→bookkeep 步骤并链接独立文件。
- `docs/v1.0.0-prelaunch-plan.md`：Phase 3 三项全部勾选（含 PPT 大纲模块补勾，代码其实已在 Phase 2 随 executor 落地）；质量门禁「安全预检脚本」项勾选。

### 测试
- 新增 `tests/test_security_preflight.py`（6 例：R1/R2/R3 检测、R2 联网白名单豁免、干净文件通过、scripts/ 实测通过）。
- 新增 `tests/test_v097_execute.py`（6 例：意图分类、渲染交付物、缺成本拦截写回、带 baseline 写回、CSV 路由、PPT 不被「记账」误路由）。
- `tests/test_boundary.py` 超长文本分类断言补 `execute` 意图（边界测试覆盖新意图）。
- 全套测试 **138 passed**（126 → 138，新增 12 例），零回归。

---

## v0.9.6 — 执行引擎增强 + 缺陷修补（2026-08-27）

方向 B（执行 + 度量）执行引擎打磨，**修复实测暴露的功能级缺陷（D1/D2）+ 三处增强（E1–E4）**。
全套测试 123 → **126 passed**（新增 3 例 D1 回归），零回归。测试 2 / 测试 3 已用修正后正道命令复验通过。

### 安全修复（CodeQL CWE-20）
- **S1 · 修复 `skillhub_client.py` URL 子串消毒不完整**
  - 原代码 `if homepage and "github.com" in homepage:` 仅做子串包含判断，可能导致任意位置含 `github.com` 的恶意 URL 被误判为合法 GitHub 仓库。
  - 改为 `urllib.parse.urlparse(homepage).hostname`，并对 hostname 小写归一化后仅接受 `github.com` 或 `*.github.com`；解析异常兜底为 `None`。
  - 修复 GitHub CodeQL 告警 *Incomplete URL substring sanitization #1*。

### 缺陷修补（D1–D2，实测 Test 2/3 根因）
- **D1 · 新增「一等创建空账本」命令 `--init-ledger`（Test 2/3 根因修复）**
  - 此前用户只能用 `echo {"tasks":[]} > 账本.json`（PowerShell 下报语法错）或 `python -c "open(...).write('{\"tasks\":[]}')"`（PowerShell 下 `\"` 未转义致 SyntaxError）来建账本，两个写法在用户真实环境均失败。
  - 新增 `executor.py --init-ledger <path>`：写入 `{"tasks":[]}`（UTF-8、ensure_ascii=False），父目录自动创建；账本已存在时幂等跳过不覆盖。执行引擎首次记账不再依赖脆弱 shell 命令。
- **D2 · E4 友好提示改为推荐 `--init-ledger`**
  - 原 E4 提示里教用户 `echo {"tasks":[]}` ——正是 Test 2 在 PowerShell 失败的命令。改为推荐安全的 `.venv\Scripts\python scripts\executor.py --init-ledger <path>`。

### 增强（E1–E4）
- **E1 · 打通自动记账闭环（功能级修复）**
  - `executor.propose_ledger` 新增 `baseline_tokens` / `baseline_minutes` 参数并透传给 `ledger_agent.run_long_chain`。
  - CLI 新增 `--baseline-tokens` / `--baseline-minutes`；配合 `--confirm-ledger` 即可在**空账本**上真正写回（此前因 P0 护栏永远拦截 baseline 缺省条目，执行引擎的自动记账对首条记录是条死路）。
  - 不传 baseline 时仍走 P0 护栏拦截（不污染账本），行为向后兼容。
- **E2 · 修复「已拦截：None」**
  - `executor.py` 误读 `res.get('reason')`，实际键名为 `block_reason`；改为 `res.get('block_reason') or res.get('reason')`，拦截时显示真实原因。
  - 连带修复 `host_hook.py` 同款键名 bug。
- **E3 · 周报引擎行内锚点增强**
  - `render_weekly_report` 按 `；`/`;` 拆分一行内的多个要点，分别归类；识别行内前缀 `风险：`/`下周：`/`阻塞：`/`概览：` 等路由。
  - 修复测试1 中「一行混合要点被整行抢走、丢失『风险与阻塞』段」的问题。
- **E4 · 缺失账本文件友好提示**
  - `--apply-ledger` 指向不存在文件时，捕获 `FileNotFoundError` 输出友好提示（推荐 `--init-ledger`），不再抛出原始栈；交付物照常生成，仅跳过记账。

### 测试
- 新增 3 例 D1 回归：`--init-ledger` 建空账本 / 对已存在账本幂等跳过 / init→带 baseline 写回→report_engine 生成 HTML 全闭环。
- 既有 E1–E4 共 5 例回归不变。

---

## v0.9.5 — 执行引擎落地（方向 B，稳定点）

- 任务执行引擎 `executor.py`：周报 / 会议纪要 / 数据分析（CSV 本地计算）/ 文档整理 / PPT 大纲 五大模块，纯标准库、零依赖、不联网、不读密钥。
- 执行 + 度量闭环：执行完任务可选自动记回 ledger（复用 `run_long_chain` P0 护栏，默认 dry-run）。
- 可选富格式导出 docx / xlsx（缺失优雅降级为 md / csv）。
- 宿主钩子 `host_hook.on_executor_completed` 复用 v0.7 事件 cost 形态直接记回。
- 测试套件达 118 例（含 17 边界 + 13 跨 Agent 可移植）。

> 更早版本（v0.5–v0.9.4）演进见 README「演进路线」。
