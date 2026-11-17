## Description:

Helps agents search MJZJ SkillHub and ClawHub skills, filter free, paid, popular, and recent listings, provide installation guidance, and submit MJZJ skill publishing applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjzj-tec](https://clawhub.ai/user/mjzj-tec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover MJZJ SkillHub and ClawHub marketplace skills, compare labels and pricing, get installation guidance, and prepare skill publishing submissions for MJZJ review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated upload and publishing actions require an MJZJ API key.

Mitigation: Configure MJZJ_API_KEY only when those actions are intended, and update the key through the MJZJ user center if authorization fails.

Risk: Publishing applications send skill metadata, source URL, labels, price type, tags, and any cover image to MJZJ for review.

Mitigation: Review those fields with the user before submitting a publishing application.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mjzj-tec/skills/mjzj-skillhub)
- [MJZJ SkillHub](https://skillhub.mjzj.com)
- [MJZJ Agent API Key page](https://mjzj.com/user/agentapikey)
- [MJZJ skill label groups API](https://data.mjzj.com/api/skill/groupLabels)
- [MJZJ skill query API](https://data.mjzj.com/api/skill/query)
- [MJZJ temporary upload API](https://data.mjzj.com/api/common/applyUploadTempFile)
- [MJZJ skill publishing application API](https://data.mjzj.com/api/skillManage/applyNew)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API request examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated upload and publishing actions require MJZJ_API_KEY; public search actions do not require authentication.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
