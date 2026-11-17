## Description:

Smart cost optimization skill for OpenClaw that helps reduce API costs through model routing, session management, output efficiency, free model usage, and bundled audit, monitoring, backup, health-check, and reporting scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rajdeep09-dev](https://clawhub.ai/user/rajdeep09-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to analyze agent API spending, choose lower-cost model routes, apply budget-oriented presets, and monitor cost trends while keeping user confirmation before configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled scripts may execute or process configuration files and can be unsafe with untrusted input.

Mitigation: Review scripts before installation, use a fixed release version, and run audit, report, and dashboard scripts only against trusted local configuration files.

Risk: API tokens, generated configuration, instance data, and webhook URLs may be exposed if handled carelessly.

Mitigation: Do not pass API keys on the command line, keep generated config and instance files private, and use only HTTPS webhook or provider endpoints that the user trusts.

Risk: Configuration patches or cron jobs can change agent behavior or create recurring automation.

Mitigation: Require explicit user confirmation before applying patches, installing cron jobs, or changing provider and model settings.

## Reference(s):

- [Model Tier Reference Card](artifact/references/model-tiers.md)
- [Configuration Templates](artifact/references/setup-config.md)
- [Cost Optimizer ClawHub Page](https://clawhub.ai/rajdeep09-dev/skills/open-optimise)
- [Publisher Profile](https://clawhub.ai/user/rajdeep09-dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration snippets, and generated reports or dashboards from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or generate configuration changes, backups, audit reports, monitoring output, webhook reports, and cost dashboard files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 7.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
