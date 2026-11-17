## Description:

Create and edit Instagram Shop product posts, carousel stories, Reels covers, Stories, creator seeding assets and cohesive social-commerce grids.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, commerce teams, and developers use this skill to generate or edit Instagram social-commerce image assets for feed posts, carousels, Stories, Reels covers, creator seeding, and social ads while preserving product and brand consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials could be exposed or misused if a custom base URL or AI_HIVE_BASE_URL points to an untrusted endpoint.

Mitigation: Use the default AI Hive endpoint or a fully trusted endpoint, use a limited API key, and avoid passing credentials through shared shell history.

Risk: Downloaded generation results could be written outside the intended output folder under unsafe server-response or endpoint conditions.

Mitigation: Review the output directory before running downloads, prefer a dedicated working folder, and inspect generated file paths before using the assets.

Risk: Installing dependencies globally can affect the host Python environment.

Mitigation: Install requests and any supporting packages in a virtual environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/instagram-ins-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key portal](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with bash command examples; the CLI returns JSON task status and can download generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI Hive API credentials, optional reference images, batch generation, routing mode, output directory, and submit-only mode.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
