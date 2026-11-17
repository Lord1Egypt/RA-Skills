## Description:

Automates Meta Business Suite workflows through the Graph API for publishing, scheduling, analytics, comment management, uploads, and post deletion on Facebook Pages and Instagram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nachx639](https://clawhub.ai/user/nachx639)

### License/Terms of Use:


## Use Case:

Developers and social media operators use this skill to guide an agent through Meta Graph API actions for Facebook Page and Instagram business account publishing, scheduling, analytics, comment management, media upload, and deletion workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meta account tokens can authorize actions against real Facebook Pages and Instagram business accounts.

Mitigation: Use least-privilege Meta tokens, prefer environment variables or a tightly protected cache, avoid putting access tokens in URLs, and review the skill before connecting a real business account.

Risk: Publishing, commenting, scheduling, or deleting content can change public business account state.

Mitigation: Require explicit user confirmation before executing publish, comment, schedule, or delete commands.

## Reference(s):

- [Meta Graph API documentation](https://developers.facebook.com/docs/graph-api)
- [ClawHub skill page](https://clawhub.ai/nachx639/skills/meta-business-suite)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, python3, META_PAGE_ACCESS_TOKEN, and META_PAGE_ID; examples target Meta Graph API v25.0.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
