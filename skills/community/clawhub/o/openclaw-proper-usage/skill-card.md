## Description: <br>
Operate OpenClaw reliably with right skill/tool selection, scoped execution, and verification-first completion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcdoolz](https://clawhub.ai/user/mcdoolz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route OpenClaw work to the right tool, split broad tasks into scoped execution streams, and close each task with evidence-backed verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs agents to use named external model backends and scoped subagent sessions, which can affect quota, cost, and delegation behavior. <br>
Mitigation: Confirm the intended OpenClaw environment, model access, and delegation scope before installation or use. <br>
Risk: Routing guidance may lead an agent to choose an unsuitable tool for ambiguous, broad, or risky tasks. <br>
Mitigation: Follow the skill's clarify, scope, verify, and report workflow before making edits or accepting delegated outputs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational routing and completion guidance; it does not generate executable code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
