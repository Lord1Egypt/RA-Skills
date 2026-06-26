## Description: <br>
Use when executing a written implementation plan in the current session with sequential task execution and review checkpoints when subagent-driven mode is not available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to execute written implementation plans sequentially when subagent-driven execution is unavailable or unnecessary. It guides the agent through plan review, task execution, validation checkpoints, and completion handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-impact administrative actions can affect agents, tokens, permissions, content, mail, or skill deletion. <br>
Mitigation: Install only for trusted ZenHeart L0/admin operators and confirm authorization rules, audit logging, recovery paths, and deployment runbooks before use. <br>
Risk: Credential exposure could compromise ZENLINK_TOKEN. <br>
Mitigation: Protect ZENLINK_TOKEN and restrict use to operators who understand the credential handling guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-executing-plans) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown guidance with task lists and inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include code edits, verification results, and concise status updates when used by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
