## Description:

Contentful GraphQL (contentful.com). Use this skill for ANY Contentful GraphQL request — searching and reading data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use the skill to inspect the Contentful GraphQL action contract and search or read content in a connected Contentful space and environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs remote CLI installers whose contents were not verified, and the hosted connector implementation was not verified.

Mitigation: Review and approve CLI setup separately, prefer a reviewed and pinned release, inspect bundled-skill synchronization settings, and connect only the Contentful access needed.

## Reference(s):

- [Contentful GraphQL API documentation](https://www.contentful.com/developers/docs/references/graphql/)
- [Contentful](https://www.contentful.com)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [JSON action requests and Contentful GraphQL query results, with brief Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query results depend on the connected Contentful space, environment, and account permissions.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
