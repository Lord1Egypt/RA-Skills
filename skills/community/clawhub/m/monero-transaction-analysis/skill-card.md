## Description:

Analyze Monero transactions by inspecting inputs, outputs, ring signatures, fund flows, and privacy features for forensic and verification purposes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumaimiao](https://clawhub.ai/user/liumaimiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, forensic analysts, compliance teams, and incident responders use this skill to understand Monero transaction structure, evaluate privacy signals, and document authorized transaction analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transaction analysis heuristics can produce false positives or overstate traceability for privacy-preserving Monero activity.

Mitigation: Treat findings as probabilistic, corroborate with authorized evidence, and document uncertainty in compliance or incident-response workflows.

Risk: Third-party explorers or services may expose lookup metadata, and privacy claims should not be assumed without verification.

Mitigation: Prefer trusted local tooling or privacy-preserving network access, and independently verify any explorer privacy policy before use.

## Reference(s):

- [Monero Transaction Analysis on ClawHub](https://clawhub.ai/liumaimiao/skills/monero-transaction-analysis)
- [Monero Research Lab](https://research.getmonero.org/)
- [RingCT Technical Paper](https://eprint.iacr.org/2017/045.pdf)
- [Monero StackExchange](https://monero.stackexchange.com/)
- [xmrchain.net Monero Explorer](https://xmrchain.net)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with illustrative shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational analysis guidance; no executable code is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
