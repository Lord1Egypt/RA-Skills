## Description: <br>
Generates daily Kuaishou AI-content reports by scanning RedFox data, clustering viral videos, and summarizing trends, creators, growth signals, and investigation directions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, creators, MCNs, brands, and industry researchers use this skill to monitor Kuaishou AI content trends, find viral videos and creators, and generate structured daily intelligence reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and supports command-line or local-file key configuration. <br>
Mitigation: Prefer the REDFOX_API_KEY environment variable, avoid plaintext config or command history exposure, and rotate the key if it may have been written to local files. <br>
Risk: The skill can run a localhost preview server with API and image proxy endpoints. <br>
Mitigation: Run the preview server only when needed and keep it bound to localhost. <br>
Risk: The subscription option can create a scheduled task that persists after the initial run. <br>
Mitigation: Review the LaunchAgent or crontab entry before using --subscribe and remove it with --unsubscribe when no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/ks-ai-feed) <br>
- [Publisher profile](https://clawhub.ai/user/redfox-data) <br>
- [RedFox API keys](https://redfox.hk/settings/api-keys?souce=github) <br>
- [RedFox login](https://www.redfox.hk/login) <br>
- [Engine strategy](references/engine-strategy.md) <br>
- [Investigation modes](references/investigation-modes.md) <br>
- [Investigation templates](references/investigation-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, structured terminal tables, and generated HTML report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a RedFox API key. Can start a localhost preview server and can optionally create a scheduled daily report task.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
