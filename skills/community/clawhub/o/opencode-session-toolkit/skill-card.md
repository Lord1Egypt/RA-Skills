## Description: <br>
Read the local OpenCode SQLite database, run cross-directory session queries, and export sessions to Markdown files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wufei-png](https://clawhub.ai/user/wufei-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local OpenCode sessions, query session and message data, and export selected sessions into Markdown archives. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read sensitive local OpenCode session history, including prompts, file paths, private code, and possible secrets. <br>
Mitigation: Use narrow filters, review the matched scope before export, write exports to a private directory, and inspect exported Markdown before sharing. <br>
Risk: A broad export can unintentionally capture all local OpenCode sessions. <br>
Mitigation: Prefer project, session, title, directory, and time filters; use --all only when a full export is intended. <br>
Risk: Overwriting export files can replace previously saved session archives. <br>
Mitigation: Avoid --overwrite unless replacement is intentional; otherwise let the script create collision-safe filenames. <br>


## Reference(s): <br>
- [OpenCode SQLite Schema Reference](references/schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/wufei-png/opencode-session-toolkit) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands, SQL snippets, JSON inspection output, and Markdown export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The export script writes one Markdown file per selected OpenCode session and requires explicit filters or --all for full exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
