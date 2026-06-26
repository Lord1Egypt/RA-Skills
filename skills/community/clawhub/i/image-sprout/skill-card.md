## Description: <br>
Generate and iterate on images with consistent style and subject identity using Image Sprout projects, reusable reference images, derived guides, and persistent instructions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to set up Image Sprout projects, derive reusable style and subject guides from references, generate images through the CLI, and pass generated image paths to downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web UI has no authentication if exposed beyond a trusted network. <br>
Mitigation: Run the web UI on localhost or a private network only, and do not expose it to the public internet. <br>
Risk: Concurrent agents can collide if they rely on shared current-project state. <br>
Mitigation: Pass --project explicitly in agent workflows instead of relying on image-sprout project use. <br>
Risk: Generated image paths and CLI results may be consumed by later tools without review. <br>
Mitigation: Use --json output for structured handoff and review generated images before publishing or using them in production workflows. <br>


## Reference(s): <br>
- [Image Sprout on ClawHub](https://clawhub.ai/tmchow/image-sprout) <br>
- [Image Sprout homepage](https://github.com/tmchow/image-sprout) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output handling guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use Image Sprout JSON CLI output and image paths for downstream workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
