## Description: <br>
Spawn and manage sub-agents with precise prompts, track their progress, and optimize outcomes using layered prompt design and SkillBoss API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to design structured prompts for research, build, and review sub-agents, track active agent work, and route selected prompts through SkillBoss API Hub when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to use a sensitive SkillBoss API key. <br>
Mitigation: Use a least-privilege key, store it only in the environment, and rotate or revoke it if exposed. <br>
Risk: Selected prompts may be sent to the third-party SkillBoss API Hub. <br>
Mitigation: Do not send confidential repository, customer, credential, or regulated data unless that transfer is approved. <br>
Risk: The skill can guide agents to create or modify project files and tracking notes. <br>
Mitigation: Constrain work to a designated workspace and require human review before writes outside that scope. <br>
Risk: The skill can guide agents to run local code or shell commands. <br>
Mitigation: Review generated commands before execution and run them with least-privilege local permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/martin-agent-orchestration) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with prompt templates, tracking tables, code examples, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference SKILLBOSS_API_KEY for optional SkillBoss API Hub calls.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
