# Life Money Skill — 人生搞钱规划Skill

**简体中文** ｜ [English](README.en.md)

把职业变现诊断做成一件事能跑完的流程：**访谈建档 → 7 轮分析 → 一份能直接看的 HTML 报告**。

> Send your résumé and career story in, get a single-file HTML career-monetization diagnostic out — hidden skills, income opportunities, leverage, higher-pay directions, AI side services and a 90-day plan.

> 状态：开发中（Phase 0-4 已完成）｜Hermes Agent Skill

---

## 解决什么问题

| 痛点 | Life Money 怎么做 |
|---|---|
| 不知道自己身上哪些能力能卖钱 | 第 1 轮就做「隐藏技能盘点」，从真实经历里挖出市场会付费的能力，并给出依据 |
| 想搞副业但不知道从哪下手 | 每条收入机会都配「第一步」——本周就能执行的具体动作 |
| 计划做完就躺平，没有验收 | 90 天计划分 3 阶段，每阶段一个可验证的里程碑 |
| 目标太虚（「我要月入过万」） | 门禁 2 强制确认每月额外收入目标，所有收入口径都对齐它 |
| 副业想法超出现实时间 | 门禁 3 确认每周可投入时间，AI 副业方案全部受该预算约束 |

---

## 怎么用

在装了本 Skill 的 Agent 中，直接说话：

```
帮我做一次职业变现诊断，简历我发你
```

```
我每周只有 6 小时，想每月多赚 2000，看看我能做什么
```

Agent 会自动走：建档（要材料 + 访谈补全）→ 7 轮分析（中途 2 道确认）→ 渲染报告 → 交付。

---

## 产出长什么样

`report.html` —— 单文件、离线可开、可直接打印 PDF：

| 部分 | 内容 |
|---|---|
| 封面 / 摘要 | 身份 + 目标徽章 + 5 条关键发现 |
| 01 隐藏技能 | 10 项被低估能力（价值 / 谁付费 / AI 如何放大 / 依据） |
| 02 收入机会 | 机会矩阵图 + 10 条机会（成本 / 时间 / 难度 / 潜力 + 第一步） |
| 03 变现路径 | 服务 / 咨询产品 / 数字产品 / 自由职业 分组盘点 |
| 04 最大杠杆 | 如果只做一件事，做哪个 |
| 05 高薪方向 | 薪酬阶梯图 +「为什么是你」资格对照 |
| 06 AI 副业服务 | 时间预算图 + 5 个 AI 增效服务（受每周可投入时间约束） |
| 07 90 天计划 | 三阶段时间线 + 里程碑徽章 |
| 附录 A / B | 7 个原始提示词（可复制复用）· 来源与免责声明 |

示例成品：[**在线预览**](https://luojiangyong.com/life-money-skill/examples/demo/report.html) ｜ [`examples/demo/report.html`](examples/demo/report.html)（虚构人设，非真实数据）

---

## 报告预览

> 点击任意图片打开**在线完整报告**（GitHub Pages 实时渲染）。

| 封面 · 目标徽章 · 关键发现 | 收入机会矩阵 |
|---|---|
| [![封面](docs/images/report-01-cover.jpg)](https://luojiangyong.com/life-money-skill/examples/demo/report.html) | [![机会矩阵](docs/images/report-02-matrix.jpg)](https://luojiangyong.com/life-money-skill/examples/demo/report.html) |
| 品牌封面 · 目标徽章 · 5 条关键发现 | 难度 × 潜力矩阵，珊瑚 = 优先启动 |

| 薪酬阶梯 | AI 副业时间预算 |
|---|---|
| [![薪酬阶梯](docs/images/report-03-salary.jpg)](https://luojiangyong.com/life-money-skill/examples/demo/report.html) | [![时间预算](docs/images/report-04-budget.jpg)](https://luojiangyong.com/life-money-skill/examples/demo/report.html) |
| 月薪区间对照「你当前」虚线 | 每个 AI 服务周工时 ≤ 每周可投入 |

| 90 天计划时间线 | 原始提示词（深色附录） |
|---|---|
| [![时间线](docs/images/report-05-timeline.jpg)](https://luojiangyong.com/life-money-skill/examples/demo/report.html) | [![原始提示词](docs/images/report-06-prompts.jpg)](https://luojiangyong.com/life-money-skill/examples/demo/report.html) |
| 三阶段行动 + 可验证里程碑 | 7 段 canonical 原文，可复制复用 |

---

## 工作流

```
用户材料 + 访谈
    │
    ├─ L1 建档 ──门禁 1──▶ profile.json
    ├─ L2 分析 ──门禁 2/3─▶ analysis.json（7 轮）
    ├─ L3 渲染 ──────────▶ report.html
    └─ L4 验证交付 ──────▶ projects/<YYYY-MM-DD>-<slug>/
```

**不做**：不接外部 LLM API（7 轮分析由 Agent 执行）；不把用户数据放进仓库；不写「保证收入」类承诺。

---

## 三道门禁（不可跳过）

| 门禁 | 触发点 | 用户要做什么 | 默认值 |
|---|---|---|---|
| 1 | L1 建档 | 提供材料（简历 / 项目报告 / 作品集）+ 确认信息 | — |
| 2 | 隐藏技能后、收入机会前 | 选每月额外赚取目标 | 1000-3000 元/月 |
| 3 | AI 副业服务前 | 填每周启动可投入时间 | 6 小时 |

---

## 目录结构

```
life-money-skill/
├── SKILL.md                     ← 路由中枢（入口）
├── CONSTITUTION.md              ← 设计宪法（5 原则 / 7 维度 / 禁止模式）
├── README.md / README.en.md     ← 中文 / English 说明
├── LICENSE                      ← MIT
├── docs/images/                 ← README 素材（报告预览截图）
├── references/                  ← 领域知识（按需加载）
│   ├── seven-prompts.md         ← 7 提示词 canonical 原文（唯一真源）
│   ├── interview-guide.md       ← 建档协议 + 门禁 1
│   ├── analysis-specs.md        ← 7 轮分析规格 + 门禁 2/3
│   ├── report-design.md         ← 报告设计系统 + 图表规格
│   ├── data-calibration.md      ← 市场校准（可选，≤3 次检索）
│   └── cases/                   ← 案例库（INDEX + 模板 + 案例）
├── scripts/
│   ├── render_report.py         ← analysis.json → report.html（含校验）
│   └── verify_repo.py           ← 仓库自检（契约 + 渲染 + 结构）
├── assets/
│   ├── schemas/                 ← 两个公共契约（profile / analysis）
│   └── templates/report.css     ← 报告样式系统
├── examples/demo/               ← 虚构人设完整示例（含成品报告）
├── projects/                    ← 运行产物（gitignored，含用户敏感数据）
└── .github/workflows/ci.yml     ← CI：每次 push 跑同一套自检
```

---

## 安装

本仓库是**开发仓库（唯一真源）**，Hermes 中的安装副本为薄路由。安装到 Hermes 待定（当前未安装）。

```bash
git clone https://github.com/LuoJiangYong/life-money-skill.git
```

---

## 开发自检

```bash
python scripts/verify_repo.py
```

1. **契约校验** —— 示例数据 ↔ 两个 JSON Schema（零依赖校验器，关键字白名单，不支持即报错）
2. **渲染冒烟** —— 跑通 `render_report.py` 并产出报告
3. **结构核对** —— 组件计数精确匹配（10 / 10 / 5 / 3 / 5 / 7 / 3 / 5 / 10）

CI 每次 push 自动运行同一套检查 + 仓库边界检查（`projects/` 不得入库）。

---

## 来源与致谢

本 Skill 的方法论源自 X 用户 **@Raul_IA_Prod** 的 7 段提示词（西班牙语原作，经翻译与本地化整理）——用结构化提问把「我不知道自己能做什么」变成可执行的变现路径。7 轮分析维度按其方法重构，报告附录保留这 7 段提示词的 canonical 原文以便复用。

> canonical 原文：[`references/seven-prompts.md`](references/seven-prompts.md)
>
> Methodology adapted from @Raul_IA_Prod's 7 prompts on X (originally in Spanish).

---

## 许可证

[MIT](LICENSE) © 2026 Jiang Yong Luo

---

## 版本

v1.0.0 —— 完整诊断管线：访谈建档 → 7 轮分析 → 单文件 HTML 报告（含 4 组可视化）；零依赖自检脚本 + CI 质量门。
