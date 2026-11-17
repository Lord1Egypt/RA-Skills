# label-compliance-checker · 医疗器械标签合规核对器

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

## English

### What it does
Checks medical-device **label/IFU mandatory elements** per official rules: **Regulations on Medical Device Instructions and Labels (Order No. 6), articles 10–11** (clause numbers pending manual verification; official texts prevail).

- **Insufficient input → strict presumption**: omitted `has_*` fields are **treated as missing** and stated in `warnings` (`rc=1`) — never silently counted as complete. Values other than yes/no → `rc=2`.
- **Out of scope**: consistency of label content with the registration certificate / technical requirements, UDI applicability, implant-specific items.

### Install & run (zero-dependency, Python 3.8+)
```bash
python label-compliance-checker.py --has_name yes --has_reg_no yes --has_manufacturer yes --has_indications yes --has_warnings yes --has_lot yes --has_udi yes   # all present → rc=0
python label-compliance-checker.py --has_name yes --has_reg_no no    # missing element → rc=1
python label-compliance-checker.py --has_name banana                 # invalid value → rc=2
python label-compliance-checker.py --demo                            # 3 built-in smoke cases
```
Params: `has_name / has_reg_no / has_manufacturer / has_indications / has_warnings / has_lot / has_udi` (yes/no; none given → `rc=2`).

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `compliant`, `missing_fields`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

### Compliance & IP
- LGD-Powered badge · theory TH-MED-004 · ambassador 诺康 (MED-domain lead voice)
- Decision support only; human review required.
- **Layered licence**: code `label-compliance-checker.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

### Family set
| Stage | Tool | Ambassador |
|---|---|---|
| Non-clinical research | non-clinical-checker | 诺康 |
| Post-market adverse events | pms-vigilance-intake | 诺康 |
| Recall | recall-decision-checker | 诺康 |
| Labelling | label-compliance-checker | 诺康 |
| Import/export | import-export-router | 诺衡 |

## 中文

### 它做什么
依据官方规则核对医疗器械**标签/说明书法定要素**：**《医疗器械说明书和标签管理规定》（总局令 第6号）第10-11条**（条款号待人工核对；以官方文本为准）。

- **输入不足 → 从严推定**：缺省的 `has_*` 字段按**缺失**处理并在 `warnings` 中说明（`rc=1`）——绝不静默算齐；非 yes/no 取值 → `rc=2`。
- **不做什么**：标签内容与注册证/技术要求的一致性、UDI 适用性、植入物专项要素。

### 安装与运行（零依赖，Python 3.8+）
```bash
python label-compliance-checker.py --has_name yes --has_reg_no yes --has_manufacturer yes --has_indications yes --has_warnings yes --has_lot yes --has_udi yes   # 全有 → rc=0
python label-compliance-checker.py --has_name yes --has_reg_no no    # 缺要素 → rc=1
python label-compliance-checker.py --has_name banana                 # 非法值 → rc=2
python label-compliance-checker.py --demo                            # 3 个内置冒烟用例
```
参数：`has_name / has_reg_no / has_manufacturer / has_indications / has_warnings / has_lot / has_udi`（yes/no；全不给 → `rc=2`）。

### 输出
确定性 JSON IR，含 `rc`（**0**=ok / **1**=完成有告警 / **2**=输入不全或非法）、`compliant`、`missing_fields`、`warnings` 与 `aigc_mark`（GB 45438-2025 元数据；`is_generated: true`，标注依据待核对）。

### 条款号待人工核对清单
| 条款 | 用途 | 状态 |
|---|---|---|
| 说明书和标签管理规定 第6号 第10条 | 标签法定要素 | 待人工核对 |
| 说明书和标签管理规定 第6号 第11条 | 说明书法定要素 | 待人工核对 |

### 合规与署名
- LGD-Powered 徽章 · 理论 TH-MED-004 · 大使 诺康（MED 域首席发声人）
- 本工具为决策支持，须人工复核。
- **分层许可**：代码 `label-compliance-checker.py` = MIT；本 `README.md` / `SKILL.md` 及一切理论文本**不在 MIT 覆盖范围内**（保留所有权利）。

### 家族合集
| 环节 | 工具 | 大使 |
|---|---|---|
| 非临床研究 | non-clinical-checker | 诺康 |
| 上市后不良事件 | pms-vigilance-intake | 诺康 |
| 召回 | recall-decision-checker | 诺康 |
| 标签 | label-compliance-checker | 诺康 |
| 进出口 | import-export-router | 诺衡 |

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
