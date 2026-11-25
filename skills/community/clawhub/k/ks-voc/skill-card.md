## Description:

Searches public Kuaishou videos, creator posts and follower statistics, and video comments, returning structured JSON without logging in or interacting with accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, researchers, and account operators can find public Kuaishou videos by keyword, review creator posts and follower statistics, and inspect video comments for topic research, competitor monitoring, creator screening, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and supplied URLs are sent to guaikei.com; the security scan is benign but medium confidence, with partial script inspection.

Mitigation: Avoid confidential queries and share only terms or links you are authorized to send; review returned public data before relying on it.

Risk: API requests require a GUAIKEI_API_TOKEN and may consume paid plan usage.

Mitigation: Use result limits appropriate to the task and check the service plan before requesting larger result sets.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/ks-voc)
- [Guaikei API service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON records with concise text summaries as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results, creator posts and profile statistics, or video comments; result limits depend on the API plan.]

## Skill Version(s):

1.1.3 (source: server-resolved release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
