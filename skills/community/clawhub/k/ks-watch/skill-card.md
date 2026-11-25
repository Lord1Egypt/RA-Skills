## Description:

This skill retrieves public Kuaishou (Kwai) videos, creator metrics, and comments as JSON for sentiment, negative-mention, brand, and reputation review; it does not log in or publish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External analysts and marketing teams use the skill to research Kuaishou topics, review competitors and creators, and inspect public comments for sentiment and brand mentions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Twelve of 34 components were only partly inspected, so the security evidence is incomplete.

Mitigation: Review the remaining scripts before installation, especially for high-trust use or workflows involving sensitive information.

## Reference(s):

- [Command options](references/options.md)
- [FAQ](references/faq.md)
- [Kuaishou public-data API](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON envelope containing video, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One envelope per command; results cover public content and account metrics.]

## Skill Version(s):

1.1.3 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
