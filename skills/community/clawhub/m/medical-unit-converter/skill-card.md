## Description:

Convert medical laboratory values between units (mg/dL to mmol/L, etc.) with formula transparency and clinical reference ranges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to convert specific numeric medical laboratory values between recognized clinical unit systems and return transparent conversion results with reference-range context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference ranges may be mistaken for medical interpretation or advice.

Mitigation: Use the skill only for unit conversion and treat reference ranges as informational; require qualified clinical review for diagnosis, treatment, or interpretation.

Risk: Documentation does not fully match script behavior, including supported analytes and JSON field names.

Mitigation: Validate the actual supported analytes and output schema before relying on the skill in automated workflows.

Risk: NaN or infinite numeric values can undermine automated conversion workflows if accepted upstream.

Mitigation: Pre-validate inputs as finite numeric values before invoking the converter.

## Reference(s):

- [Medical Unit Converter References](artifact/references/guidelines.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON conversion results or concise Markdown fallback reports with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include converted values, source and target units, analyte names, and reference-range context when supported.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
