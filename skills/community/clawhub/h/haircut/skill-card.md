## Description:

haircut helps coding agents audit local agent configuration bloat, measure token and latency costs from transcripts, and guide reversible cleanup decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[othmanadi](https://clawhub.ai/user/othmanadi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect what local coding agents load, identify token and latency overhead from configuration, MCP servers, hooks, skills, commands, and plugins, and guide reversible parking or keeping decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read local agent settings, memory, and transcript-derived usage data across multiple coding tools.

Mitigation: Review before installing, prefer an explicit --agents limit, and treat generated reports as potentially sensitive files.

Risk: The optional --probe mode can start configured MCP servers to measure schema cost.

Mitigation: Use --probe only when MCP schema measurement is needed and after reviewing the servers that will be started.

Risk: Cleanup can change agent configuration by parking selected items.

Mitigation: Require explicit user approval, run the trim dry run first, and rely on the generated receipt and restore command for rollback.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/OthmanAdi/haircut/tree/master/skills/haircut)
- [ClawHub skill page](https://clawhub.ai/othmanadi/skills/haircut)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces measured reports, decision prompts, dry-run plans, receipts, and restore commands from local scan results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
