## Description:

Unofficial Go client for the Roark voice AI agent testing and monitoring API, with typed methods for agents, calls and transcripts, chats, simulations, run plans, personas, metrics, webhooks and projects, authenticated with a bearer key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this Go client to integrate applications with Roark for voice agent monitoring, simulations, metrics, and project management. They can use its setup guidance to install the package, configure credentials, choose operations, and handle responses safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review found no reported issues in the reviewed material, but two local references could not be matched to bundled artifact files, leaving the review incomplete with medium confidence.

Mitigation: Check referenced materials before relying on guidance that depends on them.

Risk: Some API operations can create or delete resources, start simulations, collect metrics, change configuration, or promote revisions; calls, transcripts, recordings, and credentials may also contain private data.

Mitigation: Run consequential operations only when requested, keep the bearer credential out of source control and logs, and return only the private data needed for the task.

## Reference(s):

- [Setup and API usage reference](artifact/references/setup.md)
- [go-roark source repository](https://github.com/psyb0t/go-roark)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-roark)
- [Roark API](https://api.roark.ai)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.22.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
