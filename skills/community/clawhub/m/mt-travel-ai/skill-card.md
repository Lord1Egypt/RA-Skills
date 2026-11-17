## Description:

mt-travel-ai helps agents handle travel planning and booking-related requests using Meituan travel supply for hotels, transport, attraction tickets, vacation products, and itinerary recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qy-zhang](https://clawhub.ai/user/qy-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-service agents can use this skill to answer travel requests, plan itineraries, find hotels, query flights or trains, and surface attraction tickets or vacation packages. The artifact limits use away from passport, visa, overseas-destination, and non-travel Meituan requests.

### Deployment Geography for Use:

Global, with behavior focused on Meituan-supported travel inventory.

## Known Risks and Mitigations:

Risk: A Meituan developer token may be exposed in the chat transcript or saved in plaintext local configuration.

Mitigation: Use a secure secret-entry and storage mechanism, avoid sharing real tokens in chat where possible, and rotate any token that may have been exposed.

Risk: The skill installs a globally available npm CLI without a pinned version.

Mitigation: Use a version-pinned or sandboxed CLI installation and review package provenance before enabling it for production use.

Risk: Travel outputs may be incomplete, stale, or unsuitable for a user's constraints if returned CLI data is accepted without review.

Mitigation: Review returned travel details, prices, links, and availability before booking or presenting them as final recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qy-zhang/skills/mt-travel-ai)
- [Meituan developer token page](https://developer.meituan.com/zh/v2/dev/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown travel responses with links, images, prices, ratings, and inline shell or configuration commands when setup is required.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may preserve CLI-returned Markdown details verbatim and may include user prompts for missing city, query, or credential setup.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
