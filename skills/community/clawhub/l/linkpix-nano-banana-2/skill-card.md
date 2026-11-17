## Description:

Creates and edits e-commerce product images with the Nano Banana 2 workflow for Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce operators, advertisers, and sellers use it to create or adapt product images for listings and advertising creatives.

### Deployment Geography for Use:

China (uses the domestic Qinghu AI service)

## Known Risks and Mitigations:

Risk: Automatic global upgrades and tool-provided upgrade commands can change the installed dependency.

Mitigation: Review the exact upgrade command before running it and prefer a reviewed, fixed dependency version.

Risk: An API key could be exposed if shared in chat, and image workflows can send images or prompts for external processing.

Mitigation: Configure the API key locally and use only images authorized for external processing, including prompt polishing.

Risk: Executable dependency behavior and service data retention are unverified.

Mitigation: Review dependencies and confirm service data handling before using sensitive images or prompts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/linkpix-nano-banana-2)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Images, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Generated image assets; Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image count, model, size, and quality are selected from the available qhkit options.]

## Skill Version(s):

0.1.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
