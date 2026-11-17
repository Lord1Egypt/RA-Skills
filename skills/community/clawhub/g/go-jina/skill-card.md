## Description:

Unofficial Go client for the Jina AI APIs, generated with oapi-codegen. Package `jina` (`github.com/psyb0t/go-jina`) calls api.jina.ai for embeddings, reranking, the model list, chat completions (document OCR) and batch embedding jobs; package `jinareader` (`github.com/psyb0t/go-jina/reader`) calls r.jina.ai to read a web page as markdown, text, HTML or JSON. Every endpoint is a typed `...WithResponse` method on `ClientWithResponses`, auth is a bearer API key set through `WithRequestEditorFn`, and responses decode into `JSON200` and per-status error fields. Use when Go code needs Jina embeddings, a reranker or the Reader API, or already imports go-jina.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers can use this skill to add typed clients for Jina AI embeddings, reranking, model discovery, chat completions, batch jobs, and web page reading. It guides API setup, bearer key handling, request construction, and response/error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text, images, documents, and URLs used with the clients are sent to Jina AI.

Mitigation: Send only content approved for sharing with Jina AI.

Risk: Batch embedding jobs can incur charges, and cancellation affects a job.

Mitigation: Authorize paid jobs explicitly and cancel only jobs owned by the task.

Risk: The external Go dependency is not bundled or audited here.

Mitigation: Review and pin the dependency before use.

## Reference(s):

- [go-jina source repository](https://github.com/psyb0t/go-jina)
- [go-jina package documentation](https://pkg.go.dev/github.com/psyb0t/go-jina)
- [setup and API reference](references/setup.md)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-jina)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.6.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
