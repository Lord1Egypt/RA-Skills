## Description:

Stores epidemiology study designs, statistical methods, concepts, and paper table layouts from paper-analysis sessions in a local SQLite knowledge base with duplicate prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chircken891](https://clawhub.ai/user/chircken891)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers and analysts use this skill to preserve research-method notes from paper analysis in a structured local repository. It captures study designs, statistical methods, epidemiology concepts, and table-layout conventions, prompts for missing details, and reports what was added or skipped.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research-method notes and paper-analysis details are retained on disk in a local SQLite database.

Mitigation: Use the skill only when local retention is acceptable, and avoid saving confidential, proprietary, or unpublished material unless the database path and access controls are appropriate.

Risk: Incomplete session context can produce sparse or uncertain database records.

Mitigation: Prompt the user for missing fields before insertion and mark unknown values as needing supplementation rather than presenting them as complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chircken891/skills/method-repository)
- [OpenClaw ClawHub homepage](https://github.com/openclaw/clawhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files]

**Output Format:** [Markdown summary with database updates and SQL/Python insertion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists selected analysis details to a local SQLite database and reports added, skipped, and total record counts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
