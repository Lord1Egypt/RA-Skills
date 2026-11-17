## Description:

Posta helps agents create, upload, schedule, publish, and analyze social media content across Instagram, TikTok, LinkedIn, YouTube, X/Twitter, Facebook, Pinterest, Threads, and Bluesky.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stgime](https://clawhub.ai/user/stgime)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage social media workflows from an agent: authenticate with Posta, create captions and media, upload assets, schedule or publish posts, inspect platform limits, and review analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posta credentials, fal.ai credentials, and cached tokens can expose social media accounts if stored carelessly.

Mitigation: Prefer POSTA_API_TOKEN, keep Posta and fal.ai credentials out of project .env files, and clear /tmp/.posta_token after use.

Risk: Publish, schedule, and delete actions can change live social media content or account state.

Mitigation: Require explicit user confirmation before publishing, scheduling, deleting, or changing TikTok privacy settings.

Risk: Image generation sends prompts and campaign context to fal.ai and may spend API credits.

Mitigation: Confirm before calling fal.ai and avoid sending confidential prompts or unreleased campaign content unless external sharing is acceptable.

Risk: Changing POSTA_BASE_URL can redirect authenticated API calls away from the production Posta API.

Mitigation: Set POSTA_BASE_URL only for trusted development environments.

## Reference(s):

- [Posta ClawHub Skill Page](https://clawhub.ai/stgime/skills/posta)
- [Posta API Reference](references/posta-api-reference.md)
- [Content Generation Patterns](references/content-generation.md)
- [Workflow Examples](examples/workflows.md)
- [fal.ai API Keys](https://fal.ai/dashboard/keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON request bodies, and formatted analytics summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Posta and fal.ai APIs when credentials are configured and the user confirms actions that publish, schedule, delete, or spend image-generation credits.]

## Skill Version(s):

1.4.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
