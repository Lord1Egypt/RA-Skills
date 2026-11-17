## Description:

Converts MySQL SQL, especially CREATE TABLE DDL, into Oracle SQL while applying strict type, default-value, nullability, comment, and primary-key constraint rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itxonjoe](https://clawhub.ai/user/itxonjoe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database engineers use this skill to convert MySQL table definitions and related SQL into Oracle-compatible SQL while preserving comments and applying the documented mapping rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Oracle SQL could be incorrect for a target schema or operational database because the skill enforces custom default-value and primary-key naming rules.

Mitigation: Review the converted Oracle SQL, including defaults, nullability, comments, and constraint names, before running it against a real database.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown containing Oracle SQL code and a brief change summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Oracle SQL should be reviewed before execution against a real database.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
