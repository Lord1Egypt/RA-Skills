## Description: <br>
Still-to-video conversion guide: model selection, motion prompting, and camera movement for animating images, creating video from stills, adding motion, and product animations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okaris](https://clawhub.ai/user/okaris) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and production teams use this skill to choose image-to-video models, write motion prompts, and run inference.sh commands that animate still images into short videos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on a third-party CLI installer and account login. <br>
Mitigation: Review the installer path, prefer manual download with checksum verification, and approve infsh commands before running them. <br>
Risk: Images and prompts may be sent to external model providers during inference. <br>
Mitigation: Avoid private images or sensitive prompts unless the data-sharing behavior is acceptable for the use case. <br>


## Reference(s): <br>
- [inference.sh](https://inference.sh) <br>
- [inference.sh CLI installer](https://cli.inference.sh) <br>
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt) <br>
- [ClawHub skill page](https://clawhub.ai/okaris/image-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and model selection tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes inference.sh command examples and prompt patterns for image-to-video workflows.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
