## Description:

Phy I18n Audit helps developers audit multi-locale codebases for missing, untranslated, empty, and orphaned localization keys across JSON, YAML, PO/POT, and ARB files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect translation coverage across application locale files, identify missing or stale localization keys, and prepare CI-oriented follow-up commands or scaffold content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The suggested CI command can run an unpinned third-party npm package.

Mitigation: Prefer the local Python snippets or replace the command with a reviewed, pinned, lockfile-backed dependency before using it in CI.

Risk: Audit results may need manual adjustment for POT files, namespace layouts, scaffold generation, and template-impact ranking.

Mitigation: Review generated reports, scaffold content, and priority rankings before enforcing thresholds or sending localization work to translators.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-i18n-audit)
- [Canlah AI homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown report with code blocks and optional scaffold JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CI fail-gate commands, per-locale coverage summaries, and generated translation scaffold content.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
