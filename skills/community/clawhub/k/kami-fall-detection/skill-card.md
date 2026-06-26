## Description: <br>
Detect fall events from RTSP camera streams using KamiClaw cloud API. No local GPU needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and care-monitoring operators use this skill to configure RTSP cameras for continuous fall-event monitoring through KamiClaw cloud analysis, then route alerts to Feishu, Telegram, or Discord. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Motion-triggered camera clips are sent to KamiClaw cloud analysis and may be saved locally. <br>
Mitigation: Use only cameras and locations the user has consent to monitor, review the provider privacy policy, and disable local clip saving when retention is unnecessary. <br>
Risk: The skill handles sensitive API keys, RTSP URLs, and notification tokens. <br>
Mitigation: Store credentials outside source control, restrict access to config.json, and rotate KAMICLAW_API_KEY, webhook URLs, and bot tokens if exposed. <br>
Risk: Feishu webhook image fallback can upload images through the sm.ms hosting path. <br>
Mitigation: Avoid Feishu webhook image fallback unless that external upload path is acceptable, or use a Feishu app configuration that avoids anonymous image hosting. <br>
Risk: The setup script can remove an existing conda environment named kami-fall while recreating Python 3.10. <br>
Mitigation: Review setup.sh before execution and run it only in an environment where replacing that conda environment is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13681882136/kami-fall-detection) <br>
- [Publisher profile](https://clawhub.ai/user/13681882136) <br>
- [KamiClaw registration and API portal](https://kamiclaw-skill.kamihome.com) <br>
- [KamiClaw privacy policy](https://kamiclaw-skill.kamihome.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown setup guidance with shell commands, plus JSON Lines runtime alarm and analysis records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffmpeg, KAMICLAW_API_KEY, RTSP camera access, and optional notification credentials; runtime may save MP4 alarm clips and send Feishu, Telegram, or Discord alerts.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 1.0.9) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
