## Description: <br>
This skill helps agents use the Lumi API to upload, repurpose, localize, analyze, and publish social videos across TikTok, YouTube, and Instagram with curl-based API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffery1995](https://clawhub.ai/user/jeffery1995) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and operators use this skill to collect publishing parameters, call Lumi APIs, translate or dub Chinese social videos, and publish or review localized output for international channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish videos through connected Lumi social accounts after the user selects target platforms. <br>
Mitigation: Use a dedicated Lumi API key and verify the selected account, platform, caption or title, and visibility before posting. <br>
Risk: Repurposed or localized content may be published before human review when auto-publish targets are provided. <br>
Mitigation: Use the localization-only workflow when the processed video should be reviewed before publication. <br>


## Reference(s): <br>
- [Lumi homepage](https://lumipath.cn) <br>
- [Lumi voice catalog](https://lumipath.cn/voices) <br>
- [connections.openapi.json](references/connections.openapi.json) <br>
- [videos.openapi.json](references/videos.openapi.json) <br>
- [social-posts.openapi.json](references/social-posts.openapi.json) <br>
- [localization.openapi.json](references/localization.openapi.json) <br>
- [tts.openapi.json](references/tts.openapi.json) <br>
- [repurpose.openapi.json](references/repurpose.openapi.json) <br>
- [insights.openapi.json](references/insights.openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with curl commands and API request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LUMI_API_KEY and user-confirmed publishing parameters before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
