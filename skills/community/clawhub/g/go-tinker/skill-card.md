## Description:

Unofficial Go client for the Thinking Machines Tinker API, generated with oapi-codegen. `tinker.NewClientWithResponses(baseURL, auth)` from `github.com/psyb0t/go-tinker` gives typed methods for every endpoint of the Tinker training API (create and unload LoRA models, forward and forward-backward passes, optimizer steps, sampling, saving and loading weights, retrieving futures, server capabilities, health). Auth is an `X-API-Key` header set in a request editor. Use when Go code needs to call the Tinker API, or the project already imports go-tinker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this skill to add and call the unofficial typed Go client for Thinking Machines Tinker, including model training, sampling, and result retrieval. It guides installation, request authentication, endpoint usage, and response handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Training calls can incur compute costs, and model changes can affect model state.

Mitigation: Authorize training costs and model changes explicitly; use only models the task created or the user named.

Risk: An exposed API key or untrusted endpoint could compromise access credentials.

Mitigation: Keep the API key private, read it from TINKER_API_KEY, and use a trusted HTTPS endpoint.

Risk: The client is unofficial and may differ from the official SDK's supported features.

Mitigation: Review the project's API coverage and consider pinning the dependency version before relying on it.

## Reference(s):

- [Setup and endpoint reference](artifact/references/setup.md)
- [Project repository](https://github.com/psyb0t/go-tinker)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-tinker)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-tinker)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown with Go code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
