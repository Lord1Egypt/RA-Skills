## Description:

Summarizes per-model Codex or Claude usage costs from local CodexBar cost JSON, including current-model and all-model breakdowns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[landercortazarromero](https://clawhub.ai/user/landercortazarromero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to summarize CodexBar local cost output by current model or by all models for Codex and Claude usage. It supports reviewing existing CodexBar JSON from the CLI, a file, or stdin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on CodexBar reading local Codex or Claude usage logs to compute cost summaries.

Mitigation: Install and run it only where local usage-log access is acceptable.

Risk: The workflow requires a third-party CodexBar Homebrew cask dependency.

Mitigation: Review the CodexBar cask source before installing when that dependency is not already trusted.

## Reference(s):

- [CodexBar CLI quick ref](artifact/references/codexbar-cli.md)
- [Korta Model Usage ClawHub page](https://clawhub.ai/landercortazarromero/skills/korta-model-usage)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Text, JSON]

**Output Format:** [Markdown guidance with bash commands; the bundled script emits plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports provider, mode, model, input, days, format, and pretty-print options.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
