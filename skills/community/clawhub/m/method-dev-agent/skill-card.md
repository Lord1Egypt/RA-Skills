## Description:

Method Dev Agent helps pharmaceutical analysis labs manage chromatographic method development through experiment records, method retrieval, basic trend analysis, and local SQLite storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teagec](https://clawhub.ai/user/teagec)

### License/Terms of Use:


## Use Case:

Pharmaceutical analysis researchers, QC method-development scientists, lab managers, and CRO analytical teams use this skill to structure chromatography experiments, preserve method knowledge, and review basic development trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled publishing workflow can upload all unignored project files, including sensitive lab data, to a fixed GitHub remote without review.

Mitigation: Review the working copy and ignored files before publishing, and do not run publishing commands from a directory containing experiment databases, exports, credentials, .env files, or confidential lab records.

Risk: Local pharmaceutical or regulated laboratory records may contain sensitive data.

Mitigation: Use approved local environments, keep regulated data out of unapproved deployments, and follow applicable laboratory data-handling controls.

Risk: The paid offering references cryptocurrency payment.

Mitigation: Verify the payment recipient through an independent trusted channel before sending funds.

## Reference(s):

- [Method Dev Agent on ClawHub](https://clawhub.ai/teagec/skills/method-dev-agent)
- [Publisher profile: teagec](https://clawhub.ai/user/teagec)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with inline shell commands, configuration notes, and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local Streamlit and SQLite workflows for laboratory method-development records.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
