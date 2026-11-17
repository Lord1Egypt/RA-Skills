## Description: <br>
Neural Context Engine Free helps agents store and recall local associative memory using graph-style spreading activation for decisions, errors, preferences, and todos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add persistent local memory for cross-session recall of decisions, errors, preferences, facts, and todos. It is intended for agents that can run the referenced memory tooling and use recalled context during later work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to persist conversation-derived facts, decisions, errors, preferences, and todos in local memory. <br>
Mitigation: Review the local database location and avoid storing secrets, regulated personal data, or other sensitive content. <br>
Risk: Automatically reused memories may be stale, incomplete, or applied with limited user control. <br>
Mitigation: Review recalled context before relying on it for important decisions, and prune or correct outdated memories. <br>
Risk: Optional external embedding providers may cause relevant content to leave the local environment if enabled. <br>
Mitigation: Keep external embedding providers disabled unless their data handling is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/neural-context-engine-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce memory records, todo identifiers, command results, and configuration snippets depending on the requested workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
