## Description: <br>
Builds session-scoped temporary memory palaces for extended conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and other agent users use this skill to structure temporary session context during extended conversations, multi-step projects, reviews, debugging, and research. It helps organize decisions, artifacts, progress, issues, and next steps so context can be recovered across interruptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on common words such as "session" or "context" and organize sensitive conversation details in the current session. <br>
Mitigation: Use it only when session-organization behavior is intended, and avoid invoking it for unrelated conversations that contain sensitive details. <br>
Risk: Generated session structures can preserve incorrect assumptions, decisions, or stale project state. <br>
Mitigation: Review the organized context before relying on it for follow-up work, handoff, export, or archival. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/nm-memory-palace-session-palace-builder) <br>
- [Memory Palace plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace) <br>
- [Session Palace Templates](modules/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with structured lists, template layouts, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces session-organization guidance only; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata; artifact frontmatter lists 1.9.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
