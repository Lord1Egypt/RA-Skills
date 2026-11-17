## Description:

Generate professional fashion and product advertising images with AI models holding or wearing products.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

Marketing and creative teams use this skill to generate product advertising visuals that place a selected product with a human model in a directed fashion or campaign scene. Agents can use it to prepare creative briefs, choose style and camera packs, upload product and model references, and run the remote image generation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product/model images and campaign text are sent to ComfyDeploy for remote generation.

Mitigation: Use only inputs that are approved for third-party processing and avoid confidential or sensitive imagery unless the external service terms permit that use.

Risk: The bundled script can invoke a local usage tracker if ~/clawd/scripts/track-usage.sh exists, passing prompt and result metadata.

Mitigation: Review, remove, or disable the tracker before installation when usage telemetry is not desired.

Risk: The security scan verdict is suspicious because the script performs the advertised generation work while also including undisclosed usage tracking behavior.

Mitigation: Review the skill before deployment, pin dependencies, and run it in an environment where outbound network access and local helper scripts are controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/morpheus-fashion-design)
- [Model catalog referenced by skill](https://github.com/PauldeLavallaz/model_management)
- [ComfyDeploy queue endpoint referenced by skill](https://api.comfydeploy.com/api/run/deployment/queue)
- [ComfyDeploy upload endpoint referenced by skill](https://api.comfydeploy.com/api/file/upload)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with command examples and a generated PNG image file when the helper script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires product and model image inputs plus a campaign brief and target audience; the helper script uploads images to ComfyDeploy and downloads the generated image.]

## Skill Version(s):

1.4.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
