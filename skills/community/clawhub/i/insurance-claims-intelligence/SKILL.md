---
name: Insurance Claims Intelligence Expert
description: Advisory skill for insurance claims processing workflows — provides templates, checklists, and decision-support frameworks for medical OCR, liability determination, anti-fraud assessment, and claims reporting. Human review required for all claim decisions. Keywords: insurance claims, claims advisory, medical OCR, anti-fraud, insurance tech, China insurance, decision support, 智能理赔, 理赔风控, 医疗单据识别, 责任认定, 理赔报告, 秒赔, 理赔决策, 医疗险理赔, 重疾理赔, 车险理赔.
slug: insurance-claims-intelligence
version: 1.2.0

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Insurance Claims Intelligence Expert / 保险行业智能理赔专家

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**



> **⚠️ DISCLAIMER / 免责声明**
> - **English:** This skill provides advisory templates, checklists, and decision-support frameworks ONLY. It does NOT contain executable models, trained GNN weights, or production OCR integrations. All accuracy figures (e.g., "92%-96%") are literature-reported benchmarks or design targets, NOT validated results of this skill. ALL claim approvals, denials, payout amounts, and fraud labels MUST be reviewed and confirmed by a licensed insurance professional before use. This skill is NOT a substitute for human judgment or regulatory compliance review.
> - **中文：** 本Skill仅提供咨询模板、检查清单和决策支持框架，不含可执行模型、已训练GNN权重或生产级OCR集成。所有准确率数据（如"92%-96%"）均来自文献基准或设计目标，非本Skill实测结果。所有理赔核准、拒付、赔付金额及欺诈标签，**必须经持证保险专业人士审核确认后方可使用**。本Skill不可替代人工判断或监管合规审查。

> **🔒 DATA SECURITY / 数据安全**
> - Medical invoices, diagnosis records, and claimant data are sensitive personal information under China's Personal Information Protection Law (PIPL). Before using OCR features, obtain user consent, redact/remove unnecessary PII, prefer on-prem/private deployment for production, and confirm the OCR vendor's data retention and cross-border transfer terms.
> - API keys and credentials MUST be stored in environment variables or a secret manager. Never hardcode keys in production systems.
> - **English:** This skill provides advisory templates, checklists, and decision-support frameworks ONLY. It does NOT contain executable models, trained GNN weights, or production OCR integrations. All accuracy figures (e.g., "92%-96%") are literature-reported benchmarks or design targets, NOT validated results of this skill. ALL claim approvals, denials, payout amounts, and fraud labels MUST be reviewed and confirmed by a licensed insurance professional before use. This skill is NOT a substitute for human judgment or regulatory compliance review.
> - **中文：** 本Skill仅提供咨询模板、检查清单和决策支持框架，不含可执行模型、已训练GNN权重或生产级OCR集成。所有准确率数据（如"92%-96%"）均来自文献基准或设计目标，非本Skill实测结果。所有理赔核准、拒付、赔付金额及欺诈标签，**必须经持证保险专业人士审核确认后方可使用**。本Skill不可替代人工判断或监管合规审查。

---

## Artifact Type / 作品类型

**This is a documentation-and-template skill.** It contains:
- ✅ Workflow checklists and decision trees
- ✅ Report templates and output formats
- ✅ Reference architectures and integration guidance
- ✅ Example Python code (requires your own API keys and data)

It does NOT contain:
- ❌ Pre-trained ML/GNN models
- ❌ Executable OCR or claims processing code
- ❌ Bundled third-party API credentials

---

## Trigger Keywords / 触发关键词

**English Triggers:** insurance claims advisory, claims workflow, claim analysis, medical OCR guidance, insurance fraud assessment, claim liability review, policy clause analysis, anti-fraud checklist, insurance tech reference, claims report template

**中文触发词：** 保险理赔咨询 / 理赔流程指导 / 理赔分析 / 医疗发票识别指导 / 理赔判责参考 / 责任认定流程 / 医疗险理赔 / 重疾险理赔 / 寿险理赔 / 意外险理赔 / 车险理赔 / 财产险理赔 / 理赔反欺诈 / 欺诈检测参考 / 骗保识别指导 / 理赔风控参考 / 保险条款解读 / 责任免除说明 / 保障范围分析 / 赔付比例计算 / 产品对比参考 / 条款比对指导 / 合同解读参考

---

## Core Capabilities / 核心能力（咨询框架）

### 1. Medical Receipt OCR — Guidance Framework / 医疗票据OCR识别（指导框架）

**支持的票据类型（覆盖全场景）：**

| Receipt Type / 票据类型 | Extracted Fields / 识别内容 | Insurance Types / 适用险种 |
|------------------------|-------------------|------------------|
| 全国统一门诊发票 | 发票号、医院、金额、明细项目 | 医疗险、意外险 |
| 全国统一住院发票 | 入院/出院日期、总金额、自费比例 | 医疗险、重疾险 |
| 医疗费用明细清单 | 药品明细、检查项目、单价、数量 | 医疗险 |
| 医保结算单 | 医保账户支付、自付金额、报销比例 | 医疗险 |
| 出院小结 | 诊断、住院天数、治疗经过 | 重疾险、寿险 |
| 病历首页 | 主要诊断、手术名称、ICD编码 | 重疾险 |
| 检查报告单 | 影像报告、检验结果 | 重疾险 |
| 费用结算单 | 分项金额、总计金额 | 财产险、责任险 |

> **⚠️ OCR Data Handling / OCR数据处理提醒**
> - Only send necessary fields to OCR providers; redact/unnecessary PII beforehand.
> - Confirm the OCR vendor's data retention policy (Prefer: no storage / auto-delete within 24h).
> - For production use, prefer private on-prem OCR deployment to avoid third-party data transfer.
> - **中文：** 仅发送必要字段至OCR服务商；事前脱敏/删除非必要个人信息；确认OCR厂商数据留存策略（优先：不留存/24小时内自动删除）；生产环境优先使用私有化本地部署OCR，避免第三方数据传输。

**参考技术架构（需自行集成）：**

```text
原始图像
  ↓
图像预处理（去噪/倾斜校正/二值化）
  ↓
CNN特征提取（ResNet50/EfficientNet）—— 需自行训练或调用云服务API
  ↓
RNN序列建模（BiLSTM）+ Attention机制
  ↓
CRF层解码 → 结构化文本输出
  ↓
字段标准化 → JSON/表格结构化结果
```

### 2. Liability Determination — Advisory Framework / 理赔判责引擎（咨询框架）

**咨询级判责检查清单（需人工逐项确认）：**

```text
规则1：等待期检查（人工确认）
  └─ 出险日期 - 保单生效日 < 等待期 → 建议拒付，需人工复核

规则2：既往症筛查（人工确认）
  └─ 既往症库匹配 → 责任免除 → 建议拒付/比例赔付，需人工复核

规则3：免赔额校验（人工确认）
  └─ 累计自付金额 < 免赔额 → 建议暂不赔付，需人工复核

规则4：就诊机构核查（人工确认）
  └─ 非二级及以上公立医院（需视条款）→ 提示确认，需人工复核

规则5：险种责任匹配（人工确认）
  └─ 就诊科室/诊断是否符合条款保障范围 → 建议全额/比例/拒付，需人工复核
```

> **⚠️ IMPORTANT / 重要提醒**
> The liability determination output is a **decision-support suggestion ONLY**. Final approval/denial MUST be made by an authorized human reviewer. This skill does NOT auto-approve any claim amount.
> **中文：** 判责输出**仅为决策支持建议**，最终核准/拒付**必须由授权人工审核员作出**。本Skill不对任何理赔金额进行自动审批。

### 3. Anti-Fraud Assessment — Advisory Framework / 反欺诈评估（咨询框架）

**反欺诈检查清单（咨询级）：**

```text
检查项1：就诊频率异常
  └─ 同一被保人短期内多次就诊 → 标记，建议人工调查

检查项2：票据真实性验证
  └─ 发票号重复 / 医院不存在 / 金额异常 → 标记，建议人工调查

检查项3：诊断与用药匹配性
  └─ 诊断与开具药品明显不符 → 标记，建议人工调查

检查项4：关系网络异常
  └─ 同一医生/医院集中出现在多起理赔 → 标记，建议人工调查
```

> **🔒 Anti-Fraud Data Governance / 反欺诈数据治理**
> - Retention limit / 留存期限：反欺诈图谱数据建议留存不超过 2 年，除非监管要求的更长留存期。
> - Access control / 访问控制：图谱查询权限仅开放给授权欺诈调查员，禁止非授权人员访问。
> - Data correction workflow / 数据更正流程：被保人有权请求更正错误数据，必须在 15 个工作日内处理。
> - Poisoning safeguard / 污染防护：新案件数据进入图谱前，须经人工审核确认，防止恶意污染。

### 4. Claims Report Templates / 理赔报告模板

```markdown
# 理赔分析报告（咨询草稿）
**生成时间**: YYYY-MM-DD HH:mm
**案件编号**: CL-XXXXXXXX
**险种类别**: [险种名称]
**处理状态**: [咨询草稿 — 需人工审核]
**免责声明**: 本报告为AI辅助生成的咨询草稿，所有结论须经持证理赔师审核确认后方可生效。
---
## 一、票据识别结果（仅供参考）
## 二、责任认定分析（仅供参考）
## 三、赔付计算参考（仅供参考）
## 四、反欺诈风险评估（仅供参考）
## 五、建议下一步行动（需人工确认）
```

---

## Compliance & Human Review / 合规与人工审核要求

| Compliance Item / 合规项 | Regulatory Basis / 监管依据 | Human Review Requirement / 人工审核要求 |
|--------------------|--------------------|----------------------|
| 理赔时效 | 《保险法》第23条 | 核定结果须经人工确认后发出 |
| 材料完整性 | 理赔管理办法 | 缺失材料列表由人工最终确认 |
| 反欺诈合规 | 《反保险欺诈工作办法》2024 | 欺诈标记须经人工调查确认 |
| 数据安全 | 《个人信息保护法》 | 医疗数据脱敏处理须经人工检查 |
| 资金安全 | 反洗钱规定 | 大额理赔须人工复核 + 主管审批 |

**ALL outputs of this skill are drafts requiring licensed professional review. / 本Skill所有输出均为草稿，须经持证专业人士审核。**

---

## Output Format / 输出格式规范

All outputs must include the following disclaimer:

```markdown
> ⚠️ **免责声明 / Disclaimer**
> 本输出为AI辅助咨询草稿，所有理赔决定、拒付结论、赔付金额及欺诈标签
> 须经【持证保险理赔师】审核确认后方可生效。
> This is an AI-assisted draft. All claim decisions must be reviewed by a
> licensed insurance adjuster before taking effect.
```

---

## References / 参考文件

| File / 文件 | Content / 内容说明 |
|------|---------|
| `references/claims_ocr_tech.md` | OCR技术架构参考 + 4家服务商对比 + Python示例代码（需自行配置API Key） |
| `references/claims_liability_engine.md` | 判责规则参考 + 机器学习模型参考 + 3家公司实践参考 |
| `references/claims_report_templates.md` | 报告模板 + 7种险种通知书模板参考 |

> **⚠️ Reference files contain example code only. You must:**
> - Provide your own API keys and store them in environment variables
> - Provide your own training data and models
> - Ensure human review of all outputs before use
> - **中文：** 参考文件仅含示例代码，您必须：自行提供API密钥并存入环境变量；自行准备训练数据和模型；确保所有输出经人工审核后方可使用。
