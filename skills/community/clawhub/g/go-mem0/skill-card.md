## Description:

Unofficial Go client for the Mem0 Platform API, with typed methods for memory and related platform operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate Go applications with the hosted Mem0 Platform API for memory and related platform operations. It is also useful when a project already depends on github.com/psyb0t/go-mem0.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The client sends memory content, queries, and metadata to the hosted Mem0 API.

Mitigation: Send only the data needed for the task and scope filters to the intended user, agent, app, or run.

Risk: Create, update, and delete operations can change hosted memories and related resources.

Mitigation: Use these operations only on task-owned resources when the user requested the change.

Risk: The security review is medium confidence and partial because some referenced paths were unavailable.

Mitigation: Review the skill guidance and source material before relying on behavior tied to unavailable references.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-mem0)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-mem0)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typed Go API usage instructions, including authentication, request and response handling, and endpoint guidance.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
