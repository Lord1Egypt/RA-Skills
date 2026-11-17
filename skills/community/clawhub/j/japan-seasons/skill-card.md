## Description:

Query Japanese seasonal travel data, including cherry blossom forecasts, autumn foliage tracking, and festival search, using the Japan Seasons API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ko-syun](https://clawhub.ai/user/ko-syun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer Japan travel timing questions by calling the Japan Seasons API for sakura, kouyou, and matsuri data, then summarizing the results for users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an API key and Japan travel queries to jpseasons.dokos.dev.

Mitigation: Confirm the deployment trusts jpseasons.dokos.dev before installing or using the skill, and keep the API key in an environment variable or request header rather than user-visible text.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/ko-syun/skills/japan-seasons)
- [Japan Seasons API](https://jpseasons.dokos.dev)
- [Japan Seasons API dashboard](https://jpseasons.dokos.dev/dashboard)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and summarized JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an X-API-Key header for API requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
