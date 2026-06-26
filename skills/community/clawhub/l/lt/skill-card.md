## Description: <br>
Agents can sign plugins, rotate credentials without losing identity, and publicly attest to behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ltte](https://clawhub.ai/user/ltte) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure 0.protocol identity and attestation workflows, including signed plugin claims, wallet queries, and authenticated task handoffs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent identity records or public transfer payloads may expose secrets, credentials, customer data, personal data, internal identifiers, or sensitive task context if included by the user. <br>
Mitigation: Review express and transfer payloads and visibility settings before execution, and omit sensitive data from public or durable records. <br>


## Reference(s): <br>
- [0.protocol README / Spec](https://github.com/0isone/0protocol) <br>
- [0.protocol API Reference](https://github.com/0isone/0protocol/blob/main/API.md) <br>
- [0.protocol Migration Guide](https://github.com/0isone/0protocol/blob/main/migration.md) <br>
- [0.protocol Why](https://github.com/0isone/0protocol/blob/main/WHY.md) <br>
- [0.protocol MCP Endpoint](https://mcp.0protocol.dev/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter for the recommended setup path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
