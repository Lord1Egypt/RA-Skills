## Description:

Build respectful multi-touch outreach sequences with channel mix, follow-up timing, objection handling, and logging templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business teams use this skill to draft respectful multi-touch outreach cadences from an offer, target persona, channels, timeline, proof assets, and stated boundaries. It helps produce first-touch messages, follow-ups, reply branches, a tracking sheet, and a testing plan for review before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated outreach copy may contain inaccurate claims, unsupported proof, or language that is not appropriate for the recipient.

Mitigation: Review every draft before sending, keep claims tied to user-provided proof assets, and mark uncertain details for confirmation.

Risk: A cadence can become spammy or ignore recipient boundaries if used without judgment.

Mitigation: Use preview or draft mode first, honor opt-outs and channel rules, and do not treat the skill as an automated sending system.

Risk: The local helper script writes a JSON output file.

Mitigation: Pass an explicit output path and inspect the generated file before using it in a campaign workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/outreach-sequence-crafter)
- [Publisher profile](https://clawhub.ai/user/52yuanchangxing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with optional local JSON file output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled helper script can write an outreach sequence JSON file to an explicit local output path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter lists 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
