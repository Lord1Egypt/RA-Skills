## Description: <br>
Project context tracker using `.malp/` directories for discovering, opening, creating, refreshing, and maintaining local project context notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inertia186](https://clawhub.ai/user/inertia186) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage local project reconnaissance notes in `.malp/` directories, including active, attic, and unindexed context states. It helps preserve working knowledge without silently loading unrelated or archived context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create `.malp/` folders in user-named paths and maintain an index under `~/.malp-home/`. <br>
Mitigation: Use it only for paths the user explicitly asks to track, and review generated `.malp/` files before sharing or committing them. <br>
Risk: Project context notes may accidentally include secrets or sensitive working knowledge. <br>
Mitigation: Do not put secrets in `.malp/` notes, and choose whether `.malp/` files should be ignored by git or intentionally tracked. <br>
Risk: Archived or unindexed context could be mistaken for active project state. <br>
Mitigation: Keep active, attic, and unindexed states explicit, and avoid loading archived or cross-referenced malps unless the user asks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/inertia186/malp) <br>
- [Operational behavior and file conventions](artifact/references/tasks.md) <br>
- [Active, attic, and unindexed states](artifact/references/indexing.md) <br>
- [Attic and archive semantics](artifact/references/attic.md) <br>
- [Version control strategies for `.malp/`](artifact/references/repo-strategies.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown or plain text with optional shell commands and local file guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or refresh `.malp/` directories and maintain an index under `~/.malp-home/` only when the user asks it to track a path.] <br>

## Skill Version(s): <br>
0.1.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
