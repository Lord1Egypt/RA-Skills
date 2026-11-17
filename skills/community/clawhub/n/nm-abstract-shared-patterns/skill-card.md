## Description:

Provides reusable patterns for validation, error handling, testing, workflow structure, and shared skill scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as a reference library for consistent validation checks, error reporting, testing scaffolds, workflow templates, and reusable pattern maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code blocks and shell commands are templates and may be copied into real tooling without enough review.

Mitigation: Review, adapt, and test each snippet before use; keep generated validation and workflow code under normal code review.

Risk: The path-validation example is weak for production use.

Mitigation: Harden path validation against traversal, symlinks, and unexpected base directories before using it in real tools.

Risk: Broad trigger terms may load the skill in more contexts than intended.

Mitigation: Confirm the skill is relevant before applying its patterns, and avoid importing unused modules into an agent context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-shared-patterns)
- [OpenClaw homepage](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)
- [Validation Patterns](modules/validation-patterns.md)
- [Error Handling Patterns](modules/error-handling.md)
- [Testing Templates](modules/testing-templates.md)
- [Workflow Patterns](modules/workflow-patterns.md)
- [Advanced Pattern Composition](modules/advanced.md)
- [Creating a New Shared Pattern](modules/creation.md)
- [Editing an Existing Shared Pattern](modules/editing.md)
- [Troubleshooting Shared-Pattern Integration](modules/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code blocks, tables, checklists, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only reference patterns; example code and commands should be reviewed before reuse.]

## Skill Version(s):

1.9.19 (source: server release evidence; artifact frontmatter says 1.9.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
