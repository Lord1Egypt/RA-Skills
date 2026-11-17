## Description:

Rewrites Chinese articles into substantially rephrased Markdown while preserving the original meaning, improving readability, and optionally assessing similarity risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyzxs](https://clawhub.ai/user/pyzxs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content editors use this skill to transform source articles or article files into rewritten Chinese Markdown drafts while retaining the core information. It is intended for users who have rights to the source material and need readability, style, and similarity-risk review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is designed to rewrite articles to reduce similarity checks, which can enable copyright or attribution misuse.

Mitigation: Use only with source material the user has rights to, preserve appropriate attribution, and review output for copyright and platform-policy compliance before publication.

Risk: The workflow can read source files and write rewritten output files.

Mitigation: Approve exact input and output paths before execution and avoid granting broad filesystem access.

Risk: The artifact references helper skills for humanization and writing polish.

Mitigation: Review those helper skills independently before installing or allowing the workflow to depend on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pyzxs/skills/jl-content-rewriter)
- [AI humanizer reference](references/ai-humanizer.md)
- [Evaluation dimensions](references/evaluation-dimensions.md)
- [Principled review](references/principled-review.md)
- [Risk assessment](references/risk-assessment.md)
- [User command flow](references/user-command.md)
- [Word replacement](references/word-replace.md)
- [Writing polish](references/writing-polish.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown article content with optional Markdown status and similarity-risk report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a rewritten _final.md file near the source file or in a configured output directory; the artifact specifies preserving core meaning and keeping length within about 10%.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
