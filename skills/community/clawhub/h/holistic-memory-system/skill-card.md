## Description: <br>
6-layer autonomous memory system for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add a layered memory system for OpenClaw agents, including local logs, semantic search, crystallized notes, health checks, and maintenance automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create long-running host jobs through cron and startup automation. <br>
Mitigation: Review the proposed cron entries before use, avoid the cron `install` command and @reboot startup unless they are required, and remove scheduled jobs that are not needed. <br>
Risk: The skill persists user memory and may sync it with weak privacy controls. <br>
Mitigation: Define what data may be logged, retained, deleted, or excluded from memory, and keep Syncthing or SSH sharing disabled until all peers and folders are trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/kofna3369/holistic-memory-system) <br>
- [Holistic Memory System Report](HOLISTIC_MEMORY_SYSTEM_REPORT.md) <br>
- [README](README.md) <br>
- [FABRIQUER-MEMOIRE-AGENT](references/FABRIQUER-MEMOIRE-AGENT.md) <br>
- [Holistic Memory Blueprint](references/holistic-memory-blueprint.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with Python and shell command examples; runtime scripts write JSON, JSONL, Markdown, and log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local files under ~/.openclaw and can install recurring cron jobs when explicitly invoked.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
