## Description:

Helps office workers draft reports and meeting notes, analyze local data, and track AI token usage and estimated time savings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Office workers and teams use this skill to create weekly reports, meeting notes, summaries, presentation outlines, and local data analyses. They can review token usage and estimated efficiency gains in a local ledger and report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads selected local files and can write reports or change the efficiency ledger.

Mitigation: Provide only intended file paths, preview ledger changes, and confirm writes only after reviewing them.

Risk: Optional host-usage import may read local usage traces.

Mitigation: Enable import only when needed and review which local usage files are selected.

Risk: Optional export packages can vary between installations.

Mitigation: Pin optional dependencies when reproducible document exports are needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/elisabeth15501/skills/office-token-booster)
- [Quickstart](artifact/QUICKSTART.md)
- [Host portability contract](artifact/docs/portability-contract.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Reports, Files, Guidance]

**Output Format:** [Text and Markdown; local reports in HTML or JSON, data in CSV, and optional DOCX or XLSX exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local processing; ledger updates require confirmation, and optional document exports require additional packages.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
