## Description: <br>
Extracts a structured Hong Kong IPO snapshot with company fields, offer mechanics, timing, source provenance, and field-level quality signals for one IPO symbol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackstoic](https://clawhub.ai/user/hackstoic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch normalized facts for a single Hong Kong IPO symbol before analysis, scoring, or a human summary. It is most useful when machine-readable IPO data and field-level quality cues are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as read-only snapshot extraction, but the bundled runtime also includes scoring, decision workflows, profile and watchlist management, and persistent local state. <br>
Mitigation: Review commands before execution, run only the snapshot command for read-only use, and set HKIPO_HOME to an isolated directory if using stateful features. <br>
Risk: Decision-support and scoring outputs could be mistaken for investment advice. <br>
Mitigation: Treat generated scores or participation recommendations as analytical inputs only; require human review and independent source checks before acting. <br>
Risk: IPO source data may be partial, degraded, stale, or conflicting. <br>
Mitigation: Check issues, field_sources, quality.missing_fields, quality.conflicts, and quality.overall_confidence before making strong claims. <br>


## Reference(s): <br>
- [HK IPO Snapshot Extractor on ClawHub](https://clawhub.ai/hackstoic/hkipo-snapshot-extractor) <br>
- [AiPO API Documentation](runtime/hkipo-next/references/aipo-api.md) <br>
- [API Guide](runtime/hkipo-next/references/api-guide.md) <br>
- [Analysis Guide](runtime/hkipo-next/references/analysis-guide.md) <br>
- [IPO Mechanism Reference](runtime/hkipo-next/references/ipo-mechanism.md) <br>
- [Risk Preferences Reference](runtime/hkipo-next/references/risk-preferences.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON, Markdown, or plain text snapshot output; optional exported Markdown files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes field_sources, issues, quality.missing_fields, quality.conflicts, quality.overall_confidence, and degraded or partial data status indicators when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, pyproject.toml, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
