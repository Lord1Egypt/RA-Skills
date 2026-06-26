## Description: <br>
Transforms AI agents from task-followers into proactive partners that anticipate needs, preserve working memory, recover from context loss, and improve over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ranthemaster](https://clawhub.ai/user/ranthemaster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users apply this skill to configure an assistant with proactive behavior, persistent workspace memory, compaction recovery, self-improvement routines, and security guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent workspace memory can retain broad conversation, profile, or project details without enough consent, retention, or redaction controls. <br>
Mitigation: Set explicit boundaries for writable memory files, forbid storing passwords, tokens, cookies, and private identifiers, and periodically review or delete generated memory files. <br>
Risk: Proactive behavior, spawned agents, network activity, or external actions can exceed the user's intended scope. <br>
Mitigation: Require user confirmation before external actions, spawned agents, shared-channel posts, destructive file operations, or changes that affect security posture. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ranthemaster/proactive-agent-2) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and workspace file layout examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instructs the agent to create and maintain persistent workspace memory files.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 3.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
