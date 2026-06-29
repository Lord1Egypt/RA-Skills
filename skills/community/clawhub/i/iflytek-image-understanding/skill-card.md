## Description: <br>
Use when user asks to analyze an image, describe image contents, or answer questions about a picture. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to describe a user-selected image or answer targeted questions about its contents through iFlytek's Spark Vision image understanding service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts are sent to iFlytek's remote API for processing. <br>
Mitigation: Use only images and prompts that your privacy, data handling, and compliance requirements allow you to share with iFlytek. <br>
Risk: Images may contain IDs, receipts, medical documents, confidential screenshots, or other regulated information. <br>
Mitigation: Screen inputs before use and avoid regulated or confidential images unless the third-party upload is explicitly approved. <br>
Risk: The skill requires iFlytek API credentials in environment variables. <br>
Mitigation: Provide credentials through the runtime environment, avoid committing them to files, and rotate them if exposed. <br>


## Reference(s): <br>
- [iFlytek Image Understanding service](https://www.xfyun.cn/services/image_understanding) <br>
- [iFlytek image service documentation](https://console.xfyun.cn/services/image) <br>
- [iFlytek console](https://console.xfyun.cn) <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-image-understanding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain text image-analysis responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May output raw WebSocket JSON frames when requested; default responses are assembled text from the remote image understanding API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
