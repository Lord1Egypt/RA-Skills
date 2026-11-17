## Description:

Scans a specified directory and classifies files under the GB/T 35273 personal information security specification by matching filenames and supported file contents to sensitive or general personal-information categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkming1998](https://clawhub.ai/user/kkming1998)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance reviewers, and privacy operations teams can use this skill to scan directories for files that may contain sensitive or general personal information and to generate classification reports for review. It is useful for bulk privacy assessment, data labeling, and file-naming compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan reads filenames and, by default, supported file contents in the directory supplied by the user.

Mitigation: Run scans only on narrowly scoped directories and use --name-only when content access is not needed.

Risk: Automated keyword classifications can miss context or overstate sensitivity.

Mitigation: Treat results as review aids and manually verify sensitive classifications before making compliance or handling decisions.

Risk: CSV reports created from untrusted directory contents may carry spreadsheet-handling risk.

Mitigation: Open generated CSV files cautiously and review them with tools or settings appropriate for untrusted spreadsheet data.

Risk: Some file formats, including legacy .doc and PDF files, are not read for content by the bundled scanner.

Mitigation: Review unsupported formats manually or convert them to supported text-readable formats before relying on scan results.

## Reference(s):

- [GB/T 35273 classification rules](references/classification_rules.md)
- [ClawHub skill page](https://clawhub.ai/kkming1998/skills/mingshu-classifier)
- [ClawHub publisher profile](https://clawhub.ai/user/kkming1998)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scan results may be displayed as terminal text or written as CSV or JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include file path, file name, category, category name, matched keywords, keyword source, and suggested handling.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
