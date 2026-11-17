## Description:

Domain registrar and DNS manager using the Name.com CORE API. Use when the user asks to search for, buy, or register domains, manage DNS records (A, AAAA, CNAME, MX, TXT), solve ACME DNS-01 challenges for TLS certificates, or update dynamic DNS for residential/home-lab setups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patramsey](https://clawhub.ai/user/patramsey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage Name.com domains and DNS records through an MCP-enabled agent. It supports domain availability checks, domain registration, nameserver updates, DNS record management, ACME DNS-01 challenge setup, and dynamic DNS updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs an unpinned npm server that receives powerful Name.com registrar credentials.

Mitigation: Review and pin the exact namecom-clawbot version before installing, run it in an isolated environment, and start with sandbox credentials.

Risk: Production Name.com credentials can expose DNS, domain-transfer, and purchase risk.

Mitigation: Use Name.com IP whitelisting, avoid exposing production registrar credentials unless the risk is accepted, and prefer account credit or payment controls for purchases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/patramsey/skills/namecom-registrar)
- [namecom-clawbot homepage](https://github.com/patramsey/namecom-clawbot)
- [namecom-clawbot npm package](https://www.npmjs.com/package/namecom-clawbot)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm plus Name.com username and API token environment variables.]

## Skill Version(s):

0.0.14 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
