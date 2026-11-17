## Description:

Transforms raw brain dumps, messy ideas, and planning notes into structured contracts and implementation specs under ./docs/ideation/{project-name}/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skidvis](https://clawhub.ai/user/skidvis)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to convert scattered feature ideas or dictated planning notes into reviewable contracts, PRDs, and implementation specs. It is intended for planning work that benefits from codebase exploration, confidence scoring, and explicit user approval before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads relevant project files to understand architecture and conventions.

Mitigation: Install only where project-file reading is acceptable, and review the scope of files used during planning.

Risk: The skill writes planning documents under ./docs/ideation/ that may guide later implementation work.

Mitigation: Review generated contracts, PRDs, and specs before approval or handoff to implementation.

## Reference(s):

- [openclaw-skill-ideation on ClawHub](https://clawhub.ai/skidvis/skills/openclaw-skill-ideation)
- [Confidence Assessment Rubric](references/confidence-rubric.md)
- [Contract Template](references/contract-template.md)
- [PRD Template](references/prd-template.md)
- [Spec Template](references/spec-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files and concise handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes planning artifacts under ./docs/ideation/{project-name}/ after user approval.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
