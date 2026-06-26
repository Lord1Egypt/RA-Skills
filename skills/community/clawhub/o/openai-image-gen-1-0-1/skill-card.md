## Description: <br>
Batch-generate images via OpenAI Images API. Random prompt sampler + `index.html` gallery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shi8103312](https://clawhub.ai/user/shi8103312) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate batches of OpenAI image outputs from either random structured prompts or user-provided prompts, then review the saved images, prompt mapping, and gallery locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts are sent to the configured OpenAI API endpoint. <br>
Mitigation: Use a dedicated API key, verify OPENAI_BASE_URL or OPENAI_API_BASE before running, and avoid sending sensitive prompt content. <br>
Risk: Generated prompts and gallery files are stored locally. <br>
Mitigation: Review generated files before sharing them and avoid untrusted HTML-like prompt text before opening the gallery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shi8103312/openai-image-gen-1-0-1) <br>
- [OpenAI Images API endpoint](https://api.openai.com/v1/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Images, Files, JSON, HTML] <br>
**Output Format:** [PNG image files, prompts.json, and a local index.html thumbnail gallery] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports count, model, prompt, size, quality, timeout, sleep, output directory, API key, and dry-run options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
