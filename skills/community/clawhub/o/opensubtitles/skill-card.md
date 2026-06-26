## Description: <br>
Read-only OpenSubtitles skill to search and download subtitles via API, then extract timestamped scene context so agents can answer questions about a show without spoilers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dennisooki](https://clawhub.ai/user/dennisooki) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and developers use this skill to find subtitles, request subtitle download links, and extract a timestamp-bounded subtitle window for context-aware answers about media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can contact OpenSubtitles with API credentials, passwords, or tokens for search, login, and download-link requests. <br>
Mitigation: Treat OPENSUBTITLES_API_KEY, OPENSUBTITLES_PASSWORD, and OPENSUBTITLES_TOKEN as secrets, and approve login or download actions explicitly. <br>
Risk: Requesting a download link may affect OpenSubtitles account quota. <br>
Mitigation: Check the local subtitle cache before requesting a download link and include the remaining quota from the API response when a download is requested. <br>
Risk: Subtitle context can reveal more scene information than the user intended. <br>
Mitigation: Use the default timestamp-bounded window and adjust --window-mins only when the user asks for more or less context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dennisooki/opensubtitles) <br>
- [OpenSubtitles API reference](references/opensubtitles-api.md) <br>
- [OpenSubtitles API key setup](https://www.opensubtitles.com/consumers) <br>
- [OpenSubtitles API endpoint](https://api.opensubtitles.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENSUBTITLES_API_KEY, OPENSUBTITLES_USER_AGENT, curl, jq, and awk; optional login credentials or token are used for download-link requests.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
