## Description: <br>
Run the agent like an executive operator with calm briefings, sharp prioritization, context recovery, and proactive follow-through. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Jarvis to give an agent a calm executive operating style for ambiguous, high-stakes, or interrupted work. It helps the agent produce concise briefings, prioritize next steps, recover context, and maintain visible approval boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local profile notes in ~/jarvis/ may accumulate sensitive personal or business context. <br>
Mitigation: Keep stored details minimal and review the Jarvis memory files periodically. <br>
Risk: Approved AGENTS.md, SOUL.md, or HEARTBEAT.md seed blocks can steer later agent behavior in the workspace. <br>
Mitigation: Read each seed block before approval, keep changes additive and visible, and remove the blocks if they no longer match the workspace. <br>
Risk: The executive persona could overstate awareness or capability if used without its boundaries. <br>
Mitigation: Follow the documented boundary rules: state what was observed, distinguish inference, and avoid claims of hidden monitoring or external control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/jarvis) <br>
- [Skill homepage](https://clawic.com/skills/jarvis) <br>
- [Setup guide](artifact/setup.md) <br>
- [Safety boundaries](artifact/boundaries.md) <br>
- [Operating modes](artifact/operating-modes.md) <br>
- [Workspace seed blocks](artifact/openclaw-seed.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional shell commands and local configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only behavior profile; optional state is stored locally under ~/jarvis/ and approved workspace seed files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
