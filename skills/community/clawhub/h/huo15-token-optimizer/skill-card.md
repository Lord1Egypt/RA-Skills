## Description:

辉火 Token 优化器 — 在不降低 OpenClaw 性能的前提下，系统化扫描、清理、监控工作区 token 消耗。安全模式：默认 dry-run，备份先行，AGENTS 永不自动替换。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to scan workspace memory and instruction files, preview token cleanup actions, generate token reports, monitor size thresholds, and restore files from backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify persistent OpenClaw workspace memory files, including DREAMS.md, after confirmation.

Mitigation: Review dry-run output before execution, keep an independent backup, and use forced cleanup only after confirming the proposed file changes.

Risk: Custom workspace or restore paths can increase the chance of unintended file changes.

Mitigation: Avoid custom --workspace and --restore paths unless they have been manually checked against the intended OpenClaw workspace.

Risk: Replacing AGENTS.md could alter user-specific instructions or rules.

Mitigation: Keep auto_replace_agents false and review AGENTS.md changes manually; the artifact states AGENTS.md is never automatically replaced by default.

## Reference(s):

- [Token Best Practices](references/token-best-practices.md)
- [OpenClaw Configuration Guide](references/openclaw-config-guide.md)
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- [DeepSeek Context Caching](https://api-docs.deepseek.com/guides/context_caching)
- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with inline shell commands and script-generated JSON or Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleanup defaults to dry-run and requires explicit force execution; restore uses dated backups.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
