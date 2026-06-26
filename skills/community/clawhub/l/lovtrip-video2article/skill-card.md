## Description: <br>
Converts a user-provided YouTube video into a structured article with a title, author, summary, and Markdown body using Google Gemini. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lizhijun](https://clawhub.ai/user/lizhijun) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, travel writers, and agents use this skill to turn public YouTube videos, especially travel videos, into structured article drafts. It supports MCP, CLI, and standalone script workflows for generating localized Markdown article content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected YouTube URL, prompt, and generation request are sent to Google Gemini and may consume Gemini API quota. <br>
Mitigation: Use the skill only with inputs appropriate for Google Gemini processing, and run it with a Gemini API key and quota you intend to use for this purpose. <br>
Risk: The MCP setup uses the lovtrip npm package and may install the latest package version. <br>
Mitigation: Prefer the included reviewed script path, or pin and review the lovtrip npm package version before giving it a Gemini API key. <br>
Risk: Gemini safety filters may block videos with sensitive content, and generated article drafts may require editorial review. <br>
Mitigation: Use publicly accessible videos, check for blocked or incomplete generations, and review the generated article before publication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lizhijun/lovtrip-video2article) <br>
- [LovTrip](https://lovtrip.app) <br>
- [LovTrip guides](https://lovtrip.app/guides) <br>
- [LovTrip developer documentation](https://lovtrip.app/developer) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [JSON object containing title, author, summary, and a Markdown article body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YouTube video URL, a Gemini API key, and optional language or prompt inputs.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
