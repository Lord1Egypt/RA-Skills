## Description: <br>
Compare health insurance plans, estimate total yearly costs, and choose coverage that fits medical usage, prescriptions, and financial risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to compare health insurance options, model yearly costs across utilization scenarios, and prepare enrollment or renewal decisions with clear trade-offs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may handle sensitive health, prescription, provider, budget, or insurance decision details in local memory. <br>
Mitigation: Ask for explicit approval before writing memory, store only durable decision context, and avoid IDs, policy numbers, payment details, or unredacted confirmations unless the user can protect them securely. <br>
Risk: Insurance recommendations can be wrong if plan documents, provider network status, formularies, deadlines, or user assumptions are incomplete or outdated. <br>
Mitigation: Label assumptions, verify plan IDs, provider network fit, medication coverage, effective dates, and enrollment confirmations against authoritative plan materials before treating a recommendation as final. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/health-insurance) <br>
- [Skill Homepage](https://clawic.com/skills/health-insurance) <br>
- [Comparison Checklist](comparison-checklist.md) <br>
- [Cost Model](cost-model.md) <br>
- [Coverage Framework](coverage-framework.md) <br>
- [Enrollment Playbook](enrollment-playbook.md) <br>
- [Memory Template](memory-template.md) <br>
- [Setup](setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured checklists, cost calculations, recommendations, and optional shell commands for local setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; optional local memory is written only after explicit user approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
