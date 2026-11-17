# 金融AI合规守门 / Finance AI Compliance Guard

The first cross-domain landing piece of the LGD three laws — translating "registered · evidenced · gated" into the compliance language of the "financial / licensed-institution AI (advisory · risk control · AML)" domain.

## English

### Pain point
Financial AI is heavily regulated: missing model identity, data lineage or compliance sign-off is a violation — yet no tool maps "registered · evidenced · gated" onto the financial context.

### Quick start
```bash
python fin_guard.py --rubric
python fin_guard.py --system "your system description"
python fin_guard.py --answers '{...}' --json
```

### How the three laws map in this domain
- Registered → identity / version / source / responsible-party registration (this domain's terminology)
- Evidenced → six evidence artifact types (this domain's evidence types)
- Gated → trigger / review / release / retro four gates (this domain's thresholds)

### Positioning
This skill is the **first-claim definition piece** of the "凡自治之物" standard in the financial / licensed-institution AI domain — others can copy the features, but not the definition power of the standard.

![LGD-Powered](lgd-powered.png)

© XLGD · SynomosAI

## 中文

LGD 三律跨域首占件 · 把"有籍·有证·有门禁"翻译进「金融 / 持牌机构 AI 应用（投顾·风控·反洗钱）」本域合规语言。

### 痛点
金融AI监管严，模型身份/数据血缘/合规签发缺失即违规；市面无把"有籍·有证·有门禁"映射到金融语境的工具。

### 快速开始
```bash
python fin_guard.py --rubric
python fin_guard.py --system "你的系统描述"
python fin_guard.py --answers '{...}' --json
```

### 三律本域映射
- 有籍 → 身份/版本/来源/责任主体登记（本域术语）
- 有证 → 六类证据工件（本域证据类型）
- 有门禁 → 触发/评审/放行/复盘四道门禁（本域阈值）

### 定位
本技能是"凡自治之物"标准在金融 / 持牌机构 AI 应用（投顾·风控·反洗钱）域的**首占定义件**——别人可抄功能，抄不走标准定义权。

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
