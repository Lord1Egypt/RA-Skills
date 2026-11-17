## Description:

Health Mate is an executable OpenClaw health-report skill that reads Markdown health logs from an explicitly configured MEMORY_DIR and generates localized daily, weekly, and monthly reports with optional Tavily, webhook, public PDF, or font-download behavior only when configured.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate structured health-management summaries from local Markdown logs. It supports daily, weekly, and monthly localized reporting for wellness tracking, diet and hydration review, fitness habits, and configured chronic-condition monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell runners handle report and config text unsafely enough to require review before installation.

Mitigation: Review or avoid the shell runner scripts until heredoc handling and .env loading are fixed; prefer reviewed direct Python entry points where appropriate.

Risk: Health report data may leave the local machine when webhook, Telegram, Tavily, public PDF publishing, or runtime font download options are enabled.

Mitigation: Leave those credentials and publishing settings unset unless the data transfer is intended, and review generated reports before sharing links or notifications.

Risk: Project-local config/.env can contain secrets and sensitive local paths.

Mitigation: Keep config/.env owner-only, include only keys the skill should read, and re-check MEMORY_DIR, report preferences, webhook, Tavily, and publishing settings after upgrades or reinstalls.

## Reference(s):

- [Health Mate ClawHub listing](https://clawhub.ai/tankeito/skills/health-mate)
- [Health Mate project homepage](https://github.com/tankeito/Health-Mate)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Localized Markdown and text report content, generated PDF files, local logs, and configuration-guided command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces daily, weekly, and monthly health reports from local memory files; optional delivery, retrieval, public PDF publishing, and runtime font download depend on configured environment variables.]

## Skill Version(s):

1.5.4 (source: server release metadata, SKILL.md frontmatter, and changelog released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
