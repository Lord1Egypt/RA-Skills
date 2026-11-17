# LGD 徽章验真器 / LGD Badge Verifier

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Verify a badge certificate: recompute fingerprint (anti-tamper) + evidence-hash format + registry cross-check (serial exists & not revoked).

**Pain point**: issuance without verification is forgeable — the loop lacked reverse checking and the trust chain broke.

Part of the **LGD moat loop**: Passport (registered) → Evidence chain (evidenced) → Gate (gated) → **Badge (issued/verified)**.

Zero-dependency (stdlib only). See `scripts/` for CLI usage (`--help`).

© XLGD · SynomosAI Governance Line · LGD-Powered

## 中文

验徽章证书：指纹重算防篡改 + 证据哈希格式 + 台账对账（serial 存在且未吊销）。

**痛点**：只签发不验真即可被伪造——闭环缺了反向核查，信任链断裂。

属于 **LGD 闭环**：护照（有籍）→ 证据链（有证）→ 门禁（有门禁）→ **徽章（签发/核验）**。

零依赖（仅 stdlib）。CLI 用法见 `scripts/`（`--help`）。

---

© XLGD · SynomosAI Governance Line · LGD-Powered

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
