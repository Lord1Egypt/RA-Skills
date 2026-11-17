## Description:

Helps developers integrate Go applications with Cerebras inference using the unofficial go-cerebras client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Go code that calls Cerebras for chat or text completions and model lookup, including projects that already use go-cerebras.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client is an unofficial dependency.

Mitigation: Review and pin the dependency before use.

Risk: Requests send the API key and prompts to the configured provider endpoint.

Mitigation: Keep the API key in an environment variable, use a trusted HTTPS endpoint, and send only prompts intended for that provider.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-cerebras)
- [go-cerebras source repository](https://github.com/psyb0t/go-cerebras)
- [go-cerebras package documentation](https://pkg.go.dev/github.com/psyb0t/go-cerebras)
- [Setup and reference](references/setup.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the complete-response client; streaming requires reading the response body from the plain client.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
