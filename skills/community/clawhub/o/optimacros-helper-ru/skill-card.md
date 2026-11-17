## Description:

Provides Russian-language assistance for Optimacros formulas, model design, access controls, scripts, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qmaijo](https://clawhub.ai/user/qmaijo)

### License/Terms of Use:

MIT-0

## Use Case:

Optimacros modelers, administrators, and implementation consultants use this skill to draft and review formulas, design model structures, reason about access controls, and evaluate script automation choices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advises on Optimacros access rights, DCA, scripts, exports, and service accounts; incorrect application could expose data or disrupt a real model.

Mitigation: Review proposed permission or automation changes with an Optimacros model owner before applying them, especially in production models.

Risk: Formula and modeling suggestions may depend on model-specific dimensions, versions, time settings, and confirmed Optimacros behavior.

Mitigation: Validate formulas and structural changes in a test view or non-production copy before deploying them broadly.

Risk: Guidance covers integration scripts that may interact with FTP, DWH, OLTP, or external databases.

Mitigation: Use least-privilege service accounts, separate secrets management, resource limits, and appropriate script locking for integration automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qmaijo/skills/optimacros-helper-ru)
- [Skill instructions](artifact/SKILL.md)
- [Optimacros formulas notes](artifact/optimacros-formulas-notes.md)
- [Optimacros model objects notes](artifact/optimacros-model-objects-notes.md)
- [Optimacros scripts, access, and security notes](artifact/optimacros-scripts-access-security-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Russian-language Markdown guidance with inline Optimacros formulas and occasional JavaScript or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory responses should be checked against the user's Optimacros model, permissions, and platform documentation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
