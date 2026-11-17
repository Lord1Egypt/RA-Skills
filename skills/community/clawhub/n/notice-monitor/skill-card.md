## Description:

Notice Monitor monitors configured website announcement pages, filters new notices by keywords and categories, deduplicates previously sent items, and sends scheduled notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryharbin](https://clawhub.ai/user/jerryharbin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and procurement teams use this skill to track government, procurement, bidding, and other announcement pages for configured keywords and receive concise notification reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill can run shell commands from scraped or configured text.

Mitigation: Review notification content and configuration before enabling the skill, and prefer a fixed version that removes shell-based message sending.

Risk: The security summary notes a default external DingTalk recipient in the artifact.

Mitigation: Replace all example notification targets with organization-approved recipients before running the skill.

Risk: The security guidance recommends using only trusted HTTPS URLs.

Mitigation: Configure monitoring tasks only for trusted HTTPS notice pages and review each URL before scheduling recurring runs.

Risk: The security guidance advises avoiding cron until notification delivery is verified.

Mitigation: Run the skill manually or in dry-run mode first, verify delivery behavior, and enable cron only after review.

Risk: The security guidance recommends a fixed version that runs Chromium with sandboxing enabled.

Mitigation: Run in an isolated environment and prefer a version that enables Chromium sandboxing before production use.

## Reference(s):

- [ClawHub Notice Monitor skill page](https://clawhub.ai/jerryharbin/skills/notice-monitor)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown-style notification reports, YAML configuration examples, and command-line usage snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are driven by configured tasks, keywords, schedules, notification targets, and deduplication state.]

## Skill Version(s):

1.0.1 (source: server release evidence, package.json, and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
