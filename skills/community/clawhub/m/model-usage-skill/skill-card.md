## Description: <br>
Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current model or a full model breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JustAskNudge](https://clawhub.ai/user/JustAskNudge) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to summarize local CodexBar cost logs by model for Codex or Claude, including the most recent model or a full model cost breakdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local CodexBar cost data, which may reflect sensitive local usage patterns. <br>
Mitigation: Install only from a trusted CodexBar CLI source and review raw CodexBar JSON or local session logs before sharing them. <br>
Risk: Summaries are limited by CodexBar cost JSON fields and do not split token counts by model. <br>
Mitigation: Use the output for cost analysis and confirm token-level conclusions against the underlying CodexBar data. <br>


## Reference(s): <br>
- [CodexBar CLI quick ref](references/codexbar-cli.md) <br>
- [ClawHub skill page](https://clawhub.ai/JustAskNudge/model-usage-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Text or JSON summaries with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost-only per-model summaries; token counts are not split by model in CodexBar output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
