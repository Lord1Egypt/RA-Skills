## Description:

Li Etl Handle Safe helps agents read, write, clean, transform, sort, filter, deduplicate, and merge Excel and CSV spreadsheet data without arbitrary code execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform local spreadsheet ETL work on Excel and CSV files, including reading, writing, cleaning, type conversion, filtering, sorting, deduplication, and merging. It is suited to routine data-preparation workflows where file paths are trusted and spreadsheet backups are maintained.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lockfile uses unsecured third-party HTTP dependency URLs despite the artifact documentation claiming official HTTPS npm sources.

Mitigation: Review dependencies before installation, refresh the lockfile from approved HTTPS package sources, and prefer a release with corrected package provenance.

Risk: Spreadsheet write operations lack clearly documented overwrite safeguards.

Mitigation: Use the skill only on trusted file paths, keep backups of important spreadsheets, and require callers to choose output paths deliberately before writing.

Risk: Spreadsheet cleaning, row deletion, deduplication, and CSV export can unintentionally change data.

Mitigation: Run transformations on copies first, inspect results before replacing source files, and document formula-safe CSV export expectations for downstream spreadsheet use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-etl-handle-safe)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JavaScript examples and generated Excel or CSV files when file-writing functions are used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file operations depend on caller-supplied paths and options.]

## Skill Version(s):

1.0.2 (source: evidence release metadata, package.json, skill.yaml, and SKILL.md version text)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
