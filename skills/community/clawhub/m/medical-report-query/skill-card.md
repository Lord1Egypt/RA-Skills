## Description:

Medical Report Query helps agents query and summarize Oracle and SQL Server medical database reports for outpatient, inpatient, pharmacy, insurance, revenue, and operations reporting in clinics and community hospitals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a85012712](https://clawhub.ai/user/a85012712)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare operations staff and authorized analysts use this skill to request routine clinic and community-hospital reports from medical databases, including outpatient volume, inpatient occupancy, pharmacy inventory, insurance reconciliation, and fee analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward querying sensitive patient, billing, insurance, and pharmacy data.

Mitigation: Install it only where the agent has authorized, least-privilege access to the relevant medical databases, and require confirmation before database queries.

Risk: Generated reports or exports may expose protected identifiers or billing details.

Mitigation: Mask patient and billing identifiers by default, restrict exports, and apply healthcare privacy, audit, and recipient controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured report guidance, with optional SQL-oriented query assistance and report export guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be tailored for Markdown, Excel, or HTML; sensitive data should be masked by default.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
