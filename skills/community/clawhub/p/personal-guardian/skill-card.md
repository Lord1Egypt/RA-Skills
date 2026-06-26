## Description: <br>
Personal Guardian is a personal emergency-response agent that assesses SOS, vital-sign, location, and device signals to coordinate escalation, notifications, location sharing, recording, emergency-call, broadcast, and incident-review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaalenwow](https://clawhub.ai/user/aaalenwow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to model, configure, or simulate personal emergency response flows that escalate from risk detection to contact notification, location sharing, emergency-service outreach, and incident review. Real emergency integrations require explicit authorization, local-law review, and tested cancellation paths before use. <br>

### Deployment Geography for Use: <br>
Global; emergency-calling, privacy, health-data, and broadcast behavior must be localized to the user's jurisdiction before real-world deployment. <br>

## Known Risks and Mitigations: <br>
Risk: Broad autonomous access to microphones, cameras, health data, location, calling, messaging, social broadcast, nearby broadcast, and drone channels could expose sensitive information or trigger unwanted actions. <br>
Mitigation: Keep all real integrations disabled by default and enable each channel only after explicit user configuration, consent, and authorization checks. <br>
Risk: False alarms or mistaken escalation could notify contacts, call emergency services, or broadcast user location unnecessarily. <br>
Mitigation: Test cancellation and override flows, verify emergency-call authorization, and require localized escalation rules before connecting live phone, SMS, or emergency-service channels. <br>
Risk: Incident audio, location traces, contacts, and health signals are sensitive and may persist after an emergency. <br>
Mitigation: Use local encrypted storage where possible and define clear retention, review, export, and deletion rules before deployment. <br>
Risk: The artifact references 120/110 and jurisdiction-specific emergency behavior that may not match the user's location. <br>
Mitigation: Localize emergency numbers, dispatch wording, privacy requirements, and permitted broadcast channels for each deployment geography. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aaalenwow/personal-guardian) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/aaalenwow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and structured text with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe simulated emergency actions, escalation levels, contact workflows, and incident records; real-world execution requires authorized integrations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
