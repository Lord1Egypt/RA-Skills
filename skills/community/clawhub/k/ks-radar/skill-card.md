## Description:

This skill searches public Kuaishou videos, creator posts, and video comments, returning structured data for content and competitor research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use it to research public Kuaishou videos, creator activity, and comment themes for topic selection and competitor analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, account identifiers, and video or profile links are sent to the third-party API; the security assessment had partial coverage.

Mitigation: Send only public-data queries you are comfortable sharing with guaikei.com, and account for the assessment's partial coverage when deciding whether to use the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/guaikei/skills/ks-radar)
- [Guaikei API and access information](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, API data]

**Output Format:** [Structured JSON response envelopes containing search results, creator posts, or comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public Kuaishou data. API plan limits vary; monthly plans cap searches at 30 results, creator posts at 50, and comments at 60.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
