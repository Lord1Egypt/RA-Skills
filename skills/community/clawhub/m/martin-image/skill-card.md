## Description:

Run and customize local ComfyUI workflows via HTTP API to generate images from prompts, run user workflows, or download model weights for use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godferylindsay](https://clawhub.ai/user/godferylindsay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and image-generation users use this skill to run local ComfyUI workflows, adjust prompts or workflow JSON, download model weights, and retrieve generated image outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can fetch user-supplied model URLs and may install the pget binary automatically.

Mitigation: Use an isolated local account or environment, prefer --no-pget, and download only trusted HTTPS model URLs with known checksums.

Risk: Downloaded model files are written under the configured ComfyUI models directory and can overwrite existing files when overwrite behavior is enabled.

Mitigation: Review the destination subfolder under ~/ComfyUI/models before downloading and avoid overwrite mode unless replacement is intentional.

Risk: The skill can run local or user-supplied ComfyUI workflow JSON through the local ComfyUI API.

Mitigation: Inspect workflow JSON before execution and run workflows only in an isolated local ComfyUI environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/godferylindsay/skills/martin-image)
- [SkillBoss setup guide](https://skillboss.co/skill.md)
- [pget downloader](https://github.com/replicate/pget)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, workflow JSON edits, script output JSON, and generated image file references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reachable local ComfyUI server and may write downloaded model weights under the configured ComfyUI models directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
