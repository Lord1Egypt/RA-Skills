## Description:

Analyze code-change blast radius with the impact CLI. Use when reviewing diffs, assessing merge or deployment risk, finding affected tests, diffing public contracts, visualizing callers, detecting orphan code, or writing PR/MR impact summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albert-lv](https://clawhub.ai/user/albert-lv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use the impact CLI to review repository changes, identify affected tests and callers, inspect public contract changes, and prepare pull request or merge request impact summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions received a low confidence persistence warning, and some local references could not be resolved.

Mitigation: Review the install instructions and decide whether to install the tool in `~/.local/bin`; inspect or resolve the missing references before relying on the setup.

## Reference(s):

- [Impact Analyzer project](https://github.com/nano-harness/impact-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Text analysis, JSON results, compact LLM context, and Markdown PR/MR impact summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are review guidance; validate findings with business context and relevant tests.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
