## Description: <br>
Scenario-focused Sparki skill for highlight extraction while using the official Sparki setup, API-key, and upload workflow guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fischerlam](https://clawhub.ai/user/fischerlam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to route local video files through Sparki for highlight reels, event recaps, sports clips, and other edits that keep the strongest moments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video files and edit prompts are uploaded to Sparki's remote service for processing. <br>
Mitigation: Use the skill only for videos and prompt text that may be shared with Sparki, and avoid uploading confidential or regulated footage unless approved. <br>
Risk: Running setup can store a long-lived Sparki API key in local OpenClaw configuration. <br>
Mitigation: Prefer supplying SPARKI_API_KEY as an environment variable, rotate keys when needed, and protect or remove local configuration files that contain credentials. <br>
Risk: Downloaded video outputs are written to a local configured output path by default. <br>
Mitigation: Review or override output paths before downloading, especially in shared workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fischerlam/highlight-reels) <br>
- [Sparki Homepage](https://sparki.io) <br>
- [Sparki Telegram Upload](https://t.me/Sparki_AI_bot/upload) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with Sparki CLI commands and JSON CLI responses; completed runs can download MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPARKI_API_KEY, uploads MP4 or MOV files to Sparki, and writes downloaded results under the configured Sparki output directory unless an output path is provided.] <br>

## Skill Version(s): <br>
1.0.12 (source: SKILL.md frontmatter, _meta.json, ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
