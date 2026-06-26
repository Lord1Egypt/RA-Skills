## Description: <br>
Searches and reads X (Twitter) profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces, and publishes posts after the user completes OAuth in the browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaimengphp](https://clawhub.ai/user/chaimengphp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to search and read Twitter/X data, monitor social activity, and publish text or media posts through AIsa after browser OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The posting client can expose the full AISA API key in normal command output. <br>
Mitigation: Avoid running status, authorize, or post commands in shared logs, CI, screenshots, or transcripts until the client redacts the key. <br>
Risk: The skill can publish text, images, and videos to Twitter/X after OAuth authorization. <br>
Mitigation: Confirm the exact content, media files, account authorization state, and quoted or replied-to tweet target before treating a publish result as successful. <br>
Risk: Local media files selected by the user are uploaded through the AIsa relay as part of posting workflows. <br>
Mitigation: Use only intended workspace file paths and do not include sensitive local files as media attachments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chaimengphp/openclaw-aisa-twitter-search) <br>
- [Publisher profile](https://clawhub.ai/user/chaimengphp) <br>
- [OpenClaw homepage](https://openclaw.ai) <br>
- [AIsa API Reference](https://docs.aisa.one/reference/) <br>
- [OpenClaw Twitter OAuth](references/post_twitter.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; posting uses browser OAuth and may upload local image or video files.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
