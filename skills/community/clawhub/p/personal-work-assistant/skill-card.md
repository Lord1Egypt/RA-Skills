## Description:

Personal Work Assistant aggregates in-progress Teambition tasks and DingTalk group, mention, all-hands, and direct-message activity, tracks unresolved items in a persistent task ledger, and produces a concise daily action report delivered to DingTalk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zpeng6834-arch](https://clawhub.ai/user/zpeng6834-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual workplace users use this skill to consolidate task and message streams into a daily action report, with unresolved items carried forward until closed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes live-looking credentials and user identifiers.

Mitigation: Remove and rotate shipped credentials before installation, and replace config.yaml with placeholders or user-provided secrets.

Risk: The skill collects sensitive workplace chats, direct messages, and task data.

Mitigation: Require explicit user and organizational approval, scope monitored conversations narrowly, and redact sensitive content where possible.

Risk: Raw DingTalk content may be sent to an undeclared third-party AI endpoint.

Mitigation: Approve the LLM provider and endpoint before use, or replace it with an approved provider that satisfies the organization's data-handling requirements.

Risk: Scheduled automation and the SQLite ledger may continue collecting or retaining data after setup.

Mitigation: Document how to remove the cron job, disable direct-message collection, and purge the local task ledger.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zpeng6834-arch/skills/personal-work-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown daily report with setup guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single daily report stream; scheduled DingTalk delivery is configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
