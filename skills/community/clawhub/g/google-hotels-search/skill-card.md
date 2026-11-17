## Description:

Search live Google Hotels stays by location, dates and occupancy, returned in one unified schema alongside every other booking platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stayingapi](https://clawhub.ai/user/stayingapi)

### License/Terms of Use:

MIT-0

## Use Case:

Travel agents, developers, and agent users use this skill to search Google Hotels stays by location, dates, occupancy, and filters through StayingAPI. It helps agents retrieve live lodging search results in a unified accommodation schema.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hotel-search details and StayingAPI account requests are sent to an external StayingAPI service.

Mitigation: Use the skill only when external API sharing is acceptable for the request, and prefer a sandbox key during evaluation.

Risk: The skill requires a StayingAPI key that could expose account access if stored in broadly readable shell configuration.

Mitigation: Store STAYINGAPI_KEY in the agent or runtime secret mechanism rather than a shared profile or checked-in file.

Risk: Live calls may consume paid credits or hit API rate limits during polling.

Mitigation: Review StayingAPI pricing before live use, honor Retry-After headers, back off between poll attempts, and cap polling attempts.

## Reference(s):

- [Authentication setup](references/auth-setup.md)
- [StayingAPI homepage](https://stayingapi.com)
- [StayingAPI documentation](https://stayingapi.com/docs)
- [StayingAPI OpenAPI contract](https://api.stayingapi.com/openapi.json)
- [StayingAPI pricing](https://stayingapi.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request details, JSON response handling notes, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires STAYINGAPI_KEY and network access to api.stayingapi.com; live calls may require async polling.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
