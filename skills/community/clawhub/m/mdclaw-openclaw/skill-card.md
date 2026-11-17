## Description:

MDClaw OpenClaw provides a Python client and agent-facing guidance for text-to-speech, text-to-image, text-to-video, image-to-video, image upload, search, weather, and webpage-summary calls through the MDClaw gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnskycn](https://clawhub.ai/user/cnskycn)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to call the MDClaw OpenClaw gateway for multimodal media generation and utility tasks, including API-key registration, image uploads, asynchronous video polling, and downloading generated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, webpage URLs, uploaded image files, registration details, and API-authenticated requests are sent to an external MDClaw gateway.

Mitigation: Use the skill only with approved data, avoid sensitive files or private URLs, and confirm users are comfortable sending requests to the documented gateway.

Risk: Example scripts may print API-key prefixes and generated media URLs to logs.

Mitigation: Avoid sharing logs from example runs and treat generated media URLs and API-key snippets as sensitive operational data.

Risk: Download helpers write generated image or video content to caller-provided output paths.

Mitigation: Choose output paths deliberately and review generated media before distributing or using it in downstream workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnskycn/skills/mdclaw-openclaw)
- [MDClaw OpenClaw gateway endpoint](https://backend.appmiaoda.com/projects/supabase287606411725160448/functions/v1/openclaw-skill-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON-like API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce URLs for generated audio, images, videos, uploaded files, task identifiers, and downloaded local files.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
