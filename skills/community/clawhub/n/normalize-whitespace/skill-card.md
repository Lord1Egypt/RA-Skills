## Description:

Normalize indentation of a large reference text document (e.g. README.md) to a consistent TAB style while keeping content byte-identical.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to normalize leading whitespace in large prose-heavy text documents while preserving content and protecting verbatim regions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally guides an agent to edit local text files, so incorrect target selection or unreviewed changes could alter a document unexpectedly.

Mitigation: Confirm the target file and indentation convention before writes, classify ambiguous lines with the user, run the whitespace-only integrity diff, and review the final diff before accepting changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/normalize-whitespace)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with inline shell commands and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill outputs a step-by-step editing and verification procedure; it does not include executable bundled code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
