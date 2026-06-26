## Description: <br>
Hybrid development workflow: local model plans, Copilot codes, local model validates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangyoumo](https://clawhub.ai/user/wangyoumo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure iterative product development across local-model planning, Copilot implementation, and local-model validation. It helps produce requirements, task packs, implementation notes, test coverage review, defect lists, and release recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and phase outputs may include credentials, private keys, customer data, or confidential project details if pasted into Copilot or saved in artifacts. <br>
Mitigation: Review and redact sensitive information before sharing prompts, task packs, logs, or phase outputs with any assistant or repository. <br>
Risk: The skill may activate more often than intended in general development conversations. <br>
Mitigation: Use it explicitly for hybrid workflow, phase-a, phase-b, phase-c, task-pack, Copilot handoff, or validation tasks. <br>


## Reference(s): <br>
- [Hybrid Dev on ClawHub](https://clawhub.ai/wangyoumo/hybrid-dev) <br>
- [Publisher profile](https://clawhub.ai/user/wangyoumo) <br>
- [Execution checklist](checklists.md) <br>
- [Customer registry prompt suite](prompts/customer-registry.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance and prompt outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses three phase output directories for planning, implementation handoff, and validation artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
