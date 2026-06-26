## Description: <br>
Imou/Lechange device operation for PTZ control, snapshot capture, and image download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imou-openplatform](https://clawhub.ai/user/imou-openplatform) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to control Imou/Lechange cloud cameras, capture snapshots, optionally save images, and move PTZ-capable devices through the Imou Open API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Imou/Lechange cameras and move PTZ devices. <br>
Mitigation: Install it only when camera operation is intended, use least-privileged Imou credentials, and review PTZ requests before execution. <br>
Risk: Snapshots may capture sensitive locations and can be saved to local paths. <br>
Mitigation: Review snapshot requests for sensitive spaces and choose save paths deliberately. <br>
Risk: Requests are sent to the configured Imou Open API base URL. <br>
Mitigation: Set IMOU_BASE_URL explicitly for the correct region or data center. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imou-openplatform/imou-device-operate) <br>
- [Publisher Profile](https://clawhub.ai/user/imou-openplatform) <br>
- [Imou Open API Reference - Device Operate](references/imou-operate-api.md) <br>
- [Imou Developer Portal](https://open.imou.com) <br>
- [Imou International Developer Portal](https://open.imoulife.com) <br>
- [Imou Development Specification](https://open.imoulife.com/book/http/develop.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line text output with optional downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snapshot prints a downloadable URL and can save an image to a chosen path; PTZ prints a success or error message.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
