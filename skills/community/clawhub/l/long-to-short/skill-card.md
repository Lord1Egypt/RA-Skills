## Description: <br>
Scenario-focused Sparki skill for turning long videos into short-form clips while using the latest official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn podcasts, interviews, talks, streams, and other long-form videos into short clips, reels, or shorts with stronger hooks and cleaner cutdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected videos and prompts are uploaded to Sparki for processing. <br>
Mitigation: Use the skill only for videos and prompts that may be shared with Sparki, and avoid submitting sensitive media unless approved for that service. <br>
Risk: The Sparki API key may be stored in local OpenClaw configuration. <br>
Mitigation: Prefer SPARKI_API_KEY from the environment or protect ~/.openclaw/config/sparki.json with appropriate local access controls. <br>
Risk: Changing the API base URL can send requests and uploads to a non-default endpoint. <br>
Mitigation: Use the default Sparki API base URL unless the alternative endpoint is explicitly trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fischerlam/long-to-short) <br>
- [Publisher Profile](https://clawhub.ai/user/fischerlam) <br>
- [Sparki](https://sparki.io) <br>
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands return JSON status and result data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SPARKI_API_KEY and user-selected local or Telegram Mini App video uploads; generated video results are downloaded or linked by the Sparki service.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata, SKILL.md frontmatter, _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
