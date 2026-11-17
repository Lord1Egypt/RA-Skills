## Description:

A skill by Kami SmartHome. Capture frames from your camera, describe them with AI, and search your visual history using natural language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13681882136](https://clawhub.ai/user/13681882136)

### License/Terms of Use:

MIT-0

## Use Case:

External users and smart-home operators use this skill to capture or import camera images, index visual history, and retrieve matching images with natural-language queries. Developers can configure camera streams, retention, and search thresholds for RTSP-based monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Camera frames, imported images, and search text may be sent to Kamivision for cloud inference.

Mitigation: Use the skill only when that data sharing is acceptable, verify KAMIVISION_API_URL is the intended HTTPS Kami endpoint, and avoid processing sensitive images unnecessarily.

Risk: Camera stream URLs and API keys can expose private credentials if stored or logged insecurely.

Mitigation: Restrict permissions on image_config.json and log files, avoid embedding camera passwords in stream URLs when possible, and rotate credentials if exposure is suspected.

Risk: The setup script can install Python tooling and may request sudo package installation for build dependencies.

Mitigation: Review setup.sh before running it and approve sudo installation only when system-wide changes are acceptable.

Risk: Captured images, imported images, SQLite metadata, and FAISS indexes are stored locally.

Mitigation: Set retention to the shortest practical period, protect the data directory, and delete local frame and index data when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/13681882136/skills/kami-image-search)
- [Publisher profile](https://clawhub.ai/user/13681882136)
- [Kamivision Flow](https://kamiclaw-skill.kamihome.com/)
- [Kamivision privacy policy](https://kamiclaw-skill.kamihome.com/privacy)
- [Kamivision API endpoint](https://kamiclaw-skill-api.kamihome.com/v1/detect)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce JSON search results, camera status output, configuration updates, and local image/index files.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
