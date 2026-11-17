## Description:

Pre-screens submitted text or local documents for repeated or highly similar passages, originality score, flagged segments, and optional paraphrasing suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run a local originality pre-check on text or document content before review, submission, or revision. It helps identify duplicate-pattern segments and generate rewrite suggestions, but it is not a comprehensive plagiarism search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The report can include excerpts from the analyzed document and may expose sensitive text if written to a shared location.

Mitigation: Run the skill in an isolated workspace and choose output paths deliberately for each analysis.

Risk: The checker performs local duplicate-pattern analysis and cannot confirm plagiarism against external databases or internet sources.

Mitigation: Use results as a pre-screen only and send important cases to manual review or a comprehensive plagiarism service.

Risk: A provided output path can overwrite an existing writable file.

Mitigation: Write reports to a new or disposable path and inspect existing files before using --output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/plagiarism-checker-pre-screener)
- [Algorithm Technical Documentation](references/algorithm.md)
- [Paraphrasing Guide](references/paraphrasing_guide.md)

## Skill Output:

**Output Type(s):** [text, json, markdown, shell commands, guidance]

**Output Format:** [JSON report or plain-text report with originality score, flagged segments, similarity scores, matching segment indexes, summary, and optional paraphrasing suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a report file when an output path is provided; local analysis only and no external source corpus lookup.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
