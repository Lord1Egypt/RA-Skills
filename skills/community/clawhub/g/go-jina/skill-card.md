## Description:

Typed Go clients for Jina AI embeddings, reranking, chat completions, batch jobs, model discovery, and web page reading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add typed clients for Jina AI's embedding, reranking, chat, batch, model-list, and Reader APIs to a Go project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, images, documents, and URLs sent through the clients are processed by Jina AI's hosted services.

Mitigation: Send only data that is approved for sharing with Jina AI.

Risk: API credentials and batch-job operations can expose access or incur charges.

Mitigation: Read the API key from the environment, do not log credentials or Authorization headers, and create or cancel only jobs the task owns when requested.

Risk: The security review is partial, and setup details and the listed API operations need review before installation.

Mitigation: Review the setup reference and confirm that the API operations fit the intended use before installing.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-jina)
- [Project homepage](https://github.com/psyb0t/go-jina)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/go-jina)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.6.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
