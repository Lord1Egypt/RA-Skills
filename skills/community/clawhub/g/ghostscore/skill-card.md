## Description: <br>
Private reputation scoring for AI agents - query on-chain credit tiers earned via x402 micropayments through Unlink shielded transfers on Monad, and verify tier proofs via zero-knowledge attestations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drewM33](https://clawhub.ai/user/drewM33) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and AI-agent operators use GhostScore to query read-only reputation tiers, list tier-gated endpoints, verify existing zero-knowledge attestations, and understand the GhostScore protocol without signing transactions or moving funds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the GhostScore service and publisher for API responses and attestation verification context. <br>
Mitigation: Install only if the GhostScore service and publisher are trusted, and validate returned reputation or attestation data before relying on it for access decisions. <br>
Risk: The skill requires a GhostScore API key and a Monad RPC URL. <br>
Mitigation: Provide only MONAD_RPC_URL and GHOSTSCORE_API_KEY, prefer a scoped or revocable API key where available, and avoid sharing unrelated credentials. <br>
Risk: Wallet private keys, seed phrases, or signing keys would create avoidable fund-control exposure if provided to an agent. <br>
Mitigation: Never provide wallet private keys, seed phrases, signing keys, or write-enabled blockchain credentials; the reviewed artifact is read-only and verification-only. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/drewM33/ghostscore) <br>
- [GhostScore Homepage](https://github.com/drewM33/ghostscore) <br>
- [GhostScore Frontend](https://ghostscore-app.onrender.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown text with structured reputation, endpoint, and attestation verification results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MONAD_RPC_URL for read-only Monad queries and GHOSTSCORE_API_KEY for GhostScore API requests.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
