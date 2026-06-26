## Description: <br>
Translate videos into a specified target language using the Keevx API, with support for audio-only translation, subtitle generation, dynamic duration adjustment, supported-language lookup, and translation task status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baidu-xiling](https://clawhub.ai/user/baidu-xiling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to translate or dub videos through the Keevx API, including uploading local files, submitting translation tasks, and checking task status. It is also useful for discovering supported target languages before submitting a translation request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted videos, video URLs, task metadata, and callback URLs are sent to Keevx for processing. <br>
Mitigation: Use the skill only with media approved for third-party processing, avoid confidential or regulated footage unless approved, and prefer least-privilege API keys and time-limited private URLs. <br>
Risk: Local file inputs are uploaded before translation and generated output links are temporary. <br>
Mitigation: Confirm the selected file before upload and download translated videos or subtitle files promptly after successful completion. <br>


## Reference(s): <br>
- [Keevx Skill Page](https://clawhub.ai/baidu-xiling/keevx-video-translate) <br>
- [Keevx Home](https://www.keevx.com/main/home) <br>
- [Official API Docs - Supported Languages](https://docs.keevx.com/api-reference/endpoint/ListSupportedLanguages) <br>
- [Official API Docs - Submit Translation](https://docs.keevx.com/api-reference/endpoint/SubmitVideoTranslate) <br>
- [Official API Docs - Check Status](https://docs.keevx.com/api-reference/endpoint/GetTranslationStatus) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KEEVX_API_KEY and jq for the full workflow script; generated video and subtitle URLs are retained for 7 days.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
