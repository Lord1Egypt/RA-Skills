## Description: <br>
即梦 4.0 图片生成器，通过文本描述生成高质量图片，支持多图编辑与智能比例。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FelixHsp](https://clawhub.ai/user/FelixHsp) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content creators use this skill to generate, edit, and compose images with VolcEngine Jimeng AI 4.0 from text prompts and optional reference image URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, reference image URLs, and uploaded or referenced images are sent to VolcEngine for processing. <br>
Mitigation: Avoid confidential images, secrets, internal-only URLs, and proprietary prompts unless the user's policy permits that disclosure. <br>
Risk: VolcEngine credentials are required to run the skill. <br>
Mitigation: Use least-privilege or short-lived credentials when possible, keep .env files out of git, and rotate keys if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/FelixHsp/jimeng-generator) <br>
- [Jimeng 4.0 API reference](docs/jimengv4.md) <br>
- [VolcEngine authorization reference](docs/authorization.md) <br>
- [VolcEngine visual API endpoint](https://visual.volcengineapi.com) <br>
- [VolcEngine signing documentation](https://www.volcengine.com/docs/6369/67269) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, API Calls, Configuration] <br>
**Output Format:** [JSON status with local PNG file paths and optional image URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved to a local output directory unless --no-save is used.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
