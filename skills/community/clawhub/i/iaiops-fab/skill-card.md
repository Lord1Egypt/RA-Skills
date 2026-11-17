## Description:

Provides fab engineers with read-first SECS/GEM and OPC UA workflows for equipment status, alarms, process data, downtime analysis, OEE, and data quality, with management-of-change controls for writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Fab equipment engineers and operations teams use this skill to inspect SECS/GEM and OPC UA equipment data, investigate downtime and alarms, assess OEE and data quality, and prepare configuration or evidence exports. Equipment writes follow the documented management-of-change approval workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write tools can change production equipment state.

Mitigation: Follow the documented management-of-change workflow: use the default dry run, retain the before-value for undo, and require a named approver's double confirmation. SIS endpoints reject equipment writes.

Risk: A benign scan does not guarantee zero risk; this release scan covered its single Markdown file, and executable-file checks were not applicable.

Mitigation: Review the skill and the site-specific equipment configuration before deployment, and keep production writes within the documented approval workflow.

## Reference(s):

- [Industrial-AIOps Fab on ClawHub](https://clawhub.ai/zw008/skills/iaiops-fab)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration, Files]

**Output Format:** [Text and structured findings, with configuration drafts and data or evidence exports when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first equipment findings; configuration drafts preserve unconfirmed values for human review.]

## Skill Version(s):

0.34.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
