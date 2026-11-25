## Description:

Retrieves public Kuaishou videos, creator posts, and video comments by keyword or link, returning structured data to support user insight and product opportunity analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, and market researchers can search public Kuaishou videos, inspect creators’ public posts, and review video comments. They use the returned data to inform content research, audience insight, and product opportunity analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or profile links are sent to www.guaikei.com to retrieve data.

Mitigation: Use only non-sensitive keywords and links to public Kuaishou content.

Risk: The security review had medium confidence, inspected 20 of 32 components, and reported a degraded tool-misuse analyzer, leaving uncertainty about tool scope and code behavior.

Mitigation: Review the skill’s requested permissions and relevant scripts before installation, especially if its runtime access would be broader than expected.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/kuaishou-user-insight)
- [Guaikei service and API access](https://www.guaikei.com)
- [Complete command options](artifact/references/options.md)
- [Release changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [JSON envelope containing video, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are limited to public Kuaishou data; supported request limits depend on the token plan.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
