## Description:

Writes Go code with go-coolify (package coolify, github.com/psyb0t/go-coolify), an unofficial generated client for the Coolify API covering applications, deployments, databases, services, projects, servers and teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add or update Go code that reads or changes Coolify resources through the unofficial go-coolify client. It provides setup, authentication, operation selection, and response-handling guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and could not resolve one local path-like reference, so its benign result has medium confidence.

Mitigation: Review the operation guidance before installing, especially guidance about infrastructure-changing actions and retries.

Risk: Retrying a Coolify operation that changes infrastructure may repeat an action whose first attempt already succeeded.

Mitigation: Check whether the action succeeded before retrying, and use changing operations only when the user requested them.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-coolify on pkg.go.dev](https://pkg.go.dev/github.com/psyb0t/go-coolify)
- [go-coolify source repository](https://github.com/psyb0t/go-coolify)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and setup guidance; no files are produced directly by the skill.]

## Skill Version(s):

0.12.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
