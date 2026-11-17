## Description:

Guides an agent through booking appointments at Shanghai municipal hospitals using the hospital platform in WeChat on a USB-connected Android phone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlittlebear](https://clawhub.ai/user/openlittlebear)

### License/Terms of Use:

MIT-0

## Use Case:

People booking care in Shanghai and their authorized agents can use this skill to select a hospital, department and appointment slot, then confirm the booking with the user's visit card and SMS code.

### Deployment Geography for Use:

Shanghai, China

## Known Risks and Mitigations:

Risk: The agent can submit a real hospital appointment with a selected visit card, time slot and fee.

Mitigation: Have the user confirm the hospital, department, date, visit card and fee before final submission.

Risk: Screenshots and logs may expose patient identity, medical details or SMS verification codes.

Mitigation: Ask the user for the SMS code directly and avoid retaining screenshots or logs with names, ID numbers, phone numbers or codes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/openlittlebear/skills/hospital-android-adb)
- [Shanghai municipal hospital appointment platform](https://internethospital.shdc.org.cn)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown and command-line text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appointment details and confirmation status should be reviewed with the user before submission.]

## Skill Version(s):

2.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
