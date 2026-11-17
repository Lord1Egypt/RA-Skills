## Description:

NotaryOS seals AI agent actions and declined actions with Ed25519 cryptographic receipts for later verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellothere012](https://clawhub.ai/user/hellothere012)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use NotaryOS to issue, verify, look up, and chain cryptographic receipts for agent actions, file changes, commands, configuration changes, API calls, and declined actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected action payloads and metadata to an external NotaryOS service.

Mitigation: Use it only when external receipt issuance is acceptable, and manually allowlist safe receipt fields before sealing actions.

Risk: The included sanitizer does not provide complete privacy protection for all sensitive data.

Mitigation: Avoid sending raw message bodies, file contents, credentials, authentication headers, health data, financial data, or other sensitive fields.

Risk: The installed notaryos SDK is an external dependency used to contact the receipt service.

Mitigation: Pin and audit the SDK version before use in production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hellothere012/skills/notaryos)
- [NotaryOS GitHub Repository](https://github.com/hellothere012/notaryos)
- [NotaryOS Documentation](https://notaryos.org/docs)
- [NotaryOS API Documentation](https://notaryos.org/api-docs)
- [notaryos on PyPI](https://pypi.org/project/notaryos/)
- [notaryos on npm](https://www.npmjs.com/package/notaryos)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sanitized payload examples, receipt verification guidance, and SDK configuration notes.]

## Skill Version(s):

2.4.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
