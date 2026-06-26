## Description: <br>
Optimization suite for OpenClaw agents to prevent token leaks and context bloat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klautimus](https://clawhub.ai/user/klautimus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to reduce context bloat by isolating background tasks, configuring memory search, and applying reset-and-summarize workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional transcript indexing can expose sensitive past conversations through local search. <br>
Mitigation: Index selectively, remove secrets before indexing, and include only transcripts the user is comfortable making searchable later. <br>
Risk: Applying configuration examples without review can change OpenClaw cron or memory behavior. <br>
Mitigation: Review openclaw.json edits before applying them and keep cron jobs intentional. <br>
Risk: Restart-based reset workflows can discard active session context if important details are not saved first. <br>
Mitigation: Save important session context to long-term memory or logs before restarting OpenClaw. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/klautimus/openclaw-token-memory-optimizer) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenClaw configuration checks and memory-management workflow recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and package.json declare 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
