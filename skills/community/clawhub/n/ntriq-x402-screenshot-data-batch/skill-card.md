## Description: <br>
Batch extract text, UI elements, and data from up to 500 screenshots. Flat $6.00 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to call Ntriq's x402 screenshot extraction API, sending batches of screenshot URLs for text, UI element, layout, and table extraction into JSON analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Screenshots are sent to a third-party service and may contain sensitive UI content or data. <br>
Mitigation: Only submit screenshot URLs approved for sharing with Ntriq, and avoid secrets, personal data, or proprietary material unless authorized. <br>
Risk: Using the endpoint requires a flat $6.00 USDC x402 payment. <br>
Mitigation: Confirm the payment amount, Base mainnet use, and x402 payment header before sending requests. <br>
Risk: Provider-side local inference does not mean screenshots remain on the user's own machine. <br>
Mitigation: Treat processing as third-party provider processing unless Ntriq supplies separate data-handling commitments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ntriq-gh/ntriq-x402-screenshot-data-batch) <br>
- [Ntriq x402 Homepage](https://x402.ntriq.co.kr) <br>
- [x402 Protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, shell commands, JSON] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts up to 500 screenshot URLs with optional extract_type and language parameters; returns per-image analysis results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
