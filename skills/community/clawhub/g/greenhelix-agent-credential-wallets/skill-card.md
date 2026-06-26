## Description: <br>
Build agent credential wallets with Verifiable Intent, SD-JWT delegation chains, cross-protocol presentation (AP2/UCP/ACP/x402), eIDAS 2.0 EUDI compliance, and reputation-bound credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this guide to design agent credential wallets, delegation chains, and credential presentation flows for agent commerce systems that integrate with GreenHelix APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide is documentation-only, but its examples should be treated as live state-changing code if executed. <br>
Mitigation: Use sandbox credentials or a least-privilege GreenHelix API key, verify GREENHELIX_API_URL before running snippets, and review each request before execution. <br>
Risk: The verifier examples are illustrative and are not sufficient as production credential verification logic. <br>
Mitigation: Add real DID resolution, signature verification, disclosure checks, expiration checks, revocation checks, and constraint-chain validation before production use. <br>
Risk: The skill references a sensitive credential environment variable, GREENHELIX_API_KEY. <br>
Mitigation: Store the key securely, avoid committing it, rotate it as needed, and scope it to only the required GreenHelix access. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mirni/greenhelix-agent-credential-wallets) <br>
- [GreenHelix sandbox](https://sandbox.greenhelix.net) <br>
- [GreenHelix A2A Commerce Gateway API](https://api.greenhelix.net/v1) <br>
- [Agent delegation credential schema](https://greenhelix.net/credentials/agent-delegation/v1) <br>
- [Verifiable intent credential schema](https://greenhelix.net/credentials/verifiable-intent/v1) <br>
- [EUDI delegation credential schema](https://greenhelix.net/credentials/eudi-delegation/v1) <br>
- [Reputation-bound delegation credential schema](https://greenhelix.net/credentials/reputation-bound-delegation/v1) <br>
- [Dispute evidence credential schema](https://greenhelix.net/credentials/dispute-evidence/v1) <br>
- [Related GreenHelix production hardening skill](https://clawhub.ai/skills/greenhelix-agent-production-hardening) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guide with Python examples and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples may call GreenHelix APIs if a user runs them.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
