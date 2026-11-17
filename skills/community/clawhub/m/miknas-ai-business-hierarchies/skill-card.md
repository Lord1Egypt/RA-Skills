## Description:

Build and operate autonomous AI businesses using hierarchical agent systems with folder-based company structures, daily tracking, auto-optimization, and self-healing capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miknasbh-stack](https://clawhub.ai/user/miknasbh-stack)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to plan and operate AI-managed business structures with CEO, manager, supervisor, and worker agents. It provides templates, shell setup flows, and reporting automation for department-based business operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation can run business-agent reporting on a schedule and may continue after the user has forgotten it is installed.

Mitigation: Inspect generated cron entries before installation, run with a low-privilege account, and periodically review or remove scheduled jobs that are no longer needed.

Risk: Generated daily reports may store sensitive agent conversation history or business data.

Mitigation: Store reports in access-controlled locations, avoid capturing secrets or regulated data, and review report contents before sharing.

Risk: The skill encourages agents to perform outreach, financial, HR, payroll, and operational tasks that can affect real people or live business systems.

Mitigation: Require explicit human approval and audit logs before agents send outreach, change finances, handle HR or payroll, or modify production systems.

Risk: Weak business-name validation may allow unsafe paths or confusing cron entries.

Mitigation: Restrict business names to simple letters, numbers, and hyphens before running setup scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/miknasbh-stack/skills/miknas-ai-business-hierarchies)
- [README](artifact/README.md)
- [Strategic Layer Template](artifact/assets/business-template.md)
- [Business Setup Script](artifact/scripts/setup-business.sh)
- [Daily Reporting Setup Script](artifact/scripts/setup-daily-reporting.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, generated folder structures, cron configuration, and business strategy templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local business directories, strategy files, reporting scripts, and scheduled cron entries when users run the provided scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
