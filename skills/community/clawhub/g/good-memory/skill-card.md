## Description: <br>
Good Memory restores OpenClaw session context after resets by detecting prior session files and reinserting recent conversation history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acilgit](https://clawhub.ai/user/acilgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to recover recent chat context when sessions are reset, rotated, or restarted. It is intended for environments where automatic restoration of prior conversation history is desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically reads and reinserts prior session history, which may expose sensitive chat content in the active context. <br>
Mitigation: Use only in trusted, single-user OpenClaw environments or add explicit opt-in and session-scope controls before deployment. <br>
Risk: The installer persists startup behavior by modifying AGENTS.md and maintaining a session tracker. <br>
Mitigation: Review installer changes before use, back up AGENTS.md, restrict tracker access, and provide a clear disable and deletion path. <br>
Risk: Automatic restoration can cross session boundaries if the deployment is shared or mis-scoped. <br>
Mitigation: Avoid shared agents and sensitive workflows unless session ownership is validated and restoration is limited to the intended user or chat. <br>


## Reference(s): <br>
- [Good Memory ClawHub page](https://clawhub.ai/acilgit/good-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit recovered conversation excerpts from recent OpenClaw session history.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata, artifact frontmatter, and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
