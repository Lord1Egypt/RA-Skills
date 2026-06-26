# Insurance Claims Intelligence Expert / 保险行业智能理赔专家

> **⚠️ DISCLAIMER / 免责声明**
> - **English:** This is an **advisory and template-only skill**. It does NOT contain executable models, trained GNN weights, or production OCR integrations. All accuracy figures (e.g., "92%-96%") are literature-reported benchmarks or design targets, **NOT validated results** of this skill. ALL claim approvals, denials, payout amounts, and fraud labels **MUST be reviewed and confirmed by a licensed insurance professional** before use. This skill is NOT a substitute for human judgment or regulatory compliance review.
> - **中文：** 本Skill**仅为咨询模板和参考框架**，不含可执行模型、已训练GNN权重或生产级OCR集成。所有准确率数据（如"92%-96%"）均来自文献基准或设计目标，**非本Skill实测结果**。所有理赔核准、拒付、赔付金额及欺诈标签，**必须经持证保险专业人士审核确认后方可使用**。本Skill不可替代人工判断或监管合规审查。

> **🔒 DATA SECURITY NOTICE / 数据安全提醒**
> - Medical invoices and claimant data are sensitive personal information. Before using OCR features, obtain user consent, redact unnecessary PII, and prefer on-prem/private deployment.
> - API keys MUST be stored in environment variables or a secret manager. Never hardcode keys.
> - **中文：** 医疗发票和理赔申请人数据属于敏感个人信息。使用OCR功能前，须获得用户同意，脱敏非必要个人信息，优先使用本地私有化部署。API密钥必须存入环境变量或密钥管理器，禁止硬编码。

---

## ✨ What This Skill Provides / 本Skill提供的内容

| Type / 类型 | Description / 说明 |
|-------------|---------------------|
| 📋 Workflow checklists / 流程检查清单 | Step-by-step claims review checklists for human reviewers |
| 📄 Report templates / 报告模板 | Standardized output formats for claims analysis reports |
| 🏗️ Reference architectures / 参考架构 | Guidance on OCR integration, rules engines, and GNN design |
| 💡 Example code / 示例代码 | Python examples (require your own API keys and data) |
| 📚 Company practices reference / 公司实践参考 | Summaries of industry best practices (advisory only) |

**This skill does NOT provide:** executable models, pre-trained weights, bundled API credentials, or automated claim approval.

---

## Core Features / 核心功能（咨询级）

### 1. Medical Receipt OCR — Integration Guidance / 医疗票据OCR（集成指导）

**Supported document types / 支持票据类型（8类）：**
门诊发票 / 住院发票 / 医疗费用明细清单 / 医保结算单 / 出院小结 / 病历首页 / 检查报告单 / 费用结算单

**Integration options / 集成方案参考：**
- Baidu AI OCR / 百度AI开放平台
- Tencent Cloud OCR / 腾讯云OCR
- Ali Cloud OCR / 阿里云OCR
- Infologic OCR / 合合信息OCR

> ⚠️ **Data Handling / 数据处理：** Only send necessary fields. Redact/unnecessary PII beforehand. Confirm vendor's data retention policy.
> **中文：** 仅发送必要字段，事前脱敏非必要个人信息，确认服务商数据留存策略。

### 2. Liability Determination — Advisory Checklist / 理赔判责（咨询检查清单）

Provides structured checklists for human reviewers:
- ✅ Waiting period check / 等待期检查
- ✅ Pre-existing condition screen / 既往症筛查
- ✅ Deductible verification / 免赔额校验
- ✅ Hospital level verification / 就诊机构核查
- ✅ Policy coverage match / 险种责任匹配

> ⚠️ **All results are suggestions only. Final decisions MUST be made by authorized human reviewers.**
> **中文：** 所有结果仅为建议，最终决定必须由授权人工审核员作出。

### 3. Anti-Fraud Assessment — Checklist / 反欺诈评估（检查清单）

Structured red-flag checklist for fraud investigation:
- 🚩 Unusual visit frequency / 就诊频率异常
- 🚩 Invoice authenticity verification / 票据真实性验证
- 🚩 Diagnosis-medication mismatch / 诊断与用药不匹配
- 🚩 Provider-case network anomalies / 医疗机构-案件网络异常

**Data governance requirements / 数据治理要求：**
- Retention limit / 留存期限：≤ 2 years (or per regulatory requirement) / 不超过2年（或监管要求期限）
- Access control / 访问控制：Authorized fraud investigators only / 仅授权欺诈调查员可访问
- Correction workflow / 更正流程：Data subjects have the right to request correction / 数据主体有权请求更正

### 4. Claims Report Templates / 理赔报告模板

Standardized templates for 7 insurance types:
- Health insurance / 医疗险
- Critical illness insurance / 重疾险
- Life insurance / 寿险
- Accident insurance / 意外险
- Auto insurance / 车险
- Property insurance / 财产险
- Group insurance / 团险

All templates include the required disclaimer: "This is an AI-assisted draft requiring licensed professional review."

---

## 🚀 Quick Start / 快速上手

```bash
# Install this skill (installs advisory templates only)
npx clawhub install insurance-claims-intelligence

# Use in WorkBuddy (advisory mode only)
/insurance-claims-intelligence "Generate a claims review checklist for this outpatient case"
/insurance-claims-intelligence "Create a fraud risk assessment template for these 5 cases"
```

> ⚠️ **All outputs are drafts. Human review is mandatory.**
> **中文：** 所有输出均为草稿，人工审核是强制要求。

---

## 📖 What's Included / 包含内容

| File / 文件 | Content / 内容说明 |
|-------------|---------------------|
| `SKILL.md` | Full skill definition, trigger keywords, advisory workflows |
| `references/claims_ocr_tech.md` | OCR integration guidance + provider comparison + example Python code (API key required) |
| `references/claims_liability_engine.md` | Liability checklist + model reference + 3 company practices (advisory) |
| `references/claims_report_templates.md` | Report templates + 7 insurance type notice templates |

---

## Provenance / 来源说明

- **Author / 作者：** @gechengling
- **Skill type / Skill类型：** Advisory templates and reference frameworks only / 仅含咨询模板和参考框架
- **Contains executable code:** NO / 不含可执行代码
- **Contains pre-trained models:** NO / 不含预训练模型
- **Requires API credentials:** YES — you must provide your own OCR/LLM API keys / 需要您自行提供OCR/LLM API密钥
- **License / 开源协议：** MIT-0

---

## Required Human Review / 强制人工审核要求

| Action / 操作 | Human Review Required? / 需人工审核？ |
|---------------|----------------------------------------|
| Claim approval / 理赔核准 | ✅ MANDATORY / 强制 |
| Claim denial / 理赔拒付 | ✅ MANDATORY / 强制 |
| Payout amount decision / 赔付金额决定 | ✅ MANDATORY / 强制 |
| Fraud label assignment / 欺诈标签标记 | ✅ MANDATORY / 强制 |
| Customer-facing notice generation / 客户通知书生成 | ✅ MANDATORY / 强制 |

---

## Contact / 联系方式

If you have questions about this skill, contact: [@gechengling on ClawHub](https://clawhub.ai/gechengling)

---

*Last updated: 2026-05-05 — v1.2.0 — Added comprehensive disclaimers, removed auto-approval language, added data governance requirements.*
