## Description: <br>
Convert screenshots into structured data, including visible text, UI layout, tables, and charts, with paid x402 access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert screenshot images into machine-readable text, layout descriptions, table data, chart summaries, or full JSON for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots may contain sensitive personal, financial, credential, customer, or internal business information and are sent to a third-party remote service. <br>
Mitigation: Submit only screenshots you are authorized to process and avoid regulated or sensitive content unless provider privacy, retention, and deletion practices are acceptable. <br>
Risk: Each API call uses paid x402 access on Base mainnet. <br>
Mitigation: Confirm the payment amount, network, and authorization before invoking the service, and monitor agent workflows that can make repeated calls. <br>


## Reference(s): <br>
- [ntriq x402 screenshot service](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-screenshot-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, analysis] <br>
**Output Format:** [JSON response with extracted text, UI layout, tables, charts, and key metrics depending on extract_type.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an image URL or base64 screenshot and supports extract_type values full, text, layout, or data plus an optional language setting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
