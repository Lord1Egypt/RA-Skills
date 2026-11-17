## Description:

Generate polished, read-only business reports from CSV/XLSX into static deliverables (xlsx+pdf+pptx) using ReportStudio Community.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xutianliang77-create](https://clawhub.ai/user/xutianliang77-create)

### License/Terms of Use:


## Use Case:

Employees and business analysts use this skill to convert local CSV or XLSX data into professional XLSX, PDF, and PPTX reports with data-supported trends, KPI summaries, and TopN breakdowns. Agents should use it when a user provides a spreadsheet path and asks for monthly, weekly, operational, or management reporting deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports may contain business-sensitive summaries from the selected CSV or XLSX input files.

Mitigation: Review generated XLSX, PDF, and PPTX outputs before sharing them outside the intended audience.

Risk: The local ReportStudio module reads user-selected spreadsheet files and writes report artifacts, usually under ./artifacts.

Mitigation: Run the skill only on intended input files and confirm the output directory before execution.

## Reference(s):

- [Acceptance checklist](references/acceptance.md)
- [ClawHub skill page](https://clawhub.ai/xutianliang77-create/skills/openclaw-reportstudio-community)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [JSON summary with generated XLSX, PDF, and PPTX files plus a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports are read-only static deliverables, usually written under ./artifacts; warnings identify insufficient history, unrecognized fields, or truncated trend exports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
