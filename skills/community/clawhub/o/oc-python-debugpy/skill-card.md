## Description:

Debug Python with pdb, breakpoint(), post-mortem inspection, and debugpy remote attach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect Python state, diagnose exceptions and failing tests, and debug local, long-running, or remote processes with the smallest suitable debugger.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was incomplete because several referenced paths could not be assessed.

Mitigation: Review the referenced material before relying on the skill's debugging guidance.

Risk: A reachable debug listener can expose control of the attached process and its runtime state.

Mitigation: Bind debug servers to 127.0.0.1; use an isolated environment or tunnel if remote access is needed.

## Reference(s):

- [Python Debugpy on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-python-debugpy)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with inline Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
