---
name: little-steve-agent-guard
version: 0.1.4
description: Little Steve Agent Guard: a self-evolving security system for agent skills. Wraps all skill commands with risk assessment, audit logging, approval levels, and continuous rule evolution. / 小史安全卫士：面向 Agent Skill 的自进化安全系统。为所有技能命令提供风险评估、审计日志、分级审批和持续规则进化。
homepage: https://github.com/EchoOfZion/little-steve-agent-guard
requires:
  bins:
    - jq
---

# Little Steve Agent Guard

A self-evolving security system for agent skills. Wraps all skill command execution with risk assessment, audit logging, tiered approval, and continuous rule learning.

## Dependencies

- **jq** (required) — install via `brew install jq` or `apt install jq`

## Filesystem Scope

This is a **cross-skill security guard**. By design, it needs read access to other skills' directories to:
- `guard-exec.sh`: read target scripts for static risk analysis before execution
- `capability-diff.sh`: compare a skill's SKILL.md declarations against its actual scripts

The guard does **not** write to other skills' directories. All writes (audit logs, rules) stay within its own `reports/` and `rules/` directories.

## Bypass & Emergency Procedures

The runbook (`docs/runbook.md`) documents emergency bypass procedures (circuit-break, manual script execution, log reset). These are **human-operator-only** actions for when the guard itself malfunctions. The agent must never execute bypass procedures autonomously.

## CRITICAL: Execution Rule

**ALL skill script executions MUST go through guard-exec.sh.** Never call skill scripts directly. Always use:

```bash
bash {baseDir}/scripts/guard-exec.sh exec <script-path> [args...]
```

Example:

```bash
bash {baseDir}/scripts/guard-exec.sh exec {workspaceDir}/skills/<other-skill>/scripts/<script>.sh <command> [args...]
```

## Approval Levels

- **L1 (low/medium risk)**: Auto-execute, audit logged
- **L2 (dry-run)**: Preview without executing
- **L3 (high risk)**: Block and prompt user — output warning, wait for user to reply "确认" or "confirm"
- **BLOCK (critical)**: Reject entirely, no execution possible

When guard-exec.sh returns exit code 10 (prompt), present the warning to the user and wait for confirmation. On "确认"/"confirm", re-run with `confirm` instead of `exec`.

## Agent Command Conventions

1. Execute a skill command (with guard)
```bash
bash {baseDir}/scripts/guard-exec.sh exec <script> [args...]
```

2. Confirm a prompted action (after user approval)
```bash
bash {baseDir}/scripts/guard-exec.sh confirm <script> [args...]
```

3. Preview without executing
```bash
bash {baseDir}/scripts/guard-exec.sh dry-run <script> [args...]
```

4. Quick risk check
```bash
bash {baseDir}/scripts/guard-exec.sh check <script> [args...]
```

5. Run capability consistency check on a skill
```bash
bash {baseDir}/scripts/capability-diff.sh check --skill-dir <skill-path>
```

6. View audit stats
```bash
bash {baseDir}/scripts/audit.sh stats
```

7. Generate weekly security report
```bash
bash {baseDir}/scripts/weekly-report.sh generate [days]
```

8. Manage rules
```bash
bash {baseDir}/scripts/promote-rule.sh list
bash {baseDir}/scripts/promote-rule.sh add --rule <name> --pattern <regex> --level <low|medium|high|critical>
bash {baseDir}/scripts/promote-rule.sh promote --rule <name>
bash {baseDir}/scripts/promote-rule.sh demote --rule <name>
```

9. Test candidate rules against history
```bash
bash {baseDir}/scripts/replay-verify.sh test --rule <name>
bash {baseDir}/scripts/replay-verify.sh test-all
```

## Five Core Security Policies (Immutable)

1. **Least Privilege** — scripts only access their own data directory
2. **Credential Protection** — no secrets in args, output, or logs
3. **Capability Consistency** — runtime must match SKILL.md declarations
4. **Outbound Control** — no undeclared network access
5. **High-Risk Confirmation** — destructive/critical actions need human approval

## Risk Classification

| Level | Examples |
|-------|---------|
| low | read-only: list, view, status check |
| medium | single-item mutation: add, update status |
| high | delete, bulk mutation, file write outside data/ |
| critical | network access, secret exposure, system commands |

## Data Files

- `reports/audit-events.jsonl` — audit log (auto-created)
- `reports/failure-dataset.json` — failure samples for evolution
- `rules/active/*.rule` — active custom rules
- `rules/candidates/*.rule` — candidate rules pending promotion

---

# 小史安全卫士

面向 Agent Skill 的自进化安全系统。为所有技能命令提供风险评估、审计日志、分级审批和持续规则进化。

## 依赖

- **jq**（必须）— 通过 `brew install jq` 或 `apt install jq` 安装

## 文件系统范围

这是一个**跨技能安全卫士**。按设计，它需要读取其他技能目录的权限：
- `guard-exec.sh`：执行前读取目标脚本做静态风险分析
- `capability-diff.sh`：对比技能的 SKILL.md 声明与实际脚本行为

卫士**不会**写入其他技能的目录。所有写入（审计日志、规则）都在自身的 `reports/` 和 `rules/` 目录内。

## 绕过与紧急操作

运行手册（`docs/runbook.md`）记录了紧急绕过操作（熔断、直接执行脚本、日志重置）。这些是**仅限人工操作员**的紧急措施，用于卫士本身出故障的情况。Agent 绝对不可以自主执行绕过操作。

## 关键规则：执行约束

**所有技能脚本执行必须通过 guard-exec.sh。** 不要直接调用技能脚本，始终使用：

```bash
bash {baseDir}/scripts/guard-exec.sh exec <脚本路径> [参数...]
```

## 审批分级

- **L1（低/中风险）**：自动执行，记录审计日志
- **L2（预览）**：只预览不执行
- **L3（高风险）**：阻断并提示用户——显示警告，等待用户回复"确认"
- **阻断（严重）**：直接拒绝，无法执行

当 guard-exec.sh 返回退出码 10（提示）时，向用户展示警告并等待确认。用户回复"确认"后，用 `confirm` 替代 `exec` 重新执行。

## Agent 执行约定

1. 执行技能命令（带防护）
```bash
bash {baseDir}/scripts/guard-exec.sh exec <脚本> [参数...]
```

2. 确认被提示的操作（用户批准后）
```bash
bash {baseDir}/scripts/guard-exec.sh confirm <脚本> [参数...]
```

3. 预览不执行
```bash
bash {baseDir}/scripts/guard-exec.sh dry-run <脚本> [参数...]
```

4. 快速风险检查
```bash
bash {baseDir}/scripts/guard-exec.sh check <脚本> [参数...]
```

5. 对技能做声明-行为一致性检查
```bash
bash {baseDir}/scripts/capability-diff.sh check --skill-dir <技能路径>
```

6. 查看审计统计
```bash
bash {baseDir}/scripts/audit.sh stats
```

7. 生成周报
```bash
bash {baseDir}/scripts/weekly-report.sh generate [天数]
```

8. 管理规则
```bash
bash {baseDir}/scripts/promote-rule.sh list
bash {baseDir}/scripts/promote-rule.sh add --rule <名称> --pattern <正则> --level <low|medium|high|critical>
bash {baseDir}/scripts/promote-rule.sh promote --rule <名称>
bash {baseDir}/scripts/promote-rule.sh demote --rule <名称>
```

9. 测试候选规则
```bash
bash {baseDir}/scripts/replay-verify.sh test --rule <名称>
bash {baseDir}/scripts/replay-verify.sh test-all
```

## 五条核心安全策略（不可变）

1. **最小权限** — 脚本只能访问自身数据目录
2. **凭证保护** — 参数、输出、日志中不得出现密钥
3. **能力一致性** — 运行时行为必须与 SKILL.md 声明一致
4. **外发控制** — 不得有未声明的网络访问
5. **高风险确认** — 破坏性/严重操作需人工审批

## 风险分级

| 级别 | 示例 |
|------|------|
| low | 只读操作：列表、查看、状态检查 |
| medium | 单项变更：新增、更新状态 |
| high | 删除、批量变更、数据目录外写文件 |
| critical | 网络访问、密钥暴露、系统命令 |

## 数据文件

- `reports/audit-events.jsonl` — 审计日志（自动创建）
- `reports/failure-dataset.json` — 失败样本（用于进化）
- `rules/active/*.rule` — 活跃自定义规则
- `rules/candidates/*.rule` — 候选规则（待晋升）
