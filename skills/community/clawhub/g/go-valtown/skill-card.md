## Description:

An unofficial typed Go client for calling the Val Town API to manage vals and related account resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add and use a typed client for Val Town's API. It provides setup, authentication, endpoint, pagination, and error-handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was benign with medium confidence, but scanner coverage was partial because some local references could not be resolved.

Mitigation: Review the available skill files and resolve the missing references before relying on the scan result.

Risk: Some API operations can delete account resources, write SQL, or send email, and the skill says those changes cannot be undone through this client.

Mitigation: Use these operations only when requested, verify the target resources and inputs, and keep the API token out of source control and logs.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [GitHub project](https://github.com/psyb0t/go-valtown)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-valtown)

## Skill Output:

**Output Type(s):** [Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use a Val Town API token supplied through the environment.]

## Skill Version(s):

0.1.5 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
