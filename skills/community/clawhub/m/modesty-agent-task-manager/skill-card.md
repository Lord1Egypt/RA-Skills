## Description: <br>
Manages and orchestrates multi-step, stateful agent workflows; handles task dependencies, persistent state, error recovery, and external rate-limiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow builders use this skill to define, parse, and run multi-step agent workflows with task dependencies, resumable local state, rate-limit handling, and optional SkillBoss-powered reasoning or notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task content can be sent to the SkillBoss API Hub and notifications can be delivered externally. <br>
Mitigation: Use a least-privilege SkillBoss API key, avoid secrets or private business data in task requests, and confirm recipients before enabling notifications. <br>
Risk: Workflow state can be persisted locally in task_state.json and cooldown timestamp files. <br>
Mitigation: Run the skill in a controlled workspace and inspect or delete local state files after use. <br>
Risk: cooldown.sh can execute wrapped shell commands with weak safeguards. <br>
Mitigation: Do not use it with untrusted task names or command arguments unless the eval behavior is removed or replaced. <br>


## Reference(s): <br>
- [Task Structure Schema](references/task_schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-agent-task-manager) <br>
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell scripts, JSON task definitions, and command-line output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; may persist task_state.json and cooldown timestamp files during use.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
