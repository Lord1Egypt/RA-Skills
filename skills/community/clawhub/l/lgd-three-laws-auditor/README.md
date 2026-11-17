# LGD 三律合规自检器（凡自治之物）· lgd-three-laws-auditor

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> LGD (Lifecycle Governance Doctrine) — proposed by SynomosAI, empirically validated across the regulated-industry full lifecycle.
> **Everything autonomous: registered, evidenced, gated.** This tool is the "definer" of that governance idea — turning the three laws into a self-assessable standard rubric.

## English

### The three-laws standard (as defined by this tool)
| Law | Checklist items |
|---|---|
| **LGD-I REGISTERED** | identity registration · version registration · lineage registration · responsibility registration |
| **LGD-II EVIDENCED** | six artifact types: identity / data / verification / behavior-boundary / change / issuance |
| **LGD-III GATED** | trigger gate · review gate · release gate · retro gate |

### Usage
```bash
python scripts/lgd_audit.py --rubric                       # full standard (usable as external governance doc)
python scripts/lgd_audit.py --system "system description"  # heuristic self-assessment (pending confirmation, no fabrication)
python scripts/lgd_audit.py --answers answers.json --json  # formal scorecard
```
Answer format: `{"LGD-I REGISTERED": {"identity":"yes","version":"partial",...}}`, status in `yes|partial|no|unknown`.

### Competitive advantage
Market governance tools are all point guardrails with **no unified "autonomous entity" judging standard**. This tool is the carrier of the standard — whoever self-assesses in the three-laws vocabulary adopts our governance definition power.

© XLGD · SynomosAI Governance Line · MIT · LGD-Powered

## 中文

> LGD 全程治理论 · 由 SynomosAI 提出，并在受监管行业全生命周期治理实践中完成实证。
> **凡自治之物：有籍、有证、有门禁。** 本工具是这套治理思想的「定义器」——把三律做成可自评的标准 rubric。

### 三律标准（本工具定义）

| 律 | 检查项 |
|---|---|
| **LGD-I 有籍 REGISTERED** | 身份登记 · 版本登记 · 血缘登记 · 责任登记 |
| **LGD-II 有证 EVIDENCED** | 身份/数据/验证/行为边界/变更/签发 六类证据工件 |
| **LGD-III 有门禁 GATED** | 触发门禁 · 评审门禁 · 放行门禁 · 复盘门禁 |

### 用法

```bash
python scripts/lgd_audit.py --rubric                       # 看完整标准（可作对外治理文档）
python scripts/lgd_audit.py --system "系统描述"            # 启发式自评（标待确认，不编造）
python scripts/lgd_audit.py --answers 答卷.json --json     # 正式评分卡
```

答卷格式：`{"LGD-I 有籍 REGISTERED": {"身份登记":"yes","版本登记":"partial",...}}`，状态取 `yes|partial|no|unknown`。

### 竞争优势说明

市场治理工具全是单点护栏，**无统一"自治物"评判标准**。本工具即标准载体——谁用三律词汇自评，谁就采用了我们的治理定义权。

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
