## Description:

Scan any public web page for GDPR/CCPA/ePrivacy privacy and cookie-consent signals, with static-HTML limitations stated in the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foomworks](https://clawhub.ai/user/foomworks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site owners, and compliance reviewers use this skill to scan public web pages for observable privacy and cookie-consent signals before launch or during audits. It reports detected trackers, consent tooling, privacy and Do-Not-Sell links, cookie attributes, HTTPS status, risks, and concrete fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned URLs are sent to a remote third-party service.

Mitigation: Scan only public pages, and avoid private, sensitive, or unpublished URLs unless the service is trusted for that use.

Risk: Static HTML analysis cannot determine whether trackers fire before user consent or prove legal compliance.

Mitigation: Treat results as risk signals and follow up with browser-based testing and legal review for compliance decisions.

## Reference(s):

- [Privacy Scan ClawHub page](https://clawhub.ai/foomworks/skills/privacy-scan)
- [Publisher profile](https://clawhub.ai/user/foomworks)
- [Privacy Scan service](https://privacy-scan.foomworks.workers.dev)
- [Privacy Scan MCP endpoint](https://privacy-scan.foomworks.workers.dev/mcp)
- [Privacy Scan OpenAPI document](https://privacy-scan.foomworks.workers.dev/openapi.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries with optional JSON API responses and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one public URL; static HTML only; sends the scanned URL to a remote third-party service.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
