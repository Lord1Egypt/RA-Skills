# Multi-Model Consensus Council — Operation & User Guide

## 📋 Version History

| Version | Date | Changes |
|:---|:---|:---|
| V1.0.0 | 2026-04-19 | Initial release: core framework, 3-round convergence, 6-section report |
| V1.1.0 | 2026-04-24 | Added English operation guide (merged with Chinese, English first); translation reviewed and approved by multi-model committee (Gemini/Doubao/GLM, avg 81/100); wording optimizations |
| V1.1.3 | 2026-04-24 | SKILL.md and references/ converted to pure Chinese for AI readability; docs/ retains full bilingual documentation for global community |
| V1.2.0 | 2026-04-25 | Restored public ClawHub version (was local customized); sync all files |
| V1.2.1 | 2026-04-25 | **CRITICAL FIX**: Removed hardcoded model list (A1/A2/A4...) from SKILL.md; replaced with dynamic scan via `openclaw models list`; examples updated to use generic `[Model A/B/C]` placeholders |
| V1.2.2 | 2026-04-25 | SYNC: Full file sync to GitHub and ClawHub after v1.2.1 hotfix |
| V1.2.3 | 2026-04-25 | **UX FIX**: Clarify first-time user flow: auto-scan models → default to first 3 → prompt user to confirm/modify before starting decision |
| V1.2.4 | 2026-04-25 | **CRITICAL FIX**: OUTPUT_TEMPLATE.md - remove "匿名委员" from all 3 round prompt templates; replaced with real-name format `{模型名称}（实名委员）` |
| V1.2.5 | 2026-04-25 | **ENFORCEMENT**: SKILL.md - add mandatory threshold check rules; add forbidden items for skipping threshold/convergence checks; state machine now has explicit checkpoint enforcement |
| V1.2.6 | 2026-04-25 | **Real-name Transparency**: Judges use standard model names; 3-layer architecture (organizer/judge/sub-agent); 100-point scoring; Round 0 preparation phase added |
| V1.5.0 | 2026-04-25 | Sync all document versions to V1.5.0; renamed SCHEMA.md; full English content aligned with Chinese |
| V1.5.1 | 2026-04-26 | Added round-start user notification rule; added convergence score threshold parameter; added exception handling rules section |
| V1.5.2 | 2026-04-26 | Added judgment method configurable parameter; clarified unanimous-pass rule as default |
| **V1.6.0** | **2026-04-27** | **MAJOR FIX**: Rewrote sub-agent result recovery; added runtime environment adaptation matrix; Push-based waiting flow; runtime self-check; simplified state management; added TROUBLESHOOTING.md |
| **V1.6.1** | **2026-04-27** | **Clarified judgment rules**: Separated "Pass" vs "Convergence" vs "Consensus Selection"; clarified convergence discussion scope; renamed "Round 3" to "Final Round"; added Consensus Selection for final round |
| **V1.6.2** | **2026-04-27** | **Core logic refactored**: Removed "Convergence"; introduced "Decision Point" level review; "Convergence Discussion" renamed to "Dispute Discussion"; final report includes decision point status (✅/🟡/🔴) |
| **V1.6.5** | **2026-04-30** | **Security Hardening**: Removed unused `Exec` from allowed-tools; reduced max concurrent sub-agents from 13 to 6; added `Write` tool path restriction (memory directory only); added model-routing early termination rule in TROUBLESHOOTING.md |
| **V1.6.6** | **2026-04-30** | **Security Fix**: Replaced `openclaw.json` file scan with `openclaw models list` command to avoid exposing provider tokens; corrected committee size description from 3-13 to 3-6 models; added Read/Write tool path whitelist in SKILL.md |
| **V1.6.7** | **2026-04-30** | **Auditability Fix**: Clarified tool usage scope—organizers use Read/Write, judges receive content via task parameter and must not call any tools; removed contradictory "internal-only" markings; eliminated ambiguous judge spawn instructions in OUTPUT_TEMPLATE.md |

---

## 🎯 Plugin Overview

**Multi-Model Consensus Council** is a "Digital Think Tank" designed for OpenClaw. It coordinates multiple large language models (e.g., GPT, Gemini, Doubao) to collaboratively analyze, debate, and synthesize decisions, effectively eliminating single-model bias.

### Core Advantages

- **Decentralized Decision-Making**: Cross-validates reasoning across models, ensuring rigor.
- **Adversarial Review**: Rapidly identifies logical flaws through peer evaluation.
- **Elastic Scaling**: Adjust the number of "decision committee members" anytime based on task complexity.
- **Bias Elimination**: Multi-model independent review avoids single-AI cognitive blind spots.
- **Quantitative Decision-Making**: 6-dimension scoring + weighted matrix, conclusions are evidence-based.
- **Transparency & Trust**: Real-name committee system, model identity visible.
- **Flexible Configuration**: All parameters adjustable — number of members, decision rounds, pass threshold, etc.

---

## ⚖️ Core Governance Principle: Identity Purity

To ensure absolute objectivity, this plugin enforces the **"Identity Purity Principle"**:

- **Identity Transparency**: All committee members are identified by their model name (e.g., Kimi K2.6, GPT-5.4), maintaining visual transparency.
- **No Role Assignment**: Committee members are forbidden from having preset roles such as "architect" or "auditor".
- **No Biased Prompting**: Tasks must not include inducing prompts or identity roles targeted at committee members, preventing bias from prompt engineering.
- **No Sub-Agent Delegation**: Judges are strictly prohibited from spawning sub-agents. They must think independently and output their own conclusions. Complex tasks are decomposed and distributed by the organizer.
- **No Duplicate Review Principle**: If the organizer (the current model in use) is a committee member, their submitted content counts as their Round 1 review result — no duplicate self-review is required. If the organizer is not a committee member, they are responsible only for organizing and summarizing; they do not participate in the review.

---

## How to Use

- **Activation**: In OpenClaw, type "启动多模型决策委员会" (Start Multi-Model Consensus Council), "审议这个方案" (Review this plan), "对这个方案进行决策" (Make a decision on this plan), or "启动决策" (Start decision) to activate. On first use, the system will prompt you to enter configuration mode and select the model lineup.
- **Configuration**: Adjust parameters as needed, such as rounds, threshold, number of members, and member models.

### Parameter Configuration

| Command Keyword | Adjustable Parameter | Description |
|:---|:---|:---|
| "换模型" / "Change models" | Committee model mix | Select models from the locally connected model list |
| "改轮数" / "Change rounds" | Decision rounds | Default 3 rounds; 2 for routine tasks; 3-6 for critical decisions |
| "改阈值" / "Change threshold" | Judgment thresholds | **Pass threshold**: default ≥90%; **Pending threshold**: default [72%, 90%); **Reject threshold**: default <72% |
| "增加委员" / "Add member" | Committee size | Increase number of committee members |
| "减少委员" / "Remove member" | Committee size | Decrease number of committee members |
| "确认配置" / "Confirm config" | Confirm current config | Confirm current parameters and begin decision |

### Parameter Recommendations

- **Model Selection**: Recommend at least 1 model with strong logical reasoning and 1 model with strong Chinese-language comprehension.
- **Round Recommendations**: Routine tasks: 2 rounds; Decisions involving architecture, funding, or core rules: 3-5 rounds.
- **Threshold Settings**:
  - **Strict**: ≥95% (near-unanimous)
  - **Efficient**: ≥75% (majority)

---

## Decision Process (3-Round Convergence Mechanism)

The Multi-Model Consensus Council adopts a 3-round convergence mechanism, with each round using a **100-point scoring system**, ultimately producing a decision result.

---

### Round 0: Preparation (Preparation)

**Task**: Upon receiving a decision task, the **organizer** (the current model in use) summarizes the user background, requirements, and the proposal to initiate the decision application. Content format:

- **Project Name**: {Project Name}
- **Project Background**: {Project Background}
- **Project Requirements**: {Project Requirements}
- **Proposal Under Review**: {Proposal Under Review}
- **Decision Members**: {Decision Members: pull from configured model lineup}
- **Decision Rounds**: {Decision Rounds: pull from configured round count}
- **Threshold Settings**: {Threshold Settings: pull from configured threshold}
- **Submit Decision**: {Submit whether the user wants to begin decision}

---

### Round 1: Independent Evaluation (Blind Evaluation)

**Action**: Upon receiving the decision confirmation, the organizer distributes the preparation content to each selected model's independent sub-session. Each committee member conducts closed-door review **without any awareness of other members' opinions**.

**Review Dimensions**: Logical completeness, risk analysis, resource cost estimation, feasibility review, optimization suggestions — all scored on a **100-point scale**.

**Review Duration**: No more than 3 minutes per round. If not all sub-sessions are recovered after 3 minutes, the organizer terminates the process and returns results.

**Core Output**: The organizer summarizes each committee member's initial review report, voting results, scores, and disagreement points or controversy areas.

---

### Round 2: Dispute Discussion

**Action**: The organizer extracts all decision points that did NOT achieve full pass in Round 1 (any judge scoring below threshold) and compiles them into an "unresolved decision points list." These unresolved points only are redistributed to all committee members for re-discussion and re-scoring. Points already with full pass are frozen and not re-discussed.

**Review Duration**: No more than 3 minutes per round. If not all sub-sessions are recovered after 3 minutes, the organizer terminates the process and returns results.

**Core Output**: Summarizes re-scoring results. If all previously unresolved points now achieve full pass, output the final report. If any remain unresolved, proceed to the final round.

---

### Final Round: Final Duel

**Special Note**: Regardless of how many rounds are configured, the Final Duel is **always the last round**.
- 3-round config: Round 3 is the Final Duel
- 5-round config: Round 5 is the Final Duel
- N-round config: Round N is the Final Duel

**Action**: After dispute discussion, if any decision points still have judges scoring below threshold, those unresolved points are redistributed to all committee members for a final round of discussion and re-scoring.

**Review Duration**: No more than 3 minutes per round. If not all sub-sessions are recovered after 3 minutes, the organizer terminates the process and returns results.

**Core Output**: If all decision points now achieve full pass, output the final report. If any remain unresolved, output the final report with each decision point's status tagged: ✅ Full Pass / 🟡 Pending User Decision / 🔴 Disputed.

---

### Round Extension (for non-default round settings)

| Extension Type | Description |
|:---|:---|
| Increase rounds (4 or more) | 2nd-to-last round follows "Dispute Discussion"; last round follows "Final Duel"; middle rounds loop dispute discussion |
| Decrease rounds (2 rounds) | Round 1 follows "Independent Evaluation"; Round 2 directly outputs the final report (treated as final round) |

---

## Final Output: 6-Section Consensus Report

The decision output is a standardized report containing:

1. **Voting Record** — Quantitative scoring matrix (by decision point)
2. **Summary** — Each committee member's core arguments (with model name noted)
3. **Execution Plan** — Conclusion version + detailed version
4. **Decision Point Status** — Each decision point's pass status
5. **Conclusion Summary** — One-sentence verdict + confidence level
6. **Risk Advisory** — Key risks and mitigation recommendations

**Decision Point Status Tags**:
| Status | Meaning | Tag |
|:---|:---|:---|
| Full Pass | All judges scored ≥ threshold on this point | ✅ Green — Passed |
| Pending Decision | All judges chose same option but some scores below threshold | 🟡 Yellow — Pending User Confirmation |
| Disputed | Judges chose different options | 🔴 Red — Disputed, reason noted |

---
*Version: V1.6.7*
*Developer: Zeekr0808*
*Email: Zeekr0808@outlook.com*

---

# 多模型决策委员会 — 操作与使用指南

## 版本变更记录

| 版本 | 日期 | 更新内容 |
|:---|:---|:---|
| V1.0.0 | 2026-04-19 | 初始版本，包含核心框架、3轮收敛机制、6段式报告 |
| V1.1.0 | 2026-04-24 | **新增英文操作文档**（与中文合并，英文在上）；经多模型委员会翻译质量审核通过（均分81/100） |
| V1.1.3 | 2026-04-24 | SKILL.md和references/转为纯中文（精简）；docs/保留双语完整文档（面向全球用户） |
| V1.2.0 | 2026-04-25 | 恢复为公共ClawHub版本（曾为本地定制版）；同步所有文件 |
| V1.2.1 | 2026-04-25 | **关键修复**：删除SKILL.md中硬编码的模型列表（A1/A2/A4...）；改为执行时动态扫描通过`openclaw models list`获取实时模型列表；示例中的模型引用改为通用占位符`[模型A/B/C]` |
| V1.2.2 | 2026-04-25 | 同步：v1.2.1热修复后全文件同步到GitHub和ClawHub |
| V1.2.3 | 2026-04-25 | **用户体验修复**：明确首次使用流程：自动扫描模型 → 默认前3个 → 提示用户确认或修改评委后再开始决策 |
| V1.2.4 | 2026-04-25 | **关键修复**：OUTPUT_TEMPLATE.md - 删除所有3轮prompt模板中的「匿名委员」，改为「{模型名称}（实名委员）」格式 |
| V1.2.5 | 2026-04-25 | **强制判定机制**：SKILL.md - 新增「强制判定规则」章节，明确 Round 1/2 后的阈值判定和收敛判定为不可跳过步骤；禁止行为新增跳项判定禁止规则 |
| V1.2.6 | 2026-04-25 | **实名显性化**：评委以标准大模型名称显名，透明可溯源；三层架构（组织者/评委/子Agent）；100分制评分；第0轮准备阶段 |
| V1.5.0 | 2026-04-25 | 同步所有文档版本号至V1.5.0；英文内容全量对齐中文 |
| V1.5.1 | 2026-04-26 | 新增「每轮开始前通知用户」规则；新增「收敛分差阈值」可配置参数；新增「异常处理规则」章节 |
| V1.5.2 | 2026-04-26 | 新增「判定方式」可配置参数，明确全票通过制为默认判定规则 |
| **V1.6.0** | **2026-04-27** | **重大修复**：重写子Agent结果回收机制，新增运行时环境适配矩阵；新增Push-based等待流程；新增运行时自检；简化状态管理；新增TROUBLESHOOTING.md |
| **V1.6.1** | **2026-04-27** | **判定规则澄清**：区分「通过」「收敛」「一致性选择」三个独立概念；澄清收敛讨论范围；「第3轮」更名为「最后一轮」；新增最终轮「一致性选择」机制 |
| **V1.6.2** | **2026-04-27** | **核心逻辑重构**：取消「收敛」概念，引入「决策点」级别评审；通过判定改为全员通过/非全员通过；「收敛讨论」改为「分歧讨论」；最终报告新增决策点通过状态标注（✅绿色/🟡黄色/🔴红色） |
| **V1.6.5** | **2026-04-30** | **安全加固**：移除 allowed-tools 中未使用的 Exec；最大并发子Agent从13降至6；新增 Write 工具路径限制（仅限 memory 目录）；TROUBLESHOOTING.md 新增模型路由偏差提前终止规则 |
| **V1.6.6** | **2026-04-30** | **安全修复**：将`openclaw.json`文件扫描改为`openclaw models list`命令，避免暴露 provider token；修正委员会规模描述从3-13为3-6个模型；SKILL.md 新增 Read/Write 工具路径白名单声明 |
| **V1.6.7** | **2026-04-30** | **可审计性修复**：明确工具使用分工——组织者使用 Read/Write，评委通过 task 参数接收内容且不得调用任何工具；删除"仅供内部"标记；消除 OUTPUT_TEMPLATE.md 中评委 spawn 的歧义表述 |

---

## 插件定位

**多模型决策委员会** 是专为 OpenClaw 设计的"数字智库"。它支持调动多个不同架构的大模型（如 GPT、Gemini、豆包等）同时对同一任务进行协同思考、对抗辩论与共识合成，有效消除单模型偏见，综合性给出最优建议。

## 核心优势

- **去中心化决策**：交叉验证不同模型逻辑，确保方案的严谨性。
- **对抗性评审**：通过模型间的互评，快速锁定潜在的逻辑漏洞。
- **弹性扩容**：根据任务难度，随时增加或减少"决策委员"的数量。
- **消除偏见**：多模型独立评审，避免单一AI的认知盲区。
- **量化决策**：6维度评分 + 加权矩阵，结论有据可查。
- **透明可信**：实名委员制、模型身份透明。
- **灵活配置**：参数可调，如决策成员人数、决策轮次、通过阈值等，均可可自定义。

---

## 核心治理原则：身份纯净

为了确保结果的绝对客观，本插件强制执行 **"身份纯净原则"**：
- **角色透明化**：决策委员会成员均会注明其身份（大模型名称），保持可视化透明。
- **严禁设定角色**：禁止给委员设定诸如"架构师"、"审计员"等身份标签。
- **严禁引导提示**：任务下发时不得针对评审委员设置诱导性提示词或诱导性身份角色，防止产生的偏见。
- **严禁子Agent委托**：评委严禁spawn任何子Agent，只能独立思考和输出结论；禁止二次委托，所有子任务由组织者统一分发和回收，确保链路完全可控。
- **评审不重复原则**：若组织者（即当前使用模型）是评审委员会成员，则组织者提交内容即视同为其在本轮的评审结果，无需重复自评。若组织者不是评审委员会成员，则仅负责组织实施和汇总评委意见，不参与评审。

---

## 使用方法
-  **启动**：在OpenClaw中，输入指令"启动多模型决策委员会"、"审议这个方案"、"对这个方案进行决策"、"启动决策"即可启动多模型决策委员会。首次使用时会提醒用户进入配置模式，并选择模型组合。
- **配置**：根据需要，可配置参数，如：轮数、阈值、委员数量、委员模型等。

### 参数配置
配置参数可采用指令方式，如："修改配置"、"调整参数"、"增加委员"、"确认配置"。
| 指令关键词 | 可调参数 | 说明 |
|:---|:---|:---|
| "换模型" | 委员模型组合 | 从用户本地接入的模型列表中选择模型组合加入 |
| "改轮数" | 决策轮数 | 默认3轮，日常事务可设为2轮，重大决策可设3-6轮 |
| "改阈值" | 判定阈值 | **通过阈值**：默认≥90%；**待决策阈值**：默认[72%, 90%)；**否定阈值**：默认<72% |
| "增加委员" / "减少委员" | 委员数量 | 支持2-6个模型同时评审 |
| "确认配置" | 确认当前配置 | 确认当前参数后开始决策 |

## 参数建议
- **模型选择**：建议至少包含 1 个具备强逻辑推理能力的模型和 1 个具备强中文语境理解能力的模型。
- **轮次建议**：日常事务建议 2 轮；涉及架构、资金、核心规则的决策，建议 3-5 轮。
- **阈值设定**：
  - **严谨型**：≥95%（全票通过）
  - **效率型**：≥75%（多数通过）

---

## 决策流程（3轮决策机制）
多模型决策委员会采用 3 轮决策机制，基于决策点级别评审，每轮进行100分制评分，最终给出决策结果。具体流程如下：

---

### 第 0 轮：准备与框架确认 (Preparation & Framework Confirmation)
**决策准备**：组织者（当前使用模型）接收到决策任务后，将用户背景、需求、待审方案汇总，判断评审方案类型，发起决策申请。内容格式为：
- **项目名称**：{项目名称}
- **项目背景**：{项目背景}
- **项目需求**：{项目需求}
- **待审方案**：{待审方案}
- **评审方案类型**：{单方案评审 / 二选一评审 / 决策点拆分评审}
- **决策点拆分及权重**（仅决策点拆分评审时填写）：
  - 决策点1（{维度名称}）：{权重}%
  - 决策点2（{维度名称}）：{权重}%
  - ……
- **决策成员**：{决策成员：调取已配置的模型组合}
- **决策轮次**：{决策轮次：调取已配置的轮数}
- **阈值设置**：{阈值设置：调取已配置的阈值}
- **提交决策**：{用户确认评审类型及配置后开始决策}

**评审方案类型**（由组织者根据方案复杂程度判断）：
- **单方案评审**：简单/日常方案，评委直接对整体方案打分（0-100分制）
- **二选一评审**：提供方案A和方案B两套完整方案，评委先选择其中一个方案（落选方案直接PASS），再对选中方案的每个决策点逐项打分（0-100分制），加权平均计算总分
- **决策点拆分评审**：复杂/多维度方案，组织者将方案拆解为若干「决策点」，每个决策点对应一个具体评审维度。评委对每个决策点逐项打分（0-100分制）。整体方案得分为各决策点评分的加权平均值，由组织者自动计算，不再由评委单独打分

---

### 第 1 轮：独立评估 (Blind Evaluation)

**动作说明**：组织者接收到决策确认后，将准备流程相关内容分发至各选定模型的独立子会话中。每位委员在**完全无法感知他方意见**的情况下进行背对背评审。

**评审维度**：方案逻辑合理性、完整性、潜在风险分析、实施资源消耗预估、可行性评审、优化建议，并按照100分值进行评分。

**评审时长**：不超过3分钟/轮。若3分钟仍未回收所有子会话，组织者将结束流程并返回结果。

**核心产出**：组织者汇总各委员的初评报告及投票结果及打分结果，以及分歧意见或争议点。

---

### 第 2 轮：分歧讨论 (Dispute Discussion)

**动作说明**：组织者将第1轮中标记为「未通过」的决策点整理为「未通过决策点清单」，仅将这些未通过项下发给所有委员，要求评委**只针对这些未通过决策点**进行讨论并重新评分。已通过的决策点不再讨论。

**评审时长**：不超过3分钟/轮。若3分钟仍未回收所有子会话，组织者将结束流程并返回结果。

**核心产出**：汇总本轮重新评分结果，若所有决策点全员通过则直接输出最终报告；若仍有未通过项则进入下一轮。

---

### 最后一轮：最终辩论 (Final Duel)

**特殊说明**：无论配置多少轮，最终辩论始终是**最后一轮**。
- 3轮配置：第3轮为最终辩论
- 5轮配置：第5轮为最终辩论
- N轮配置：第N轮为最终辩论

**动作说明**：经过分歧讨论后，仍有决策点未通过时启用。组织者将仍未通过的决策点再次下发给所有委员，要求评委进行最后一轮讨论和重新评分。

**评审时长**：不超过3分钟/轮。若3分钟仍未回收所有子会话，组织者将结束流程并返回结果。

**核心产出**：若所有决策点全员通过，输出最终报告；若仍有未通过项，将未通过项标注状态后输出最终报告。

---

### 轮次扩展说明

| 扩展类型 | 说明 |
|:---|:---|
| 增加轮次（4轮及以上） | 倒数第2轮参照「分歧讨论」；最后一轮参照「最终辩论」；中间轮次循环分歧讨论 |
| 减少轮次（2轮） | 第1轮参照"独立评估"，第2轮直接输出最终报告 |

---

## 最终输出：6段式共识报告

决策完成后，输出标准化报告，包含：

1. **投票记录** — 量化评分矩阵（含决策点级别评分）
2. **汇总说明** — 各委员核心论点（注明大模型）
3. **执行方案** — 结论版 + 说明版
4. **决策点通过清单** — 各决策点通过状态
5. **结论摘要** — 一句话裁定 + 置信度
6. **风险提示** — 主要风险与缓解建议

**决策点通过状态标注**：

| 状态 | 含义 | 标注 |
|:---|:---|:---|
| 全员通过 | 所有评委在该决策点评分均≥阈值 | ✅ 绿色 — 通过 |
| 待决策 | 推荐顺序一致但有评委评分低于阈值 | 🟡 黄色 — 待用户确认 |
| 有分歧 | 推荐顺序不一致 | 🔴 红色 — 有分歧，附原因 |

---
*版本: V1.6.7*
*开发者: Zeekr0808*
*邮箱: Zeekr0808@outlook.com*
