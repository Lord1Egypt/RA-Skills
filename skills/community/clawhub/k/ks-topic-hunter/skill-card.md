## Description:

Search public Kuaishou videos by keyword, retrieve creator posts and follower metrics, or read video comments as structured JSON without logging in or posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts can use this skill to research public Kuaishou videos, creator activity, and comments for topic discovery, competitor monitoring, creator screening, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and public video or creator links are sent to www.guaikei.com; scanner confidence is medium and some scripts had only partial inspection.

Mitigation: Send only information appropriate to share with that service, and review its privacy terms before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/guaikei/skills/ks-topic-hunter)
- [Guaikei service and token setup](https://www.guaikei.com)
- [Command options](references/options.md)
- [FAQ and environment setup](references/faq.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON containing video search results, creator posts and profile metrics, or video comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schema-backed results; available record counts depend on request and token plan limits.]

## Skill Version(s):

1.1.3 (source: server release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
