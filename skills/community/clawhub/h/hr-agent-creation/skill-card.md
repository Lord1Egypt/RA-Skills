## Description:

Creates and configures an HR-style OpenClaw agent that can help create other agents, bind them to Feishu group chats, and collect detailed setup requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingqiu2180](https://clawhub.ai/user/jingqiu2180)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to generate an HR agent workspace, configure OpenClaw registration, and bind the agent to a Feishu group after confirming required settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates a powerful Feishu-connected OpenClaw agent and modifies local OpenClaw configuration.

Mitigation: Install only in a controlled OpenClaw environment after confirming the Feishu group ID and service-account permissions.

Risk: Generated configuration may grant broader tool or file access than intended.

Mitigation: Apply least-privilege tool policy outside the generated markdown and review the workspace files before starting the agent.

Risk: Weak safeguards around local configuration and script behavior can make production use harder to audit or reverse.

Mitigation: Keep ~/.openclaw/openclaw.json at 600 or stricter, address the temporary-file and jq interpolation issues, and document unbind and removal steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jingqiu2180/skills/hr-agent-creation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw workspace files, Feishu binding configuration, and operational test commands when the bundled scripts are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
