## Description:

Plan reproducible ML experiment runs with explicit parameters, metrics, and artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0x-professor](https://clawhub.ai/user/0x-professor)

### License/Terms of Use:


## Use Case:

Developers and ML engineers use this skill before model training to define tracking-ready experiment plans with datasets, parameters, metrics, thresholds, and expected artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV exports can carry attacker-controlled values that may be opened in spreadsheet software.

Mitigation: Review or sanitize untrusted experiment values before exporting to CSV or opening generated CSV files in spreadsheets.

Risk: The script creates output directories before checking the dry-run flag, so dry-run execution can still affect the filesystem.

Mitigation: Treat --dry-run as a planning marker in output, not as a guarantee of no filesystem changes, until the script behavior is fixed.

Risk: Experiment plans may contain incorrect metrics, thresholds, parameters, or artifact expectations.

Mitigation: Review generated plans against the training objective and tracking policy before using them for model runs.

## Reference(s):

- [Tracking Guide](references/tracking-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/0x-professor/skills/ml-experiment-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON, Markdown, or CSV experiment-plan files produced by the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reads an optional JSON experiment definition and writes a local output artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
