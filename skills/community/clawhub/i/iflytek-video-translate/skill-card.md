## Description: <br>
Helps agents create, list, and inspect iFlytek video translation tasks for AI dubbing and multilingual video localization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, localization teams, and content teams use this skill to submit videos to iFlytek for translation, check task status, and retrieve task details for dubbed or localized video workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs and related task metadata are sent to iFlytek under the configured account. <br>
Mitigation: Use only video URLs and account credentials approved for iFlytek processing, and avoid submitting sensitive media unless that external processing is intended. <br>
Risk: The confirm_transcript action can skip manual transcript review and continue downstream processing. <br>
Mitigation: Require explicit human approval before running confirm_transcript, especially for workflows where transcript quality or review gates matter. <br>


## Reference(s): <br>
- [iFlytek Video Translation Documentation](https://www.xfyun.cn/doc/Develop/Video_Translation) <br>
- [iFlytek Console](https://console.xfyun.cn) <br>
- [ClawHub Skill Page](https://clawhub.ai/iflytek.skills/iflytek-video-translate) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, XFYUN_API_KEY, and XFYUN_API_SECRET; API responses may include task IDs, statuses, subtitle URLs, and output video URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
