## Description:

Collects a user-confirmed NetEase Cloud Music main playlist, recent-week listening ranking, and all-time listening ranking, then writes local JSONL, CSV, aggregate data, and analysis prompts without performing the profile analysis itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dragonknightk](https://clawhub.ai/user/dragonknightk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent-client users use this skill to organize their own NetEase Cloud Music listening data into local files and reusable AI analysis prompts. It is intended for personal, local data collection from a logged-in desktop client session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts NetEase Cloud Music with a local authenticated debugging port for collection.

Mitigation: Run it only in a trusted local environment and close NetEase Cloud Music after collection to end the debug-enabled session.

Risk: Generated files under outputs/ can contain private playlist and listening-rank data.

Mitigation: Keep the output directory private, do not commit it to public repositories, and share only the files needed for the intended analysis.

Risk: CSV exports may be opened in spreadsheet applications.

Mitigation: Open CSV files cautiously and review them before importing into tools that evaluate formulas or external content.

Risk: Installation and Python dependencies come from external package or marketplace sources.

Mitigation: Prefer pinned or reviewed installation sources and dependencies before running the collection scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dragonknightk/skills/ncm-listening-profile)
- [Project Homepage](https://github.com/dragonknightk/ncm-listening-profile)
- [API Collection Reference](references/api-patterns.md)
- [Environment Reference](references/environment.md)
- [Schema Reference](references/schemas.md)
- [Troubleshooting Reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, local JSONL/CSV/JSON files, diagnostics, and reusable prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under timestamped local run directories and may contain private listening data.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
