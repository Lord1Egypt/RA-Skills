## Description: <br>
调用海康云眸开放平台视频云录制能力，包括云录制项目、转码录制任务、文件管理、流量管理、资源上传和视频剪辑。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hik-cloud-open](https://clawhub.ai/user/hik-cloud-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to manage Hik-Cloud video recording projects, recording and frame extraction tasks, files, project flow limits, uploads, and video clips through the Hik-Cloud OpenAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Hik-Cloud credentials and OAuth tokens. <br>
Mitigation: Use least-privileged credentials, prefer environment variables over CLI tokens, and protect or clear the token cache on shared machines. <br>
Risk: The skill can alter or delete cloud recording resources, stop tasks, change flow limits, and initiate uploads or downloads. <br>
Mitigation: Require explicit human confirmation before destructive or high-impact operations. <br>
Risk: Custom base URLs can redirect credential-backed requests to nonstandard endpoints. <br>
Mitigation: Use the default Hik-Cloud endpoint unless the custom base URL is controlled and trusted. <br>


## Reference(s): <br>
- [认证说明](references/auth.md) <br>
- [视频云录制文档摘要](references/video-recording.md) <br>
- [海康云眸开放平台视频云录制 API](https://pic.hik-cloud.com/opencustom/apidoc/online/open/b6f980108b8242258716079c118d5702.html) <br>
- [ClawHub skill page](https://clawhub.ai/hik-cloud-open/hik-cloud-open-video-recording) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; helper output is text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Hik-Cloud credentials in HIK_OPEN_CLIENT_ID and HIK_OPEN_CLIENT_SECRET.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
