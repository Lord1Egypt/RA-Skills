## Description:

Product Fruits (productfruits.com). Use this skill for ANY Product Fruits request — searching and reading data. Whenever a task involves Product Fruits, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a connected OOMOL account can list Product Fruits knowledge-base articles and categories, or retrieve localized article and category content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a remote installer whose contents are unverified and may make automatic agent-skill changes.

Mitigation: Review and approve the CLI installation separately, including its automatic agent-skill changes, before running the setup fallback.

Risk: The live connector implementation is unverified and mediates access to the Product Fruits account.

Mitigation: Confirm that OOMOL should mediate access to the account and review the connector before relying on it.

## Reference(s):

- [Product Fruits](https://productfruits.com)
- [Product Fruits REST API authentication documentation](https://help.productfruits.com/en/article/rest-api-authentication)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, JSON]

**Output Format:** [Connector results in JSON; article content may be Markdown or HTML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only knowledge-base lookups; results vary by action and may include localized content.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
