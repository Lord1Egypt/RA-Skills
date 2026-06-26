## Description: <br>
Generate images, videos, upscale or enhance images, and train LoRA styles through the Krea.ai API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albertsalgueda](https://clawhub.ai/user/albertsalgueda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creative operators, and agents use this skill to run Krea.ai media workflows from shell commands, including image and video generation, image enhancement, LoRA style training, job lookup, and multi-step creative pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, private URLs, local media, and training images may be sent to Krea.ai for generation, enhancement, or style training. <br>
Mitigation: Use this skill only when Krea.ai data handling is approved for the content, and avoid submitting secrets, regulated data, private URLs, or confidential media. <br>
Risk: API tokens can be exposed if passed directly on the command line. <br>
Mitigation: Prefer the KREA_API_TOKEN environment variable over the --api-key argument. <br>
Risk: Generation and training jobs can spend paid compute units or require a higher Krea.ai plan. <br>
Mitigation: Check available models, costs, and parameters before running jobs, and review downloaded outputs before opening or sharing them. <br>


## Reference(s): <br>
- [Krea API OpenAPI Specification](https://api.krea.ai/openapi.json) <br>
- [ClawHub release page](https://clawhub.ai/albertsalgueda/krea) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [Markdown with inline shell commands and saved file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save generated images, videos, and JSON manifests to the current working directory or a selected output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
