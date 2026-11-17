## Description:

Generate monthly and annual operations reports from IMRC system data and Meixin message context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Operations analysts and developers use this skill to collect IMRC project, budget, contract, investment, risk, and message data and generate structured Markdown reports for monthly or annual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to collect internal business data and Meixin message content.

Mitigation: Use it only with authorization for the relevant IMRC pages and messages, and apply retention and redaction rules before processing personal or confidential communications.

Risk: Generated KPI, personnel, and project statements may be misleading because report values can be hard-coded or sample-derived.

Mitigation: Treat generated statements as untrusted until hard-coded values are replaced with validated calculations from source data.

Risk: Collected data and generated reports are stored locally.

Mitigation: Store outputs in controlled workspaces, restrict access to generated files, and remove local data that is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/imrc-report)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)
- [IMRC page configuration](artifact/config/pages.json)
- [Report template](artifact/config/report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with JSON intermediate data and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON data files under memory/imrc_data and Markdown reports to a requested output path.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
