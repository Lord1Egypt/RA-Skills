## Description:

A read-only Kuaishou data skill that searches public videos, retrieves creator posts and account metrics, and collects video comments as structured JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and analysts use this skill to research Kuaishou content topics, compare public video and creator metrics, and review video comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict, but its review was partial: 22 of 34 components were scanned and some executable files could not be fully interpreted.

Mitigation: Review the skill files before use and run it only in an environment where you are comfortable using its required API token.

Risk: The skill sends search keywords or video and creator links to the Guaikei service to retrieve public Kuaishou data.

Mitigation: Use only public Kuaishou queries and avoid sending links or keywords you do not want shared with that service.

## Reference(s):

- [Options and query limits](references/options.md)
- [Setup and FAQ](references/faq.md)
- [Release changelog](references/changelog.md)
- [Guaikei Kuaishou data service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON data envelope containing search results, creator information and posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result limits depend on the API plan; monthly plan caps are 30 search results, 50 creator posts, and 60 comments.]

## Skill Version(s):

1.1.3 (source: frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
