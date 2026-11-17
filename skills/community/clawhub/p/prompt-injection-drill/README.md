# 提示词注入演练器 / Prompt Injection Drill

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

Generate 8 categories of injection attack drills for your system prompt (role/instruction override, exfiltration, encoding bypass, tool abuse, forged authority, long-horizon, refusal bypass) + expected-behavior checklist for pre-launch red-teaming.

**Pain point**: Prompts ship untested: one 'ignore previous instructions' disarms them — broken not by experts but by random drive-by lines.

LGD-III 有门禁（上线前先挨一遍打） · TH-LGD-013

Part of the **LGD moat** (凡自治之物: registered / evidenced / gated).

Zero-dependency (stdlib only). See `scripts/` for CLI usage (`--help`).

© SynomosAI (LGD initiative) · LGD-Powered

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

