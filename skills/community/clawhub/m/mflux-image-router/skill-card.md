## Description: <br>
Routes local mflux image generation requests across an Apple Silicon Mac fleet and provides setup, API, and monitoring guidance for using ollama-herd with mflux models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twinsgeeks](https://clawhub.ai/user/twinsgeeks) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure local mflux image generation through an ollama-herd fleet router, generate images via HTTP APIs, and monitor image generation activity across trusted Mac devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local router can process image prompts and also exposes non-image endpoints for text, audio, embeddings, and chat workloads. <br>
Mitigation: Keep the router limited to trusted devices and use non-image endpoints only when prompt, audio, or text processing by that fleet is intended. <br>
Risk: The setup depends on local ollama-herd and mflux packages and models that run on user-managed machines. <br>
Mitigation: Review the packages before installation and confirm model downloads or changes before running commands that alter the local fleet environment. <br>
Risk: Generated images and fleet-manager configuration files can be user data or operational state. <br>
Mitigation: Do not delete or modify generated images or files under ~/.fleet-manager/ unless the user explicitly confirms the action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/twinsgeeks/mflux-image-router) <br>
- [ollama-herd Package](https://pypi.org/project/ollama-herd/) <br>
- [ollama-herd Repository](https://github.com/geeks-accelerator/ollama-herd) <br>
- [Agent Setup Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/agent-setup-guide.md) <br>
- [Image Generation Guide](https://github.com/geeks-accelerator/ollama-herd/blob/main/docs/guides/image-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with bash, Python, and JavaScript examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to produce local HTTP requests, example code, and operational guidance for mflux image generation; generated image files are produced by the local router, not by the skill text itself.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
