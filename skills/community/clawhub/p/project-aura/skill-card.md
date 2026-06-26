## Description: <br>
Project Aura adds seven emotional personality modules and adaptive local phrase weighting to AI companions for more personalized emotional interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryanchen3777](https://clawhub.ai/user/bryanchen3777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Project Aura to add configurable emotional phrase selection, feedback-based weighting, and companion-style response variation to AI companion workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for romantic or emotionally intense AI companion phrasing. <br>
Mitigation: Review or replace the bundled phrase JSON before use so the companion tone matches the deployment context. <br>
Risk: Phrase counts and ratings persist locally in JSON. <br>
Mitigation: Treat the local phrase store as user-specific data and clear or rotate it when persistence is not desired. <br>
Risk: The optional yua-memory integration may introduce longer-term retention beyond this skill. <br>
Mitigation: Evaluate the separate memory project before enabling any long-term memory or indefinite retention behavior. <br>


## Reference(s): <br>
- [Project Aura on ClawHub](https://clawhub.ai/bryanchen3777/project-aura) <br>
- [README](artifact/README.md) <br>
- [CHANGELOG](artifact/CHANGELOG.md) <br>
- [yua-memory Integration Notes](artifact/yua_memory_README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python strings, JSON-backed configuration, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Phrase counts and ratings are persisted locally in JSON when the selector is used.] <br>

## Skill Version(s): <br>
1.8.0 (source: server release metadata and changelog, released 2026-03-29) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
