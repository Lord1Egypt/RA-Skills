## Description: <br>
Local-first OpenClaw inference plugin that routes prompts to local Ollama models first, strips private context before optional cloud fallback, and records audit and metrics data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shivaclaw](https://clawhub.ai/user/shivaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Nirvana to run OpenClaw prompts through local models by default, with configurable cloud fallback for tasks that need external model capacity. It is intended for workflows where privacy boundaries, audit logging, and local inference cost control matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and stripped context can be sent to cloud providers when fallback is enabled. <br>
Mitigation: Disable cloud fallback for sensitive work and keep context-boundary enforcement enabled. <br>
Risk: The plugin reads sensitive agent files and persists audit, metrics, and response data locally. <br>
Mitigation: Review identityFilesNeverExport, audit and cache retention settings, and local file access before deployment. <br>
Risk: Migration guidance includes deleting Nirvana audit and metrics logs. <br>
Mitigation: Back up logs and confirm retention requirements before running log-deletion commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shivaclaw/nirvana-plugin) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [INSTALL.md](artifact/INSTALL.md) <br>
- [MIGRATION.md](artifact/MIGRATION.md) <br>
- [config.schema.json](artifact/config.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Shell commands, Audit logs, Metrics] <br>
**Output Format:** [Model responses with JSON configuration, local log files, and command-line setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes requests between local and cloud providers, caches responses, and persists audit and metrics data locally.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata, created 2026-04-19T20:21:41Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
