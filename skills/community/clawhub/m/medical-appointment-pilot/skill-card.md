## Description: <br>
A high-trust, HIPAA-aware appointment agent for medical and dental clinics. Prevents scheduling errors via ThumbGate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinic staff and supervised appointment agents use this skill to intake medical or dental appointment requests, check practitioner fit, screen insurance, and propose booking details while following privacy and emergency-handoff rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to handle medical appointment data and booking workflows without enough privacy, storage, or human-control boundaries. <br>
Mitigation: Install only as a draft scheduling prompt or staff-assisted intake aid until the clinic defines secure collection, storage, retention, credential scoping, and human confirmation for bookings and urgent-care handoffs. <br>
Risk: Connecting the skill directly to live schedules, patient records, insurance systems, Google Sheets, or APIs could expose sensitive data or create unconfirmed bookings. <br>
Mitigation: Do not connect live systems until the clinic has reviewed data handling, credential scope, retention, and human approval requirements. <br>


## Reference(s): <br>
- [ThumbGate Prevention Rules](thumbgate-rules.md) <br>
- [ClawHub skill listing](https://clawhub.ai/igorganapolsky/medical-appointment-pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown and structured appointment-handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports staff-assisted appointment intake, booking checks, privacy guardrails, and emergency handoff prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
