## Description:

An unofficial typed Go client for calling the Label Studio API from Go applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this typed Go client to integrate Go applications with Label Studio, including project, task, annotation, prediction, storage, and administration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial because an AGENTS.md reference was missing, so some evidence is incomplete.

Mitigation: Review the available source and the missing reference before relying on the scanner result.

Risk: API calls can create, update, or delete Label Studio data.

Mitigation: Perform data-changing actions only when requested and on resources within the user's scope.

Risk: API credentials and task content are sent to the configured Label Studio server.

Mitigation: Use a trusted server URL, HTTPS for remote servers, and keep API tokens out of source code, logs, and request headers shared for debugging.

## Reference(s):

- [Setup and reference](artifact/references/setup.md)
- [go-label-studio on GitHub](https://github.com/psyb0t/go-label-studio)
- [go-label-studio package documentation](https://pkg.go.dev/github.com/psyb0t/go-label-studio)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Go code and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.10.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
