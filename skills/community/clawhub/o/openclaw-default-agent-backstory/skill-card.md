## Description: <br>
Build, bootstrap, and maintain a stable OpenClaw default agent identity by interviewing the user, updating IDENTITY.md, and seeding core context files (AGENTS.md, SOUL.md, TOOLS.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msaum](https://clawhub.ai/user/msaum) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to bootstrap a new workspace identity or refresh an existing agent backstory through a five-question interview and structured context-file updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or refresh workspace identity, operating, and memory files, which may replace customized context if accepted without review. <br>
Mitigation: Review the planned file list and ask for a diff or backup before allowing updates to AGENTS.md, SOUL.md, IDENTITY.md, MEMORY.md, or memory/. <br>
Risk: The generated backstory or identity can encode assumptions when user input is incomplete. <br>
Mitigation: Answer the five interview questions where possible and review IDENTITY.md for marked assumptions before relying on the generated identity. <br>
Risk: Memory and user-context files can contain sensitive personal preferences, routines, or workspace details. <br>
Mitigation: Avoid adding secrets or regulated data to memory files, and periodically prune MEMORY.md and daily notes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/msaum/openclaw-default-agent-backstory) <br>
- [OpenClaw Context Documentation](https://docs.openclaw.ai/concepts/context) <br>
- [Bootstrap Core Files](artifact/references/bootstrap-core-files.md) <br>
- [Ranked Question Bank](artifact/references/question-bank.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown context files, interview questions, concise summaries, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or refreshes OpenClaw identity, operating, memory, heartbeat, and bootstrap files in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
