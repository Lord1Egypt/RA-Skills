## Description: <br>
Three-layer Working, Short-Term, and Long-Term memory management for AI agents, with hooks, cron-based cleanup and distillation, and CLI commands for preferences, entities, events, and episodic notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JochenYang](https://clawhub.ai/user/JochenYang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local cross-session memory to OpenClaw agents, including user preferences, entities, events, working memory, short-term notes, and agent episodic memory. It is suited to workflows where automatic local persistence and periodic memory distillation are intended. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic hooks and cron jobs persist session-derived data in local memory files, which can retain sensitive preferences, events, or learnings. <br>
Mitigation: Enable the skill only when local cross-session memory is intended, avoid storing secrets, and periodically inspect or delete the configured memory directory. <br>
Risk: Cleanup has an avoidable code-execution path because it can run MEMORY_DIR/index.py. <br>
Mitigation: Review or patch cleanup before enabling cron, and keep the memory directory restricted to trusted local files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JochenYang/open-memory-system) <br>
- [README.md](README.md) <br>
- [Cron configuration guide](crons/memory-crons.txt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands and local memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and reads local filesystem memory under the configured MEMORY_DIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
