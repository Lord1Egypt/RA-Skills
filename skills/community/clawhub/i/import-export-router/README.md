# import-export-router · 医疗器械进出口路径判定器

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> AI-assisted decision-support CLI. NOT legal advice — verify against official texts. Text verified: 2026-09-26.

## English

### What it does
Routes medical-device **import/export compliance paths** per official rules: **NMPA imported-device registration rules + export sales certificate issuance + FDA / EU MDR** (rule sources pending manual verification; official texts prevail).

- **Insufficient input → strict presumption**: missing `is_registered` is treated as **not registered** (stricter path + `warnings`, `rc=1`) — never silently the lenient registered path.
- **Out of scope**: device classification (I/II/III), registration-testing details, destination-country document lists and timelines.

### Install & run (zero-dependency, Python 3.8+)
```bash
python import-export-router.py --direction import --is_registered yes   # complete args → rc=0
python import-export-router.py --direction export --is_registered no    # strict warning → rc=1
python import-export-router.py --direction banana                       # invalid input → rc=2
python import-export-router.py --demo                                   # 4 built-in smoke cases
```
Params: `direction` (import/export, required) / `is_registered` (yes/no) / `dest_region` (cn/us/eu/other).

### Output
Deterministic JSON IR with `rc` (**0** = ok / **1** = completed with warnings / **2** = insufficient or invalid input), `route`, `required_docs`, `warnings`, and `aigc_mark` (GB 45438-2025 metadata; `is_generated: true`, label basis noted as pending verification).

### Compliance & IP
- LGD-Powered badge · theory TH-MED-005 · ambassador 诺衡 (MED-domain lead voice)
- Decision support only; human review required.
- **Layered licence**: code `import-export-router.py` = MIT; this `README.md` / `SKILL.md` and all theory text are **not covered by MIT** (all rights reserved).

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
依据官方规则路由医疗器械**进出口合规路径**：**NMPA 进口医疗器械注册规定 + 出口销售证明办理 + FDA / EU MDR**（规则源待人工核对；以官方文本为准）。

- **输入不足 → 从严推定**：缺 `is_registered` 按**未注册**处理（更严路径 + `warnings`，`rc=1`）——绝不静默走宽松的已注册路径。
- **不做什么**：产品分类（I/II/III 类）、注册检测细节、目的国材料清单与时限。

### 安装与运行（零依赖，Python 3.8+）
```bash
python import-export-router.py --direction import --is_registered yes   # 参数齐 → rc=0
python import-export-router.py --direction export --is_registered no    # 从严告警 → rc=1
python import-export-router.py --direction banana                         # 非法输入 → rc=2
python import-export-router.py --demo                                     # 4 个内置冒烟用例
```
参数：`direction`（import/export，必填）/ `is_registered`（yes/no）/ `dest_region`（cn/us/eu/other）。

### 输出
确定性 JSON IR，含 `rc`（**0**=ok / **1**=完成有告警 / **2**=输入不全或非法）、`route`、`required_docs`、`warnings` 与 `aigc_mark`（GB 45438-2025 元数据；`is_generated: true`，标注依据待核对）。

### 条款号待人工核对清单
| 条款 / 规则 | 用途 | 状态 |
|---|---|---|
| NMPA 进口医疗器械注册规定 | 进口路径判定 | 待人工核对 |
| 《医疗器械出口销售证明》办理规定 | 出口路径判定 | 待人工核对 |
| FDA 510(k)/PMA | 出口美国准入 | 待人工核对 |
| EU MDR | 出口欧盟准入 | 待人工核对 |

### 合规与署名
- LGD-Powered 徽章 · 理论 TH-MED-005 · 大使 诺衡（MED 域首席发声人）
- 本工具为决策支持，须人工复核。
- **分层许可**：代码 `import-export-router.py` = MIT；本 `README.md` / `SKILL.md` 及一切理论文本**不在 MIT 覆盖范围内**（保留所有权利）。

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
