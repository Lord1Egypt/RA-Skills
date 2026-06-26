## Description: <br>
Use CodexBar CLI local cost usage to summarize per-model usage for Codex or Claude, including the current most recent model or a full model breakdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[landercortazarromero](https://clawhub.ai/user/landercortazarromero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to summarize local CodexBar cost logs by model for Codex or Claude. It supports a current-model view, all-model cost breakdowns, and text or JSON output from CLI, file, or stdin input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CodexBar usage logs and generated summaries may reveal private model usage and cost information. <br>
Mitigation: Run the skill only in environments where local usage and cost data can be viewed, and avoid sharing generated summaries outside the intended audience. <br>
Risk: The skill depends on CodexBar and its Homebrew tap for the default local cost collection path. <br>
Mitigation: Install only if the CodexBar CLI and tap are acceptable for the environment; otherwise provide reviewed JSON through the file or stdin input path. <br>


## Reference(s): <br>
- [CodexBar CLI quick ref](references/codexbar-cli.md) <br>
- [Korta Model Usage on ClawHub](https://clawhub.ai/landercortazarromero/korta-model-usage) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, plus text or JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cost-only per-model summaries; token counts are not split by model in CodexBar output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
