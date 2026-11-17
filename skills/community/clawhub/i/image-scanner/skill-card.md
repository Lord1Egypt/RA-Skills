## Description:

Scans image folders to identify image formats, classify files by filename-based style cues, and produce a Chinese-language organization report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrxolin](https://clawhub.ai/user/mrxolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to scan local photography folders, summarize image formats and sizes, and classify images into broad style categories before organizing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is Chinese-language and may be harder for non-Chinese readers to review before acting on its report.

Mitigation: Install only if the operator is comfortable reviewing Chinese-language prompts and report output.

Risk: Future or optional classification behavior may organize files in bulk.

Mitigation: Run it first on a specific test folder and review the report and output path before using classification on important photo libraries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrxolin/skills/image-scanner)
- [Publisher profile](https://clawhub.ai/user/mrxolin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text console report with usage commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports image counts, formats, file sizes, modification times, and filename-derived style labels; current color analysis is reported as unknown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
