## Description:

Extract structured data from product pages, job listings, and company pages, and generate working AI endpoints from schemas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[renoblabs](https://clawhub.ai/user/renoblabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to call paid extraction micro-services that turn product, job, and company pages into structured data, or generate FastAPI endpoint code from schemas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target URLs or schemas are sent to a paid external service.

Mitigation: Confirm the user is comfortable sharing those inputs before invoking the service.

Risk: Contact extraction may collect emails and phone numbers.

Mitigation: Use contact extraction only on lawfully obtained pages and for legitimate business purposes.

Risk: Generated FastAPI code may be incomplete or unsafe to run as-is.

Mitigation: Review and test generated code before execution or deployment.

## Reference(s):

- [High-Value Extractors on ClawHub](https://clawhub.ai/renoblabs/skills/high-value-extractors)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples; endpoint responses are JSON and may include code strings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid x402 endpoints; contact extraction may return emails and phone numbers.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
