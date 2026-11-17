## Description:

Coordinates multiple selected language models to independently review, debate, score, and synthesize complex decisions into a consensus report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeekr0808-hue](https://clawhub.ai/user/zeekr0808-hue)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw to compare multiple model judgments for proposals, architecture choices, planning decisions, and other complex questions that benefit from independent scoring and consensus synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decision prompts and related context may be shared across multiple selected model sessions.

Mitigation: Use only with information that can be disclosed to those model sessions, and avoid confidential, regulated, credential-containing, financial, legal, or personal data unless sharing is explicitly approved.

Risk: Decision reports may be stored automatically and retain sensitive context after the review is complete.

Mitigation: Confirm where reports are written, disable or limit archival where possible, and delete retained reports according to the user's data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zeekr0808-hue/skills/multi-model-consensus)
- [Operation and user guide](docs/USER_GUIDE.md)
- [Output template](references/OUTPUT_TEMPLATE.md)
- [State machine specification](references/STATE_MACHINE.md)
- [Troubleshooting guide](references/TROUBLESHOOTING.md)
- [End-to-end verification case](references/VERIFICATION_CASE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown consensus report with scoring tables, decision-point status, recommendations, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-by-model voting records, confidence notes, unresolved decision points, and user-facing status updates during review rounds.]

## Skill Version(s):

1.9.1 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
