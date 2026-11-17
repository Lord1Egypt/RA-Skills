## Description:

Send medication reminders over the user's messaging channel — interview once to build meds-state.json, then handle dose replies (took / took-at / snooze / skip / undo) in plain language. Injection-aware: reconstituted peptides and other mg/mL vials get automatic syringe-unit math, so reminders read "Ipamorelin 200mcg = 20 units on your U-100".

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegizmopro](https://clawhub.ai/user/thegizmopro)

### License/Terms of Use:

MIT

## Use Case:

People who want medication reminders in a messaging channel can use this skill to configure schedules, receive reminders and follow-ups, and record dose replies. It can also calculate syringe units from reconstituted medication concentrations; it is a reminder aid, not a medical device.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current release may disable other reminders during scheduler setup or record a dose as taken without an explicit confirmation.

Mitigation: Use a corrected release before relying on the reminders; preview setup changes and confirm unrelated scheduler configurations remain enabled. Record doses as taken only after an explicit confirmation.

Risk: History recovery and timing defects may affect dose records or reminder delivery.

Mitigation: Use a corrected release before relying on dose history or reminder timing.

Risk: Medication details are disclosed to the configured messaging service and message recipients.

Mitigation: Review the configured sender and recipients, protect the medication state and history files, and enable log redaction where appropriate.

## Reference(s):

- [Med Reminder release page](https://clawhub.ai/thegizmopro/skills/med-reminder)

## Skill Output:

**Output Type(s):** [Text, Configuration, Shell commands, Guidance]

**Output Format:** [Medication reminder messages, JSON configuration, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reminder content can include medication details and is sent through the user's configured messaging channel.]

## Skill Version(s):

1.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
