## Description:

Personal CRM built on monday.com that tracks contacts, last interactions, next meetings, and topics, syncs daily from Calendar and email, and prepares pre-meeting briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and individual operators use this skill to maintain a monday.com personal CRM from calendar and email activity, answer contact-history questions, add new contacts, and prepare meeting briefings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring access to calendar, email, CRM data, and local credentials may expose sensitive personal and business information.

Mitigation: Use dedicated least-privilege Google and monday.com access, store private values outside the skill text, and review permissions before installing.

Risk: The artifact includes a pattern for sourcing an executable context file, which can run unexpected shell content if the file is modified.

Mitigation: Replace sourced context files with private configuration that is parsed as data, or inspect and restrict the file before use.

Risk: Automated WhatsApp briefings and daily cron tasks can send sensitive or unwanted messages and keep running after installation.

Mitigation: Require confirmation before outbound WhatsApp messages and document how to inspect, modify, and remove the daily cron task.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/netanel-abergel/skills/heleni-personal-crm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose CRM updates, contact summaries, pre-meeting briefing text, cron setup commands, and WhatsApp briefing content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
