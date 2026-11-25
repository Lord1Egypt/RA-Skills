## Description:

Prepares pull requests by running quality gates, drafting descriptions, and validating tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers preparing a change for review use this skill to check repository state, run project quality gates, summarize changes and tests, and draft a grounded pull request description.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some local references were unresolved during partial security scanning, leaving evidence about them incomplete.

Mitigation: Review unresolved references and confirm their guidance fits the target project before relying on it.

Risk: Suggested checklists, output guidance, and example commands may not fit every repository or environment.

Mitigation: Check the proposed steps and commands against the target project's requirements before running them.

## Reference(s):

- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown pull request description with command examples and test plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a facts table, change summary, test plan, and checklist.]

## Skill Version(s):

1.10.4 (source: server release evidence; artifact frontmatter says 1.10.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
