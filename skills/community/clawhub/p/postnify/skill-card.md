## Description:

Postnify helps agents schedule social media and chat posts across 28+ channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[postnifyhq](https://clawhub.ai/user/postnifyhq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide authenticated Postnify CLI workflows for discovering integrations, uploading media, creating or scheduling posts, managing post status, and reviewing analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions that create, schedule, upload media for, or delete public posts.

Mitigation: Require explicit user confirmation before any post creation, scheduling, media upload, status change, or deletion command is run.

Risk: The CLI installation source and version are under-scoped in the skill text.

Mitigation: Pin or verify the postnify CLI package version and source before installing or executing it.

Risk: A custom POSTNIFY_API_URL can redirect authenticated requests to an untrusted endpoint.

Mitigation: Use the default Postnify endpoint unless the custom endpoint is explicitly trusted and reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/postnifyhq/skills/postnify)
- [Postnify Website](https://postnify.com)
- [Postnify npm Package](https://www.npmjs.com/package/postnify)
- [Postnify API Endpoint](https://platform.postnify.com/api)
- [Postnify CLI Auth Endpoint](https://cli-auth.postnify.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance often includes commands that call the postnify CLI and may require OAuth2 or API-key authentication.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
