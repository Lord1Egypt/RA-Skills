## Description: <br>
Extract text, classify document type, and pull tables from any document image. Pay $0.05 USDC per call via x402 (no API key needed). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent users use this skill to call a paid document intelligence service for text extraction, document classification, summarization, and table extraction from document images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends document images to an external paid document-processing service, despite artifact text claiming no cloud upload. <br>
Mitigation: Treat the service as external processing and do not submit confidential or regulated documents unless that use is approved. <br>
Risk: Using the skill can initiate x402 wallet payments. <br>
Mitigation: Confirm the destination, network, amount, and each wallet payment before sending a request. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ntriq-gh/ntriq-x402-document-intel) <br>
- [Publisher profile](https://clawhub.ai/user/ntriq-gh) <br>
- [ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API request parameters, payment header guidance, and example response structures.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
