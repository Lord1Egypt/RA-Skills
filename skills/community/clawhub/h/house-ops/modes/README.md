# modes/ — 工作模式库

house-ops 的"大脑"：由编码 agent 执行的 Markdown 提示词文件。**一个文件 = 一个工作流**；`_` 前缀为共享上下文/模板，不是可路由模式。

| 文件 | 层 | 用途 |
|---|---|---|
| `_shared.md` | 系统 | 评分体系、配套分级参考、小区软素质信号、全局规则、SoT 表（可自动更新，勿放个人数据） |
| `_profile.template.md` | 种子 | 复制为 `_profile.md`（用户画像语义层，gitignore） |
| `_brief.template.md` | 种子 | 复制为 `_brief.md`（速筛简版画像，triage 专用，gitignore） |
| `_custom.template.md` | 种子 | 复制为 `_custom.md`（家规/评分口径覆盖，gitignore） |
| `intake.md` | 模式 | 多轮对话采集购房需求（含家庭结构→衍生需求翻译）→ 生成画像 |
| `triage.md` | 模式 | 60 秒快速速筛（对照 `_brief.md` 三问），不落报告 |
| `evaluate.md` | 模式 | 单房源六维评级 → 报告 + watchlist 登记；Machine Summary schema SoT |
| `deep-dive.md` | 模式 | 高分房源（≥4.0）六轴深挖 |
| `compare.md` | 模式 | 2-6 套已评估房源对比矩阵 + 场景化结论 |
| `visit.md` | 模式 | 带看前定制清单 / 带看后记录复盘与增量重评 |
| `negotiate.md` | 模式 | 高分房源核实清单、议价策略、沟通话术草稿 |
| `contract.md` | 模式 | 交易文件条款走查（配合 `templates/contract-checklist.cn.yml`） |
| `watchlist.md` | 模式 | 关注清单查看/更新/汇总 |
| `stats.md` | 模式 | 找房数据统计与模式分析（优先跑 `scripts/stats.mjs`） |
| `doctor.md` | 模式 | 环境与数据健康自检（无 AI 快速版 `scripts/doctor.mjs`） |

上下文加载顺序：`_shared.md` → `_profile.md` → `_custom.md` → `{mode}.md`（`triage` 只加载 `_brief.md`）。用户层后读、覆盖系统层。
