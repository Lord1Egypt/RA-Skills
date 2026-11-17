## Description:

Daily incremental update of HIPPOCAMPUS.md with domain-filtered 14-day rolling context for all agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[comicsansbestfont](https://clawhub.ai/user/comicsansbestfont)

### License/Terms of Use:

MIT-0

## Use Case:

Agent operators and workspace agents use this skill to refresh HIPPOCAMPUS.md with recent, domain-filtered context, open threads, commitments, and domain sections. It is intended for OpenClaw-style workspaces where agent memory, activity feeds, peer context, and selected operational files are available to the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can gather and persist operational context across listed OpenClaw workspaces, including CRM, family conversation-derived data, journals, cron logs, and peer context.

Mitigation: Install it only where those reads and summaries are intended and acceptable, and review the configured source lists before deployment.

Risk: The decay step can change learning files beyond HIPPOCAMPUS.md by marking pending entries stale and archiving older stale entries.

Mitigation: Review scripts/decay.py before use and run the skill in a version-controlled or otherwise recoverable workspace.

## Reference(s):

- [Agent Domain Registry](references/agent-registry.md)
- [Domain-Specific Section Definitions](references/domain-sections.md)
- [Hippocampus Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, guidance]

**Output Format:** [Markdown file and concise Markdown delivery message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a 14-day rolling, domain-filtered context summary and may run a decay check that updates learning status or archive files.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
