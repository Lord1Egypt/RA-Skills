# LGD 三律闭环认证（有籍→有证→有门禁）· lgd-certify

> LGD 旗舰执行器。市场**唯一**把「有籍护照签发 → 有证证据链 → 有门禁签发 → 可挂载徽章」做成闭环的 CLI。

## 三命令闭环

```bash
python scripts/lgd_certify.py init --dir ./my-ai                 # 建 evidence/ 六类骨架
python scripts/lgd_certify.py register --dir ./my-ai --name "客服助手" --id "did:web:medxpert/ka" --issuer MedXpert
python scripts/lgd_certify.py evidence --dir ./my-ai             # 放六类工件后重跑→链式哈希
python scripts/lgd_certify.py gate --dir ./my-ai                # 三律评审 PASS→certification.json + BADGES.md
```

- `register` 有籍：算法护照（三锚一票同源）+ SHA-256 指纹
- `evidence` 有证：六类证据工件（身份/数据/验证/行为边界/变更/签发）链式哈希
- `gate` 有门禁：评审 PASS/FAIL，签发认证 + medxpert.cn 三律徽章嵌入码

## 护城河

闭环链路 + 可挂载视觉徽章（medxpert.cn/badge 已上线）。"凡用 LGD 工具即有徽章"。

© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237) · 保留所有权利（All rights reserved） · LGD-Powered

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
