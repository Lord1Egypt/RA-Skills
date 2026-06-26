## Description: <br>
Secure n8n workflow automation integration for coding tasks with credential isolation, input validation, audit logging, rate limiting, and granular permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelmaz](https://clawhub.ai/user/nelmaz) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to inspect, execute, and modify n8n workflows from an agent while following documented controls for credentials, permissions, confirmations, and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an n8n API key that can affect workflows. <br>
Mitigation: Use a least-privilege n8n key, keep the default readonly posture where possible, and avoid full mode for production. <br>
Risk: Advertised confirmations, rate limits, permission modes, and audit logging may be guidance rather than enforced protections. <br>
Mitigation: Independently enforce permissions, rate limits, and change review in the n8n environment before allowing workflow changes. <br>
Risk: Credentials can be exposed if stored in shell startup files, configuration files, or plaintext credential storage. <br>
Mitigation: Provide N8N_URL and N8N_API_KEY through a secure runtime environment or secret manager and scan files before publishing. <br>
Risk: Public publishing steps can expose secrets if files or commit history are not reviewed first. <br>
Mitigation: Review artifacts and commit history for secrets before following any public publishing workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nelmaz/n8n-automation-secure) <br>
- [Security reference](references/security.md) <br>
- [Setup validation script](scripts/validate-setup.sh) <br>
- [n8n API documentation](https://docs.n8n.io/api/) <br>
- [OpenClaw security documentation](https://docs.openclaw.ai/security) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell, JSON, YAML, and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce n8n API calls and setup guidance that require N8N_URL and N8N_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
