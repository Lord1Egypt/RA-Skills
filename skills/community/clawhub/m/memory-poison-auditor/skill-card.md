## Description:

Audits OpenClaw memory files for injected instructions, brand bias, hidden steering, and memory poisoning patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2404589803](https://clawhub.ai/user/2404589803)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit OpenClaw long-term memory files before trusting them for planning, recommendations, or future agent behavior. It helps identify injected instructions, brand steering, suspicious authority claims, and memory blocks that should be reviewed, cleaned, or quarantined.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI review can send suspicious memory excerpts to a configurable external AI service.

Mitigation: Use local scan mode by default and enable --with-ai only when the endpoint and API key are trusted for the memory content being reviewed.

Risk: Cleaning mode can rewrite memory files when clean --apply is used.

Mitigation: Review audit reports manually before applying cleanup and keep the generated backups for recovery.

Risk: Audit results may classify memory as PASS, WARN, or BLOCK based on configured patterns and thresholds.

Mitigation: Treat WARN and BLOCK results as review prompts rather than automatic final decisions for high-impact workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2404589803/skills/memory-poison-auditor)
- [ClawHub publisher profile](https://clawhub.ai/user/2404589803)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Text or JSON audit summaries with PASS, WARN, and BLOCK recommendations; command examples and configuration are documented in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit reports and, when clean --apply is used, creates backups before rewriting suspicious memory blocks.]

## Skill Version(s):

0.1.0 (source: server release metadata, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
