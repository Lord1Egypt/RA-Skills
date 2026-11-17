## Description:

Interact directly with the monday.com GraphQL API to read and create boards, items, columns, updates, and users without a third-party gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonah-saltzman](https://clawhub.ai/user/jonah-saltzman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent query and update a monday.com workspace through the official GraphQL API client. It supports task lookup, board inspection, item creation, status updates, and related workspace operations when an authenticated monday.com token is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated monday.com API access can give an agent broad workspace read and write capability.

Mitigation: Use a least-privileged monday.com token and explicitly confirm create, update, and delete-style operations before execution.

Risk: API tokens may be exposed if copied into prompts, logs, or generated code.

Mitigation: Provide MONDAY_API_TOKEN through the environment or approved secret injection and avoid printing or storing the token.

Risk: Dependency installation is not fully reproducible without a lockfile or pinned transitive dependencies.

Mitigation: Pin dependencies and add a lockfile before deploying in a sensitive workspace.

## Reference(s):

- [Monday Direct ClawHub skill page](https://clawhub.ai/jonah-saltzman/skills/monday-direct)
- [monday.com API client package](https://www.npmjs.com/package/@mondaydotcomorg/api)
- [monday.com API release notes](https://developer.monday.com/api-reference/docs/release-notes)
- [GraphQL API best practices](artifact/references/graphql-api-best-practices.md)
- [API client best practices](artifact/references/api-client-best-practices.md)
- [Backend usage rules](artifact/references/backend-usage-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MONDAY_API_TOKEN; API calls return JSON on success and structured errors on failure.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
