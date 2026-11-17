## Description:

Provides Go developers with typed guidance for calling Meta’s Llama API using the unofficial go-llama-api client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate applications with Meta’s Llama API for chat completions, model discovery, moderation, and file uploads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed Llama API key could be misused.

Mitigation: Read LLAMA_API_KEY from the environment; do not hardcode, commit, log, or print request headers containing it.

Risk: Prompts and uploaded files are sent to Meta when requests run.

Mitigation: Send only prompts and files the user intends to share, and upload files only when requested.

Risk: This is an unofficial client dependency.

Mitigation: Review the dependency version before adding it to a project.

## Reference(s):

- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-llama-api)
- [Package documentation](https://pkg.go.dev/github.com/psyb0t/go-llama-api)
- [Setup and reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-llama-api)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream instructions and examples for Go projects.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
