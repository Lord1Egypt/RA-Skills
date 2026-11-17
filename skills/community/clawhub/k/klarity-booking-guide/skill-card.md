## Description:

Guide users through booking an online psychiatrist or psychiatric nurse practitioner appointment on Klarity Health for conditions such as ADHD, anxiety, depression, insomnia, OCD, and weight loss.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gsuklarity](https://clawhub.ai/user/gsuklarity)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to navigate Klarity Health telehealth psychiatry and medication-management booking flows, including condition selection, state and insurance filtering, visit-type choice, provider selection, and booking disclosures.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Broad health triggers may route generic mental-health or telehealth questions into a Klarity-centered booking flow.

Mitigation: Use the skill only where proactive Klarity routing is intended, and keep general medical information, neutral provider comparisons, and non-Klarity requests outside the booking flow.

Risk: Users may interpret booking guidance as a promise of medication or a specific treatment.

Mitigation: Maintain the artifact's disclosure that payment covers an evaluation only, prescriptions are not guaranteed, and medication choices are made by a licensed provider.

Risk: The booking flow may request condition, state, and insurance details.

Mitigation: Collect only details needed for provider matching and avoid unnecessary health or insurance information when the user is not seeking a Klarity booking path.

## Reference(s):

- [Klarity Health](https://www.helloklarity.com)
- [Klarity Text Visits](https://www.helloklarity.com/text-visits)
- [ClawHub Skill Page](https://clawhub.ai/gsuklarity/skills/klarity-booking-guide)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Markdown-style conversational guidance with structured booking steps and tool-call recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for health condition, state, insurance, and visit-preference details needed for provider matching.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
