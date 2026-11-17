## Description:

Performs a 6-dimension memory health check assessing integrity, freshness, bloat, orphans, duplicates, and coverage with optional auto-repair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chongjie-ran](https://clawhub.ai/user/chongjie-ran)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to assess local memory stores for integrity issues, staleness, bloat, orphaned files, duplicates, and coverage gaps, then review generated reports and repair recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repair mode can permanently delete local memory files without the interactive confirmation implied by the documentation.

Mitigation: Run dry-run or diagnostic-only modes first, keep a backup of the OpenClaw memory workspace, and avoid auto-repair or orphan-removal options until the files to be removed have been reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chongjie-ran/skills/memory-health-check)
- [README](artifact/README.md)
- [Design document](artifact/DESIGN.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text, JSON reports, Markdown documentation, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health reports are written under the local OpenClaw memory workspace; repair options may modify or delete local memory files.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
