## Description:

Generates and self-executes a diff-derived test plan for a PR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to validate pull request changes with area-specific checks, assess whether tests catch regressions, and summarize the resulting evidence before merge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanners rate the skill suspicious because it may handle contributor-controlled filenames unsafely, and a revert-test safety check may still alter existing changes.

Mitigation: Review proposed commands and file paths, confirm the working tree is clean, and preserve existing changes before running revert-tests.

Risk: The scan is partial because several local path-like references could not be resolved, so coverage is incomplete.

Mitigation: Review unresolved path references and the skill before relying on its checks.

## Reference(s):

- [ClawHub validate-pr release](https://clawhub.ai/athola/skills/nm-sanctum-validate-pr)
- [Project/plugin page (metadata homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown validation summary table with checks, evidence references, and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes proposed or executed verification commands and pass, fail, or inconclusive outcomes.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
