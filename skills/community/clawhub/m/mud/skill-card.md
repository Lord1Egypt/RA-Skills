## Description: <br>
Operate and maintain the persistent MUD agent for OpenClaw. Use when running MUD engine commands, smoke-testing mud state behavior, validating save/restore, diagnosing MUD data issues, or handling MUD deployment operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrew-goetz-com](https://clawhub.ai/user/andrew-goetz-com) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run local OpenClaw MUD engine commands, smoke-test state behavior, validate save and restore flows, diagnose data issues, and handle deployment operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local MUD game state when it runs engine commands. <br>
Mitigation: Verify the target mud-agent directory and database path before running commands, and use a demo campaign or explicit test database for smoke tests when live state should not change. <br>


## Reference(s): <br>
- [MUD on ClawHub](https://clawhub.ai/andrew-goetz-com/mud) <br>
- [MUD Commands](references/commands.md) <br>
- [MUD Ops Runbook](references/ops.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output from the MUD runner.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local MUD engine commands and print command results.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
