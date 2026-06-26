## Description: <br>
Register as buyer or seller, create and manage USDC escrow trades on Kryptone/PrivacyEscrow via HTTP API using an agent API key or human JWT authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[webcraft3r](https://clawhub.ai/user/webcraft3r) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent register buyer or seller roles and manage Kryptone/PrivacyEscrow USDC escrow trades through authenticated HTTP API calls. It supports trade creation, acceptance, deposit signature submission, settlement, dispute opening, and buyer ad workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact USDC escrow actions with an API key. <br>
Mitigation: Install only if the publisher and Kryptone/PrivacyEscrow server are trusted, inject AGENT_API_KEY only for this skill, and require manual review of trade ID, role, counterparty, and USDC amount before creating, accepting, submitting signatures for, or settling trades. <br>
Risk: Exposure or reuse of AGENT_API_KEY could let an agent act as the mapped Solana identity. <br>
Mitigation: Set KRYPTONE_API_BASE_URL explicitly, keep AGENT_API_KEY scoped to this skill, and rotate the key if it is exposed. <br>
Risk: On-chain deposit and settlement workflows affect USDC funds. <br>
Mitigation: Keep buyer signing separate from prompts and require human review before signing deposit transactions or triggering settlement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/webcraft3r/krypton-agent) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI helpers print JSON API responses and require KRYPTONE_API_BASE_URL plus AGENT_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
