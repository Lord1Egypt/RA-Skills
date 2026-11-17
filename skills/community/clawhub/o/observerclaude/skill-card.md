## Description:

observerclaude is an embedded UX research observer for OpenClaw that logs interactions, surveys, friction and delight signals, token cost estimates, and daily research reports with charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[giulianomorse](https://clawhub.ai/user/giulianomorse)

### License/Terms of Use:


## Use Case:

OpenClaw users, product teams, and UX researchers use this skill to observe real assistant usage, collect structured interaction records and surveys, and produce periodic research reports. It is intended for environments where participants knowingly opt into broad local usage logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill continuously records and persists broad usage data, including verbatim user requests, which is too broad for default installation.

Mitigation: Enable it only for an intentional UX research study, review the ~/.uxr-observer/ data directory and retention behavior, and narrow collection or add pre-storage redaction before using it around confidential work.

Risk: Raw local logs and generated reports may contain sensitive work context before report redaction is applied.

Mitigation: Inspect report contents and redaction logs before sharing, use the documented pause and delete controls when collection is not appropriate, and avoid collecting sensitive sessions unless additional controls are in place.

Risk: Optional Google Docs or email delivery could disclose report contents outside the local environment.

Mitigation: Review any Google or email integration before enabling it, require explicit user-selected recipients, and confirm delivery only after the user verifies the report was sent as intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/giulianomorse/skills/observerclaude)
- [Publisher profile](https://clawhub.ai/user/giulianomorse)
- [Observation taxonomy](artifact/observation-taxonomy.md)
- [Observation record schema](artifact/observation.json)
- [Redaction rules](artifact/redaction-rules.md)
- [Report template](artifact/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON and JSONL records, PNG charts or text chart fallbacks, survey prompts, and local configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local observations, surveys, aggregates, heartbeat status, reports, charts, and redaction logs under ~/.uxr-observer/.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
