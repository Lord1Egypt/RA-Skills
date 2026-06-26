## Description: <br>
GwapScore Protocol helps agents design, explain, audit, and extend deterministic Solana wallet trust scoring using canonical events, attestations, confidence, caps, review triggers, and partner-safe explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwapupward-hub](https://clawhub.ai/user/gwapupward-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, protocol operators, and partner integration teams use this instruction-only skill to produce GwapScore v2 scoring logic, score explanations, API designs, review packets, and integration guidance for Solana wallet trust workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated wallet trust scores or labels may be misleading if used without confidence, explanations, manual review, or dispute paths. <br>
Mitigation: Use scores with confidence levels, evidence explanations, review actions, and dispute paths for severe labels. <br>
Risk: Granting wallet signing, payment, secret, network, or background execution permissions would exceed the reviewed instruction-only package behavior. <br>
Mitigation: Install as a read-only instruction skill unless a separate implementation is reviewed before enabling those permissions. <br>
Risk: High-impact gating or partner decisions can be unfair when based on score alone. <br>
Mitigation: Apply both score and confidence thresholds, honor unresolved severe risk flags, and route ambiguous or severe cases to manual review. <br>


## Reference(s): <br>
- [GwapScore Protocol on ClawHub](https://clawhub.ai/gwapupward-hub/gwap-score-protocol) <br>
- [GwapScore Protocol v2 Scoring Model](references/scoring-model-v2.md) <br>
- [GwapScore Protocol v2 Confidence Model](references/confidence-model-v2.md) <br>
- [Canonical Event Schema](references/canonical-event-schema.md) <br>
- [Attestation Taxonomy](references/attestation-taxonomy.md) <br>
- [Decay and Recovery Rules](references/decay-and-recovery-rules.md) <br>
- [Manual Review Policy](references/manual-review-policy.md) <br>
- [Feature Gating Thresholds](references/feature-gating-thresholds.md) <br>
- [Partner Integration Policy](references/partner-integration-policy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and TypeScript-style examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; generated scores should include confidence, explanations, caps, risk flags, and review actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence, package.json, OpenClaw.plugin.json, README.md, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
