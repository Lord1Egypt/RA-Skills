## Description: <br>
Batch extract structured data from up to 500 invoices/receipts. Flat $9.00 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operations teams use this skill to call a paid API that extracts structured invoice and receipt fields from batches of image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Invoice or receipt image URLs, fetched document contents, and extracted financial fields are sent to a third-party service. <br>
Mitigation: Use only documents you are authorized to process, and avoid regulated, confidential, customer, or payment-sensitive documents unless the service's retention and logging practices are acceptable. <br>
Risk: The skill describes a paid x402 request with a flat $9.00 USDC charge on Base mainnet. <br>
Mitigation: Confirm wallet policy, payment header generation, network, and expected cost before allowing an agent to call the endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-invoice-extract-batch) <br>
- [Ntriq X402 homepage](https://x402.ntriq.co.kr) <br>
- [Invoice extract batch API](https://x402.ntriq.co.kr/invoice-extract-batch) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls] <br>
**Output Format:** [Markdown guidance with HTTP request, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The API returns JSON results with invoice status, counts, and extracted fields; image URL batches are limited to 500 per call.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
