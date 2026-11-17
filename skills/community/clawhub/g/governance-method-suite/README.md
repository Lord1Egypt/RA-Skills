# LGD Governance Method Suite / LGD 治理方法论合集

## English

One playbook for the full AI-agent governance loop. It orchestrates 9 independently published sub-skills by slug — it does **not** vendor their internals.

**Flow:** red-team drill → injection shield → leak scan → desensitization → kill-switch → badge issue/verify → skill gate → publish gate.

### Sub-skills (already published, independent)
| Stage | Slug |
|-------|------|
| Red-team drill | `agent-redteam-kit` |
| Injection shield | `prompt-injection-shield` |
| Leak scan | `prompt-leak-scanner` |
| Desensitization | `doc-desens-scanner` |
| Kill switch | `agent-kill-switch` |
| Badge issue | `lgd-badge-issuer` |
| Badge verify | `lgd-badge-verify` |
| Skill quality gate | `skill-quality-gate` |
| Publish gate | `publish-quality-gate` |

### Run
```bash
python3 scripts/governance_flow.py --list
python3 scripts/governance_flow.py --route redteam
python3 scripts/governance_flow.py --route lgd-badge-verify
```

This package is pure documentation + a read-only router: no network, no business-data writes, no acting on your behalf.

## 中文

一套方法论跑通智能体治理全流程。按 slug 编排 9 个已独立发布的子技能，**不内嵌子包内部实现**。

**闭环：** 红队演练 → 注入防护 → 泄漏扫描 → 文档脱敏 → 停机开关 → 徽章签发/核验 → 技能质量门 → 发布门。

### 子技能（已独立发布）
| 环节 | slug |
|------|------|
| 红队演练 | `agent-redteam-kit` |
| 注入防护 | `prompt-injection-shield` |
| 泄漏扫描 | `prompt-leak-scanner` |
| 文档脱敏 | `doc-desens-scanner` |
| 停机开关 | `agent-kill-switch` |
| 徽章签发 | `lgd-badge-issuer` |
| 徽章核验 | `lgd-badge-verify` |
| 技能质量门 | `skill-quality-gate` |
| 发布门 | `publish-quality-gate` |

### 运行
```bash
python3 scripts/governance_flow.py --list
python3 scripts/governance_flow.py --route redteam
python3 scripts/governance_flow.py --route lgd-badge-verify
```

本包为纯文档 + 只读路由：无网络、不写业务数据、不代执行。
