## Description:

Extracts dates and concise event summaries from public Chinese news-list pages and returns an Excel-compatible CSV table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilimoss-china](https://clawhub.ai/user/lilimoss-china)

### License/Terms of Use:

MIT

## Use Case:

External users and operators use this skill to turn public institutional news roundups, activity lists, and monthly reports into two-column timelines for briefs, reports, or event records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided URLs may expose sensitive or access-controlled content if the skill is used outside public pages.

Mitigation: Use the skill on public, non-sensitive pages and avoid private, intranet, or credentialed URLs.

Risk: Spreadsheet values copied from source content can create formula-safety issues when cells begin with characters such as =, +, -, or @.

Mitigation: Sanitize formula-leading cell values before opening, sharing, or publishing generated CSV or spreadsheet files.

Risk: Irregular pages, image-only content, PDFs, or ambiguous dates can lead to missed rows or incorrect summaries.

Mitigation: Review generated rows against the source page and manually correct uncertain dates or summaries before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilimoss-china/skills/news-to-excel-skill)
- [Usage guide](artifact/usage.md)
- [FAQ](artifact/faq.md)
- [CSV to Excel helper script](artifact/generate_excel.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [CSV content, Markdown tables, and optional XLSX files generated from CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs use two columns: time and event summary; the helper script can convert UTF-8 CSV input to an XLSX workbook.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
