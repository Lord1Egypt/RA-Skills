## Description:

Orchestrates and validates a QBO month-end close by reading client SOPs, running close checks, tracking progress, proposing journal entries, and producing a controller-ready Excel workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and accounting operators use this skill to run and rerun monthly close workflows for QBO-connected clients, validate close checklist items, and prepare controller review materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is intended to access QBO credentials and client financial data.

Mitigation: Run it only in an approved environment where those credentials and client records are expected to be available.

Risk: Dependency drift can change the behavior or security posture of the workbook generation path.

Mitigation: Install dependencies in a virtual environment and pin openpyxl to a reviewed version.

Risk: Some proposed journal entry amounts may be estimates or marked TBD.

Mitigation: Require controller review before posting or relying on proposed journal entries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/skills/month-end-close)
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash commands and file output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a controller-ready Excel workbook with close checklist, trial balance, proposed entries, and CDC log; some proposed journal entry amounts may be TBD pending review.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
