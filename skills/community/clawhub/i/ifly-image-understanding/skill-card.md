## Description: <br>
ifly-image-understanding analyzes images and answers questions using iFlytek Spark Vision over its WebSocket API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to send a local JPG or PNG image with a natural-language question to iFlytek Spark Vision and receive an image-understanding answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and questions are sent to iFlytek for processing. <br>
Mitigation: Use only images approved for that provider and avoid highly sensitive content unless the deployment has explicit approval. <br>
Risk: Credentials and billing quota are required for the iFlytek API. <br>
Mitigation: Use a dedicated iFlytek app and API key where possible, store credentials in environment variables, and monitor usage or billing. <br>
Risk: The package includes a local Claude settings file that is not needed for normal use. <br>
Mitigation: Ignore or remove the stray .claude local settings file before deployment if it is not part of the target environment. <br>


## Reference(s): <br>
- [iFlytek Console](https://console.xfyun.cn) <br>
- [iFlytek Image Understanding Service](https://console.xfyun.cn/services/image) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text answer by default, with optional raw WebSocket JSON frames] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET; accepts JPG, JPEG, or PNG images up to 4MB; max response tokens are configurable up to 8192.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
