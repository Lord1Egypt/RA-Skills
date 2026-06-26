## Description: <br>
Provides a reusable, evidence-backed workflow for development tasks with success criteria, checkpointing, quality gates, and implementation-ready next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xammarie](https://clawhub.ai/user/xammarie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to turn task inputs, constraints, and available artifacts into a concise plan, ranked findings, risks, mitigations, and concrete next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill name suggests flaky-test hunting, while the reviewed artifact behaves more like a broad planning and checklist workflow. <br>
Mitigation: Use it for structured development planning, and supplement flaky-test investigations with concrete CI triage steps such as reproduction loops, seed and time isolation, quarantine criteria, and verification commands. <br>
Risk: Planning outputs can be misleading if they are based on incomplete or weak task evidence. <br>
Mitigation: Apply the skill's quality gates: keep claims evidence-backed, state assumptions and tradeoffs, use checkpoints, and include fallbacks for risky work. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with ranked findings, action plans, risk mitigations, checklists, and commands where useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
