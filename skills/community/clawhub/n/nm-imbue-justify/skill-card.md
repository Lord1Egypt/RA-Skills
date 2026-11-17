## Description:

Audits changes for additive bias and Iron Law compliance

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Justify after implementation and before committing or opening a pull request to assess whether each change was necessary, minimally scoped, and consistent with tests and design invariants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is partial because some referenced files were not included in the package.

Mitigation: Check whether the missing references matter to your use, and review the skill contents before installing.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-imbue-justify)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown justification report with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
