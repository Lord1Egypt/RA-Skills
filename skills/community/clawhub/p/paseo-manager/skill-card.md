## Description:

Routes requests from a dedicated Paseo entry workspace to a matching workspace and agent, reusing an existing agent or handing off to a newly created one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanickxia](https://clawhub.ai/user/yanickxia)

### License/Terms of Use:

MIT-0

## Use Case:

People using Paseo as a shared request entry point can use this skill to find the right workspace and route work to a suitable existing agent or prepare a handoff to a new one.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete because one local reference could not be resolved, and a benign verdict does not guarantee safety.

Mitigation: Check that the environment-provided Paseo references and capabilities are available before relying on a handoff, and review their behavior before use.

## Reference(s):

- [CLI fallback instructions](references/cli.md)
- [Paseo Manager on ClawHub](https://clawhub.ai/yanickxia/skills/paseo-manager)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands]

**Output Format:** [Markdown guidance and handoff briefings with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
