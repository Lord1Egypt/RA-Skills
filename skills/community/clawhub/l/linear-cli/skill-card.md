## Description: <br>
Linear CLI skill for OpenClaw workflows, powered by Api2Cli (a2c) against Linear's GraphQL API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonvanlaak](https://clawhub.ai/user/simonvanlaak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to run Linear issue, project, comment, and workflow-state operations from an agent-accessible CLI backed by Linear's GraphQL API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Linear API key and can access or modify Linear workspace data through supported commands. <br>
Mitigation: Use the least-privileged Linear token available, avoid sharing the key in chat or logs, and review commands before allowing changes to issues, projects, comments, or workflow states. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simonvanlaak/linear-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a2c on PATH and a Linear API key in LINEAR_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
