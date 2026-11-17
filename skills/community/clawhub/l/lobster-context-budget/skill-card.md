## Description:

Audits Claude Code context window consumption across agents, skills, MCP servers, and rules. Identifies bloat, redundant components, and produces prioritized token-savings recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit Claude Code context usage across agents, skills, rules, MCP servers, and CLAUDE.md files. It helps identify context bloat, redundant components, and prioritized token-saving changes before expanding a local agent setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated report may expose details from local agent, skill, rule, MCP, or CLAUDE.md configuration files.

Mitigation: Review the report before sharing it outside the local environment and redact sensitive setup details.

Risk: Token counts and savings estimates are approximate and may not match the exact model tokenizer or runtime context assembly.

Mitigation: Treat recommendations as planning guidance and verify high-impact changes against actual session behavior before removing components.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/skills/lobster-context-budget)
- [Publisher profile](https://clawhub.ai/user/wangxiaofei860208-source)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with context estimates, issue flags, prioritized recommendations, and optional verbose per-file breakdowns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include estimated token counts, component counts, ranked savings opportunities, and local configuration details surfaced from scanned setup files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
