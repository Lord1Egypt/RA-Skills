## Description:

Generates Morgan Stanley-style equity research DOCX reports with structured sections, financial tables, and publication-grade charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjkj999999](https://clawhub.ai/user/yjkj999999)

### License/Terms of Use:

MIT

## Use Case:

External analysts, fund managers, and finance professionals use this skill to create sell-side research reports, buy-side investment memos, industry deep dives, earnings updates, valuation analyses, and related DOCX report packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or overwrite local DOCX files at the selected output path.

Mitigation: Confirm the destination path before running the CLI or API and review generated files before distributing them.

Risk: Reports may include private data, local image content, or draft financial analysis supplied by the user.

Mitigation: Use only intended inputs and avoid embedding private local images or confidential data unless the report is meant to contain them.

Risk: Morgan Stanley-style branding and disclaimer text could be misleading if shared externally without review.

Mitigation: Review and adjust branding, source labels, disclaimers, and financial claims before external publication.

## Reference(s):

- [Skill documentation](SKILL.md)
- [README](README.md)
- [Project link from README](https://github.com/yjkj999999/ms-research-report)
- [ClawHub skill listing](https://clawhub.ai/yjkj999999/skills/ms-research-report)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration]

**Output Format:** [DOCX files generated from Python API or CLI inputs, with Markdown and code guidance for agent use.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local Word documents and optional chart images during rendering; matplotlib charts degrade to text placeholders when matplotlib is unavailable.]

## Skill Version(s):

1.1.0 (source: server release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
