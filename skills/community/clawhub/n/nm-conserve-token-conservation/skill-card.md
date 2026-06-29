## Description: <br>
Enforces token quota management at session start with conservation and compression checks for session starts and large context loads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill at session start or before broad investigations to set token budgets, plan context reads, consider delegation, and decide whether compaction or a new thread is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make agents more conservative about file reads and context expansion, which may slow broad investigations. <br>
Mitigation: Use it when token budget matters and require explicit user approval before expanding beyond the planned read budget. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-conserve-token-conservation) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/conserve) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with checklist items and concise next actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces token budgeting, context planning, delegation, compression, and logging guidance; does not install code or run commands.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
