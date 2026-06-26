## Description: <br>
Edit or combine images by applying styles or elements from one image to another while preserving identity, pose, and lighting using the AtlasCloud Nanobanana model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guilherme-funchal](https://clawhub.ai/user/guilherme-funchal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and image-editing agents use this skill to call AtlasCloud Nanobanana image-to-image generation for tasks such as swapping clothing, combining reference images, or transferring visual style while preserving key subject details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requires an AtlasCloud API token and evidence reports overly loose credential handling, including a bundled API key. <br>
Mitigation: Remove and rotate any bundled key before use, then use only a scoped, revocable AtlasCloud token and avoid storing it in general agent memory. <br>
Risk: Image URLs, prompts, prediction metadata, and generated output URLs are sent to AtlasCloud and written to local result files. <br>
Mitigation: Submit only prompts and image URLs that are acceptable to share with AtlasCloud, and review or clear last_result.json and last_url.txt when they contain sensitive output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guilherme-funchal/nano-banana-atlas-ai) <br>
- [AtlasCloud API endpoint](https://api.atlascloud.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payload examples, shell commands, and generated image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes the latest prediction metadata to last_result.json and the generated image URL to last_url.txt.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
