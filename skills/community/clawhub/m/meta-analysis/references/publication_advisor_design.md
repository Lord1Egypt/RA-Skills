# 发表建议引擎（Publication Advisor）设计备忘

> 状态：P2 备档（未实现，待后续排期）
> 创建：2026-09-13

## 目标

基于分析结果 + 领域，给出论文撰写和投稿的实用建议，包括：
- 论文结构模板（IMRaD 各段怎么写）
- 限制段要点
- 目标期刊推荐
- 审稿人可能问的问题（扩展版）
- 投稿前检查清单

## 输入

```python
{
    "stats": {...},          # coze 返回的 stats
    "task": "pairwise_meta",
    "params": {"sm": "OR"},
    "topic": "EGFR-TKI 一线治疗 NSCLC",  # 研究主题
    "field": "oncology",                  # 领域（从 topic 推断或用户指定）
    "grade": "Moderate",                  # GRADE 等级（来自 quality_advice）
    "interpretation": {...},              # 来自 interpretation.py
}
```

## 输出

```python
publication_advice = {
    "reporting_checklist": "PRISMA 2020: 需报告检索策略、筛选流程、偏倚风险评估、GRADE。",
    "strengths": ["多中心研究合并", "低异质性", "发表偏倚不显著"],
    "limitations": ["纳入研究数较少（k=5）", "高异质性未解释", "仅中文文献"],
    "discussion_template": "本研究发现 XX 与 YY 显著相关（OR=2.15, 95%CI 1.38-3.35）。然而，高异质性（I²=78%）提示...",
    "reviewer_likely_questions": [
        "是否评估了纳入研究的偏倚风险（Cochrane RoB 2.0 / NOS）？",
        "是否探索了异质性来源？",
        "是否考虑了发表偏倚对结果的影响？",
    ],
    "journal_fit": "建议投稿方向：流行病学 / 公共卫生 / 对应专科期刊（IF 2-5 档）。",
    "prisma_checklist": ["检索策略", "筛选流程", "偏倚风险评估", "GRADE"],
    "data_availability": "建议公开分析代码与数据。",
}
```

## 实现方案

### 文件：`adapters/publication_advisor.py`

```python
def advise_publication(stats, task, params, topic="", field=""):
    """基于分析结果生成发表建议。"""
    # 1. 调用 interpretation + quality_advice 获取基础解读
    # 2. 基于 field 选择领域模板（oncology / cardiology / psychology ...）
    # 3. 生成 discussion_template（填空式）
    # 4. 推荐期刊（基于 field + 研究类型 + IF 档位）
    # 5. 返回结构化建议
```

### 领域知识库：`references/field_templates.json`

```json
{
  "oncology": {
    "journal_tiers": [
      {"name": "Lancet Oncology", "if": 50, "tier": "top"},
      {"name": "JCO", "if": 40, "tier": "top"},
      {"name": "Annals of Oncology", "if": 30, "tier": "high"},
      {"name": "European Journal of Cancer", "if": 8, "tier": "mid"},
    ],
    "reporting_guideline": "PRISMA + CONSORT (RCT) / STROBE (观察性)",
    "common_limitations": ["仅英文文献", "未注册 protocol", "回顾性设计"]
  },
  "cardiology": { "..." : "..." }
}
```

## 依赖

- `interpretation.py`（P0 已就绪）
- `quality_advice.py`（P1 已就绪）
- `references/field_templates.json`（需新建，按领域积累）

## 测试策略

- 单测：各领域模板渲染、期刊推荐逻辑
- 集成：run_analysis 中可选启用（`advise=True`）

## 落地优先级

P2 — 待 P0+P1 稳定后（≥2 周无 P0/P1 bug）再启动。
