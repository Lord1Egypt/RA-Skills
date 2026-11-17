## Description:

Guides developers in creating Claude Code skills using test-driven development and persuasion principles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to design and validate Claude Code skills through test-driven development, description writing, modular documentation, and deployment checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment guidance may overwrite an existing skill.

Mitigation: Inspect deployment targets and preserve or back up existing skill files before applying changes.

Risk: Testing advice may reuse real prompts or transcripts without a stated sanitization step.

Mitigation: Use synthetic examples where practical; otherwise remove identifying or confidential details and confirm the material is authorized for reuse.

Risk: The security analysis is incomplete because it reports missing referenced paths.

Mitigation: Resolve and review referenced files in the installed release before relying on its deployment or testing guidance.

## Reference(s):

- [TDD methodology](modules/tdd-methodology.md)
- [Description writing](modules/description-writing.md)
- [Progressive disclosure](modules/progressive-disclosure.md)
- [Validation](modules/validation.md)
- [Deployment checklist](modules/deployment-checklist.md)
- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with example code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task-dependent; may include a skill definition and supporting modules.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
