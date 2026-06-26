## Description: <br>
Batch-generate images via the OpenAI Images API with a random prompt sampler and local HTML gallery output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate batches of images from provided or sampled prompts, then review the saved image files, prompt mapping, and local gallery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OpenAI API key and image generation may incur usage costs. <br>
Mitigation: Keep OPENAI_API_KEY in the environment, do not print or embed it in outputs, and review count, model, size, and quality settings before running large batches. <br>
Risk: Generated images, prompts.json, and the local gallery may contain sensitive prompt or image content. <br>
Mitigation: Write outputs only to a trusted local output directory and do not upload or transmit generated files to external services unless separately reviewed. <br>
Risk: Opening generated galleries from untrusted prompt text can expose a reviewer to unexpected local HTML content. <br>
Mitigation: Open only galleries produced in the current project output directory and treat prompt text from untrusted sources as untrusted content. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/snazar-faberlens/openai-image-gen-hardened) <br>
- [OpenAI Images API reference](https://platform.openai.com/docs/api-reference/images) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/openai-image-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; the script produces image files, prompts.json, and an index.html gallery.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and OPENAI_API_KEY; supports model, prompt, count, size, quality, background, output format, style, and output directory options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
