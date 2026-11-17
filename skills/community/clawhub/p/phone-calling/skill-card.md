## Description:

Make international phone calls to any country. Low per-minute rates. Pay with PayPal or UPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adisahani](https://clawhub.ai/user/adisahani)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to place and manage paid international phone calls through Ringez, including balance checks, call initiation, status checks, hangup, call history, and DTMF actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad power to initiate real phone calls that may contact unintended recipients or incur costs.

Mitigation: Require explicit user confirmation of the destination number, call mode, and possible cost before each call; check balance first and use an idempotency key for call initiation.

Risk: Direct or automated calling can bypass the user's phone and reduce user control over live outreach.

Mitigation: Keep bridge mode as the normal path and enable direct or bulk-style calling only after deliberate approval for the specific use case.

Risk: DTMF actions can transmit sensitive information such as PINs, passwords, OTPs, or banking secrets.

Mitigation: Do not send secrets through DTMF; for sensitive menus, instruct the user to enter values themselves through a trusted channel.

Risk: Transcription, recording, sentiment analysis, and webhooks can expose call content and participant data.

Mitigation: Enable these features only after confirming participant consent, retention requirements, and webhook security controls such as HTTPS and signature verification.

Risk: Session IDs, API keys, and webhook secrets can authorize calls or expose call data if mishandled.

Mitigation: Store credentials in protected secret storage, avoid logging them, rotate exposed keys, and prefer pinned, verified SDK versions or the scoped REST API.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adisahani/skills/phone-calling)
- [Ringez OpenAPI Specification](artifact/openapi.json)
- [Ringez API Specification](artifact/ringez-api-spec.md)
- [Ringez Quick Start Guide](artifact/ringez-quickstart-guide.md)
- [Ringez Implementation Guide](artifact/ringez-implementation-guide.md)
- [Ringez Production API](https://ringez-api.vercel.app/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP, JSON, Python, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, request examples, and setup guidance requiring a Ringez session or API key.]

## Skill Version(s):

1.0.7 (source: server evidence, frontmatter, CHANGELOG, and OpenAPI; released 2026-02-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
