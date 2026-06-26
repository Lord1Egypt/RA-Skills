## Description: <br>
Records RTSP/RTMP multi-camera streams and lets an agent start or stop recording, check status, search clips by natural language, list recent events, and view logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure RTSP/RTMP cameras, run local background recording, and query indexed clips with natural language through Kamivision AI processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles surveillance footage, search queries, and an API key while using remote AI uploads. <br>
Mitigation: Review the configuration before installation, use dedicated camera and API credentials, and avoid sensitive camera locations unless affected people consent. <br>
Risk: The bundled setup path may install Python and dependencies automatically. <br>
Mitigation: Prefer a manually managed Python 3.10 environment and inspect setup.sh before running it. <br>
Risk: Background recording and automatic retention cleanup can capture or remove footage unexpectedly. <br>
Mitigation: Confirm the camera list, storage path, and retention days before starting recording, and review logs or backups for critical footage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/13681882136/kami-video-search) <br>
- [Kamivision homepage](https://kamiclaw-skill.kamihome.com) <br>
- [Kamivision privacy policy](https://kamiclaw-skill.kamihome.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update stream_config.json, start or stop local background recording, read logs, and call the Kamivision API for video analysis and search.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
