## Description:

Guides Go developers in using a typed client for Perplexity's REST API across chat, search, embeddings, agents, and related endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to add the go-perplexity package to a Go project and make typed requests to Perplexity for chat, search, embeddings, agents, and related endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An API key could be exposed if hardcoded, committed, logged, or included in printed request headers.

Mitigation: Read the key from an environment variable, such as PERPLEXITY_API_KEY; do not hardcode, commit, or log it, and do not print request headers.

Risk: API calls can incur costs or change account state, including creating, updating, or deleting skills and managing agent runs.

Mitigation: Make billable or state-changing calls only when requested by the user, and only on resources created for or named in the task.

Risk: The security verdict has medium confidence because scan coverage was partial and the guidance flags instruction scope for attention.

Mitigation: Review the skill and its setup reference before use, and apply ordinary care when following its instructions.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-perplexity)
- [Project repository](https://github.com/psyb0t/go-perplexity)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-perplexity)
- [Setup and reference](references/setup.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use bearer API key authentication and may call billable or account-changing endpoints.]

## Skill Version(s):

0.5.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
