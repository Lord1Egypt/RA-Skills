## Description:

Analyze and reclaim macOS disk space through intelligent cleanup recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wusuiling-if](https://clawhub.ai/user/wusuiling-if)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to diagnose macOS storage usage, identify safe cleanup candidates, and prepare user-confirmed cleanup actions for caches, application remnants, large files, and development tooling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup workflows can permanently remove useful user or system data if deletion guidance is followed too casually.

Mitigation: Prefer preview-only analysis, Finder Trash or backups, and exact per-item deletion only after the user understands the impact.

Risk: Broad deletion commands or Docker prune workflows can remove valuable caches, stopped containers, or database volumes.

Mitigation: List every cleanup target, inspect Docker objects and database volumes individually, and require explicit confirmation for each risky item.

Risk: Commands that require sudo or broad filesystem access increase the impact of a mistake.

Mitigation: Keep analysis read-only by default, avoid unattended sudo cleanup, and ask the user to run only reviewed commands.

## Reference(s):

- [macOS Cleanup Targets Reference](references/cleanup_targets.md)
- [Mole Integration Guide](references/mole_integration.md)
- [Safety Rules for macOS Cleanup](references/safety_rules.md)
- [Mole](https://github.com/tw93/Mole)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown reports with inline shell commands and optional text or JSON summaries from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleanup recommendations should be previewed, explained, and confirmed by the user before deletion.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
