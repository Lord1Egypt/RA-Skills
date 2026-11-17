## Description:

Unofficial typed Go client for managing Lovable projects, publishing, deployment status, analytics, security data, workspaces, groups, and members through the Lovable API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers can use the typed client to read Lovable project, workspace, analytics, and security data, and to perform project management or publishing actions when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and embed URLs carry access credentials.

Mitigation: Use a minimally scoped Lovable key, keep credentials and token-bearing embed links private, and never log authorization headers.

Risk: The unofficial Go dependency is outside the security review of the bundled documentation.

Mitigation: Review and pin the dependency before using it with sensitive projects.

Risk: Project edits and publishing operations can change account resources or access.

Mitigation: Request explicit user authorization before performing account-changing actions.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-lovable)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-lovable)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May cover authenticated API access and account-changing operations.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
