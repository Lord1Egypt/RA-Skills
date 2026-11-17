## Description:

Koyomi Behavior guides agents to communicate clearly, base conclusions on evidence, verify work before making claims, and avoid vague or unsupported assertions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yl11023](https://clawhub.ai/user/yl11023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make an assistant stricter about validating results, stating evidence, and giving clear conclusions before claiming a task is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has a broad trigger and may alter routine assistant tone or impose Chinese/Kaguya-style wording conventions.

Mitigation: Deploy it only where stricter verification behavior and the associated tone conventions are acceptable, and review outputs for user-facing fit.

Risk: The skill encourages command-based verification, which can add extra tool use or delay before conclusions.

Mitigation: Use it in workflows where evidence-backed completion claims are more important than terse responses, and keep high-impact actions subject to human confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yl11023/skills/koyomi-behavior)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Promotes independent verification before final conclusions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
