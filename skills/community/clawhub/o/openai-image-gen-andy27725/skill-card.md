## Description: <br>
Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users use this skill to generate image batches from provided or randomly sampled prompts, then review saved image files with a local HTML gallery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OpenAI API key and can incur image-generation costs. <br>
Mitigation: Run it only with an intended `OPENAI_API_KEY`, choose the count and model deliberately, and monitor API usage. <br>
Risk: Prompts are sent to the OpenAI Images API. <br>
Mitigation: Review custom and randomly generated prompts before execution, and avoid including confidential or sensitive content. <br>
Risk: Generated files are written locally, with the default directory based on the user's environment. <br>
Mitigation: Use `--out-dir` to confine outputs to a known folder before sharing or archiving results. <br>


## Reference(s): <br>
- [OpenAI Images API reference](https://platform.openai.com/docs/api-reference/images) <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/openai-image-gen-andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [Files, API Calls, Shell commands, Configuration instructions] <br>
**Output Format:** [Image files, JSON prompt mapping, and HTML gallery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces PNG, JPEG, or WebP images, prompts.json, and index.html in a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
