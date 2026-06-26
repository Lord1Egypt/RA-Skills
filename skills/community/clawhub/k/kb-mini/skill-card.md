## Description: <br>
Kb Mini stores, searches, recalls, and optionally captures personal or shared knowledge for OpenClaw agents using local SQLite-backed command-line and hook workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThomasLiu](https://clawhub.ai/user/ThomasLiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to persist useful notes, configuration details, decisions, and reusable context, then retrieve that knowledge manually or inject related entries before future agent turns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic after-turn capture can persist full conversation text, including sensitive or secret-like content, in private or shared databases. <br>
Mitigation: Use private KB mode for sensitive work, avoid automatic capture unless conversation storage is acceptable, and do not store credentials or secrets. <br>
Risk: Shared knowledge-base mode can expose retained conversation context to multiple agents without explicit access-control, redaction, retention, or deletion guarantees in the evidence. <br>
Mitigation: Use shared mode only when the sharing boundary is intentional and retention, deletion, and access practices are reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ThomasLiu/kb-mini) <br>
- [API interface specification](references/api-spec.md) <br>
- [Database schema](references/db-schema.md) <br>
- [Retrieval pipeline](references/retrieval-pipeline.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create and query persistent SQLite knowledge-base records through manual commands and OpenClaw before/after hooks.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
