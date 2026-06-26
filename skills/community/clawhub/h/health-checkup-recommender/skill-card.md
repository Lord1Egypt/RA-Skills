## Description: <br>
Evidence-based health checkup recommendation service for personalized checkup plans based on age, gender, symptoms, and family history, with QR-code booking support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbihai](https://clawhub.ai/user/ryanbihai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and care-support agents use this skill to collect basic health context, recommend checkup items, calculate pricing, and prepare a booking QR flow. It is intended to support preventive checkup planning, not medical diagnosis or treatment. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles health-related conversation context and may document handoff to an external human-support workflow. <br>
Mitigation: Require explicit user opt-in before any handoff, preview the fields to be shared, and minimize or redact health context that is not necessary for the requested support action. <br>
Risk: Booking and QR workflows depend on third-party ihaola services. <br>
Mitigation: Tell users when they are leaving the skill flow for ihaola booking and confirm that personal booking details are entered by the user on the third-party site. <br>
Risk: Health checkup recommendations could be mistaken for medical diagnosis. <br>
Mitigation: Present recommendations as preventive checkup planning guidance and include a clear instruction to consult a qualified clinician for symptoms, abnormal results, or medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryanbihai/health-checkup-recommender) <br>
- [Publisher profile](https://clawhub.ai/user/ryanbihai) <br>
- [ihaola homepage](https://www.ihaola.com.cn) <br>
- [Booking information](reference/booking_info.md) <br>
- [Checkup item catalog](reference/checkup_items.json) <br>
- [Evidence mappings](reference/evidence_mappings_2025.json) <br>
- [Risk logic table](reference/risk_logic_table.json) <br>
- [Symptom mapping](reference/symptom_mapping.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown recommendations with inline shell commands and optional QR-code image output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local reference data for item selection and pricing; QR booking requires explicit user consent.] <br>

## Skill Version(s): <br>
4.6.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
