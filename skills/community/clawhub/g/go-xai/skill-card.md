## Description:

Unofficial Go client for the xAI (Grok) REST API at https://api.x.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add typed Go calls to xAI APIs, including chat, responses, embeddings, image and video generation, and file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some xAI API calls incur charges or change account state, including file and skill changes and stored response deletion.

Mitigation: Review the requested operation before calling it, and limit changes to resources the user identified or the task created.

Risk: The bearer API key can be exposed if it is hardcoded, committed, or logged.

Mitigation: Read the key from XAI_API_KEY or another secret store, and do not log request headers.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-xai repository](https://github.com/psyb0t/go-xai)
- [go-xai package documentation](https://pkg.go.dev/github.com/psyb0t/go-xai)
- [xAI API](https://api.x.ai)
- [ClawHub skill listing](https://clawhub.ai/psyb0t/skills/go-xai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use a bearer API key supplied through XAI_API_KEY.]

## Skill Version(s):

0.2.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
