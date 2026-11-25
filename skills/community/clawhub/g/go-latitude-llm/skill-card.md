## Description:

Unofficial Go client for the Latitude LLM ops platform API at latitude.so (not Latitude.sh), generated with oapi-codegen. Package latitude (github.com/psyb0t/go-latitude-llm) provides latitude.NewClientWithResponses with a typed ...WithResponse method for every endpoint: projects, traces and spans, scores and annotations, saved searches, issues, API keys, OAuth keys, account and members. Auth is an organization API key or user OAuth token as a Bearer header added through a request editor. Use when Go code needs to call the Latitude LLM API, or already imports go-latitude-llm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use this Go client to call the Latitude LLM API to inspect projects, traces, scores and issues, or to perform authorized organization operations. It also provides typed Go request and response methods for the API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan is partial because two local references were unresolved.

Mitigation: Review the available skill and setup material before installing.

Risk: Organization operations can create or delete resources, change issues, revoke keys, manage members, or send exports by email.

Mitigation: Use write and export operations only within the user’s request, and verify the target and export recipients before sending.

Risk: Bearer credentials and trace or member data may be exposed if logged or sent to an untrusted API URL.

Mitigation: Read credentials from the environment, avoid logging tokens, headers, trace contents, or member information, and send credentials only to the trusted API URL.

## Reference(s):

- [Setup and API reference](artifact/references/setup.md)
- [Module source repository](https://github.com/psyb0t/go-latitude-llm)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-latitude-llm)
- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/go-latitude-llm)

## Skill Output:

**Output Type(s):** [Code, API Calls, Configuration instructions, Guidance]

**Output Format:** [Go code with concise Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples should check HTTP status and success response fields; the client does not provide automatic retries, pagination loops, or a default timeout.]

## Skill Version(s):

0.1.6 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
