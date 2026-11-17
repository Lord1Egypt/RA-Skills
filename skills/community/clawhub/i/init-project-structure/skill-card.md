## Description:

Use when starting a new project from scratch and the user wants the full plan/build/recap/document workflow scaffolded.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adelvillar1](https://clawhub.ai/user/adelvillar1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize a new project with agent memory, local secret placeholders, documentation contracts, and plan/recap workflows. It is intended for greenfield projects or existing codebases that need a structured methodology scaffold.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CLAUDE.md content can shape future agent behavior and project workflow decisions.

Mitigation: Review CLAUDE.md before adopting it, with particular attention to branch, deployment, and staging conventions.

Risk: Project initialization can create or update files that become part of the repository.

Mitigation: Use the skill's pre-flight checks and overwrite prompts, then review generated files before committing.

Risk: Local credentials could be accidentally placed in tracked project files.

Mitigation: Keep credentials only in gitignored CLAUDE.local.md placeholders and do not add real secrets to tracked documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adelvillar1/skills/init-project-structure)
- [Publisher profile](https://clawhub.ai/user/adelvillar1)
- [CLAUDE template for 2-environment topology](artifact/references/CLAUDE-template-simple.md)
- [CLAUDE template for 3-environment topology](artifact/references/CLAUDE-template-full.md)
- [Technical documentation template](artifact/references/TECHNICAL-DOCUMENTATION-template.md)
- [Functional specifications template](artifact/references/FUNCTIONAL-SPECIFICATIONS-template.md)
- [Plans README template](artifact/references/docs-plans-README-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, directory scaffolding, shell commands, and concise implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project-level files and documentation templates; CLAUDE.local.md is intended to remain gitignored and contain placeholders only.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
