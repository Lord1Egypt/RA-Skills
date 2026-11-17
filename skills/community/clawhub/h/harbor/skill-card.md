## Description:

Persistent cross-session memory, credential isolation, and schema learning for OpenClaw agents, with local storage under ~/.harbor/ and optional cloud sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx13719](https://clawhub.ai/user/zx13719)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Harbor to give OpenClaw agents persistent memory, credential-brokered API access, and reusable schema learning across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Harbor asks for persistent memory access and credential-broker authority.

Mitigation: Install only after review, prefer pinned audited versions, use dedicated low-scope API tokens, and review what is remembered before enabling sync.

Risk: Agent or tool code that uses `harbor auth get` can receive raw credentials.

Mitigation: Prefer brokered requests through `harbor fetch --auth` when possible and avoid `harbor auth get` in agent/tool code unless raw-key handling is required and reviewed.

Risk: The recommended plugin may create a cloud account on first load, even though data sync requires later user action.

Mitigation: Tell users about the account-creation behavior before installation and use `harbor cloud disable` when cloud features are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zx13719/skills/harbor)
- [Publisher profile](https://clawhub.ai/user/zx13719)
- [Harbor homepage](https://harbor.oseaitic.com)
- [Harbor repository](https://github.com/oSEAItic/harbor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead agents to use Harbor CLI or MCP tools for memory, credential access, schema learning, and OpenClaw configuration.]

## Skill Version(s):

0.4.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
