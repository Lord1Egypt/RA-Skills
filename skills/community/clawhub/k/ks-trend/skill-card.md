## Description:

Searches public Kuaishou videos, creator posts and follower data, and video comments, returning structured JSON for trend research and content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use it to find trending topics, monitor public creator activity, shortlist KOLs, and review comment trends on Kuaishou.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and medium-confidence; search terms or public Kuaishou links may be sent to the third-party service.

Mitigation: Submit only public-data queries and links you are comfortable sharing with guaikei.com.

Risk: Using the service requires a GUAIKEI_API_TOKEN.

Mitigation: Keep the token in the required environment variable and out of prompts and shared files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/ks-trend)
- [Guaikei Kuaishou data API and token access](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Configuration and troubleshooting FAQ](references/faq.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON envelope with video search, creator post, or comment results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public-data results; successful responses may include estimated cost metadata. Saving results is optional.]

## Skill Version(s):

1.1.3 (source: frontmatter, references/changelog.md, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
