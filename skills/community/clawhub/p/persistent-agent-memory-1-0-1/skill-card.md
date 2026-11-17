## Description:

Add persistent memory to any agent so it can remember prior work, maintain context across sessions, and continue long-running workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyzx](https://clawhub.ai/user/gyzx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to let agents store, retrieve, and delete persistent memories by semantic meaning across sessions and long-running workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected memory text and metadata are sent to Coral Bricks and retained for cross-session recall.

Mitigation: Do not store credentials, secrets, regulated personal data, or confidential business material unless authorized and comfortable with the provider's retention behavior.

Risk: Deletion is semantic rather than exact, so a delete query can affect memories beyond the intended wording or miss related content.

Mitigation: Use narrow deletion queries and verify the result with a retrieval query after deletion.

Risk: The skill depends on a remote API key and service endpoint.

Mitigation: Provide CORAL_API_KEY through approved secret handling and limit access to environments authorized to use the Coral Bricks service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gyzx/skills/persistent-agent-memory-1-0-1)
- [Coral Bricks](https://coralbricks.ai)
- [Persistent Memory for AI Agents](https://www.coralbricks.ai/blog/persistent-memory-openclaw)
- [Coral Bricks Privacy Policy](https://www.coralbricks.ai/privacy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; memory operations return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CORAL_API_KEY, curl, and python3; CORAL_API_URL can override the default Coral Bricks API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
