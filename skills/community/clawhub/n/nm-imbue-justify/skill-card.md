## Description: <br>
Audits changes for additive bias and Iron Law compliance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill after implementation work or before merging changes to audit diffs for additive bias, test mutation, unnecessary abstractions, and invariant changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic review-related prompts may activate the strict justification checklist when a narrower audit was intended. <br>
Mitigation: Use explicit triggers or narrower activation rules when installing the skill in environments that only need this audit on direct request. <br>
Risk: The skill proposes review judgments about code changes and may surface incorrect or overly strict recommendations. <br>
Mitigation: Have a human reviewer confirm the justification report and scan proposed changes before merging or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-justify) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/athola) <br>
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with inline shell commands and review tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a structured justification report covering additive-bias score, Iron Law compliance, change-by-change justification, risk assessment, and recommendations.] <br>

## Skill Version(s): <br>
1.9.13 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
