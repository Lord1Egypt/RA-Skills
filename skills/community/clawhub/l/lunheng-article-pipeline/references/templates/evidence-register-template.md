> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# 证据登记表

> E1-0 模板 v2.13.0-E1-0（2026-09-24）
> 对象、字段和枚举唯一真源：[`../_shared/真源/evidence-object-model.md`](../_shared/真源/evidence-object-model.md)
> 用途：供 T1/T3/T4/T7/T8 共享的项目级证据登记；不替代文献卡、数据卡或案例卡。

## 项目元数据

- 项目：
- 生成阶段：T1 / T3 / T4 / T7 / T8
- 生成时间：
- 证据截止时间：
- 外部服务同意模式：
- 证据登记状态：`not_started` / `in_progress` / `needs_review` / `complete`

## 分片（v2.13.2；并行写者必读）

> 本表是**主表**，**唯一生产者 = 主控**。并行角色（T1 / T2 / T3 / T1b / T2b …）一律写自己的分片 `research/evidence-register-<角色号>.md`，**禁止**整文件覆盖本表（实测发生过整段静默覆盖）。

- 主表：`run/<项目名>/research/evidence-register.md`
- 分片清单：<逐项列 `evidence-register-<角色号>.md`，含存在性>
- 并表时间：
- 分片齐全性：<✅ / ⚠️ 缺哪个角色的分片>

## 证据统计

> 统计必须与下方实际记录一致；空表只能填 `0`，不得写“已完成”。

- PaperRecord：0
- SnippetRecord：0
- ClaimEvidenceLink：0
- 直接支持（`direct` / `directly_supports`）：0
- 间接支持（`indirect` / `indirectly_supports`）：0
- 仅主题相关（`thematic` / `contextualizes`）：0
- 反向证据（`counter_evidence` / `contradicts`）：0
- 证据不足（`insufficient`）：0
- 未核验：0
- 全文可核验：0
- 仅摘要：0
- 无证据核心主张：0
- 疑似主张强度超过证据：0

## PaperRecord：论文记录

```yaml
record_type: paper
paper_id: doi:10.xxxx/xxxxx
title: "论文标题"
authors: ["作者一", "作者二"]
year: 2024
venue: "期刊或会议"
identifiers:
  doi: "10.xxxx/xxxxx"
  pmid: null
  arxiv: null
source_records:
  - source: semantic_scholar
    source_id: ""
    retrieved_at: "YYYY-MM-DD"
source_agreement: 1
access:
  abstract: available
  full_text: unavailable
  pdf: unavailable
trust_level: published
retrieval_status: candidate
notes: "付费墙/摘要限制/身份去重说明"
```

## SnippetRecord：原文片段

```yaml
record_type: fulltext_snippet
evidence_id: E-001
paper_id: doi:10.xxxx/xxxxx
source_ref: [L01]
query: "检索词"
text: "原文片段；不得用模型概述冒充原文。"
snippet_kind: abstract
section: "Abstract"
location:
  page: null
  paragraph: null
  locator: null
retrieved_at: "YYYY-MM-DD"
access_basis: abstract_only
relevance_score: null
support_type: indirect
verification_status: needs_human_review
notes: "该片段能支持什么、不能支持什么"
```

## ClaimEvidenceLink：主张—证据关系

```yaml
record_type: claim_evidence_link
claim_id: C-001
evidence_id: E-001
source_ref: [L01]
relation: indirectly_supports
claim_strength:
  causal_force: 2
  evidence_force: 2
  wording: "与……相关"
allowed_use: qualified_body_claim
review_status: needs_human_review
reviewer: T4
reviewed_at: null
notes: "需要的限定语或缺口"
```

## 主张—证据汇总表

| Claim ID | 正文主张摘要 | Evidence ID | 来源 | 关系 | 证据访问状态 | G15 措辞是否匹配 | 复核状态 | 缺口 |
|---|---|---|---|---|---|---|---|---|
| C-001 | （示例）主张摘要 | E-001 | [L01] | indirectly_supports | abstract_only | 待核 | needs_human_review | 缺直接原文 |

## 反向证据与限制

- 反向证据编号及对应主张：
- 仅摘要可得文献：
- 仅元数据可得记录：
- 付费墙/访问失败：
- 需要主人核验或裁决：

## T7/T8 抽验记录

- **分片齐全性**（主表 + 全部分片存在且非空）：未检查
- **主张关系是否已回写**（登记表 `ClaimEvidenceLink` 计数 ≠ 0，且与映射表逐字一致）：未检查（主表为 0 而映射表有条目 ⇒ **P1**）
- 核心主张是否均可回指 ClaimEvidenceLink：未检查
- 登记来源是否存在对应 `[Lxx]` / `[Dxx]` / `[Cxx]`：未检查
- 证据关系与正文措辞是否一致：未检查
- 访问限制是否在交付说明/局限性披露：未检查
- 抽验结论：
