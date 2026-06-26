# Little Steve Agent Guard

Your agent runs skills. Skills run scripts. Scripts do things to your files. Who's watching?

Agent Guard sits between the agent and every skill it runs. Every command passes through a risk assessment, gets an audit trail, and follows approval rules — automatically. No secrets leak, no undeclared behavior, no silent failures.

It's not paranoia. It's engineering.

## How It Works

```
User → Agent → guard-exec.sh → [risk check] → skill script
                    ↓
              audit-events.jsonl
```

Every execution is classified (low → medium → high → critical), logged, and gated:
- **Low/Medium**: auto-execute, logged
- **High**: block and ask you first
- **Critical**: reject outright

## Key Components

| Script | Purpose |
|--------|---------|
| `guard-exec.sh` | Wrapper — all skill commands go through here |
| `audit.sh` | Structured audit logging |
| `capability-diff.sh` | Check SKILL.md vs actual script behavior |
| `weekly-report.sh` | Automated security report |
| `promote-rule.sh` | Manage custom detection rules |
| `replay-verify.sh` | Test rules against historical data |

## Self-Evolution

Agent Guard learns from its own history:
1. **Observe** — collect failure and false-positive samples
2. **Propose** — generate candidate detection rules
3. **Verify** — replay against history before promoting
4. **Promote** — only rules with proven benefit go live

## Dependency

- `jq`

## Quick Start

```bash
# Execute a skill command through guard
bash scripts/guard-exec.sh exec /path/to/skill/scripts/script.sh add --title "test"

# Check risk without executing
bash scripts/guard-exec.sh check /path/to/script.sh delete --id 1

# View audit stats
bash scripts/audit.sh stats

# Generate weekly report
bash scripts/weekly-report.sh generate

# Run capability consistency check
bash scripts/capability-diff.sh check --skill-dir /path/to/skill
```

---

# 小史安全卫士

你的 agent 运行技能，技能运行脚本，脚本操作你的文件。谁在看着？

安全卫士坐在 agent 和每个技能之间。每条命令都经过风险评估、留下审计记录、遵循审批规则——全自动。没有密钥泄露，没有未声明行为，没有静默失败。

这不是多疑，这是工程。

## 工作原理

```
用户 → Agent → guard-exec.sh → [风险检查] → 技能脚本
                    ↓
              audit-events.jsonl
```

每次执行都会被分级（low → medium → high → critical）、记录、拦截：
- **低/中风险**：自动执行，记录日志
- **高风险**：阻断，先问你
- **严重**：直接拒绝

## 核心组件

| 脚本 | 用途 |
|------|------|
| `guard-exec.sh` | 包装器——所有技能命令通过这里执行 |
| `audit.sh` | 结构化审计日志 |
| `capability-diff.sh` | 检查 SKILL.md 与脚本实际行为的一致性 |
| `weekly-report.sh` | 自动安全周报 |
| `promote-rule.sh` | 管理自定义检测规则 |
| `replay-verify.sh` | 用历史数据测试规则 |

## 自进化

安全卫士从自身历史中学习：
1. **观察** — 收集失败和误拦截样本
2. **提议** — 生成候选检测规则
3. **验证** — 晋升前用历史回放测试
4. **晋升** — 只有经过验证的规则才上线

## 依赖

- `jq`

## 快速开始

```bash
# 通过 guard 执行技能命令
bash scripts/guard-exec.sh exec /path/to/skill/scripts/script.sh add --title "test"

# 检查风险不执行
bash scripts/guard-exec.sh check /path/to/script.sh delete --id 1

# 查看审计统计
bash scripts/audit.sh stats

# 生成周报
bash scripts/weekly-report.sh generate

# 一致性检查
bash scripts/capability-diff.sh check --skill-dir /path/to/skill
```
