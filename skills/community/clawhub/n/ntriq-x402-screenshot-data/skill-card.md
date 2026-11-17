## Description:

Convert screenshots into structured data, including text, UI layout, tables, and charts, with paid access through x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ntriq-gh](https://clawhub.ai/user/ntriq-gh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to send screenshot URLs or base64 images to ntriq's x402 API and receive extracted text, UI layout, tables, charts, or structured JSON for downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots are sent to ntriq's external API and may contain sensitive or confidential information.

Mitigation: Submit only screenshots approved for external processing, and avoid passwords, tokens, personal data, financial records, customer information, or confidential dashboards unless privacy and retention practices have been confirmed.

Risk: The service is paid per call through x402 on Base mainnet.

Mitigation: Confirm payment headers, network, and expected per-call cost before invoking the service, especially for automated or high-volume workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ntriq-gh/skills/ntriq-x402-screenshot-data)
- [ntriq x402 screenshot service](https://x402.ntriq.co.kr)
- [x402 protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, JSON, structured data]

**Output Format:** [JSON or plain text depending on extract_type]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output can include full structured JSON, visible text, layout analysis, or table and chart data based on the requested extraction mode.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
