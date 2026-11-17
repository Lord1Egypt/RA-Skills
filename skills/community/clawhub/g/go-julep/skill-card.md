## Description:

Unofficial Go client for the Julep API, generated with oapi-codegen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate applications with Julep through the typed go-julep client. It provides setup, authentication, endpoint, and response-handling guidance, including cautions around account changes and billed executions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests send selected data to the Julep API at the configured base URL.

Mitigation: Verify the destination and use only data appropriate to send there.

Risk: API keys can expose the associated Julep account if disclosed.

Mitigation: Read the key from an environment variable, and do not hardcode, commit, or log it.

Risk: Update, delete, secret, and execution operations can change account state or start billed work.

Mitigation: Use them only when explicitly authorized for resources the task owns.

Risk: This is an unofficial dependency.

Mitigation: Review the dependency and pin its version before adoption.

## Reference(s):

- [Setup and API client reference](references/setup.md)
- [go-julep package documentation](https://pkg.go.dev/github.com/psyb0t/go-julep)
- [go-julep project](https://github.com/psyb0t/go-julep)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-julep)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration instructions, Shell commands]

**Output Format:** [Markdown with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and endpoint guidance for the Go client.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
