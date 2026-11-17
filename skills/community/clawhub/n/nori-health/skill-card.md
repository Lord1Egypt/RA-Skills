## Description:

Nori Health sends health-related questions about sleep, workouts, nutrition, weight, heart rate, HRV, and related insights to Nori and returns the coach's plain-text reply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danmurphy1217](https://clawhub.ai/user/danmurphy1217)

### License/Terms of Use:


## Use Case:

External users use this skill to ask Nori health-coaching questions based on connected wearable, nutrition, workout, weight, and lab data. It is not intended for emergencies, medical diagnosis, or prescriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health-related questions and context are sent to Nori's service for processing.

Mitigation: Use the skill only for information you are comfortable sharing with Nori and avoid submitting sensitive health details you do not want processed there.

Risk: The skill requires a Nori API key to be stored for OpenClaw use.

Mitigation: Store the API key in the documented environment variable or OpenClaw configuration and regenerate it in the Nori app if it is invalid or exposed.

Risk: The skill is not intended for emergency care, diagnosis, or prescriptions.

Mitigation: Direct emergency, diagnostic, or prescription requests to a doctor or emergency services instead of using this skill.

## Reference(s):

- [Nori Health](https://nori.health)
- [ClawHub Skill Page](https://clawhub.ai/danmurphy1217/skills/nori-health)
- [ClawHub Publisher Profile](https://clawhub.ai/user/danmurphy1217)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses with setup and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For successful requests, the skill returns Nori's reply directly without additional formatting.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
