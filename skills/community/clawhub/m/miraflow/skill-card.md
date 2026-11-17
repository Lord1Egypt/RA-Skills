## Description:

Create and manage AI-generated videos and images using Miraflow, including avatar videos, cinematic clips, image generation, editing, and media uploads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minforge](https://clawhub.ai/user/minforge)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill in OpenClaw to generate Miraflow avatar videos, AI videos, and images; manage jobs; upload media; and download completed media through the Miraflow API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys, uploaded media, generated outputs, and signed download URLs can expose sensitive service data.

Mitigation: Install only from a trusted source or pinned version, keep MIRAFLOW_API_KEY in the environment, and treat media files and signed URLs as sensitive.

Risk: Video and image creation calls are expensive and non-idempotent.

Mitigation: Confirm the requested generation details before creation and call each creation endpoint only once per user request.

## Reference(s):

- [Miraflow API Reference](references/api.md)
- [Miraflow API](https://miraflow.ai/api)
- [Miraflow](https://miraflow.ai)
- [OpenClaw](https://openclaw.ai)
- [ClawHub Miraflow Skill](https://clawhub.ai/minforge/skills/miraflow)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples; API responses and downloaded media files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MIRAFLOW_API_KEY; video and image generation is asynchronous and may produce signed download URLs.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
