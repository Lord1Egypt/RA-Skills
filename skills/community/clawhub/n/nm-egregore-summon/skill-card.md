## Description: <br>
Autonomous orchestrator for manifest work items through the development lifecycle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to process manifest work items through intake, build, quality, and ship stages. It is intended for autonomous repository workflows that need stateful retries, budget handling, and resumable pipeline execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can take broad, persistent control over repository work. <br>
Mitigation: Install it only when autonomous repository orchestration is intended, review `.egregore` configuration before running, and prefer bounded mode for controlled runs. <br>
Risk: The workflow can resume itself through scheduled heartbeat or cooldown recovery prompts. <br>
Mitigation: Confirm scheduled prompts can be monitored and cancelled before use, and disable or remove the heartbeat when autonomous operation should stop. <br>
Risk: Pull requests may be merged with limited human checkpoints when auto-merge is enabled. <br>
Mitigation: Disable or tightly gate auto-merge, require human PR review, and use least-privilege GitHub credentials in a clean repository or worktree. <br>
Risk: The orchestrator proceeds through ambiguity instead of waiting for human input. <br>
Mitigation: Review the decision log and PR body before accepting changes, especially when requirements are incomplete or scope is unclear. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-egregore-summon) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [Project homepage from ClawHub metadata](https://github.com/athola/claude-night-market/tree/master/plugins/egregore) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands, configuration snippets, and skill invocation instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include repository workflow actions, manifest updates, branch and PR operations, scheduled resume prompts, and decision logs.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
