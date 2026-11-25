## Description:

Writes Go code with the unofficial go-coolify client for the Coolify API, covering applications, deployments, databases, services, projects, servers, and teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to write Go code that integrates with Coolify through the unofficial go-coolify client, including inspecting resources and making infrastructure changes when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and notes a low-confidence concern about autonomous decisions.

Mitigation: Review the skill instructions before installing, and check outcomes before retrying infrastructure changes.

Risk: Coolify operations can change or delete user infrastructure, and API requests use a bearer token.

Mitigation: Run mutating operations only when requested; send the token only to the intended HTTPS instance, and never hardcode, commit, or log it.

## Reference(s):

- [Setup and API usage](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-coolify)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-coolify)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/go-coolify)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go source code and Markdown setup guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides callers to use a user-supplied Coolify API URL and token; infrastructure-changing operations are performed only when requested.]

## Skill Version(s):

0.13.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
