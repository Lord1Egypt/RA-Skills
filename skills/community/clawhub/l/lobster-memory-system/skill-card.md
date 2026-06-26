## Description: <br>
Lobster Memory System provides a modular, versioned, automatically backed-up memory structure for AI assistants. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzhqqq123](https://clawhub.ai/user/wzhqqq123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to set up persistent local memory, daily backups, session-aware memory loading, and self-improvement notes for OpenClaw or Clawdbot-style assistants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory and scheduled backups can retain sensitive user, project, or credential-like data. <br>
Mitigation: Do not store API keys, private data, or secrets in memory files; review backup encryption, retention, access controls, and deletion behavior before enabling the workflow. <br>
Risk: The installation flow asks users to run PowerShell setup scripts with ExecutionPolicy Bypass. <br>
Mitigation: Obtain scripts from a trusted source, inspect them before execution, and avoid ExecutionPolicy Bypass unless the need and impact are understood. <br>
Risk: Automated backup and cleanup commands can change or remove local files if configured incorrectly. <br>
Mitigation: Review the target directories, backup retention settings, ACL changes, and removal commands before enabling scheduled tasks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wzhqqq123/lobster-memory-system) <br>
- [Project homepage](https://github.com/openclaw/lobster-memory-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and PowerShell or bash command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory-structure guidance, initialization steps, scheduled-backup commands, and maintenance workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md frontmatter, skill.yaml, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
