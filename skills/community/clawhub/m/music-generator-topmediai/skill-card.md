## Description: <br>
Generate AI music, background music, or lyrics through the TopMediai API, with polling for preview and full-audio generation results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Topmediai](https://clawhub.ai/user/Topmediai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate lyrics, songs, instrumental background music, task status updates, and MP4 conversions through TopMediai using a configured API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Creative prompts, lyrics, task IDs, and song IDs are sent to TopMediai under the user's API key. <br>
Mitigation: Use the skill only for data that may be shared with TopMediai, and review TopMediai account, privacy, and usage terms before sending sensitive content. <br>
Risk: The skill requires a private TOPMEDIAI_API_KEY and may affect paid quota or billing. <br>
Mitigation: Keep the .env file private, avoid committing API keys, and monitor TopMediai quota and billing while running generation tasks. <br>
Risk: Changing TOPMEDIAI_BASE_URL can redirect prompts and credentials to another endpoint. <br>
Mitigation: Leave TOPMEDIAI_BASE_URL set to https://api.topmediai.com unless the replacement endpoint is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Topmediai/music-generator-topmediai) <br>
- [TopMediai API base URL](https://api.topmediai.com) <br>
- [TopMediai API key page](https://www.topmediai.com/api/basic-information/interface-key/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API Calls, shell commands, guidance] <br>
**Output Format:** [Text responses containing JSON status payloads and generated media URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns lyrics, task IDs, preview-ready and full-ready events, failure or timeout status, and MP4 generation results when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
