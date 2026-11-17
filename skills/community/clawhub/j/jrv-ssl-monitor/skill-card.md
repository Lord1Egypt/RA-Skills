## Description:

Check SSL/TLS certificate expiry, issuer, protocol, and SANs for one or more domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnywang2001](https://clawhub.ai/user/johnnywang2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to check certificate expiry, issuer, TLS protocol, and Subject Alternative Names for one or more domains. It can support cron jobs, CI/CD certificate gates, pre-deployment validation, and domain certificate audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation that uses --json may misread certificate health if it relies only on process exit codes.

Mitigation: Parse the JSON status fields directly or wrap the command with explicit status handling before using it in CI, cron, or alerting.

Risk: The checker reports certificate health details but is not a full domain security audit or certificate-chain validator.

Mitigation: Use it as one certificate monitoring signal and pair it with dedicated TLS and domain security tooling for broader assurance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnywang2001/skills/jrv-ssl-monitor)
- [Publisher profile](https://clawhub.ai/user/johnnywang2001)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, json, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled checker accepts one or more domains plus port, timeout, warning threshold, and JSON-output options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
