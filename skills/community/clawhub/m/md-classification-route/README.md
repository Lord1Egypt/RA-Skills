# md-classification-route · 医疗器械分类与注册路径初判器 / MD Classification & Registration Route Screener

[![LGD](https://img.shields.io/badge/LGD-Governance-blue)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

Zero-dependency deterministic CLI screener for medical-device compliance.
**Decision support only — NOT legal/regulatory advice. Always verify against official texts.** Text verified: 2026-09-26.

### Why

Which class should a device be filed under, and which pathway should it take — get it wrong once and the entire dossier must be redone. Classification is the first domino of multi-market market access.

### What it does

Screens `md-classification-route` against public rule sources: **EU MDR (EU) 2017/745 Annex VIII / China Medical Device Classification Catalog / FDA 21 CFR 860**.
Outputs deterministic JSON IR with `rc` (0 = ok / 1 = ok with warnings / 2 = insufficient input),
`error_code`, and GB 45438-2025 AIGC metadata. No network, no API key, no third-party packages.

- **Insufficient input → strict presumption**: a software device without `--contact` → warning that MDR Rule 11 may push it to Class III; a long-term invasive device without `--implant` → warning that Rule 8 may place it in Class III (`rc=1`). It never silently returns the lenient class as final.
- Measured: `--market cn --invasive no --active yes` → rc=0; `--market eu --invasive yes --duration long_term --implant yes` → rc=1; `--market jp --active yes` → rc=2.

### Run it (Python 3.8+)

```bash
python md-classification-route.py --demo
python md-classification-route.py --json <your args...>
```

### Compliance & IP

- Author: SynomosAI contributors · © 2026 SynomosAI · MIT License
- Theory anchor: `TH-MED-006` (LGD · registry / evidence / gate)
- Published by an AI-assisted studio; the institution bears responsibility for the output.

---

## 中文

零依赖确定性 CLI 医疗器械合规初判器。
**仅作决策支持——不构成法律/法规建议。务必以官方文本复核。** 文本核验日期：2026-09-26。

### 为什么

器械该按几类报、走哪条路——判错一次，整套资料重做。分类是多市场准入的第一块多米诺骨牌。

### 它做什么

对照公开规则源筛查 `md-classification-route`：**EU MDR (EU) 2017/745 附件八 /《医疗器械分类目录》/ FDA 21 CFR 860**。
输出确定性 JSON IR，含 `rc`（0=正常 / 1=带告警正常 / 2=输入不足）、`error_code` 与 GB 45438-2025 AIGC 元数据。无网络、无 API key、无第三方依赖。

- **输入不足→从严推定**：软件器械未给 `--contact` → 告警 MDR Rule 11 可能将其推至 Class III；长期侵入器械未给 `--implant` → 告警 Rule 8 可能将其列入 Class III（`rc=1`）。绝不静默返回宽松类别作为最终结论。
- 实测：`--market cn --invasive no --active yes` → rc=0；`--market eu --invasive yes --duration long_term --implant yes` → rc=1；`--market jp --active yes` → rc=2。

### 运行（Python 3.8+）

```bash
python md-classification-route.py --demo
python md-classification-route.py --json <your args...>
```

### 合规与知识产权

- 作者：SynomosAI contributors · © 2026 SynomosAI · MIT 许可
- 理论锚点：`TH-MED-006`（LGD · 有籍 / 有证 / 有门禁）
- 由 AI 辅助工作室发布；机构对产出负责。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `md-classification-route.py` | **MIT** |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在代码许可覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依其自身许可使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 SynomosAI. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块：**A 段公共段逐字复制、未删改；B 段资产参数段按本包真值填写**；发布 / 重提前须照最新版本复核。）

## Family

| 环节 | 工具 | 位置 |
|---|---|---|
| 分类与路径 | `md-classification-route` | 本批 |
| 注册资料-技术文件 | `SynomosAI-reg-hub` | 存量枢纽 |
| 临床评价（选路） | `clin-eval-route-picker` | 存量 |
| 临床评价（证据要素） | `cer-equivalence-check` | 本批 |
| 检测项目与实验室匹配 | `test-lab-match-check` | 本批 |
| 申报前非临床研究 | `non-clinical-checker` | 存量 |
| UDI（格式校验） | `udi-format-validator` | 存量 |
| UDI（数据库提交） | `udi-db-submission-check` | 本批 |
| 上市后·PMCF 计划 | `pmcf-plan-check` | 存量 |
| 上市后·PMCF 评价报告 | `pmcf-evaluation-report-check` | 本批 |
| 上市后·不良事件 | `pms-vigilance-intake` | 存量 |
| 上市后·召回 | `recall-decision-checker` | 存量 |
| 标签与说明书 | `label-compliance-checker` | 存量 |
| 进出口路径 | `import-export-router` | 存量 |
