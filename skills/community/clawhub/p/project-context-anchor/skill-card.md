## Description: <br>
Writes a project-local AI_CONTEXT.md snapshot that captures project structure, recent changes, active plans, and a compact bootstrap block for cross-session AI handoff. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiao3333](https://clawhub.ai/user/xiao3333) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assisted engineering teams use this skill to create a project-root context snapshot for session recovery, team handoff, and continuity across AI tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated AI_CONTEXT.md can persist recent project and chat context, including sensitive project details. <br>
Mitigation: Inspect AI_CONTEXT.md before committing or sharing it, run a secrets scan, and keep it out of version control for private or credential-heavy work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiao3333/project-context-anchor) <br>
- [Publisher profile](https://clawhub.ai/user/xiao3333) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown file with a compact AI_BOOTSTRAP_BLOCK] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes AI_CONTEXT.md in the project root and may include project structure, git history, diffs, decisions, plans, and session-derived context.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
