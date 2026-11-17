## Description:

Token消耗优化器 helps agents audit token usage, estimate API costs, and produce prioritized optimization plans using prompt slimming, history management, tool-output compression, caching, model routing, and CCR-style reversible compression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to diagnose high token/API costs and generate quantified cost-reduction plans for prompts, tool outputs, RAG, conversation history, model routing, caching, and budget forecasting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cache sharing across agents may expose private code, logs, or workspace context beyond the intended scope.

Mitigation: Enable cache sharing only with explicit opt-in, per-workspace isolation, secret redaction, and short retention.

Risk: Failed-session analysis may process sensitive logs or conversation history.

Mitigation: Apply secret redaction and retention limits before analysis, and restrict access to approved workspaces.

Risk: Automatic configuration changes may degrade agent behavior or token efficiency if applied without review.

Mitigation: Require human-approved configuration diffs and keep a rollback path for any applied changes.

## Reference(s):

- [Token消耗优化器 detailed reference](references/details.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with tables, checklists, code snippets, command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output; guidance expects quantified savings estimates and quality checks.]

## Skill Version(s):

1.5.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
