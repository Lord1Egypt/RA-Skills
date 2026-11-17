## Description:

A typed Go client for Writer's API, covering chat, text completions, models, files, Knowledge Graphs, no-code applications, and related tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers building Go applications use this client to call Writer services for chat, completions, model discovery, file and Knowledge Graph operations, no-code applications, and related tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and files supplied for upload are sent to Writer.

Mitigation: Review the content before sending and avoid sharing information that should not be sent to Writer.

Risk: The client uses a Writer API key for authenticated requests.

Mitigation: Keep the key in WRITER_API_KEY; do not hard-code, commit, or log it.

Risk: File and Knowledge Graph operations can upload or delete user data.

Mitigation: Perform uploads or deletions only when requested and only for resources owned by the task.

## Reference(s):

- [Setup and API reference](artifact/references/setup.md)
- [Project repository (listed in skill documentation)](https://github.com/psyb0t/go-writer-ai)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-writer-ai)
- [ClawHub release](https://clawhub.ai/psyb0t/skills/go-writer-ai)

## Skill Output:

**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions]

**Output Format:** [Go code, shell commands, and Writer API responses (JSON or raw HTTP)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Response shape depends on the selected endpoint; streaming responses are exposed as raw HTTP responses.]

## Skill Version(s):

0.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
