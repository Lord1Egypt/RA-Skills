# Procurement Admission Qualification Checklist (Reference)

A generic, adaptable baseline for B2B supplier / vendor procurement admission. Replace or extend per industry (medical, construction, software, etc.). Severity rules follow the skill's P0/P1/P2 model.

## Mandatory documents (presence required; missing → P0)

| # | Document | Why it matters |
|---|---|---|
| 1 | 营业执照 (Business license) | Legal entity identity; anchors USCC and legal name |
| 2 | 统一社会信用代码 (USCC) | Unique legal identifier; must match the license |
| 3 | 法定代表人 / 授权代表证明 | Who may bind the supplier |
| 4 | 行业资质证书 (if applicable) | e.g. 建筑资质、医疗器械经营许可、ISP 牌照 |
| 5 | 开户许可 / 银行账户信息 | Payment routing for settled procurement |
| 6 | 近一年财报或税务摘要 | Financial viability signal |
| 7 | 合规 / 反腐败声明 | Anti-bribery, sanction-screening attestation |

## Recommended documents (missing → P2; weakness → P1)

- ISO 9001 / ISO 27001 / 行业特定体系认证
- 产品检测报告 / 第三方认证
- 典型客户案例（含可量化结果）
- 售后服务 / SLA 承诺
- 数据安全 / 隐私合规材料（如处理个人信息）

## Consistency dimensions

### Identity
Legal name and USCC must be identical across every submitted document. Divergence is a P0 — it can mean two different legal entities or a typo that breaks the contract later.

Check: 营业执照 vs 产品册 vs 案例 vs 合同抬头.

### Certificate validity
Each certificate has an issue and expiry date. Expired mandatory cert → P0; expiry within 90 days → P1 (warn the buyer before admission lapses mid-contract).

Check: name, issuer, expiry, mandatory flag.

### Financial consistency
Revenue / scale figures stated in the financials, tax summary, and case studies should reconcile within a tolerance band (~10%). Large divergence → P1 (reconcile, do not pick the nicer number).

### Scope match
Declared business scope (from the license) should cover the products / services being admitted. Mismatch → P1 (the supplier may not be legally permitted to deliver).

Check: 申报经营范围 vs 产品类目.

### Case-study quality
A case study should show a measurable outcome (volume, uptime, cost saved). Boilerplate ("we served many clients with excellent service") → P1 (weak evidence for admission).

## Severity rules

- **P0**: identity conflict; expired mandatory cert; missing mandatory document; missing USCC.
- **P1**: near-expiry cert; revenue inconsistency; weak case study; missing recommended qualification; scope mismatch.
- **P2**: cosmetic / formatting issues that do not affect admission readiness.
