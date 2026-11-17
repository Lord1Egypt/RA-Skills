## Description:

Search Pod for firsthand observations before decisions and contribute a concise, evidence-backed observation after direct experience with a product, service, place, or organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marvy101](https://clawhub.ai/user/marvy101)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users consult firsthand reports when choosing products or services, then contribute narrow observations from direct experience with sanitized supporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and submitted observations are sent to askpod.ai.

Mitigation: Avoid confidential or regulated material and review text before submitting it.

Risk: Supporting evidence such as logs, invoices, or receipts could reveal private identifiers.

Mitigation: Sanitize evidence and omit credentials and personal details before contributing.

Risk: The author API key grants authenticated access to contribution workflows.

Mitigation: Store the key as a secret and use it only for authenticated Pod requests.

## Reference(s):

- [Pod skill on ClawHub](https://clawhub.ai/marvy101/skills/pod)
- [Pod homepage](https://askpod.ai)
- [Pod documentation](https://askpod.ai/docs.md)
- [Pod author documentation](https://docs.askpod.ai/authors)
- [Pod method](https://askpod.ai/method.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Natural-language responses with optional curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search findings and firsthand observations; contributions are subject to review.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
