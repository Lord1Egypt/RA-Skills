## Description:

Reviews outpatient chronic disease materials for diabetes or hypertension from OCR or document inputs and produces an internal medical model assessment with a structured JSON decision and natural-language rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Insurance and healthcare operations teams use this skill to review submitted chronic disease materials for diabetes or hypertension and summarize whether the provided records support the requested outpatient chronic disease review. The output is administrative review support and not a medical diagnosis or treatment recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw medical records and bearer tokens can be sent to a configurable model endpoint.

Mitigation: Use only authorized data, pre-redact patient identifiers before use, and keep --base pinned to a trusted HTTPS endpoint.

Risk: Sensitive raw JSON, text summaries, or prepared OCR arrays can be written to disk.

Mitigation: Write outputs only to a private controlled directory, avoid --save-prepared unless needed, and remove retained files according to local data-handling policy.

Risk: Administrative review results could be mistaken for clinical judgment.

Mitigation: Treat the output as review support only and defer clinical diagnosis or treatment decisions to qualified medical professionals.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/med-chronic-disease-review)
- [Default internal medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Structured JSON response plus natural-language text summary, with command output that reports saved file paths and a preview.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run validation; normal execution writes raw JSON and text summary files to the configured output paths.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
