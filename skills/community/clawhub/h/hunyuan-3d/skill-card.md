## Description: <br>
腾讯混元生3D API (OpenAI兼容接口) - 基于混元大模型的3D模型生成 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wszhhx](https://clawhub.ai/user/wszhhx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to configure Tencent Hunyuan 3D access and run text-to-3D or image-to-3D generation jobs through a Python command-line helper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided prompts or image URLs to Tencent Hunyuan 3D. <br>
Mitigation: Use it only with content appropriate for Tencent processing, and avoid submitting secrets, confidential prompts, private image URLs, or regulated content. <br>
Risk: The helper downloads generated model files from service-provided URLs to the local filesystem. <br>
Mitigation: Treat returned model files as downloaded internet content and scan or review them before opening them in other tools. <br>
Risk: The skill requires a Tencent Hunyuan 3D API key in HUNYUAN_3D_API_KEY. <br>
Mitigation: Store the API key as an environment variable or secret, avoid committing it, and rotate it if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wszhhx/hunyuan-3d) <br>
- [Tencent Hunyuan 3D OpenAI-compatible API documentation](https://cloud.tencent.com/document/product/1804/126189) <br>
- [Tencent Hunyuan 3D submit task API documentation](https://cloud.tencent.com/document/product/1804/123447) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, API Calls, Files, JSON] <br>
**Output Format:** [Markdown guidance with command examples; generated model files and info.json when the helper script is executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python and HUNYUAN_3D_API_KEY; saves generated 3D assets under an output directory organized by date and job ID.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
