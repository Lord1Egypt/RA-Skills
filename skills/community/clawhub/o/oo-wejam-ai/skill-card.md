## Description:

Use the OOMOL-connected Jam integration to export one page of training data for reporting or BI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use the OOMOL-connected account to export one page of Jam training data for reporting or BI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run unverified remote CLI code and automatically change agent skills.

Mitigation: Review and preinstall a vetted CLI release, and check automatic skill synchronization settings before use.

Risk: Exported data passes through OOMOL.

Mitigation: Connect Jam with the minimum necessary permissions and consider whether the exported data is appropriate for that workflow.

## Reference(s):

- [Jam data export API documentation](https://docs.wejam.ai/external/coach/help-and-reference/data-export-api)
- [Jam homepage](https://wejam.ai)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-wejam-ai)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Shell commands with JSON action responses and Markdown reporting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Exports one page of Jam training data per action.]

## Skill Version(s):

1.0.5 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
