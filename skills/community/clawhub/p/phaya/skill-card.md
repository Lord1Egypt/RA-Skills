## Description:

Phaya Media API helps agents use the Phaya SaaS backend to generate images, videos, audio, music, embeddings, and LLM chat completions through authenticated REST API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boombignose](https://clawhub.ai/user/boombignose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and external users use this skill to call a Phaya-hosted API for media generation, LLM chat, embeddings, media utilities, and account credit checks. It is most useful when an agent needs concrete endpoint guidance, request schemas, polling patterns, curl commands, or Python examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generation endpoints can spend real Phaya credits, and video jobs can be materially more expensive than basic image tests.

Mitigation: Use a scoped API key with a small credit balance, check credits before use, start with low-cost endpoints, and confirm expensive generation jobs before submitting them.

Risk: Prompts, uploaded media, and third-party media URLs may be sent to Phaya and upstream providers.

Mitigation: Avoid private prompts, regulated data, unpublished media, and third-party video URLs unless the user accepts the applicable data handling.

Risk: Account, upload/download, and cache-invalidation endpoints can expose account data or create side effects beyond simple generation.

Mitigation: Review the exact endpoint and inputs before use, keep credentials least-privilege where possible, and avoid account or cache operations unless explicitly requested.

## Reference(s):

- [Phaya Media API on ClawHub](https://clawhub.ai/boombignose/skills/phaya)
- [Endpoint Reference](artifact/endpoints.md)
- [Usage Examples](artifact/examples.md)
- [Agent Quickstart](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request bodies, Python examples, and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PHAYA_API_KEY and PHAYA_BASE; API calls can return job IDs, polling statuses, media URLs, chat text, embeddings, and account credit data.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
