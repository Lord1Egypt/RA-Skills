## Description: <br>
Transform raw brain dumps (dictated freestyle) into structured implementation artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skidvis](https://clawhub.ai/user/skidvis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to turn messy feature ideas, dictated notes, and scattered planning input into contracts, PRDs, implementation specs, and execution handoff guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect relevant project files while planning changes. <br>
Mitigation: Install only in workspaces where project-file review is acceptable, and avoid using it in repositories with secrets or sensitive business code unless that access is intended. <br>
Risk: Generated contracts, specs, and validation commands may contain incorrect or unsuitable implementation guidance. <br>
Mitigation: Review generated planning artifacts and commands before approving the plan or running any suggested validation steps. <br>
Risk: The skill writes planning documents under ./docs/ideation/. <br>
Mitigation: Review generated files before committing or sharing them, especially when planning work on private systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skidvis/openclaw-skill-ideation) <br>
- [Confidence assessment rubric](artifact/references/confidence-rubric.md) <br>
- [Contract template](artifact/references/contract-template.md) <br>
- [PRD template](artifact/references/prd-template.md) <br>
- [Implementation spec template](artifact/references/spec-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files and conversational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes planning artifacts under ./docs/ideation/{project-name}/ after confidence checks and user approvals.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
