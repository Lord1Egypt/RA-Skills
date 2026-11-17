## Description:

HAI Agent Framework provides a hook event system, automatic conversation-memory extraction, and four predefined agents for code review, test generation, security scanning, and documentation writing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragons777-cpu](https://clawhub.ai/user/dragons777-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to configure hook-driven agent workflows, automate memory loading and conversation analysis, and invoke specialist agents for code review, test generation, security scanning, and documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent conversation-memory collection may retain sensitive conversation or project data.

Mitigation: Use an isolated environment and avoid sensitive chats or projects unless memory collection, retention, and deletion controls are clear.

Risk: Unpinned external installation and installed hook scripts may introduce unexpected behavior.

Mitigation: Verify the publisher and version, review installed .hai scripts and hook configurations before enabling them, and enable only the hooks required for the intended workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dragons777-cpu/skills/hai-agent-framework)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include hook configuration examples, agent invocation patterns, script commands, and memory-management guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
