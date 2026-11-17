# 健康宣称合规扫描 / Health Claim Guard

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

> `health-claim-guard` v1.0.1 · LGD Moat Family · Zero-dependency · Domain: health

## English

Dropping "cures it" or "99% effective" into a sales copy casually — ad-law fines run into the hundreds of thousands. One command does the first pass: compliant PASS (rc=0) / violation FAIL (rc=1) / usage error (rc=2); `--json` supported.

### Usage
```bash
python scripts/health_claim_guard.py --help
```

### Disclaimer
Screening aid only, not legal / medical advice.

## 中文

带货文案随手写根治、有效率 99%，广告法罚款动辄数十万——一条命令完成初筛：合规 PASS（rc=0）/ 违规 FAIL（rc=1）/ 用法错误（rc=2），支持 `--json`。

### 用法
```bash
python scripts/health_claim_guard.py --help
```

### 免责
合规初筛辅助，不构成专业意见。

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
