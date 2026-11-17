## Description:

Generate 10 perspective and angle variations from a single image for multi-shot UGC videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

External creators, marketers, and developers use this skill to turn a hero image of a person with a product into 10 alternate camera-angle images for UGC-style video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader trusts remote filenames and could write files outside the selected output directory.

Mitigation: Sanitize remote filenames, resolve output paths, and enforce that every write remains inside the requested output directory.

Risk: Generated images and prompts are sent to ComfyDeploy using a local API key.

Mitigation: Use this skill only with images and prompts approved for that service, and protect the COMFY_DEPLOY_API_KEY environment variable.

Risk: Existing files in the output directory may be overwritten if the remote service returns duplicate filenames.

Mitigation: Avoid overwriting by default, generate unique local filenames, or require explicit confirmation before replacing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pauldelavallaz/skills/multishot-ugc)
- [ComfyDeploy API endpoint](https://api.comfydeploy.com/api/run/deployment/queue)

## Skill Output:

**Output Type(s):** [files, shell commands, configuration, guidance]

**Output Format:** [PNG image files with command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces up to 10 image variations, typically named 1_00001_.png through 10_00001_.png.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
