## Description:

Formats, reviews, and proposes corrections for InterSystems IRIS/Cache ObjectScript code against naming, locking, transaction, comment, SQL, and style rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review IRIS/Cache ObjectScript, identify convention and quality issues, and generate corrected code with explanations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad command and file-editing authority for a formatter.

Mitigation: Use it only in trusted IRIS/ObjectScript repositories, review proposed file changes before applying them, and restrict shell commands to a clear user-approved list.

Risk: Automatic code correction can introduce incorrect or unintended behavior.

Mitigation: Review the full generated code or diff, run project tests where available, and keep a recoverable copy of the original code before accepting edits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/iris-formatter-free)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, guidance]

**Output Format:** [Markdown with corrected code blocks, review findings, and optional JSON-style summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose complete rewritten ObjectScript files and explain each correction.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
