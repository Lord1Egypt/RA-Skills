## Description:

Safe OpenClaw config planning/apply workflow with bilingual execution receipts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edmond-ai](https://clawhub.ai/user/edmond-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use OC Guard to plan, review, validate, and apply OpenClaw configuration changes with explicit receipts, backup, rollback, and confirmation gates for high-risk changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect high-impact OpenClaw configuration, including agent, tool, plugin, channel, and gateway behavior.

Mitigation: Run apply operations only by someone authorized to change OpenClaw behavior, review proposals first, and require explicit confirmation for high-risk changes.

Risk: Natural-language requirements and generated receipts or temporary files may contain sensitive configuration details.

Mitigation: Prefer reviewed local JSON proposal files, avoid including secrets in natural-language requests or parent-object changes, and treat /tmp/oc-guard-* files and receipts as sensitive.

Risk: The security verdict is suspicious due to under-scoped external AI use and unsafe local artifact storage.

Mitigation: Review before installing, scan the package before deployment, and validate redaction and temporary-file handling in the target environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edmond-ai/skills/oc-guard)
- [README](README.md)
- [Safety notes](docs/SAFETY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Bilingual execution receipts, Markdown guidance, shell commands, and JSON proposal files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, openclaw, and opencode; high-risk apply operations require explicit confirmation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
