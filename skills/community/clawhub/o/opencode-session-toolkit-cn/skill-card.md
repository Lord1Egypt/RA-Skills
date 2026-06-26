## Description: <br>
Reads the local OpenCode SQLite database to support cross-directory session queries, message inspection, and Markdown export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufei-png](https://clawhub.ai/user/wufei-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenCode users use this skill to find local sessions across projects, inspect message records, and export selected conversations to Markdown for private review or archival. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported Markdown may contain private OpenCode conversation history and project data. <br>
Mitigation: Keep generated Markdown private and review or redact it before sharing. <br>
Risk: A full export can capture more session history than intended. <br>
Mitigation: Prefer narrow filters such as session, project, title, directory, or date range, and use --all only when a full export is intended. <br>
Risk: The skill depends on local opencode and uv commands found on PATH. <br>
Mitigation: Ensure the local opencode and uv commands are trusted before running the export workflow. <br>


## Reference(s): <br>
- [OpenCode SQLite Schema Reference](references/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/wufei-png/opencode-session-toolkit-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with SQL and shell command examples; the export script writes Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated exports may contain private conversation and project data.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
