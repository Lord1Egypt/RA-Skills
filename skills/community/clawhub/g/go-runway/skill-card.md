## Description:

This skill helps Go developers use the unofficial typed go-runway client to call Runway's generation, task, and organization APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Go developers use this skill to integrate the typed go-runway client into a Go project for Runway generation, task polling, and organization account operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some references in SKILL.md could not be resolved in the security review.

Mitigation: Check the linked package and documentation references before installing.

Risk: Runway prompts, images, and other inputs sent by the client leave the local machine, and generation endpoints can spend organization credits or alter resources.

Mitigation: Send only inputs approved for Runway processing; run paid or destructive operations only when requested and only on resources the task created or named.

Risk: An API key could be exposed if it is hardcoded, committed, or logged.

Mitigation: Read the key from RUNWAYML_API_SECRET and never hardcode, commit, log, or print request headers.

## Reference(s):

- [Setup and reference](references/setup.md)
- [go-runway source repository](https://github.com/psyb0t/go-runway)
- [go-runway package documentation](https://pkg.go.dev/github.com/psyb0t/go-runway)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with Go code examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples cover client setup, API calls, and task polling; endpoint and model details can be looked up in package documentation.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
