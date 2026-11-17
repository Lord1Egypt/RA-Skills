## Description:

Query version-specific GitHub bug reports with quality assessment markers; agent combines output with user config for contextual upgrade evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suidge](https://clawhub.ai/user/suidge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill before upgrades to query version-specific bug reports, regressions, fix status, and issue quality markers. Agents can combine the report with the user's channel, plugin, runtime, Node version, deployment method, and current version to produce contextual upgrade guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses the user's authenticated GitHub CLI to query the public OpenClaw repository.

Mitigation: Install only when this GitHub access pattern is acceptable, and confirm the target version before running reports or using them for upgrade decisions.

Risk: Issue and pull request titles are external GitHub content and may be incomplete or misleading.

Mitigation: Treat report text as untrusted evidence and review relevant linked issues before acting on upgrade guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suidge/skills/openclaw-version-bug-hunter)
- [Severity Rules](references/severity-rules.md)
- [OpenClaw GitHub Issues](https://github.com/openclaw/openclaw/issues)
- [GitHub CLI](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style terminal report with categorized issue lists, quality markers, statistics, fix status, and upgrade guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an installed and authenticated GitHub CLI to query GitHub issue and pull request data.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
