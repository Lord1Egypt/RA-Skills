## Description: <br>
Search YouTube videos, channels, and trends through the AISA YouTube SERP client. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill for YouTube content research, channel discovery, competitor tracking, trend monitoring, and SERP analysis through the bundled AISA client. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube search queries are sent to the third-party AISA relay at api.aisa.one. <br>
Mitigation: Use the skill only for searches that are acceptable to send to that relay; avoid private or sensitive queries unless the relay is approved for the use case. <br>
Risk: The skill requires an AISA_API_KEY that may incur usage charges. <br>
Mitigation: Use a scoped key where available, monitor usage, and rotate or revoke the key if it is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/openclaw-aisa-youtube-aisa) <br>
- [Publisher profile](https://clawhub.ai/user/bibaofeng) <br>
- [AISA YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; bundled CLI emits JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; optional country, language, filter token, result count, competitor name, and topic parameters are supported by the bundled CLI.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
