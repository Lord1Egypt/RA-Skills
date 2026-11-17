# Life Money Skill — 设计宪法（CONSTITUTION）

> 本文档定义 Life Money Skill 的最高设计原则、架构约束与禁止模式。
> 所有 Phase、所有文件、所有决策均受此宪法约束。与本文冲突者，以本文为准。
>
> 固化日期：2026-09-18 | 版本：v1.1 | 状态：Phase 1 生效
> v1.1（2026-09-18）：落地三道用户门禁；移除 memory/ 治理（用户决定）

---

## 一、项目定位

把「7 提示词职业变现法」（原作者 X @Raul_IA_Prod）产品化为 Hermes 内的职业变现诊断 Skill：

**材料收集（门禁 1：简历 / 项目报告 / 作品集 + 访谈）→ profile.json → 7 轮结构化分析（含门禁 2/3）→ analysis.json → 单文件 HTML 诊断报告**

- 是：个人职业变现诊断 + 报告生产；本地、私有、可重复运行。
- 不是：不承诺收入结果；非招聘 / 投递工具；不自动对外发布；不做多租户平台。

## 二、5 条设计原则

### 1. 高内聚 HIGH COHESION — One module, one job.

- SKILL.md 只做路由与装配；访谈协议、分析规格、报告设计知识、渲染逻辑各归其边界。
- 7 个提示词的 canonical 原文只存在于 `references/seven-prompts.md`，任何地方不得复制后各自漂移。
- 报告版式规则只存在于 `references/report-design.md` + 渲染脚本的设计 token 中，不散落在模板注释里。

### 2. 低耦合 LOW COUPLING — Share contracts, not internals.

- 两个 JSON Schema（`career_profile` / `career_analysis`）是唯一公共契约；渲染脚本与模板只消费这两个契约，不读散落的自定义字段。
- 契约变更必须同步检查：schema → 渲染脚本 → 分析规格 → 报告设计 → 示例。
- 换报告视觉只改设计 token + 模板，不动分析逻辑；换分析规格只改 references，不动 schema 结构（除非新增字段）。

### 3. 可扩展 EXTENSIBLE — New capability through an extension point.

- 新报告章节 = schema 加字段 + 模板加区块；主流程不动。
- 新分析维度 = **禁止**（见 §六）。7 个维度是对源方法论的忠实约束，扩展只能发生在表达层与质量标准层。
- 新增能力优先通过 references 文档沉淀，而非新增脚本。

### 4. 易维护 MAINTAINABLE — Traceability over cleverness.

- 7 个提示词的 canonical 原文固化于 `references/seven-prompts.md`；报告附录引用同一文本，任何地方不得复制后各自漂移。
- 分析结论必须可回溯到 profile 字段；涉及推断必须在 `summary.assumptions` 显式声明。
- 渲染产物必须可读回验证（文件存在 + 截图 QA），不得声称未验证的成功。

### 5. 高效简洁 LEAN — No abstraction before pain is real.

- 单模板、单渲染脚本起步；没有第二个真实模板需求前，不做模板系统、不做插件体系。
- 不引入外部 LLM API——7 轮分析由 Agent 执行。
- 报告质量优化必须基于试渲染与截图证据，不基于审美想象。

## 三、目录布局

```
life-money-skill/
├── CONSTITUTION.md           # 本文件：设计宪法
├── SKILL.md                  # 路由中枢（Phase 1，正文目标 ≤3500 chars）
│
├── references/               # 领域知识（Phase 1-2）
│   ├── seven-prompts.md      # 7 提示词 canonical 原文（唯一真源）
│   ├── interview-guide.md    # 访谈协议 + 材料解析规则（简历/项目报告/作品集）+ 门禁 1
│   ├── analysis-specs.md     # 7 轮分析输出规格 / 质量标准 / 反模式（含门禁 2/3）
│   ├── report-design.md      # 报告设计系统（中文适配 + tokens）
│   ├── data-calibration.md   # 市场数据校准检索指南（可选步骤）
│   └── cases/                # 案例库（INDEX + _TEMPLATE + 案例文件）
│       ├── INDEX.md
│       └── _TEMPLATE.md
│
├── scripts/                  # 确定性逻辑
│   ├── render_report.py      # analysis.json → report.html（校验 + 渲染）
│   └── verify_repo.py        # 仓库自检（契约 + 渲染冒烟 + 结构核对）
│
├── assets/
│   ├── schemas/              # 公共契约（Phase 0）
│   │   ├── career_profile.schema.json
│   │   └── career_analysis.schema.json
│   └── templates/            # 报告模板（report.css；Phase 3）
│
├── examples/                 # 完整示例与设计基准（虚构人设，无真实数据）
│   └── demo/                 # profile.json + analysis.json + report.html
│
├── docs/images/              # README 素材（报告预览截图）
│
├── projects/                 # 运行产物（.gitignore；含用户敏感数据）
│   └── <YYYY-MM-DD>-<slug>/
│       ├── profile.json
│       ├── analysis.json
│       ├── report.html
│       └── screenshots/
│
└── .gitignore
```

> 注：本项目不设 `memory/`（用户决定，2026-09-18）；接手信息以「宪法 + 文件头 + git log」为准。

## 四、数据流

```
用户材料：简历 / 项目报告 / 作品集等（门禁 1）
    │  访谈补全 → 用户确认信息准确；缺项追问，不猜测
    ▼
profile.json（Contract 1：career_profile.schema.json）
    │
    ▼
7 轮分析（Agent 执行，维度见 §五）
    │  分析 1 后 ─▶ 门禁 2：用户选每月额外赚取目标（默认 1000-3000 元/月）
    │  分析 6 前 ─▶ 门禁 3：用户填每周启动可投入时间（默认 6 小时）
    ▼
analysis.json（Contract 2：career_analysis.schema.json）
    │
    ▼
render_report.py（校验 + 渲染）
    │
    ▼
report.html（终产物）→ 截图 QA → 交付 projects/<run>/
```

## 五、7 个分析维度（不可增删）

对应源方法论 7 个提示词，顺序即执行顺序：

| # | 提示词 | 输出字段 |
|---|--------|---------|
| 1 | 发现我的隐藏技能 | `hidden_skills` |
| 2 | 寻找收入机会 | `income_opportunities` |
| 3 | 变现我的经验（企业战略家视角） | `monetization_paths` |
| 4 | 找到我最大的杠杆机会 | `leverage` |
| 5 | 向我展示什么薪水更高 | `higher_pay_roles` |
| 6 | 创建一个由 AI 驱动的副收入来源 | `ai_services` |
| 7 | 构建我的 90 天计划 | `plan_90d` |

> 执行顺序含三道用户门禁：门禁 1（材料与信息确认，建档收口）→ 门禁 2（分析 1 后、分析 2 前：收入目标）→ 门禁 3（分析 6 前：每周启动时间）。默认值随 `references/analysis-specs.md` 维护。

维度名称、数量、顺序变更 = 破坏性变更，必须经用户批准并同步两个 Schema、分析与报告模板。

## 六、禁止模式

这些是硬性禁止项。违反任一条，产出无效。

### 数据与隐私

- ❌ 不编造 profile 之外的经历、数字、头衔；数字必须来自用户原话。
- ❌ 报告不写「保证收入 / 保证成功」类承诺；附录保留免责声明。
- ❌ 不把 `projects/` 下任何用户数据提交进 git（.gitignore 双保险 + 提交前 `git status` 检查）。
- ❌ 不把简历原文、薪资等敏感信息写入报告明文以外的任何仓库文件。

### 架构与抽象

- ❌ 7 个分析维度不可增删、不可改名、不可合并。
- ❌ 不调用外部 LLM API；不引入运行时网络依赖（渲染为纯本地）。
- ❌ 没有第二个真实消费者前，不做模板系统 / 插件体系 / 多语言体系。
- ❌ 不做与两个 Schema 平行的第二套数据模型。

### 流程与交付

- ❌ 不跳过三道用户门禁（门禁 1 材料与信息确认 / 门禁 2 收入目标 / 门禁 3 每周启动时间）。
- ❌ 渲染失败 / 未验证不得声称成功；必须读回文件 + 截图验证。
- ❌ 不自动对外发布报告；生成即终点。

## 七、元数据治理

### 文件级元数据

领域 / 参考类 `.md` 文件头部包含（`SKILL.md` 以 frontmatter 为准；本宪法以版本头为准）：

```markdown
> 路径：<repo-relative-path>
> 职责：<一句话>
> Phase：<0|1|2|3|4>
> 依赖：[<直接依赖的文件>]
> 被依赖：[<直接消费本文件的文件>]
> 最后更新：<YYYY-MM-DD>
```

### 版本管理

- 通过 git 管理，不建 CHANGELOG.md；commit 格式 `feat(phase<N>): <描述>`。
- 每完成一个可验证微批次 → 清理 → commit → push。

### 元数据方案约束

- 采用「文件头 + git log」轻量治理；受治理文件 ≥15 时，允许启用**单文件** `metadata/registry.md`。
- 禁止多文件 YAML 体系（registry.yaml / fields.yaml / dependencies.yaml）与配套验证脚本。

## 八、规则优先级与事实来源

1. 用户对当前任务的明确批准与范围变更。
2. 本宪法。
3. 已批准的阶段计划与公共契约（两个 Schema）。
4. 当前源码、脚本与可读回产物。
5. 旧提示词、历史总结、实验草稿。

开始任何任务前先读实时仓库；事实判断以实时仓库为准，旧总结与历史结论只作定位辅助。

## 九、变更控制

1. 修改本宪法 = 需用户明确确认，讨论影响范围，同步更新相关文件。
2. 修改公共契约（Schema）= 检查渲染脚本、分析规格、报告模板、示例的同步；破坏性变更递增 `schema_version`。
3. 新增 Phase / 扩大边界 = 单独批准，不随「顺手」执行。
