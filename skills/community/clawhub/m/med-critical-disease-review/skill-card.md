## Description:

Assesses structured inpatient medical records against 28 critical-disease insurance claim categories, calls a medical assessment API, and returns raw JSON plus a natural-language conclusion with evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Claims operations teams and developers use this skill to submit inpatient medical record data for critical-disease insurance review and produce a conclusion, reasons, and evidence for downstream review. The skill is an insurance-criteria assessment aid and is not a medical diagnosis or treatment tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill handles sensitive medical records and has misleading privacy and persistence claims.

Mitigation: Install only where operators are authorized to send records to the documented assessment service, and clarify de-identification, retention, endpoint allowlisting, credential handling, and output-file protections before using real patient data.

Risk: The skill stores raw API responses and natural-language assessment results as local files by default.

Mitigation: Use controlled output paths, restrict access to generated files, and avoid storing real patient data unless local storage controls are approved.

Risk: The assessment service requires an API credential for `Authorization: Bearer <LLM_API_KEY>`.

Mitigation: Provide credentials through an approved secret-handling process, avoid hard-coding keys, and limit access to authorized operators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/med-critical-disease-review)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Assessment service base URL](https://skills-medical.hivoice.cn)
- [Assessment API endpoint](https://skills-medical.hivoice.cn/api/v1/assessment/assess/{disease})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; runtime outputs are raw JSON and natural-language text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a disease identifier, an input medical-record artifact or JSON payload, and an API key for the assessment service.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
