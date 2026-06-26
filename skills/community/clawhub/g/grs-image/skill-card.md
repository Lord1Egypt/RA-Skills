## Description: <br>
GrsAI Nano Banana Pro image generation skill that uses the GrsAI API to create images from Chinese or English prompts for interior design renders, launch posters, and design materials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapleslove](https://clawhub.ai/user/mapleslove) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and agents use this skill to generate GrsAI images from prompts, choose model, aspect ratio, and resolution settings, and save the generated image locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are submitted to GrsAI for processing. <br>
Mitigation: Avoid sending confidential prompts, personal images, internal URLs, or regulated data unless that external processing is acceptable. <br>
Risk: The script reads an API key from the environment and uses it for GrsAI requests. <br>
Mitigation: Keep GRSAAI_API_KEY private and run the skill only in a trusted Python environment. <br>
Risk: The selected output path can overwrite files accessible to the current user. <br>
Mitigation: Choose output filenames carefully and review paths before running commands that save generated images. <br>


## Reference(s): <br>
- [GrsAI Nano Banana API documentation](https://grsai.ai/zh/dashboard/documents/nano-banana) <br>
- [Interior design prompt templates](references/prompts.json) <br>
- [ClawHub skill page](https://clawhub.ai/mapleslove/grs-image) <br>


## Skill Output: <br>
**Output Type(s):** [files, shell commands, guidance] <br>
**Output Format:** [PNG image files saved to disk, with terminal status text and generated image URL output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GRSAAI_API_KEY and network access to GrsAI; supports prompt, model, aspect ratio, resolution, output path, and optional reference image URLs or Base64 input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
