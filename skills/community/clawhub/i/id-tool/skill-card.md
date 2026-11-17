## Description:

Reports local user and group identity information for permission debugging and process security context checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to inspect a process's local user and group identity while debugging permissions or security context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation overstates the bundled helper's compatibility with the Unix id command and may imply unsupported options.

Mitigation: Treat the skill as a minimal identity-reporting helper and verify required option support before relying on it in operational workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/id-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text identity output with concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports local operating-system identity information; documented option coverage may exceed the bundled helper implementation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
