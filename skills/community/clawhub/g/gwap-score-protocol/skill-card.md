## Description:

GwapScore Protocol is an instruction-only skill for deterministic Solana wallet trust scoring using onchain activity, confidence, attestations, caps, and review triggers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwapupward-hub](https://clawhub.ai/user/gwapupward-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent builders, and partner integration teams use this skill to design, explain, audit, or extend GwapScore Protocol v2 scoring for Solana wallets. It helps agents produce scoring logic, score explanations, category breakdowns, risk flags, confidence outputs, manual review packets, and partner-safe trust labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet scores may influence labels, gating, payment flows, escrow recommendations, or other user-facing trust decisions.

Mitigation: Review fairness, dispute handling, confidence thresholds, and legal or product implications before using the score in a real application.

Risk: A score without confidence can overstate certainty for thin, new, or conflicting wallet evidence.

Mitigation: Use confidence separately from score, cap low-confidence profiles where appropriate, and disclose conflicting evidence in explanations.

Risk: Ambiguous Sybil, scam-cluster, fraud, dispute, or compromised-wallet signals can create unfair severe labels.

Mitigation: Route ambiguous or high-impact cases through manual review, preserve evidence pointers, and provide a dispute path for severe negative outcomes.

Risk: Partner-facing outputs can be misread as wealth, personal worth, identity, legal status, or personal creditworthiness.

Mitigation: Frame outputs as observed onchain trust behavior, avoid unsupported personal inferences, and require product or legal review before creditworthiness framing.

## Reference(s):

- [GwapScore Protocol ClawHub skill page](https://clawhub.ai/gwapupward-hub/skills/gwap-score-protocol)
- [GwapScore Protocol v2 Scoring Model](artifact/references/scoring-model-v2.md)
- [GwapScore Protocol v2 Confidence Model](artifact/references/confidence-model-v2.md)
- [Canonical Event Schema](artifact/references/canonical-event-schema.md)
- [Attestation Taxonomy](artifact/references/attestation-taxonomy.md)
- [Decay and Recovery Rules](artifact/references/decay-and-recovery-rules.md)
- [Manual Review Policy](artifact/references/manual-review-policy.md)
- [Feature Gating Thresholds](artifact/references/feature-gating-thresholds.md)
- [Partner Integration Policy](artifact/references/partner-integration-policy.md)
- [Score Output Template](artifact/templates/score-output-template.md)
- [Risk Escalation Template](artifact/templates/risk-escalation-template.md)
- [Manual Review Template](artifact/templates/manual-review-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown prose with TypeScript and JSON examples or templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only outputs may include score explanations, category breakdowns, risk flags, caps, confidence levels, partner response shapes, and manual review packets.]

## Skill Version(s):

1.0.1 (source: server release metadata, package.json, OpenClaw.plugin.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
