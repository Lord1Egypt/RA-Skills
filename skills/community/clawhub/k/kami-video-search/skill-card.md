## Description:

RTSP/RTMP multi-camera stream recording with AI-powered video search for starting and stopping recording, checking status, searching clips by natural language, listing recent events, and viewing logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[13681882136](https://clawhub.ai/user/13681882136)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect RTSP/RTMP cameras, record footage locally, generate searchable event indexes, and retrieve relevant clips through natural-language queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private camera footage and can upload frames or videos to Kamivision for AI analysis.

Mitigation: Use it only when users are comfortable with that data flow, review Kamivision privacy terms, and keep upload mode and endpoint settings explicit.

Risk: Camera credentials, API keys, and RTSP URLs may appear in local configuration or logs.

Mitigation: Store credentials outside shared or backed-up folders, redact RTSP URLs before sharing files or logs, and protect the local workspace.

Risk: The setup script can install tooling through a curl-to-bash path if Python 3.10 is missing.

Mitigation: Prefer preinstalling Python 3.10 through a trusted package manager and review setup commands before execution.

Risk: Background recording, automatic deletion, and stop commands affect security-sensitive footage and retention.

Mitigation: Require explicit user confirmation before starting or stopping recording and review retention settings before deployment.

Risk: Changing KAMI_API_URL could route camera data away from the intended service.

Mitigation: Restrict KAMI_API_URL to the intended HTTPS Kamivision endpoint unless a trusted administrator approves a different endpoint.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/13681882136/skills/kami-video-search)
- [Kamivision skill homepage](https://kamiclaw-skill.kamihome.com)
- [Kamivision privacy policy](https://kamiclaw-skill.kamihome.com/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May start or stop background recording processes and update local camera configuration after user confirmation.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
