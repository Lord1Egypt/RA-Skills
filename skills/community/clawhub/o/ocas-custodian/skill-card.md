## Description:

Custodian monitors OpenClaw gateway logs, cron jobs, skill journals, and OCAS data directories, then classifies failures, applies bounded non-destructive repairs, initializes missing skill state, and escalates unresolved issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indigokarasu](https://clawhub.ai/user/indigokarasu)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and maintainers use Custodian to run automated health checks, review log and cron failures, initialize missing skill state, and handle bounded repair or escalation during quiet hours.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests persistent background maintenance authority and can modify scheduler state, initialize skill storage, and apply repair commands.

Mitigation: Require explicit opt-in for background tasks, review cron and heartbeat registrations, and scope write access to intended OpenClaw paths.

Risk: Automatic self-update behavior can change the skill after installation.

Mitigation: Disable self-updates or require approval for each update, and review the release before enabling the updated skill.

Risk: Cross-skill reads and web-search queries may expose operational context.

Mitigation: Restrict cross-skill access to required files and sanitize or approve external search queries before execution.

Risk: Repair commands that include placeholders or paths could affect unintended files if parameters are unchecked.

Mitigation: Validate placeholders and resolved paths before execution, and permit only non-destructive, reversible actions from the known-issues registry.

## Reference(s):

- [Known Issues Registry](references/known_issues.json)
- [Custodian Escalated Issue Repair Plan](references/plans/custodian-repair.plan.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-style status or record descriptions with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scan reports, SkillStatus JSON, issues and fixes JSONL records, repair plans, and proposed shell or configuration changes.]

## Skill Version(s):

1.0.0 (source: skill.json, README changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
