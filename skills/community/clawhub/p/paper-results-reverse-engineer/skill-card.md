## Description:

Paper Results Reverse Engineer helps agents deconstruct Results sections from psychology papers using study-profile-first classification, adaptive analysis branches, source verification, causal-language guardrails, and file-first Markdown reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin77-chris](https://clawhub.ai/user/bin77-chris)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and students use this skill to analyze psychology paper Results sections, uploaded PDFs, figure captions, screenshots, or partial excerpts. It produces structured reverse-engineering notes, figure and table explanations, evidence-boundary checks, presentation support, and optional writer-transfer guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags under-scoped local command and file-handling instructions for PDFs and temporary outputs.

Mitigation: Review before installing; prefer uploaded PDFs or pasted Results text, avoid arbitrary filesystem paths, and require shell-free or tightly reviewed PDF handling.

Risk: PDF processing may read local files or leave temporary analysis artifacts.

Mitigation: Use private per-run temporary files, sanitized filenames, confirmation before cleanup or deletion, and the artifact's file-first output and cleanup verification rules.

Risk: Paper analysis can introduce unsupported claims, fabricated statistics, causal overclaims, or copied target-paper content.

Mitigation: Apply source verification against the original paper text, causal-language guardrails, anti-template-contamination checks, and Module H limits that abstract writing patterns without copying original sentences or statistics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin77-chris/skills/paper-results-reverse-engineer)
- [README](README.md)
- [Changelog](CHANGELOG.md)
- [Execution constraints](docs/execution-constraints.md)
- [Source verification](docs/source-verification.md)
- [Causal language guardrails](docs/causal-language-guardrails.md)
- [Module H writer transfer specification](docs/module-h-spec.md)
- [Prompt templates](references/prompt-templates.md)
- [Function labels](references/function-labels.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [File-first Markdown analysis with concise chat summaries and optional inline command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports quick, standard, close-reading, and Module H writer-transfer modes; default output is a local Markdown file with path, core findings, self-check, and manual-review items summarized in chat.]

## Skill Version(s):

3.0.4 (source: frontmatter, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
