## Description:

Automate workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to invoke workflow automation tasks from a command-line workflow, configure the required API key, and receive JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow automation scope and API-key requirement are too vague for users to understand what access they are granting.

Mitigation: Review the skill before installing and do not provide a real API key until the publisher documents the service, data sent, and execution path.

Risk: The artifact references an automation script that is not supplied in the release evidence.

Mitigation: Require the publisher to supply the referenced script or explain how the execution path is provided before using the skill with credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-workflow-automation)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash examples and JSON result expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AUTOMATION_API_KEY environment variable; expected downstream result is JSON.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
