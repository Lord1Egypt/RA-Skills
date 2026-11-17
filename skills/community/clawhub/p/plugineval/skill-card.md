## Description:

PluginEval Quality Evaluation with enhanced UI. Wraps plugineval-core with vetting and reporting features. Requires plugineval-core.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donmeusi](https://clawhub.ai/user/donmeusi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use PluginEval to vet OpenClaw skills before installation or publication by combining security checks, quality evaluation, anti-pattern detection, and report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The main workflow depends on unpinned external code.

Mitigation: Install only trusted and pinned releases of plugineval-core and verify dependency provenance before use.

Risk: Standalone setup can copy external scripts into PATH.

Mitigation: Review copied scripts before adding them to PATH and limit execution to trusted local environments.

## Reference(s):

- [PluginEval ClawHub page](https://clawhub.ai/donmeusi/skills/plugineval)
- [External dependencies](EXTERNAL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports depend on plugineval-core and local workspace evaluation scripts.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
