## Description:

NadMail gives AI agents a wallet-authenticated @nadmail.ai email identity for registering, sending mail, reading an inbox, and optionally boosting internal messages with MON-based emo-buy transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to equip an agent with a NadMail address, wallet-based SIWE registration, email sending, inbox access, and optional MON-backed boosts for internal NadMail messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet identity material and local NadMail auth tokens.

Mitigation: Use a dedicated low-balance wallet, prefer environment variables or encrypted storage, keep local NadMail files out of version control, and avoid entering wallet passwords in shared or recorded terminals.

Risk: Sending and inbox operations transmit email and inbox data to api.nadmail.ai.

Mitigation: Use the skill only for email content appropriate for the NadMail service and review recipients, subjects, and message bodies before sending sensitive information.

Risk: Emo-buy and credit workflows can involve MON spending, and the security guidance says not to rely on the local emo-buy cap as a hard financial limit.

Mitigation: Review each spending prompt, keep wallet balances low, monitor external credit purchases and emo-buy amounts, and treat local caps as convenience controls rather than complete financial safeguards.

Risk: The authoritative security verdict is suspicious because the skill handles wallet secrets and financial actions with weak safeguards.

Mitigation: Review and update dependencies before serious use, scan the artifact before deployment, and limit execution to trusted environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daaab/skills/nadmail)
- [NadMail Website](https://nadmail.ai)
- [NadMail API Docs](https://api.nadmail.ai/api/docs)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No structured post-processing required.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0 and package.json reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
