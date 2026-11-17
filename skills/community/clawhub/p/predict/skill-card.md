## Description:

Predict is a local forecasting helper for structuring trend forecasts, scenario planning, probability evaluation, and risk assessment with explicit uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[projectsnowwork](https://clawhub.ai/user/projectsnowwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to organize forecasts, scenarios, probability judgments, and decision risks while documenting assumptions and uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overstate its analytical depth relative to the bundled implementation.

Mitigation: Treat outputs as structured forecasting notes and checklists unless the missing analytical scripts are added and reviewed.

Risk: Forecasts and probability estimates may be misleading if users treat them as guaranteed predictions.

Mitigation: Document assumptions, uncertainty, and confidence levels, then update forecasts as new information becomes available.

Risk: The bundled forecast script writes forecast metadata to local storage.

Mitigation: Review locally retained forecast records and delete them according to the user's data retention needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/projectsnowwork/skills/predict)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text guidance with optional local JSON forecast records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the bundled forecast script is used, it records forecast metadata under ~/.openclaw/workspace/memory/predict.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
