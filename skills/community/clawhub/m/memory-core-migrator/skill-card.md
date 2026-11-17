## Description:

Safely migrates OpenClaw memory from LanceDB Pro, official LanceDB list captures, QMD, or Markdown into memory-core. Use when an owner asks to migrate, audit, deduplicate, benchmark, cut over, or roll back an OpenClaw memory backend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airbing11](https://clawhub.ai/user/airbing11)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw owners and operators use this skill to migrate memory from supported LanceDB, QMD, or Markdown sources into memory-core, and to audit, benchmark, stage, cut over, or roll back the migration with reviewable evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial: 18 of 26 components were fully scanned, and confidence is medium, so some behavior remains uncertain.

Mitigation: Review the included source and begin with synthetic fixtures or a copied export; require a verified backup and run-bound approval before production writes.

Risk: Memory exports, reports, backups, and logs may contain private conversations, personal data, or credentials.

Mitigation: Keep run artifacts in restricted local storage, redact secret-like metadata, and do not publish raw exports or reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airbing11/skills/memory-core-migrator)
- [Compatibility guide](references/compatibility.md)
- [Operations guide](references/operations.md)
- [Benchmark methodology](docs/benchmark-methodology.md)
- [Operator FAQ](docs/faq.md)
- [Operator recipes](docs/recipes.md)

## Skill Output:

**Output Type(s):** [Shell commands, JSON/JSONL, Markdown, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions with shell commands, JSON/JSONL manifests and audit reports, and staged Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; production writes require explicit application and run-bound approval.]

## Skill Version(s):

0.1.0-rc.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
