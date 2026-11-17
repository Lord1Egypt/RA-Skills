## Description:

PDF 知识提取技能 converts PDF files into Markdown, repairs CJK spacing, adds YAML metadata, and extracts structured knowledge rules from standards documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linlannet](https://clawhub.ai/user/linlannet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, documentation engineers, and knowledge-management teams use this skill to convert trusted PDF standards or trusted PDF URLs into Markdown with metadata, then extract structured rules such as frequencies, thresholds, grades, periods, formulas, materials, and specifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes under-scoped remote fetching for PDF inputs.

Mitigation: Use only trusted local PDFs or trusted URLs, run in an isolated virtual environment, and avoid hosts with access to sensitive internal network services.

Risk: An undocumented utility reads a hard-coded OpenClaw workspace path.

Mitigation: Remove or disable decode_files.py unless that local workspace metadata utility is explicitly needed and reviewed.

Risk: Dependency behavior can change if packages are installed without version pins.

Mitigation: Pin and review dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linlannet/skills/pdf-skills)
- [README.md](artifact/README.md)
- [ioc-kms-dataset](https://gitee.com/linlannet/ioc-kms-dataset)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown files with YAML front matter, optional JSON or Markdown rule reports, and command-line guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Markdown filenames may include an extracted sequence number and standards identifier; extracted metadata can include source, document hash, page counts, scanned-page count, and character count.]

## Skill Version(s):

1.0.0 (source: release evidence; skill documentation also notes v1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
