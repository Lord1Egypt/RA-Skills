## Description: <br>
Call Hidream txt2img async API with exposed auth and request parameters for generating images from text prompts, building runnable Python command examples, enforcing allowed resolution values, and troubleshooting Hidream task polling/results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhihui-chen-xx](https://clawhub.ai/user/zhihui-chen-xx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to submit Hidream text-to-image jobs, poll for completion, and return generated image URLs in a structured result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and bearer tokens are sent to Hidream when the script calls the txt2img API. <br>
Mitigation: Use HIDREAM_AUTHORIZATION instead of inline tokens, avoid confidential prompts unless Hidream's data handling is acceptable, and review the API use before deployment. <br>
Risk: The script polls an external image-generation service and may wait until timeout. <br>
Mitigation: Set appropriate polling interval and timeout values for the environment and handle nonzero exit codes in automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhihui-chen-xx/hd-txt2img) <br>
- [Hidream txt2img async API endpoint](https://www.hidreamai.com/api-pub/gw/v3/image/txt2img/async) <br>
- [Publisher profile](https://clawhub.ai/user/zhihui-chen-xx) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with runnable shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Hidream bearer token; prompt, resolution, image count, version, request ID, polling interval, and timeout are configurable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
