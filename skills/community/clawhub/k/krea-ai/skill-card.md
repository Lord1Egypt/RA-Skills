## Description:

Generate images through the Krea.ai API using Nano Banana 2 by default, with support for Flux, Imagen 4, Seedream 3, Ideogram 3.0, Nano Banana Pro, and Nano Banana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomas-mikula](https://clawhub.ai/user/tomas-mikula)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit explicit image-generation prompts to Krea.ai, poll generation jobs at a controlled interval, and receive generated image URLs in the agent response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and provided image URLs are sent to Krea.ai using the configured KREA_API_TOKEN.

Mitigation: Use this skill only for prompts and source images that are appropriate to share with Krea.ai, and configure the token only in environments intended for Krea API use.

Risk: Generated image URLs may be shareable external links depending on Krea's hosting behavior.

Mitigation: Review returned URLs before redistributing them and avoid treating them as private storage locations.

Risk: Krea API rate limits can cause 429 responses or delayed jobs.

Mitigation: Follow the skill's limits: submit at most one job every 10 seconds, poll every 6 seconds, cap polling at 40 attempts, and wait before retrying after rate limits.

## Reference(s):

- [Krea API documentation](https://docs.krea.ai/developers/introduction)
- [Krea API token settings](https://krea.ai/settings/api-tokens)
- [ClawHub skill page](https://clawhub.ai/tomas-mikula/skills/krea-ai)
- [ClawHub publisher profile](https://clawhub.ai/user/tomas-mikula)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown text containing the selected model, a short result summary, and generated image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KREA_API_TOKEN; submitted prompts and image URLs are sent to Krea.ai.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
