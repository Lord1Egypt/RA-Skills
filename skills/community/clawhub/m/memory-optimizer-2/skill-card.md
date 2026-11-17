## Description:

Analyzes AI agent memory files to detect duplicates, stale information, missing indexes, and structure issues, generating detailed reports and auto-fix options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lokix94](https://clawhub.ai/user/lokix94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to audit AI agent memory and instruction files, then generate reports or apply cleanup actions for duplicate, stale, or poorly structured entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apply mode can rewrite persistent agent memory and instruction files with limited safeguards.

Mitigation: Run dry-run first, inspect proposed changes, create backups, and use --apply only in trusted workspaces.

Risk: Running apply mode in repositories with symlinks or untrusted AGENTS.md/TOOLS.md content can affect files that influence future agent behavior.

Mitigation: Avoid apply mode on untrusted workspaces and review target paths and file contents before allowing rewrites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lokix94/skills/memory-optimizer-2)
- [Server-resolved GitHub source](https://github.com/lokix94/peru-hub/tree/main/skills/memory-optimizer)
- [Publisher profile](https://clawhub.ai/user/lokix94)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON summaries, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run output is available by default; apply mode can modify memory and agent instruction markdown files.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
