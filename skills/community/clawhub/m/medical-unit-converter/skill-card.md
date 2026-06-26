## Description: <br>
Convert medical laboratory values between units with formula transparency and clinical reference ranges for supported analytes including glucose, cholesterol, creatinine, and hemoglobin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, clinical documentation teams, and developers use this skill to convert supported laboratory values between common clinical unit systems and return reference-range context for review. It is intended for unit conversion and education, not diagnosis or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Converted values and included reference ranges may be mistaken for clinical interpretation. <br>
Mitigation: Use the skill for unit conversion and general education only; verify values and reference intervals against the lab report, local laboratory ranges, and qualified clinical judgment. <br>
Risk: Age, sex, pregnancy status, specimen type, or lab methodology can change the relevant reference interval. <br>
Mitigation: Treat reference ranges as informational context and confirm patient-specific ranges with the issuing laboratory or qualified clinician. <br>
Risk: Documentation and script behavior differ for some analytes and output field names. <br>
Mitigation: Review the actual JSON output and supported-analyte list before integrating this skill into automated workflows. <br>


## Reference(s): <br>
- [Medical Unit Converter reference guidelines](references/guidelines.md) <br>
- [Medical Unit Converter on ClawHub](https://clawhub.ai/aipoch-ai/medical-unit-converter) <br>
- [AIpoch publisher profile](https://clawhub.ai/user/aipoch-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON conversion results when the packaged script is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Structured responses separate objective, inputs, assumptions, workflow, deliverable, risks, and next checks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
