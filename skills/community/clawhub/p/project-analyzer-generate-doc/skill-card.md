## Description: <br>
Generates hierarchical L3/L2/L1 documentation for Java Maven multi-module projects, including MyBatis SQL mapping, Maven dependency analysis, task monitoring, retry, checkpoint resume, and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze Java/Maven/MyBatis repositories and generate .ai-doc documentation that helps agents and humans understand file-level, module-level, and project-level architecture. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a selected Java/Maven repository and writes generated documentation, task state, and logs into .ai-doc or a configured output path. <br>
Mitigation: Run it only on repositories selected for documentation, review generated output before relying on it, and use a separate output path for sensitive projects when appropriate. <br>
Risk: Document migration, merge, and deletion-adjacent cleanup behavior can modify existing documentation files if approved. <br>
Mitigation: Review the proposed migration or cleanup plan and approve only intended file moves, merges, or removals. <br>
Risk: The package metadata includes a PowerShell npm script with an execution-policy bypass. <br>
Mitigation: Do not run the script unless the local artifact is trusted and the execution-policy behavior is understood. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [Context Compression](references/context-compression.md) <br>
- [Checkpoint Resume](references/checkpoint-resume.md) <br>
- [Incremental Update](references/incremental-update.md) <br>
- [Retry Mechanism](references/retry-mechanism.md) <br>
- [Subagent Task Template](references/subagent-task-template.md) <br>
- [Task Monitoring](references/task-monitoring.md) <br>
- [Security Fixes](SECURITY_FIXES.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/endcy/project-analyzer-generate-doc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JSON task summaries and state, PowerShell command snippets, and configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated documentation, task state, and logs under .ai-doc or a user-selected output path.] <br>

## Skill Version(s): <br>
2.1.4 (source: ClawHub release evidence and CHANGELOG-v2.1.4.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
