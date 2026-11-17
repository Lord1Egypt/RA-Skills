## Description:

AI-powered meeting summary generator that converts meeting notes into professional summaries and action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icepopma](https://clawhub.ai/user/icepopma)

### License/Terms of Use:

MIT

## Use Case:

External users and teams use this skill to turn meeting notes or a notes file into a concise meeting summary with decisions, action items, discussion points, attendees, and next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs paid billing by default and includes a merchant key in the package.

Mitigation: Confirm billing behavior and merchant-key handling before installation; use test mode only for evaluation and set SKILLPAY_MERCHANT_KEY explicitly where approved.

Risk: Meeting notes are sent to the Sloan OpenClaw agent, whose exact privileges are not defined in the evidence.

Mitigation: Use only non-sensitive notes until the Sloan agent configuration, data handling, and access controls are reviewed.

Risk: Dependency installation sources and pinned installer versions need review before deployment.

Mitigation: Review package-lock.json and install dependencies from trusted, pinned sources before commercial use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/icepopma/skills/meeting-summary-generator)
- [Publisher profile](https://clawhub.ai/user/icepopma)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown meeting summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid run by default; supports optional title, date, file input, and test mode.]

## Skill Version(s):

1.1.2 (source: server release metadata and package.json; SKILL.md frontmatter states 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
