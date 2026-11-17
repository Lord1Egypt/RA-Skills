## Description:

Mixpost is a self-hosted social media management software that helps you schedule and manage your social media content across multiple platforms including Facebook, Twitter/X, Instagram, LinkedIn, Pinterest, TikTok, YouTube, Mastodon, Google Business Profile, Threads, Bluesky, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lao9s](https://clawhub.ai/user/lao9s)

### License/Terms of Use:


## Use Case:

Social media managers and operators use this skill to let an agent prepare Mixpost API requests for managing accounts, media, tags, and posts in a self-hosted Mixpost workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a user-provided Mixpost token that can operate a workspace.

Mitigation: Use the least-privileged Mixpost token available and store it only in the intended agent environment.

Risk: Create, publish, approve, schedule, and delete requests can affect live social media content.

Mitigation: Review proposed requests before execution, especially actions that publish immediately or delete content from Mixpost or connected social accounts.

Risk: A misconfigured Mixpost URL could send requests to the wrong instance.

Mitigation: Confirm MIXPOST_URL points to the intended self-hosted Mixpost instance before using the skill.

## Reference(s):

- [Mixpost homepage](https://mixpost.app)
- [Mixpost skill on ClawHub](https://clawhub.ai/lao9s/skills/mixpost)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MIXPOST_URL, MIXPOST_ACCESS_TOKEN, and MIXPOST_WORKSPACE_UUID supplied by the user.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
