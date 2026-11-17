## Description:

Extract a structured Hong Kong IPO snapshot with company fields, offer mechanics, timing, source provenance, and field-level quality signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackstoic](https://clawhub.ai/user/hackstoic)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to extract normalized single-symbol Hong Kong IPO facts before summarizing, scoring, or making downstream comparisons. It is intended for read-only snapshot extraction, with quality fields that help users treat partial or conflicting source data cautiously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled runtime includes broader stateful financial workflows beyond snapshot extraction.

Mitigation: Use the documented snapshot command for read-only extraction and review any score, decision-card, review, or apply-suggestions workflow before relying on it.

Risk: The runtime may write local profile, watchlist, review, or suggestion state.

Mitigation: Set HKIPO_HOME to an isolated directory before running the bundled CLI.

Risk: IPO source data may be partial, degraded, or conflicting.

Mitigation: Check issues, quality.missing_fields, quality.conflicts, quality.overall_confidence, and meta.data_status before making strong claims.

Risk: Financial scoring or decision outputs can be mistaken for investment advice.

Mitigation: Treat score and decision-card outputs as review aids and verify conclusions with independent financial analysis.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hackstoic/skills/hkipo-snapshot-extractor)
- [Skill Instructions](artifact/SKILL.md)
- [hkipo-next README](artifact/runtime/hkipo-next/README.md)
- [AiPO API Documentation](artifact/runtime/hkipo-next/references/aipo-api.md)
- [IPO Analysis Guide](artifact/runtime/hkipo-next/references/analysis-guide.md)
- [API Guide](artifact/runtime/hkipo-next/references/api-guide.md)
- [Hong Kong IPO Mechanism Guide](artifact/runtime/hkipo-next/references/ipo-mechanism.md)
- [Risk Preference Types](artifact/runtime/hkipo-next/references/risk-preferences.md)
- [AiPO Data Source](https://aipo.myiqdii.com)
- [AASTOCKS IPO Data Source](https://www.aastocks.com/tc/stocks/market/ipo/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON, Markdown, or text generated from CLI-backed IPO snapshot data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshot outputs include field sources, missing fields, conflicts, confidence signals, and degraded or partial data status where applicable.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, pyproject.toml, and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
