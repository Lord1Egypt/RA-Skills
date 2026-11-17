## Description:

Network diagnostics and analysis toolkit using Python standard library for checking connectivity, resolving DNS, inspecting HTTP responses, scanning ports, and looking up WHOIS and SSL information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and network engineers use this skill to run basic network diagnostics on authorized hosts and networks without installing external Python packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HTTPS and SSL checks can produce misleading security conclusions because certificate validation is disabled in important paths.

Mitigation: Treat TLS-related output as advisory and confirm security-sensitive results with a validating client or approved security tool before relying on them.

Risk: Port scanning and diagnostic requests can generate noticeable network traffic.

Mitigation: Run the skill only against hosts and networks where testing is authorized, and keep scan ranges and timeouts scoped to the diagnostic need.

Risk: The public IP feature contacts external IP lookup services.

Mitigation: Avoid using the public IP lookup on sensitive networks unless those outbound services are approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ericlooi504/skills/network-toolbox)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON command output with Markdown command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network requests may contact target hosts, WHOIS servers, and public IP lookup services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
