## Description:

Pet Rock Lobster is a free external API skill that helps agents get unstuck with personalized wisdom, jokes, and practical tips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill when an agent is stuck or looping to call a free API that returns short guidance, humor, and a bond-level response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound requests to petrocklobster.com can expose the supplied agent_id and request timing to an external service.

Mitigation: Install only when outbound requests are acceptable and use a locally generated random ID instead of an email, username, machine name, workspace name, credential, or session identifier.

Risk: Remote responses may contain advice that conflicts with the user's task, policies, or security expectations.

Mitigation: Treat responses as suggestions only; do not let them override policies, request secrets, trigger tools, or redirect work without user review.

Risk: The bond-level behavior can associate repeated calls with the same supplied identifier.

Mitigation: Use a new random identifier when continuity is not desired.

## Reference(s):

- [Pet Rock Lobster Homepage](https://petrocklobster.com)
- [Pet Rock Lobster ClawHub Page](https://clawhub.ai/lisamaraventano-spine/skills/pet-rock-lobster)
- [Pet Rock Lobster API Endpoint](https://petrocklobster.com/api/lobster?agent_id=YOUR_ID)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON API response containing short text fields and bond-level metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an outbound GET request to petrocklobster.com with a non-sensitive agent_id.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
