## Description:

Formats, quality-checks, and lightly standardizes Chinese official documents according to GB/T 9704-2012, producing Word documents and review reports for user-provided drafts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External users and office-document operators use this skill to format Chinese official-document drafts into GB/T 9704-2012-style DOCX files, inspect existing DOCX files for format issues, and standardize surface-level wording when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Style-cleaning suggestions could change or obscure intended meaning if accepted without review.

Mitigation: Confirm flagged wording changes before accepting them, especially where the report marks content for human review.

Risk: Runtime behavior depends on Python document-processing packages that may vary across environments.

Mitigation: Use a pinned or prebuilt Python environment for python-docx and pypdf when repeatable output matters.

Risk: Overwriting outputs can leave hidden timestamped backup files in the same directory.

Mitigation: Review and remove backup files when processing sensitive documents or sharing output folders.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/chesaram/skills/gongwen-format-pro)
- [GB/T 9704-2012 reference](artifact/references/gb9704-2012.md)
- [Quality-check checklist](artifact/references/qc-checklist.md)
- [Style-cleaning rules](artifact/references/style-guide.md)
- [CLI reference](artifact/references/cli-reference.md)
- [FAQ](artifact/references/faq.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Text, Configuration, Guidance]

**Output Format:** [DOCX files, Markdown reports, cleaned text files, JSON-compatible configuration, and concise user-facing status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts over user-provided documents; does not call external APIs according to artifact metadata.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and user-supplied target metadata; artifact frontmatter and manifest list 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
