## Description: <br>
Batch detect and mask PII across up to 500 text inputs. Flat $6.00 USDC via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ntriq-gh](https://clawhub.ai/user/ntriq-gh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance teams use this skill to submit batches of text to a paid x402 PII-detection service, receive per-input findings, and optionally receive masked text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text and payment authorization are sent to the provider's remote API. <br>
Mitigation: Only submit data approved for this provider, and confirm privacy, logging, retention, deletion, and payment practices before use. <br>
Risk: The skill can initiate a paid $6 USDC batch request through x402. <br>
Mitigation: Require explicit operator approval before sending an X-PAYMENT header or otherwise authorizing payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ntriq-gh/ntriq-x402-pii-detect-batch) <br>
- [Ntriq x402 homepage](https://x402.ntriq.co.kr) <br>
- [PII detect batch endpoint](https://x402.ntriq.co.kr/pii-detect-batch) <br>
- [Ntriq x402 services](https://x402.ntriq.co.kr/services) <br>
- [x402 protocol](https://x402.org) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline HTTP, JSON, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes a batch API that returns JSON PII findings and optional masked text.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
