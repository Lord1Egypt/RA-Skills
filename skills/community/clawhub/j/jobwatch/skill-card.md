## Description:

JobWatch helps OpenClaw users monitor configured career pages, judge postings against a personal job-search profile, send match alerts and digests, archive postings, track application status, and answer questions about watched jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywc668](https://clawhub.ai/user/ywc668)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to run an opt-in job-search monitor for their own configured companies, personal criteria, alerts, digests, archives, and application tracking. Developers can configure local or third-party services for scraping, LLM judging, notifications, and knowledge-base storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitoring can run persistently and continue scraping, judging, and notifying after setup.

Mitigation: Enable scheduled runs only after explicit consent and know how to remove the jobwatch-* cron entries before live monitoring.

Risk: The skill handles sensitive job-search profile data and can process untrusted job-posting text through scraping, LLM, notification, and knowledge-base services.

Mitigation: Prefer default local modes, approve only the egress destinations needed, review RSS URLs for trusted public hosts, and use dedicated revocable API keys.

Risk: Host credential reuse increases impact if enabled unnecessarily.

Mitigation: Avoid JOBWATCH_ALLOW_HOST_CREDS unless needed; when used, grant only the specific credential scope required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ywc668/skills/jobwatch)
- [Publisher profile](https://clawhub.ai/user/ywc668)
- [Project homepage](https://github.com/ywc668/jobwatcher)
- [Chinese reference](references/SKILL.zh.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON records, shell commands, alerts, digests, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local jobwatch profile, state, queue, run, archive, and knowledge-base files; optional integrations can send job URLs, job descriptions, profile text, notifications, and archived documents after consent.]

## Skill Version(s):

1.2.3 (source: server release metadata, frontmatter, and changelog released 2026-07-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
