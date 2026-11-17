## Description:

Looks up journal and magazine abbreviations, converts between full names and ISO 4 or MEDLINE abbreviations, and standardizes BibTeX journal fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, authors, editors, and developer agents use this skill to verify journal abbreviations, expand abbreviations, search uncertain journal titles, and standardize BibTeX references before manuscript submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote fallback lookups may share journal names from a manuscript topic with external journal services.

Mitigation: Avoid remote fallback lookups for confidential manuscript topics unless sharing those journal names is acceptable.

Risk: BibTeX processing and cache management can write files locally.

Mitigation: Use dry-run before BibTeX changes and choose explicit output paths carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agents365-ai/skills/journal-abbrev)
- [Publisher profile](https://clawhub.ai/user/agents365-ai)
- [Project homepage](https://github.com/Agents365-ai/journal-abbrev)

## Skill Output:

**Output Type(s):** [guidance, shell commands, text, JSON, files]

**Output Format:** [Markdown guidance with CLI commands; the CLI can return JSON or human-readable text and can write BibTeX output files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Python 3 CLI with local cache management and optional network fallbacks to journal data services.]

## Skill Version(s):

1.0.2 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
