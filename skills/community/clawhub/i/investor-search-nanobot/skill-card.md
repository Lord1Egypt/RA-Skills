## Description:

Builds sourced investor lists for a chosen market, checks investor identity and duplicates, and delivers an Excel workbook with an honest account of coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bcpp](https://clawhub.ai/user/bcpp)

### License/Terms of Use:

MIT-0

## Use Case:

Fundraising teams, deal sourcers, and investor researchers use this skill to find and verify family offices, venture capital and private equity firms, and angel investors in a market, or to enrich an existing investor list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Investor research is stored persistently in the agent workspace.

Mitigation: Use a separate workspace per team or user and control access to stored research files.

Risk: The generated workbook may be posted automatically to the current chat, including shared channels.

Mitigation: Review the destination and workbook contents before using the skill in a shared or public chat.

Risk: Installing the latest available release may introduce unreviewed changes.

Mitigation: Prefer a pinned installer version and review updates before deploying them.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bcpp/skills/investor-search-nanobot)
- [Publisher website](https://www.bcpp.io)
- [File and field definitions](references/files.md)
- [Workspace and delivery guidance](references/environment.md)
- [Research reporting guidance](references/report.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Guidance]

**Output Format:** [Excel workbook (.xlsx) with sourced investor records and research sheets, plus a brief status report; CSV text as a last resort]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps research files in the agent workspace for subsequent runs; may attach the workbook to the current chat.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; SKILL.md lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
