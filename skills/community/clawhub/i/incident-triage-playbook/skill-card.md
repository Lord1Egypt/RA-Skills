## Description:

Runbook-first incident triage workflow for service outages and high-error alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiarani](https://clawhub.ai/user/jiarani)

### License/Terms of Use:


## Use Case:

Operations teams and on-call engineers use this skill to run a consistent first-15-minute triage flow for service outages and high-error alerts, including intake, timeline capture, ownership, checklist execution, and incident reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The playbook references triage and workflow commands that may not exist in the installer's environment.

Mitigation: Verify that the referenced commands are available and mapped to local incident-management procedures before relying on the skill during an incident.

Risk: A healthcheck script reports a different skill label than the incident triage playbook.

Mitigation: Use the skill frontmatter, release metadata, and file hashes as the authoritative identity signals, and update local healthcheck expectations before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiarani/skills/incident-triage-playbook)
- [Operations checklist template](templates/checklist.md)
- [Incident summary report template](templates/report.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with command examples and reusable incident checklist and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts only echo version and healthcheck status.]

## Skill Version(s):

1.2.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
