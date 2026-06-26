## Description: <br>
Runs a controlled OpenClaw browser workflow in Jimeng to generate a video, wait for completion, and download the resulting MP4 locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohao-ui](https://clawhub.ai/user/haohao-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need an agent to create a Jimeng video, find the latest generated video, and return a verified local MP4 path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a Jimeng browser session and may act under the user's logged-in account. <br>
Mitigation: Install and run it only with an OpenClaw browser profile intended for Jimeng video generation. <br>
Risk: Long-running generation can stall or exceed the expected wait window. <br>
Mitigation: Use the documented state machine, 20-30 second polling interval, 12-minute timeout, and explicit FAILED(timeout) result. <br>
Risk: A download may appear complete without producing a usable file. <br>
Mitigation: Verify that the local file exists, has size greater than zero, and is an MP4 or the page-declared video format. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/haohao-ui/jimeng-video-openclaw-stable) <br>
- [Jimeng Video Workspace](https://jimeng.jianying.com/ai-tool/home/?workspace=0&type=video) <br>
- [Jimeng Asset Library](https://jimeng.jianying.com/ai-tool/asset) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with OpenClaw command guidance and a local file path report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the local absolute path, file existence, file size, video format, or an explicit FAILED(...) state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
