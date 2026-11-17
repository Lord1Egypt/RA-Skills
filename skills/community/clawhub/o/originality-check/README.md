# originality-check · 赛事作品原创性查重器 / Contest Originality Checker

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with the organizing committee. Text verified: 2026-09-26.

### What it does
Checks **submission originality** by fingerprint comparison against a known-hashes corpus, per **UIBC originality rules + academic-misconduct definitions** (rule source pending manual verification; the latest UIBC charter prevails).

- **Insufficient input → strict presumption**: an empty/missing `known_hashes` corpus makes any "no duplicate" verdict **unreliable** — the tool states this in `warnings` (`rc=1`) instead of silently passing the work off as original. Malformed `known_hashes` JSON → `rc=2`.
- Similarity is a simple algorithm (prefix comparison); real screening needs MinHash/SimHash + human review (noted in output `notes`).

### Install & run (zero-dependency, Python 3.8+)
```bash
python originality-check.py --submission_hash sha256:new999 --known_hashes '["sha256:aaa111","sha256:bbb222"]'   # clean w/ corpus → rc=0
python originality-check.py --submission_hash sha256:aaa111 --known_hashes '["sha256:aaa111"]'                   # duplicate hit → rc=1
python originality-check.py --submission_hash sha256:new999                                                      # empty corpus → strict warning, rc=1
python originality-check.py --submission_hash sha256:x --known_hashes '{bad'                                     # invalid JSON → rc=2
python originality-check.py --demo                                                                               # 3 built-in smoke cases
```
Params: `submission_hash` (required) / `known_hashes` (JSON string list).

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `similarity`, `is_duplicate`, `exact_match`, `matches`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

Real excerpt (`--demo`, case 3, verbatim warnings):
```json
{
  "input": {"submission_hash": "sha256:new999"},
  "result": {
    "similarity": 0.0, "is_duplicate": false, "exact_match": false, "matches": [],
    "warnings": ["known_hashes 为空（未提供对照指纹库）：本输出「无重复」不可靠，请提供历史/公开库指纹后复核；不静默按原创通过处理。"]
  },
  "rc": 1
}
```

### Rule-source checklist pending manual verification
| Rule / value | Use | Status |
|---|---|---|
| UIBC originality rules | Duplicate-detection rule source | Pending |
| Similarity threshold 0.85 | Duplicate-detection breakpoint | Pending |

### Compliance & IP
- LGD-Powered badge · theory TH-EVT-005 · ambassador Nuoyuan @ DAT-domain chief voice
- This tool is decision support; human review is required.
- **Layered licence**: code `originality-check.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

### Family set
| Contest stage | Tool | Ambassador |
|---|---|---|
| Registration / submission portal | contest-submission-portal | Nuosheng |
| Problem generation | problem-set-generator | Nuosheng |
| Judging rubric scoring | judging-rubric-grader | Nvlv |
| Anti-cheat / identity verification | anti-cheat-identity | Nuowei |
| Submission plagiarism check | originality-check | Nuoyuan |

## 中文

> AI 辅助决策支持 CLI，服务 UIBC 赛事运营。**非最终裁决**——须以组委会复核为准。文本核验日期：2026-09-26。

### 它做什么
按 **UIBC 原创性规范 + 学术不端界定**（规则源待人工核对；以最新 UIBC 章程为准），用指纹比对方式核查**作品原创性**。

- **输入不足→从严推定**：`known_hashes` 指纹库为空/缺失时，任何「无重复」结论都**不可靠**——工具在 `warnings` 中声明（`rc=1`），而不静默按原创通过。`known_hashes` JSON 畸形 → `rc=2`。
- 相似度为简单算法（前缀比对）；真正筛选需 MinHash/SimHash + 人工评审（输出 `notes` 已注明）。

### 安装与运行（零依赖，Python 3.8+）
```bash
python originality-check.py --submission_hash sha256:new999 --known_hashes '["sha256:aaa111","sha256:bbb222"]'   # 库内干净 → rc=0
python originality-check.py --submission_hash sha256:aaa111 --known_hashes '["sha256:aaa111"]'                   # 命中重复 → rc=1
python originality-check.py --submission_hash sha256:new999                                                      # 空库 → 从严告警，rc=1
python originality-check.py --submission_hash sha256:x --known_hashes '{bad'                                     # 非法 JSON → rc=2
python originality-check.py --demo                                                                               # 3 个内置冒烟案例
```
参数：`submission_hash`（必填）/ `known_hashes`（JSON 字符串列表）。

### 输出
确定性 JSON IR，含 `rc`（**0**=正常 / **1**=带告警完成 / **2**=输入不足或非法）、`similarity`、`is_duplicate`、`exact_match`、`matches`、`warnings` 与 `aigc_mark`（GB 45438-2025 元数据；`is_generated: true`，标注依据待核）。

### 规则源待人工核对清单
| 规则 / 数值 | 用途 | 状态 |
|---|---|---|
| UIBC 原创性规范 | 重复判定规则来源 | 待人工核对 |
| 相似度阈值 0.85 | 重复判定断点 | 待人工核对 |

### 合规与知识产权
- LGD-Powered 徽章 · 理论 TH-EVT-005 · 大使诺源 @ DAT 域首席发声人
- 本工具为决策支持，须人工复核。
- **分层许可**：代码 `originality-check.py` = MIT；本 `README.md` / `SKILL.md` 及一切理论文本**不在 MIT 覆盖范围**（保留所有权利）。

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
© 2026 SynomosAI. All rights reserved.
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
