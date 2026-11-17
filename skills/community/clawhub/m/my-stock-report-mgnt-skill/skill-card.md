## Description:

my_stock_report_mgnt_skill helps agents archive and retrieve U.S. stock analysis report conclusions in a DingTalk multidimensional table through the dingtalk-ai-table integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canonxu](https://clawhub.ai/user/canonxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they explicitly request the analysis report multidimensional table or the skill name, so an agent can validate, archive, and query U.S. stock analysis report conclusions and document links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock analysis summaries and document links may be stored in the configured DingTalk base and sheet.

Mitigation: Confirm the DingTalk Base ID and Sheet ID before installation and use only a table approved for those report summaries and links.

Risk: Incorrect or incomplete report fields could create low-quality table records.

Mitigation: Require all six documented fields to be present and format-valid before inserting a record.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canonxu/skills/my-stock-report-mgnt-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown tables and structured field payloads for DingTalk table operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Insert records require six validated fields; query responses are filtered and presented as Markdown tables.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
