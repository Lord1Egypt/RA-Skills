# Insurance Solvency Report Generator (C-ROSS) / 偿付能力报告生成器（偿二代二期工程）#

> **English:** AI-powered solvency report generator for China insurance regulation (C-ROSS Phase II, effective 2022). Generates quarterly and annual solvency reports, stress testing reports, and regulatory disclosure documents. Built for CFOs, actuaries, and compliance teams. Covers all 22 regulatory rules.

**Keywords:** solvency, C-ROSS, China insurance, solvency ratio, regulatory reporting, insurance capital, CBIRC, C-ROSS Rules II*

## ✨ Features#

- ✅ **C-ROSS Phase II Framework** — 3-pillar system (quantitative, qualitative, market discipline), 22 regulatory rules*
- ✅ **Capital Calculation Engine** — actual capital (core + subsidiary) and minimum capital calculation templates with Excel formulas*
- ✅ **Solvency Report Generator** — quarterly/annual report structure templates per CBIRC format*
- ✅ **Stress Testing Module** — 4-scenario stress test (basic/mild/severe/adverse) with report template*
- ✅ **Pressure Test Report Template** — standard format with conclusions and capital replenishment plan*

## 🚀 Quick Start#

```bash
# Install this skill
npx clawhub install @gechengling/insurance-solvency-reporter

# Use in WorkBuddy
/insurance-solvency-reporter "Generate Q2 2026 quarterly solvency report"
/insurance-solvency-reporter "Run stress test with mild pressure scenario"
```

---

> **中文介绍：** 偿付能力报告生成器——基于中国偿二代二期工程（C-ROSS Rules II，2022年起实施）的垂直精算Skill。覆盖偿付能力充足率计算、实际资本/最低资本计算、压力测试、风险综合评级、季度/年度监管报告生成。适用：保险公司财务总监/精算负责人/合规部、偿付能力季度报告编制、保险监管报送。

**关键词：** 偿付能力、偿付能力报告、C-ROSS、偿二代、核心资本、最低资本、综合资本充足率、偿付能力充足率、压力测试、风险资本、保险监管报告*

## ✨ 核心功能#

- ✅ **C-ROSS偿二代二期工程全框架** — 三支柱体系（偿付能力监管规则1-22号）*
- ✅ **实际资本计算** — 核心资本分级结构（核心一级/二级+附属一级/二级）*
- ✅ **最低资本计算框架** — 保险/市场/信用/操作风险最低资本模板*
- ✅ **偿付能力报告结构** — 季度快报/季度分析报告/年度报告/临时报告*
- ✅ **压力测试与情景分析** — 基本/轻度/重度/逆向四层压力情景*

## 🚀 快速上手#

```bash
# 安装此技能
npx clawhub install @gechengling/insurance-solvency-reporter

# 在WorkBuddy中使用
/insurance-solvency-reporter "生成2026年第二季度偿付能力报告"
/insurance-solvency-reporter "运行压力测试（轻度压力情景）"
```

## 📖 What's Included / 包含内容#

| File / 文件 | Content / 内容说明 |
|------|---------|
| `SKILL.md` | Full skill definition / 完整技能定义 |
| `references/cross_rules_ii_summary.md` | C-ROSS Rules II 全22号规则核心速查 |
| `references/solvency_calculation.md` | 实际资本/最低资本计算模板 |
| `references/solvency_report_template.md` | 偿付能力季度/年度报告标准模板 |
| `references/pressure_test_guide.md` | 压力测试情景设置与报告撰写指南 |
