## Description:

Generate AI images with Nano Banana Pro through the Media.io OpenAPI, including prompt-based generation, reference-image workflows, multi-image fusion, character consistency, and up to 4K output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wondershare-boop](https://clawhub.ai/user/wondershare-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to submit Nano Banana Pro image-generation jobs through Media.io, poll task results, and integrate generated image workflows using a Media.io API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Media.io API key can submit generation jobs and query account credit balance.

Mitigation: Use a dedicated, least-privilege Media.io key where available and monitor account usage.

Risk: Running scripts/skill_router.py directly performs the Credits query rather than an image-generation request.

Mitigation: Run the script directly only when you intend to query credits; otherwise invoke the documented Nano Banana Pro or Task Result APIs from controlled code.

Risk: The skill depends on the Python requests package without pinned dependency versions.

Mitigation: Install dependencies in a virtual environment and pin reviewed package versions for production use.

## Reference(s):

- [Media.io API documentation](https://platform.media.io/docs/)
- [Media.io developer homepage](https://developer.media.io/)
- [Media.io pricing](https://developer.media.io/pricing.html)
- [ClawHub skill page](https://clawhub.ai/wondershare-boop/skills/mediaio-nano-banana-pro-image-generator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; API calls return JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Media.io API key in API_KEY or an explicit api_key argument.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
