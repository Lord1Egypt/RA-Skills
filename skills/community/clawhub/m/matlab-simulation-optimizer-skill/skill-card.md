## Description:

Audits and optimizes MATLAB simulation programs against a corresponding academic paper or specification while preserving paper-mandated algorithm logic, parameters, metrics, and experiment settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orbisz](https://clawhub.ai/user/orbisz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare MATLAB simulation source code with a paper or specification, fix paper-code mismatches, optimize runtime, and document changes in a Chinese optimization summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly edit MATLAB source files and write reports in the project.

Mitigation: Ask the agent to show a change plan first, review diffs before accepting edits, and run the listed verification commands on representative cases.

Risk: The bundled self-evolution workflow can write diary entries and propose changes to the skill itself.

Mitigation: Remove or ignore the self-evolution section unless explicitly desired, and do not allow installed skill changes without human review.

Risk: Performance optimizations could accidentally change paper-mandated algorithm logic, parameters, stopping criteria, or metrics.

Mitigation: Require the traceability table and summary to identify preserved paper conditions, then compare pre/post results on deterministic reduced-size runs.

## Reference(s):

- [MATLAB 仿真论文对照检查清单](references/matlab-audit-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown summary, MATLAB source edits, traceability tables, verification notes, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes optimization_summary.md by default and may produce matlab_static_scan.json when the bundled static scanner is used.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
