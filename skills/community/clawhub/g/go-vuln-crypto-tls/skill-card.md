## Description: <br>
Use when auditing Go code involving TLS configuration, certificate validation, JWT token parsing, SAML assertion verification, webhook signature checking, or cryptographic operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhy0](https://clawhub.ai/user/yhy0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to audit Go code for TLS, certificate validation, JWT, SAML, webhook HMAC, and related cryptographic verification mistakes. It provides checklist-driven review guidance and grep-based search paths for CWE-295, CWE-347, and CWE-345 patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prompts grep searches over a repository, which may expose code contents to the running agent. <br>
Mitigation: Use it only on codebases the agent is authorized to read. <br>
Risk: The reference cases and audit findings may be incomplete or need confirmation before security decisions are made. <br>
Mitigation: Verify referenced cases and manually review candidate findings before relying on them as authoritative vulnerability conclusions. <br>


## Reference(s): <br>
- [Go Crypto/TLS Real-World Cases](references/cases.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/yhy0/go-vuln-crypto-tls) <br>
- [Publisher Profile](https://clawhub.ai/user/yhy0) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with checklist items and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit guidance; prompts repository grep searches and manual verification of findings.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
