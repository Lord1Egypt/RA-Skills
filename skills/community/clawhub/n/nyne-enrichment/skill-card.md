## Description:

Enriches a person by email, phone, LinkedIn URL, or name using the Nyne API, returning identity, contact, social profile, work, education, and optional social post data through an async polling workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelfanous2](https://clawhub.ai/user/michaelfanous2)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to enrich a person profile from identifiers such as email, phone, LinkedIn URL, or name, then inspect returned contact, social, work, education, and optional social activity data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retrieve sensitive personal details through third-party enrichment.

Mitigation: Use it only with a legitimate basis for person enrichment and request the minimum fields needed for the task.

Risk: Newsfeed and AI-enhanced search can broaden the amount of personal and social activity data collected.

Mitigation: Prefer lite mode and avoid newsfeed or AI-enhanced search unless the added data is clearly necessary.

Risk: Example commands can expose credential prefixes and leave enrichment responses containing personal data in temporary files.

Mitigation: Replace credential-check and temp-file examples with local handling that does not print secrets or retain PII in /tmp.

## Reference(s):

- [Nyne API](https://api.nyne.ai)
- [Nyne Person Enrichment API](https://api.nyne.ai/person/enrichment)
- [ClawHub Skill Page](https://clawhub.ai/michaelfanous2/skills/nyne-enrichment)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands, curl examples, jq filters, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces asynchronous API request and polling guidance; returned fields are optional and depend on available enrichment data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
