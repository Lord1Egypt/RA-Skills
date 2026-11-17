## Description:

Provides guidance for using an unofficial, typed Go client for the Zulip REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Go developers use this skill to install and integrate an unofficial Zulip client for messaging, user and channel management, subscriptions, uploads, and event polling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security inspection was partial because one reference could not be resolved, leaving the evidence incomplete.

Mitigation: Review the unresolved reference and use judgment before installing.

Risk: API credentials and request content are sent to the configured Zulip server, and write operations can change organization data or settings.

Mitigation: Use a trusted HTTPS server, keep credentials out of source code and logs, and make changes only when requested for the specified resources.

## Reference(s):

- [Setup and API usage guide](artifact/references/setup.md)
- [Project homepage](https://github.com/psyb0t/go-zulip)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-zulip)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/go-zulip)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use the generated Go client API.]

## Skill Version(s):

0.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
