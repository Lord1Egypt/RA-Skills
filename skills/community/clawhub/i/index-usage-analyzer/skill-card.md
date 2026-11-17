## Description:

Analyzes database indexes and suggests redundant ones to remove for schema optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to inspect SQLite index metadata and identify indexes that may be redundant by naming pattern. It supports schema maintenance and performance review by producing analysis output without modifying the database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives deletion-style index recommendations from naming patterns that may be weak evidence for true redundancy.

Mitigation: Require database-owner review and stronger query/workload evidence before acting on any suggested index removal.

Risk: The analyzer writes recommendations to the fixed path /root/.schema/recommendation.json.

Mitigation: Run it without elevated privileges where possible and ensure downstream tooling treats the file as advisory input only.

Risk: The skill requires access to database schema metadata.

Mitigation: Use it only against databases where schema metadata access is authorized and appropriate.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, json, code, guidance]

**Output Format:** [JSON analysis report with a recommendation file path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes index-drop recommendations to /root/.schema/recommendation.json and prints a JSON report.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
