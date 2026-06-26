## Description: <br>
Mapick -- Skill recommendation and privacy protection for OpenClaw; it scans local skills, suggests missing skills, and helps keep other skills from seeing sensitive data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunlleyevan](https://clawhub.ai/user/sunlleyevan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use Mapick to discover relevant skills, audit skill safety, manage privacy consent, clean unused skills, and generate usage summaries without manually inspecting every installed skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mapick can read and modify installed skill directories and can guide install, removal, upgrade, backup, and notification setup flows. <br>
Mitigation: Inspect each command plan before confirming, keep backups enabled, and only approve changes to skills you intend to manage. <br>
Risk: Recommendation, profile, status, and related metadata may be sent to api.mapick.ai after consent or through paths that security evidence describes as less clearly gated. <br>
Mitigation: Use local-only mode when backend communication is not acceptable, review `/mapick privacy log`, and avoid entering secrets or sensitive client details into profile or workflow prompts. <br>
Risk: Offline security results are not equivalent to a backend scan and may give misleading confidence. <br>
Mitigation: Treat local-only security output as preliminary, prefer backend-scanned results when possible, and review the skill manually before installation. <br>


## Reference(s): <br>
- [Mapick ClawHub release](https://clawhub.ai/sunlleyevan/mapick) <br>
- [Publisher profile](https://clawhub.ai/user/sunlleyevan) <br>
- [Declared Mapick API host](https://api.mapick.ai) <br>
- [README](README.md) <br>
- [Multi-step Flows](reference/flows.md) <br>
- [Rendering Rules](reference/rendering.md) <br>
- [Outbound HTTP manifest](scripts/lib/http.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and concise user-facing text with inline shell commands and JSON-backed command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Node.js 22.14 or later is required; command output is clamped and network operations use consent-gated calls to api.mapick.ai.] <br>

## Skill Version(s): <br>
1.0.28 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
