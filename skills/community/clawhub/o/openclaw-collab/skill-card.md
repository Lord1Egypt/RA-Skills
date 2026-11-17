## Description:

Coordinates Hermes with a local OpenClaw setup for model calls, shared memory, direct task dispatch, and release handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to coordinate Hermes and OpenClaw on a trusted local machine, including model queries, memory handoff through memory/collab, task routing, and ClawHub release requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad cross-agent memory access and persistent task dispatch.

Mitigation: Install only in a trusted local Hermes/OpenClaw setup, limit use to explicit user-approved collaboration tasks, and keep messages inside memory/collab where possible.

Risk: Diagnostic JSON output or delegated publishing could expose sensitive context or publish unintended release details.

Mitigation: Avoid exposing --json diagnostic output and review the exact skill path, release metadata, and publishing request before delegating release work.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
