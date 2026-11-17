## Description:

Post-mortem analysis for AI agent failures that captures workspace state, reconstructs timelines, and identifies likely root causes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Incident Replay to capture before and after workspace snapshots, compare file changes, detect incident triggers, reconstruct timelines, and generate post-mortem reports for AI agent failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can copy broad workspace file contents into persistent local incident data.

Mitigation: Set a narrow WORKSPACE_ROOT, exclude secrets and unrelated projects, and review generated snapshots and reports before sharing or committing them.

Risk: Snapshot data may include credentials, logs, agent memory, or other sensitive local files if configured too broadly.

Mitigation: Aggressively configure EXCLUDE_PATTERNS for secrets, credentials, logs, agent memory, generated incident data, and any files outside the intended investigation scope.

Risk: Workspaces writable by untrusted users can affect what the forensic snapshot captures.

Mitigation: Run the tool only in trusted local workspaces and avoid using it in shared or untrusted writable directories.

Risk: Root cause classification is heuristic and cannot prove causation.

Mitigation: Treat classifications and remediation as investigative guidance, then verify findings with human review before taking corrective action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/incident-replay)
- [README](README.md)
- [Limitations](LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON incident reports, JSON snapshots, and command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent local incident data and reports under the configured data directory.]

## Skill Version(s):

1.0.6 (source: server release; artifact frontmatter remains 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
