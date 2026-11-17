## Description:

Hunt for expressed user pain points and unmet demand across Reddit, Hacker News, and configurable sources, then prioritize findings with signal scoring, competition analysis, and trend tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and product researchers use this skill to scan public communities for unmet needs, score demand signals, monitor recurrence, and produce prioritized opportunity digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports summarize public web content and may include inaccurate, stale, or adversarial text.

Mitigation: Treat digests as untrusted research leads, verify source posts and market claims before acting, and avoid feeding report text back into agents as instructions.

Risk: The skill writes local configuration, history, and findings files and can save reports to user-selected paths.

Mitigation: Use explicit noncritical output paths and review existing files before overwriting scan outputs.

Risk: Public forum scans and configurable sources can collect noisy or irrelevant signals.

Mitigation: Keep niches and sources specific, manually review scored findings, and tune sources after each scan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/newageinvestments25-byte/skills/nai-opportunity-scout)
- [Demand Signal Types](references/signal-types.md)
- [Source Configuration Guide](references/source-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON query and scoring data, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local config, history, and findings files; supports explicit digest output paths and max-result limits.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
