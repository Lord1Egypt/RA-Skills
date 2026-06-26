## Description: <br>
本地 Ollama 文生图工具，使用 x/z-image-turbo 模型根据中文提示词生成 1024x1024 图片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiafeimao-gjf](https://clawhub.ai/user/jiafeimao-gjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate local images from Chinese text prompts through an Ollama service and save the resulting PNG files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a local Ollama service for image generation. <br>
Mitigation: Install and run it only where local Ollama access is intended, and confirm the service is running at the expected localhost endpoint before use. <br>
Risk: Broad image-request phrases may activate the skill during ordinary agent conversations. <br>
Mitigation: Review whether the invocation phrases match the intended agent behavior before deployment. <br>
Risk: Generated image files are written to a local output directory. <br>
Mitigation: Review the configured output directory and local file retention expectations before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiafeimao-gjf/ollama-t2i) <br>
- [Local Ollama service endpoint](http://localhost:11434/api/generate) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text] <br>
**Output Format:** [PNG image files plus console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Images are saved under images/ or the requested output directory; each generation request uses the local Ollama service and may take about 90 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
