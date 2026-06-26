## Description: <br>
Batch document OCR, classification, and extraction for up to 500 images with a flat $15.00 USDC x402 payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit batches of document image URLs for OCR, extraction, summarization, classification, or table analysis through the provider's x402-enabled service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Document URLs, document contents, and extracted text may be sent to a third-party remote service. <br>
Mitigation: Use only documents appropriate for that provider, and avoid confidential, regulated, identity, legal, medical, financial, or business-sensitive content unless privacy, retention, and deletion terms have been reviewed. <br>
Risk: The skill describes a paid x402 flow that charges a flat $15.00 USDC per batch request. <br>
Mitigation: Confirm payment headers, network, recipient, and request size before execution, and require user approval for purchases. <br>


## Reference(s): <br>
- [Ntriq x402 document service homepage](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-document-intel-batch) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results depend on remote document analysis for the requested image URLs and analysis type.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
