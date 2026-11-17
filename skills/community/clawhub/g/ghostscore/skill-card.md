## Description:

Private reputation scoring for AI agents that queries on-chain credit tiers earned via x402 micropayments through Unlink shielded transfers on Monad and verifies tier proofs via zero-knowledge attestations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drewm33](https://clawhub.ai/user/drewm33)

### License/Terms of Use:

MIT

## Use Case:

External developers and AI-agent operators use GhostScore to check agent reputation tiers, list gated API endpoints, and verify existing zero-knowledge attestations without signing transactions or handling wallet private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a GhostScore API key and makes network calls to the GhostScore backend and Monad RPC.

Mitigation: Use only the required read-only RPC and API credentials, and do not provide wallet private keys, seed phrases, or signing credentials.

Risk: Users could confuse reputation lookup and verification with payment, signing, or attestation generation.

Mitigation: Keep payment, signing, wallet handling, and attestation generation outside the skill; use the skill only for read-only queries and verification.

## Reference(s):

- [GhostScore GitHub Repository](https://github.com/drewM33/ghostscore)
- [GhostScore ClawHub Skill](https://clawhub.ai/drewm33/skills/ghostscore)
- [GhostScore Frontend](https://ghostscore-app.onrender.com)
- [GhostScore API](https://ghostscore-api.onrender.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain text with optional structured verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only outputs may include reputation tiers, endpoint lists, and attestation validity summaries.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
