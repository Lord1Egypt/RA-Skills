## Description: <br>
Recognizes image content, extracts OCR text, identifies objects and scenes, and analyzes screenshots by sending images to a configured vision model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangning823-arch](https://clawhub.ai/user/wangning823-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to run OCR, object recognition, scene analysis, and screenshot analysis on static images from an agent workflow, especially on Android and Termux systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Images may be uploaded to a remote vision-model provider, and the artifact includes an embedded fallback API key. <br>
Mitigation: Configure a trusted API key explicitly, remove or distrust the fallback key, and process only images approved for that provider. <br>
Risk: Screenshots, documents, QR codes, account pages, or other images can contain private or credential-like data. <br>
Mitigation: Avoid private or credential-containing images unless the user accepts the upload path and the remote provider's data handling terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangning823-arch/image-recognition) <br>
- [Aliyun Model Studio documentation](https://help.aliyun.com/zh/model-studio/) <br>
- [Aliyun Model Studio pricing](https://help.aliyun.com/zh/model-studio/pricing) <br>
- [OpenRouter chat completions endpoint](https://openrouter.ai/api/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Analysis] <br>
**Output Format:** [Plain text returned from a Python CLI or function call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit error strings for missing files, API failures, network timeouts, or provider errors.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
