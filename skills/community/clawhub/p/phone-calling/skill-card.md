## Description: <br>
Make international phone calls to any country. Low per-minute rates. Pay with PayPal or UPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adisahani](https://clawhub.ai/user/adisahani) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent place international phone calls, check balances and call status, end calls, send DTMF tones, and retrieve call history through the Ringez API. It is best suited to user-approved personal, appointment, reservation, or support calls where destination, consent, expected cost, and maximum duration are confirmed before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can initiate paid external phone calls and consume account balance. <br>
Mitigation: Require explicit approval for each destination number, call mode, expected cost, maximum duration, and whether DTMF or transcription will be used before initiating a call. <br>
Risk: Calls, DTMF digits, transcripts, recordings, and webhook payloads may contain sensitive personal or business information. <br>
Mitigation: Confirm participant consent where required, avoid unnecessary transcription or recording, use HTTPS and verified webhook signatures, and limit transcript or webhook forwarding to approved systems. <br>
Risk: Batch campaigns, sales outreach, or automated dialing can create consent, telecom, and abuse risks. <br>
Mitigation: Avoid campaign and sales use unless consent, legal compliance, rate limits, SDK provenance, and Ringez data-retention controls have been verified. <br>
Risk: Retries or repeated user actions can create duplicate calls. <br>
Mitigation: Use a fresh idempotency key for each user-approved call attempt and reuse it only for network retries within the documented deduplication window. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adisahani/phone-calling) <br>
- [Ringez API Base URL](https://ringez-api.vercel.app/api/v1) <br>
- [OpenAPI Specification](artifact/openapi.json) <br>
- [Ringez API Specification](artifact/ringez-api-spec.md) <br>
- [Ringez Quick Start Guide](artifact/ringez-quickstart-guide.md) <br>
- [Ringez Implementation Guide](artifact/ringez-implementation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with HTTP, JSON, bash, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Ringez account credentials or session credentials; phone calls may consume paid minutes and can expose call metadata, DTMF digits, recordings, transcripts, or webhook payloads depending on enabled options.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter, changelog, openapi.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
