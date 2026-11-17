## Description:

Build and qualify local-business prospect lists by category and geography using Crawlora's Google Maps dataset, live Google Maps, Apple Maps, Yelp, and public business websites. Use when the user wants a deduplicated lead shortlist or CSV with business contacts and qualification evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, researchers, and other business users can build deduplicated local-business prospect lists for a chosen category and geography, with qualification criteria and source evidence. The skill returns a shortlist or CSV and does not authorize outreach or CRM imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the service requires sending a Crawlora API key with requests to Crawlora.

Mitigation: Provide a key only if you choose to use the service; keep it in the environment and use the bundled helper, which sends it over HTTPS and removes its temporary restricted-permission curl config on exit.

Risk: The security scan was partial because it could not resolve one local path-like reference.

Mitigation: Review the unresolved reference before deployment; the scan guidance notes that its evidence is incomplete.

## Reference(s):

- [Endpoint reference](artifact/reference/endpoints.md)
- [Crawlora](https://crawlora.net)
- [ClawHub skill page](https://clawhub.ai/crawlora-org/skills/local-business-prospecting)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV]

**Output Format:** [Markdown table or CSV, with source evidence and qualification details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deduplicated shortlist with requested business details, qualification evidence, source URLs, retrieval time, and refresh status.]

## Skill Version(s):

1.0.16 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
