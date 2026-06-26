## Description: <br>
Optimizes OpenClaw workspace foundation files such as AGENTS, MEMORY, SOUL, TOOLS, IDENTITY, and USER to reduce context noise, with a required optimization proposal and user confirmation before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to audit persistent workspace context files, move stale material into deeper memory storage, delete obsolete bootstrap content, and keep active context concise after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reorganize persistent workspace context files and may delete obsolete BOOTSTRAP.md content after approval. <br>
Mitigation: Review the proposed file list and ask for a diff or dry run before approving changes, especially for MEMORY.md, AGENTS.md, SOUL.md, IDENTITY.md, USER.md, and BOOTSTRAP.md. <br>
Risk: Cleanup decisions could remove or archive context that is still useful for future agent behavior. <br>
Mitigation: Require the skill's optimization plan, expected size changes, and target archive paths before execution; append archived content instead of overwriting existing memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/openclaw-workspace-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown proposal and summary, with workspace file edits after confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No credentials or external binaries are required; proposed file changes must be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
