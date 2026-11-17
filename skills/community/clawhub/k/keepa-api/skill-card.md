## Description:

Keepa Api helps agents query Amazon product details, price history, sales rank history, search results, and best seller data through the Keepa API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boyd4y](https://clawhub.ai/user/boyd4y)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to configure and run Keepa API queries for Amazon ASIN lookups, price history, sales rank history, product search, and best seller lists across supported marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a Keepa API key and sends product queries to Keepa, and the security evidence says key handling can expose the key.

Mitigation: Prefer an environment variable, keep any CONFIG.md file out of repositories and backups, restrict config file permissions, avoid logging real keys in terminals or CI, and rotate the key if exposure is suspected.

Risk: The security verdict is suspicious and recommends review before installation.

Mitigation: Review the skill and its shell script before deployment, and install it only if sending the configured Keepa API key and product queries to Keepa is acceptable.

## Reference(s):

- [Keepa API Reference](references/api-docs.md)
- [Keepa API Documentation](https://keepa.com/#!api)
- [Keepa Category Reference](https://keepa.com/#!category)
- [Keepa API Examples](https://github.com/keepacom/api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands, tabular text reports, and optional formatted JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and a user-provided Keepa API key.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
