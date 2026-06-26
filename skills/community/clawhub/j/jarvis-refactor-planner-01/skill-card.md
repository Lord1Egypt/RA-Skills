## Description: <br>
Plan low-risk refactors with seams, tests, and rollback points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xammarie](https://clawhub.ai/user/xammarie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical leads use this skill to turn refactoring goals and development artifacts into evidence-backed plans, risk-ranked findings, checklists, commands, and rollback-aware next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated refactoring plans or command checklists could be applied to production code without sufficient review. <br>
Mitigation: Review generated checklists and commands before use, especially for production code or irreversible changes. <br>
Risk: A plan may rely on incomplete artifacts or assumptions from the user-provided development context. <br>
Mitigation: Use the skill's quality gates to make assumptions explicit, require evidence-backed claims, and define fallback paths. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with concise summaries, ranked findings, action plans, risks, mitigations, and optional command checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exact checklists or commands where useful; generated plans should be reviewed before application.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
