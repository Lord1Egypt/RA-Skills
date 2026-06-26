## Description: <br>
Add persistent memory to any agent so it can remember prior work, maintain context across sessions, and continue long-running workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[divyvasal](https://clawhub.ai/user/divyvasal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to store, retrieve, and delete persistent memory by semantic meaning so an agent can carry facts, preferences, and workflow context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memory text, metadata, and search queries are sent to Coral Bricks and may persist across sessions. <br>
Mitigation: Use a dedicated revocable API key and avoid storing secrets or sensitive regulated data. <br>
Risk: The forget command deletes by semantic query and does not preview matching memories. <br>
Mitigation: Phrase deletion queries carefully and verify important deletions after running them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/divyvasal/persistent-agent-memory) <br>
- [Coral Bricks homepage](https://coralbricks.ai) <br>
- [Persistent Agent Memory for AI Agents](https://www.coralbricks.ai/blog/persistent-memory-openclaw) <br>
- [Coral Bricks privacy policy](https://www.coralbricks.ai/privacy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration guidance] <br>
**Output Format:** [Shell command invocations and JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CORAL_API_KEY plus curl and python3; memory operations call the Coral Bricks Memory API.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
