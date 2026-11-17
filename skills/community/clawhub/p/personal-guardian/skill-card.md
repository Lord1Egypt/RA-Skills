## Description:

Personal Guardian is an emergency-assistance agent that assesses personal safety signals and drafts escalation plans for location sharing, recording, emergency-contact notification, and preauthorized emergency calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaalenwow](https://clawhub.ai/user/aaalenwow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to simulate, design, or integrate personal emergency workflows that classify SOS, vitals, location, and device signals into response levels and produce response plans or incident records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes autonomous use of sensitive channels such as phone, messaging, microphone, contacts, location, social posting, and sensors.

Mitigation: Require explicit per-channel preauthorization, recipient allowlists, cancellation controls, and audit logs before granting any real device or communications access.

Risk: Emergency calls and rescue workflows may be configured for the wrong locale or emergency-number scheme.

Mitigation: Verify locale, jurisdiction, emergency numbers, and escalation policy before enabling any emergency-call or broadcast behavior.

Risk: Simulated actions may be presented as if they were active real-world actions.

Mitigation: Label simulation mode clearly and block real calls, messages, recording, or broadcasts unless production authorization and configuration checks pass.

Risk: Incident data may include highly sensitive location, audio, health, and contact information.

Mitigation: Define retention, deletion, encryption, and post-incident review rules before collecting or sharing incident data.

## Reference(s):

- [Personal Guardian on ClawHub](https://clawhub.ai/aaalenwow/skills/personal-guardian)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown/text guidance with optional JSON incident records and Python CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may describe emergency actions that require explicit user authorization, correct locale configuration, and clear simulation labeling before any real-world use.]

## Skill Version(s):

0.1.0 (source: server release metadata and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
