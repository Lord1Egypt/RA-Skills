## Description: <br>
Extract structured invoice data (vendor, line items, totals, tax) from any invoice image. Pay $0.03 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit invoice or receipt images to ntriq's x402 invoice extraction service and receive structured invoice fields for accounting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice or receipt data is sent to ntriq's remote service despite artifact text claiming no cloud upload. <br>
Mitigation: Use only invoices you are comfortable sending to that service and verify ntriq's privacy and retention terms before use. <br>
Risk: Each x402 request can spend $0.03 USDC on Base mainnet. <br>
Mitigation: Keep wallet approvals or spending limits tight and review payment behavior before installing or automating the skill. <br>


## Reference(s): <br>
- [Ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-invoice-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API calls, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with HTTP and curl examples; the service response is structured JSON invoice data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts invoice image URL or base64 input, optional output language, and x402 payment header; each call costs $0.03 USDC on Base mainnet.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
