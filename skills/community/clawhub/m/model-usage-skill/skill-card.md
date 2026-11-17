## Description:

Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current model or a full model breakdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justasknudge](https://clawhub.ai/user/justasknudge)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to inspect local CodexBar cost data, identify current or historical per-model spend for Codex or Claude, and produce text or JSON usage summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CodexBar reads local Codex and Claude usage logs to calculate costs.

Mitigation: Use the skill only where that local log access is acceptable; supply a reviewed JSON file or stdin input when tighter control over the analyzed data is needed.

Risk: The documented install path uses a third-party Homebrew cask for CodexBar.

Mitigation: Review the cask source and CodexBar installation path before installing in sensitive environments.

## Reference(s):

- [Model Usage Skill on ClawHub](https://clawhub.ai/justasknudge/skills/model-usage-skill)
- [justasknudge publisher profile](https://clawhub.ai/user/justasknudge)
- [CodexBar CLI quick reference](artifact/references/codexbar-cli.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; script output is plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost-only per-model summaries; token counts are not split by model in CodexBar cost output.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
