## Description:

This skill uses Juhe Data's Chinese ID card information query API to parse a provided resident ID number for encoded sex, birth date, household registration area, and format hints through a paid Alipay AI Pay flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query basic encoded information from a Chinese resident ID number after payment. The skill is limited to code-rule parsing and must not be used for identity authenticity checks, public security real-name verification, or bulk collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes full Chinese resident ID numbers and sends the query value to Juhe's service.

Mitigation: Require explicit user consent before the paid query, send only the ID number needed for the lookup, mask the ID in all user-facing output, and avoid logging or storing the full value.

Risk: The artifact suggests installing an Alipay payment dependency using a mutable latest package with automatic confirmation.

Mitigation: Use a pinned and reviewed package version, avoid automatic confirmation during installation, and require the user to approve both installation and payment actions.

Risk: Payment handling can expose users to unintended charges if order details or the 402 payment response are altered.

Mitigation: Preserve the original 402 response for the payment skill, display product name, amount, transaction number, and user order number, and proceed only after explicit payment confirmation.

Risk: The API result is based on ID-number encoding rules and third-party data, not official identity verification.

Mitigation: State that results are for reference only and cannot prove whether an ID card is genuine or whether a person has been verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/juhemcp/skills/juhe-idcard-query-a2a)
- [Publisher Profile](https://clawhub.ai/user/juhemcp)
- [Juhe A2A Query Endpoint](https://apis.juhe.cn/a2a/query)
- [Output Format](artifact/OUT_FORMAT.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown table output with masked ID numbers and payment-flow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only returned API fields; full ID numbers must be masked in user-facing output and excluded from logs.]

## Skill Version(s):

1.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
