## Description:

Collects official master's admissions information for Hong Kong universities, including tuition, dates, deadlines, English requirements, program details, and official links, and formats the results as Excel-compatible TSV, Word/PDF-compatible HTML, HTML, and Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Students, education consultants, and analysts use this skill to collect, compare, and format Hong Kong master's admissions data from official university sources. The generated reports support admissions research and planning, but should be verified against the official university pages before decisions are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated admissions reports can misstate official-source coverage or contain outdated tuition, deadline, requirement, or programme availability information.

Mitigation: Treat generated reports as drafts and verify all decision-relevant admissions details directly on official university pages.

Risk: Generated HTML reports may handle collected data unsafely or include unvalidated links.

Mitigation: Review and escape collected data, validate links, and avoid opening or hosting generated HTML until it has been checked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/hku)
- [Skill definition](SKILL.md)
- [Usage guide](README.md)
- [Data schema](skill/DATA-SCHEMA.md)
- [Collection prompt](skill/COLLECTION-PROMPT.md)
- [Full collection workflow](skill/workflows/full-collection.md)
- [HTML output template](skill/output-templates/html-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown, Excel-compatible TSV, self-contained HTML, and Word/PDF-compatible HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated admissions data should be treated as a draft and verified against official university pages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
