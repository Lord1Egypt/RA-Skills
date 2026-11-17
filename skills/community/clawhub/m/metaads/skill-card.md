## Description:

Manage Meta ad campaigns by reading, creating, updating campaigns, ad sets, ads, creatives, and retrieving insights via the Marketing API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otman-ai](https://clawhub.ai/user/otman-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketing operations teams use this skill to have agents retrieve campaign data, create paused campaigns, ad sets, ads, and creatives, and analyze Meta ads performance through the Marketing API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents toward live ad-changing actions such as create, update, pause, and scale.

Mitigation: Require explicit approval before create, update, pause, or scale actions, and keep newly created ad objects paused until reviewed.

Risk: Unsafe token handling or broad response logging could expose sensitive account and advertising data.

Mitigation: Use Authorization headers rather than URL tokens, prefer read-only tokens unless writes are required, and redact or disable full response logging.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/otman-ai/skills/metaads)
- [Meta Graph API v19.0 endpoint](https://graph.facebook.com/v19.0/)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration, markdown]

**Output Format:** [Markdown with endpoint, payload, and workflow examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Meta Marketing API requests and performance recommendations; write actions should require approval.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
