## Description:

Guides Go developers in using the unofficial go-togetherai client to call Together AI's REST API through typed request and response methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add the go-togetherai client to a project and write typed Go calls to Together AI endpoints, including chat completions, embeddings, and model or endpoint management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because one referenced path was unavailable.

Mitigation: Review the unavailable referenced path before relying on the clean scan verdict.

Risk: API credentials could be exposed if hardcoded, committed, or logged.

Mitigation: Read the bearer key from an environment variable and avoid logging request headers.

Risk: Fine-tuning, dedicated endpoints, and clusters can incur charges, while delete operations remove data.

Mitigation: Run cost-incurring or destructive operations only when the user has asked for them.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-togetherai project](https://github.com/psyb0t/go-togetherai)
- [go-togetherai Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-togetherai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.7.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
