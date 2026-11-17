## Description:

Paper Rewrite is a paid Chinese-language academic paper rewriting skill that sends submitted manuscript text to a remote AI service to reduce textual similarity while preserving the original meaning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2789-bin](https://clawhub.ai/user/2789-bin)

### License/Terms of Use:

MIT-0

## Use Case:

External users can submit Chinese academic paper text for AI-assisted rewriting intended to reduce textual similarity while preserving the original meaning. The service is paid per request and may return payment authorization details before producing a rewrite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted paper text is sent to a third-party paid remote service.

Mitigation: Do not submit confidential, unpublished, personal, or institution-restricted papers unless the user explicitly accepts sending that text to the service.

Risk: The service call disables normal TLS certificate validation.

Mitigation: Review before installing and avoid routine use until the service uses normal TLS certificate validation and clear data handling terms.

Risk: The skill can request payment authorization before returning rewrite output.

Mitigation: Require explicit user confirmation before each paid use and avoid payment authorization unless the user understands the charge.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2789-bin/skills/paper-rewrite)
- [Service homepage](https://192.144.154.90/demo/a2m/resource)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON response containing rewritten text or payment-required details, with agent-facing prose guidance as needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single requests support up to 30000 characters; payment authorization may be required before rewrite output is returned.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
