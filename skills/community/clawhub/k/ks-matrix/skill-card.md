## Description:

Queries publicly available Kuaishou videos, creator posts and profile metrics, and comments, returning structured JSON for account monitoring and comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketing teams, analysts, and MCNs use it to collect public Kuaishou data across accounts for comparison, content research, competitor monitoring, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted search terms and links are sent to a third-party API, and the security scan notes that some scripts were only partially inspected.

Mitigation: Avoid sending confidential terms or links, and review the package code before deployment.

## Reference(s):

- [API access and token setup](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/guaikei/skills/ks-matrix)
- [Usage options](references/options.md)
- [FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only results for keyword searches, creator posts and profile metrics, or comments; result limits depend on the API plan.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
