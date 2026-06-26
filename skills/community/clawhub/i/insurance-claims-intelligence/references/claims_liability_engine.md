# 保险理赔判责引擎参考框架（advisory only / 咨询级）

> ⚠️ **DISCLAIMER / 免责声明**
> - **English:** This document provides advisory frameworks, checklists, and reference code ONLY. It does NOT contain production-ready models, pre-trained weights, or automated claim decision capabilities. All accuracy figures (e.g., "93% cases", "60 seconds") are literature-reported benchmarks or design targets, NOT validated results of your deployment. ALL claim approvals, denials, and payout amounts MUST be reviewed and confirmed by a licensed insurance professional before use.
> - **中文：** 本文档仅提供咨询框架、检查清单和参考代码，不含生产级模型、预训练权重或自动化理赔决策能力。所有准确率数据（如"93%案件"、"60秒"）均来自文献基准或设计目标，非您部署后的实测结果。所有理赔核准、拒付及赔付金额**必须经持证保险专业人士审核确认后方可使用**。

> 🔒 **Human Review Mandatory / 强制人工审核**
> - **NO automatic approval** — this framework only generates **decision-support suggestions**.
> - **严禁自动审批** — 本框架仅生成**决策支持建议**，不具有任何自动审批能力。
> - All outputs are **drafts** requiring licensed adjuster review and regulatory compliance check.
> - 所有输出均为**草稿**，须经持证理赔师审核及监管合规检查。

---

## 一、判责引擎参考架构（人工审核框架）

### 架构说明（所有输出需人工确认）

```
输入层：OCR结构化数据 + 保单信息 + 被保险人档案
  ↓
预处理层：数据清洗 → 字段标准化 → 缺失值处理
  ↓
规则引擎层（粗筛）：确定型规则快速分流
  ├─ 等待期检查 → 建议拒付/继续（须人工确认）
  ├─ 既往症检查 → 建议拒付/比例赔付/继续（须人工确认）
  ├─ 免赔额检查 → 建议暂不赔付/继续（须人工确认）
  ├─ 医院级别检查 → 提示确认/继续（须人工确认）
  └─ 险种责任匹配 → 建议全额/比例/拒付（须人工确认）
  ↓
ML推理层（精审）：不确定案件深度分析（参考框架）
  ├─ NLP诊断解析 → ICD编码映射（须人工确认）
  ├─ 治疗合理性分析 → DRG/DIP对照（须人工确认）
  ├─ 费用异常检测 → 孤立森林/LOF（须人工确认）
  └─ 欺诈风险评分 → 知识图谱参考（须人工确认）
  ↓
赔付计算层：条款公式 → 核定金额参考（须人工确认）
  ↓
输出层：理赔核定建议 / 拒付建议 / 补充材料建议
  ↓
⚠️ 【强制环节】持证理赔师人工审核 → 合规检查 → 最终决定
```

> ⚠️ **重要：** 以上架构中的任何"自动"、"秒级"、"全自动"描述均已删除。本框架仅提供**建议**，所有决定须由授权人工审核员作出。

---

## 二、规则引擎参考清单（需人工逐项确认）

### 2.1 等待期检查（参考清单）

| 险种 | 标准等待期 | 特殊约定 | 判责参考逻辑（须人工确认） |
|------|-----------|---------|--------------------------|
| 医疗险 | 30天 | 意外无等待期 | 出险日期 - 保单生效日 < 等待期 → 建议拒付（意外除外），**须人工确认** |
| 重疾险 | 90天/180天 | 意外无等待期 | 确诊日期 - 保单生效日 < 等待期 → 建议拒付，**须人工确认** |
| 寿险 | 90天/180天 | 意外无等待期 | 身故日期 - 保单生效日 < 等待期 → 建议拒付，**须人工确认** |
| 意外险 | 无等待期 | 次日生效 | 直接通过（仍须人工确认） |

```python
# ⚠️ 参考代码（须自行测试、验证，并经人工审核后使用）
def check_waiting_period(policy: dict, claim: dict) -> dict:
    """等待期检查（参考实现，须经人工审核）"""
    waiting_days = policy.get("waiting_days", 30)
    effect_date = parse_date(policy["effect_date"])
    incident_date = parse_date(claim["incident_date"])
    is_accident = claim.get("is_accident", False)

    if is_accident:
        return {"pass": True, "reason": "意外事故无等待期（建议，须人工确认）"}

    days_diff = (incident_date - effect_date).days
    if days_diff < waiting_days:
        return {
            "pass": False,
            "reason": f"等待期内（生效{days_diff}天，等待期{waiting_days}天）",
            "action_suggestion": "REJECT",  # ⚠️ 仅为建议，非自动决定
            "human_review_required": True
        }
    return {"pass": True, "reason": f"等待期已过（生效{days_diff}天）", "human_review_required": True}
```

### 2.2 既往症筛查（参考清单）

**既往症定义（监管标准，仅供参考）：**
1. 保险合同生效前，医生已有明确诊断、长期治疗未间断
2. 保险合同生效前，医生已有明确诊断、治疗后症状未完全消失、有间断用药
3. 保险合同生效前，医生已有明确诊断、但未予治疗
4. 保险合同生效前，已有体检异常、但未确诊

```python
# ⚠️ 参考代码（须自行准备患者病史数据，并经人工审核）
def check_preexisting(claim_diagnosis: str, patient_history: list) -> dict:
    """既往症筛查（参考实现，须经人工审核）"""
    risk_score = 0
    matched_conditions = []

    for condition in patient_history:
        if fuzzy_match(claim_diagnosis, condition["diagnosis"]):
            risk_score += condition.get("severity", 1)
            matched_conditions.append(condition["diagnosis"])

    if risk_score >= 2:
        return {
            "is_preexisting_suspected": True,  # ⚠️ 仅为疑似，非确诊
            "matched": matched_conditions,
            "action_suggestion": "REJECT",
            "human_review_required": True,
            "note": "须由理赔师结合病历进一步确认"
        }
    return {"is_preexisting_suspected": False, "human_review_required": True}
```

### 2.3 免赔额校验（参考清单）

```python
# ⚠️ 参考代码（须经人工审核）
def check_deductible(claim_amount: float, policy: dict, ytd_paid: float) -> dict:
    """免赔额校验（参考实现，须经人工审核）"""
    deductible = policy.get("deductible", 0)
    self_pay = claim_amount

    accumulated = ytd_paid + self_pay
    if accumulated <= deductible:
        return {
            "pass": False,
            "reason": f"未达免赔额（累计{accumulated:.2f}元，免赔{deductible:.2f}元）",
            "action_suggestion": "DEFER",
            "human_review_required": True
        }

    payable = accumulated - deductible
    return {
        "pass": True,
        "payable_suggestion": payable,  # ⚠️ 仅为建议金额
        "reason": f"已达免赔额，建议赔付{payable:.2f}元",
        "human_review_required": True
    }
```

### 2.4 医院级别核查（参考清单）

| 医院等级 | 医疗险 | 重疾险 | 寿险 | 意外险 |
|---------|--------|--------|------|--------|
| 三甲 | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） |
| 三乙/三丙 | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） |
| 二甲 | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） | ✅ 建议通过（须人工确认） |
| 二乙 | 视条款（须人工确认） | 视条款（须人工确认） | ✅ 建议通过（须人工确认） | 视条款（须人工确认） |
| 一级/社区 | 视条款（须人工确认） | 视条款（须人工确认） | ✅ 建议通过（须人工确认） | 视条款（须人工确认） |
| 私立医院 | 视条款（通常排除，须人工确认） | 视条款（须人工确认） | 视条款（须人工确认） | 视条款（须人工确认） |

### 2.5 险种责任匹配（参考清单）

```python
# ⚠️ 参考代码（须经人工审核）
def match_coverage(diagnosis: str, policy_coverage: dict) -> dict:
    """责任范围匹配（参考实现，须经人工审核）"""
    icd_code = map_to_icd10(diagnosis)  # 须自行实现并验证

    if policy_coverage["type"] == "critical_illness":
        if icd_code in policy_coverage.get("covered_icd", []):
            return {"match": True, "payout_type_suggestion": "FULL", "human_review_required": True}
        else:
            return {"match": False, "action_suggestion": "REJECT", "human_review_required": True}

    if policy_coverage["type"] == "medical":
        if is_medical_necessary(diagnosis) and in_medical_catalog(icd_code):
            return {"match": True, "payout_type_suggestion": "REIMBURSE", "human_review_required": True}
        else:
            return {"match": False, "action_suggestion": "REJECT", "human_review_required": True}

    if policy_coverage["type"] == "accident":
        if claim.get("accident_proof"):
            return {"match": True, "payout_type_suggestion": "FULL_OR_PARTIAL", "human_review_required": True}
        else:
            return {"match": False, "action_suggestion": "REQUEST_DOC", "human_review_required": True}
```

---

## 三、机器学习精审参考框架（须人工确认所有输出）

### 3.1 NLP诊断解析 + ICD编码映射（参考）

```python
# ⚠️ 参考代码（须自行准备训练数据和模型，输出须经人工确认）
import torch
from transformers import BertTokenizer, BertModel

def diagnose_nlp_analysis(diagnosis_text: str) -> dict:
    """
    NLP诊断解析参考实现
    ⚠️ 须自行 fine-tune 模型，输出须经人工确认
    """
    # ⚠️ 须自行准备训练好的模型和ICD-10数据库
    # tokenizer = BertTokenizer.from_pretrained("your-fine-tuned-model")
    # model = BertModel.from_pretrained("your-fine-tuned-model")
    # icd_db = load_your_icd10_database()

    raise NotImplementedError(
        "须自行准备fine-tuned模型和ICD-10数据库，并对所有输出进行人工审核"
    )
```

### 3.2 治疗合理性分析（DRG/DIP对照参考）

```python
# ⚠️ 参考代码（须经人工审核）
def check_treatment_reasonableness(diagnosis: str, treatments: list, total_fee: float) -> dict:
    """
    治疗合理性分析参考实现
    ⚠️ 须自行准备DRG标准数据库，输出须经人工确认
    """
    # drg_group = map_to_drg(diagnosis)  # 须自行实现
    # std_fee_range = drg_group["fee_range"]

    flags = []
    # if total_fee > std_fee_range[1]:
    #     flags.append(f"总费用超出DRG标准上限")
    # if total_fee < std_fee_range[0] * 0.5:
    #     flags.append(f"总费用异常偏低")

    return {
        "drg_group_suggestion": "须自行实现",
        "flags": flags,
        "reasonableness_score_suggestion": max(0, 100 - len(flags) * 20),
        "human_review_required": True,
        "note": "所有标记须经人工调查确认，不可自动拒付"
    }
```

### 3.3 欺诈风险评分（参考框架，非自动标记）

```python
# ⚠️ 参考代码（所有风险评分须经人工调查确认，不可自动拒付）
def fraud_risk_scoring_reference(claim: dict, graph: "nx.Graph | None") -> dict:
    """
    欺诈风险评分参考框架
    ⚠️ 所有评分仅为调查优先级参考，不可作为自动拒付依据
    """
    risk_score = 0
    risk_factors = []

    # 因子1：同一患者短期内多次理赔（须人工核实）
    # if claim.get("recent_claim_count", 0) >= 3:
    #     risk_score += 30
    #     risk_factors.append("同一患者短期内多次理赔，建议人工调查")

    # 因子2：多家保险公司同时索赔（须人工调查）
    # if claim.get("multi_insurer", False):
    #     risk_score += 40
    #     risk_factors.append("多家公司同时索赔，建议人工调查")

    # 所有评分仅为调查优先级参考
    if risk_score >= 70:
        action = "PRIORITY_INVESTIGATE"  # 优先调查（非自动拒付）
    elif risk_score >= 40:
        action = "ENHANCED_REVIEW"  # 加强审核
    else:
        action = "ROUTINE_REVIEW"  # 常规审核

    return {
        "risk_score_suggestion": risk_score,
        "risk_factors": risk_factors,
        "suggested_action": action,  # ⚠️ 仅为建议
        "human_review_required": True,
        "note": "所有欺诈风险评估须经人工调查确认，不可作为自动拒付依据"
    }
```

### 3.4 赔付金额计算（参考公式，须经人工确认）

```python
# ⚠️ 参考代码（所有赔付金额须经人工确认）
def calculate_payout_reference(claim_data: dict, policy: dict) -> dict:
    """赔付金额计算参考公式（须经人工确认）"""
    coverage_type = policy["coverage_type"]

    if coverage_type == "reimbursement":  # 报销型
        total_fee = claim_data["total_fee"]
        medical_insurance_pay = claim_data.get("medical_insurance_pay", 0)
        personal_pay = total_fee - medical_insurance_pay
        deductible = policy.get("deductible", 0)
        reimbursement_ratio = policy.get("reimbursement_ratio", 1.0)
        payable = max(0, (personal_pay - deductible)) * reimbursement_ratio
        return {
            "payout_suggestion": round(payable, 2),  # ⚠️ 仅为建议
            "formula": f"({personal_pay} - {deductible}) × {reimbursement_ratio}",
            "human_review_required": True
        }

    elif coverage_type == "fixed":  # 定额给付
        return {
            "payout_suggestion": policy["sum_insured"],
            "formula": "保额全额给付（须人工确认条款条件）",
            "human_review_required": True
        }

    # ... 其他险种类似，所有输出均须人工确认
```

---

## 四、行业实践参考（文献综述，非本Skill实测结果）

> ⚠️ **重要：** 以下公司实践描述为公开文献报道的参考信息，非本Skill的实测性能。部署效果取决于您的数据、模型和配置。

### 4.1 平安"111极速赔"（公开报道参考）

```
公开报道的技术方向参考：
  用户上传材料（拍照/PDF）
    ↓
  大模型解析（材料理解）
    ↓
  规则引擎判责
    ↓
  大模型复核（边缘case处理）
    ↓
  结果：公开报道称93%案件60秒内完成（⚠️ 此为平安报道数据，非本Skill承诺）
```

**创新点（公开报道摘录）：**
- 大模型理解非结构化医疗文本
- 端到端处理流程优化

### 4.2 中国人寿智能理赔（公开报道参考）

```
公开报道的理赔金额分层处理方式（⚠️ 仅供参考，须按您的合规要求配置）：
  理赔金额 ≤ 20000元 → 系统建议 → 人工审核确认 → 到账
  20000元 < 金额 ≤ 50000元 → AI建议 + 人工复核 → 当天到账
  金额 > 50000元 → 完整调查流程 → 3个工作日内
```

### 4.3 太保"数字劳动力实验室"（公开报道参考）

```
公开报道的Agent工作流方向（⚠️ 仅供参考）：
  [接收案件] → [OCR识别] → [条款解析] → [判责决策建议]
    → IF 简单案件 → 建议 → 人工确认
    → IF 复杂案件 → 生成调查清单建议 → 派单调查员（人工）
    → IF 高风险标记（建议） → 转反欺诈团队（人工调查）
```

---

## 五、判责决策参考树（所有路径须人工确认）

```
案件提交
  │
  ├─ 规则检查（参考清单）
  │   ├─ 等待期未过 → 建议拒付（须人工确认）
  │   ├─ 既往症命中 → 建议拒付/比例赔付（须人工确认）
  │   ├─ 未达免赔额 → 建议暂不赔付（须人工确认）
  │   ├─ 医院不合规 → 提示确认/建议拒付（须人工确认）
  │   └─ 险种不匹配 → 建议拒付（须人工确认）
  │
  ├─ IF 规则检查全部通过（建议）：
  │   ├─ 简单案件 → 生成赔付建议（⚠️ 须人工确认）
  │   ├─ 复杂案件 → 生成复核建议（⚠️ 须人工确认）
  │   ├─ 大额案件 → 生成调查建议（⚠️ 须人工确认）
  │   └─ 高风险标记（建议） → 进入反欺诈调查流程（人工）
  │
  └─ ⚠️【强制环节】持证理赔师人工审核 → 合规检查 → 最终决定
```

---

## 六、反欺诈数据治理规范（必读）

> 🔒 **数据治理要求（合规必备）**

### 6.1 数据留存期限
- 反欺诈图谱数据建议留存不超过 **2 年**，除非监管要求更长留存期
- 已结案件的数据须定期归档或匿名化处理

### 6.2 访问控制
- 反欺诈图谱查询权限仅开放给 **授权欺诈调查员**
- 禁止非授权人员（如客服、销售）访问欺诈评分和图谱数据
- 所有查询须留下审计日志（谁、何时、查询了哪个案件）

### 6.3 数据更正流程
- 被保险人和投诉方有权请求更正错误数据
- 数据更正请求须在 **15 个工作日内** 处理完毕
- 更正后须通知所有曾收到该错误数据的决策环节

### 6.4 图谱污染防护
- 新案件数据进入图谱前，须经 **人工审核确认** 数据质量
- 禁止将未经验证的第三方提供数据直接写入生产图谱
- 定期（建议每季度）对图谱数据进行质量审计

---

## 七、模型效果评估指标（文献参考值，非承诺）

| 指标 | 文献参考值 | 说明 |
|------|------------|------|
| 自动通过率 | ~70% | 文献报道行业水平，非本Skill承诺 |
| 误拒率（False Reject） | ≤ 2% | 文献报道行业水平，非本Skill承诺 |
| 漏检率（Fraud Escape） | ≤ 1% | 文献报道行业水平，非本Skill承诺 |
| 平均处理时长 | ≤ 1分钟（自动案件） | 取决于部署配置，非本Skill承诺 |
| 客户满意度 | ≥ 85% | 文献报道行业水平，非本Skill承诺 |

> ⚠️ **重要：** 以上指标均为文献报道的行业参考值，非本Skill的性能承诺。实际效果取决于您的数据质量、模型训练、规则配置和人工审核流程。

---

*Last updated: 2026-05-05 — 删除所有自动审批描述；准确率/性能数据标注为文献基准（非本Skill实测）；所有输出增加"须人工确认"标注；增加反欺诈数据治理规范；增加强制人工审核环节说明。*
