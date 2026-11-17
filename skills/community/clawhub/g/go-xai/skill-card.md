## Description:

Guides Go developers in using the unofficial go-xai client to call xAI's REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate xAI's API into Go projects with typed client methods. It guides setup, authentication, endpoint selection, request construction, and response handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed through source code, logs, or request headers.

Mitigation: Read the key from an environment variable and do not commit or log it or print request headers.

Risk: Some API calls incur charges or change account resources, including uploads, deletes, and public links.

Mitigation: Make paid or state-changing calls only when requested, and limit them to resources the user named or the task created.

## Reference(s):

- [Setup and API reference](references/setup.md)
- [go-xai package documentation](https://pkg.go.dev/github.com/psyb0t/go-xai)
- [go-xai project homepage](https://github.com/psyb0t/go-xai)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover typed API requests, bearer authentication, and response handling.]

## Skill Version(s):

0.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
