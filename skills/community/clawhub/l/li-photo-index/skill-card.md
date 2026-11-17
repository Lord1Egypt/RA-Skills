## Description:

Photo Index With LLM scans photo directories, uses local or configured remote vision-language models to describe images, stores a searchable local index, and returns natural-language photo search results for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let CLI-capable agents scan, index, and search personal or work photo collections using natural-language queries. It is most useful when the user has a verified local vision-language model endpoint and wants structured JSON or readable text results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private photos may be sent to a configured remote vision-language model endpoint or an unverified local endpoint.

Mitigation: Use only a verified loopback endpoint such as localhost or 127.0.0.1 by default, and enable remote endpoints only after explicit review and consent.

Risk: Auto-loaded .env configuration may silently change endpoint, API key, or privacy settings.

Mitigation: Inspect any .env file before running scans, keep API keys out of shared repositories, and verify that remote upload settings match the intended privacy posture.

Risk: The local SQLite index stores photo paths and model-generated descriptions without encryption.

Mitigation: Restrict database file permissions, avoid indexing sensitive photos until controls are reviewed, and remove or encrypt the index when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-photo-index)
- [SKILL.md](artifact/SKILL.md)
- [skill.yaml](artifact/skill.yaml)
- [Privacy Guide](artifact/PRIVACY_GUIDE.md)
- [Privacy and Data Security Report](artifact/PRIVACY.md)
- [Cross-Platform Compatibility](artifact/CROSS_PLATFORM.md)

## Skill Output:

**Output Type(s):** [text, json, files]

**Output Format:** [CLI stdout as readable text or structured JSON; scan commands also update a local SQLite photo index.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.10+, requests, and a verified local LM Studio-compatible endpoint by default; configured remote endpoints may receive image content.]

## Skill Version(s):

1.1.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
