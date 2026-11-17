## Description:

TypeScript library and CLI for Monarch Money budget management, including transaction search, category updates, account and budget listing, and authentication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davideasaf](https://clawhub.ai/user/davideasaf)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent work with Monarch Money budget data through a TypeScript CLI or library. It supports finding transactions, categorizing spending, listing accounts and budgets, and managing authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Monarch Money credentials and MFA secrets.

Mitigation: Use it only in a trusted environment, provide secrets through protected environment variables, and avoid passing passwords or MFA seeds on the command line.

Risk: Saved sessions at ~/.mm/session.json can act as live credentials.

Mitigation: Treat the session file as sensitive, restrict file permissions, and log out or remove the session when access is no longer needed.

Risk: Some operations can modify account data, including transaction updates and create/delete actions.

Mitigation: Require explicit user confirmation before write, create, delete, or deleteAllTransactionRules operations.

Risk: Debug output or stale dependencies may expose sensitive information or increase operational risk.

Mitigation: Do not enable debug logging during login, update dependencies, and fix credential redaction and session storage before production use.

## Reference(s):

- [Monarch Money API Reference](references/API.md)
- [Troubleshooting Guide](references/TROUBLESHOOTING.md)
- [Monarch Money App](https://app.monarchmoney.com)
- [Monarch Money API Endpoint](https://api.monarch.com)
- [Monarch Money Status](https://status.monarchmoney.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON snippets, and TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read or modify Monarch Money account data when the authenticated user authorizes them.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
