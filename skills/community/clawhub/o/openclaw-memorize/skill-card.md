## Description: <br>
Simple memory management for OpenClaw that saves, retrieves, searches, lists, and deletes key-value memories across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to persist decisions, preferences, metrics, ideas, links, and other small key-value notes for future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved memories persist in a local plaintext memories.json file and may be printed by the CLI. <br>
Mitigation: Do not save secrets, tokens, passwords, regulated data, or private notes unless local retention and CLI display are intentional. <br>
Risk: Publisher and source transparency are limited because server-resolved provenance is unavailable. <br>
Mitigation: Review future updates before installing and periodically delete old memories that are no longer needed. <br>


## Reference(s): <br>
- [Openclaw Memorize ClawHub listing](https://clawhub.ai/yang1002378395-cmyk/openclaw-memorize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text CLI output with JSON-backed local memory records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists key-value memories in a local plaintext memories.json file under the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
