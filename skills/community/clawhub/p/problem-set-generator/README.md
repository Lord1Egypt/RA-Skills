# problem-set-generator · 赛事赛题生成器 / Contest Problem-Set Generator

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

> AI-assisted decision-support CLI for UIBC contest operations. NOT final adjudication — verify with the organizing committee. Text verified: 2026-09-26.

### What it does
Generates **structured problem-set drafts** (background / task / constraints / deliverables / scoring) per **UIBC problem rules + season theme "Migration decisions and accountability"** (rule source pending manual verification; the latest UIBC charter prevails). Every problem is marked `review_status: pending` — committee review is required before publishing.

- **Strict on bad input**: invalid `difficulty` (not easy/mid/hard) or invalid/out-of-range `count` → `rc=2` — no silent fallback to mid/3. Custom (non-season) theme → adaptation warning, `rc=1` — never silently passed as season-compliant.
- **Honest boundary**: drafts are 3-scenario templates differentiated by difficulty-requirement sections; the committee must refine/dedupe before publishing (noted in output `notes`).

### Install & run (zero-dependency, Python 3.8+)
```bash
python problem-set-generator.py --difficulty hard --count 1                    # season theme → rc=0
python problem-set-generator.py --theme 跨境数据判定 --difficulty easy --count 1   # custom theme → warning, rc=1
python problem-set-generator.py --difficulty banana                            # invalid → rc=2
python problem-set-generator.py --count 11                                     # out of range → rc=2
python problem-set-generator.py --demo                                         # 3 built-in smoke cases
```
Params: `theme` (default = current season theme) / `difficulty` (easy/mid/hard) / `count` (1-10).

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = invalid input), `problems[]` (each with `spec`, `review_status`, `ai_note`), `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, draft text is AI-generated).

Real excerpt (`--demo`, case 3; `spec` folded; other values verbatim):
```json
{
  "input": {"theme": "跨境数据判定", "difficulty": "easy", "count": "1"},
  "result": {
    "problems": [{"index": 1, "difficulty": "入门", "review_status": "待审（组委会人工审核后方可发布）"}],
    "warnings": ["自定义主题「跨境数据判定」非当前赛季主题「迁移的判定与问责」：是否采用须组委会确认赛题适配性。"]
  },
  "rc": 1
}
```

### Rule-source checklist pending manual verification
| Rule | Use | Status |
|---|---|---|
| UIBC problem rules | Problem structure & difficulty tiers | Pending |
| Season theme "迁移的判定与问责" | Default theme & custom-theme warning basis | Pending |

### Compliance & IP
- LGD-Powered badge · theory TH-EVT-002 · ambassador Nuosheng @ contest chief voice
- This tool is decision support; human review is required.
- **Layered licence**: code `problem-set-generator.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

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
按 **UIBC 赛题规范 + 赛季主题「迁移的判定与问责」**（规则源待人工核对；以最新 UIBC 章程为准）生成**结构化赛题草稿**（背景/任务/约束/交付物/评分）。每题标记 `review_status: 待审`——发布前须组委会审核。

- **坏输入从严**：`difficulty` 非法（非 easy/mid/hard）或 `count` 越界 → `rc=2`——不静默回落到 mid/3。自定义（非赛季）主题 → 适配告警 `rc=1`——绝不静默当作赛季合规通过。
- **边界诚实**：草稿为 3 场景模板、按难度-要求段区分；发布前组委会须精修/去重（输出 `notes` 已注明）。

### 安装与运行（零依赖，Python 3.8+）
```bash
python problem-set-generator.py --difficulty hard --count 1                    # 赛季主题 → rc=0
python problem-set-generator.py --theme 跨境数据判定 --difficulty easy --count 1   # 自定义主题 → 告警，rc=1
python problem-set-generator.py --difficulty banana                            # 非法 → rc=2
python problem-set-generator.py --count 11                                     # 越界 → rc=2
python problem-set-generator.py --demo                                         # 3 个内置冒烟案例
```
参数：`theme`（默认=当前赛季主题）/ `difficulty`（easy/mid/hard）/ `count`（1-10）。

### 输出
确定性 JSON IR，含 `rc`（**0**=正常 / **1**=带告警完成 / **2**=输入非法）、`problems[]`（每条含 `spec`、`review_status`、`ai_note`）、`warnings` 与 `aigc_mark`（GB 45438-2025 元数据；`is_generated: true`，草稿文本为 AI 生成）。

### 规则源待人工核对清单
| 规则 | 用途 | 状态 |
|---|---|---|
| UIBC 赛题规范 | 赛题结构与难度分级 | 待人工核对 |
| 赛季主题「迁移的判定与问责」 | 默认主题与自定义主题告警依据 | 待人工核对 |

### 合规与知识产权
- LGD-Powered 徽章 · 理论 TH-EVT-002 · 大使诺声 @ 赛事首席发声人
- 本工具为决策支持，须人工复核。
- **分层许可**：代码 `problem-set-generator.py` = MIT；本 `README.md` / `SKILL.md` 及一切理论文本**不在 MIT 覆盖范围**（保留所有权利）。

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
