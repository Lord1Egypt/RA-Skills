## Description:

Generates SEO/GEO-optimized Chinese marketing articles for local businesses, with batch generation, keyword suggestions, and SEO quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g620710](https://clawhub.ai/user/g620710)

### License/Terms of Use:

MIT

## Use Case:

External users and marketing teams use this skill to generate, check, and plan local-business SEO/GEO content for websites, social channels, and AI-search visibility. It is aimed at commercial content marketing workflows for local services and high-value local industries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags this release as suspicious because article topics and account credentials may be sent to an undocumented plaintext HTTP backend.

Mitigation: Review the backend operator and data handling before use, require HTTPS-only service endpoints, and avoid sending sensitive topics or credentials unless the service is trusted.

Risk: The server guidance warns that the documentation and code disagree about credential handling, including a risk of users placing a DeepSeek API key in GEO_USER_KEY.

Mitigation: Use only the publisher-issued GEO_USER_KEY for this skill; rotate any DeepSeek API key that was placed in GEO_USER_KEY and align documentation with the runtime behavior.

Risk: Generated SEO/GEO content may contain inaccurate, misleading, or noncompliant claims for regulated or high-value local services.

Mitigation: Require human review, factual verification, and legal or platform-policy checks before publishing generated articles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/g620710/skills/local-geo-writer)
- [DeepSeek API endpoint referenced by documentation](https://api.deepseek.com/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown articles, plain-text status output, shell commands, and optional output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a GEO_USER_KEY credential; generated articles should be reviewed before publication.]

## Skill Version(s):

2.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
