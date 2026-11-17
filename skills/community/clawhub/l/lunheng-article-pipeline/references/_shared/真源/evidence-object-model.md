> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）

> 🌐 **语言政策**：产出语言由 Phase 0「目标语言」字段**显式选择**（中文 / English / 中英混 / 其他，**不设默认**），全流程以该字段为准；中文特化按**目标语言客观适用**——含中文时 **G14 中文 AI 痕迹闸必跑**（v2.12.40 起不再是可选项），纯外语时记 `n/a`（客观不适用，非「关闭」）；GB/T 7714-2015 引用规范为可选能力。二者均不构成使用者语种限制。

# E1 证据对象与主张—证据链模型

> 版本：v2.18.1（发布版，与 SKILL.md version: 同步）
> 状态：第一阶段基础模型；尚未接入运行时闸门、外部全文服务或数据库。
> 适用范围：论衡内部证据登记与主张—证据关系追踪。
>
> 本文件是 E1 对象、字段、枚举和边界的唯一真源。模板、角色卡、派发说明和项目运行产物只引用本文件，不重复定义同名枚举。

## 1. 设计目的

论衡现有 `[Lxx]`、`[Dxx]`、`[Cxx]` 编号继续作为交付编号。本模型增加一个可追踪中间层，使核心正文主张能够沿以下路径回溯：

```text
正文主张 C-xxx → ClaimEvidenceLink → E-xxx 证据 → L/D/C 来源记录
```

E1 不是新的质量门，也不替代 G2（来源溯源）、G15（主张强度）、G17（硬数据指纹）或 T7/T8 的既有职责。

## 2. 三类对象

### 2.1 PaperRecord：论文记录

用途：描述文献身份、元数据、来源一致性和可访问性；不直接声称该文献支持某一主张。

必填字段：

- `record_type`: 固定为 `paper`
- `paper_id`: 稳定内部身份键；优先 `doi:<规范化 DOI>`，无 DOI 时依次使用 PMID、arXiv ID、稳定 URL、规范化标题键
- `title`
- `authors`: 作者数组；机构发布物可用机构名并注明匿名发布
- `year`
- `source_records`: 至少一个来源记录，含 `source`、`source_id`（如有）、`retrieved_at`
- `retrieval_status`: `candidate` / `verified` / `rejected`

推荐字段：

- `venue`
- `identifiers`: `doi` / `pmid` / `arxiv`
- `source_agreement`: 仅描述身份和元数据在多个来源间的一致程度，不等于证据强度
- `access.abstract`: `available` / `unavailable`
- `access.full_text`: `available` / `unavailable`
- `access.pdf`: `available` / `unavailable`
- `trust_level`: `published` / `owner_supplied`
- `notes`

边界：`full_text: unavailable` 必须保留，禁止下游默认为已读全文；PaperRecord 不能单独支撑实质理论判断。

### 2.2 SnippetRecord：原文片段记录

用途：定位文献、数据或案例中的可核验片段。一个片段只记录一个明确的证据单元；过长全文应拆分，不复制无关全文。

必填字段：

- `record_type`: 固定为 `fulltext_snippet`（论文/公开文本片段）或 `case_evidence`（案例/一手材料片段）
- `evidence_id`: 全项目唯一，论文片段使用 `E-xxx`，案例片段可使用 `E-Cxx`
- `source_ref`: 对应 `[Lxx]`、`[Dxx]` 或 `[Cxx]`；若为论文片段也可同时填写 `paper_id`
- `text` 或 `excerpt`: 原文片段，不得将 LLM 概述冒充原文
- `snippet_kind`
- `support_type`
- `retrieved_at`
- `verification_status`

可选字段：

- `query`
- `section`
- `location.page` / `location.paragraph` / `location.locator`
- `access_basis`: `open_access` / `abstract_only` / `owner_supplied` / `secondary_source`
- `relevance_score`: 仅为检索排序分数，不是论证强度
- `notes`

`snippet_kind` 枚举：

```text
title | abstract | body | methods | results | discussion | conclusion | metadata_only
```

`support_type` 枚举：

```text
direct | indirect | thematic | counter_evidence | identity_only
```

规则：

- `abstract_only` 不得生成“全文研究显示”或等价表述。
- 无页码、段落或稳定定位信息时不得编造定位信息。
- `metadata_only` 只能证明文献身份或元数据，不能支撑实质主张。
- `counter_evidence` 不得静默删除，必须交由 T6/T7 处理。
- `relevance_score` 不得转换成 `evidence_force`。

### 2.3 ClaimEvidenceLink：主张—证据关系

用途：把正文主张、证据对象和交付来源绑定起来，并记录关系类型、主张措辞强度及复核状态。

必填字段：

- `record_type`: 固定为 `claim_evidence_link`
- `claim_id`: 全项目唯一，如 `C-014`
- `evidence_id`: 指向已登记的证据对象
- `relation`
- `review_status`

推荐字段：

- `source_ref`: `[Lxx]` / `[Dxx]` / `[Cxx]`
- `claim_strength.causal_force`: 0–5
- `claim_strength.evidence_force`: 1–5
- `claim_strength.wording`: 正文实际使用的动词或措辞
- `reviewer`: `T3` / `T4` / `T7` / `T8` / `owner`
- `reviewed_at`
- `allowed_use`
- `notes`

`relation` 枚举：

```text
directly_supports | indirectly_supports | contextualizes | qualifies | contradicts | insufficient
```

`review_status` 枚举：

```text
unreviewed | needs_human_review | reviewed | rejected
```

规则：

| relation | 正文用途 | 默认处置 |
|---|---|---|
| `directly_supports` | 直接证据 | 可保留当前措辞，但仍须符合 G15 |
| `indirectly_supports` | 限定后的机制判断 | 降低措辞或增加限定语 |
| `contextualizes` | 背景、概念或文献对话 | 不写成直接证明 |
| `qualifies` | 限制条件、边界或反方 | 纳入讨论/局限性 |
| `contradicts` | 反向证据 | 不得静默删除，交 T6/T7 |
| `insufficient` | 证据不足 | 不得支撑正文主张 |

### 2.4 登记表分片与写入纪律（v2.13.2，E1-3 微型实测 D-1）

**背景（实测 2026-09-25）**：T1 与 T3 并行 spawn 时按旧约定**同写** `run/<项目名>/research/evidence-register.md`（单一文件路径）。T3 于 22:14 写入 11 条 `case_evidence`，T1 于 22:30 收尾整文件写盘 ⇒ **T3 段全部消失**。危险点：文件**非空且格式合法**，状态机与 T7 审计都**无法从文件本身发现缺失**，属静默丢证据；本次靠主控比对子会话记录才逐字恢复。

规则：

- **主表** `run/<项目名>/research/evidence-register.md` 的**唯一生产者 = 主控（T0）**：在并表时刻写，负责合并、去重与统计口径归一。
- **并行写者一律写分片**：`run/<项目名>/research/evidence-register-<角色号>.md`（如 T1b 分片 / T2b 分片 / T3 分片）；**禁止**并行角色直接整文件覆盖主表。
- **写入方式**：分片首次可 `write` 建文件，其后**只追加**（`edit` 增量）；**禁止**用 `write` 覆盖任何已被其他角色写过的文件。
- **派发前置**：主控在任务书中显式写明「本路径是否存在其他并行写者」；存在 ⇒ 必须分片。
- **并表时机**：T4 初始映射前、T7 抽验前各做一次并表；并表后**保留分片文件不删**（分片是溯源证据）。
- **抽验增项（T7/T8）**：**分片齐全性** —— 主表与全部分片均存在且非空；某个并行角色的分片缺失 ⇒ 记 **P1**。
- **归约口径真源（新增）**：本节规则已**升格为全产物族通用契约** —— 字段级写入权与归约口径的**唯一真源 = [`状态归约契约.md`](状态归约契约.md)**；本节只保留 E1 专属判例与抽验增项；与真源冲突时以真源为准。

### 2.5 主张关系的强制回写（v2.13.2，E1-3 微型实测 D-4）

**背景（实测 2026-09-25）**：项目产出了 `analysis/主张—证据映射.md`（20 条 `C-xxx` 主张、六类关系枚举齐全），但**主表 `ClaimEvidenceLink` 记录数 = 0** —— 主张关系从未回写登记表。后果：E1「**单表可审计**」目标未达成，主张—证据关系审计退化回「引用存在性审计」，而这正是 E1 要修的病。

规则：

- `ClaimEvidenceLink` 是 E1 的**核心对象**：主张关系必须**回写登记表**（主表或该角色的分片）；仅存在于映射表**不算完成**。
- 映射表（`analysis/主张—证据映射.md`）继续作为 T4 的**工作底稿**；回写时由主控并表，`claim_id` / `evidence_id` / `relation` 三字段**逐字一致**（禁两处各写一套枚举值）。
- **否决项（T7/T8）**：出现「**登记表 `ClaimEvidenceLink` = 0 而映射表有条目**」⇒ 记 **P1** 并在审计/终检报告显式列出，**不得**作为「已完成 E1 覆盖」通过。
- 空表、只写统计不写记录、统计与记录不一致，均不得判为已完成（同 §5）。

## 3. 主张强度：复用 G15，不新建判据

E1 只结构化记录 G15 已有的双轴，不另立一套门：

```text
causal_force：0 描述/共现，1 一致/伴随，2 相关，3 预示/贡献，4 影响，5 强因果
evidence_force：1 推测，2 相关，3 支持，4 直接，5 多源/充分确立
```

两个轴不得混用。至少进入 P1 复核的情形包括：正文写“导致”而证据只有相关性；正文写“证明”而证据只有主题相关片段；正文写“普遍存在”而证据仅来自少量案例；摘要关键词匹配被写成全文研究结论；修订后措辞强度升级。

## 4. 来源与编号边界

- `[Lxx]`：文献；`[Dxx]`：数据；`[Cxx]`：案例；继续作为交付编号。
- `paper_id`：论文内部身份键，不取代 `[Lxx]`。
- `E-xxx`：证据片段编号；`C-xxx`：正文主张编号；二者不得混淆。
- 多源一致性只描述身份/元数据一致性，不自动等于高质量证据。
- 证据登记表记录来源和访问状态；不替代文献卡、数据卡、案例卡。

## 5. 空值与访问状态

- 不可获得的内容写明确枚举值 `unavailable`，不得留空后让下游猜测。
- 未核验关系写 `needs_human_review` 或 `unreviewed`，不得写成 `reviewed`。
- 无法支持主张写 `insufficient`，不得为了填满登记表改写为 `thematic`。
- 空证据登记表不等于“证据链已完成”；旧项目没有登记表时，按兼容规则继续运行，但不得声称已完成 E1 覆盖。

## 6. 外部服务与权限边界

E1 不新增外发类别。v2.17.0 起学术检索层（AI4Scholar 工具族 `academic_extra` + OpenAlex/Crossref）**已归入 `external-services.md` 既有类别 ②「学术检索与元数据」**（opt-in，Phase 0 勾选），不升为新类别，也不把供应商接口键名写入核心协议。未来接入任何**新的**外部全文/学术服务，仍必须先遵守 [`external-services.md`](external-services.md) 与 Phase 0 外部服务同意门；禁止上传未公开全文、客户材料或完整正文。

**E1 与学术层的接线口径**：经学术层取得的元数据与全文片段**不因工具来源可信而免核验**——`retrieval_status` 仍按 `candidate` / `verified` / `rejected` 三值实记；经 `read_*` 取得全文的 `SnippetRecord` 填 `access_basis: open_access`，仅得摘要填 `abstract_only`；批量元数据接口（shell 命令）返回的是**检索排序与被引数**，不得转写为 `evidence_force`（沿用 §2.2「`relevance_score` 不得转换成 `evidence_force`」）。E1 不新增 exec、宿主配置读取或运行时数据库依赖。

## 7. 接线状态

第一阶段只提供对象模型和模板。T1/T3/T4/T7/T8 的角色接线、机械校验和真实项目验证必须分步完成；在这些步骤完成前，E1 字段均为可选能力，不能把旧项目判为失败。
