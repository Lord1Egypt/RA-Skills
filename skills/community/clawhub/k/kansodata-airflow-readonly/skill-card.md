## Description:

Helps an agent inspect Apache Airflow DAGs, DAG runs, and task instances through read-only REST API queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect Airflow workflow metadata, diagnose DAG run or task status, and keep investigations read-only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Airflow credentials could expose more metadata than intended if configured with broad permissions.

Mitigation: Use a read-only Airflow token with the narrowest practical scope before enabling the skill.

Risk: A misconfigured or untrusted Airflow plugin could return incorrect or unintended data.

Mitigation: Verify that the referenced Airflow plugin is the trusted plugin before configuring credentials.

Risk: Operational diagnosis can be misleading if DAG or run identifiers are guessed.

Mitigation: Use exact identifiers returned by read-only list operations and stop when authentication, configuration, or lookup errors occur.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kansodata/skills/kansodata-airflow-readonly)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary with brief lists and exact Airflow identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only read-only Airflow list operations and reports configuration or authentication errors without guessing.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
