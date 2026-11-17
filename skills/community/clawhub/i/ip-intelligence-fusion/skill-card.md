## Description:

IP Intelligence Fusion investigates an explicitly supplied public IPv4 or IPv6 address and creates an auditable multi-source assessment of ownership, routing, geolocation, proxy/VPN/Tor exposure, hosting, abuse, fraud, reputation, and IP purity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianfuli](https://clawhub.ai/user/jianfuli)

### License/Terms of Use:

MIT

## Use Case:

Security, fraud, infrastructure, and operations teams use this skill to investigate public IP addresses, reconcile provider disagreement, and produce auditable JSON evidence, an offline HTML report, and a concise human-facing brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send the target public IP address to multiple third-party intelligence services.

Mitigation: Run it only for IP addresses the user is authorized to investigate and is comfortable disclosing to the selected providers.

Risk: Using --self intentionally investigates and discloses the machine's current public IP address.

Mitigation: Use --self only when that disclosure is intended; otherwise provide an explicit public IP address.

Risk: A custom SCAMALYTICS_API_URL can redirect lookups to an untrusted endpoint.

Mitigation: Set SCAMALYTICS_API_URL only after verifying the exact trusted HTTPS endpoint.

Risk: --include-raw can save third-party response data into generated reports.

Mitigation: Enable raw payload capture only when needed, and treat generated reports as sensitive review artifacts.

Risk: Configured provider credentials can expand what data is queried and returned.

Mitigation: Use existing environment credentials only, do not ask users to paste keys, and review configured provider access before deployment.

## Reference(s):

- [Fusion methodology](references/methodology.md)
- [Provider reference](references/providers.md)
- [Public-page collection](references/public-pages.md)
- [HTML report design](references/report-design.md)
- [IP Intelligence Fusion on ClawHub](https://clawhub.ai/jianfuli/skills/ip-intelligence-fusion)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown brief with generated JSON and self-contained HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are point-in-time investigation aids and preserve successful, skipped, unavailable, and failed source states.]

## Skill Version(s):

1.3.1 (source: release evidence and scripts/ip_intelligence.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
