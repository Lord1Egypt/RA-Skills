## Description:

Search public Kuaishou videos, creator posts and follower metrics, and video comments, returning structured JSON without logging in or publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, and analysts can use the skill to research public Kuaishou videos, creator activity, and comments for topic planning, competitor monitoring, creator screening, and audience insight.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and links may be sent to www.guaikei.com.

Mitigation: Only submit public Kuaishou terms and links you are comfortable sharing with that service.

Risk: ClawScan reports medium confidence and partial inspection, with 22 of 34 components fully inspected.

Mitigation: Consider the incomplete inspection coverage before installing; review the source if full coverage is required.

## Reference(s):

- [Guaikei API service and access](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/guaikei/skills/kuaishou-search-api)
- [Usage options](references/options.md)
- [FAQ and environment setup](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON response envelope containing search, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be empty or report an error; request limits depend on the API plan.]

## Skill Version(s):

1.1.3 (source: frontmatter, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
