## Description:

Helps agents structure CNY interbank pledged-repo and funding-trader analysis, collateral eligibility checks, risk controls, trade communications, and post-trade review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hjh5555](https://clawhub.ai/user/hjh5555)

### License/Terms of Use:

MIT-0

## Use Case:

External users and finance practitioners can use this skill to draft human-reviewable CNY interbank funding plans, market notes, collateral checks, counterparty messages, risk checks, and trade reviews. It is decision support only and relies on users to confirm live market data, trade instructions, account rules, counterparty limits, and compliance requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial decision support could be mistaken for binding trading, investment, regulatory, or compliance advice.

Mitigation: Use outputs as drafts for qualified human review, require confirmation of live market data and trade instructions, and avoid claiming that trades, settlement, or compliance approval have occurred.

Risk: Collateral eligibility checks can be unsafe when account rules, blacklist data, relationship tags, ratings, or custody data are missing or stale.

Mitigation: Use only confirmed internal CSV data, select the real account explicitly for live workflows, fail closed on missing material fields, and escalate unclear cases to trade, risk, or compliance reviewers.

Risk: The bundled verifier script is flagged by security guidance for live collateral use until blacklist, relationship-data, and spreadsheet-formula handling are strengthened.

Mitigation: Avoid relying on the script for live collateral decisions until it is fixed and re-reviewed; when used for testing, compare results against the documented manual verification rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hjh5555/skills/interbank-funding-trader)
- [Market Map](artifact/references/01-market-map.md)
- [Decision Playbook](artifact/references/02-decision-playbook.md)
- [Data Inputs](artifact/references/03-data-inputs.md)
- [Risk Controls](artifact/references/04-risk-controls.md)
- [Communication Style](artifact/references/05-communication-style.md)
- [Review and Learning](artifact/references/07-review-and-learning.md)
- [Collateral Verification](artifact/references/08-collateral-verification.md)
- [iFinD Finance Data Skill Coordination](artifact/references/09-ifind-finance-data-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, concise prose, optional shell commands, and generated text templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include collateral-check tables, trading-plan sections, communication drafts, risk prompts, and review notes for human approval.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
