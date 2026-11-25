## Description:

Send medication reminders over the user's messaging channel — interview once to build meds-state.json, then handle dose replies (took / took-at / snooze / skip / undo) in plain language. Injection-aware: reconstituted peptides and other mg/mL vials get automatic syringe-unit math, so reminders read "Ipamorelin 200mcg = 20 units on your U-100".

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegizmopro](https://clawhub.ai/user/thegizmopro)

### License/Terms of Use:

MIT

## Use Case:

People using OpenClaw use this skill to create and manage medication schedules, receive reminders and digests through their configured messaging channel, and record dose replies. It is a reminder tool and does not diagnose, prescribe, or verify medical details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reminder may repeat after a dose is taken or skipped, or after a delivery retry.

Mitigation: Check the recorded dose status before treating a repeated reminder as a new dose prompt.

Risk: Medication names and dose times are visible to the configured messaging provider and chat members.

Mitigation: Use a private messaging channel that you have explicitly approved.

Risk: Scheduled-run behavior and Windows task cleanup can affect reminder delivery or remove tasks.

Mitigation: Review the scheduler and retry behavior, and inspect Windows cleanup targets before using cleanup options.

Risk: Security scan coverage was partial, with some static checks degraded.

Mitigation: Review the partially inspected components and degraded checks before relying on the release.

## Reference(s):

- [ClawHub security audit](https://clawhub.ai/thegizmopro/skills/med-reminder/security-audit)

## Skill Output:

**Output Type(s):** [Configuration, Text, Guidance]

**Output Format:** [JSON medication schedule configuration and plain-language reminder messages and responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contains user-provided medication names, doses, and schedules; does not provide medical advice.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
