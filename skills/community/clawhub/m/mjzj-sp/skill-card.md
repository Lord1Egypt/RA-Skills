## Description:

查询卖家之家跨境电商服务商分类和服务商列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up MJZJ service-provider categories and search provider listings for cross-border e-commerce needs. When a user explicitly decides to contact a provider, the skill documents a handoff path that requires authentication through a separate messaging skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests MJZJ_API_KEY even though its public search endpoints do not require authentication.

Mitigation: Use the skill without an API key for search-only workflows; provide MJZJ_API_KEY only when authenticated messaging is intended.

Risk: Search results can lead into private provider messaging through a separate skill.

Mitigation: Require explicit user selection and confirmation before sending messages, and use the returned userSlug only for the selected provider.

Risk: ID-like fields, including Snowflake IDs, can lose precision if treated as numbers.

Mitigation: Preserve all ID-like values as strings across input, output, and parameter passing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-sp)
- [MJZJ service-provider portal](https://sp.mjzj.com)
- [MJZJ service-provider categories API](https://data.mjzj.com/api/spQuery/getClassifies)
- [MJZJ service-provider search API](https://data.mjzj.com/api/spQuery/queryProviders)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with curl examples and API parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public search can run without a token; authenticated provider messaging requires MJZJ_API_KEY. All ID-like fields should be preserved as strings.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
