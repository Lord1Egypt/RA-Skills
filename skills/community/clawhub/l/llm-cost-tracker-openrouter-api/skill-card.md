## Description:

Tracks OpenClaw LLM token usage and billed cost from OpenRouter and reports rolling and calendar-window spend with model breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeyiptk](https://clawhub.ai/user/joeyiptk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to collect local OpenClaw usage history and generate OpenRouter cost and token reports for daily or periodic spend monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pruning script's dry-run mode is reported to delete rows instead of only previewing them.

Mitigation: Do not use scripts/prune_usage.py --dry-run until fixed; back up config/usage.db and verify the cutoff before running any pruning command.

Risk: The skill reads OpenClaw session history and creates a local usage database.

Mitigation: Install only where local session-history access is acceptable, restrict the configured sessions directory, and protect the generated usage database.

Risk: Normal reports automatically handle OpenRouter API credentials for account-summary data.

Mitigation: Use an explicit least-privileged OpenRouter API key where possible and avoid running setup or tracker commands as root.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joeyiptk/skills/llm-cost-tracker-openrouter-api)
- [Setup Guide](artifact/SETUP_GUIDE.md)
- [Setup](artifact/SETUP.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text reports, with optional JSON output for scripting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cover 24h, 7d, 30d, 90d, and 365d windows with model-level cost and token breakdowns.]

## Skill Version(s):

1.1.2 (source: frontmatter, changelog, version.txt, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
