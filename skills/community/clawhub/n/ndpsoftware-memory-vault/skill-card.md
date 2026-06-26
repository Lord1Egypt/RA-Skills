## Description: <br>
Enables autonomous agents to store, retrieve, and recall long-term, durable memory fragments and state across independent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndp](https://clawhub.ai/user/ndp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect autonomous agents to a persistent cloud memory service for durable notes, logs, preferences, project context, task state, vector fragments, and cross-session recall. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent memory, logs, preferences, project context, and task state are sent to and retained by a remote service. <br>
Mitigation: Install only when the publisher is trusted, use a service-specific bearer token, and confirm review and deletion controls before relying on stored memory. <br>
Risk: Sensitive secrets or regulated personal data could be persisted in long-term memory. <br>
Mitigation: Avoid storing secrets, credentials, regulated personal data, or confidential material in memory fragments or logs. <br>
Risk: Retrieved memory may be stale, incomplete, or inappropriate for the current task. <br>
Mitigation: Review recalled notes and state before using them to guide agent actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ndp/ndpsoftware-memory-vault) <br>
- [Publisher profile](https://clawhub.ai/user/ndp) <br>
- [Memory Vault endpoint](https://memory-vault.ndpsoftware.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown guidance with endpoint and bearer-token configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote memory storage and recall may retain notes, logs, preferences, project context, and task state outside the active agent session.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
