## Description:

Discover and review Kuaishou creators for collaboration by searching public videos, reviewing creator posts and comments, and comparing content and engagement data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Brand marketers, content creators, market analysts, and MCN teams can use this skill to research public Kuaishou videos, creator accounts, and comments, then prepare evidence-based creator shortlists and content insights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and Kuaishou links are sent to the GUAIKEI service.

Mitigation: Avoid putting confidential or sensitive information in search terms or supplied links, and review the service terms before use.

Risk: The skill requires a GUAIKEI_API_TOKEN, and optional saved logs contain query results and timestamps.

Mitigation: Store the token as a secret, keep optional logging disabled unless needed, and handle any saved logs according to your retention rules.

Risk: The security scan was partial and some code could not be fully interpreted.

Mitigation: Review the required environment access and timestamp behavior before installing or running the skill.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/kuaishou-creator-screening)
- [Publisher profile](https://clawhub.ai/user/why20261)
- [GUAIKEI service and token access](https://www.guaikei.com)
- [Usage options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON data with concise analysis and creator shortlist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public Kuaishou video, creator, and comment data; result counts depend on the token plan.]

## Skill Version(s):

1.1.2 (source: release metadata, SKILL.md frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
