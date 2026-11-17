## Description:

Validates Markdown files in the workspace for broken local links, missing file references, and basic syntax issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanng-ide](https://clawhub.ai/user/wanng-ide)

### License/Terms of Use:


## Use Case:

Developers and documentation maintainers use this skill to scan workspace Markdown for broken local links, missing file references, and basic documentation consistency issues before release or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recursive scans may follow directory symlinks outside the requested workspace and read or report out-of-scope Markdown files.

Mitigation: Use the skill only on trusted workspaces, review scan targets before running, and prefer releases that skip symlinks or enforce root boundaries and recursion limits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wanng-ide/skills/markdown-linter)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript usage examples and JSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scan result reports total Markdown files, broken-link count, and issue details.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
