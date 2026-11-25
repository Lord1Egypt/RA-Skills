## Description:

An unofficial typed Go client for the Lovable API, with guidance for managing projects, publishing, analytics, security findings, workspaces, groups, and members.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to integrate Go applications with Lovable for project, publishing, workspace, analytics, and security operations, including requested account changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lovable API keys and embed URLs grant scoped or tokenized access to account resources.

Mitigation: Load API keys from environment variables, never log credentials, and share embed URLs only with intended recipients.

Risk: Project updates, deletion, publishing settings, publishing, and unpublishing can affect account resources or access.

Mitigation: Perform write operations only when the user requested them; check deployment and resource state before retrying uncertain writes.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-lovable repository](https://github.com/psyb0t/go-lovable)
- [go-lovable package documentation](https://pkg.go.dev/github.com/psyb0t/go-lovable)
- [Lovable API key settings](https://lovable.dev/settings/api-keys)

## Skill Output:

**Output Type(s):** [Code, API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.3.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
