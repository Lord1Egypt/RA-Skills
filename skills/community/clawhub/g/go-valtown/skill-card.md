## Description:

Provides Go developers with a typed client and guidance for managing Val Town resources through the Val Town API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to integrate Val Town API operations into Go applications, including managing vals, files, variables, blobs, SQLite, and email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account operations such as deleting resources, writing SQL, and sending email can make consequential or irreversible changes.

Mitigation: Only perform these operations when the user requests them; verify target resources first and grant the token only the permissions needed for the task.

Risk: The unofficial client uses an API token to access Val Town account data and resources.

Mitigation: Review and pin the dependency, read the token from the environment, and never commit or log the token or Authorization header.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-valtown)
- [Val Town API authentication guide](https://docs.val.town/reference/api/authentication)
- [Project repository](https://github.com/psyb0t/go-valtown)

## Skill Output:

**Output Type(s):** [Go code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
