## Description: <br>
Guides agents through implementing tamper-evident audit trails for autonomous trading bots using GreenHelix event logging, Merkle claim chains, compliance reports, and webhook forwarding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirni](https://clawhub.ai/user/mirni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance engineers use this guide to add signed, append-only audit logging, Merkle verification, event schemas, retention manifests, compliance reporting, and webhook forwarding to trading bot workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API examples may be adapted directly into production trading or compliance workflows. <br>
Mitigation: Review and modify examples before use, start with test credentials, and confirm endpoint behavior before connecting production accounts. <br>
Risk: Event payloads, reports, and webhooks may expose sensitive trading, account, or strategy data. <br>
Mitigation: Redact sensitive fields before logging, reporting, or forwarding events, and apply access controls to audit outputs. <br>
Risk: The skill depends on a signing key for agent identity. <br>
Mitigation: Store AGENT_SIGNING_KEY in a secrets manager, rotate it when needed, and avoid committing generated private keys or API credentials. <br>
Risk: Sample validation and retention code may not satisfy compliance requirements as written. <br>
Mitigation: Have compliance and security reviewers validate signature checks, retention policies, and WORM storage behavior before relying on the implementation. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/mirni/greenhelix-trading-bot-audit-trail) <br>
- [GreenHelix sandbox endpoint](https://sandbox.greenhelix.net) <br>
- [GreenHelix API endpoint](https://api.greenhelix.net/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guide with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires users to supply and protect AGENT_SIGNING_KEY for Ed25519 request signing.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
