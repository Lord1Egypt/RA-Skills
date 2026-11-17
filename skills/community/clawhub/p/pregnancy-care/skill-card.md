## Description:

A comprehensive pregnancy care assistant that tracks gestational age, manages medical checklists, provides weekly updates, and offers personalized advice for multiple users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ginwu](https://clawhub.ai/user/ginwu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their support network use this skill through an agent to track pregnancy timing, manage prenatal milestone reminders, and receive role-aware pregnancy care guidance. Agents use the bundled scripts to calculate gestational age, maintain checklist state, and summarize current pregnancy context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive pregnancy-related information may be stored locally in plaintext.

Mitigation: Use only in environments where local plaintext storage is acceptable, restrict file access, and prefer secure storage before handling real personal data.

Risk: Pregnancy records may be retained after tracking stops.

Mitigation: Confirm storage and deletion behavior with the user, and delete or archive data only with explicit consent.

Risk: Multi-user tracking can expose data if user identifiers are reused or weakly isolated.

Mitigation: Use stable, per-user identifiers and review isolation behavior before deployment in shared agent environments.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and JSON returned by helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper scripts read and write local JSON state for pregnancy tracking and milestone reminders.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
