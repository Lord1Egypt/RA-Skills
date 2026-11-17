## Description:

Jike SEO helps agents research SEO keywords across Douyin, Xiaohongshu, and WeChat by querying keyword volume, competition, related terms, suggestions, trend, and audience data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzoob](https://clawhub.ai/user/mzoob)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers, SEO specialists, and growth teams use this skill to search and analyze keywords, compare platform demand, identify low-competition opportunities, and plan content or GEO keyword strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The check command prints part of the configured API key, which could expose a credential fragment in logs or shared agent sessions.

Mitigation: Avoid running the check command in logged terminals or shared sessions; prefer using search or detail commands after configuring the key.

Risk: Keyword queries and the JIKE_SEO_API_KEY are sent to the declared SEO service.

Mitigation: Install and use the skill only when sending those queries and credentials to the Jike SEO service is acceptable for the user's workflow.

## Reference(s):

- [Jike SEO skill page](https://clawhub.ai/mzoob/skills/jike-seo)
- [Publisher profile](https://clawhub.ai/user/mzoob)
- [Product homepage](https://dso100.com)
- [API key portal](https://jike-seo.100.city)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Chinese prose with formatted keyword metrics and optional JSON from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the JIKE_SEO_API_KEY environment variable; the skill queries the declared Jike SEO API service.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
