## Description:

Retrieves public Kuaishou video search results, creator posts and profile metrics, and video comments as structured JSON for daily briefs and performance reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External Kuaishou creators, marketers, and analysts can use the skill to search public videos, review creator activity and audience metrics, and inspect video comments. Agents can use the returned data to prepare daily summaries, performance reviews, and weekly reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reported a possible privacy disclosure gap, and inspection was partial (22 of 34 components fully inspected). The skill sends search terms or Kuaishou links to the Guaikei service and can retrieve public comments.

Mitigation: Use only public Kuaishou information, avoid including sensitive details in search terms, URLs, or comments, and review the partially inspected code and data handling before deployment.

Risk: When saving is enabled, retrieved data is written to local temporary-directory logs.

Mitigation: Enable saved logs only when needed and review or remove them before sharing the machine or its files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/ks-brief)
- [Guaikei API service and access](https://www.guaikei.com)
- [CLI options](artifact/references/options.md)
- [FAQ](artifact/references/faq.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [Structured JSON data envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video search results, creator posts or profile statistics, or video comments. Request limits depend on the API token plan. Requires Node.js 16.14+ and GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.1.3 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
