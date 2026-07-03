## Description: <br>
Huo15 Token Optimizer scans, reports, monitors, and can clean OpenClaw workspace token usage with dry-run previews and backup-first file changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw workspace context files, estimate token usage, generate token reports, monitor oversized workspace files, and preview cleanup actions before modifying files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forced cleanup can truncate DREAMS.md files in OpenClaw workspaces. <br>
Mitigation: Run scan and clean --dry-run first, inspect the preview, and use --force only after confirming the proposed truncation and backup location. <br>
Risk: The artifact contains an AGENTS.md replacement path guarded by auto_replace_agents, while the public safety text says AGENTS.md is never automatically replaced. <br>
Mitigation: Keep auto_replace_agents set to false, review config changes before use, and manually inspect any AGENTS.md action before accepting cleanup. <br>
Risk: Backups are written under ~/.openclaw/.token-opt-backups and restoration depends on date-based backup folders. <br>
Mitigation: Confirm the backup directory exists after cleanup and retain the backup date needed for clean.py --restore. <br>


## Reference(s): <br>
- [Token Best Practices](references/token-best-practices.md) <br>
- [OpenClaw Configuration Guide](references/openclaw-config-guide.md) <br>
- [Anthropic Prompt Caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) <br>
- [DeepSeek Context Caching](https://api-docs.deepseek.com/guides/context_caching) <br>
- [OpenClaw Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON scan output, and Markdown reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cleanup defaults to dry-run unless --force is supplied; reports and monitoring alerts are generated from local OpenClaw workspace files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
