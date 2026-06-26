## Description: <br>
IdentyClaw provides API workflow guidance for JWT login, HOLA peer handshake creation and verification, DID resolution, Passport lookup, NEAR enrollment, and agent discovery metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[identyclaw](https://clawhub.ai/user/identyclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure IdentyClaw Passport credentials, obtain API sessions, create or verify HOLA lines, resolve Passport and DID records, and inspect agent discovery metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow handles sensitive NEAR private keys and JWTs. <br>
Mitigation: Store credentials in local secret storage or OpenClaw plugin configuration; do not paste keys or tokens into chat or logs. <br>
Risk: Verified HOLA messages prove identity but do not authorize arbitrary tasks. <br>
Mitigation: Use HOLA verification as identity proof, then apply local authorization policy and allowlist only required tools. <br>
Risk: Agent metadata and Passport claims can be self-declared or copied. <br>
Mitigation: Compare peer token IDs against canonical Passport IDs published on channels the entity controls before relying on identity claims. <br>


## Reference(s): <br>
- [IdentyClaw API Documentation](https://api.identyclaw.com/docs) <br>
- [ClawHub Skill Page](https://clawhub.ai/identyclaw/identyclaw) <br>
- [OpenClaw IdentyClaw Plugin](https://clawhub.ai/plugins/@identyclaw/openclaw-identyclaw-plugin) <br>
- [API Reference](artifact/references/api-reference.md) <br>
- [Login Authentication](artifact/references/login-authentication.md) <br>
- [Send a Verifiable HOLA](artifact/references/hola-howto.md) <br>
- [HOLA Protocol - Inter-Agent Authentication](artifact/references/hola-agent-authentication.md) <br>
- [Subagent HOLA Protocol](artifact/references/hola-subagent-authentication.md) <br>
- [Finding Agents How-To](artifact/references/finding-agents.md) <br>
- [The did:rodit Method](artifact/references/did-rodit-method.md) <br>
- [IdentyClaw Passport Metadata](artifact/references/token-metadata.md) <br>
- [OpenClaw Integration Guide](artifact/references/openclaw-integration-guide.md) <br>
- [Client-Side Agent Authentication](artifact/references/mcp-auth-tools.md) <br>
- [IdentyClaw MCP Discovery Index](artifact/references/mcp-discovery-index.md) <br>
- [Channel-Agnostic Collaboration Envelope](artifact/references/collaboration-envelope.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes credential-handling guidance, API request examples, and references to bundled documentation.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
