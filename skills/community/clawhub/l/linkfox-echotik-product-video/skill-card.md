## Description:

Queries promotional videos associated with a TikTok Shop product and helps sellers analyze engagement, estimated sales, GMV, creator, and publishing signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and agent users use this skill to inspect TikTok product promotional videos, compare engagement and estimated conversion metrics, and identify creator content linked to a product ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends product queries, API keys, and session metadata to LinkFox endpoints.

Mitigation: Use it only when LinkFox is trusted for the business data involved, and protect or rotate API keys if exposed.

Risk: The onboarding flow can ask for phone-number login, SMS verification, API-key generation, plan selection, and payment order creation.

Mitigation: Prefer obtaining an API key directly from the first-party LinkFox site, and require the user to confirm any paid plan or order action.

Risk: Endpoint override environment variables could redirect requests away from the expected LinkFox services.

Mitigation: Avoid setting endpoint override variables unless they are intentionally reviewed for the current environment.

Risk: The skill writes API responses and cache/session files locally, which may contain sensitive product or account context.

Mitigation: Periodically review and delete local LinkFox cache and session files when they are no longer needed.

## Reference(s):

- [EchoTik product video API reference](references/api.md)
- [Authentication and billing onboarding guide](references/onboarding.md)
- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-echotik-product-video)
- [LinkFox Skills](https://skill.linkfox.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API results and saved JSON data files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can write full API responses to local LinkFox session data files and print either full JSON or summaries depending on response size.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
