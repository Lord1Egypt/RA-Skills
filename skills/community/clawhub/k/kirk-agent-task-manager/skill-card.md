## Description: <br>
Manages multi-step, stateful agent workflows with task dependencies, persistent state, error recovery, notification delivery, and external rate-limit handling through SkillBoss API Hub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create persistent, multi-step workflows that can resume after interruption, coordinate role-specific actions, parse human task requests, and send notifications through SkillBoss. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow descriptions, prompts, notification recipients, and notification content may be sent to SkillBoss. <br>
Mitigation: Install only if SkillBoss is trusted for that data, avoid sending sensitive task content unnecessarily, and review notification recipients before use. <br>
Risk: The release requires a SkillBoss API key. <br>
Mitigation: Keep the API key protected, scope and rotate it as appropriate, and avoid committing it to source control or shared logs. <br>
Risk: The cooldown wrapper executes dynamic command text through eval. <br>
Mitigation: Do not pass untrusted or user-controlled command text to cooldown.sh unless it is patched to avoid eval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/kirk-agent-task-manager) <br>
- [SkillBoss Setup Guide](https://skillboss.co/skill.md) <br>
- [Task Structure Schema](references/task_schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell scripts, JSON task definitions, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and may create local task_state.json and agent_task_manager_data files during execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
