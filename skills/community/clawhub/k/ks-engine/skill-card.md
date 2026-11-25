## Description:

Read-only Kuaishou analytics for searching public videos, reviewing creator and follower data, and analyzing video comments as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use the skill to research Kuaishou topics, compare public creator activity, review audience feedback, and identify content trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send keywords and video or creator links to guaikei.com.

Mitigation: Submit only public data queries you are comfortable sharing with the service.

Risk: Runtime permissions were not verified, and some scripts received only partial inspection.

Mitigation: Review the scripts and required permissions before installation or use.

## Reference(s):

- [API and token access](https://www.guaikei.com)
- [Command options](references/options.md)
- [FAQ and environment setup](references/faq.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public Kuaishou data; successful responses may include an estimated cost.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
