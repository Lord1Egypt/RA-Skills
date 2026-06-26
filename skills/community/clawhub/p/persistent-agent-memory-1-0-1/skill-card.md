## Description: <br>
Add persistent memory to any agent so it can remember prior work, maintain context across sessions, and continue long-running workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gyzx](https://clawhub.ai/user/gyzx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to store, retrieve, and delete persistent memories by meaning so agents can preserve context across sessions and long-running workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memories are stored with a third-party service and can persist across sessions. <br>
Mitigation: Use a dedicated Coral API key and avoid storing secrets, credentials, regulated personal data, or confidential business data. <br>
Risk: The package documents coral_* helper scripts that are missing from the artifact. <br>
Mitigation: Verify where the helper scripts come from before installing or executing the skill. <br>
Risk: Persisted memories may be recalled later when they are stale, irrelevant, or no longer appropriate to use. <br>
Mitigation: Review retrieved memories before relying on them and periodically delete memories that should no longer persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gyzx/persistent-agent-memory-1-0-1) <br>
- [Coral Bricks](https://coralbricks.ai) <br>
- [Coral Bricks Privacy Policy](https://www.coralbricks.ai/privacy) <br>
- [Persistent Memory for AI Agents](https://www.coralbricks.ai/blog/persistent-memory-openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CORAL_API_KEY plus curl and python3; memories use the default collection and may take up to 1 second to become retrievable after storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
