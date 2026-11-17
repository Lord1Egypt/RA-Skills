## Description:

Apply high-fidelity localization to structured artifacts such as web apps, docs, PDFs, slide decks, Office files, subtitles, code repositories, and game assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuki61256-cell](https://clawhub.ai/user/yuki61256-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, localization engineers, and content teams use this skill to translate structured artifacts while preserving layout, placeholders, stable identifiers, encoding, and delivery safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation workflows may lead an agent to run install, build, test, lint, or render commands from user-provided artifacts.

Mitigation: Require review of exact commands first and run them in an isolated environment without sensitive credentials.

Risk: Structured translation can damage layout, placeholders, stable identifiers, encoding, or file relationships if scope is not protected.

Mitigation: Use the documented boundaries, format checklists, and quality gates before handoff, and report skipped content or residual fidelity risk.

## Reference(s):

- [Workflow](references/workflow.md)
- [Decision Thresholds](references/decision-thresholds.md)
- [Artifact Pipelines](references/artifact-pipelines.md)
- [Translation Boundaries](references/translation-boundaries.md)
- [Format Risk Checklists](references/format-risk-checklists.md)
- [Locale-Sensitive Typography](references/locale-sensitive-typography.md)
- [Quality Gates](references/quality-gates.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Localized artifacts or repositories plus Markdown status, validation, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes protected or skipped items and any remaining fidelity risk.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
