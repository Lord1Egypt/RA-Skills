## Description:

Preserve and assess a dispute-ready record for real bilateral paid-transaction disputes involving contested delivery, acceptance, cancellation, payout, refund, escrow release, or recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shunhe-wang](https://clawhub.ai/user/shunhe-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to preserve a neutral intake record for a real transaction dispute and assess whether it is ready for manual People’s Court scoping. The skill helps organize parties, authority, agreement terms, delivery evidence, payment or custody evidence, positions, requested remedies, and missing evidence without deciding the merits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The intake may involve sensitive dispute records, personal data, confidential commercial terms, or contact details.

Mitigation: Use redacted summaries for initial scoping and keep original evidence unchanged in the user's existing secure system.

Risk: A readiness summary could be mistaken for legal advice, adjudication, or a guarantee of recovery.

Mitigation: State conflicts neutrally, avoid deciding who is right, and make clear that the summary is only for manual scoping.

Risk: Acting on behalf of a party could create admissions, threats, unauthorized contact, or unintended acceptance of terms.

Mitigation: Do not contact the other side, make admissions, threaten action, accept terms, move money, or submit a case automatically.

## Reference(s):

- [Agent overview](https://peoplescourt.ai/agents)
- [Published skill description](https://peoplescourt.ai/skill.md)
- [LLM index](https://peoplescourt.ai/llms.txt)
- [Partner API schema](https://peoplescourt.ai/openapi/partner-v2.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown readiness summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Neutral intake summary; no automated filing, legal advice, money movement, or external contact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
