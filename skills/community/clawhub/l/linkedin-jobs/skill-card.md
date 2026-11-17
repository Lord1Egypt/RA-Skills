## Description:

Search and monitor LinkedIn job listings with city-based filters, hourly cron support, and smart deduplication across 100+ global tech hubs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yashsuman15](https://clawhub.ai/user/yashsuman15)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search LinkedIn job listings, manage recurring search profiles, and receive deduplicated job results for configured roles and locations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes web requests to LinkedIn job pages.

Mitigation: Use it only when LinkedIn web requests are acceptable for the environment, and keep scraper rate and timeout settings conservative.

Risk: Search profiles and seen-job history are stored locally.

Mitigation: Review saved search terms and delete local profile or history files when they are no longer needed.

Risk: Recurring monitoring can continue after setup if the schedule is not understood.

Mitigation: Confirm the exact cron or OpenClaw schedule before enabling monitoring, and document how to disable it.

Risk: Job listing text and links come from external pages.

Mitigation: Treat listing content as untrusted and review links, requirements, and summaries before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yashsuman15/skills/linkedin-jobs)
- [ClawHub homepage metadata](https://clawhub.ai/skills/linkedin-jobs)
- [LinkedIn Jobs](https://linkedin.com/jobs)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Configuration]

**Output Format:** [JSON job listings and Markdown-style job notifications with CLI commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local search profiles and seen-job history for recurring monitoring.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
