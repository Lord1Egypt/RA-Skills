## Description:

Connect and control ComfyUI through OpenClaw using reusable workflow templates, prompt injection, asset upload, result polling, and local output management for image generation and editing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salmonrk](https://clawhub.ai/user/salmonrk)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to let an OpenClaw agent submit text-to-image and image-editing jobs to a ComfyUI server, using template IDs instead of sending complete workflow JSON in prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A ComfyUI server can influence downloaded filenames and cause local writes without safe path checks.

Mitigation: Constrain downloads to an approved output directory, normalize filenames, and reject path traversal or unexpected path components before use.

Risk: Media uploaded for image editing leaves the local workspace and is sent to the configured ComfyUI server.

Mitigation: Use only trusted ComfyUI endpoints and avoid private or sensitive media unless that transfer is acceptable.

Risk: Running the skill against a remote or shared endpoint increases exposure to untrusted responses.

Mitigation: Review the skill before installation and prefer local or controlled ComfyUI servers until download path handling is fixed or constrained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/salmonrk/skills/openclaw-comfyui)
- [artifact/README.md](artifact/README.md)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/manifest.json](artifact/manifest.json)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI responses that report generated file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses template IDs for bundled ComfyUI workflows and can download generated outputs to the local workspace.]

## Skill Version(s):

1.0.4 (source: server release metadata and artifact/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
