## Description:

Linear CLI skill for OpenClaw workflows, powered by Api2Cli (a2c) against Linear's GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simonvanlaak](https://clawhub.ai/user/simonvanlaak)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Linear workflows from an agent-accessible CLI surface, including reading issues, listing issues by team or project, adding comments, and setting workflow state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a Linear API key and advertises issue-changing commands while the package lacks the referenced wrapper and Api2Cli configuration needed to verify behavior.

Mitigation: Review before installing or using; do not provide a Linear API key until the missing wrapper and Api2Cli configuration are present and inspectable, and use a key scoped only to the intended Linear reads, comments, and workflow-state changes.

## Reference(s):

- [ClawHub Linear CLI skill page](https://clawhub.ai/simonvanlaak/skills/linear-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a2c on PATH and a Linear API key in LINEAR_API_KEY.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
