## Description:

Provides guidance and examples for querying GitCode REST API data for repositories, branches, issues, pull requests, commits, tags, users, organizations, search, webhooks, members, and releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to find GitCode REST API endpoints, authentication requirements, request examples, response fields, status codes, and rate-limit guidance for repository and collaboration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill covers write, admin, membership, webhook, settings, transfer, and deletion API operations.

Mitigation: Require explicit user confirmation before any POST, PUT, PATCH, DELETE, membership, webhook, settings, transfer, or deletion operation.

Risk: Token handling guidance includes user-provided tokens and query-string access_token usage.

Mitigation: Use a narrowly scoped read-only token by default, prefer GITCODE_TOKEN from the environment, do not paste tokens into chat, and do not put tokens in URLs.

Risk: The release is flagged suspicious by the authoritative security scan because read-only querying and higher-risk operations are mixed without enough safeguards.

Mitigation: Install only when a broad GitCode API reference is needed and review generated API calls before execution.

## Reference(s):

- [GitCode API documentation](https://docs.gitcode.com/docs/apis/)
- [GitCode personal access tokens](https://gitcode.com/setting/token-classic)
- [GitCode API reference](artifact/reference.md)
- [GitCode API examples](artifact/examples.md)
- [ClawHub skill page](https://clawhub.ai/autoxj/skills/gitcode)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, API endpoint details, and token configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a GitCode personal access token via GITCODE_TOKEN for authenticated endpoints.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
