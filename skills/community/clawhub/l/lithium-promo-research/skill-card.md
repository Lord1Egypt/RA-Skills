## Description:

Lithium Promo Research helps research trade shows, B2B platforms, and industry media for lithium battery equipment promotion across the United States, Japan, Korea, Russia, and Europe, then supports Excel dashboard report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardcoder849](https://clawhub.ai/user/richardcoder849)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, sales operations teams, and market researchers use this skill to compile candidate promotion channels for lithium battery equipment by country, platform type, and product line, and to generate Excel dashboard reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated spreadsheets may contain untrusted scraped or user-provided values, including formulas that could execute when opened in spreadsheet software.

Mitigation: Treat JSON input and scraped data as untrusted, sanitize values before spreadsheet generation, and review generated workbooks before sharing.

Risk: Report files are written to local output paths and may expose sensitive research data if placed in shared locations.

Mitigation: Use explicit output paths, restrict file permissions as needed, and confirm the destination before distributing generated reports.

Risk: The release evidence describes the helper as partly unfinished, so generated platform data and summaries may be incomplete.

Mitigation: Review the generated recommendations against source links and validate important platform, pricing, and contact details before business use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richardcoder849/skills/lithium-promo-research)
- [United States promotion guide](references/us.md)
- [Japan promotion guide](references/jp.md)
- [Korea promotion guide](references/kr.md)
- [Russia promotion guide](references/ru.md)
- [Europe promotion guide](references/eu.md)
- [Search templates](references/search-templates.md)
- [Product lines](references/product-lines.json)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON data files, text summaries, and Excel workbook reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate XLSX dashboard reports and intermediate JSON files for search tasks, parsed platforms, and scored platform recommendations.]

## Skill Version(s):

1.1.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
