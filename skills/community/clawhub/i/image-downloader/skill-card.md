## Description: <br>
Helps an agent collect image candidates by keyword from Bing and supported sources, download them into local keyword folders, avoid repeated downloads, and report the saved directory and run summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[16miku](https://clawhub.ai/user/16miku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill when they need a reusable workflow for keyword-based public image downloading, including local file output, duplicate avoidance, source statistics, and a concise completion report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates downloaded image files and metadata/history under downloads/<keyword>/ on the local filesystem. <br>
Mitigation: Run it only in an approved workspace and review or clean generated download directories according to local data-retention expectations. <br>
Risk: The artifact documents a cron workflow that can send downloaded images to Feishu through host OpenClaw/Feishu credentials. <br>
Mitigation: Do not enable scheduled sending unless the recipient, channel, credentials, and operational need have been explicitly verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/16miku/image-downloader) <br>
- [GitHub repository](https://github.com/16Miku/image-downloader-skill) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces downloaded image files and local metadata/history under downloads/<keyword>/ when executed.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
