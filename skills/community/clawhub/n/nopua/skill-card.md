## Description: <br>
NoPUA coaches an agent to respond to repeated failures with persistent investigation, verification, and proactive completion rather than pressure or fear. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuji-labs](https://clawhub.ai/user/wuji-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to guide an AI assistant when it is stuck, repeatedly failing, or becoming passive. It emphasizes tool-based investigation, evidence-backed verification, and structured handoff when the boundary is reached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages persistent investigation and proactive tool use, which can exceed user expectations in sensitive repositories, production systems, or paid APIs. <br>
Mitigation: Set explicit boundaries before use, including when the agent must ask before destructive commands, broad searches, deployments, paid API calls, or long-running work. <br>
Risk: Repeated-failure coaching can lead to unnecessary continued work if the agent does not recognize when it has reached a real boundary. <br>
Mitigation: Require evidence-backed status reports, clear assumptions, and a structured handoff when the skill's stopping criteria are reached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuji-labs/nopua) <br>
- [Project homepage](https://github.com/wuji-labs/nopua) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown] <br>
**Output Format:** [Markdown guidance with checklists and structured report templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only coaching skill; release security evidence reports no executable code, credential handling, persistence, or hidden install behavior.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
