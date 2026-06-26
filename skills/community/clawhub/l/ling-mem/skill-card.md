## Description: <br>
Shared Memory gives coding agents a durable, local-first memory interface through the `ling-mem` CLI so facts, preferences, decisions, and cross-session context can be recalled across supported hosts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linggen](https://clawhub.ai/user/linggen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and coding-agent users use this skill to add, search, update, delete, and periodically consolidate local memory records across Claude Code, Codex, OpenClaw, Linggen, and other CLI-capable hosts. It is intended for users who want persistent agent context while retaining local storage control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run a remote installer and install the ling-mem CLI. <br>
Mitigation: Review the installer path before use and prefer manual CLI installation when stronger supply-chain control is required. <br>
Risk: The skill can read local agent session logs and store personal facts durably. <br>
Mitigation: Avoid storing secrets or sensitive personal data, and periodically review or delete memory rows in the local browser or CLI. <br>
Risk: Retrieved memories may be injected into future prompts sent to the configured LLM. <br>
Mitigation: Disable or limit auto-recall where available and review stored facts for sensitivity and staleness. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linggen/ling-mem) <br>
- [Linggen homepage](https://linggen.dev) <br>
- [Skill README](artifact/README.md) <br>
- [Shared memory design](artifact/doc/shared-memory-design.md) <br>
- [Routing rules](artifact/references/routing-rules.md) <br>
- [Dream flow](artifact/references/dream-flow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide agents to operate the local ling-mem CLI, omit embedding vectors from displayed JSON, and may include visible memory-recall notes when retrieved facts shape a response. Security guidance: review before installing because the skill can install code, read local agent session logs, durably store personal facts, and inject retrieved memories into future LLM prompts; prefer manual CLI installation, limit auto-recall where available, avoid storing secrets or sensitive personal data, and periodically review or delete local memory rows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
