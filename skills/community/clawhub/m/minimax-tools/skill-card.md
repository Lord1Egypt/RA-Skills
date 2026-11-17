## Description:

Provides MiniMax-backed image understanding and web search for agents when users ask to analyze images or retrieve current online information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oujakivi](https://clawhub.ai/user/oujakivi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route image-analysis and online-search requests through MiniMax tools after configuring a MiniMax API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install and runtime path relies on unverified shell installers and unpinned external code.

Mitigation: Use verified and pinned installation sources for uv and minimax-coding-plan-mcp, and review the skill before installing.

Risk: The MiniMax tools receive credentials and inherit the runtime environment.

Mitigation: Use a scoped MiniMax API key and avoid running the skill in an environment that contains unrelated secrets.

Risk: Image references, prompts, and search queries may be sent to the configured MiniMax service.

Mitigation: Avoid submitting sensitive inputs unless the configured MiniMax account and service terms are appropriate for that data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oujakivi/skills/minimax-tools)
- [Publisher profile](https://clawhub.ai/user/oujakivi)
- [MiniMax API host](https://api.minimaxi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and JSON-formatted tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured MiniMax API key; image references, prompts, and search queries may be sent to the configured MiniMax service.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
