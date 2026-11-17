## Description:

Use when integrating a new service with the IAM (Identity and Access Management) system - covers gRPC client setup, JWT token validation, permission checks, and REST API usage for the changyuanfeilun platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[effort02](https://clawhub.ai/user/effort02)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when connecting services to the changyuanfeilun IAM system. It helps them configure gRPC clients or REST calls, validate JWT tokens, check permissions, retrieve account context, and preserve app and tenant scoping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication guidance could lead services to expose or trust sensitive identity data insecurely.

Mitigation: Review before production IAM use, require TLS or mTLS for IAM gRPC traffic, and ensure user and tenant identity come from verified tokens or a trusted gateway that strips forged headers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/effort02/skills/iam-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with Java, XML, YAML, table, and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes IAM integration snippets, required headers, multi-tenancy rules, account status codes, and common implementation mistakes.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
