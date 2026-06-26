## Description: <br>
Cross-session context manager for AI agents with checkpoint and snapshot workflows, Build-Verify-Fix closure, entropy management, restore support, progress tracking, and agent configuration linting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanzhou3](https://clawhub.ai/user/lanzhou3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage local agent workspace continuity across sessions, including checkpoints, restores, verification reports, progress state, cleanup, and configuration linting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup agent can alter global agent memory and run repeatedly in daemon mode. <br>
Mitigation: Review the MEMORY.md path, back up MEMORY.md and .harness, and run in dry-run mode before enabling --run or --daemon. <br>
Risk: The memory archival helper can route MEMORY.md content through memory-palace and truncate the original file after archival. <br>
Mitigation: Disable or explicitly trust the memory-palace archival helper before allowing memory compression to execute. <br>
Risk: Custom verification command rules and forced restore or delete commands can perform privileged local workspace operations. <br>
Mitigation: Review custom verify rules before execution and treat restore, delete, and cleanup commands as privileged operations. <br>


## Reference(s): <br>
- [Architecture and design reference](references/architecture.md) <br>
- [Requirements and acceptance criteria](references/requirement.md) <br>
- [Technical knowledge package](references/knowledge-package.md) <br>
- [Maintenance guide](references/maintenance.md) <br>
- [ClawHub skill page](https://clawhub.ai/lanzhou3/openclaw-harness) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace files and reports when the documented harness commands are run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
