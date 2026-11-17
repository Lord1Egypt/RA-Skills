# 办公室提效助手（office-token-booster）

> 把重复办公任务交给技能，把省下的 Token 和時間看得見。

> 🏷️ **当前版本：v1.0.0**（参赛版正式发布 · 2026-09-05）｜ 完整发布说明见 [`RELEASE_NOTES.md`](RELEASE_NOTES.md)

`office-token-booster` 是一个面向**办公生产力**场景的 AI 技能（OpenClaw格式），
帮你把会议纪要、Excel 数据分析、周报、文档提炼等重复任务自动化，并**量化每次任务节省的 Token 与耗时**。

本技能是 `agent-analytics-report`（AI 助手用量分析报告）的**姐妹产品线**——
两者复用同一套「报告渲染 + 异常检测」思路，但定位完全不同：

| 产品线 | 平台 | 定位 |
|--------|------|------|
| `agent-analytics-report` | 通用 Agent 宿主 | 分析 AI 助手自身用量与成本 |
| `office-token-booster` | 天禧 AI / OpenClaw | 办公任务自动化 + 提效可视化 |

## 特性

- 🗂️ **办公任务自动化**：会议纪要、数据分析、周报、文档提炼
- 📊 **提效可视化**：内置「提效账本」，把节省的 Token / 耗时算清楚、画出来
- 🔒 **本地优先**：报告本地生成，不联网、不上传你的内容
- 🧩 **OpenClaw 格式**：可直接提交天禧 AI 技能广场 / ClawHub

## 快速开始

本技能**既帮你做**办公任务（周报/纪要/数据分析/文档整理/PPT 大纲），**又自动记下**每次帮你省了多少 Token/时间 —— 执行与度量一体。

最快上手方式：看 **[QUICKSTART.md](QUICKSTART.md)**，5 分钟跑通「初始化账本 → 执行任务 → 确认写回 → 看提效报告」闭环。

```bash
# 1) 初始化空账本（仅首次）
python scripts/executor.py --init-ledger ledger.json

# 2) 执行任务，拿到交付物（不写账本）
python scripts/executor.py --type 周报生成 --input 本周事件.txt --output 周报.md

# 3) 预览并确认写回（执行 + 自动记账，默认 dry-run）
python scripts/executor.py --type 周报生成 --input 本周事件.txt \
  --apply-ledger ledger.json --skill-tokens 1800 --baseline-tokens 12000 --baseline-minutes 25 --confirm-ledger

# 4) 看提效报告（HTML）
python scripts/report_engine.py ledger.json --format html --output 提效报告.html
```

如果你是天禧 / OpenClaw 宿主用户，直接说「帮我写一份周报」「整理一下会议纪要」「分析这个 CSV」即可触发，技能默认走 **dry-run 预览 + 确认写回**，不污染账本。

## 使用示例

下表列出在天禧 / OpenClaw 中**直接说出**即可触发本技能的提示词，及其对应的真实行为：

| 你想做的事 | 说这句话 | 技能会做什么 |
|-----------|---------|------------|
| 查看本机用量 | "我最近 7 天用了多少 Token？" | 只读本机宿主用量，聚合近 7 天 Token / 耗时（零上传）|
| 用量可视化 | "把我的 AI 用量做成图表" | 生成按日 / 按模型的 Token 消耗图 |
| 生成提效报告 | "生成我的提效报告" | 基于账本 baseline 出 HTML 提效报告（节省 Token / 率 / 趋势）|
| 追问最费任务 | "哪个任务类型最费 Token？" | 锚定内核结构化回答，按**实耗**排序（已修「消耗/节省」语义坑）|
| 找自动化对象 | "哪种办公任务最该自动化？" | 按历史基线排出最该做成模板的 Top N |
| 导入真实用量 | "把本机最近 7 天宿主用量导入账本" | dry-run 预览草稿，确认后才落盘 |
| 顺手记账 | "我刚写完周报，用 AI 花了 1800 token" | 识别为完成事件，建议记账（确认才写回）|

> **边界（执行 + 自动记账）**：本技能**既帮你做**周报/会议纪要/数据分析/文档整理/PPT 大纲，又**自动记下**每次帮你省了多少 Token/时间（闭环走账本护栏，默认 dry-run）。不代发邮件、不删文件、不连外部数据库改数据、不做专业排版/多模态生成——这些交给对应专业 Skill。

本地也可直接用 CLI 验证（零依赖，Python ≥3.10）：

```bash
# 读真实用量（只读，不写盘）
python scripts/host_cost.py --days 7

# 生成提效报告（需 ledger.json）
python scripts/report_engine.py ledger.json --format html --output 提效报告.html

# 执行办公任务（方向 B 核心）：内容类走模板渲染，数据类走本地 stdlib 计算
python scripts/executor.py --type 周报生成 --input 本周事件.txt --output 周报.md
python scripts/executor.py --type 数据分析 --input 销售.csv --output 分析.md
# 执行完顺手记账：--apply-ledger 走账本护栏（baseline 缺省拦截），默认 dry-run 预览
python scripts/executor.py --type 会议纪要 --input 转录.txt --apply-ledger --skill-tokens 1800

# 可选导出（缺失 python-docx/openpyxl 时自动降级为 md/csv，零依赖默认不受影响）
python scripts/executor.py --type 周报生成 --input 本周事件.txt --output 周报 --format docx
python scripts/executor.py --type 数据分析 --input 销售.csv --output 分析 --format xlsx
```

## 目录结构

```
office-token-booster/
├── SKILL.md              # OpenClaw 格式技能定义 + 对话式诊断流程
├── config.yaml           # 替代原 config.json
├── scripts/
│   ├── diagnose.py       # 诊断内核（纯函数）：ledger -> Diagnosis，含 baseline 护栏 + 方法论说明
│   ├── report_engine.py  # 渲染层：消费 Diagnosis 产出完整报告 / 一页摘要（MD/HTML）+ JSON
│   ├── qa.py             # 对话式追问外壳：answer_followup(diagnosis, question)，锚定 Diagnosis 不编造
│   ├── ledger_agent.py   # 长链路 Agent（v0.3）：建议生成 + 写回账本（默认 dry-run，--apply 才写）
│   ├── conversation.py   # 对话编排层（v0.4）：意图路由，把 qa/报告/Agent 串成单一对话流，不改三层一行
│   ├── skill_bridge.py   # Skill 触发流（v0.6）：把宿主对话事件翻译成 conversation.handle() 调用，自动建议记账
│   ├── host_hook.py      # 宿主钩子示例（v0.7）：平台无关适配器，把宿主完成事件（含真实用量）接进 skill_bridge
│   ├── executor.py       # 任务执行引擎（v0.9.6 方向 B）：按 task_type 分发，模板渲染 / 本地 stdlib 计算 + 自动记账闭环
│   ├── type_registry.py  # 类型字典加载器：读 type_registry.json，提供 load_registry / normalize_type（executor 的执行层归一入口）
│   └── type_registry.json# 类型字典（v0.5）：标准类型名 ↔ 别名/关键词，消除自然语言记账的类型歧义
├── tests/
│   ├── test_v05.py       # v0.5 实地测试：自带临时账本跑完整流程，断言类型字典消歧 + 三层一致
│   ├── test_v06.py       # v0.6 实地测试：触发流高/中信心触发、非完成不触发、dry-run、确认后三层一致；
│   │                     #   另含「产品 HTML 报告附件」「数据可信度护栏」两个作品集展示用例
│   ├── test_v07.py       # v0.7 实地测试：断言真实用量事件 cost_source=event、写回采用宿主实测、三层一致、源码去品牌化
│   ├── test_v08.py       # v0.8 实地测试：提效洞察可视化——趋势折线图、周期对比卡、ROI 优先级卡、QA 意图分支
│   ├── test_v09_host_cost.py     # v0.9 宿主用量接入核心测试（10 例）
│   ├── test_v09_host_cost_realformat.py  # v0.9 真实嵌套格式兼容测试（3 例）
│   ├── test_v09_qa_consumption.py  # v0.9 QA 消费/节省意图路由测试（6 例）
│   ├── test_v09_skillmd.py       # v0.9 SKILL.md 定位一致性测试（4 例）
│   ├── test_v091_skill_recommender.py  # v0.9.1 Skill 推荐引擎测试（13 例）
│   ├── test_v092_skillhub_client.py  # v0.9.2 SkillHub 客户端测试（3 例）
│   ├── test_v093_clawhub_client.py   # v0.9.3 ClawHub 客户端测试（3 例）
│   ├── test_v10_executor.py # v0.9.5 执行引擎测试（15 例）：5 模块渲染结构 + CSV 指标 + 自动记账闭环 + baseline 护栏 + HTML 转义 + docx/xlsx 可选导出降级 + 宿主钩子 event cost 记账
│   ├── test_boundary.py  # 边界/负向测试（17 例）：极端输入、畸形数据、空值降级
│   ├── test_portability_cross_agent.py  # 跨 Agent 可移植性测试（14 例）：适配器协议、通用 provider
│   ├── test_renderer.py  # 渲染器冒烟测试（L6）：内置最小 allure-results fixture → 断言产出 HTML 含用例名/状态/环境/分类
│   └── helpers.py        # 测试共享辅助：账本读取、Allure 附件（JSON/TEXT/HTML）、Token 节省率图表
├── tools/
│   └── render_allure_html.py  # 零依赖 Allure→HTML 渲染器：把 allure-results 生成单个自包含 allure-report.html（无 Java）
├── references/           # 扩展文档
├── code_review_adversarial.md # 对抗式代码审查报告（正确性/健壮性/安全/架构 + 作品集增强建议）
├── README.md
└── LICENSE
```

> 三层解耦：`diagnose.py`(内核) 是「对话式诊断」「长链路 Agent」「对话编排」三个外壳的共享内核，
> 后加能力时只需消费内核，既有三层代码不受影响（见 `产品发展计划时间线_双产品线.md`）。

## 合规

- 全部本地处理，无外联、无硬编码密钥。
- MIT 协议，自研代码，可自由学习 / 修改 / 再分发。
- 节省值为用户自行估计的基准对比参考，**非平台计费数据**。

## 测试（pytest + Allure）

测试套件覆盖 v0.5–v0.9.5 的核心能力，并强制守卫「确认消息 / 摘要报告 / 内核 Diagnosis 三层数字同源（误差 < 0.05pp）」与「触发默认 dry-run 不改账本」等不变量；另含 **17 个负向/边界测试**（`test_boundary.py`）专门验证极端输入、畸形数据与空值下的优雅降级。**13 个跨 Agent 可移植性测试**（`test_portability_cross_agent.py`）守卫宿主适配器协议与通用 JSON provider 的兼容性。共 **166 个用例**（质量护栏 15 + 负向/边界 17 + 跨 Agent 可移植 13 + 各版本能力套件其余 121），全绿。三层一致测试改为**直接比对内核重算值**（不再靠正则抓文案），文案改动不会让测试误伤。

每个用例在报告里额外携带：

- `@allure.epic("office-token-booster")` + `@allure.label("layer", …)`：架构分层标签（内核层 / 编排层 / 触发层 / 宿主适配层 / 适配层 / 写回层 / 渲染层），方便按层筛选；
- `@allure.label("test_type", …)` / `component` / `risk_area` / `priority` / `suite`：一组**多维度标签**（详见 [`docs/allure-labels.md`](docs/allure-labels.md)），可按「正向/负向/边界/回归」、被测模块、业务风险域、优先级、版本套件在报告里分组/筛选，方便作品集展示测试设计思路；
- `@allure.link(...)`：源码链接，直接跳到被测函数对应行（URL 自动锚定当前 git commit SHA，本地无 git 时退化为无操作）；
- `feature/story/severity/description/step/attach`：可读的「做了什么、看到了什么」。

> 源码链接、分层标签与多维度标签由 `tests/helpers.py` 的 `src_link(...)` 助手统一注入；`tools/render_allure_html.py` 会在报告里渲染出「🔗 源码」与「层 / epic / feature / story / severity / test_type / component / risk_area / priority / suite」等徽章，审阅者在作品集里可一键溯源与按维度浏览。

**环境准备**（项目已自带 `.venv`，含 pytest 9.1.1 + allure-pytest 2.16.0）：

```bash
cd office-token-booster
python -m venv .venv && .venv\Scripts\activate      # Windows；mac/Linux 用 source .venv/bin/activate
pip install pytest allure-pytest
```

**运行：**

```bash
# 仅跑测试（不生成 Allure 数据）
python -m pytest tests/ -v

# 生成 Allure 原始数据
python -m pytest tests/ -v --alluredir=allure-results
```

**标记（markers）：** `smoke`（冒烟）/ `integration`（集成）/ `regression`（回归）。可用 `-m smoke` 仅跑冒烟。

**各版本测试要点：**

| 版本 | 文件 | 守卫点 |
|------|------|--------|
| v0.5 | `test_v05.py` | 类型字典消歧（「生成了周报」→「周报生成」）、三层数字一致、对话流（追问/建议/退出） |
| v0.6 | `test_v06.py` | 完成信号识别器、触发路由（高/中信心触发 + 字典兜底 + 非完成 passthrough + dry-run）、确认写回与三层一致；**另含「产品 HTML 报告附件」「数据可信度护栏」两个作品集展示用例** |
| v0.7 | `test_v07.py` | 真实用量 `cost_source=event`、文本成本回退 `text`、写回条目采用宿主实测、三层一致、源码去品牌化（防回归） |
| 边界/负向 | `test_boundary.py` | 跨模块极端输入与畸形数据：空/None/负数/超大数/损坏 JSON/零基线/空账本等，验证「优雅降级不崩溃」；全维度打标（layer/test_type/component/risk_area/priority/suite） |
| v0.8 | `test_v08.py` | 提效洞察可视化：趋势折线图（`build_trend_line_chart`）、本期 vs 上期周期对比（`compute_period_compare` / qa「比上周」意图）、按 ROI 排序的自动化优先级（`compute_roi_targets` / `ledger_agent.propose_automation_targets`）；单周数据降级为「周数据不足」友好提示；全维度打标 |
| v0.9 | `test_v09_host_cost.py` ×9 + `test_v09_host_cost_realformat.py` ×3 + `test_v09_qa_consumption.py` ×6 + `test_v09_skillmd.py` ×4 | 真实宿主用量接入：`host_cost` 只读本机宿主 traces/db/usage-log（含 `EventCostProvider` / `LocalProvider` / `draft_entries_from_host`，容忍脏数据·超窗·无数据降级不崩）；触发流 `cost_provider` 补全实测成本且向后兼容 `None`；`ledger_agent.import_host_usage` dry-run 不写盘；SKILL.md 定位 Option C 一致性（禁止未实现执行器承诺、含 QUICKSTART 与「可选只读本机宿主用量」声明）；QA 消费/节省意图路由；全维度打标 |
| v0.9.1 | `test_v091_skill_recommender.py` | Skill 推荐引擎：任务类型匹配（代码/对话/终端/周报）、优先级排序、格式化输出（MD/HTML）、空数据处理、最大推荐数限制；全维度打标 |
| v0.9.2 | `test_v092_skillhub_client.py` | SkillHub 客户端：搜索接口返回结构校验、结果字段完整性、安装提示格式化含技能名 |
| v0.9.3 | `test_v093_clawhub_client.py` | ClawHub 客户端：搜索接口返回结构校验、结果字段完整性、安装提示格式化含技能名 |
| v0.9.4 | `test_v094_gate.py` | **v1.0.0 质量门禁回归**：P0 缺省 baseline 写回护栏（拦截污染账本）/ P1 确认词收窄（记账优先、强确认词）/ P2 HTML 注入转义（用户字段 `html.escape` + 联网 URL 仅允 http(s)） |
| v0.9.5（方向 B） | `test_v10_executor.py` | **任务执行引擎**：5 模块渲染产物结构（周报/纪要/数据分析/文档整理/PPT 大纲）、CSV 指标计算（sum/avg/min/max/median）、自动记账闭环（propose_ledger 走 `run_long_chain` 护栏，baseline 缺省拦截不污染账本）、dry-run 预览不写盘、用户内容 HTML 转义防 XSS、**docx/xlsx 可选导出优雅降级**（缺失依赖回落 md/csv）、**宿主钩子 `host_hook.on_executor_completed` 用 event cost 自动记账**；全维度打标 |
| 可移植性 | `test_portability_cross_agent.py` | 跨 Agent 适配器协议：最小 Provider 满足接口、真实 Provider 均通过、跨 Agent 闭环、OpenAI 格式兼容、通用 JSON provider、优雅降级未知宿主、去重逻辑、CLI 参数校验 |

> 每个用例都通过 `allure.feature/story/severity/description/step/attach` 在报告里给出可读的「做了什么、看到了什么」，方便非技术评审直接看懂。

## 分享测试报告（作品集）

本仓库提供一个**零依赖**的渲染器，把 Allure 原始数据变成**单个自包含 HTML**，无需 Java、无需 allure CLI、无外部 CDN，可离线双击打开，也适合直接发出去给人看。

```bash
# 1) 跑测试生成 allure-results/（见上）
# 2) 渲染成单个 HTML（默认读取 ./allure-results → 输出 ./allure-report.html）
python tools/render_allure_html.py --results allure-results --output allure-report.html
```

**为什么不用 `allure serve`？** `allure serve` 需要本地装 Java + allure 命令行、还要起一个本地服务，发出去给别人看很不方便。单文件 `allure-report.html` 则可以：

- 直接双击在浏览器打开演示；
- 提交进 Git 仓库，或部署到 **GitHub Pages / Netlify / 任意静态托管**，附上链接即可作为作品集；
- 报告已自动注入运行环境（Python / pytest / allure / git commit）与失败分类（categories），观感接近官方 Allure。

> 提示：本地多次运行 `--alluredir` 同名目录可能累积历史结果；渲染前建议用全新目录（如 `ar_run1`）或在 CI 里每次清空。渲染器对重复结果会按文件如实呈现，建议保证 `allure-results/` 下每个用例仅一份 `*-result.json`。

### 自动生成（CI 串联）

本仓库内置 GitHub Actions（`.github/workflows/ci.yml`），每次 push / PR 到 `main` 自动：

1. 安装 `requirements-dev.txt`（pytest + allure-pytest）；
2. 跑全套测试并生成 `allure-results/`；
3. 用 `tools/render_allure_html.py` 渲染出**单个自包含 `allure-report.html`**，作为可下载的 **Allure HTML report** 构件（Artifacts）；
4. 校验提交信息是否符合 Conventional Commits（见下）。

```bash
# 本地一键复现 CI 的产物
python -m pytest tests/ -q --alluredir=allure-results
python tools/render_allure_html.py --results allure-results --output allure-report.html
```

**部署到 GitHub Pages（作品集公开链接）：** 在仓库 **Settings → Pages → Source** 选「GitHub Actions」，再创建一个仓库变量 `ENABLE_PAGES=true`，CI 的 `deploy-pages` 作业即会把报告发布到 `https://<user>.github.io/office-token-booster/`。未开启时 CI 仍正常出 Artifact，不影响测试门禁。

## 提交规范（Conventional Commits）与 CI

为让作品集的提交历史可读、可自动归类，本仓库采用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <subject>
# 例：
feat(skill_bridge): 新增宿主真实用量 cost_source 路由
fix(conversation): _parse_numbers 支持小数与万/千单位
test(v06): 增加成本解析健壮性回归用例
docs(readme): 补充 CI 与分享报告说明
ci: 新增 pytest + allure 自动渲染工作流
```

- `type` ∈ `feat` / `fix` / `test` / `docs` / `refactor` / `style` / `perf` / `build` / `ci` / `chore`；
- `scope` 可选，建议填受影响模块（如 `skill_bridge`、`v06`、`ci`）；
- CI 用 `.github/commitlint.py` 校验，不符合格式会**标红**（Merge / Revert 提交自动跳过）。

## 代码质量与清理

- 已删除与 `report_engine.py` 重复的死代码 `scripts/saving_report.py`（不再被任何模块引用）；
- 复用取代重复：`report_engine` 直接 `from diagnose import _safe_div`、`skill_bridge` 复用 `conversation._REGISTRY`（类型字典单一事实源）、测试公共辅助抽到 `tests/helpers.py`（DRY）；
- 对抗式代码审查与后续改进建议见 `code_review_adversarial.md`。

## 演进路线

- v0.1.0：技能骨架 + 提效账本报告引擎 + 办公任务定位
- v0.2（已完成）：对话式诊断 —— 三层解耦（diagnose 内核 / report_engine 渲染 / qa 追问）；一页摘要首屏（`--summary`）+ 完整报告双模板；追问语料丰富（总览/比例/类型排名/自动化优先级/周趋势/明细/最差场景/耗时/方法论/可信度/完整报告路由）；报告内置 baseline 护栏与「方法论说明」，主动暴露"节省值是自报参照"前提
- v0.3（已完成）：长链路 Agent —— `ledger_agent.py` 消费同一内核，提供「建议生成（propose_entry，按类型历史均值预填 baseline）」「待自动化建议（--targets）」「写回账本（append_entry，默认 dry-run 预览、--apply 才原子写回并自动备份）」三件套，对话层与报告层零改动
- v0.4（已完成）：对话编排层 —— 新增 `conversation.py`，用意图路由（classify + handle）把 qa 追问 / 报告 / ledger_agent 写回串成单一对话流；支持自然语言记账（解析类型与成本、历史均值预填基线、确认才写回）、被动记账建议（"我刚生成了周报，花了1800 token"也能识别）、连续对话（记账前后随意追问/看摘要/看建议），纯粘合层、不改既有三层一行
- v0.5（已完成）：类型字典消歧 —— 新增 `scripts/type_registry.json`（标准名 ↔ 别名映射）与 `tests/test_v05.py`（实地测试脚本）；`conversation._detect_type` 改为「账本已知类型 → 字典别名 → 短语抓取+字典模糊 → 全新类型候选」四级匹配，消除"周报"误判短词/多义歧义，词典缺失自动降级；qa/report_engine/ledger_agent/diagnose 仍零改动
- v0.6（已完成）：Skill 触发流 —— 新增 `scripts/skill_bridge.py` 与 `tests/test_v06.py`；`on_conversation_event(event)` 把**宿主对话事件**翻译成 `conversation.handle()` 调用，用 `is_completion_event` 识别「任务完成」信号（高/中/低信心），自动建议记账并暂存待确认条目；`_lenient_type` 用类型字典做大小写不敏感兜底识别；触发默认 dry-run 不写账本，用户「确认」才写回；内核与三层外壳 + 编排层零改动
- v0.7（已完成）：真实闭环 + 去品牌化 —— 升级 `scripts/skill_bridge.py` + 新增 `scripts/host_hook.py` 与 `tests/test_v07.py`；`on_conversation_event` 现可消费宿主回报的真实用量 `event["cost"]`（实测优先级高于文本解析，`cost_source="event"`）与结构化完成标志 `event["completed"]`，把"提效"从"用户自报"升级为"实测成本"；`host_hook.py` 是平台无关的宿主钩子示例（不 import 任何平台 SDK、无网络、无硬编码密钥，满足 OpenClaw/天禧 安全红线）；`skill_bridge` 去品牌化为通用「宿主对话事件」，可同时服务 天禧 / OpenClaw，比赛仓库可直接复用内核；内核与三层外壳 + 编排层仍零改动
- v0.8（已完成）：提效洞察可视化 —— `diagnose` 内核新增 `compute_period_compare`（本期 vs 上期，含方向/环比百分比，单周数据返回 None 并触发友好降级）与 `compute_roi_targets`（按「月度节省 ÷ 投入工时」排自动化 ROI）；`report_engine` 新增零依赖内联 SVG **趋势折线图**（`build_trend_line_chart`）、**本期 vs 上期**对比卡（`build_compare_card`）、**最该自动化（按 ROI 排序 Top N）**卡（`build_roi_card`），注入完整报告与摘要双模板；`qa` 新增「比上周/环比」意图分支（数据不足给出「周数据不足」提示）；`ledger_agent.propose_automation_targets` 改为消费内核 ROI 排序结果。新增 `tests/test_v08.py`（8 例，全维度打标）；用例总数 36 → 44。内核与三层外壳 + 编排层仍零改动
- v0.9（已完成）：诚实定位 + 真实宿主用量接入 —— SKILL.md 定位收敛为 Option C「办公室 Token 洞察与提效助手」：明确「只度量、不执行」，新增 QUICKSTART 与「可选只读本机宿主用量」Non-goals 声明（不联网、无密钥，满足安全红线）；新增 `scripts/host_cost.py`（隔离层，`CostRecord` / `EventCostProvider` / `LocalProvider` / `draft_entries_from_host`，纯标准库、无网络、无密钥、脏数据降级不崩），把 `skill_tokens` 从「用户自报」升级为「宿主实测」；`skill_bridge.on_conversation_event` 新增 `cost_provider` 参数（事件无 cost 时用宿主实测补全并标注来源，向后兼容 `None`）；`ledger_agent` 新增 `import_host_usage`（默认 dry-run 不写盘）。新增 `tests/test_v09_host_cost.py`（9 例）+ `tests/test_v09_skillmd.py`（4 例），守卫「诚实定位不回潮」；用例总数 44 → 57。内核与三层外壳 + 编排层仍零改动
- v0.9.2（已完成）：SkillHub 联网搜索 —— 新增 `scripts/skillhub_client.py`（SkillHub HTTP 客户端，支持搜索和详情查询）与 `scripts/skill_recommender.py`（推荐引擎）；`report_engine` 新增 `--online` 参数启用联网模式，自动搜索 SkillHub 获取最新省 Token Skill 信息；所有推荐默认需用户确认才能安装，报告含 ⚠️ 安全提示；新增 `tests/test_v091_skill_recommender.py`（13 例）。用例总数 57 → 70。
- v0.9.3（已完成）：ClawHub 联网搜索 —— 新增 `scripts/clawhub_client.py`（ClawHub HTTP 客户端）；推荐引擎同时支持 SkillHub 和 ClawHub 双平台搜索；报告格式展示双平台信息（stars, installs, tags）；新增 `tests/test_v092_skillhub_client.py`（3 例）+ `tests/test_v093_clawhub_client.py`（3 例）。用例总数 70 → 76。
- v0.9.5（方向 B · 执行引擎 + Phase 2 落地 · 已完成）：执行引擎落地 —— 用户 2026-08-25 决策从方向 A（仅度量）切到 **方向 B（度量 + 真实执行）**：SKILL.md 承诺翻转「只度量、不执行」→「既帮你做、又自动记账」，triggers/non_triggers 同步更新；新增 `scripts/executor.py`（任务执行引擎，按 `task_type` 分发：周报/纪要/数据分析/文档整理/PPT 大纲，内容类走模板渲染、数据类走本地 stdlib 计算，纯标准库、无 LLM/无网络/无密钥），每次执行后 `propose_ledger` 走 `run_long_chain` 护栏自动记账（baseline 缺省拦截、默认 dry-run）；新增 `tests/test_v10_executor.py`（9 例，全维度打标）。**Phase 2 已落地**：`executor.py` 增加 `--format docx/xlsx` 可选导出（python-docx/openpyxl 为可选依赖，缺失自动降级 md/csv，零依赖默认不受影响）；`host_hook.py` 新增 `on_executor_completed(ledger_path, task_type, event, apply)`，把 executor 完成事件的真实用量（`event["cost"]`）直接记回 ledger，与 v0.7 宿主完成事件形态一致。测试 112 → **118**（执行引擎 9 → 15 例）。内核与三层外壳 + 编排层仍零改动。**v1.0.0 留作正式产品发布**：Phase 3（安全预检脚本接 CI + 对话流 execute 意图路由）与 Phase 4（bump 1.0.0 + GitHub Pages 闸门 + 天禧苍穹共创计划提交）完成后，再切 1.0.0 并开 Pages。
- 目标：提交「天禧 AI Skills 苍穹共创计划」（截止 2026-12-31）
