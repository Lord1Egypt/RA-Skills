## Description:

Image Gen helps an agent generate or edit images from text prompts or reference images using the Nano-banana API, compress large outputs, and save results to the workspace image directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zweien](https://clawhub.ai/user/zweien)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to add text-to-image and image-to-image generation workflows that save generated images, preserve originals, and compress large files for sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script sources a local .env file, so unsafe contents could execute in the user's shell.

Mitigation: Install only from a trusted publisher, restrict .env permissions, inspect configuration before running, and prefer safer config parsing before deployment.

Risk: Prompts, reference images, and generated image URLs are sent to and retrieved from the configured external image API.

Mitigation: Do not use private, regulated, or sensitive images unless the API provider is trusted for that data, and require HTTPS endpoints.

Risk: The script trusts downloaded image URLs and writes output paths provided at runtime.

Mitigation: Constrain outputs to the workspace image directory and verify downloaded files are valid images before sharing or further processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zweien/skills/image-gen-skill)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Nano-banana API](https://api.imyaigc.top)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Text]

**Output Format:** [Generated or edited image files with textual status messages and configuration-driven shell/API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are timestamped; originals may be retained and files larger than 1MB are compressed when possible.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
