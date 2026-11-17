## Description:

OpenClaw Optimize helps diagnose and tune OpenClaw performance with memory management, skill-loading analysis, history cleanup, monitoring, and troubleshooting tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhmza](https://clawhub.ai/user/zhmza)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose laggy OpenClaw deployments, generate performance reports and configuration snippets, and run memory, skill-loading, and history optimizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic optimization can delete OpenClaw memory/history files.

Mitigation: Run diagnostic or report commands first, back up OpenClaw memory and history files, and avoid --full, --clean-history, and pro auto_optimize until the deletion scope is understood.

Risk: Host-level runtime or cache changes can affect the active environment.

Mitigation: Review commands before execution, do not run with elevated privileges, and run only from a trusted OpenClaw workspace.

Risk: The README archive path is not backed by server-resolved provenance.

Mitigation: Prefer the ClawHub release package; use archive URLs from artifact documentation only after verifying the release source and hash.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhmza/skills/optimize)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python code, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic summaries, optimization plans, performance reports, and commands that modify local OpenClaw memory, history, or runtime state.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
