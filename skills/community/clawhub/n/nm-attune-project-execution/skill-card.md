## Description:

Executes implementation plans with progress tracking, checkpoint validation, and quality gates. Use after planning is complete and tasks are ready to implement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after planning to carry out implementation tasks in dependency order, track progress, and check work against acceptance criteria and quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegation may share project context with external model providers without warning.

Mitigation: Review which providers receive project context and confirm that sharing is acceptable before using delegation.

Risk: The security scan was incomplete because some referenced paths were missing from the bundle.

Mitigation: Review the complete release contents and rescan before deployment.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Code and text, including Markdown reports, shell command examples, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output depends on the implementation plan and may include progress and checkpoint reports.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
