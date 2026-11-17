## Description:

Create tamper-proof receipts for AI agent work by hashing artifacts or action manifests, posting them to api.mpps.io, and receiving an HSM-signed receipt without an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gdlg-ai](https://clawhub.ai/user/gdlg-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to create externally verifiable receipts for completed work, artifact hashes, action manifests, release bundles, or delivery workflows. It is useful when an audit trail or later verification URL is needed without adding an SDK or API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Receipt examples can send artifact labels, local paths, repository names, and commit identifiers to the external mpps.io service.

Mitigation: Use opaque labels such as "artifact" and omit repository or commit context unless that metadata is intentionally being recorded.

Risk: Sensitive data could be exposed if users place secrets, customer data, private source text, raw prompts, or unsalted hashes of short secrets in receipt context.

Mitigation: Send only non-sensitive hashes and labels, keep private content out of the request body, and salt short-secret hashes before attestation.

Risk: The skill depends on outbound network calls to api.mpps.io.

Mitigation: Review the exact request payload and confirm the deployment environment permits the external call before using the generated commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gdlg-ai/skills/mpps-attestation)
- [Mpps skills homepage](https://mpps.io/skills)
- [mpps.io](https://mpps.io)
- [Skill-declared API documentation](https://github.com/gdlg-ai/mpps.io/blob/main/docs/api.md)
- [Skill-declared verification documentation](https://github.com/gdlg-ai/mpps.io/blob/main/docs/verify.md)
- [Skill-declared security policy](https://github.com/gdlg-ai/mpps.io/blob/main/SECURITY.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks, plus JSON API response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl or another HTTP client and network access to api.mpps.io.]

## Skill Version(s):

1.4.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
