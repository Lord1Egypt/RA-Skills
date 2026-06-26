## Description: <br>
Multi-agent adversarial verification with convergence loop. Two independent review agents must both pass before output ships. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and operators use this skill to add an adversarial review gate before publishing, deploying, or shipping user-facing output. It is intended for high-stakes work where accuracy, completeness, compliance, or brand constraints need independent review before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague or subjective review rubrics can lead to inconsistent reviews, unnecessary fix loops, or weak approvals. <br>
Mitigation: Define objective pass/fail criteria for each review, cap the number of iterations, and escalate unresolved issues to a human reviewer. <br>
Risk: Review logs may contain the original task content and generated output. <br>
Mitigation: Handle review records according to the sensitivity of the source task and avoid retaining unnecessary content. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangxiaofei860208-source/lobster-santa-method) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with structured review JSON examples and workflow pseudocode] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no installed code, secrets, or hidden behavior reported by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
