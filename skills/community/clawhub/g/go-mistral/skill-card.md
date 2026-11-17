## Description:

Guides Go developers in using the unofficial typed Go client for the Mistral AI REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add and call the Go Mistral client for chat completions, embeddings, model listing, and other Mistral AI API operations. It provides setup, authentication, request, and response guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests can send prompts and files to Mistral AI for processing.

Mitigation: Send only data you intend Mistral AI to process.

Risk: A bearer API key could be exposed through source code or logs.

Mitigation: Read the key from MISTRAL_API_KEY, keep it out of source control, and do not log or print request headers.

Risk: Batch jobs can incur charges, and delete operations remove data.

Mitigation: Run batch or delete operations only when the user explicitly requests them.

Risk: The downloaded third-party dependency implementation was outside the documented security review scope.

Mitigation: Review and pin the third-party dependency version.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [Project repository](https://github.com/psyb0t/go-mistral)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-mistral)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/go-mistral)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream guidance for integrating and using the client.]

## Skill Version(s):

0.3.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
