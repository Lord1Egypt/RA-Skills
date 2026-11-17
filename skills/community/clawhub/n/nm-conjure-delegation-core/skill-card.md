## Description:

Delegates execution to external CLIs (Gemini, Qwen, MiniMax, GLM, Muse, Codex, OpenCode, Glimmer). Use for execution tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess whether execution work is suitable for delegation to external AI providers, prepare handoffs, and validate or integrate the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated prompts or context may be sent to external AI providers.

Mitigation: Keep secrets, credentials, and data that should remain local out of delegated requests.

Risk: The skill may configure an MCP server in Claude in addition to delegating to external AI CLIs.

Mitigation: Review the MCP configuration and provider access before enabling or using delegation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conjure-delegation-core)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with tables, checklists, and inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides task assessment, delegation handoff, provider setup, and result validation guidance.]

## Skill Version(s):

1.10.3 (source: artifact frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
