## Description:

A Chinese-language agent skill for bulk job-application workflows across multiple recruiting platforms, including application tracking, analytics, AI matching, and team coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, job-service teams, HR staff, and high-volume job seekers use this skill to configure and run bulk applications, track statuses, analyze outcomes, and manage candidate profiles across recruiting platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk automation can submit real job applications at scale without adequate candidate review or consent.

Mitigation: Require explicit candidate consent, dry-run review, rate limits, and per-application approval before any submission.

Risk: Credential and platform API usage can expose job-board tokens, email credentials, or AI API keys.

Mitigation: Store credentials only in a secrets manager or environment variables, scope permissions tightly, and keep secrets out of configs, logs, and generated reports.

Risk: Tracking, scheduling, and local API service modes can run automated actions without enough supervision.

Mitigation: Disable unattended schedules until reviewed, bind APIs to authenticated local-only access, and log all automated actions for audit.

Risk: Account rotation or anti-detection behavior can violate platform rules or trigger account enforcement.

Mitigation: Disable account rotation and verify each platform's permissions and terms before using automation.

Risk: The package describes Python execution but does not include the implementation scripts it references.

Mitigation: Inspect and approve any referenced scripts before execution, and block runs when script targets are missing or unverified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/job-auto-apply-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe generated reports, logs, tracking files, and application configuration for agent execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
