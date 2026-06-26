## Description: <br>
Evidence-based, approval-gated self-improvement workflow for OpenClaw. Use when the user asks to make OpenClaw or any project more reliable, faster, cheaper, safer, or higher quality with measurable before/after evidence. Ships helpers to scaffold a run directory, list and summarize past runs, compare two runs side-by-side, set artifact statuses, validate completeness, and export machine-readable JSON for CI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopendrasharma89-tech](https://clawhub.ai/user/gopendrasharma89-tech) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to run a metrics-first improvement loop for OpenClaw or another project, including baseline capture, hypotheses, approval packages, validation, outcome reporting, and CI-readable exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: UX feedback or usability-testing activities may collect participant information without enough privacy notice. <br>
Mitigation: Tell participants what is collected, why it is collected, where it will be stored, and how long it will be kept; avoid sensitive personal data unless strictly necessary. <br>
Risk: An improvement proposal or implementation run may produce incorrect guidance or regress project behavior. <br>
Mitigation: Use the skill's approval-gated modes, dry-run scaffolding, explicit validation gate, rollback plan, and run validation before treating a run as complete. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gopendrasharma89-tech/openclaw-self-improve) <br>
- [Improvement Playbooks](references/playbooks.md) <br>
- [Output Contract for OpenClaw Self-Improve](references/output-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown, json, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and generated Markdown/JSON run artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces structured improvement-run artifacts and optional CI-readable JSON summaries.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
