## Description:

Interpret blockchain data strategically; identify patterns, anomalies, and flows with data-backed evidence and explicit uncertainty.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mzfshark](https://clawhub.ai/user/mzfshark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and investigators use this skill to interpret wallet, contract, and transaction activity, map fund flows, identify anomalies, and separate evidence-backed facts from hypotheses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Findings could be mistaken for definitive financial or compliance conclusions.

Mitigation: Treat conclusions as analytical hypotheses, require transaction-level evidence, and independently verify before financial or compliance decisions.

Risk: Broad activation wording may apply the skill outside a concrete on-chain context.

Mitigation: Use the skill only when the request includes blockchain context and transaction, wallet, contract, or chain evidence.

Risk: Blockchain flow analysis could be misused for illicit activity or evasion.

Mitigation: Decline requests that facilitate illicit activity or evasion and keep analysis limited to data-backed interpretation.

## Reference(s):

- [OnChain Analysis ClawHub Skill](https://clawhub.ai/mzfshark/skills/onchain-analysis)
- [mzfshark Publisher Profile](https://clawhub.ai/user/mzfshark)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown analysis with evidence-backed findings, risk signals, hypotheses, and next checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings should cite transaction hashes or block references when available, distinguish facts from hypotheses, state missing data, and decline illicit or evasion-focused requests.]

## Skill Version(s):

2.0.0 (source: skill.yml, SKILL.md metadata, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
