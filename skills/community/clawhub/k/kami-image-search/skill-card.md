## Description: <br>
Capture frames from camera streams or imported images, describe them with the Kamivision cloud API, and search visual history using natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[13681882136](https://clawhub.ai/user/13681882136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and smart-home users use this skill to configure RTSP cameras or import local images, index them with descriptions and embeddings, and retrieve matching images with natural-language queries. It is suited for authorized camera-history review, such as deliveries, home activity, and monitoring playback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/13681882136/kami-image-search) <br>
- [Kamivision Flow](https://kamiclaw-skill.kamihome.com/) <br>
- [KamiClaw privacy policy](https://kamiclaw-skill.kamihome.com/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, json] <br>
**Output Format:** [Markdown instructions with shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.10, RTSP camera access, internet access to the KamiClaw API, and a Kamivision API key. Review authorization for each camera, protect RTSP URLs and API keys, restrict permissions on image_config.json and logs, configure retention, and start background capture only when continuous monitoring is intended.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
