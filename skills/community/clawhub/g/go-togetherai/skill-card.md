## Description:

Guides Go developers in using the unofficial go-togetherai client to call Together AI REST API endpoints with typed requests and responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to install and integrate the go-togetherai Go client for Together AI models, chat completions, embeddings, and other API operations. It guides setup, authentication, typed requests, and response handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is incomplete because one local reference was missing.

Mitigation: Review the available skill files and account for the missing reference when deciding whether to install.

Risk: Prompts and files sent through the client are processed by Together AI; fine-tuning jobs and dedicated resources can incur costs, and delete operations remove data.

Mitigation: Avoid sending sensitive content unless appropriate, and run costly or deleting operations only when explicitly requested.

Risk: A Together AI API key could be exposed if hardcoded, committed, or logged.

Mitigation: Read the key from an environment variable such as TOGETHER_API_KEY, and do not print or log request headers.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-togetherai)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-togetherai)

## Skill Output:

**Output Type(s):** [Go code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go source code and concise Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Go 1.26.11 or newer and a Together AI API key; the client reads full response bodies rather than streaming token by token.]

## Skill Version(s):

0.8.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
