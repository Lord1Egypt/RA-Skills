## Description:

Helps agents manage a user's personal context by recording journal entries, integrating external information, maintaining cognitive connections, refining a minimal knowledge kernel, and generating cognitive maps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build and maintain a personal knowledge base, capture daily judgments, connect external sources to internal reflections, and periodically distill high-value context into a compact kernel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores personal notes, external content, and derived summaries about beliefs and decision patterns.

Mitigation: Use it only in a private workspace, avoid storing secrets or regulated personal data, and periodically review stored files for sensitivity.

Risk: The bundled entropy reduction script can permanently delete notes when run with --force.

Mitigation: Prefer dry-run or report-only use, review every listed file, and create backups before any destructive cleanup.

Risk: Saved external content and inferred cognitive connections can encode misleading or outdated judgments.

Mitigation: Review generated bridge records and minimal-kernel updates before relying on them for future decisions.

## Reference(s):

- [Context Manager on ClawHub](https://clawhub.ai/lj22503/skills/lj22503-context-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown notes, structured local files, reports, and optional shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists personal notes and derived summaries in local data directories; cleanup behavior should be reviewed before destructive use.]

## Skill Version(s):

1.1.0 (source: server release metadata, clawhub.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
