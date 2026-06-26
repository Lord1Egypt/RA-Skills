## Description: <br>
HengshuiClaw activates a pressure-style persistence mode for AI coding agents that escalates through retry strategies when the agent is tempted to give up. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serein431](https://clawhub.ai/user/serein431) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to make a coding agent persist through failures, change strategies after unsuccessful attempts, and return a useful partial result or diagnostic when full completion is blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally increases agent persistence and uses pressure-style language, which may be unsuitable when stopping, refusing, or acknowledging uncertainty is the safer response. <br>
Mitigation: Install only when this behavior is desired, use clear stop language when continued attempts are not useful, and avoid relying on the skill for tasks where safety refusals, expert referral, or plain uncertainty are more important than persistence. <br>


## Reference(s): <br>
- [PER-T Techniques Reference](references/techniques.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include retry plans, diagnostics, partial solutions, and handoff notes depending on the active task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
