# judging-rubric-grader · 赛事评审打分器

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with the organizing committee. Text verified: 2026-09-26.

## English

### What it does
Grades submissions by **multi-dimension rubric weighting** per the **UIBC judging spec (weighted rubric)** (rule source pending manual verification; the latest UIBC charter prevails).

- **Insufficient input → strict presumption**: a dimension missing from `scores` is counted as **0** (lowering the total) and stated in `warnings` (`rc=1`) — never silently skipped or full-marked. A weight sum ≠ 1 also warns.
- **Out of scope**: judge deliberation, appeals, overall endorsement of submission safety/correctness.

### Install & run (zero-dependency, Python 3.8+)
```bash
python judging-rubric-grader.py --criteria '[{"dim":"innovation","weight":0.4},{"dim":"engineering","weight":0.3},{"dim":"presentation","weight":0.3}]' --scores '{"innovation":90,"engineering":85,"presentation":80}'   # complete → rc=0
python judging-rubric-grader.py --criteria '[{"dim":"innovation","weight":0.5},{"dim":"compliance","weight":0.5}]' --scores '{"innovation":90}'                                                   # missing dim → strict 0, rc=1
python judging-rubric-grader.py                                                                                                                                                  # missing args → rc=2
python judging-rubric-grader.py --demo                                                                                                                                           # 3 built-in smoke cases
```
Params: `criteria` (JSON dim/weight list, required) / `scores` (JSON dim→score object, required) / `pass_line` (default 60).

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `total`, `grade`, `per_dimension`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

### Rule-source review checklist (pending manual verification)
| Rule | Used for | Status |
|---|---|---|
| UIBC judging spec · rubric | weighted total & grade mapping | pending manual check |
| Grade breakpoints 90/80/70 / pass line | grade mapping values | pending manual check |

### Compliance & IP
- LGD-Powered badge · theory TH-EVT-003 · ambassador 诺律 (LAW-domain lead voice)
- Decision support only; human review required.
- **Layered licence**: code `judging-rubric-grader.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

### Family set
| Contest stage | Tool | Ambassador |
|---|---|---|
| Registration / submission portal | contest-submission-portal | 诺声 |
| Problem-set generation | problem-set-generator | 诺声 |
| Judging & scoring | judging-rubric-grader | 诺律 |
| Anti-cheat / identity check | anti-cheat-identity | 诺卫 |
| Plagiarism check | originality-check | 诺源 |

## 中文

### 它做什么
依据 **UIBC 评审规范（rubric 加权）**（规则源待人工核对；以最新 UIBC 章程为准）对参赛作品做**多维度加权打分**。

- **输入不足 → 从严推定**：`scores` 中缺的维度按 **0 分**计（拉低总分），并在 `warnings` 中说明（`rc=1`）——绝不静默跳过或给满分；权重之和 ≠ 1 也告警。
- **不做什么**：评委合议、申诉处理、对作品安全性/正确性的总体背书。

### 安装与运行（零依赖，Python 3.8+）
```bash
python judging-rubric-grader.py --criteria '[{"dim":"创新","weight":0.4},{"dim":"工程","weight":0.3},{"dim":"表达","weight":0.3}]' --scores '{"创新":90,"工程":85,"表达":80}'   # 参数齐 → rc=0
python judging-rubric-grader.py --criteria '[{"dim":"创新","weight":0.5},{"dim":"合规","weight":0.5}]' --scores '{"创新":90}'                                                   # 缺维度 → 从严 0 分，rc=1
python judging-rubric-grader.py                                                                                                                                                  # 缺参数 → rc=2
python judging-rubric-grader.py --demo                                                                                                                                           # 3 个内置冒烟用例
```
参数：`criteria`（JSON 维度/权重列表，必填）/ `scores`（JSON 维度→分数对象，必填）/ `pass_line`（默认 60）。

### 输出
确定性 JSON IR，含 `rc`（**0**=ok / **1**=完成有告警 / **2**=输入不全或非法）、`total`、`grade`、`per_dimension`、`warnings` 与 `aigc_mark`（GB 45438-2025 元数据；`is_generated: true`，标注依据待核对）。

### 规则源待人工核对清单
| 规则 | 用途 | 状态 |
|---|---|---|
| UIBC 评审规范·rubric | 加权总分与等级映射 | 待人工核对 |
| 等级断点 90/80/70/达标线 | 等级映射取值 | 待人工核对 |

### 合规与署名
- LGD-Powered 徽章 · 理论 TH-EVT-003 · 大使 诺律（LAW 域首席发声人）
- 本工具为决策支持，须人工复核。
- **分层许可**：代码 `judging-rubric-grader.py` = MIT；本 `README.md` / `SKILL.md` 及一切理论文本**不在 MIT 覆盖范围内**（保留所有权利）。

### 家族合集
| 赛事环节 | 工具 | 大使 |
|---|---|---|
| 报名/提交门户 | contest-submission-portal | 诺声 |
| 赛题生成 | problem-set-generator | 诺声 |
| 评审打分 | judging-rubric-grader | 诺律 |
| 反作弊/身份核验 | anti-cheat-identity | 诺卫 |
| 作品查重 | originality-check | 诺源 |

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
