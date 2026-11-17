# PMCF 计划完整性检查器 / PMCF Plan Completeness Checker

![license](https://img.shields.io/badge/license-MIT-blue) ![python](https://img.shields.io/badge/python-3.8%2B-green) ![deps](https://img.shields.io/badge/deps-zero-orange) ![LGD](https://img.shields.io/badge/LGD--Powered-三律-teal)

> `pmcf-plan-check` v1.0.0 · Zero-dependency · Deterministic output (JSON IR) · Receipt-style errors

**交公告机构之前，先用十条核心要素把 PMCF 计划过一遍秤。**

**EN**: Weigh your PMCF plan against ten core elements before the notified body does.

**关键词 / Keywords**: PMCF计划 MDCG 2020-7 MDCG 2019-8 上市后临床随访 CER 公告机构 补件

## Install & Try / 安装即试
```bash
mkdir -p ~/.claude/skills/pmcf-plan-check/scripts
curl -fsSL https://raw.githubusercontent.com/zhaoxinghua09-cell/agent-skills/main/skills/pmcf-plan-check/scripts/pmcf_plan_check.py -o ~/.claude/skills/pmcf-plan-check/scripts/pmcf_plan_check.py
python ~/.claude/skills/pmcf-plan-check/scripts/pmcf_plan_check.py --help
```
其他 Agent：`~/.config/opencode/skills/`、`~/.agents/skills/` 等同结构放置；cross-platform 对话内直接装。

## Usage / 用法
```bash
# 按字段逐项检查
python scripts/pmcf_plan_check.py --fields objectives=随访生存率变化 methods=文献+登记库 endpoints=并发症发生率 follow_up_period=24个月 statistical_plan=单臂目标值法 benefit_risk_linkage=是 pms_linkage=是 cer_update_trigger=年度 responsible_person=RA经理 timeline=2026Q4启动

# 或用 JSON 计划文件
python scripts/pmcf_plan_check.py --plan pmcf.json --json
```

## Sample output / 真机输出
```
$ pmcf_plan_check.py --plan pmcf.json
完整性 8/10（80%）
  缺失：statistical_plan（统计考量）
  存疑：follow_up_period 未含具体时长
建议补齐后重跑至 10/10 再提交公告机构。
```

## Exit codes & error receipts / 退出码与修复回执
- rc=0 ok / rc=1 findings / rc=2 usage
| 错误码 | 含义 | 建议修复 |
|---|---|---|
| PMCF_E_MISSING_FIELD | 核心要素缺失 | 按 README 要素表补齐对应字段 |
| PMCF_E_WEAK_FIELD | 字段有值但内容存疑（如随访期无数值） | 补充可核验的量化内容 |
| PMCF_E_NO_INPUT | 未提供 --plan 或 --fields | 任选其一提供计划内容 |

## FAQ
**检查通过等于公告机构认可吗？**

不等于。本工具核对的是 MDCG 2020-7/2019-8 提炼的核心要素完整性，公告机构还会审查方法学合理性。

**NMPA 侧能用吗？**

PMCF 概念源自 EU MDR；NMPA 上市后临床随访要求参照国内指导原则执行，本工具输出对两侧均为要素清单参考。


## Links / 快链
- 仓库: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/pmcf-plan-check
- 家族门户: https://zhaoxinghua09-cell.github.io/lgd-hub/
- Issues: https://github.com/zhaoxinghua09-cell/agent-skills/issues

## Disclaimer / 免责
pmcf-plan-check 输出为确定性格式/结构判定与规则化建议，不构成法规意见、安全承诺或专业咨询；关键决策请人工复核并以官方最新要求为准。

License MIT © pmcf-plan-check authors. LGD-Powered badge: [定版真源](https://SynomosAI.cn/badge/powered/svg/lgd-powered-en.svg?v=84)

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


