## Description: <br>
OpenClaw AI Doctor helps diagnose and troubleshoot OpenClaw agent failures, including startup errors, stalled tasks, tool or plugin failures, memory issues, session leakage, and skill loading problems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[speakmen](https://clawhub.ai/user/speakmen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators troubleshooting OpenClaw agents use this skill as a diagnostic checklist for collecting symptoms, checking system state, mapping likely root causes, and applying manual repair commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Manual repair commands may restart services, kill sessions, change permissions, delete lock or index files, or interrupt active work. <br>
Mitigation: Review paths and command scope first, run only the section matching the observed issue, and preserve needed work before running disruptive commands. <br>
Risk: Troubleshooting output may expose API keys, tokens, logs, configuration, policy, or memory contents. <br>
Mitigation: Redact sensitive credentials and private workspace contents before sharing command output or diagnostic artifacts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/speakmen/openclaw-ai-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with diagnostic tables and bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include manual repair commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
