## Description:

Tool for interacting with a self-hosted HomeBox inventory management service via its REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ukeyboard](https://clawhub.ai/user/ukeyboard)

### License/Terms of Use:

MIT-0

## Use Case:

HomeBox users and agents use this skill to search, add, update, delete, and inspect home inventory items, locations, and tags through a HomeBox REST API. It is aimed at low-friction inventory management from natural language requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles HomeBox credentials and can print bearer tokens during login.

Mitigation: Treat tokens as secrets, avoid passing passwords on the command line, and store the token through the agent or runtime secret mechanism.

Risk: The skill includes guidance for disabling TLS verification for self-signed certificates.

Mitigation: Prefer HTTPS with a properly trusted certificate or CA; only use disabled TLS verification on trusted networks after review.

Risk: The CLI can add, update, and delete inventory records.

Mitigation: Require explicit user confirmation before write or delete operations, and fetch current item, location, and tag IDs before acting.

## Reference(s):

- [HomeBox API Reference](references/api-reference.md)
- [Old API Swagger Summary](references/old-api-swagger-summary.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell commands with JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer plus HomeBox base URL and bearer token configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
