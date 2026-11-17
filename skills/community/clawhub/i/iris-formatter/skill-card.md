## Description:

Formats, reviews, and proposes corrections for InterSystems IRIS/Cache ObjectScript code against rules for naming, SQL style, locking, transactions, comments, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review, format, score, and produce corrected InterSystems IRIS/Cache ObjectScript code. It is aimed at code quality work where the target technology and desired review or formatting outcome are clear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad file search, file write, and command execution authority for a formatter/reviewer workflow.

Mitigation: Use it only in trusted repositories, review proposed edits before applying them, and allow command execution only when the command and its inputs are understood.

Risk: Automatic formatting and correction can introduce incorrect ObjectScript changes or misleading review results.

Mitigation: Review generated changes, run project tests or IRIS compilation checks, and treat quality scores as advisory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/iris-formatter)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with review findings, corrected ObjectScript code blocks, and JSON-style scoring summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include complete corrected code, quality scores, improvement suggestions, and environment configuration guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 3.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
