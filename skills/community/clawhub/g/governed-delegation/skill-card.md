## Description: <br>
Policy-guided governed delegation for subagent use, including decisions about whether to delegate, which model tier is allowed, whether execution must fail closed, and how to build an auditable spawn request for critical or deterministic work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joaodriessen](https://clawhub.ai/user/joaodriessen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when a task may require subagents and they need a governed execution envelope before spawning delegated work. It helps classify risk, choose an allowed model tier, decide whether to fail closed, and produce a decision or spawn request that can be audited. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper depends on a local OpenClaw policy module for canonical routing decisions. <br>
Mitigation: Confirm the target OpenClaw environment includes the expected policy module before relying on generated delegation decisions. <br>
Risk: Delegated prompts may include secrets or private data that could be handed to subagents or external model providers. <br>
Mitigation: Keep secrets and private data out of delegated prompts, and review the generated spawn request before execution. <br>
Risk: Strict or critical work can be unsafe if a requested front door does not match canonical policy. <br>
Mitigation: For Class C, Class D, or critical-write work, include an explicit front door and fail closed when the helper rejects the requested route. <br>


## Reference(s): <br>
- [Governed Delegation on ClawHub](https://clawhub.ai/joaodriessen/governed-delegation) <br>
- [Canonical model-routing policy referenced by the skill](docs/MODEL_ROUTING_POLICY.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON decision object with optional shell command usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper reads a JSON task classification from an argument or stdin and prints a governed delegation decision, including model, fail-closed status, policy source, runner, front-door status, and an optional spawn request envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
