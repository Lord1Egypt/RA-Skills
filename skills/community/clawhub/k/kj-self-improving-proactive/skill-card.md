## Description: <br>
A unified OpenClaw skill that helps an agent learn from corrections, maintain active task state, recover context, and keep work moving within explicit boundaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tfops22](https://clawhub.ai/user/tfops22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to give an OpenClaw agent a local operating model for durable memory, session state, context recovery, and bounded proactive follow-through. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores durable local notes about preferences, corrections, task state, and follow-ups. <br>
Mitigation: Review the created ~/self-improving/ and ~/proactivity/ files periodically and avoid storing credentials, tokens, or secrets in them. <br>
Risk: Workspace integration files such as AGENTS.md, SOUL.md, HEARTBEAT.md, or TOOLS.md can embed the skill's behavior into a project. <br>
Mitigation: Approve edits to those files only when the behavior should become part of the workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tfops22/kj-self-improving-proactive) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/tfops22) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with local state and configuration file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent behavior guidance and local memory/state file conventions; it does not require external binaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
