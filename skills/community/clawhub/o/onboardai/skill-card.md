## Description:

AI新员工入职引导系统，覆盖入职前准备清单、首日引导、首周看板、30-60-90天成长路线、问答助手和满意度追踪。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams, managers, buddies, and new hires use this skill to open a local onboarding dashboard for tracking preparation tasks, first-day guidance, week-one work, growth milestones, self-service questions, and onboarding feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles HR-style employee records and onboarding feedback in a browser dashboard.

Mitigation: Use placeholder or non-sensitive data until the organization has reviewed storage, export, and privacy controls for real HR records.

Risk: The dashboard includes credential-like sample content, including a WiFi password in the built-in question-answer data.

Mitigation: Replace sample credentials before use and avoid storing real shared secrets in the skill asset.

Risk: The release evidence flags unnecessary Bash and Write permissions for a local front-end dashboard.

Mitigation: Prefer a version that removes unused shell and write permissions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/onboardai)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance that directs the agent to open a local HTML dashboard; the dashboard can export JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The dashboard stores onboarding data in browser localStorage and includes sample HR records.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
